# Phase 2.2 — Core User Journeys

**Objective:** Describe the 5–8 most important things users do with your app, step by step, including what happens when something goes wrong. These journeys become your screens (Phase 4), your demo (Phase 6) and your test cases (Phase 7).

**Status:** Submitted · **Last updated:** 2026-10-17

## Done When

- [x] 5 to 8 journeys (UJ-01 … UJ-08), written in Given / When / Then form
- [x] Each journey has a happy path and at least one failure or edge-case path
- [x] Every Must-Have feature appears in the coverage table
- [x] Personas and terms match Phase 1

## 1. Writing Rules

- **Given** describes the starting situation, **When** the user's action, and **Then** the visible result.
- One action per **When**. Use **And** for extra steps.
- **Then** must be something you can check, such as a message, a screen or a saved record.

## 2. Journeys

### UJ-01 — Vehicle Registration & Preset Rules Binding

| Persona | Trigger | Pre-conditions | Features |
|---|---|---|---|
| P-01 (Davy) | User downloads the app to track her newly purchased used scooter. | App installed; user authenticated via phone number. | F-01, F-02 |

```gherkin
Scenario: Happy path
  Given Davy is on the "Add Vehicle" screen
  When she selects vehicle type "Motorcycle/Scooter", make "Honda", model "Scoopy", and year "2021"
  And she enters current odometer reading "12450" km
  And she taps "Save Vehicle"
  Then the system creates the vehicle profile
  And the system binds default model-component configs for Engine Oil (1,500 km / 90 days), Drive Belt (12,000 km / 365 days), and Spark Plug (8,000 km / 365 days)
  And Davy sees the Vehicle Dashboard displaying Green status indicators for all components

Scenario: Failure or edge case
  Given Davy is entering her vehicle details
  When she inputs an odometer reading of "-50" or leaves the field blank
  And she taps "Save Vehicle"
  Then the system highlights the odometer input with an error "Please enter a valid positive odometer reading"
  And no vehicle profile or component configs are saved
```

---

### UJ-02 — Rapid 1-Tap Service Logging with Khmer Slang Presets

| Persona | Trigger | Pre-conditions | Features |
|---|---|---|---|
| P-01 (Davy) | Davy just finished changing her engine oil at a roadside mechanic stall near campus. | Davy has an active vehicle profile; currently parked at the stall. | F-03, F-04 |

```gherkin
Scenario: Happy path
  Given Davy opens the app at the roadside shop
  When she taps the quick-action button "+ កត់ត្រាការជួសជុល (Log Service)"
  And she selects the preset tag "ប្រេងម៉ាស៊ីន (Engine Oil)"
  And she confirms current odometer "13500" km and enters cost "5.00" USD
  And she taps "រក្សាទុក (Save Record)"
  Then the system creates an immutable Service Log entry
  And the system resets the Engine Oil reminder counter to 0 km and 0 elapsed days
  And the dashboard displays the Engine Oil card in Green state: "1,500 km remaining"

Scenario: Failure or edge case
  Given Davy is entering a new service log
  When she enters an odometer reading of "11000" km, which is lower than the last recorded reading of "12450" km
  And she attempts to save the record
  Then the system displays an alert modal: "Odometer cannot be less than previous record (12,450 km)"
  And the log is blocked until a valid higher reading is entered
```

---

### UJ-03 — "At-Garage" 15-Minute Dwell Notification & Fast Log

| Persona | Trigger | Pre-conditions | Features |
|---|---|---|---|
| P-01 (Davy) | Davy arrives at a roadside repair stall and waits 15 minutes while her scooter is serviced. | Location permission granted; background geofence active; stall is pinned or detected via Google Places. | F-05, F-06, F-03 |

```gherkin
Scenario: Happy path
  Given Davy's device has been stationary within 50 meters of a known garage for 15 minutes
  When the background dwell timer reaches 15 minutes
  Then the system dispatches a local push notification: "Looks like you're at a garage. Do you want to log a service?"
  When Davy taps the push notification
  Then the app opens directly to the Log Service form pre-populated with the garage name and current date
  And Davy confirms the service item "ប៊ូស៊ី (Spark Plug)" with 1 tap

Scenario: Failure or edge case
  Given Davy is merely sitting at an adjacent coffee shop for 20 minutes near the garage
  When the push notification arrives: "Looks like you're at a garage. Do you want to log a service?"
  And Davy swipes the notification away or taps "Not at garage"
  Then the system dismisses the prompt without creating any service log and suppresses garage notifications for 12 hours
```

