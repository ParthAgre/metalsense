export interface WaterSample {
  id: number;
  location_name: string;
  latitude: number;
  longitude: number;
  sampling_date: string;
  conc_arsenic: number;
  conc_chromium: number;
  conc_copper: number;
  conc_iron: number;
  conc_manganese: number;
  conc_nickel: number;
  conc_lead: number;
  conc_zinc: number;
  conc_cadmium: number;
  conc_mercury: number;
  hpi_score: number;
  hei_score: number;
  mi_score: number;
  risk_level: 'Safe' | 'Low' | 'High';
}

export const mockSamples: WaterSample[] = [
  {
    id: 1,
    location_name: "Ganga River - Haridwar",
    latitude: 29.9457,
    longitude: 78.1642,
    sampling_date: "2024-01-28T10:00:00Z",
    conc_arsenic: 0.005,
    conc_chromium: 0.02,
    conc_copper: 0.05,
    conc_iron: 0.3,
    conc_manganese: 0.1,
    conc_nickel: 0.01,
    conc_lead: 0.001,
    conc_zinc: 1.2,
    conc_cadmium: 0.001,
    conc_mercury: 0.0001,
    hpi_score: 45.2,
    hei_score: 2.1,
    mi_score: 0.8,
    risk_level: 'Safe'
  },
  {
    id: 2,
    location_name: "Yamuna River - Delhi",
    latitude: 28.6139,
    longitude: 77.2090,
    sampling_date: "2024-01-29T14:30:00Z",
    conc_arsenic: 0.05,
    conc_chromium: 0.15,
    conc_copper: 0.45,
    conc_iron: 1.2,
    conc_manganese: 0.5,
    conc_nickel: 0.08,
    conc_lead: 0.02,
    conc_zinc: 5.5,
    conc_cadmium: 0.01,
    conc_mercury: 0.002,
    hpi_score: 110.5,
    hei_score: 15.4,
    mi_score: 4.2,
    risk_level: 'High'
  },
  {
    id: 3,
    location_name: "Mithi River - Mumbai",
    latitude: 19.0760,
    longitude: 72.8777,
    sampling_date: "2024-01-30T09:15:00Z",
    conc_arsenic: 0.02,
    conc_chromium: 0.08,
    conc_copper: 0.25,
    conc_iron: 0.8,
    conc_manganese: 0.3,
    conc_nickel: 0.05,
    conc_lead: 0.01,
    conc_zinc: 3.2,
    conc_cadmium: 0.005,
    conc_mercury: 0.001,
    hpi_score: 75.8,
    hei_score: 8.2,
    mi_score: 2.1,
    risk_level: 'Low'
  },
  {
    id: 4,
    location_name: "Hooghly River - Kolkata",
    latitude: 22.5726,
    longitude: 88.3639,
    sampling_date: "2024-01-31T11:45:00Z",
    conc_arsenic: 0.012,
    conc_chromium: 0.05,
    conc_copper: 0.15,
    conc_iron: 0.6,
    conc_manganese: 0.25,
    conc_nickel: 0.03,
    conc_lead: 0.005,
    conc_zinc: 2.5,
    conc_cadmium: 0.003,
    conc_mercury: 0.0005,
    hpi_score: 62.4,
    hei_score: 5.8,
    mi_score: 1.5,
    risk_level: 'Low'
  },
  {
    id: 5,
    location_name: "Sabarmati River - Ahmedabad",
    latitude: 23.0225,
    longitude: 72.5714,
    sampling_date: "2024-01-27T08:00:00Z",
    conc_arsenic: 0.035,
    conc_chromium: 0.12,
    conc_copper: 0.35,
    conc_iron: 1.0,
    conc_manganese: 0.4,
    conc_nickel: 0.06,
    conc_lead: 0.015,
    conc_zinc: 4.8,
    conc_cadmium: 0.008,
    conc_mercury: 0.0015,
    hpi_score: 95.2,
    hei_score: 12.1,
    mi_score: 3.5,
    risk_level: 'High'
  }
];
