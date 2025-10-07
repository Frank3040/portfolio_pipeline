# Database Design Documentation with AI Assistance Disclosure

# Database Design Documentation

This document outlines the design of the database schemas for the video streaming ETL pipeline, covering both the NoSQL (MongoDB) and relational (PostgreSQL) databases. The design focuses on supporting the pipeline's objectives of storing, transforming, and analyzing video streaming data efficiently.

## NoSQL Database Design (MongoDB)

The NoSQL database uses MongoDB to store raw and semi-structured data, leveraging its flexibility for nested documents. The following collections are defined:

### Collection: `content`
- **Purpose**: Stores core metadata for all video content (movies and series).
- **Fields**:
  - `_id`: ObjectId (automatically generated unique identifier, primary key equivalent).
  - `title`: String (content title, e.g., "Inception").
  - `type`: String (content type, e.g., "movie" or "series").
  - `release_year`: Integer (year of release).
  - `description`: String (optional content summary).
  - `language`: String (primary language, e.g., "English").
- **Indexing**: Index on `title` for text search, `_id` for primary access.
- **Notes**: Acts as the root collection, with references to `movie_details`, `series_details`, and `genres` via embedded or referenced data.

### Collection: `genres`
- **Purpose**: Stores genre information linked to content, allowing for multiple genres per content item.
- **Fields**:
  - `_id`: ObjectId (unique identifier).
  - `content_id`: ObjectId (reference to `content._id`, foreign key equivalent).
  - `genre`: String (e.g., "Action", "Drama").
- **Indexing**: Compound index on `content_id` and `genre` for efficient joins and lookups.
- **Notes**: Denormalized to support multiple genres per content item, with a one-to-many relationship to `content`.

### Collection: `movie_details`
- **Purpose**: Stores movie-specific details, linked to `content`.
- **Fields**:
  - `_id`: ObjectId (unique identifier).
  - `content_id`: ObjectId (reference to `content._id`, foreign key equivalent).
  - `duration_minutes`: Integer (movie duration in minutes).
  - `director`: String (primary director).
  - `rating`: Float (e.g., 7.8, optional rating score).
- **Indexing**: Index on `content_id` for linking to `content`.
- **Notes**: One-to-one relationship with `content` where `type` is "movie".

### Collection: `series_details`
- **Purpose**: Stores series-specific details, linked to `content`.
- **Fields**:
  - `_id`: ObjectId (unique identifier).
  - `content_id`: ObjectId (reference to `content._id`, foreign key equivalent).
  - `season_count`: Integer (number of seasons).
  - `episode_count`: Integer (total episodes across all seasons).
  - `creator`: String (series creator).
- **Indexing**: Index on `content_id` for linking to `content`.
- **Notes**: One-to-one relationship with `content` where `type` is "series".

### Collection: `series_episodes`
- **Purpose**: Stores episode-level details for series, linked to `series_details` and `content`.
- **Fields**:
  - `_id`: ObjectId (unique identifier).
  - `content_id`: ObjectId (reference to `content._id`, foreign key equivalent).
  - `season_number`: Integer (season number).
  - `episode_number`: Integer (episode number within season).
  - `title`: String (episode title).
  - `duration_minutes`: Integer (episode duration).
  - `air_date`: Date (release date of episode).
- **Indexing**: Compound index on `content_id`, `season_number`, and `episode_number` for efficient retrieval.
- **Notes**: One-to-many relationship with `series_details`, supporting detailed episode tracking.

### NoSQL Design Considerations
- **Flexibility**: Nested documents or references allow for easy addition of new fields (e.g., cast, awards).
- **Scalability**: Sharding on `content_id` can distribute data across nodes.
- **Query Performance**: Indexes on reference fields (`content_id`) optimize joins during extraction.
- **Denormalization**: Embedding genres or episode summaries in `content` could reduce lookups, but separate collections are used for normalization in the ETL process.

## Relational Database Design (PostgreSQL)

The relational database uses PostgreSQL with a normalized schema across `raw`, `processed`, and `trusted` schemas to support structured querying and analysis.

### Schema: `raw`
- **Purpose**: Temporary storage for untransformed CSV data.
- **Table: `raw.video_data`**
  - **Columns**:
    - `id`: TEXT (primary key, unique identifier).
    - `title`: TEXT (content title).
    - `type`: TEXT (content type, e.g., "movie" or "series").
    - `release_year`: INTEGER.
    - `genres`: TEXT[] (array of genres).
    - `duration_minutes`: INTEGER (for movies).
    - `season_count`: INTEGER (for series).
    - `episode_count`: INTEGER (for series).
    - `raw_data`: JSONB (raw JSON data from MongoDB for flexibility).
  - **Indexes**: Primary key on `id`.
  - **Notes**: Stores data as ingested, with arrays and JSONB for nested structures.

