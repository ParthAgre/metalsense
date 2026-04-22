from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.db.models.user import User, UserRole
from app.core import security

def seed_users():
    db: Session = SessionLocal()
    try:
        common_pwd = security.get_password_hash("password123")
        
        citizen_user = db.query(User).filter(User.email == "citizen@metalsense.com").first()
        if not citizen_user:
            citizen_user = User(
                email="citizen@metalsense.com",
                hashed_password=common_pwd,
                full_name="Standard Citizen",
                role=UserRole.citizen,
                is_active=True
            )
            db.add(citizen_user)

        res_user = db.query(User).filter(User.email == "researcher@metalsense.com").first()
        if not res_user:
            res_user = User(
                email="researcher@metalsense.com",
                hashed_password=common_pwd,
                full_name="Lead Researcher",
                role=UserRole.researcher,
                is_active=True
            )
            db.add(res_user)
            
        db.commit()
        print("Demo accounts citizen@metalsense.com and researcher@metalsense.com created successfully!")
    except Exception as e:
        db.rollback()
        print(f"Error seeding users: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_users()
