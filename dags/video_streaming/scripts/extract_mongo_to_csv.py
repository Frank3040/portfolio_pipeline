
#!/usr/bin/env python3
"""
Script to extract data from MongoDB (movies and series collections),
normalize arrays (genres and episodes_per_season), and save to CSVs in data/processed/.
Normalized tables:
- content.csv: content_id, title, type, rating, production_budget
- movie_details.csv: content_id, duration_minutes, release_year, views_count
- series_details.csv: content_id, seasons, avg_episode_duration, total_views
- content_genres.csv: content_id, genre
- series_episodes.csv: content_id, season, episode_count

Run via Airflow: Can be orchestrated in DAG.
Best practices: Error handling, structured logging, modular connections, pathlib for paths.
"""
import csv
import os
import sys
from pathlib import Path
from typing import List, Dict, Any

# Add project root to sys.path for module imports
SCRIPT_PATH = Path(__file__).resolve()
PROJECT_ROOT = SCRIPT_PATH.parent.parent  # scripts -> video_streaming_pipeline
sys.path.insert(0, str(PROJECT_ROOT))

# Now you can import from utils
from utils.db_connections import get_mongo_client
from utils.logger import setup_logger

from pymongo import MongoClient

# Project root for pathlib
PROJECT_ROOT = Path(__file__).parent.parent
DATA_PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
LOGS_DIR = PROJECT_ROOT / "logs"

def extract_and_normalize() -> None:
    """
    Extract from MongoDB, normalize, and write to CSVs.
    """
    logger = setup_logger(__name__, log_file=LOGS_DIR / "extract_mongo_to_csv.log")
    
    # Ensure directories exist
    DATA_PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    LOGS_DIR.mkdir(exist_ok=True)
    
    try:
        client = get_mongo_client()
        db = client[os.getenv('MONGO_DB', 'video_streaming')]
        
        # Fetch all documents
        movies: List[Dict[str, Any]] = list(db['movies'].find())
        series: List[Dict[str, Any]] = list(db['series'].find())
        
        if not movies and not series:
            logger.warning("No data found in MongoDB collections")
            return
        
        logger.info(f"Fetched {len(movies)} movies and {len(series)} series")
        
        # Prepare data structures
        content_rows: List[List[Any]] = []
        movie_details_rows: List[List[Any]] = []
        series_details_rows: List[List[Any]] = []
        genre_rows: List[List[str]] = []
        episode_rows: List[List[Any]] = []
        
        # Process movies
        for movie in movies:
            content_id = movie['content_id']
            content_rows.append([
                content_id,
                movie['title'],
                'movie',
                movie['rating'],
                movie['production_budget']
            ])
            movie_details_rows.append([
                content_id,
                movie['duration_minutes'],
                movie['release_year'],
                movie['views_count']
            ])
            for genre in movie.get('genre', []):
                genre_rows.append([content_id, genre])
        
        # Process series
        for ser in series:
            content_id = ser['content_id']
            content_rows.append([
                content_id,
                ser['title'],
                'series',
                ser['rating'],
                ser['production_budget']
            ])
            series_details_rows.append([
                content_id,
                ser['seasons'],
                ser['avg_episode_duration'],
                ser['total_views']
            ])
            for genre in ser.get('genre', []):
                genre_rows.append([content_id, genre])
            episodes_per_season = ser.get('episodes_per_season', [])
            if len(episodes_per_season) != ser['seasons']:
                logger.warning(f"Mismatch in seasons and episodes list for {content_id}")
            for season_num, ep_count in enumerate(episodes_per_season, start=1):
                episode_rows.append([content_id, season_num, ep_count])
        
        # Write CSVs
        csv_files = {
            'content.csv': (['content_id', 'title', 'type', 'rating', 'production_budget'], content_rows),
            'movie_details.csv': (['content_id', 'duration_minutes', 'release_year', 'views_count'], movie_details_rows),
            'series_details.csv': (['content_id', 'seasons', 'avg_episode_duration', 'total_views'], series_details_rows),
            'content_genres.csv': (['content_id', 'genre'], genre_rows),
            'series_episodes.csv': (['content_id', 'season', 'episode_count'], episode_rows),
        }
        
        for filename, (headers, rows) in csv_files.items():
            if not rows:
                logger.info(f"No data for {filename}, skipping")
                continue
            path = DATA_PROCESSED_DIR / filename
            with open(path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(headers)
                writer.writerows(rows)
            logger.info(f"Wrote {len(rows)} rows to {path}")
        
        logger.info("Extraction and normalization completed successfully")
        
    except Exception as e:
        logger.error(f"Error during extraction and normalization: {e}")
        sys.exit(1)
    finally:
        if 'client' in locals():
            client.close()

if __name__ == "__main__":
    extract_and_normalize()