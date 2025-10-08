import time
import logging
import psycopg2
import psycopg2.extras
import json
import csv
from pymongo import MongoClient, ASCENDING
from pathlib import Path
from data_generator import generate_data
import os
import plotly.graph_objects as go


def timed_execution(func, *args, **kwargs):
    """Helper to time execution of a function."""
    start = time.perf_counter()
    result = func(*args, **kwargs)
    elapsed = time.perf_counter() - start
    return result, elapsed


def run_benchmark(n: int):
    logging.info(f"Starting benchmark for n={n}")

    # Directories
    base_dir = Path(__file__).parent
    data_dir = base_dir / 'data'
    data_dir.mkdir(exist_ok=True)

    # Generate data
    csv_path, json_path = generate_data(n, data_dir)

    # DB connections
    try:
        pg_conn = psycopg2.connect(
            host="localhost",
            dbname=os.environ['POSTGRES_DB'],
            user=os.environ['POSTGRES_USER'],
            password=os.environ['POSTGRES_PASSWORD']
        )
        pg_conn.autocommit = False  # Control manual de transacciones
        
        mongo_client = MongoClient(
            f"mongodb://{os.environ['MONGO_USER']}:{os.environ['MONGO_PASSWORD']}@localhost:27017/{os.environ['MONGO_DB']}?authSource=admin"
        )
        mongo_db = mongo_client[os.environ['MONGO_DB']]
    except Exception as e:
        logging.error(f"Database connection error: {e}")
        raise

    results = {}

    try:
        # -------------------------
        # PostgreSQL (RDBMS) - CSV
        # -------------------------
        logging.info("Starting PostgreSQL CSV benchmark...")
        with pg_conn.cursor() as cur:
            cur.execute("DROP TABLE IF EXISTS csv_table")
            cur.execute("""
                CREATE TABLE csv_table (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    age INTEGER NOT NULL,
                    city TEXT NOT NULL,
                    hobbies TEXT NOT NULL
                )
            """)
            pg_conn.commit()

        # Insert with COPY (más rápido para CSV)
        def insert_csv_pg():
            with pg_conn.cursor() as cur, open(csv_path, 'r', encoding='utf-8') as f:
                cur.copy_expert(
                    "COPY csv_table (id, name, age, city, hobbies) FROM STDIN WITH CSV HEADER",
                    f
                )
                pg_conn.commit()

        _, insert_time = timed_execution(insert_csv_pg)

        # Crear índices después de la inserción (más eficiente)
        def create_indexes_csv():
            with pg_conn.cursor() as cur:
                cur.execute("CREATE INDEX idx_csv_age ON csv_table(age)")
                cur.execute("CREATE INDEX idx_csv_city ON csv_table(city)")
                pg_conn.commit()
        
        _, index_time = timed_execution(create_indexes_csv)

        # Queries
        _, flat_query_time = timed_execution(
            lambda: pg_conn.cursor().execute("SELECT COUNT(*) FROM csv_table WHERE age > 30")
        )
        
        _, nested_query_time = timed_execution(
            lambda: pg_conn.cursor().execute("SELECT COUNT(*) FROM csv_table WHERE hobbies LIKE '%sports%'")
        )
        
        # Query compleja con JOIN simulado
        _, complex_query_time = timed_execution(
            lambda: pg_conn.cursor().execute("""
                SELECT city, AVG(age) as avg_age, COUNT(*) as count
                FROM csv_table
                WHERE age > 25 AND hobbies LIKE '%sports%'
                GROUP BY city
                ORDER BY avg_age DESC
            """)
        )
        
        # Update test
        def update_csv():
            with pg_conn.cursor() as cur:
                cur.execute("UPDATE csv_table SET age = age + 1 WHERE city = 'New York'")
                pg_conn.commit()
        
        _, update_time = timed_execution(update_csv)

        results['RDBMS_CSV'] = {
            'insert': insert_time,
            'index_creation': index_time,
            'flat_query': flat_query_time,
            'nested_query': nested_query_time,
            'complex_query': complex_query_time,
            'update': update_time
        }

        # -------------------------
        # PostgreSQL (RDBMS) - JSON
        # -------------------------
        logging.info("Starting PostgreSQL JSON benchmark...")
        with open(json_path, 'r', encoding='utf-8') as f:
            data_json = json.load(f)

        with pg_conn.cursor() as cur:
            cur.execute("DROP TABLE IF EXISTS json_table")
            cur.execute("""
                CREATE TABLE json_table (
                    id SERIAL PRIMARY KEY,
                    data JSONB NOT NULL
                )
            """)
            pg_conn.commit()

        # Insert optimizado con execute_batch
        def insert_json_pg():
            with pg_conn.cursor() as cur:
                psycopg2.extras.execute_batch(
                    cur,
                    "INSERT INTO json_table (data) VALUES (%s)",
                    [(json.dumps(doc),) for doc in data_json],
                    page_size=1000
                )
                pg_conn.commit()

        _, insert_time = timed_execution(insert_json_pg)

        # Crear índices GIN para JSONB (crucial para performance)
        def create_indexes_json():
            with pg_conn.cursor() as cur:
                cur.execute("CREATE INDEX idx_json_data ON json_table USING GIN (data)")
                cur.execute("CREATE INDEX idx_json_age ON json_table ((data->>'age'))")
                cur.execute("CREATE INDEX idx_json_hobbies ON json_table USING GIN ((data->'hobbies'))")
                pg_conn.commit()
        
        _, index_time = timed_execution(create_indexes_json)

        # Queries
        _, flat_query_time = timed_execution(
            lambda: pg_conn.cursor().execute("SELECT COUNT(*) FROM json_table WHERE (data->>'age')::int > 30")
        )
        
        _, nested_query_time = timed_execution(
            lambda: pg_conn.cursor().execute("SELECT COUNT(*) FROM json_table WHERE data->'hobbies' ? 'sports'")
        )
        
        # Query compleja con operaciones JSON
        _, complex_query_time = timed_execution(
            lambda: pg_conn.cursor().execute("""
                SELECT 
                    data->>'city' as city,
                    AVG((data->>'age')::int) as avg_age,
                    COUNT(*) as count
                FROM json_table
                WHERE (data->>'age')::int > 25 AND data->'hobbies' ? 'sports'
                GROUP BY data->>'city'
                ORDER BY avg_age DESC
            """)
        )
        
        # Update test
        def update_json():
            with pg_conn.cursor() as cur:
                cur.execute("""
                    UPDATE json_table 
                    SET data = jsonb_set(data, '{age}', to_jsonb((data->>'age')::int + 1))
                    WHERE data->>'city' = 'New York'
                """)
                pg_conn.commit()
        
        _, update_time = timed_execution(update_json)

        results['RDBMS_JSON'] = {
            'insert': insert_time,
            'index_creation': index_time,
            'flat_query': flat_query_time,
            'nested_query': nested_query_time,
            'complex_query': complex_query_time,
            'update': update_time
        }

        # -------------------------
        # MongoDB (NoSQL) - CSV
        # -------------------------
        logging.info("Starting MongoDB CSV benchmark...")
        mongo_db['csv_collection'].drop()

        def insert_csv_mongo():
            data_csv = []
            with open(csv_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    row['id'] = int(row['id'])
                    row['age'] = int(row['age'])
                    data_csv.append(row)
            # Bulk insert optimizado
            mongo_db['csv_collection'].insert_many(data_csv, ordered=False)

        _, insert_time = timed_execution(insert_csv_mongo)

        # Crear índices
        def create_indexes_csv_mongo():
            mongo_db['csv_collection'].create_index([('age', ASCENDING)])
            mongo_db['csv_collection'].create_index([('city', ASCENDING)])
            mongo_db['csv_collection'].create_index([('hobbies', 'text')])
        
        _, index_time = timed_execution(create_indexes_csv_mongo)

        # Queries
        _, flat_query_time = timed_execution(
            lambda: mongo_db['csv_collection'].count_documents({'age': {'$gt': 30}})
        )
        
        _, nested_query_time = timed_execution(
            lambda: mongo_db['csv_collection'].count_documents({'hobbies': {'$regex': 'sports'}})
        )
        
        # Query compleja con agregación
        _, complex_query_time = timed_execution(
            lambda: list(mongo_db['csv_collection'].aggregate([
                {'$match': {'age': {'$gt': 25}, 'hobbies': {'$regex': 'sports'}}},
                {'$group': {
                    '_id': '$city',
                    'avg_age': {'$avg': '$age'},
                    'count': {'$sum': 1}
                }},
                {'$sort': {'avg_age': -1}}
            ]))
        )
        
        # Update test
        _, update_time = timed_execution(
            lambda: mongo_db['csv_collection'].update_many(
                {'city': 'New York'},
                {'$inc': {'age': 1}}
            )
        )

        results['NoSQL_CSV'] = {
            'insert': insert_time,
            'index_creation': index_time,
            'flat_query': flat_query_time,
            'nested_query': nested_query_time,
            'complex_query': complex_query_time,
            'update': update_time
        }

        # -------------------------
        # MongoDB (NoSQL) - JSON
        # -------------------------
        logging.info("Starting MongoDB JSON benchmark...")
        mongo_db['json_collection'].drop()

        def insert_json_mongo():
            # Bulk insert optimizado
            mongo_db['json_collection'].insert_many(data_json, ordered=False)

        _, insert_time = timed_execution(insert_json_mongo)

        # Crear índices
        def create_indexes_json_mongo():
            mongo_db['json_collection'].create_index([('age', ASCENDING)])
            mongo_db['json_collection'].create_index([('city', ASCENDING)])
            mongo_db['json_collection'].create_index([('hobbies', ASCENDING)])
        
        _, index_time = timed_execution(create_indexes_json_mongo)

        # Queries
        _, flat_query_time = timed_execution(
            lambda: mongo_db['json_collection'].count_documents({'age': {'$gt': 30}})
        )
        
        # Query nativa con array (ventaja de MongoDB)
        _, nested_query_time = timed_execution(
            lambda: mongo_db['json_collection'].count_documents({'hobbies': 'sports'})
        )
        
        # Query compleja con agregación
        _, complex_query_time = timed_execution(
            lambda: list(mongo_db['json_collection'].aggregate([
                {'$match': {'age': {'$gt': 25}, 'hobbies': 'sports'}},
                {'$group': {
                    '_id': '$city',
                    'avg_age': {'$avg': '$age'},
                    'count': {'$sum': 1}
                }},
                {'$sort': {'avg_age': -1}}
            ]))
        )
        
        # Update test
        _, update_time = timed_execution(
            lambda: mongo_db['json_collection'].update_many(
                {'city': 'New York'},
                {'$inc': {'age': 1}}
            )
        )

        results['NoSQL_JSON'] = {
            'insert': insert_time,
            'index_creation': index_time,
            'flat_query': flat_query_time,
            'nested_query': nested_query_time,
            'complex_query': complex_query_time,
            'update': update_time
        }

    finally:
        pg_conn.close()
        mongo_client.close()
        csv_path.unlink(missing_ok=True)
        json_path.unlink(missing_ok=True)

    logging.info("Benchmark completed.")
    return results


def plot_results(results: dict):
    """Generate interactive bar charts with Plotly."""
    db_types = {
        "RDBMS": ["RDBMS_CSV", "RDBMS_JSON"],
        "NoSQL": ["NoSQL_CSV", "NoSQL_JSON"]
    }

    for db, keys in db_types.items():
        fig = go.Figure()
        for k in keys:
            fig.add_trace(go.Bar(
                x=list(results[k].keys()),
                y=list(results[k].values()),
                name=k,
                text=[f"{v:.6f} s" for v in results[k].values()],
                textposition="auto"
            ))
        fig.update_layout(
            title=f"Benchmark Results - {db}",
            xaxis_title="Operation",
            yaxis_title="Time (seconds)",
            barmode="group",
            template="plotly_dark",
            height=600
        )
        fig.show()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
    res = run_benchmark(5000)
    plot_results(res)