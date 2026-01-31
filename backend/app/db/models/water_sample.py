from sqlalchemy import Column, Integer, Float, String, DateTime, func
from app.db.base_class import Base

class WaterSample(Base):
    __tablename__ = "water_samples"

    # Metadata
    id = Column(Integer, primary_key=True, index=True)
    location_name = Column(String, index=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    sampling_date = Column(DateTime(timezone=True), server_default=func.now())

    # Heavy Metals (mg/L)
    conc_arsenic = Column(Float, default=0.0)   # As
    conc_cadmium = Column(Float, default=0.0)   # Cd
    conc_chromium = Column(Float, default=0.0)  # Cr
    conc_copper = Column(Float, default=0.0)    # Cu
    conc_iron = Column(Float, default=0.0)      # Fe
    conc_lead = Column(Float, default=0.0)      # Pb
    conc_manganese = Column(Float, default=0.0) # Mn
    conc_mercury = Column(Float, default=0.0)   # Hg
    conc_nickel = Column(Float, default=0.0)    # Ni
    conc_zinc = Column(Float, default=0.0)      # Zn

    # Calculated Indices (Stored for historical record)
    hpi_score = Column(Float, nullable=True)    # Heavy Metal Pollution Index
    hei_score = Column(Float, nullable=True)    # Heavy Metal Evaluation Index
    mi_score = Column(Float, nullable=True)     # Metal Index
    
    # Interpretation (Simple string status)
    risk_level = Column(String, nullable=True)  # e.g., "Safe", "Unsafe"
