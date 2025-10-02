# AI Assistance Disclosure - Video Streaming Data Pipeline Project

- **AI Tool Used:** Grok (built by xAI)  
- **Overall Assistance Level:** 65%  
- **Main Use Cases:**  
  - Code generation: 75%  
  - Documentation: 50%  
  - Debugging: 60%  
  - Data analysis: 70%  
  - Visualizations: 55%  
- **Human Contributions:**  
  - Conceptual pipeline design  
  - Validation and testing of MongoDB and PostgreSQL scripts  
  - Customization of visualizations and views  
  - Original analysis and interpretation  

- **Verification Process:**  
  - Manual review of each AI-generated script  
  - Unit testing of Python and SQL code  
  - Comparison with expected video streaming dataset results  

---

## Work Session Log - Prompts and AI Use

"Create an Airflow DAG to load video streaming data from MongoDB into PostgreSQL"
"Generate a MongoDB collection schema for video content with nested genres and episodes"
"Create Python code to extract MongoDB data and save as CSV with normalization"
"Generate SQL script to create normalized tables in PostgreSQL processed schema"
"Write Python code to plot viewing session duration by device type using matplotlib"
"Create a script to calculate average completion percentage per content type and generate a bar plot"
"Generate documentation for ETL process and database design for video streaming project"
"Suggest indexes and optimizations for PostgreSQL video streaming tables"
"Write 5 prompts to generate Airflow DAGs with different video streaming tasks"
"Write 5 prompts for data analysis of viewing sessions and content in Python"
"Write 5 prompts to generate SQL scripts with joins and aggregations on video streaming data"
"Write 5 prompts to create plots for viewing statistics and content features in Python"

---

## AI Assistance Calculation (Simulated)

1. **Time %:**  
Total hours = 13 h, AI time ≈ 8 h 30 min → (8.5 / 13) × 100 ≈ 65%  

2. **Content %:**  
Code + documentation + prompts ≈ 65% of total project content  

3. **Complexity %:**  
Significant level (Level 3) → 67.5%  

4. **Self-Assessment Score:**  
- Q1 (Conceptualization) = 55%  
- Q2 (Implementation) = 70%  
- Q3 (Understanding) = 60%  
- Q4 (Problem-Solving) = 65%  
Average score = (55 + 70 + 60 + 65)/4 = 62.5%  

**Final AI Assistance %:**  
`0.25×65 + 0.35×65 + 0.25×67.5 + 0.15×62.5 ≈ 65% ✅`

---

# Database Design

## Overview
The database design for the video streaming pipeline includes a NoSQL (MongoDB) component for raw data storage and a relational (PostgreSQL) component for processed and analytical data. The design supports flexible data ingestion, normalization, and querying for analysis.

### NoSQL Database Design (MongoDB)
- **Collection: `content`**
  - **Purpose**: Stores core metadata for all video content.
  - **Fields**: `_id` (ObjectId), `title` (String), `type` (String, e.g., "movie" or "series"), `release_year` (Integer), `description` (String), `language` (String).
  - **Indexing**: Index on `title` for text search, `_id` for primary access.
- **Collection: `genres`**
  - **Purpose**: Links genres to content.
  - **Fields**: `_id` (ObjectId), `content_id` (ObjectId, reference to `content._id`), `genre` (String).
  - **Indexing**: Compound index on `content_id` and `genre`.
- **Collection: `movie_details`**
  - **Purpose**: Stores movie-specific details.
  - **Fields**: `_id` (ObjectId), `content_id` (ObjectId, reference to `content._id`), `duration_minutes` (Integer), `director` (String), `rating` (Float).
  - **Indexing**: Index on `content_id`.
- **Collection: `series_details`**
  - **Purpose**: Stores series-specific details.
  - **Fields**: `_id` (ObjectId), `content_id` (ObjectId, reference to `content._id`), `season_count` (Integer), `episode_count` (Integer), `creator` (String).
  - **Indexing**: Index on `content_id`.
- **Collection: `series_episodes`**
  - **Purpose**: Stores episode-level details.
  - **Fields**: `_id` (ObjectId), `content_id` (ObjectId, reference to `content._id`), `season_number` (Integer), `episode_number` (Integer), `title` (String), `duration_minutes` (Integer), `air_date` (Date).
  - **Indexing**: Compound index on `content_id`, `season_number`, `episode_number`.

### Relational Database Design (PostgreSQL)
- **Schema: `raw`**
  - **Table: `raw.video_data`**
    - **Columns**: `id` (TEXT), `title` (TEXT), `type` (TEXT), `release_year` (INTEGER), `genres` (TEXT[]), `duration_minutes` (INTEGER), `season_count` (INTEGER), `episode_count` (INTEGER), `raw_data` (JSONB).
    - **Indexes**: Primary key on `id`.
- **Schema: `processed`**
  - **Table: `content`**
    - **Columns**: `content_id` (TEXT, PK), `title` (TEXT), `type` (TEXT), `release_year` (INTEGER), `description` (TEXT), `language` (TEXT).
    - **Indexes**: PK on `content_id`.
  - **Table: `movie_details`**
    - **Columns**: `content_id` (TEXT, PK, FK to `content`), `duration_minutes` (INTEGER), `director` (TEXT), `rating` (DOUBLE PRECISION).
    - **Constraints**: FK on `content_id`.
  - **Table: `series_details`**
    - **Columns**: `content_id` (TEXT, PK, FK to `content`), `season_count` (INTEGER), `episode_count` (INTEGER), `creator` (TEXT).
    - **Constraints**: FK on `content_id`.
  - **Table: `genres`**
    - **Columns**: `content_id` (TEXT, FK to `content`), `genre` (TEXT).
    - **Constraints**: PK on `(content_id, genre)`.
    - **Indexes**: Index on `content_id`.
  - **Table: `series_episodes`**
    - **Columns**: `content_id` (TEXT, FK to `content`), `season_number` (INTEGER), `episode_number` (INTEGER), `title` (TEXT), `duration_minutes` (INTEGER), `air_date` (DATE).
    - **Constraints**: PK on `(content_id, season_number, episode_number)`.
    - **Indexes**: Index on `content_id`.
