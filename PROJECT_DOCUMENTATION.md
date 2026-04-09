# MetalSense Project Documentation

## Overview
MetalSense is a full-stack web application designed to monitor, track, and visualize environmental pollution (specifically heavy metals). The platform caters to different roles, such as Citizens for viewing data, and Researchers for uploading and processing datasets.

## Architecture
- **Frontend**: React 19 (TypeScript, Vite), Zustand context, Leaflet mapping, Recharts.
- **Backend**: Python FastAPI, SQLAlchemy (SQLite/PostgreSQL compatible), Pandas for data processing.
- **Database**: 8 core tables tracking users, spatial samples, raw measurements, processed risk indices, and educational content.

## Database Schema (8 Tables)
1. `users` - Manages authenticated accounts and roles (citizen vs researcher).
2. `datasets` - Tracks bulk CSV uploads initiated by researchers.
3. `samples` - Primary spatial entity tracking lat/lng and time of collection.
4. `measurements` - Raw value tracking for individual metal types (e.g. As, Pb, Hg) mapped to samples.
5. `risk_assessments` - Stores computed algorithmic indexes like HPI (Heavy Metal Pollution Index) and generic `risk_category`.
6. `heavy_metals` - Core dictionary of metals including symbol, safety limit standards, and health effects.
7. `education_materials` - Articles and facts linked to heavy metals for the educational dashboard.
8. `user_logs` - Audit table tracking researchers' actions and processed uploads.

## Key Added Features
1. **Authentication API**: Secure `/api/v1/auth/login` and `/api/v1/users/register` routes using JWT.
2. **Researcher Data Pipeline**:
   - `POST /api/v1/researcher/upload-csv`
   - Accepts CSV files, parses via Pandas, and automatically injects them into the spatial map database.
3. **Education Dashboard**:
   - `GET /api/v1/education/metals`
   - Drives understanding of environmental health factors.
4. **Dynamic Mapping**: The `MapView` now dynamically reads from the SQL backend, adjusting heatmaps and popup colors according to specific health risk parameters.

## Testing Setup
- `pytest` has been utilized for testcases.
- To run tests: Navigate to backend, activate venv, execute `pytest tests/test_api.py`.
