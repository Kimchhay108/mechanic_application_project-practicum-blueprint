# Phase 2.1 — MoSCoW Scope Matrix

**Objective:** Decide exactly what you will build, and just as importantly what you will not build. This matrix protects you from scope creep for the rest of the project.

**Status:** Submitted · **Last updated:** 2026-10-17

## Done When

- [x] Every feature has a stable ID (F-01, F-02, …), exactly one priority and a pain point
- [x] At least 3 Won't-Have items are listed

## 1. Priority Rules

| Priority | Rule |
|---|---|
| Must-Have | Without it, the core journey cannot be demonstrated at the defense. |
| Should-Have | Important, but the app still works without it. Built only once all Must-Haves are done. |
| Could-Have | Nice to have (visual polish, extras). Only if time remains. |
| Won't-Have | Explicitly out of scope for this project. Becomes "future work" in your thesis. |

## 2. MoSCoW Matrix

| ID | Feature | Priority | Pain point | Why this priority |
|---|---|---|---|---|
| F-01 | **Multi-Vehicle Profile Management** | Must-Have | PP-03 | Core entity needed for any user journey; users register motorcycles, scooters, or cars with initial odometer readings and model specifications. |
| F-02 | **Dynamic Model-Agnostic Maintenance Rules Engine** | Must-Have | PP-02, PP-03 | Core maintenance logic; database-driven component intervals (`model_component_configs`) allow any vehicle profile to link dynamically to standard components without hardcoded code changes. |
| F-03 | **Rapid Service Logging with Khmer Slang Presets** | Must-Have | PP-01, PP-02 | Essential transaction; lets users log completed maintenance in <10 seconds using authentic garage terms (ប្រេងម៉ាស៊ីន, ខ្សែពាន, ប៊ូស៊ី, ស្បែកហ្វ្រាំង), parts cost, and odometer. |
| F-04 | **Dual-Condition Reminder Engine & R/Y/G Health UI** | Must-Have | PP-02 | Core value proposition; calculates Upcoming (Green), Due Soon (Yellow), and Overdue (Red) states triggered on whichever comes first: mileage or calendar duration. |
| F-05 | **Roadside Mechanic Pinning & Garage Directory** | Must-Have | PP-01 | Enables users to save local roadside mechanic (*chang*) contacts and pin coordinates, alongside pre-seeded Phnom Penh garage listings via Google Places API. |
| F-06 | **Background "At-Garage" 15-Minute Dwell Notification** | Should-Have | PP-01, PP-02 | High-value automation suggested by advisor; background geofence detects 15+ minute dwell time at a garage and prompts: *"Looks like you're at a garage. Do you want to log a service?"*. |
| F-07 | **Service Photo & Receipt Attachment** | Should-Have | PP-01 | Allows users to snap photos of oil bottle labels, odometer clusters, or handwritten mechanic notes attached to service logs for verification. |
| F-08 | **Digital Vehicle Passport & PDF Maintenance Export** | Should-Have | PP-01 | Generates a clean PDF service passport summarizing all verified maintenance logs to preserve vehicle resale provenance. |
| F-09 | **Automated Rainy Season & Traffic Heavy-Wear Multiplier** | Won't-Have | PP-02 | Explicitly deferred per Advisor Feedback #5; automated weather/traffic API integration is complex and out of scope for MVP v1. |
| F-10 | **Live Background GPS Route Tracking & Speedometer** | Won't-Have | PP-02 | Continuous live GPS tracking causes excessive battery drain and phone overheating in Cambodia's climate; periodic manual odometer updates suffice for v1. |
| F-11 | **In-App Garage Booking & Work Order Payments** | Won't-Have | PP-01 | Roadside mechanics operate informally without digital appointment systems; cash and external ABA KHQR remain standard. |

## 3. Scope Changes

| Date | Change | Why |
|---|---|---|
| 2026-10-15 | Added F-05 (Roadside Mechanic Pinning & Google Places Directory) as Must-Have | Incorporated Advisor feedback and student addition to support local Cambodian roadside mechanic logging. |
| 2026-10-15 | Shifted Automated Weather/Traffic Engine (F-09) to Won't-Have (v1) | Advisor Feedback #5 recommended deferring automatic weather and traffic wear calculations to v2 to keep the MVP focused. |
| 2026-10-15 | Added F-06 (15-Minute Garage Dwell Push Notification) as Should-Have | Advisor suggested geofence dwell detection to prompt neglectful commuters (P-01) who forget to log maintenance. |
