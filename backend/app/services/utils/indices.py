from typing import Dict, List
from app.core.constants import METAL_STANDARDS, METAL_WEIGHTS

def calculate_hpi(concentrations: Dict[str, float]) -> float:
    """
    Calculate Heavy Metal Pollution Index (HPI).
    Formula: HPI = Σ(Qi * Wi) / ΣWi
    Where:
        Qi = Sub-index = ((Mi - Ii) / (Si - Ii)) * 100
        Wi = Unit Weight = 1 / Si
    """
    numerator = 0.0
    denominator = 0.0
    
    for metal, mi in concentrations.items():
        if metal not in METAL_STANDARDS:
            continue
            
        std = METAL_STANDARDS[metal]
        si = std["Si"]
        ii = std["Ii"]
        wi = METAL_WEIGHTS[metal]
        
        # Calculate Sub-index (Qi)
        # Avoid division by zero if Si == Ii (should typically not happen with Ii=0)
        if si - ii == 0:
            qi = 0
        else:
            qi = ((mi - ii) / (si - ii)) * 100
            
        numerator += (qi * wi)
        denominator += wi
        
    if denominator == 0:
        return 0.0
        
    return numerator / denominator

def calculate_hei(concentrations: Dict[str, float]) -> float:
    """
    Calculate Heavy Metal Evaluation Index (HEI).
    Formula: HEI = Σ (Mi / MACi)
    """
    hei = 0.0
    for metal, mi in concentrations.items():
        if metal in METAL_STANDARDS:
            mac = METAL_STANDARDS[metal]["MAC"]
            if mac > 0:
                hei += (mi / mac)
    return hei

def calculate_mi(concentrations: Dict[str, float]) -> float:
    """
    Calculate Metal Index (MI).
    Formula: MI = Σ (Ci / MACi)  (Ci is same as Mi here)
    """
    # MI (Tamasi & Cini, 2004) often uses specific MAC,
    # but generic definition is essentially same summation logic as HEI base steps
    # or sometimes includes weights.
    # Using basic MI = Σ (C / MAC) logic as requested.
    mi_score = 0.0
    for metal, ci in concentrations.items():
        if metal in METAL_STANDARDS:
            mac = METAL_STANDARDS[metal]["MAC"]
            if mac > 0:
                mi_score += (ci / mac)
                
    return mi_score
