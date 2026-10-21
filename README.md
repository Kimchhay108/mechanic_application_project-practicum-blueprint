# MotoCare Cambodia — Intelligent Vehicle Maintenance Tracker

Bachelor of Computer Science — Individual Capstone

| | |
|---|---|
| Student | Kimchhay |
| Advisor | Hang Sopheak |
| Term |  Year 4, Semester 1  |
| Pitch | A hyper-local vehicle maintenance companion for Cambodian scooter riders and car owners that automates preventive servicing with authentic Khmer mechanic slang, dynamic component configs, and 15-minute roadside garage dwell reminders. |

First time here? Read the guide: [template/README.md](template/README.md)

## Progress

Update this section whenever you work on a phase. Your advisor reads it to follow your progress.

| | |
|---|---|
| Now working on | Phase 3 complete (Deliverables ready for Saturday 17 October review) |
| Blockers | None |
| Last updated | 2026-10-17 |

| Phase | Planned due | Status | Submitted on |
|---|---|---|---|
| 1. Domain & Problem Teardown | Week 2 | Submitted | 2026-10-17 |
| 2. Scope, Logic & MoSCoW | Week 3 | Submitted | 2026-10-17 |
| 3. Architecture, ERD & API Planning | Week 4-5 | Submitted | 2026-10-17 |
| 4. UI/UX & Figma Design | Week 6-7 | Not started | |
| 5. Backend Core & API Implementation | Week 8-10 | Not started | |
| 6. Frontend Client & Integration | Week 11-13 | Not started | |
| 7. QA, Bug Fixes & Test Report | Week 14 | Not started | |
| 8. Code Freeze, Final Report & Defense | Week 15-16 | Not started | |

Status values: Not started · In progress · Submitted · Rework needed

## Links

| Item | Link |
|---|---|
| Figma file | *To be added in Phase 4* |
| Figma prototype | *To be added in Phase 4* |
| Alpha demo video | *To be added in Phase 6* |
| Thesis | *To be added in Phase 8* |
| Defense slides | *To be added in Phase 8* |

## How to Run

*Development commands (Phase 5 onward):*

```bash
# 1. Start PostgreSQL database with Docker
docker compose up -d

# 2. Run database migrations and seed data
npm run db:migrate
npm run db:seed

# 3. Start API server on port 8000
npm run dev

# 4. Run API contract tests
npm run test:api

# 5. Start Flutter mobile client
cd mobile && flutter run
```

## Repository Layout

| Path | Contents |
|---|---|
| `template/` | Guide and phase templates from the advisor (do not edit) |
| `context/` | My completed phase documents and evidence (Phase 1, 2, and 3) |
| `backend/` | Backend code (starts Phase 5) |
| `mobile/` | Client app code (starts Phase 6) |
| `api-specs/` | API test collection (Postman / Bruno collection) |
| `AGENTS.md` | Instructions for AI coding assistants |
