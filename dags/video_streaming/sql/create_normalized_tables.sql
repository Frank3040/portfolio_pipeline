-- Drop tables if they exist to ensure clean schema creation
DROP TABLE IF EXISTS series_episodes CASCADE;
DROP TABLE IF EXISTS content_genres CASCADE;
DROP TABLE IF EXISTS series_details CASCADE;
DROP TABLE IF EXISTS movie_details CASCADE;
DROP TABLE IF EXISTS content CASCADE;

-- Create content table
CREATE TABLE content (
    content_id VARCHAR(50) PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    type VARCHAR(50) NOT NULL CHECK (type IN ('movie', 'series')),
    rating FLOAT CHECK (rating >= 0 AND rating <= 10),
    production_budget DECIMAL(15, 2)
);

-- Create movie_details table
CREATE TABLE movie_details (
    content_id VARCHAR(50) PRIMARY KEY,
    duration_minutes INT CHECK (duration_minutes > 0),
    release_year INT CHECK (release_year >= 1888),
    views_count BIGINT CHECK (views_count >= 0),
    FOREIGN KEY (content_id) REFERENCES content(content_id) ON DELETE CASCADE
);

-- Create series_details table
CREATE TABLE series_details (
    content_id VARCHAR(50) PRIMARY KEY,
    seasons INT CHECK (seasons > 0),
    avg_episode_duration INT CHECK (avg_episode_duration > 0),
    total_views BIGINT CHECK (total_views >= 0),
    FOREIGN KEY (content_id) REFERENCES content(content_id) ON DELETE CASCADE
);

-- Create content_genres table
CREATE TABLE content_genres (
    content_id VARCHAR(50),
    genre VARCHAR(50) NOT NULL,
    PRIMARY KEY (content_id, genre),
    FOREIGN KEY (content_id) REFERENCES content(content_id) ON DELETE CASCADE
);

-- Create series_episodes table
CREATE TABLE series_episodes (
    content_id VARCHAR(50),
    season INT CHECK (season > 0),
    episode_count INT CHECK (episode_count > 0),
    PRIMARY KEY (content_id, season),
    FOREIGN KEY (content_id) REFERENCES content(content_id) ON DELETE CASCADE
);

-- Create indexes for performance
CREATE INDEX idx_content_type ON content(type);
CREATE INDEX idx_movie_details_release_year ON movie_details(release_year);
CREATE INDEX idx_series_details_seasons ON series_details(seasons);
CREATE INDEX idx_content_genres_genre ON content_genres(genre);
CREATE INDEX idx_series_episodes_season ON series_episodes(season);