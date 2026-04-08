from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models.metal import HeavyMetal
from app.db.models.education import EducationMaterial

router = APIRouter()

@router.get("/metals")
def get_heavy_metals(db: Session = Depends(get_db)):
    """Returns all heavy metals and their health impact factors."""
    metals = db.query(HeavyMetal).all()
    # If empty, return a dummy list for Demo Dashboard
    if not metals:
        return [
            {"id": 1, "symbol": "Pb", "name": "Lead", "standard_limit": 0.01, "health_effects": "Neurological damage, kidney disease."},
            {"id": 2, "symbol": "As", "name": "Arsenic", "standard_limit": 0.01, "health_effects": "Skin lesions, cancer, cardiovascular disease."},
            {"id": 3, "symbol": "Cd", "name": "Cadmium", "standard_limit": 0.003, "health_effects": "Bone demineralization, renal dysfunction."},
            {"id": 4, "symbol": "Hg", "name": "Mercury", "standard_limit": 0.001, "health_effects": "Brain and nervous system damage."}
        ]
    return metals

@router.get("/materials")
def get_education_materials(db: Session = Depends(get_db)):
    materials = db.query(EducationMaterial).all()
    if not materials:
        return [
            {"id": 1, "type": "article", "title": "How does Lead enter groundwater?", "content_markdown": "Lead typically enters drinking water from pipes and plumbing fixtures."},
            {"id": 2, "type": "fact", "title": "WHO Drinking Water Guidelines", "content_markdown": "The WHO sets parametric values for over 50 chemicals in drinking water."}
        ]
    return materials
