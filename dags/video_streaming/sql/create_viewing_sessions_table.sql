CREATE TABLE IF NOT EXISTS viewing_sessions (
    session_id VARCHAR(50) PRIMARY KEY,
    user_id VARCHAR(50) REFERENCES users(user_id) ON DELETE CASCADE,
    content_id VARCHAR(50),
    watch_date DATE,
    watch_duration_minutes INTEGER CHECK (watch_duration_minutes >= 0),
    completion_percentage FLOAT CHECK (completion_percentage BETWEEN 0 AND 100),
    device_type VARCHAR(50),
    quality_level VARCHAR(20)
);

-- Indexes for performance on joins and filters
CREATE INDEX IF NOT EXISTS idx_viewing_sessions_user_id ON viewing_sessions(user_id);
CREATE INDEX IF NOT EXISTS idx_viewing_sessions_content_id ON viewing_sessions(content_id);
CREATE INDEX IF NOT EXISTS idx_viewing_sessions_watch_date ON viewing_sessions(watch_date);