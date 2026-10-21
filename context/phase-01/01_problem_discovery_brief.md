# Phase 1.1 — Problem Discovery Brief

**Objective:** Describe the problem, who suffers from it, and why existing solutions are not good enough. Every later decision traces back to this document.

**Status:** Submitted · **Last updated:** 2026-10-17

## Done When

- [x] Every pain point has an ID (PP-01, PP-02, …) that Phase 2 can reference
- [x] The persona refers to specific pain points
- [x] At least 3 existing solutions are compared, each linked to a pain point
- [x] Your unique angle fits in one sentence

## 1. Problem Statement

**Context**

In Cambodia, over 85% of registered vehicles are motorcycles and scooters (notably Honda Dream 125 and Honda Scoopy), alongside a dense urban fleet of Japanese hybrid cars (such as the Toyota Prius 2nd/3rd generation). Urban commuters and commercial couriers navigate severe stop-and-go traffic, extreme tropical heat, and heavy dust or monsoon rain, accelerating component wear on engine oil, drive belts, spark plugs, and brake pads. Over 90% of routine vehicle maintenance is performed by informal roadside mechanics (*chang*) who transact entirely in cash or KHQR transfers without providing paper receipts, itemized invoices, or digital service records. Consequently, vehicle owners rely on fading paper stickers, blurry handwritten oil labels, or fallible memory to track service intervals.

**Pain points**

| ID | Pain point | Who suffers | How often |
|---|---|---|---|
| PP-01 | **Friction of Paperless Roadside Garages**: Informal roadside mechanics (*chang*) never issue printed invoices or digital receipts; riders leave with zero persistent record of parts replaced, oil grade poured, or previous service mileage. | Urban scooter commuters, couriers, and used car owners | Every maintenance visit (every 1,000–3,000 km or 1–3 months) |
| PP-02 | **Silent Mechanical Degradation & Forgetfulness**: Vehicle owners forget routine intervals due to absent proactive alerts, leading to severe component breakdowns (engine seizure from dry oil, snapped CVT drive belts, or brake failure). | Daily commuters and busy delivery drivers | Continuous risk; catastrophic failure occurs every 6–18 months |
| PP-03 | **Western Car-Centric App Incompatibility**: Existing maintenance software is built for Western four-wheel cars with OBD-II telematics, English-only interfaces, and rigid factory schedules, completely lacking scooter components, Khmer mechanic vocabulary, and local climate wear profiles. | Cambodian scooter riders and local mechanics | Every time a user attempts to use existing overseas tracking apps |

**Problem statement in one sentence**

> Cambodian vehicle owners struggle to maintain regular preventive servicing because informal roadside garages issue no paper or digital records and existing apps ignore local two-wheeler needs, which costs owners expensive catastrophic breakdowns (over $80–$250 in engine repairs), lost daily income, and steep resale value depreciation.

## 2. Target User Persona

| Field | P-01 (primary) | P-02 (secondary) |
|---|---|---|
| Name, age, role | **Davy**, 21, undergraduate student at RUPP; rides a 2021 Honda Scoopy. | **Sokha**, 28, full-time Foodpanda delivery courier; rides a 2020 Honda Dream 125. |
| A typical day | Commutes 14 km round-trip through Russian Federation Boulevard between home, campus, and part-time tutoring. Fills gasoline twice weekly and relies on KHQR for payments. | Rides 90–120 km daily across Phnom Penh delivering food orders in heavy traffic, tropical heat, and monsoon rain; vehicle uptime directly dictates daily earnings. |
| Daily struggles | Suffers from **PP-01** and **PP-02**. She never checks the odometer and cannot decipher mechanical jargon. When her oil sticker washes off in the rain, she forgets servicing until the engine begins rattling or overheating. | Suffers from **PP-01**, **PP-02**, and **PP-03**. Accumulates mileage rapidly; roadside mechanics swap his chain or oil in 7 minutes without paper records. Forgetting a chain tightening or oil change risks sudden roadside breakdown during delivery peak hours. |
| Goals | Keep her Scoopy running reliably without learning mechanic jargon; desires a dead-simple Red / Yellow / Green status indicator with a single tap to log a service. | Prevent engine damage and belt snaps; log oil and spark plug changes in under 10 seconds at roadside stalls; track cumulative maintenance expenses. |
| Tech literacy | Medium: Uses iPhone / Android daily for Telegram, TikTok, and ABA Mobile KHQR; abandons apps requiring complex setup or manual configuration. | Medium-Low: Uses Android smartphone for delivery driver apps, Google Maps, and ABA KHQR; requires high-contrast UI, Khmer language, and minimal typing. |
| What they would say about the problem | *"I don't know what a CVT belt or transmission oil is. I just need my phone to tell me in plain Khmer when to visit the mechanic near campus so my bike doesn't stall on the road."* | *"I ride 100 km every single day. If my Honda Dream seizes an engine valve because I forgot an oil change, I lose three days of food delivery wages and pay $120 to rebuild the cylinder head."* |

