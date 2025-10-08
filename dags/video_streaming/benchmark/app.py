import streamlit as st
from benchmark import run_benchmark
from dotenv import load_dotenv
from pathlib import Path
import logging
import os
import plotly.graph_objects as go
import pandas as pd

# Load env
load_dotenv()

# Setup logging
base_dir = Path(__file__).parent
log_dir = base_dir / 'logs'
log_dir.mkdir(exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    filename=log_dir / 'app.log',
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s'
)

st.set_page_config(page_title="DB Benchmark", page_icon="📊", layout="wide")

st.title("📊 Database Benchmark: CSV vs JSON in RDBMS and NoSQL")

st.markdown("""
Este benchmark compara el **rendimiento de inserción, indexación, consultas y actualizaciones** entre:
- **RDBMS (PostgreSQL)** con CSV y JSONB  
- **NoSQL (MongoDB)** con CSV y JSON nativo

### Operaciones probadas:
1. **Insert**: Inserción masiva de registros
2. **Index Creation**: Creación de índices optimizados
3. **Flat Query**: Consulta simple (`age > 30`)
4. **Nested Query**: Consulta en campos anidados (`hobbies contains 'sports'`)
5. **Complex Query**: Agregación con filtros, agrupación y ordenamiento
6. **Update**: Actualización masiva de registros

👉 Selecciona el tamaño de datos y ejecuta el benchmark.
""")

# Configuración en sidebar
with st.sidebar:
    st.header("⚙️ Configuración")
    n = st.slider(
        "Tamaño de datos (registros)", 
        min_value=1000, 
        max_value=50000, 
        value=5000, 
        step=1000
    )
    
    st.info(f"""
    **Registros seleccionados:** {n:,}
    
    **Nota:** Datasets más grandes mostrarán 
    diferencias más pronunciadas entre 
    las bases de datos.
    """)
    
    show_table = st.checkbox("Mostrar tabla de resultados", value=True)
    show_comparison = st.checkbox("Mostrar comparación porcentual", value=True)

# Botón principal
if st.button("🚀 Ejecutar Benchmark", type="primary"):
    with st.spinner("Ejecutando benchmark... Esto puede tomar un momento..."):
        try:
            results = run_benchmark(n)
            st.success("✅ Benchmark completado exitosamente!")
            
            # Guardar en session state
            st.session_state['results'] = results
            st.session_state['n'] = n
            
        except Exception as e:
            st.error(f"❌ Error al ejecutar el benchmark: {str(e)}")
            logging.error(f"Benchmark error: {e}")