- **Schema: `trusted`**
  - **View: `v_content_summary`**
    - **Definition**: 
      ```sql
      SELECT c.content_id, c.title, c.type, c.release_year, 
             md.duration_minutes, sd.season_count, sd.episode_count, 
             ARRAY_AGG(g.genre) AS genres
      FROM processed.content c
      LEFT JOIN processed.movie_details md ON c.content_id = md.content_id
      LEFT JOIN processed.series_details sd ON c.content_id = sd.content_id
      LEFT JOIN processed.genres g ON c.content_id = g.content_id
      GROUP BY c.content_id, c.title, c.type, c.release_year, md.duration_minutes, sd.season_count, sd.episode_count;
      ```
  - **View: `v_episode_details`**
    - **Definition**: 
      ```sql
      SELECT c.title, se.season_number, se.episode_number, se.title AS episode_title, 
             se.duration_minutes, se.air_date
      FROM processed.content c
      JOIN processed.series_details sd ON c.content_id = sd.content_id
      JOIN processed.series_episodes se ON c.content_id = se.content_id;
      ```

---

# Statistics

"Calculate the total number of viewing sessions per content type (movie/series)"
"Compute the average watch duration per device type across all sessions"
"Determine the most watched genre based on viewing session counts"
"Calculate the completion percentage distribution across all content"
"Analyze the average rating per release year for movies"

---

# Visualizations

"Create a bar plot showing total viewing sessions by content type using matplotlib"
"Generate a line plot of average watch duration by device type over time using seaborn"
"Produce a pie chart of the most watched genres based on session counts"
"Create a histogram of completion percentages across all viewing sessions"
"Generate a scatter plot of movie ratings versus release year"

---

# ETL Pipeline

## Overview
The ETL pipeline processes video streaming data, transforming raw data from MongoDB and CSV into a normalized relational structure in PostgreSQL.

## Pipeline Objectives
- Extract raw data from MongoDB and CSV.
- Transform data by normalizing nested fields and cleaning inconsistencies.
- Load normalized data into PostgreSQL for analysis.

## Architecture
- **Data Sources**: MongoDB (raw video data), CSV (user/viewing session data).
- **Database**: PostgreSQL with `raw`, `processed`, and `trusted` schemas.
- **Orchestration**: Airflow DAG (`video_streaming_pipeline`).
- **File Structure**: `scripts/`, `sql/`, `data/raw/`, `data/processed/`, `logs/`, `utils/`.

## Pipeline Steps
1. **Create Postgres Tables (`create_postgres_tables`)**:
   - **Script**: `scripts/create_postgres_tables.py`
   - **Action**: Creates tables in `processed` and `trusted` schemas.
   - **Input**: `sql/create_tables.sql`
   - **Output**: `processed` tables.
2. **Create MongoDB Collections (`create_mongodb_collections`)**:
   - **Script**: `scripts/create_mongodb_collections.py`
   - **Action**: Ensures MongoDB collections exist.
   - **Output**: MongoDB collections.
3. **Load CSVs to Postgres (`load_csvs_to_postgres`)**:
   - **Script**: `scripts/load_csvs_to_postgres.py`
   - **Action**: Loads raw CSVs into `raw` schema.
   - **Input**: `data/raw/*.csv`
   - **Output**: `raw` tables.
4. **Load JSON to MongoDB (`load_json_to_mongo`)**:
   - **Script**: `scripts/load_json_to_mongo.py`
   - **Action**: Loads JSON data into MongoDB.
   - **Input**: JSON files.
   - **Output**: Populated MongoDB collections.
5. **Extract MongoDB to CSV (`extract_mongo_to_csv`)**:
   - **Script**: `scripts/extract_mongo_to_csv.py`
   - **Action**: Extracts and normalizes MongoDB data to CSVs.
   - **Input**: MongoDB collections.
   - **Output**: `data/processed/*.csv`.
6. **Load Normalized JSONs to Postgres (`load_normalized_jsons_to_postgres`)**:
   - **Script**: `scripts/load_normalized_jsons_to_postgres.py`
   - **Action**: Loads normalized CSVs into `processed` schema.
   - **Input**: `data/processed/*.csv`
   - **Output**: `processed` tables.

## Configuration
- **Environment Variables**: `POSTGRES_*`, `MONGO_*`, `PROJECT_ROOT`, `DATA_*_PATH`.
- **Docker Setup**: PostgreSQL, MongoDB, Airflow in Docker.
- **Initialization**: `init-postgres.sh` creates database and schemas.

## Best Practices
- **Idempotency**: Uses `IF NOT EXISTS` and `ON CONFLICT`.
- **Error Handling**: Try-catch with rollback.
- **Logging**: Structured to `logs/`.
- **Security**: `data_analyst` role with `SELECT` privileges.

## Execution
- **Schedule**: Daily via Airflow.
- **Dependencies**: Parallel creation, sequential extraction/loading.

## Output
- **Data**: Normalized tables and views.
- **Files**: CSVs in `data/processed/`.

## Maintenance
- **Monitoring**: Check `logs/`.
- **Updates**: Modify SQL or scripts.
- **Scaling**: Adjust Airflow `default_args`.

## Troubleshooting
- **Duplicate Keys**: Verify deduplication in extraction.
- **Missing Files**: Check paths.
- **Database Issues**: Inspect logs.