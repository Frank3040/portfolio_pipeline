#!/usr/bin/env python3
"""
Script to load CSV files into PostgreSQL tables using COPY command.
Assumes CSVs in data/raw/.
Skips loading if data already exists in tables.
Run via Airflow: Automated and scheduled via DAG.
Best practices: Error handling, structured logging, modular connections, pathlib for paths, idempotency.
"""
import os
import sys
from pathlib import Path

# Add project root to sys.path for module imports
SCRIPT_PATH = Path(__file__).resolve()
PROJECT_ROOT = SCRIPT_PATH.parent.parent  # scripts -> video_streaming_pipeline
sys.path.insert(0, str(PROJECT_ROOT))

import psycopg2

from utils.db_connections import get_postgres_connection
from utils.logger import setup_logger

# Project root for pathlib
DATA_RAW_DIR = PROJECT_ROOT / "data" / "raw"

def main():
    logger = setup_logger(__name__, log_file=PROJECT_ROOT / "logs" / "load_csvs.log")
    
    # Ensure logs dir exists
    (PROJECT_ROOT / "logs").mkdir(exist_ok=True)
    
    try:
        conn = get_postgres_connection()
        cursor = conn.cursor()
        
        # CSV mappings: (csv_file, table_name, columns_order)
        csv_mappings = [
            (DATA_RAW_DIR / "users.csv", "users", "user_id, age, country, subscription_type, registration_date, total_watch_time_hours"),
            (DATA_RAW_DIR / "viewing_sessions.csv", "viewing_sessions", "session_id, user_id, content_id, watch_date, watch_duration_minutes, completion_percentage, device_type, quality_level")
        ]
        
        for csv_path, table_name, columns in csv_mappings:
            if not csv_path.exists():
                raise FileNotFoundError(f"CSV not found: {csv_path}")
            
            # Check if table already contains data
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            row_count = cursor.fetchone()[0]
            if row_count > 0:
                logger.info(f"Table {table_name} already contains {row_count} rows, skipping load")
                continue
            
            logger.info(f"Loading {csv_path} into {table_name}")
            with open(csv_path, 'r') as f:
                cursor.copy_expert(
                    f"COPY {table_name} ({columns}) FROM STDIN WITH CSV HEADER",
                    f
                )
            logger.info(f"Successfully loaded {csv_path} into {table_name}")
        
        conn.commit()
        logger.info("CSV loading process completed")
        
    except Exception as e:
        logger.error(f"Error loading CSVs: {e}")
        if 'conn' in locals():
            conn.rollback()
        sys.exit(1)
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    main()