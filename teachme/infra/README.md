# TeachMe Infrastructure

This directory contains local development tooling for the TeachMe monorepo.

## Services

- **API** – FastAPI application that powers lesson generation.
- **Worker** – Background worker for cache warming and experimentation.
- **Redis** – Cache storage for generated lessons.
- **Postgres** – Persistent store for feedback and telemetry.

## Usage

```sh
docker compose up --build
```

This command launches the full stack locally.