## 3. Domain Terminology

| Term | Definition in this project | Synonyms to avoid | Business rule |
|---|---|---|---|
| **Vehicle Profile** | A registered motorcycle, scooter, or car owned by the user, linked to a specific make, model, year, and starting odometer reading. | Account, Asset, Car | A user can register multiple vehicles; each vehicle has exactly one active status. |
| **Engine Oil (ប្រេងម៉ាស៊ីន)** | Motor lubrication fluid (*Preng Masin*); primary consumable for scooters, motorcycles, and passenger cars. | Lubricant, Motor Fluid | Trigger interval is evaluated on whichever occurs first: cumulative mileage limit or elapsed calendar threshold. |
| **Drive Belt (ខ្សែពាន)** | Continuous rubber CVT transmission belt (*Ksae Pean*) found on automatic scooters (e.g., Scoopy, Click). | Transmission chain, Fan belt | Applicable only to automatic scooters; triggers visual inspection and replacement alert before physical snapping. |
| **Spark Plug (ប៊ូស៊ី)** | Ignition plug (*Bousi* / *Bougie*) responsible for engine cylinder combustion. | Igniter, Electric plug | Tracked based on cumulative engine running mileage. |
| **Brake Pads (ស្បែកហ្វ្រាំង)** | Friction lining (*Sbaek Frang*) for drum or disc brake assemblies. | Brake shoes, Calipers | Evaluated based on service logs and wear multiplier factors. |
| **Roadside Mechanic (ជាង / Chang)** | Informal local garage or neighborhood repair stall providing physical maintenance. | Dealership, Auto Shop, Agency | Users can log services done by any roadside mechanic, save the shop name/phone, and pin shop coordinates. |
| **Service Log** | An immutable timestamped record of a completed maintenance event, containing odometer reading, tasks completed, parts cost, and optional shop details. | Booking, Invoice, Ticket | Once created, a service log automatically resets the corresponding maintenance reminder counters. |
| **Reminder State** | The real-time health indicator of a maintenance task: `Upcoming` (Green, >20% remaining), `Due Soon` (Yellow, ≤20% remaining or ≤7 days), `Overdue` (Red, 0 km or 0 days remaining), and `Serviced` (Completed). | Pending, Expired, Active | Calculated dynamically from current odometer and date against the model's component configuration. |

## 4. Competitor / Existing Solution Teardown

| Existing solution | Type | What it does well | Why it is inadequate (refer to PP-xx) |
|---|---|---|---|
| **Drivvo** | Mobile App (Global) | Rich graphs, multi-currency support, expense categorization for Western cars. | Inadequate for **PP-02** and **PP-03**: Cluttered with 15+ required fields per entry; no two-wheeler presets; no Khmer language or local mechanic slang; assumes OBD-II sync and formal garage invoices. |
| **Fuelio** | Mobile App (Global) | Clean fuel fill-up tracking, bi-metric odometer inputs, GPS trip logging. | Inadequate for **PP-01** and **PP-03**: Focused primarily on petrol fill-ups rather than scheduled component wear; lacks dual-condition triggers for scooters; no automatic garage visit detection; Western terminology alienates Cambodian commuters. |
| **Faded Paper Oil Sticker & Memory** | Manual physical process | Zero barrier to entry; mechanic writes date/km with ballpoint pen on a sticker pasted to the front fork or chassis. | Inadequate for **PP-01** and **PP-02**: Paper stickers peel off or blur under tropical rain, mud, and bike washes; provides no audible or push alerts; forgotten by 80% of commuters until mechanical failure occurs. |

**Your unique angle**

> A hyper-local, bilingual Khmer-English vehicle maintenance companion tailored for Cambodia's scooters and cars that combines model-agnostic component configs with automated 15-minute roadside garage dwell reminders and a 1-tap service logging interface.
