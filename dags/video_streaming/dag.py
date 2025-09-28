#!/usr/bin/env python3

import sys
from pathlib import Path

# Add project root to sys.path for module imports
SCRIPT_PATH = Path(__file__).resolve()
PROJECT_ROOT = SCRIPT_PATH.parent  # dags/video_streaming_pipeline
sys.path.insert(0, str(PROJECT_ROOT))

from datetime import timedelta
import pendulum
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator

# Import scripts
from scripts.create_postgres_tables import main as create_postgres_tables_main
from scripts.create_mongodb_collections import main as create_mongodb_collections_main
from scripts.load_csvs_to_postgres import main as load_csvs_to_postgres_main
from scripts.load_json_to_mongo import main as load_json_to_mongo_main
from scripts.extract_mongo_to_csv import extract_and_normalize as extract_mongo_to_csv_main
from scripts.load_normalized_jsons_to_postgres import main as load_normalized_jsons_to_postgres_main
default_args = {
    'owner': 'data_engineer',
    'depends_on_past': False,
    'start_date': pendulum.today('UTC').add(days=-1),  # Explicit pendulum datetime
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(seconds=30),
}

dag = DAG(
    'video_streaming_pipeline',
    default_args=default_args,
    description='ETL pipeline for video streaming data',
    schedule=timedelta(days=1),  # Daily schedule
    catchup=False,
    tags=['etl', 'video'],
)

# Task 1: Create Postgres tables
create_postgres_task = PythonOperator(
    task_id='create_postgres_tables',
    python_callable=create_postgres_tables_main,
    dag=dag,
)

# Task 2: Create MongoDB collections
create_mongo_task = PythonOperator(
    task_id='create_mongodb_collections',
    python_callable=create_mongodb_collections_main,
    dag=dag,
)

# Task 3: Load CSVs to Postgres
load_csvs_task = PythonOperator(
    task_id='load_csvs_to_postgres',
    python_callable=load_csvs_to_postgres_main,
    dag=dag,
)

# Task 4: Load JSON to Mongo
load_json_task = PythonOperator(
    task_id='load_json_to_mongo',
    python_callable=load_json_to_mongo_main,
    dag=dag,
)

# Task 5: Extract MongoDB to CSV
extract_mongo_task = PythonOperator(
    task_id='extract_mongo_to_csv',
    python_callable=extract_mongo_to_csv_main,
    dag=dag,
)

# Task 6: Load Normalized JSONs to Postgres
load_normalized_json_task = PythonOperator(
    task_id='load_normalized_jsons_to_postgres',
    python_callable=load_normalized_jsons_to_postgres_main,
    dag=dag,
)

# Dependencies: Parallel creation, then parallel loads, then extract
create_postgres_task >> load_csvs_task
create_mongo_task >> load_json_task >> extract_mongo_task >> load_normalized_json_task