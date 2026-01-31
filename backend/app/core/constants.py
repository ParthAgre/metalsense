from typing import Dict, TypedDict

# Heavy Metal Standards (mg/L) & Weights
# Si: Standard Permissible Limit (BIS/WHO)
# Ii: Ideal Value (Usually 0 for heavy metals)
# Wi: Unit Weight (1/Si, normalized later if needed, but HPI formula uses strict 1/Si usually)
# MAC: Maximum Allowable Concentration (used for HEI/MI, often same as Si or slightly higher)

class MetalStandard(TypedDict):
    Si: float  # Permissible Limit
    Ii: float  # Ideal Value
    # Wi will be calculated as 1/Si
    MAC: float # Max Allowable (often same as Si for some indices)

# Based on user inputs and common standards (BIS 10500 / WHO)
METAL_STANDARDS: Dict[str, MetalStandard] = {
    "arsenic":   {"Si": 0.01,  "Ii": 0.0, "MAC": 0.01},  # As
    "cadmium":   {"Si": 0.003, "Ii": 0.0, "MAC": 0.003}, # Cd
    "chromium":  {"Si": 0.05,  "Ii": 0.0, "MAC": 0.05},  # Cr
    "copper":    {"Si": 0.05,  "Ii": 0.0, "MAC": 1.5},   # Cu (BIS: 0.05, WHO: 2.0 - user img says 0.05 BIS)
    "iron":      {"Si": 0.3,   "Ii": 0.0, "MAC": 0.3},   # Fe
    "lead":      {"Si": 0.01,  "Ii": 0.0, "MAC": 0.01},  # Pb
    "manganese": {"Si": 0.1,   "Ii": 0.0, "MAC": 0.3},   # Mn (BIS acceptable 0.3)
    "mercury":   {"Si": 0.001, "Ii": 0.0, "MAC": 0.001}, # Hg
    "nickel":    {"Si": 0.02,  "Ii": 0.0, "MAC": 0.02},  # Ni (User img says 0.02)
    "zinc":      {"Si": 5.0,   "Ii": 0.0, "MAC": 15.0},  # Zn
}

# Pre-calculate Weights (Wi = 1 / Si)
METAL_WEIGHTS = {metal: 1.0 / std["Si"] for metal, std in METAL_STANDARDS.items()}


# Health Risk Assessment Constants
# RfD: Oral Reference Dose (mg/kg/day)
# CSF: Cancer Slope Factor (mg/kg/day)^-1
# Source: USEPA Integrated Risk Information System (IRIS)

class RiskParams(TypedDict):
    RfD: float
    CSF: float | None # None if not carcinogenic

RISK_PARAMS: Dict[str, RiskParams] = {
    "arsenic":   {"RfD": 3.0E-4, "CSF": 1.5},
    "cadmium":   {"RfD": 5.0E-4, "CSF": 6.3}, # Inhalation CSF is different, oral often lower/debated, using common proxy
    "chromium":  {"RfD": 3.0E-3, "CSF": 0.5}, # Cr(VI) is higher risk
    "copper":    {"RfD": 4.0E-2, "CSF": None},
    "iron":      {"RfD": 7.0E-1, "CSF": None},
    "lead":      {"RfD": 3.5E-3, "CSF": 0.0085}, # RfD for Pb is complex, using provisional
    "manganese": {"RfD": 1.4E-1, "CSF": None},
    "mercury":   {"RfD": 3.0E-4, "CSF": None},
    "nickel":    {"RfD": 2.0E-2, "CSF": None}, # heavily dependent on soluble salts
    "zinc":      {"RfD": 3.0E-1, "CSF": None},
}

# Exposure Parameters (Defaults)
class ExposureDefaults(TypedDict):
    BW: float # Body Weight (kg)
    IR: float # Ingestion Rate (L/day)
    EF: int   # Exposure Frequency (days/year)
    ED: int   # Exposure Duration (years)
    AT: int   # Averaging Time (days) - Non-Carcinogenic
    AT_C: int # Averaging Time (days) - Carcinogenic (Lifetime)

EXPOSURE_DEFAULTS = {
    "adult": {
        "BW": 70.0,
        "IR": 2.2, # Avg water consumption
        "EF": 365,
        "ED": 30,  # 30 years residence
        "AT": 30 * 365,
        "AT_C": 70 * 365 # 70 years lifetime expectancy
    },
    "child": {
        "BW": 15.0, # Approx 3-5 year old
        "IR": 1.0,
        "EF": 365,
        "ED": 6,
        "AT": 6 * 365,
        "AT_C": 70 * 365 # Lifetime risk still averaged over 70 years
    }
}