### Schema: `processed`
- **Purpose**: Normalized data for analysis.
- **Table: `content`**
  - **Columns**:
    - `content_id`: TEXT (primary key).
    - `title`: TEXT.
    - `type`: TEXT (e.g., "movie" or "series").
    - `release_year`: INTEGER.
    - `description`: TEXT.
    - `language`: TEXT.
  - **Indexes**: Primary key on `content_id`.

- **Table: `movie_details`**
  - **Columns**:
    - `content_id`: TEXT (primary key, foreign key to `content.content_id`).
    - `duration_minutes`: INTEGER.
    - `director`: TEXT.
    - `rating`: DOUBLE PRECISION.
  - **Constraints**: Foreign key on `content_id` referencing `content`.

- **Table: `series_details`**
  - **Columns**:
    - `content_id`: TEXT (primary key, foreign key to `content.content_id`).
    - `season_count`: INTEGER.
    - `episode_count`: INTEGER.
    - `creator`: TEXT.
  - **Constraints**: Foreign key on `content_id` referencing `content`.

- **Table: `genres`**
  - **Columns**:
    - `content_id`: TEXT (foreign key to `content.content_id`).
    - `genre`: TEXT.
  - **Constraints**: Primary key on composite `(content_id, genre)`.
  - **Indexes**: Index on `content_id` for joins.

- **Table: `series_episodes`**
  - **Columns**:
    - `content_id`: TEXT (foreign key to `content.content_id`).
    - `season_number`: INTEGER.
    - `episode_number`: INTEGER.
    - `title`: TEXT.
    - `duration_minutes`: INTEGER.
    - `air_date`: DATE.
  - **Constraints**: Primary key on composite `(content_id, season_number, episode_number)`.
  - **Indexes**: Index on `content_id` for joins.

### Schema: `trusted`
- **Purpose**: Analytical views for data analysts.
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
  - **Purpose**: Provides a consolidated view of content with genres as an array.

- **View: `v_episode_details`**
  - **Definition**: 
    ```sql
    SELECT c.title, se.season_number, se.episode_number, se.title AS episode_title, 
           se.duration_minutes, se.air_date
    FROM processed.content c
    JOIN processed.series_details sd ON c.content_id = sd.content_id
    JOIN processed.series_episodes se ON c.content_id = se.content_id;
    ```
  - **Purpose**: Lists episode details for series content.

### Relational Design Considerations
- **Normalization**: Separates content, movie/series details, genres, and episodes into distinct tables to reduce redundancy.
- **Integrity**: Foreign keys ensure referential integrity between tables.
- **Performance**: Indexes on foreign keys and composite primary keys optimize joins and lookups.
- **Scalability**: Partitioning `series_episodes` by `content_id` can improve performance for large datasets.
- **Analyst Access**: Views in `trusted` schema provide pre-aggregated data, accessible by `data_analyst` role with `SELECT` privileges.

## Design Principles
- **Flexibility**: NoSQL supports evolving data structures; relational schema supports structured queries.
- **Consistency**: Normalization in PostgreSQL ensures data integrity; MongoDB allows semi-structured raw data.
- **Security**: Role-based access in PostgreSQL (`data_analyst`) restricts modifications.
- **Efficiency**: Indexes and bulk operations (e.g., `COPY`) optimize data loading and querying.

## Maintenance
- **Updates**: Add new fields to MongoDB collections or PostgreSQL tables via scripts/SQL files.
- **Monitoring**: Check for index usage and storage growth.
- **Backup**: Regular dumps of MongoDB and PostgreSQL databases.

## Troubleshooting
- **Duplicate Keys**: Ensure deduplication during ETL for PostgreSQL.
- **Missing References**: Verify foreign key constraints in `processed` schema.
- **Performance**: Adjust indexes or partitioning if query times increase.

---

## 2. AI Assistance Disclosure

### 2.1 AI Tool and Usage Summary

- **AI Tool Used:** ChatGPT 5-mini  
- **Overall Assistance Level:** 45%  

**Primary Use Cases:**  
- Code generation: 55%  
- Documentation: 35%  
- Debugging: 40%  
- Data analysis: 45%  
- Visualization: 40%

