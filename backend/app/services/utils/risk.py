from typing import Dict, Any, Literal
from app.core.constants import RISK_PARAMS, EXPOSURE_DEFAULTS

def calculate_cdi(c: float, ir: float, ef: int, ed: int, bw: float, at: int) -> float:
    """
    Calculate Chronic Daily Intake (CDI).
    Formula: CDI = (C * IR * EF * ED) / (BW * AT)
    
    Params:
        c: Concentration (mg/L)
        ir: Ingestion Rate (L/day)
        ef: Exposure Frequency (days/year)
        ed: Exposure Duration (years)
        bw: Body Weight (kg)
        at: Averaging Time (days)
    """
    numerator = c * ir * ef * ed
    denominator = bw * at
    
    if denominator == 0:
        return 0.0
        
    return numerator / denominator

def calculate_hq(cdi: float, rfd: float) -> float:
    """
    Calculate Hazard Quotient (HQ).
    Formula: HQ = CDI / RfD
    """
    if rfd == 0:
        return 0.0
    return cdi / rfd

def calculate_cancer_risk(cdi: float, csf: float) -> float:
    """
    Calculate Lifetime Cancer Risk (LCR).
    Formula: Risk = CDI * CSF
    """
    return cdi * csf

def get_comprehensive_risk_assessment(concentrations: Dict[str, float]) -> Dict[str, Any]:
    """
    Generate full risk assessment for both Adult and Child scenarios.
    Returns:
        {
            "adult": { ...risk data... },
            "child": { ...risk data... }
        }
    """
    results = {}
    
    for demographic in ["adult", "child"]:
        params = EXPOSURE_DEFAULTS[demographic]
        geo_results = {
            "metals": {},
            "total_hq": 0.0, # Hazard Index (HI)
            "total_cancer_risk": 0.0
        }
        
        for metal, conc in concentrations.items():
            if metal not in RISK_PARAMS:
                continue
            
            risk_consts = RISK_PARAMS[metal]
            
            # 1. Provide CDI (Non-Carcinogenic Assumption usually uses AT = ED * 365)
            # 2. Provide CDI_Carcinogenic (Uses AT = 70 * 365)
            
            # --- Non-Carcinogenic Risks (HQ) ---
            cdi_nc = calculate_cdi(
                c=conc,
                ir=params["IR"],
                ef=params["EF"],
                ed=params["ED"],
                bw=params["BW"],
                at=params["AT"] 
            )
            
            hq = calculate_hq(cdi_nc, risk_consts["RfD"])
            geo_results["total_hq"] += hq
            
            # --- Carcinogenic Risks (LCR) ---
            lcr = 0.0
            if risk_consts["CSF"] is not None:
                cdi_c = calculate_cdi(
                    c=conc,
                    ir=params["IR"],
                    ef=params["EF"],
                    ed=params["ED"],
                    bw=params["BW"],
                    at=params["AT_C"] # Lifetime averaging
                )
                lcr = calculate_cancer_risk(cdi_c, risk_consts["CSF"])
                geo_results["total_cancer_risk"] += lcr
                
            geo_results["metals"][metal] = {
                "CDI": cdi_nc,
                "HQ": hq,
                "CancerRisk": lcr if risk_consts["CSF"] else "Non-Carcinogenic"
            }
            
        results[demographic] = geo_results
        
    return results
