# Phase 3.1 — Tech Stack & Feasibility

**Objective:** Choose a tech stack that fits your Must-Have features and that you can deliver alone, list the external services those features need, and plan for what could go wrong.

**Status:** Submitted · **Last updated:** 2026-10-17

## Done When

- [x] Every stack layer has a choice, a version and a reason
- [x] Every external service has a fallback
- [x] Your stack is written in `AGENTS.md`

## 1. Tech Stack Selection & Justification

| Layer | Your choice (with version) | Alternative considered | Why this choice |
|---|---|---|---|
| Backend language & framework | **Node.js (v20 LTS) + Express.js (v4.19) with TypeScript (v5.4)** | Python (FastAPI), Dart (Frog) | High industry adoption in Cambodia, fast JSON serialization, excellent TypeScript type safety shared across models, and lightweight deployment to local port 8000. |
| Database | **PostgreSQL (v16) via Docker Compose; Drift (SQLite v3) on mobile client** | MongoDB, MySQL | Relational schema with strict foreign keys and check constraints is essential for immutable service logs, model configs, and reminder rule states. Drift provides zero-latency offline storage on mobile. |
| Client (mobile or web) | **Flutter SDK (v3.24) with Dart (v3.5) and Riverpod (v2.5)** | React Native, Native Android (Kotlin) | Single codebase for iOS and Android; compiles to high-performance native ARM code; rich widget ecosystem for responsive Cambodian Khmer Unicode typography. |
| Authentication | **JWT (JSON Web Tokens) with bcrypt password hashing** | Supabase Auth, Firebase Auth | Complete control over auth payload and bearer tokens; lightweight, zero vendor lock-in, and strictly follows the capstone requirement `Authorization: Bearer <token>`. |
| API testing tool | **Bruno (v1.30) & Postman Collection (v2.1)** | Insomnia, cURL | Text-based collection files committed directly to `api-specs/`; easily runs in Git workflows and allows reproducible status and body assertion tests. |
| Hosting / running locally | **Docker Compose (v2.27) for PostgreSQL; Node runtime on `http://localhost:8000`** | Pure cloud deployment (AWS/GCP) | Zero-cost local development environment guaranteeing repeatable database initialization, migrations, and local seed scripts. |

## 2. Third-Party Service Dependencies

| Service | Purpose | Provider | Free-tier limit | Fallback if it fails |
|---|---|---|---|---|
| **Google Places API (Nearby Search)** | Pre-seed and search verified motorcycle garages and auto repair shops across Phnom Penh (F-05). | Google Cloud Platform | $200 monthly free credit (~28,000 requests) | App falls back to local database seed of pre-collected Phnom Penh garages and user-pinned custom garage coordinates. |
| **Native Geofence & Dwell Detection** | Background monitoring for 15+ minute dwell time near known garages (F-06). | Native Android Geofencing / iOS CoreLocation via Flutter `geofence_service` | 100% free (device-native operating system API) | In-app foreground location check when user opens the app, plus manual mechanic pinning. |
| **Local Device Notifications** | Proactive reminders for overdue maintenance (F-04) and garage dwell prompts (F-06). | `flutter_local_notifications` (v17.x) | 100% free (device-native OS notification tray) | Visual badge counters and high-contrast Red / Yellow / Green dashboard cards on app launch. |
| **Receipt / Invoice Media Storage** | Storing camera snapshots of mechanic notes, oil labels, and odometers (F-07). | Supabase Storage / Local app filesystem cache | 1 GB free bucket storage | Local device document directory cache; photos remain viewable locally even if cloud upload is pending. |

## 3. Top Risks

| Risk | What you'll do about it |
|---|---|
| **Battery drain from continuous background location tracking** | Do not run continuous GPS polling. Use OS-level passive geofencing circular regions (radius 50m) with 15-minute dwell filters, requiring zero CPU wakeups until entering garage boundaries. |
| **Neglectful users forgetting to update odometer readings** | Implement automated weekly push check-in prompts ("Quick tap: what's your current km?"), and calculate estimated wear using daily mileage heuristics (e.g. 15 km/day for student commuters, 90 km/day for couriers). |
| **Offline usage at rural roadside stalls with zero cellular coverage** | Architect Flutter client with Drift (SQLite) local-first storage. Users can log services, view reminder states, and pin mechanics offline; sync queue pushes changes to backend API once connectivity returns. |
| **Inaccurate mechanic terminology across different Cambodian provinces** | Seed the database with authentic colloquial Khmer mechanic slang (ប្រេងម៉ាស៊ីន, ខ្សែពាន, ប៊ូស៊ី, ស្បែកហ្វ្រាំង) with dual English subtitles, ensuring immediate comprehension across all user personas. |
