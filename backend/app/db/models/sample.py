from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from traitlets import Bool
from geoalchemy2 import Geography
import enum
from app.db.base_class import Base

class SourceType(str, enum.Enum):
    GROUNDWATER = "Groundwater"
    EFFLUENT = "Industrial Effluent"
    SURFACE = "Surface Water"

class Sample(Base):
    __tablename__ = "samples"

    id = Column(Integer, primary_key=True, index=True)
    # PostGIS point: SRID 4326 is the standard for WGS84 (Lat/Long)
    location = Column(Geography(geometry_type='POINT', srid=4326), nullable=False)
    timestamp = Column(DateTime, nullable=False)
    source_type = Column(Enum(SourceType), nullable=False) # e.g., Handpump, River [cite: 152]
    
    # Context for calculations
    standard_preference = Column(String, default="BIS") # [cite: 244]
    background_reference = Column(String, default="Average_Shale") # [cite: 89, 90]

    measurements = relationship("Measurement", back_populates="sample", cascade="all, delete")
    assessment = relationship("RiskAssessment", back_populates="sample", uselist=False, cascade="all, delete-orphan")

class Measurement(Base):
    __tablename__ = "measurements"

    id = Column(Integer, primary_key=True, index=True)
    sample_id = Column(Integer, ForeignKey("samples.id"), nullable=False)
    
    # Metal type (As, Pb, etc.) and its standardized concentration (mg/L)
    metal = Column(String, nullable=False) # [cite: 80, 186]
    concentration = Column(Float, nullable=False) # Always stored in mg/L [cite: 254]
    
    # TODO: Define the back-reference to Sample
    sample = relationship("Sample", back_populates="measurements")


