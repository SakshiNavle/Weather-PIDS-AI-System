# PIDS Calibration AI — Frontend Dashboard

React + TypeScript + Vite frontend for the Weather-Based Sensor Calibration Suggestion System (PIDS). Consumes the FastAPI backend at `/api/v1` — no hardcoded data.

## Setup

```bash
npm install
cp .env.example .env   # adjust VITE_API_BASE_URL if your backend isn't on 127.0.0.1:8000
npm run dev
```

Build for production:

```bash
npm run build
```

## Backend expectations

This frontend was built against the endpoint shapes described in the project brief:

- `GET /api/v1/dashboard`
- `GET /api/v1/sensors`, `POST /api/v1/sensors`, `GET/PUT/DELETE /api/v1/sensors/{id}`
- `GET /api/v1/weather/history`
- `GET /api/v1/predictions`, `GET /api/v1/predictions/sensor/{id}`, `POST /api/v1/predictions/run?sensor_id=`, `POST /api/v1/predictions/run-all`
- `GET /api/v1/recommendations`, `GET /api/v1/recommendations/risk/{level}`, `GET /api/v1/recommendations/sensor/{id}`
- `GET /api/v1/alerts`, `GET /api/v1/alerts/{id}`, `DELETE /api/v1/alerts/{id}`

**Before running against your real backend**, open `http://127.0.0.1:8000/docs` and confirm these paths and response fields match exactly — your repo tree shows `alerts.py`, `predictions.py`, `recommendations.py`, `sensors.py`, `weather.py`, `dashboard.py` routers, but I don't have their route bodies, so a couple of endpoint names above are my best inference from your spec (flagged below) and may need a one-line tweak in the matching `src/api/*.ts` file:

- `weather/current` (used for a possible standalone "current weather" endpoint) — if your `weather.py` only exposes `/weather/history`, the app already falls back to `history[0]` on the Weather and Dashboard pages, so this is safe either way.
- `predictions/run?sensor_id=` — confirm whether your backend expects a query param or a path param (`/predictions/run/{sensor_id}`); adjust `src/api/predictionApi.ts` if it's the latter.
- `alerts/{id}` DELETE for deactivation — confirm your `alerts.py` actually supports delete/deactivate; if not, remove the action from `AlertDetailModal`.

## Project structure

See `src/` — `api/` (axios services), `types/`, `hooks/` (polling + backend status), `components/` (layout, dashboard, sensors, weather, predictions, recommendations, alerts, common), `pages/`, `styles/` (design tokens + shared CSS).

## Design

Dark industrial IoT theme — Space Grotesk (display) + IBM Plex Mono (data/numbers) + Inter (body), cyan-teal accent, four-tier risk color scale (LOW/MEDIUM/HIGH/SEVERE). Signature element: the segmented radial risk gauge on the dashboard.
