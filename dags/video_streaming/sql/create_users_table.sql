CREATE TABLE IF NOT EXISTS users (
    user_id VARCHAR(50) PRIMARY KEY,
    age INTEGER CHECK (age >= 0),
    country VARCHAR(100),
    subscription_type VARCHAR(50),
    registration_date DATE,
    total_watch_time_hours FLOAT CHECK (total_watch_time_hours >= 0)
);

-- Index for performance on common queries
CREATE INDEX IF NOT EXISTS idx_users_country ON users(country);
CREATE INDEX IF NOT EXISTS idx_users_registration_date ON users(registration_date);