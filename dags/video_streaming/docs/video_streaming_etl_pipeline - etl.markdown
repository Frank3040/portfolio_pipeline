# Video Streaming ETL Pipeline Documentation

## Overview
This ETL (Extract, Transform, Load) pipeline processes video streaming data, extracting raw data from MongoDB, transforming it into a normalized relational structure, and loading it into PostgreSQL for analytical use. The pipeline is orchestrated using Apache Airflow in a Dockerized environment, adhering to best practices for modularity, error handling, logging, and idempotency.

## Pipeline Objectives
- **Extract**: Retrieve video streaming data (movies and series) from MongoDB and load raw CSV data into PostgreSQL.
- **Transform**: Normalize nested arrays (e.g., genres, episodes) and clean data for consistency.
- **Load**: Store normalized data in PostgreSQL `processed` schema and create views in `trusted` schema for analysts.
- **Access Control**: Provide read-only access to `data_analyst` role for views in `trusted` schema.

## Architecture
- **Data Sources**:
  - MongoDB: Stores raw video streaming data (movies and series with nested fields like genres and episodes).
  - CSV: Additional raw data loaded into PostgreSQL `raw` schema.
- **Database**: PostgreSQL with three schemas:
  - `raw`: Stores untransformed CSV data.
  - `processed`: Contains normalized tables (`content`, `movie_details`, `series_details`, etc.).
  - `trusted`: Hosts analytical views for data analysts.
- **Orchestration**: Airflow DAG (`video_streaming_pipeline`) schedules and manages tasks.
- **File Structure**:
  - `scripts/`: Python scripts for ETL tasks.
  - `sql/`: SQL files for table creation.
  - `data/raw/`: Raw CSV storage.
  - `data/processed/`: Normalized JSONs/CSVs.
  - `logs/`: Log files for debugging.
  - `utils/`: Reusable modules (`db_connections.py`, `logger.py`).

## Pipeline Steps
The pipeline is executed via the `video_streaming_pipeline` DAG with the following tasks:

1. **Create Postgres Tables (`create_postgres_tables`)**:
   - **Script**: `scripts/create_postgres_tables.py`
   - **Action**: Executes SQL to create tables in `processed` and `trusted` schemas if they don’t exist.
   - **Input**: `sql/create_tables.sql`
   - **Output**: Tables in `processed` schema (`content`, `movie_details`, `series_details`, etc.)
   - **Idempotency**: Uses `CREATE TABLE IF NOT EXISTS`.

2. **Create MongoDB Collections (`create_mongodb_collections`)**:
   - **Script**: `scripts/create_mongodb_collections.py`
   - **Action**: Ensures MongoDB collections for movies and series exist.
   - **Output**: MongoDB collections.
   - **Idempotency**: Checks for existing collections.

3. **Load CSVs to Postgres (`load_csvs_to_postgres`)**:
   - **Script**: `scripts/load_csvs_to_postgres.py`
   - **Action**: Loads raw CSVs (e.g., `users.csv`, `viewing_sessions.csv`) into `raw` schema using `COPY`.
   - **Input**: `data/raw/*.csv`
   - **Output**: Tables in `raw` schema.
   - **Idempotency**: Skips loading if tables contain data.

4. **Load JSON to MongoDB (`load_json_to_mongo`)**:
   - **Script**: `scripts/load_json_to_mongo.py`
   - **Action**: Loads JSON data into MongoDB collections.
   - **Input**: JSON files.
   - **Output**: Populated MongoDB collections.
   - **Idempotency**: Overwrites or skips existing records.

5. **Extract MongoDB to CSV (`extract_mongo_to_csv`)**:
   - **Script**: `scripts/extract_mongo_to_csv.py`
   - **Action**: Extracts data from MongoDB, normalizes nested fields (e.g., genres, episodes), and saves as CSVs in `data/processed/`.
   - **Input**: MongoDB collections.
   - **Output**: Normalized CSVs (e.g., `content.csv`, `genres.csv`).
   - **Idempotency**: Deduplicates data during normalization.

