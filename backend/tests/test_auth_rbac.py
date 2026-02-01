from fastapi.testclient import TestClient
from app.main import app
from app.db.database import SessionLocal, init_db
from app.api import deps
from app.db.models.user import User, UserRole
from app.core import security
import pytest

# Setup Test Client
client = TestClient(app)

def setup_module(module):
    """Setup logic to run before tests"""
    init_db()
    
# Helpers
def create_test_user(email: str, role: UserRole):
    db = SessionLocal()
    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        db.close()
        return existing_user
    
    user = User(
        email=email,
        hashed_password=security.get_password_hash("testpassword"),
        full_name=f"Test {role.value.capitalize()}",
        role=role,
        is_active=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    db.close()
    return user

def get_auth_header(email: str):
    response = client.post("/api/v1/auth/login", json={"email": email, "password": "testpassword"})
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def test_register_citizen():
    response = client.post(
        "/api/v1/users/register",
        json={"email": "newcitizen@example.com", "password": "testpassword", "full_name": "New Citizen", "role": "citizen"}
    )
    # 200 OK or 400 if already exists
    if response.status_code == 400:
        assert response.json()["detail"] == "Email already registered"
    else:
        assert response.status_code == 200
        assert response.json()["email"] == "newcitizen@example.com"
        assert response.json()["role"] == "citizen"

def test_login_and_me():
    create_test_user("login@example.com", UserRole.citizen)
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "login@example.com", "password": "testpassword"}
    )
    assert response.status_code == 200
    token = response.json()["access_token"]
    
    headers = {"Authorization": f"Bearer {token}"}
    response_me = client.get("/api/v1/users/me", headers=headers)
    assert response_me.status_code == 200
    assert response_me.json()["email"] == "login@example.com"

def test_rbac_citizen_access_researcher_route():
    # Citizen logic
    create_test_user("citizen@example.com", UserRole.citizen)
    headers = get_auth_header("citizen@example.com")
    
    # Try to access researcher-only route (create sample)
    # We use dummy data
    payload = {
        "latitude": 10.0,
        "longitude": 10.0,
        "timestamp": "2023-01-01T12:00:00",
        "source_type": "Groundwater",
        "standard_preference": "WHO",
        "measurements": []
    }
    
    response = client.post("/api/v1/researcher/samples", json=payload, headers=headers)
    # Expect 403 Forbidden
    assert response.status_code == 403
    print("✅ Citizen correctly denied access to researcher route.")

def test_rbac_researcher_access_researcher_route():
    # Researcher logic
    create_test_user("researcher@example.com", UserRole.researcher)
    headers = get_auth_header("researcher@example.com")
    
    # Try to access researcher-only route
    payload = {
        "latitude": 10.0,
        "longitude": 10.0,
        "timestamp": "2023-01-01T12:00:00",
        "source_type": "Groundwater",
        "standard_preference": "WHO",
        "measurements": []
    }
    
    # If 202 (Created) or 422 (Validation Error), success (Auth passed).
    # If 403, FAILURE (Auth failed).
    # If 500, FAILURE (DB Error - PostGIS might still be broken).
    
    response = client.post("/api/v1/researcher/samples", json=payload, headers=headers)
    
    if response.status_code == 403:
        pytest.fail("Researcher was denied access!")
    elif response.status_code == 500:
        pytest.fail(f"Server Error (DB may be broken): {response.text}")
        
    print(f"✅ Researcher allowed access (Status: {response.status_code})")

if __name__ == "__main__":
    # Simple manual run
    try:
        setup_module(None)
        test_register_citizen()
        test_login_and_me()
        test_rbac_citizen_access_researcher_route()
        test_rbac_researcher_access_researcher_route()
        print("\n🎉 All Auth & RBAC tests passed!")
    except Exception as e:
        print(f"\n❌ Tests Failed: {e}")
        # raise e
