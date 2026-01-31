import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.base import Base
from typing import Generator

# 1. Load environment variables
load_dotenv()

from app.core.config import settings

# 2. Database Connection
DATABASE_URL = settings.DATABASE_URL

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


def get_db() -> Generator:
    """
    Dependency function to yield a database session.
    Ensures the session is closed after the request is completed.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Allow running this file directly to test setup
if __name__ == "__main__":
    init_db()