
# Usar la imagen oficial de Airflow
FROM apache/airflow:3.0.1

# Cambiar a usuario root para instalar paquetes del sistema
USER root

# Instalar dependencias del sistema necesarias
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        python3-dev \
        build-essential \
        curl \
        wget \
        vim \
        git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Cambiar de vuelta al usuario airflow
USER airflow

# Copiar el archivo de requirements si existe
COPY requirements.txt /tmp/requirements.txt

# Instalar dependencias de Python adicionales
RUN pip install --no-cache-dir --user \
    # Conectores para bases de datos
    #psycopg2-binary \
    #pymongo \
    #sqlalchemy \
    # Librerías para manejo de datos
    #pandas \
    #numpy \
    #scikit-learn \
    # Librerías para APIs y requests
    #requests \
    #boto3 \
    # Librerías para procesamiento de video (si las necesitas)
    #opencv-python-headless \
    #pillow \
    # Airflow providers adicionales
    apache-airflow-providers-postgres \
    apache-airflow-providers-mongo \
    apache-airflow-providers-http \
    # Otras dependencias comunes
    #python-dotenv \
    #pydantic \
    # Si tienes un requirements.txt, instalarlo
    && if [ -f /tmp/requirements.txt ]; then pip install --no-cache-dir --user -r /tmp/requirements.txt; fi


# Establecer variables de entorno para tu proyecto

ENV PROJECT_ROOT="/opt/airflow/"
ENV PYTHONPATH="${PYTHONPATH}:/opt/airflow/dags"
# Crear un script de entrada personalizado
COPY --chown=airflow:root entrypoint.sh /opt/airflow/custom-entrypoint.sh
RUN chmod +x /opt/airflow/custom-entrypoint.sh

# El usuario debe ser airflow para el funcionamiento correcto
USER airflow

# Exponer puertos necesarios
EXPOSE 8080

# Usar el entrypoint por defecto de Airflow
ENTRYPOINT ["/entrypoint"]