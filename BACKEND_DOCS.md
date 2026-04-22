# MetalSense Backend Documentation

## Overview
MetalSense is a spatial water quality analytics platform designed for researchers and citizens. The backend is built with **FastAPI**, providing a high-performance, asynchronous API for handling large environmental datasets, calculated risk indices, and role-based access control.

---

## 1. Technical Stack
- **Framework**: FastAPI (Python)
- **Database**: SQLite (via SQLAlchemy ORM)
- **Data Processing**: Pandas (CSV parsing)
- **Security**: OAuth2 with JWT (JSON Web Tokens)
- **Async Processing**: Python Background Tasks for risk index calculations.

---

## 2. Database Schema (SQLAlchemy Models)

### User Model (`app.db.models.user`)
Handles authentication and RBAC.
- `id`: Primary Key.
- `full_name`: User's display name.
- `email`: Unique login identifier.
- `hashed_password`: Securely stored password.
- `role`: Role of the user (`researcher` or `citizen`).

### Dataset Model (`app.db.models.dataset`)
Represents a CSV file uploaded by a researcher.
- `uploader_id`: Link to the User.
- `filename`: Name of the source file.
- `upload_status`: `processing` or `completed`.
- `samples`: Relationship to all samples imported from this file (with `delete-orphan` cascade).

### Sample Model (`app.db.models.sample`)
Geospatial sampling point.
- `lat`, `lng`: Coordinates.
- `location_name`, `state`, `district`: Regional metadata.
- `timestamp`: Date of sampling.
- `measurements`: Relationship to chemical data.
- `assessment`: Relationship to calculated risk scores.

### Measurement Model (`app.db.models.sample`)
Chemical concentration for a specific sample.
- `metal`: Element name (e.g., As, Fe).
- `concentration`: Numeric value in **mg/L**.

### RiskAssessment Model (`app.db.models.risk`)
Calculated safety metrics.
- `hpi`: Heavy Metal Pollution Index.
- `mi`: Metal Index.
- `risk_category`: `Safe`, `Moderately Polluted`, or `Hazardous`.

---

## 3. Core API Routes

### Authentication (`/api/v1/auth`)
- `POST /login`: Accepts email/password, returns JWT.

### Researcher Operations (`/api/v1/researcher`)
- `POST /upload-csv`: Ingests CSV files, handles unit conversions (ppb/ppm to mg/L), and triggers background risk calculations.
- `GET /samples`: Fetches all samples with their risk scores. Supports query-based uploader filtering.
- `GET /dashboard-stats`: Returns aggregated data for the logged-in researcher (average HPI, risk distribution, metal averages).
- `GET /uploads`: Lists datasets owned by the researcher.
- `DELETE /uploads/{id}`: Purges a dataset and all associated spatial points.

### Education & Public Data (`/api/v1/education`)
- `GET /metals`: Returns WHO/BIS standard limits for various heavy metals.
- `GET /materials`: Returns educational articles on water safety.

---

## 4. Business Logic: Risk Indices

### Heavy Metal Pollution Index (HPI)
HPI is calculated as the ratio of measured concentration to standard limits, weighted by the relative importance of the metal (inverse of the standard limit).
- **Hazardous**: HPI > 100
- **Polluted**: HPI > 50
- **Safe**: HPI <= 50

### Metadata Parsing
The CSV ingestion engine is flexible and identifies columns using regex for:
- Coordinates (`lat`, `lng`)
- Region (`state`, `district`)
- Units: Automatically converts `(ppb)` to `mg/L` (division by 1000).

---

## 5. Security & RBAC
The system implements strict **Role-Based Access Control**:
- **Citizen**: Can view maps, logs, and education. Cannot upload data.
- **Researcher**: Full data management capabilities (Upload, Delete, Private Dashboard).

Authentication is handled via the `Authorization: Bearer <token>` header on protected routes.
