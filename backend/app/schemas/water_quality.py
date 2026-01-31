from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Optional
from datetime import datetime
from enum import Enum
from typing import Literal, List


class MetalConcentration(BaseModel):
    metal: Literal["As", "Pb", "Cd", "Hg", "Cr", "Fe", "Mn", "Ni", "Zn", "Cu"] 
    concentration: float = Field(..., ge=0.0)
    unit: Literal["mg/L", "µg/L"] = "mg/L"


    @model_validator(mode='after')
    def validate_and_normalize(self) -> 'MetalConcentration':
        if self.unit == "µg/L":
            # Direct adjustment of the attribute
            self.concentration = self.concentration / 1000
        return self

class CreateSample(BaseModel):
    latitude: float = Field(..., ge=-90.0, le=90.0)
    longitude: float = Field(..., ge=-180.0, le=180.0)
    timestamp: datetime = Field(default_factory=datetime.now)
    source_type: Literal["Groundwater", "Industrial Effluent", "Surface Water"]
    measurements: List[MetalConcentration] = Field(..., min_length=1)
    standard_preference: Literal["BIS", "WHO"] = "BIS"
    
    
    @model_validator(mode='after')
    def check_at_least_one_metal(self) -> 'CreateSample':
        if not self.measurements:
            raise ValueError("At least one metal measurement is required.")
        return self