# Mostrar resultados si existen
if 'results' in st.session_state:
    results = st.session_state['results']
    n = st.session_state['n']
    
    # Tabs para organizar la visualización
    tab1, tab2, tab3 = st.tabs(["📈 Gráficas", "📊 Tablas", "🔍 Análisis"])
    
    with tab1:
        # Split DB types
        db_types = {
            "RDBMS (PostgreSQL)": ["RDBMS_CSV", "RDBMS_JSON"],
            "NoSQL (MongoDB)": ["NoSQL_CSV", "NoSQL_JSON"]
        }
        
        for db, keys in db_types.items():
            st.subheader(f"📌 {db}")
            
            # Preparar datos
            operations = list(results[keys[0]].keys())
            
            # Gráfica de barras agrupadas
            fig = go.Figure()
            
            colors = {'RDBMS_CSV': '#636EFA', 'RDBMS_JSON': '#EF553B', 
                     'NoSQL_CSV': '#00CC96', 'NoSQL_JSON': '#AB63FA'}
            
            for k in keys:
                fig.add_trace(go.Bar(
                    x=operations,
                    y=[results[k][op] for op in operations],
                    name=k.replace('_', ' '),
                    text=[f"{results[k][op]:.4f}s" for op in operations],
                    textposition="auto",
                    marker_color=colors.get(k, '#FFA15A')
                ))
            
            fig.update_layout(
                title=f"{db} - Benchmark con {n:,} registros",
                xaxis_title="Operación",
                yaxis_title="Tiempo (segundos)",
                barmode="group",
                template="plotly_dark",
                height=500,
                hovermode='x unified'
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("---")
    
    with tab2:
        if show_table:
            st.subheader("📋 Resultados Detallados")
            
            # Crear DataFrame
            df_data = []
            for db_type, config in [('RDBMS', 'CSV'), ('RDBMS', 'JSON'), 
                                   ('NoSQL', 'CSV'), ('NoSQL', 'JSON')]:
                key = f"{db_type}_{config}"
                for op, time_val in results[key].items():
                    df_data.append({
                        'Base de Datos': db_type,
                        'Formato': config,
                        'Operación': op,
                        'Tiempo (s)': round(time_val, 6)
                    })
            
            df = pd.DataFrame(df_data)
            
            # Tabla con estilo
            st.dataframe(
                df.pivot_table(
                    values='Tiempo (s)', 
                    index='Operación', 
                    columns=['Base de Datos', 'Formato']
                ).style.format("{:.6f}").background_gradient(cmap='RdYlGn_r'),
                use_container_width=True
            )
            
            # Exportar CSV
            csv = df.to_csv(index=False)
            st.download_button(
                label="📥 Descargar resultados (CSV)",
                data=csv,
                file_name=f"benchmark_results_{n}_records.csv",
                mime="text/csv"
            )
    
    with tab3:
        if show_comparison:
            st.subheader("🔍 Análisis Comparativo")
            
            # Comparaciones clave
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### 🏆 Ganador por Operación")
                
                operations = list(results['RDBMS_CSV'].keys())
                for op in operations:
                    times = {
                        'RDBMS CSV': results['RDBMS_CSV'][op],
                        'RDBMS JSON': results['RDBMS_JSON'][op],
                        'NoSQL CSV': results['NoSQL_CSV'][op],
                        'NoSQL JSON': results['NoSQL_JSON'][op]
                    }
                    winner = min(times, key=times.get)
                    winner_time = times[winner]
                    
                    st.metric(
                        label=op.replace('_', ' ').title(),
                        value=winner,
                        delta=f"{winner_time:.6f}s"
                    )
            
            with col2:
                st.markdown("### 📊 Diferencias Porcentuales")
                
                st.markdown("**RDBMS: CSV vs JSON**")
                for op in operations:
                    csv_time = results['RDBMS_CSV'][op]
                    json_time = results['RDBMS_JSON'][op]
                    diff = ((json_time - csv_time) / csv_time) * 100
                    
                    st.metric(
                        label=op.replace('_', ' ').title(),
                        value=f"{abs(diff):.2f}%",
                        delta="JSON más rápido" if diff < 0 else "CSV más rápido",
                        delta_color="normal" if diff < 0 else "inverse"
                    )
                
                st.markdown("---")
                st.markdown("**NoSQL: CSV vs JSON**")
                for op in operations:
                    csv_time = results['NoSQL_CSV'][op]
                    json_time = results['NoSQL_JSON'][op]
                    diff = ((json_time - csv_time) / csv_time) * 100
                    
                    st.metric(
                        label=op.replace('_', ' ').title(),
                        value=f"{abs(diff):.2f}%",
                        delta="JSON más rápido" if diff < 0 else "CSV más rápido",
                        delta_color="normal" if diff < 0 else "inverse"
                    )
            
            # Insight general
            st.markdown("---")
            st.markdown("### 💡 Insights")
            
            # Calcular totales
            total_rdbms_csv = sum(results['RDBMS_CSV'].values())
            total_rdbms_json = sum(results['RDBMS_JSON'].values())
            total_nosql_csv = sum(results['NoSQL_CSV'].values())
            total_nosql_json = sum(results['NoSQL_JSON'].values())
            
            fastest = min([
                ('RDBMS CSV', total_rdbms_csv),
                ('RDBMS JSON', total_rdbms_json),
                ('NoSQL CSV', total_nosql_csv),
                ('NoSQL JSON', total_nosql_json)
            ], key=lambda x: x[1])
            
            st.success(f"""
            **Configuración más rápida (tiempo total):** {fastest[0]} 
            con {fastest[1]:.4f} segundos
            """)
            
            st.info("""
            **Observaciones clave:**
            - MongoDB generalmente es más rápido en **inserciones** debido a su arquitectura sin esquema
            - PostgreSQL sobresale en **consultas complejas** gracias a su optimizador de queries
            - El formato **JSON nativo** en MongoDB tiene ventaja en operaciones con arrays
            - Los **índices GIN** de PostgreSQL mejoran significativamente las búsquedas en JSONB
            """)

else:
    st.info("👆 Haz clic en 'Ejecutar Benchmark' para comenzar")