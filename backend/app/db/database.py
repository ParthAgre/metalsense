import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime, func
from sqlalchemy.orm import sessionmaker, declarative_base
from app.db.models.sample import Sample, Measurement # noqa
from app.db.models.risk import RiskAssessment  # noqa
from app.db.base import Base
from app.db.models.sample import Sample, Measurement
from app.db.models.risk import RiskAssessment


# 1. Load environment variables
load_dotenv()

# 2. Database Connection
# Ensure your .env file has valid credentials
DATABASE_URL = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)



# 4. Initialization Function
def init_db():
    print("⏳ Connecting to database...")
    try:
        # This checks the DB and creates tables if they don't exist
        Base.metadata.create_all(bind=engine)
        print("✅ Success! Tables created.")
    except Exception as e:
        print(f"❌ Error: {e}")

# Allow running this file directly to test setup
if __name__ == "__main__":
    init_db()