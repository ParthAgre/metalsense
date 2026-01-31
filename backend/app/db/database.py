import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.base import Base
from typing import Generator

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