
#!/bin/bash
set -e

# Script para crear múltiples bases de datos en PostgreSQL
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    -- Crear base de datos para el proyecto de video streaming
    CREATE DATABASE video_streaming;
    
    -- Crear usuario específico para el proyecto (opcional)
    CREATE USER video_user WITH ENCRYPTED PASSWORD 'video_password';
    
    -- Otorgar permisos
    GRANT ALL PRIVILEGES ON DATABASE video_streaming TO video_user;
    GRANT ALL PRIVILEGES ON DATABASE video_streaming TO airflow;

EOSQL

echo "PostgreSQL databases and tables created successfully!"