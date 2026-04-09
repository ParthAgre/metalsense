from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.db.models.metal import HeavyMetal

def seed_metals():
    db: Session = SessionLocal()
    try:
        metals = [
            HeavyMetal(name="Arsenic", symbol="As", standard_limit=0.01, health_effects="Skin lesions, cancer, cardiovascular issues."),
            HeavyMetal(name="Lead", symbol="Pb", standard_limit=0.015, health_effects="Neurological damage, delayed physical development."),
            HeavyMetal(name="Mercury", symbol="Hg", standard_limit=0.002, health_effects="Kidney damage, nervous system disorders."),
            HeavyMetal(name="Cadmium", symbol="Cd", standard_limit=0.005, health_effects="Bone damage, kidney failure."),
        ]
        
        for m in metals:
            existing = db.query(HeavyMetal).filter(HeavyMetal.name == m.name).first()
            if not existing:
                db.add(m)
        db.commit()
        print("Successfully seeded Heavy Metals!")
    except Exception as e:
        db.rollback()
        print(f"Error seeding metals: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_metals()
