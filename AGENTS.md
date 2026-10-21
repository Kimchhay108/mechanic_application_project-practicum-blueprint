# Agent Instructions

This is a solo Bachelor capstone monorepo. The student's planning documents in `context/` are the source of truth. Read the relevant ones before doing any work.

## Context, in reading order

1. `README.md`: project summary and current progress
2. `context/phase-01/`: the problem, users and domain terms
3. `context/phase-02/`: scope (MoSCoW matrix) and user journeys
4. `context/phase-03/`: tech stack, architecture, database design and API contracts
5. `context/phase-04/`: screens and design tokens (starts Phase 4)
6. `context/phase-05/` to `context/phase-08/`: implementation, testing and thesis records, once they exist

## Rules

- Never edit anything in `template/`. It belongs to the advisor.
- Only build features listed in the MoSCoW matrix, following its priority rules. Won't-Haves and unlisted features need a scope change entry first.
- Implement endpoints exactly as the API contracts specify. If a contract must change, update the contract document first.
- An endpoint must pass in the API test collection (`api-specs/`) before any screen uses it.
- Use the domain terms from Phase 1.1 for names in code, the database and the UI.
- Never commit secrets. Real values go in git-ignored `.env` files; keep `.env.example` up to date.
- After finishing a task, update the matching tracker in `context/` and the Progress section of `README.md`.

## Stack and commands

- **Mobile Client:** Flutter SDK (v3.24) with Dart (v3.5) and Riverpod (v2.5) state management. Local offline cache using Drift (SQLite v3).
- **Backend API:** Node.js (v20 LTS) + Express.js (v4.19) with TypeScript (v5.4). REST API on port 8000 (`/api/v1`).
- **Database:** PostgreSQL (v16) running via Docker Compose.
- **Authentication:** JWT Bearer tokens (`Authorization: Bearer <token>`).
- **API Specs:** Postman / Bruno collection in `api-specs/motocare_api_collection.json`.

```bash
# Start backend database
docker compose up -d

# Install backend dependencies & start development server
npm install
npm run dev

# Run API test suite
npm run test:api

# Run Flutter mobile client
cd mobile && flutter pub get && flutter run
```
