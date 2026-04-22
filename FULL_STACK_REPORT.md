# Full Stack Development Report: MetalSense
**Spatial Data Analytics Platform for Environmental Safety**

---

## 1. Project Overview & Motivation

### The Problem
Environmental pollution, specifically heavy metal contamination in water bodies, is a critical public health issue. However, the data collected by researchers is often stored in complex spreadsheets (CSVs) that are inaccessible to the general public. There is a "data gap" between scientific findings and public awareness.

### The Solution: MetalSense
MetalSense is a professional full-stack application designed to:
1.  **Ingest** complex scientific datasets via a researcher-friendly pipeline.
2.  **Calculate** mathematically validated risk indices (HPI, HEI, etc.) in real-time.
3.  **Visualize** these risks through interactive maps and analytical dashboards for both citizens and researchers.

---

## 2. Technical Architecture: The "Full Stack" Strategy

The project employs a **Decoupled Architecture**, following modern industry standards for high scalability and separation of concerns.

### Frontend Layer (The Presentation)
- **Framework**: React 19 (TypeScript).
- **Core Libraries**: `Vite` for development, `React-Leaflet` for GIS mapping, and `Recharts` for analytical visualization.
- **State Management**: Built with native React Hooks and LocalStorage for session persistence.
- **Design Philosophy**: A clinical, high-density "Steel & Glass" aesthetic, ensuring data legibility without visual clutter.

### Backend Layer (The Engine)
- **Framework**: FastAPI (Python). Chosen for its asynchronous execution capabilities and automatic schema validation.
- **Database Logic**: SQLAlchemy ORM for object-relational mapping, ensuring that Python objects and Database records stay in sync.
- **Asynchronous Workflow**: Heavy mathematical computations are handled by **Background Tasks**, ensuring the user never experiences "UI Freezing" during large file processing.

### Database Layer (The Memory)
- **Engine**: PostgreSQL. A robust, ACID-compliant relational database.
- **Schema Design**: Normalized into 8 related tables, allowing for "one-to-many" relationships between sampling points and their individual chemical measurements.

---

## 3. Scientific Engine: Theoretical Framework

One of the "Hard" concepts in this project is the translation of raw chemical readings into safety indices.

### Heavy Metal Pollution Index (HPI)
HPI is a weighted arithmetic index that provides a single value representing overall water quality.
- **Formula**: `HPI = Σ(Wi * Qi) / ΣWi`
- **Calculation**: We first calculate sub-indices (`Qi`) for each metal based on its concentration vs. WHO standards and then apply weight factors (`Wi`) based on the metal's relative toxicity.

### Health Risk Assessment (HQ & HI)
We implement USEPA-standard risk models:
- **Hazard Quotient (HQ)**: Calculated as `Daily Intake / Reference Dose`.
- **Hazard Index (HI)**: The sum of all HQs. If **HI > 1**, it indicates potential non-carcinogenic health effects.

---

## 4. Engineering Case Studies: Overcoming Challenges

### Challenge 1: Heterogeneous CSV Data
In the real world, researchers use different naming conventions for CSV columns (e.g., "Latitude" vs. "Lat").
- **Solution**: We implemented a **Regex-based column detection engine** in the backend that intelligently identifies coordinate, regional, and metal columns regardless of the filename.

### Challenge 2: Local Database Migration
Initially started on SQLite, the project required a more robust solution for concurrent uploads.
- **Solution**: Migrated to a **PostgreSQL** instance. This required re-architecting the `DATABASE_URL` construction (to handle special characters in passwords) and creating a schema-sync utility (`reset_db.py`) to ensure the local tables perfectly match the Python models.

---

## 5. Security & RBAC (Role-Based Access Control)

To protect data integrity, we implemented **JWT (JSON Web Token) Authentication**:
- **Stateless Auth**: The server doesn't store sessions; the client provides a signed token with every request.
- **RBAC**: FastAPI "Dependencies" act as middle-wares to check user roles:
  - **Citizen Role**: Restricted to GET requests (MapView/Logs).
  - **Researcher Role**: Authorized for POST/DELETE operations (CSV Upload/Delete).

---

## 6. Presentation Talking Points & Demo Script

Use these points during your showcase to impress your evaluators:

### Intro (Dashboard)
*"Notice the 'Stat Cards' at the top—these provide an immediate summary of the active researcher's dataset, including their average HPI score and risk distribution. This is calculated dynamically from the PostgreSQL database."*

### The Map (GIS Integration)
*"On the MapView, we use Leaflet to render sample points. The markers are color-coded based on the calculated risk category (Green for Safe, Red for Hazardous). I integrated custom popups that display high-density metal concentrations using a Slate-Glass design."*

### The Data Pipeline (The "Wow" Factor)
*"The most complex part of the system is the Ingestion Pipeline. If I upload a CSV, notice that the system remains responsive. This is because the CSV parsing and HPI calculations are happening in a separate background thread. Once processed, the UI fetches the updated results."*

---

## 7. Potential QA / Viva Trainer

**Q: Why did you use JWT instead of traditional Cookies/Sessions?**
**A**: JWT is stateless, making the application more scalable. It allows the frontend (Vite) and backend (FastAPI) to reside on different servers without complex session synchronization.

**Q: How do you handle non-standard units (e.g., ppb vs ppm) in uploads?**
**A**: Our backend includes a normalization logic that detects unit suffixes in CSV headers. If it sees `(ppb)`, it automatically divides the concentration by 1000 to normalize it to `mg/L` before storage.

**Q: Why PostgreSQL over a NoSQL database like MongoDB?**
**A**: Water quality data is highly relational (Samples have many Measurements). SQL's ACID compliance and relational mappings (One-to-Many) ensure that chemical data never loses its reference to the physical sampling site.
