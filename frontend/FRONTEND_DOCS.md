# MetalSense Frontend Documentation

## Overview
The MetalSense Frontend is a professional, high-performance data analytics dashboard built with **React** and **TypeScript**. It is designed for clear spatial visualization and scientific data management.

---

## 1. Technical Stack
- **Framework**: React 18 (Vite-based)
- **Language**: TypeScript
- **State Management**: React Hooks (useState, useEffect, useMemo) + LocalStorage (for JWT/Role).
- **Styling**: Vanilla CSS (Modular) with a "Professional Matte" Design System.
- **Charts**: Recharts (High-performance SVG charts).
- **Maps**: Leaflet (using React-Leaflet) with custom marker and popup logic.
- **Icons**: Lucide-React.
- **API Client**: Axios with interceptor patterns for Auth.

---

## 2. Design System: "Modern Corporate"
The interface follows a strict "Steel & Glass" matte aesthetic designed for data legibility.
- **Background**: Matte Slate (`#0f172a`).
- **Cards**: Surface Dark Slate (`#1e293b`) with 8-10px border radius.
- **Primary Color**: Action Blue (`#3b82f6`).
- **Typography**: Inter (Sans-serif) for clinical data presentation.

---

## 3. Component Architecture

### Core Layout (`/src/components/Layout.tsx`)
The master wrapper providing:
- **Sidebar**: Matteo navigation with role-based link rendering.
- **Header**: Displays page title and user initials circle.
- **Main Content**: Scrollable container for page components.

### Dashboard (`/src/pages/Dashboard.tsx`)
The high-level summary view:
- **Stat Cards**: Dynamic display of HPI, Sample count, and Safety status.
- **Pollutant Analytics**: Bar charts showing average metal concentrations.
- **Risk Distribution**: Visualization of the dataset safety classification.

### Map View (`/src/pages/MapView.tsx`)
Spatial visualization of water quality:
- **Interactive Layers**: Toggleable Leaflet markers.
- **Color Coding**: Red (Hazardous), Orange (Polluted), Green (Safe).
- **Popups**: High-density cards showing precise metal measurements (As, Fe, U, etc.).
- **Filtering**: Multi-layered dropdowns (State, District, Quality).

### Water Logs (`/src/pages/DataLogs.tsx`)
The "Scientific Ledger" of the project:
- **High-Density Table**: Tabular view of all sampled sites.
- **Secondary Filtering**: Real-time client-side filtering by Quality and Geography.
- **Data Ingestion**: Dedicated upload button for CSV import (Researcher only).

### Risk Alerts (`/src/pages/RiskAlerts.tsx`)
The safety advisory module:
- **Dynamic Calculation**: Real-time filtering of hazardous sites from active datasets.
- **External Guidelines**: Direct links to WHO and CGWB water safety standards.

---

## 4. Security & Routing
- **ProtectedRoute**: A custom wrapper that redirects unauthenticated users to `/auth`.
- **Role Control**: Components check `localStorage.getItem('role')` to hide/show sensitive features (like Upload/Delete).
- **JWT Handling**: Tokens are sent in the `Authorization: Bearer` header for all protected API calls.

---

## 5. Setup & Development
1. **Installation**: `npm install`
2. **Environment**: Ensure the Backend is running on `localhost:8000`.
3. **Run**: `npm run dev`
