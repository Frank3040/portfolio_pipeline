#!/usr/bin/env python3
"""
Script to load JSON file into MongoDB collections (movies and series).
Assumes JSON in data/raw/content.json.
Skips loading if data already exists in collections.
Run via Airflow: Automated and scheduled via DAG.
Best practices: Error handling, structured logging, modular connections, pathlib for paths, idempotency.
"""
import json
import sys
from pathlib import Path
import os

# Add project root to sys.path for module imports
SCRIPT_PATH = Path(__file__).resolve()
PROJECT_ROOT = SCRIPT_PATH.parent.parent  # scripts -> video_streaming_pipeline
sys.path.insert(0, str(PROJECT_ROOT))

from pymongo.errors import BulkWriteError

from utils.db_connections import get_mongo_client
from utils.logger import setup_logger

# Project root for pathlib
DATA_RAW_DIR = PROJECT_ROOT / "data" / "raw"

def main():
    logger = setup_logger(__name__, log_file=PROJECT_ROOT / "logs" / "load_json.log")
    
    # Ensure logs dir exists
    (PROJECT_ROOT / "logs").mkdir(exist_ok=True)
    
    try:
        client = get_mongo_client()
        db = client[os.getenv('MONGO_DB', 'video_streaming')]
        
        json_path = DATA_RAW_DIR / "content.json"
        if not json_path.exists():
            raise FileNotFoundError(f"JSON not found: {json_path}")
        
        with open(json_path, 'r') as f:
            data = json.load(f)
        
        # Insert movies
        if 'movies' in data and data['movies']:
            movies_collection = db['movies']
            # Check if collection already contains data
            if movies_collection.count_documents({}) > 0:
                logger.info(f"Collection 'movies' already contains {movies_collection.count_documents({})} documents, skipping load")
            else:
                movies_collection.insert_many(data['movies'])
                logger.info(f"Loaded {len(data['movies'])} movies")
        
        # Insert series
        if 'series' in data and data['series']:
            series_collection = db['series']
            # Check if collection already contains data
            if series_collection.count_documents({}) > 0:
                logger.info(f"Collection 'series' already contains {series_collection.count_documents({})} documents, skipping load")
            else:
                series_collection.insert_many(data['series'])
                logger.info(f"Loaded {len(data['series'])} series")
        
        logger.info("JSON loading process completed")
        
    except BulkWriteError as e:
        logger.error(f"Bulk write error (duplicates?): {e.details}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Error loading JSON: {e}")
        sys.exit(1)
    finally:
        if 'client' in locals():
            client.close()

if __name__ == "__main__":
    main()