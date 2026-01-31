from typing import Dict, TypedDict

# ==========================================
# 1. WATER QUALITY STANDARDS (BIS/WHO)
# ==========================================
# Si: Standard Permissible Limit (mg/L)
# Ii: Ideal Value (mg/L) - Usually 0 for toxics
# MAC: Maximum Allowable Concentration (mg/L)
# Bn: Geochemical Background Value (mg/L proxy or mg/kg)
# ==========================================

class MetalStandard(TypedDict):
    Si: float
    Ii: float
    MAC: float
    Bn: float

METAL_STANDARDS: Dict[str, MetalStandard] = {
    "arsenic":   {"Si": 0.01,  "Ii": 0.0, "MAC": 0.01,  "Bn": 12.70},
    "cadmium":   {"Si": 0.003, "Ii": 0.0, "MAC": 0.003, "Bn": 0.10},
    "chromium":  {"Si": 0.05,  "Ii": 0.0, "MAC": 0.05,  "Bn": 67.30},
    "copper":    {"Si": 0.05,  "Ii": 0.0, "MAC": 1.5,   "Bn": 22.50},
    "iron":      {"Si": 0.3,   "Ii": 0.0, "MAC": 0.3,   "Bn": 15000.0},
    "lead":      {"Si": 0.01,  "Ii": 0.0, "MAC": 0.01,  "Bn": 21.00},
    "manganese": {"Si": 0.1,   "Ii": 0.0, "MAC": 0.3,   "Bn": 500.0},
    "mercury":   {"Si": 0.001, "Ii": 0.0, "MAC": 0.001, "Bn": 0.02},
    "nickel":    {"Si": 0.02,  "Ii": 0.0, "MAC": 0.02,  "Bn": 31.00},
    "zinc":      {"Si": 5.0,   "Ii": 0.0, "MAC": 15.0,  "Bn": 65.40},
}

# Pre-calculate Weights (Wi = 1 / Si)
METAL_WEIGHTS = {metal: 1.0 / std["Si"] for metal, std in METAL_STANDARDS.items()}


# ==========================================
# 2. HEALTH RISK PARAMETERS (USEPA/IRIS)
# ==========================================
# RfD: Oral Reference Dose (mg/kg/day)
# CSF: Cancer Slope Factor (mg/kg/day)^-1
# ==========================================

class RiskParams(TypedDict):
    RfD: float
    CSF: float | None

RISK_PARAMS: Dict[str, RiskParams] = {
    "arsenic":   {"RfD": 0.0003, "CSF": 1.5},
    "cadmium":   {"RfD": 0.0005, "CSF": 6.3},
    "chromium":  {"RfD": 0.003,  "CSF": 0.5},
    "copper":    {"RfD": 0.04,   "CSF": None},
    "iron":      {"RfD": 0.7,    "CSF": None},
    "lead":      {"RfD": 0.0014, "CSF": 0.0085},
    "manganese": {"RfD": 0.024,  "CSF": None},
    "mercury":   {"RfD": 0.0003, "CSF": None},
    "nickel":    {"RfD": 0.02,   "CSF": None},
    "zinc":      {"RfD": 0.3,    "CSF": None},
}


# ==========================================
# 3. EXPOSURE SCENARIOS (Adult vs Child)
# ==========================================
# BW: Body Weight (kg)
# IR: Ingestion Rate (L/day)
# EF: Exposure Frequency (days/year)
# ED: Exposure Duration (years)
# AT: Averaging Time (days)
# ==========================================

class ExposureDefaults(TypedDict):
    BW: float
    IR: float
    EF: int
    ED: int
    AT: int

EXPOSURE_DEFAULTS: Dict[str, ExposureDefaults] = {
    "adult": {
        "BW": 70.0,
        "IR": 2.2,
        "EF": 350,
        "ED": 70,
        "AT": 25550, # 70 years * 365
    },
    "child": {
        "BW": 15.0,
        "IR": 1.8,
        "EF": 350,
        "ED": 6,
        "AT": 2190,  # 6 years * 365
    }
}