---

### UJ-04 — Resolving Overdue Alert via Odometer Update

| Persona | Trigger | Pre-conditions | Features |
|---|---|---|---|
| P-02 (Sokha) | Sokha receives a weekly push alert reminding him to update his delivery mileage. | Sokha rides a Honda Dream 125; last odometer recorded was 18,200 km. | F-02, F-04 |

```gherkin
Scenario: Happy path
  Given Sokha opens the app after 10 days of heavy delivery riding
  When he taps "Update Odometer" and inputs "19850" km
  Then the system re-evaluates all component reminder rules against the new odometer
  And the system detects Engine Oil has exceeded the 1,500 km threshold (1,650 km ridden)
  Then the Engine Oil card switches to Red Overdue state with alert: "Overdue by 150 km! Change engine oil immediately to prevent engine seizure."
  When Sokha logs an engine oil change service
  Then the status card returns to Green

Scenario: Failure or edge case
  Given Sokha mistakenly types an extra digit, entering "198500" km instead of "19850" km
  When he taps "Confirm Odometer"
  Then the system displays a warning: "This update increases mileage by 180,300 km. Please verify your odometer photo or reading."
  And requires explicit re-confirmation before applying the update
```

---

### UJ-05 — Pinning a Roadside Mechanic & Garage Directory Search

| Persona | Trigger | Pre-conditions | Features |
|---|---|---|---|
| P-01 (Davy) | Davy discovers a skilled and honest neighborhood mechanic (*chang*) and wants to remember the shop. | App open; GPS active. | F-05 |

```gherkin
Scenario: Happy path
  Given Davy is on the "Garages" screen
  When she taps "Pin My Mechanic (+ បន្ថែមជាងម៉ូតូ)"
  And she enters shop name "ជាង រិទ្ធ ជួសជុលម៉ូតូ (Mechanic Rith)", phone "012888999", and confirms current GPS pin
  And she taps "Save Mechanic"
  Then the mechanic is saved to her personal garage directory
  And the shop location is registered for future 15-minute background dwell detection

Scenario: Failure or edge case
  Given Davy searches for nearby garages but has no internet connection
  When she queries the garage directory
  Then the app loads cached local mechanics and user-pinned shops from the local SQLite database
  And displays an offline banner: "Showing offline saved garages. Connect to internet for live Google Places search."
```

---

### UJ-06 — Generating Digital Vehicle Passport & PDF Export

| Persona | Trigger | Pre-conditions | Features |
|---|---|---|---|
| P-02 (Sokha) | Sokha is selling his Honda Dream 125 and wants to prove to the buyer that it was regularly serviced. | Vehicle has 10+ completed service logs stored in database. | F-07, F-08 |

```gherkin
Scenario: Happy path
  Given Sokha navigates to the Vehicle Settings menu
  When he selects "Export Digital Maintenance Passport (PDF)"
  And he selects date range "All Time" and taps "Generate PDF"
  Then the app compiles vehicle specs, total expenditure ($86.50), and chronological table of service logs with mechanic names and odometer readings
  And opens the native share sheet allowing Sokha to send the PDF via Telegram to the prospective buyer

Scenario: Failure or edge case
  Given a new user with 0 completed service logs attempts to export a PDF passport
  When the user taps "Export Digital Maintenance Passport"
  Then the system displays an empty state dialog: "No service logs found. Complete at least one maintenance log before generating a passport."
  And PDF generation is cancelled
```

## 3. Coverage

| Must-Have feature | Covered by journey(s) |
|---|---|
| F-01 Multi-Vehicle Profile Management | UJ-01 |
| F-02 Dynamic Model-Agnostic Maintenance Rules Engine | UJ-01, UJ-04 |
| F-03 Rapid Service Logging with Khmer Slang Presets | UJ-02, UJ-03 |
| F-04 Dual-Condition Reminder Engine & R/Y/G Health UI | UJ-02, UJ-04 |
| F-05 Roadside Mechanic Pinning & Garage Directory | UJ-03, UJ-05 |
