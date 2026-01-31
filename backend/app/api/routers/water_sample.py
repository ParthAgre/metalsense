from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.database import SessionLocal
from app.db.models.water_sample import WaterSample
from app.schemas.water_sample import WaterSampleCreate, WaterSampleResponse, IndicesResponse, RiskAssessmentResponse
from app.services.utils.indices import calculate_hpi, calculate_hei, calculate_mi
from app.services.utils.risk import get_comprehensive_risk_assessment

router = APIRouter(
    prefix="/samples",
    tags=["Water Samples"]
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=WaterSampleResponse)
def create_sample(sample: WaterSampleCreate, db: Session = Depends(get_db)):
    """
    Create a new water sample entry.
    Automatically calculates HPI, HEI, and MI indices.
    """
    data = sample.model_dump()
    
    # Extract metal concentrations for calculation
    # Only fields starting with conc_ are metals
    concentrations = {
        key.replace("conc_", ""): value 
        for key, value in data.items() 
        if key.startswith("conc_")
    }
    
    # Calculate Indices
    hpi = calculate_hpi(concentrations)
    hei = calculate_hei(concentrations)
    mi = calculate_mi(concentrations)
    
    # Determine basic risk level based on HPI (Example logic)
    risk_level = "Safe"
    if hpi > 100: # Common threshold
        risk_level = "Unsafe"
    elif hpi > 15: # Critical Pollution Index threshold
        risk_level = "High Pollution"
        
    db_sample = WaterSample(
        **data,
        hpi_score=hpi,
        hei_score=hei,
        mi_score=mi,
        risk_level=risk_level
    )
    
    db.add(db_sample)
    db.commit()
    db.refresh(db_sample)
    
    # Attach dynamic fields for response model
    # (Pydantic 'from_attributes' handles DB mapping, but we construct nested explicitly if needed 
    # OR rely on Pydantic to map via properties if we added them to model. 
    # Simpler: just construct the response dict/object)
    
    response_obj = db_sample
    
    # Inject indices object for response
    response_obj.indices = IndicesResponse(
        hpi=hpi,
        hei=hei,
        mi=mi,
        interpretation=risk_level
    )
    
    # Calculate Risk Assessment on the fly
    risk_data = get_comprehensive_risk_assessment(concentrations)
    response_obj.risk_assessment = RiskAssessmentResponse(**risk_data)
    
    return response_obj

@router.get("/", response_model=List[WaterSampleResponse])
def read_samples(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    samples = db.query(WaterSample).offset(skip).limit(limit).all()
    
    # Enrich samples with calculated data if it wasn't stored/needs re-calc
    # Since we store scores, we just need to structure them.
    # Risk assessment is heavy, maybe omit for list view? 
    # For now, let's include it but optimize if needed.
    
    results = []
    for s in samples:
        # Re-construct concentrations map
        concentrations = {
            "arsenic": s.conc_arsenic,
            "cadmium": s.conc_cadmium,
            "chromium": s.conc_chromium,
            "copper": s.conc_copper,
            "iron": s.conc_iron,
            "lead": s.conc_lead,
            "manganese": s.conc_manganese,
            "mercury": s.conc_mercury,
            "nickel": s.conc_nickel,
            "zinc": s.conc_zinc
        }
        
        s.indices = IndicesResponse(
            hpi=s.hpi_score if s.hpi_score is not None else 0.0,
            hei=s.hei_score if s.hei_score is not None else 0.0,
            mi=s.mi_score if s.mi_score is not None else 0.0,
            interpretation=s.risk_level or "Unknown"
        )
        
        risk_data = get_comprehensive_risk_assessment(concentrations)
        s.risk_assessment = RiskAssessmentResponse(**risk_data)
        results.append(s)
        
    return results

@router.get("/{sample_id}", response_model=WaterSampleResponse)
def read_sample(sample_id: int, db: Session = Depends(get_db)):
    s = db.query(WaterSample).filter(WaterSample.id == sample_id).first()
    if s is None:
        raise HTTPException(status_code=404, detail="Sample not found")
        
    concentrations = {
        "arsenic": s.conc_arsenic,
        "cadmium": s.conc_cadmium,
        "chromium": s.conc_chromium,
        "copper": s.conc_copper,
        "iron": s.conc_iron,
        "lead": s.conc_lead,
        "manganese": s.conc_manganese,
        "mercury": s.conc_mercury,
        "nickel": s.conc_nickel,
        "zinc": s.conc_zinc
    }
    
    s.indices = IndicesResponse(
        hpi=s.hpi_score if s.hpi_score is not None else 0.0,
        hei=s.hei_score if s.hei_score is not None else 0.0,
        mi=s.mi_score if s.mi_score is not None else 0.0,
        interpretation=s.risk_level or "Unknown"
    )
    
    risk_data = get_comprehensive_risk_assessment(concentrations)
    s.risk_assessment = RiskAssessmentResponse(**risk_data)
    
    return s
