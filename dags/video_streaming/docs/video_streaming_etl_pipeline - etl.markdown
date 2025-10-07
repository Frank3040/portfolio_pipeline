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

---

### AI Assistance Disclosure - Video Streaming Data Pipeline Project

* **AI Tool Used:** Grok (built by xAI)

* **Overall Assistance Level:** 45%

* **Main Use Cases:**

  * Code generation: 55%
  * Documentation: 35%
  * Debugging: 40%
  * Data analysis: 45%
  * Visualizations: 40%

* **Human Contributions:**

  * Conceptual pipeline design
  * Validation and testing of MongoDB and PostgreSQL scripts
  * Customization of visualizations and views
  * Original analysis and interpretation

* **Verification Process:**

  * Manual review of each AI-generated script
  * Unit testing of Python and SQL code
  * Comparison with expected video streaming dataset results

---

## Work Session Log - Prompts and AI Use

* **Session 1:** Create an Airflow DAG to load video streaming data from MongoDB into PostgreSQL. The prompt requested an automated ETL pipeline definition with detailed extract, transform, and load tasks, including Airflow operators and schedule intervals.
* **Session 2:** Generate a MongoDB collection schema for video content with nested genres and episodes. The AI was asked to model complex document structures while maintaining references for relational mapping.
* **Session 3:** Create Python code to extract MongoDB data and save it as CSV with normalization. The prompt emphasized transforming nested JSON fields into flat tabular data suitable for SQL ingestion.
* **Session 4:** Generate SQL script to create normalized tables in PostgreSQL processed schema. The AI was tasked with defining primary and foreign keys, indexes, and constraints.
* **Session 5:** Write Python code to plot viewing session duration by device type using matplotlib. The AI produced code to visualize user engagement patterns.
* **Session 6:** Create a script to calculate average completion percentage per content type and generate a bar plot. The AI handled both calculation and chart generation.
* **Session 7:** Generate documentation for the ETL process and database design for the video streaming project. The prompt requested structured documentation including architecture, data flow, and maintenance sections.
* **Session 8:** Suggest indexes and optimizations for PostgreSQL video streaming tables. The AI recommended indexing strategies based on expected query patterns.
* **Session 9:** Write 5 prompts to generate Airflow DAGs with different video streaming tasks, focusing on data ingestion, transformation, and analytics workflows.
* **Session 10:** Write 5 prompts for data analysis of viewing sessions and content in Python, emphasizing exploratory analysis and user engagement insights.
* **Session 11:** Write 5 prompts to generate SQL scripts with joins and aggregations on video streaming data. The AI focused on analytical queries for content and user trends.
* **Session 12:** Write 5 prompts to create plots for viewing statistics and content features in Python, with detailed visualization requirements and layout preferences.

---

## AI Assistance Calculation

1. **Time %:**
   Total hours = 13 h, AI time ≈ 5 h 50 min → (5.83 / 13) × 100 ≈ **45%**

2. **Content %:**
   Code + documentation + prompts ≈ **45%** of total project content

3. **Complexity %:**
   Moderate level (Level 2) → **47.5%**

4. **Self-Assessment Score:**

   * Q1 (Conceptualization) = 45%
   * Q2 (Implementation) = 50%
   * Q3 (Understanding) = 45%
   * Q4 (Problem-Solving) = 40%
     Average score = (45 + 50 + 45 + 40)/4 = **45%**

**Final AI Assistance %:**
`0.25×45 + 0.35×45 + 0.25×47.5 + 0.15×45 ≈ 45%`