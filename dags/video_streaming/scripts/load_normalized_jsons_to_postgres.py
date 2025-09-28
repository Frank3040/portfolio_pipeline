#!/usr/bin/env python3
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
DATA_PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
SQL_SCHEMA_PATH = PROJECT_ROOT / "sql" / "create_normalized_tables.sql"

def execute_schema_file(conn, schema_path):
    """Execute SQL schema file to create tables and indexes."""
    with open(schema_path, 'r') as f:
        sql_commands = f.read()
    cursor = conn.cursor()
    cursor.execute(sql_commands)
    conn.commit()
    cursor.close()

def main():
    logger = setup_logger(__name__, log_file=PROJECT_ROOT / "logs" / "load_normalized_csvs.log")
    
    # Ensure logs and sql dirs exist
    (PROJECT_ROOT / "logs").mkdir(exist_ok=True)
    (PROJECT_ROOT / "sql").mkdir(exist_ok=True)
    
    try:
        conn = get_postgres_connection()
        
        # Execute schema creation
        if not SQL_SCHEMA_PATH.exists():
            raise FileNotFoundError(f"Schema SQL file not found: {SQL_SCHEMA_PATH}")
        logger.info(f"Executing schema creation from {SQL_SCHEMA_PATH}")
        execute_schema_file(conn, SQL_SCHEMA_PATH)
        
        # CSV mappings: (csv_file, table_name, columns_order)
        csv_mappings = [
            (DATA_PROCESSED_DIR / "content.csv", "content", "content_id, title, type, rating, production_budget"),
            (DATA_PROCESSED_DIR / "movie_details.csv", "movie_details", "content_id, duration_minutes, release_year, views_count"),
            (DATA_PROCESSED_DIR / "series_details.csv", "series_details", "content_id, seasons, avg_episode_duration, total_views"),
            (DATA_PROCESSED_DIR / "content_genres.csv", "content_genres", "content_id, genre"),
            (DATA_PROCESSED_DIR / "series_episodes.csv", "series_episodes", "content_id, season, episode_count")
        ]
        
        for csv_path, table_name, columns in csv_mappings:
            if not csv_path.exists():
                raise FileNotFoundError(f"CSV not found: {csv_path}")
            
            # Check if table already contains data
            cursor = conn.cursor()
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            row_count = cursor.fetchone()[0]
            if row_count > 0:
                logger.info(f"Table {table_name} already contains {row_count} rows, skipping load")
                cursor.close()
                continue
            
            logger.info(f"Loading {csv_path} into {table_name}")
            with open(csv_path, 'r') as f:
                cursor.copy_expert(
                    f"COPY {table_name} ({columns}) FROM STDIN WITH CSV HEADER",
                    f
                )
            logger.info(f"Successfully loaded {csv_path} into {table_name}")
            cursor.close()
        
        conn.commit()
        logger.info("Normalized CSV loading process completed")
        
    except Exception as e:
        logger.error(f"Error loading normalized CSVs: {e}")
        if 'conn' in locals():
            conn.rollback()
        sys.exit(1)
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    main()