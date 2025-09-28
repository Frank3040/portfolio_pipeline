import os
from pathlib import Path
from typing import Optional

import psycopg2
from psycopg2.extras import RealDictCursor
from pymongo import MongoClient

from dotenv import load_dotenv

load_dotenv()

def get_postgres_connection(db_name: Optional[str] = None) -> psycopg2.extensions.connection:
    """
    Modular function to create PostgreSQL connection.
    Best practice: Centralized connection management with error handling.
    """
    try:
        conn = psycopg2.connect(
            host=os.getenv('POSTGRES_HOST', 'localhost'),
            port=os.getenv('POSTGRES_PORT', '5432'),
            database=db_name or os.getenv('PROJECT_POSTGRES_DB', 'video_streaming'),
            user=os.getenv('POSTGRES_USER', 'postgres'),
            password=os.getenv('POSTGRES_PASSWORD', 'secret123')
        )
        return conn
    except psycopg2.Error as e:
        raise Exception(f"Failed to connect to PostgreSQL: {e}")

def get_mongo_client(db_name: Optional[str] = None) -> MongoClient:
    """
    Modular function to create MongoDB client with authentication.
    Best practice: Centralized connection management with error handling.
    """
    try:
        client = MongoClient(
            host=os.getenv('MONGO_HOST', 'localhost'),
            port=int(os.getenv('MONGO_PORT', '27017')),
            username=os.getenv('MONGO_USER', 'admin'),
            password=os.getenv('MONGO_PASSWORD', 'secret123'),
            authSource='admin'  # Use 'admin' database for authentication
        )
        # Test connection
        client.admin.command('ismaster')
        return client
    except Exception as e:
        raise Exception(f"Failed to connect to MongoDB: {e}")