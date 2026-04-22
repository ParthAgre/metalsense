import sys
import os
# Add the current directory to sys.path to allow importing 'app'
sys.path.append(os.getcwd())

from app.db.database import engine, Base
from seed_metals import seed_metals
from seed_users import seed_users
from app.db.base import Base # Ensure all models are loaded [cite: 1]

def reset_db():
    print("Dropping all tables...")
    Base.metadata.drop_all(bind=engine)
    
    print("Recreating all tables...")
    Base.metadata.create_all(bind=engine)
    
    print("Seeding database...")
    seed_metals()
    seed_users()
    
    print("Database reset and seeded successfully!")

if __name__ == "__main__":
    reset_db()
