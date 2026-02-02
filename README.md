# GamePulse — RAWG ML API

End-to-end data & ML project using RAWG video game data:
ingestion on AWS, ETL into PostgreSQL, model training, and a FastAPI service for predictions and analytics.

## 🔥 What this project demonstrates
- AWS data ingestion pipeline (Lambda → S3)
- Event-driven ETL (S3 trigger → Lambda → PostgreSQL upsert)
- Clean relational schema + raw JSON storage
- ML training + evaluation (baseline → improved model)
- FastAPI endpoints for prediction + analytics (text & visual)

## 🧱 Architecture
RAWG API → Ingestion Lambda → S3 (raw JSON) → ETL Lambda → PostgreSQL (RDS) → ML Training → FastAPI

## 📦 Repository structure


## ✅ Milestones
- [ ] Create PostgreSQL schema (raw + structured)
- [ ] Ingestion Lambda (RAWG → S3) with state tracking
- [ ] ETL Lambda (S3 → Postgres) with idempotent upsert
- [ ] ML baseline training + evaluation
- [ ] FastAPI `/predict` endpoint
- [ ] Analytics endpoints: `/ask-text` and `/ask-visual`
- [ ] Deployment notes (AWS + Docker)

## 🛡️ Notes
- No secrets are committed. Use AWS SSM / Secrets Manager.
- All SQL queries for analytics are read-only and validated.

## 📍 Status
🚧 In progress — building the first working pipeline end-to-end.
