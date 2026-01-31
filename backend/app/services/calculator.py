import math
from typing import List, Dict
from app.services.constants import METAL_STANDARDS, METAL_WEIGHTS, RISK_PARAMS, EXPOSURE_DEFAULTS

class EnvironmentalCalculator:
    
    @staticmethod
    def calculate_hpi(measurements: Dict[str, float]) -> float:
        """
        Computes Heavy Metal Pollution Index (HPI).
        HPI = Σ(Qi * Wi) / ΣWi where Qi = (Mi/Si) * 100
        """
        total_weighted_qi = 0.0
        sum_weights = 0.0
        
        for metal, concentration in measurements.items():
            if metal in METAL_STANDARDS:
                si = METAL_STANDARDS[metal]["Si"]
                wi = METAL_WEIGHTS[metal]
                
                # Sub-index calculation (Qi) [cite: 232, 250]
                qi = (concentration / si) * 100
                
                total_weighted_qi += (qi * wi)
                sum_weights += wi
        
        return total_weighted_qi / sum_weights if sum_weights > 0 else 0.0

    @staticmethod
    def calculate_hei(measurements: Dict[str, float]) -> float:
        """
        Computes Heavy Metal Evaluation Index (HEI).
        HEI = Σ(Mi / MACi) [cite: 238]
        """
        return sum(
            concentration / METAL_STANDARDS[metal]["MAC"]
            for metal, concentration in measurements.items()
            if metal in METAL_STANDARDS
        )

    @staticmethod
    def calculate_i_geo(metal: str, concentration: float) -> float:
        """
        Computes Geo-accumulation Index (I-geo) for a single metal.
        I-geo = log2(Cn / (1.5 * Bn)) [cite: 89]
        """
        if metal not in METAL_STANDARDS:
            return 0.0
        
        bn = METAL_STANDARDS[metal]["Bn"]
        # Convert concentration to mg/kg if necessary, 
        # but here we assume normalized units as per research 
        return math.log2(concentration / (1.5 * bn)) if concentration > 0 else 0.0

    @staticmethod
    def calculate_health_risk(measurements: Dict[str, float], group: str = "child") -> Dict[str, float]:
        """
        Computes Hazard Index (HI) and Carcinogenic Risk (CR).
        HI = Σ(CDI / RfD) [cite: 303, 304]
        """
        params = EXPOSURE_DEFAULTS[group]
        total_hq = 0.0
        total_cr = 0.0
        
        for metal, conc in measurements.items():
            if metal in RISK_PARAMS:
                # Chronic Daily Intake (CDI) [cite: 292]
                cdi = (conc * params["IR"] * params["EF"] * params["ED"]) / (params["BW"] * params["AT"])
                
                # Non-carcinogenic HQ [cite: 303]
                rfd = RISK_PARAMS[metal]["RfD"]
                total_hq += (cdi / rfd)
                
                # Carcinogenic Risk (CR) [cite: 308]
                csf = RISK_PARAMS[metal]["CSF"]
                if csf:
                    total_cr += (cdi * csf)
                    
        return {"hazard_index": total_hq, "cancer_risk": total_cr}