# Phase 3.4 — API Contracts & Test Collection

**Objective:** Specify every endpoint before you implement it, and write a test request for each one in your API testing tool. The tests fail now and turn green during Phase 5.

**Status:** Submitted · **Last updated:** 2026-10-17

## Done When

- [x] Every endpoint has an ID (EP-01, EP-02, …) and a contract card (Section 3)
- [x] Every Must-Have journey step is covered by an endpoint
- [x] The test collection in `api-specs/` has one request per endpoint, named with its EP-ID

## 1. Conventions (all projects)

- Local base URL `http://localhost:8000`; every route starts with `/api/v1`.
- Request and response bodies are JSON.
- Protected routes need the header `Authorization: Bearer <token>`.
- Every error response uses one shape: `{"error": {"code": "ERROR_CODE", "message": "Readable text", "details": []}}`.
- Status codes: 200 OK, 201 Created, 400 Validation error, 401 Not logged in, 403 Not allowed, 404 Not found, 409 Conflict, 500 Server error.

## 2. API Specification Table

| ID | Method | Endpoint | Description | Auth required | Feature |
|---|---|---|---|---|---|
| EP-01 | GET | /api/v1/health | System health check and status | No | n/a |
| EP-02 | POST | /api/v1/vehicles | Create new vehicle and bind model-component rules | Yes | F-01, F-02 |
| EP-03 | GET | /api/v1/vehicles | List authenticated user's vehicles with reminder statuses | Yes | F-01, F-04 |
| EP-04 | PATCH | /api/v1/vehicles/:vehicleId/odometer | Update odometer reading and re-evaluate reminder states | Yes | F-02, F-04 |
| EP-05 | GET | /api/v1/vehicles/:vehicleId/reminders | Get all active component reminder rules and R/Y/G health | Yes | F-02, F-04 |
| EP-06 | POST | /api/v1/vehicles/:vehicleId/services | Log completed service entry and reset component reminders | Yes | F-03, F-04 |
| EP-07 | GET | /api/v1/vehicles/:vehicleId/services | Retrieve paginated service history logs for vehicle | Yes | F-03 |
| EP-08 | POST | /api/v1/garages | Pin and register a local roadside mechanic or garage | Yes | F-05 |

## 3. Endpoint Contract Cards

### EP-02 — POST /api/v1/vehicles

Request body:

```json
{
  "vehicle_model_id": "9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d",
  "license_plate": "1JJ-8888",
  "current_odometer": 12450
}
```

Success response (201 Created):

```json
{
  "data": {
    "id": "e4a77b80-1a22-4cf4-90a6-5c58c148f980",
    "user_id": "a1b2c3d4-e5f6-7a8b-9c0d-1e2f3a4b5c6d",
    "vehicle_model_id": "9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d",
    "license_plate": "1JJ-8888",
    "current_odometer": 12450,
    "created_at": "2026-10-17T08:30:00.000Z",
    "updated_at": "2026-10-17T08:30:00.000Z",
    "bound_reminders_count": 3
  }
}
```

| Error | When it happens |
|---|---|
| 400 VALIDATION_ERROR | `vehicle_model_id` missing or not a valid UUID; `current_odometer` is negative. |
| 401 UNAUTHORIZED | Missing or expired `Authorization: Bearer <token>` header. |
| 403 FORBIDDEN | n/a |
| 404 NOT_FOUND | `vehicle_model_id` does not exist in `vehicle_models` table. |

---

### EP-03 — GET /api/v1/vehicles

Request body: none

Success response (200 OK):

```json
{
  "data": [
    {
      "id": "e4a77b80-1a22-4cf4-90a6-5c58c148f980",
      "model": {
        "make": "Honda",
        "model": "Scoopy",
        "vehicle_type": "scooter"
      },
      "license_plate": "1JJ-8888",
      "current_odometer": 12450,
      "health_summary": {
        "status": "upcoming",
        "overdue_count": 0,
        "due_soon_count": 0
      }
    }
  ]
}
```

| Error | When it happens |
|---|---|
| 400 VALIDATION_ERROR | n/a |
| 401 UNAUTHORIZED | Missing or invalid Bearer token. |
| 403 FORBIDDEN | n/a |
| 404 NOT_FOUND | n/a |

---

### EP-04 — PATCH /api/v1/vehicles/:vehicleId/odometer

Request body:

```json
{
  "odometer_km": 13500,
  "source": "manual"
}
```

Success response (200 OK):

```json
{
  "data": {
    "vehicle_id": "e4a77b80-1a22-4cf4-90a6-5c58c148f980",
    "previous_odometer": 12450,
    "current_odometer": 13500,
    "updated_reminders": [
      {
        "component_code": "ENGINE_OIL",
        "status": "due_soon",
        "remaining_km": 150,
        "next_due_odometer": 13650
      }
    ]
  }
}
```

| Error | When it happens |
|---|---|
| 400 VALIDATION_ERROR | `odometer_km` is less than `current_odometer` (e.g. attempting to decrease mileage). |
| 401 UNAUTHORIZED | Missing or invalid Bearer token. |
| 403 FORBIDDEN | Authenticated user is not the owner of this vehicle. |
| 404 NOT_FOUND | `vehicleId` not found in `vehicles` table. |

---

### EP-05 — GET /api/v1/vehicles/:vehicleId/reminders

Request body: none

Success response (200 OK):

```json
{
  "data": [
    {
      "id": "f5b88c91-2b33-4de5-81b7-6d69d259e091",
      "component": {
        "code": "ENGINE_OIL",
        "name_en": "Engine Oil",
        "name_km": "ប្រេងម៉ាស៊ីន"
      },
      "interval_km": 1500,
      "interval_days": 90,
      "last_serviced_odometer": 12000,
      "last_serviced_date": "2026-08-01",
      "next_due_odometer": 13500,
      "next_due_date": "2026-10-30",
      "status": "due_soon",
      "remaining_km": 200,
      "remaining_days": 13
    }
  ]
}
```

