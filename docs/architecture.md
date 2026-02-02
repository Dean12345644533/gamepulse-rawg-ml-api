# Architecture — GamePulse

This project follows a simple, production-oriented architecture for data ingestion, processing, storage, and serving ML predictions.

## High-level flow

1. **Ingestion (AWS Lambda)**
   - Calls the RAWG API
   - Fetches game details
   - Stores raw JSON into S3 (`rawg/games/...`)

2. **Processing / ETL (AWS Lambda triggered by S3)**
   - Triggered whenever a new JSON is uploaded to S3
   - Normalizes the payload
   - Upserts structured data into PostgreSQL (RDS)

3. **Storage (PostgreSQL)**
   - `rawg_games_raw` stores the full JSON payload (traceability)
   - `rawg_games` stores structured features (analytics & ML)

4. **ML training**
   - Uses the structured table to train predictive models
   - Produces evaluation metrics and exports a model artifact

5. **API layer (FastAPI)**
   - `/predict` endpoint uses the trained model to return predictions
   - Future endpoints:
     - `/ask-text` for safe analytics (text → SQL → response)
     - `/ask-visual` for chart responses (SQL → matplotlib → PNG)

## Design principles

- **Idempotent processing**
  - ETL uses `ON CONFLICT DO UPDATE` so reprocessing the same game does not duplicate rows.

- **Raw + Structured storage**
  - Raw JSON is kept for auditing and future reprocessing.
  - Structured tables enable fast analytics and ML.

- **Separation of concerns**
  - Ingestion is isolated from ETL to keep responsibilities clear and maintainable.

## Data contracts

- Ingestion writes: `s3://<bucket>/rawg/games/<game_id>_<timestamp>.json`
- ETL reads: RAWG JSON payload (single game detail)
- ETL writes: `rawg_games` (structured row per game)

## Future improvements

- Store DB credentials in AWS Secrets Manager / SSM
- Add DLQ + retry strategy for failed events
- Add CI checks (linting, formatting, tests)
- Add IaC (Terraform / SAM) for reproducible deployments
