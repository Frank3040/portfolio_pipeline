#!/usr/bin/env python3
"""
Script to create MongoDB collections (movies and series).
MongoDB is schemaless, so this ensures collections exist and adds basic indexes.
Run via Airflow: Automated and scheduled via DAG.
Best practices: Error handling, structured logging, modular connections.
"""
import sys
from pathlib import Path
import os

# Add project root to sys.path for module imports
SCRIPT_PATH = Path(__file__).resolve()
PROJECT_ROOT = SCRIPT_PATH.parent.parent  # scripts -> video_streaming_pipeline
sys.path.insert(0, str(PROJECT_ROOT))

# Now you can import from utils
from utils.db_connections import get_mongo_client
from utils.logger import setup_logger

from pymongo import MongoClient
from pymongo.errors import OperationFailure

def main():
    logger = setup_logger(__name__, log_file=PROJECT_ROOT / "logs" / "create_collections.log")
    
    try:
        client = get_mongo_client()
        db = client[os.getenv('MONGO_DB', 'video_streaming')]
        
        existing_collections = db.list_collection_names()
        
        # Create collections if not exist
        
        if 'movies' not in existing_collections:
            movies_collection = db.create_collection("movies")
            # Add indexes for performance (common queries on content_id, genre, rating)
            movies_collection.create_index("content_id", unique=True)
            movies_collection.create_index("genre")
            movies_collection.create_index("rating")
            
            logger.info("MongoDB collection 'movies' created with indexes")
            
        elif 'series' not in existing_collections:
            series_collection = db.create_collection("series")
            # Add indexes for performance (common queries on content_id, genre, rating)
            series_collection.create_index("content_id", unique=True)
            series_collection.create_index("genre")
            series_collection.create_index("rating")
        
        logger.info("MongoDB collection 'series' created with indexes")
        
    except OperationFailure as e:
        logger.error(f"Authentication or operation error: {e.details}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Error creating collections: {e}")
        sys.exit(1)
    finally:
        if 'client' in locals():
            client.close()

if __name__ == "__main__":
    main()