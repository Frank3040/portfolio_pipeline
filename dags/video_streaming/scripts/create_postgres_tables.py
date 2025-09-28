#!/usr/bin/env python3
"""
Script to create PostgreSQL tables by executing SQL files.
Run via Airflow: Automated and scheduled via DAG.
Best practices: Error handling, structured logging, modular connections.
"""
import sys
from pathlib import Path

# Add project root to sys.path for module imports
SCRIPT_PATH = Path(__file__).resolve()
PROJECT_ROOT = SCRIPT_PATH.parent.parent  # scripts -> video_streaming_pipeline
sys.path.insert(0, str(PROJECT_ROOT))

# Now you can import from utils
from utils.db_connections import get_postgres_connection
from utils.logger import setup_logger

import psycopg2

# SQL directory
SQL_DIR = PROJECT_ROOT / "sql"

def main():
    logger = setup_logger(__name__, log_file=PROJECT_ROOT / "logs" / "create_tables.log")
    
    try:
        conn = get_postgres_connection()
        cursor = conn.cursor()
        
        # List SQL files for table creation
        sql_files = sorted(SQL_DIR.glob("create_*.sql"))
        if not sql_files:
            raise FileNotFoundError("No SQL files found in sql/ directory")
        
        for sql_file in sql_files:
            logger.info(f"Executing SQL file: {sql_file}")
            with open(sql_file, 'r') as f:
                sql_content = f.read()
            cursor.execute(sql_content)
            logger.info(f"Successfully executed: {sql_file.name}")
        
        conn.commit()
        logger.info("All tables created successfully")
        
    except Exception as e:
        logger.error(f"Error creating tables: {e}")
        sys.exit(1)
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    main()