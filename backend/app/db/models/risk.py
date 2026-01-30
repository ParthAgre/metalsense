from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from traitlets import Bool
from app.db.base_class import Base # Assuming your declarative_base is here
import enum

class RiskAssessment(Base):
    __tablename__ = "risk_assessments"

    id = Column(Integer, primary_key=True, index=True)
    sample_id = Column(Integer, ForeignKey("samples.id"), nullable=False)
    
    # Calculated Indices
    hpi = Column(Float)  # Heavy Metal Pollution Index [cite: 231]
    hei = Column(Float)  # Heavy Metal Evaluation Index [cite: 238]
    mi = Column(Float)   # Metal Index [cite: 241]
    i_geo_max = Column(Float)  # Max Geo-accumulation Index [cite: 90]
    
    # Health Risks
    hazard_index = Column(Float)  # Non-carcinogenic risk [cite: 304]
    cancer_risk_child = Column(Float)  # Lifetime cancer risk for children [cite: 308, 321]
    
    # Simplified status for Citizens
    risk_category = Column(String)  # e.g., "Extensively Polluted" [cite: 175]
    is_safe = Column(Bool, default=True) # Binary flag for the "Traffic Light" map

    sample = relationship("Sample", back_populates="assessment")