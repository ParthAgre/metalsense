from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime

# --- Base Schema (Common Fields) ---
class WaterSampleBase(BaseModel):
    location_name: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    
    # Heavy Metal Concentrations (mg/L)
    # Defaulting to 0.0 facilitates easier testing and creation
    conc_arsenic: float = Field(0.0, ge=0.0)
    conc_cadmium: float = Field(0.0, ge=0.0)
    conc_chromium: float = Field(0.0, ge=0.0)
    conc_copper: float = Field(0.0, ge=0.0)
    conc_iron: float = Field(0.0, ge=0.0)
    conc_lead: float = Field(0.0, ge=0.0)
    conc_manganese: float = Field(0.0, ge=0.0)
    conc_mercury: float = Field(0.0, ge=0.0)
    conc_nickel: float = Field(0.0, ge=0.0)
    conc_zinc: float = Field(0.0, ge=0.0)

# --- Create Schema (Input) ---
class WaterSampleCreate(WaterSampleBase):
    pass

# --- Nested Response Sub-Models ---
class IndicesResponse(BaseModel):
    hpi: float
    hei: float
    mi: float
    interpretation: str

# Risk Models
class RiskValue(BaseModel):
    CDI: float
    HQ: float
    CancerRisk: float | str # str for "Non-Carcinogenic"

class DemographicRisk(BaseModel):
    metals: Dict[str, RiskValue]
    total_hq: float
    total_cancer_risk: float

class RiskAssessmentResponse(BaseModel):
    adult: DemographicRisk
    child: DemographicRisk

# --- Response Schema (Output) ---
class WaterSampleResponse(WaterSampleBase):
    id: int
    sampling_date: datetime
    
    # Calculated Fields
    indices: Optional[IndicesResponse] = None
    risk_assessment: Optional[RiskAssessmentResponse] = None

    class Config:
        from_attributes = True
