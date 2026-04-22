# MetalSense: Professional Data Analytics Platform for Environmental Safety

## 1. Executive Summary
MetalSense is a full-stack spatial water quality analytics platform designed to bridge the gap between complex environmental data and public health awareness. It provides specialized interfaces for **Researchers** to manage large environmental datasets and **Citizens** to visualize safety risks in their local regions. The platform specializes in detecting heavy metal patterns and calculating scientifically validated risk indices.

---

## 2. Technology Stack

### Backend: High-Performance Engine
- **Framework**: [FastAPI](https://fastapi.tiangolo.com/) (Python 3.13) - Selected for its high performance, asynchronous support, and automatic OpenAPI (Swagger) documentation.
- **Database ORM**: [SQLAlchemy 2.0](https://www.sqlalchemy.org/) - Provides a powerful abstraction layer for SQL databases.
- **Database**: [PostgreSQL](https://www.postgresql.org/) - Chosen for its robustness, ACID compliance, and suitability for production-grade spatial data.
- **Data Processing**: [Pandas](https://pandas.pydata.org/) - Used for high-speed CSV parsing, unit normalization, and data cleaning.
- **Security**: JWT (JSON Web Tokens) with Python-Jose for stateless, secure authentication.

### Frontend: Modern Analytical Dashboard
- **Framework**: [React 19](https://react.dev/) with [TypeScript](https://www.typescriptlang.org/) - Ensures type safety and highly interactive UI components.
- **Build Tool**: [Vite](https://vitejs.dev/) - Provides extremely fast development starts and optimized production builds.
- **GIS Mapping**: [Leaflet](https://leafletjs.com/) & [React-Leaflet](https://react-leaflet.js.org/) - For high-performance spatial rendering of sample points.
- **Data Visualization**: [Recharts](https://recharts.org/) - For high-density SVG charts and trend analysis.
- **State Management**: React Hooks (State/Effect/Memo) with local persistence for session tokens.
- **Styling**: Vanilla CSS (Modular) with a Slate/Glassmorphism design system.

---

## 3. System Architecture
The application follows a **Decoupled Architecture**, where the Frontend and Backend communicate over an authenticated REST API.

1.  **Client Layer**: React-based dashboard requesting data via Axios.
2.  **API Layer**: FastAPI endpoints handling routing, validation (Pydantic), and Authentication (OAuth2/JWT).
3.  **Service Layer**: Business logic for scientific calculations (HPI, HEI) and background task orchestration.
4.  **Database Layer**: PostgreSQL storing normalized spatial and chemical data.

### Asynchronous Processing Workflow
To ensure the UI remains responsive, heavy calculations are offloaded to **Background Tasks**:
- Researcher uploads 10,000+ data points via CSV.
- FastAPI accepts the file, returns "Accepted (202)", and launches a background thread.
- The background thread parses the CSV, saves raw entries, and triggers the `EnvironmentalCalculator`.
- Results are persisted to the `RiskAssessment` table once processing is complete.

---

## 4. Database Schema & Data Modeling
The database is structured into 8 critical tables ensuring data integrity and scalability:

- **`users`**: Stores credentials, hashed passwords (Bcrypt), and Role-Based attributes (`citizen` vs `researcher`).
- **`datasets`**: Tracks metadata for bulk uploads (filename, upload status, uploader link).
- **`samples`**: The central geospatial entity (lat/lng, regional metadata, source type).
- **`measurements`**: A one-to-many relationship linking a sample to various chemical concentrations (As, Pb, Fe, etc.).
- **`risk_assessments`**: Stores the final computed scientific scores and the "Safe/Hazardous" classification.
- **`heavy_metals`**: Core dictionary of metals, their WHO/BIS standard limits, and health descriptions.
- **`education_materials`**: Educational content parsed for the Citizen Dashboard.
- **`user_logs`**: Audit trail tracking data modifications.

---

## 5. Scientific Calculation Engine
MetalSense implements a multi-tiered risk assessment model, ranging from simple threshold checks to complex carcinogenic risk formulas.

### Level 1: Sub-Index Concentration (Qi)
Calculation of the percentage ratio of a measured metal vs. its international safety standard.
`Qi = (Mi / Si) * 100`  
*(Mi = Measured concentration, Si = Standard limit)*

### Level 2: Heavy Metal Pollution Index (HPI)
A weighted arithmetic index aggregating multiple metals into a single safety score.
- **Hazardous**: HPI > 100
- **Highly Polluted**: HPI > 50
- **Safe**: HPI ≤ 50

### Level 3: Health Risk Assessment (HQ & HI) - High Complexity
Based on the United States Environmental Protection Agency (USEPA) health risk models:
- **CDI (Chronic Daily Intake)**: Tracks how much metal enters the body daily based on weight, age, and exposure frequency.
- **Hazard Quotient (HQ)**: The ratio of CDI to the Reference Dose (RfD).
- **Hazard Index (HI)**: The sum of all individual metal HQs. An HI > 1 indicate potential non-carcinogenic health effects.
- **Carcinogenic Risk (CR)**: Calculated by multiplying CDI by the Cancer Slope Factor (CSF).

---

## 6. Security Model & RBAC
Security is enforced using **Role-Based Access Control (RBAC)** at the API level.

### Authentication Flow
1. User provides Email/Password.
2. Backend verifies using **Bcrypt** hashing.
3. Backend issues a **Stateless JWT** containing the user's ID and Role.
4. Frontend stores the token and includes it in the `Authorization: Bearer <token>` header.

### Access Levels
- **Citizen**: `READ-ONLY`. Access to MapView, DataLogs (viewing), and Education. Restricted from any path under `/api/v1/researcher`.
- **Researcher**: `FULL ACCESS`. Can upload CSVs, delete datasets they own, and access private analytics dashboards.

---

## 7. Data Pipeline (Ingestion & Cleaning)
The CSV ingestion engine is built for flexibility with non-standardized external datasets:
1.  **Column Detection**: Uses Regex to identify `lat`, `long`, `site`, and `concentration` columns even with inconsistent naming.
2.  **Unit Normalization**: Automatically detects units like `(ppb)` or `(ppm)` and converts them to the standardized `mg/L` using Pydantic validation.
3.  **Deduplication**: Checks coordinates and timestamps to prevent redundant database entries.

---

## 8. API Reference Summary

| Method | Endpoint | Description | Role Required |
| :--- | :--- | :--- | :--- |
| **POST** | `/api/v1/auth/login` | Returns JWT Access Token. | Public |
| **POST** | `/api/v1/researcher/upload-csv` | Asynchronously ingests water data. | Researcher |
| **GET** | `/api/v1/researcher/samples` | Fetches all spatial points with risk. | Public |
| **GET** | `/api/v1/researcher/dashboard-stats` | Aggregated analytics for researchers. | Researcher |
| **DELETE** | `/api/v1/researcher/uploads/{id}` | Purges a dataset and its map points. | Researcher |

---

## 9. Operation Guide: How to Run
Ensure you have **Python 3.13**, **PostgreSQL**, and **Node.js** installed.

### Backend Setup
1.  Navigate to `/backend`.
2.  Install requirements: `pip install -r requirements.txt`.
3.  Configure `.env` with your Postgres credentials.
4.  Initialize Database: `python -m app.db.database`.
5.  Seed Data: `python seed_metals.py` and `python seed_users.py`.
6.  Run Server: `uvicorn app.main:app --reload`.

### Frontend Setup
1.  Navigate to `/frontend`.
2.  Install dependencies: `npm install`.
3.  Run Server: `npm run dev`.
4.  Access via `http://localhost:5173`.