| Error | When it happens |
|---|---|
| 400 VALIDATION_ERROR | Invalid UUID format in URL path parameter. |
| 401 UNAUTHORIZED | Missing or invalid Bearer token. |
| 403 FORBIDDEN | Authenticated user does not own `vehicleId`. |
| 404 NOT_FOUND | `vehicleId` not found. |

---

### EP-06 — POST /api/v1/vehicles/:vehicleId/services

Request body:

```json
{
  "garage_id": "c3d4e5f6-7a8b-9c0d-1e2f-3a4b5c6d7e8f",
  "service_date": "2026-10-17",
  "odometer_km": 13500,
  "total_cost_cents": 500,
  "currency": "USD",
  "notes": "Changed engine oil with Motul 10W-40 at roadside stall near RUPP",
  "items": [
    {
      "component_code": "ENGINE_OIL",
      "cost_cents": 500,
      "notes": "10W-40 4T Scooter Oil"
    }
  ]
}
```

Success response (201 Created):

```json
{
  "data": {
    "service_log_id": "b7c8d9e0-1f2a-3b4c-5d6e-7f8a9b0c1d2e",
    "vehicle_id": "e4a77b80-1a22-4cf4-90a6-5c58c148f980",
    "odometer_km": 13500,
    "total_cost_cents": 500,
    "reset_reminders": [
      {
        "component_code": "ENGINE_OIL",
        "new_status": "upcoming",
        "next_due_odometer": 15000,
        "next_due_date": "2027-01-15"
      }
    ]
  }
}
```

| Error | When it happens |
|---|---|
| 400 VALIDATION_ERROR | `odometer_km` < previous vehicle odometer; `items` list is empty; `total_cost_cents` is negative. |
| 401 UNAUTHORIZED | Missing or invalid Bearer token. |
| 403 FORBIDDEN | User does not own the vehicle. |
| 404 NOT_FOUND | `vehicleId` or `garage_id` not found. |

---

### EP-07 — GET /api/v1/vehicles/:vehicleId/services

Request body: none

Success response (200 OK):

```json
{
  "data": [
    {
      "id": "b7c8d9e0-1f2a-3b4c-5d6e-7f8a9b0c1d2e",
      "service_date": "2026-10-17",
      "odometer_km": 13500,
      "total_cost_cents": 500,
      "currency": "USD",
      "garage_name": "ជាង រិទ្ធ ជួសជុលម៉ូតូ (Mechanic Rith)",
      "items": [
        {
          "name_km": "ប្រេងម៉ាស៊ីន",
          "name_en": "Engine Oil",
          "cost_cents": 500
        }
      ]
    }
  ]
}
```

| Error | When it happens |
|---|---|
| 400 VALIDATION_ERROR | Invalid UUID format in parameter. |
| 401 UNAUTHORIZED | Missing or invalid Bearer token. |
| 403 FORBIDDEN | User does not own the vehicle. |
| 404 NOT_FOUND | `vehicleId` not found. |

---

### EP-08 — POST /api/v1/garages

Request body:

```json
{
  "name": "ជាង រិទ្ធ ជួសជុលម៉ូតូ (Mechanic Rith)",
  "phone": "+85512888999",
  "address": "Russian Federation Blvd, near RUPP Gate 1, Phnom Penh",
  "latitude": 11.5682710,
  "longitude": 104.8907320
}
```

Success response (201 Created):

```json
{
  "data": {
    "id": "c3d4e5f6-7a8b-9c0d-1e2f-3a4b5c6d7e8f",
    "name": "ជាង រិទ្ធ ជួសជុលម៉ូតូ (Mechanic Rith)",
    "phone": "+85512888999",
    "address": "Russian Federation Blvd, near RUPP Gate 1, Phnom Penh",
    "latitude": 11.5682710,
    "longitude": 104.8907320,
    "is_verified": false,
    "created_at": "2026-10-17T08:45:00.000Z"
  }
}
```

| Error | When it happens |
|---|---|
| 400 VALIDATION_ERROR | `name` is blank; `latitude` not in [-90, 90] or `longitude` not in [-180, 180]. |
| 401 UNAUTHORIZED | Missing or invalid Bearer token. |
| 403 FORBIDDEN | n/a |
| 404 NOT_FOUND | n/a |

## 4. Test Collection

The API test collection is stored as runnable specification files inside `api-specs/`. Each request checks the HTTP status code and response payload structure.

| ID | Request name in collection | Assertions |
|---|---|---|
| EP-01 | EP-01 Health Check | status 200; `status` equals `"ok"`; `timestamp` is ISO-8601 string |
| EP-02 | EP-02 Create Vehicle Profile | status 201; `data.id` is UUID; `data.bound_reminders_count` >= 1 |
| EP-03 | EP-03 List User Vehicles | status 200; `data` is array; `data[0].health_summary.status` exists |
| EP-04 | EP-04 Update Odometer | status 200; `data.current_odometer` equals request `odometer_km` |
| EP-05 | EP-05 Get Vehicle Reminders | status 200; `data` is array; contains `component.name_km` and `status` |
| EP-06 | EP-06 Log Service Entry | status 201; `data.service_log_id` is UUID; `data.reset_reminders` is array |
| EP-07 | EP-07 List Service Logs | status 200; `data` is array; `data[0].total_cost_cents` is integer |
| EP-08 | EP-08 Pin Garage | status 201; `data.id` is UUID; `data.name` equals submitted name |
