import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime, func
from sqlalchemy.orm import sessionmaker, declarative_base

# 1. Load environment variables
load_dotenv()

# 2. Database Connection
# Ensure your .env file has valid credentials
DATABASE_URL = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 3. The MetalSense Schema
class WaterSample(Base):
    __tablename__ = "water_samples"

    # Metadata
    id = Column(Integer, primary_key=True, index=True)
    location_name = Column(String, index=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    sampling_date = Column(DateTime(timezone=True), server_default=func.now())

    # Heavy Metals (mg/L or µg/L) - Based on your research paper
    conc_arsenic = Column(Float, default=0.0)   # As
    conc_chromium = Column(Float, default=0.0)  # Cr
    conc_copper = Column(Float, default=0.0)    # Cu
    conc_iron = Column(Float, default=0.0)      # Fe
    conc_manganese = Column(Float, default=0.0) # Mn
    conc_nickel = Column(Float, default=0.0)    # Ni
    conc_lead = Column(Float, default=0.0)      # Pb
    conc_zinc = Column(Float, default=0.0)      # Zn
    conc_cadmium = Column(Float, default=0.0)   # Cd (Common in heavy metal indices)
    conc_mercury = Column(Float, default=0.0)   # Hg (Common high risk)

    # Calculated Indices
    hpi_score = Column(Float, nullable=True)    # Heavy Metal Pollution Index
    hei_score = Column(Float, nullable=True)    # Heavy Metal Evaluation Index
    mi_score = Column(Float, nullable=True)     # Metal Index
    
    # Risk Assessment
    risk_level = Column(String, nullable=True)  # e.g., "Safe", "Low", "High"

# 4. Initialization Function
def init_db():
    print("⏳ Connecting to database...")
    try:
        # This checks the DB and creates tables if they don't exist
        Base.metadata.create_all(bind=engine)
        print("✅ Success! Table 'water_samples' created.")
    except Exception as e:
        print(f"❌ Error: {e}")

# Allow running this file directly to test setup
if __name__ == "__main__":
    init_db()