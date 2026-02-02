-- ===============================
-- RAW DATA TABLE
-- ===============================
-- Stores the full RAWG payload as JSONB for traceability
CREATE TABLE IF NOT EXISTS rawg_games_raw (
    game_id BIGINT PRIMARY KEY,
    payload JSONB NOT NULL,
    ingested_at TIMESTAMPTZ DEFAULT NOW()
);

-- ===============================
-- STRUCTURED FEATURES TABLE
-- ===============================
-- Optimized for analytics and ML
CREATE TABLE IF NOT EXISTS rawg_games (
    game_id BIGINT PRIMARY KEY,
    slug TEXT,
    name TEXT,
    released DATE,
    updated TIMESTAMPTZ,

    rating DOUBLE PRECISION,
    rating_top INT,
    ratings_count INT,
    metacritic INT,

    added INT,
    playtime INT,

    reviews_text_count INT,
    suggestions_count INT,

    reddit_count INT,
    twitch_count INT,
    youtube_count INT,

    has_website BOOLEAN,
    website TEXT,

    processed_at TIMESTAMPTZ DEFAULT NOW()
);

-- ===============================
-- INDEXES (important for ML + API)
-- ===============================
CREATE INDEX IF NOT EXISTS idx_rawg_games_released
    ON rawg_games (released);

CREATE INDEX IF NOT EXISTS idx_rawg_games_rating
    ON rawg_games (rating);

CREATE INDEX IF NOT EXISTS idx_rawg_games_metacritic
    ON rawg_games (metacritic);