**Human Contributions:**  
- Conceptual design of database architecture (schemas, tables, and relationships)  
- Validation and testing of all SQL and Python scripts  
- Custom optimization of indexes and constraints  
- Integration and validation with the ETL pipeline  

**Verification Process:**  
- Manual review of every AI-generated script  
- Execution and unit testing in PostgreSQL and MongoDB environments  
- Comparison against expected dataset outcomes  

---

### 2.2 Estimation of AI Assistance Percentage

The estimation was calculated according to the **AI-Assistance-Disclosure-Guide** using multiple methods.

#### **Method 1: Time-Based**
- Total hours: 12 h  
- Time using AI: 5.4 h  
- Formula: `(5.4 / 12) × 100 = 45%`

#### **Method 2: Content/Code-Based**
- AI-generated code lines: 450 out of 1000  
- AI-generated documentation words: 900 out of 2000  
- Code estimation: `(450 / 1000) × 100 = 45%`  
- Documentation estimation: `(900 / 2000) × 100 = 45%`

#### **Method 3: Project Components**
| Component | Weight | AI Assistance | Contribution |
|------------|---------|---------------|---------------|
| Data analysis | 25% | 40% | 10% |
| SQL code | 25% | 50% | 12.5% |
| Documentation | 20% | 35% | 7% |
| Debugging | 15% | 40% | 6% |
| Visualization | 15% | 40% | 6% |
| **Total** | **100%** |  | **45.5% ≈ 45%** |

---

### 2.3 Self-Assessment Framework

Each question below is based on the **AI-Assistance-Disclosure-Guide** self-assessment model.

| Question | Description | Self Score (%) |
|-----------|--------------|----------------|
| Q1 | **Initiative and Conceptualization:** Defined the schema and structure independently, AI helped refine relationships. | 40 |
| Q2 | **Implementation:** AI generated SQL and Python templates; heavily modified for production readiness. | 50 |
| Q3 | **Understanding and Validation:** Fully understood AI outputs, validated with test datasets. | 45 |
| Q4 | **Problem Solving:** Identified all errors and applied AI-assisted debugging for query optimization. | 45 |
| **Average** |  | **(40 + 50 + 45 + 45)/4 = 45%** |

---

### 2.4 Final AI Assistance Calculation

Using the formula from the _AI-Assistance-Disclosure-Guide_:

\[
\text{Final AI Assistance %} = (0.25 × \text{Time %}) + (0.35 × \text{Content %}) + (0.25 × \text{Complexity %}) + (0.15 × \text{Self-Assessment})
\]

**Values:**  
Time % = 45  
Content % = 45  
Complexity % = 47.5  
Self-Assessment = 45  

**Computation:**  
`(0.25×45) + (0.35×45) + (0.25×47.5) + (0.15×45) = 45%`

 **Final AI Assistance Percentage: 45%**

---

### 2.5 AI Usage Log Summary

#### **Session 1: Schema Design (MongoDB)**
- **Duration:** 2 h  
- **AI Time:** 1 h  
- **Prompt:** “Design a MongoDB schema for video content with genres, series, and episodes maintaining referential integrity.”  
- **AI Output:** Base JSON schema with collections and references.  
- **Human Contribution:** Adjusted field types, added indexing, and normalization notes.  
- **Assistance Estimate:** 45%

#### **Session 2: SQL Schema and Constraints (PostgreSQL)**
- **Duration:** 2 h  
- **AI Time:** 1 h  
- **Prompt:** “Create normalized SQL scripts for processed and trusted schemas with constraints and indexes for the ETL pipeline.”  
- **AI Output:** Initial DDL scripts.  
- **Human Contribution:** Revised data types, optimized constraints.  
- **Assistance Estimate:** 45%

#### **Session 3: Documentation and Validation**
- **Duration:** 1.5 h  
- **AI Time:** 45 min  
- **Prompt:** “Generate documentation explaining MongoDB and PostgreSQL design principles, normalization, and scalability.”  
- **AI Output:** Structured documentation draft.  
- **Human Contribution:** Rewriting, styling, and adding validation notes.  
- **Assistance Estimate:** 45%

---

### 2.6 Assistance Level Classification

According to the **Assistance Levels by Activity** section of the guide, this project falls under:

- **Level 2: Moderate Assistance (21–50%)**
  - Base structures and templates generated by AI.  
  - Significant human modification and testing.  
  - AI used primarily for code scaffolding and documentation structure.

---

### Summary

This AI disclosure ensures transparency, reproducibility, and accountability for the database design process. The collaboration between human expertise and AI assistance resulted in a consistent, validated, and scalable schema design with a total AI contribution of **45%**.