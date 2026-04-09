from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.db.models.user import User, UserRole
from app.core import security

def seed_users():
    db: Session = SessionLocal()
    try:
        citizen_pwd = security.get_password_hash("password")
        researcher_pwd = security.get_password_hash("password")
        
        citizen_user = db.query(User).filter(User.email == "citizen1@example.com").first()
        if not citizen_user:
            citizen_user = User(
                email="citizen1@example.com",
                hashed_password=citizen_pwd,
                full_name="citizen1",
                role=UserRole.citizen,
                is_active=True
            )
            db.add(citizen_user)

        res_user = db.query(User).filter(User.email == "researcher1@example.com").first()
        if not res_user:
            res_user = User(
                email="researcher1@example.com",
                hashed_password=researcher_pwd,
                full_name="researcher1",
                role=UserRole.researcher,
                is_active=True
            )
            db.add(res_user)
            
        db.commit()
        print("Users citizen1 and researcher1 created successfully!")
    except Exception as e:
        db.rollback()
        print(f"Error seeding users: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_users()