6. **Load Normalized JSONs to Postgres (`load_normalized_jsons_to_postgres`)**:
   - **Script**: `scripts/load_normalized_jsons_to_postgres.py`
   - **Action**: Loads normalized CSVs into `processed` schema tables using `COPY`.
   - **Input**: `data/processed/*.csv`
   - **Output**: `processed` schema tables.
   - **Idempotency**: Skips duplicate records.

## Database Schema
### Raw Schema
- Stores untransformed CSV data (e.g., `users`, `viewing_sessions`).
- Example Columns (for `users`): `user_id`, `age`, `country`, `subscription_type`, `registration_date`, `total_watch_time_hours`.
- Example Columns (for `viewing_sessions`): `session_id`, `user_id`, `content_id`, `watch_date`, `watch_duration_minutes`, `completion_percentage`, `device_type`, `quality_level`.

### Processed Schema
- **content**: Core content details (e.g., `content_id` (PK), `title`, `type`, `release_year`).
- **movie_details**: Movie-specific data (e.g., `content_id` (FK), `duration_minutes`).
- **series_details**: Series-specific data (e.g., `content_id` (FK), `season_count`).
- **genres**: Normalized genres (e.g., `content_id` (FK), `genre`).
- Other tables as needed for normalized data.

### Trusted Schema
- Views for analysts (not explicitly detailed but assumed similar to Spotify pipeline).
- Access: `data_analyst` role has `SELECT` privileges on `trusted` schema.

## Configuration
- **Environment Variables** (`.env`):
  - `POSTGRES_HOST`, `POSTGRES_PORT`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`
  - `MONGO_HOST`, `MONGO_PORT`, `MONGO_USER`, `MONGO_PASSWORD`
  - `PROJECT_ROOT`, `DATA_RAW_PATH`, `DATA_PROCESSED_PATH`
  - `_PIP_ADDITIONAL_REQUIREMENTS`: Includes `psycopg2`, `pymongo`.
- **Docker Setup**: PostgreSQL, MongoDB, and Airflow run in Docker containers.
- **Initialization**: `init-postgres.sh` creates database, schemas (`raw`, `processed`, `trusted`), and `data_analyst` role.

## Best Practices
- **Idempotency**: Scripts use `IF NOT EXISTS` for table/collection creation and skip duplicates during loading.
- **Error Handling**: Try-catch blocks with transaction rollback on failure.
- **Logging**: Structured logging to `logs/` using `utils.logger.setup_logger`.
- **Modularity**: Reusable utilities (`db_connections.py`, `logger.py`) and separate SQL files.
- **Security**: `data_analyst` role restricted to `SELECT` on `trusted` schema.
- **Efficiency**: Uses `COPY` for PostgreSQL and bulk operations for MongoDB.

## Execution
- **Schedule**: Daily via Airflow DAG (`video_streaming_pipeline`).
- **Dependencies**: Parallel table/collection creation, followed by parallel CSV/JSON loads, then sequential extraction and loading.
- **Command**: Deployed in Airflow; scripts can be run standalone for testing.

## Output
- **Data**: Normalized tables in `processed` schema, views in `trusted` schema.
- **Files**: Normalized CSVs in `data/processed/`.

## Maintenance
- **Monitoring**: Check `logs/` for errors or skipped tasks.
- **Updates**: Modify SQL files for new tables/views or adjust transformation logic in scripts.
- **Scaling**: Adjust Airflow `default_args` (e.g., `retries`, `retry_delay`) for robustness.

## Troubleshooting
- **Duplicate Key Errors**: Verify deduplication in `extract_mongo_to_csv.py`.
- **Missing Files**: Check paths in `DATA_RAW_PATH` and `DATA_PROCESSED_PATH`.
- **Database Issues**: Inspect `init-postgres.sh` and MongoDB/PostgreSQL logs.