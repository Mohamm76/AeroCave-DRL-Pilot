
-- database/init.sql

-- إنشاء جدول سجلات الطيران (Flight Logs)
CREATE TABLE IF NOT EXISTS flight_logs (
    id SERIAL PRIMARY KEY,
    session_id VARCHAR(50) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    step_number INT NOT NULL,
    pos_x FLOAT NOT NULL,
    pos_y FLOAT NOT NULL,
    pos_z FLOAT NOT NULL,
    vel_x FLOAT NOT NULL,
    vel_y FLOAT NOT NULL,
    vel_z FLOAT NOT NULL,
    battery_level FLOAT NOT NULL DEFAULT 100.0,
    current_algorithm VARCHAR(20) NOT NULL DEFAULT 'PPO',
    status VARCHAR(20) NOT NULL DEFAULT 'FLYING', -- 'FLYING', 'CRASHED', 'FINISHED'
    reward FLOAT NOT NULL
);

-- إنشاء فهرس (Index) لتسريع استعلامات البث المباشر حسب الجلسة
CREATE INDEX IF NOT EXISTS idx_session_id ON flight_logs(session_id);