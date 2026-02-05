from fastapi.testclient import TestClient
from app.main import app
from app.db.database import SessionLocal, init_db
from app.api import deps
from app.db.models.user import User, UserRole
from app.core import security
import pytest
from tests.test_auth_rbac import create_test_user, get_auth_header

client = TestClient(app)

def setup_module(module):
    init_db()

def test_change_password():
    email = "changepass@example.com"
    create_test_user(email, UserRole.citizen)
    headers = get_auth_header(email)
    
    # login with old password should work
    login_resp = client.post("/api/v1/auth/login", json={"email": email, "password": "testpassword"})
    assert login_resp.status_code == 200

    # Change password
    payload = {
        "current_password": "testpassword",
        "new_password": "newpassword123"
    }
    response = client.post("/api/v1/users/change-password", json=payload, headers=headers)
    assert response.status_code == 200
    assert response.json()["email"] == email
    
    # Old password should fail
    fail_resp = client.post("/api/v1/auth/login", json={"email": email, "password": "testpassword"})
    assert fail_resp.status_code == 401
    
    # New password should work
    success_resp = client.post("/api/v1/auth/login", json={"email": email, "password": "newpassword123"})
    assert success_resp.status_code == 200

def test_refresh_token():
    email = "refresh@example.com"
    create_test_user(email, UserRole.citizen)
    headers = get_auth_header(email)
    
    response = client.post("/api/v1/auth/refresh-token", headers=headers)
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

def test_logout():
    email = "logout@example.com"
    create_test_user(email, UserRole.citizen)
    
    response = client.post("/api/v1/auth/logout")
    assert response.status_code == 200
    assert response.json()["msg"] == "Successfully logged out"

def test_password_recovery_flow():
    email = "recovery@example.com"
    create_test_user(email, UserRole.citizen)
    
    # 1. Request recovery
    response = client.post(f"/api/v1/auth/password-recovery/{email}")
    assert response.status_code == 200
    
    # Since we mock the email sending, we can't easily get the token from the response or creating it manually 
    # and mocking the verify function, OR we can just test the reset endpoint independently with a manually created token.
    
    # Manually create a reset token
    reset_token = security.create_access_token(data={"sub": email})
    
    # 2. Reset Password
    payload = {
        "token": reset_token,
        "new_password": "resetpassword123"
    }
    
    # Note: Body param in FastAPI for singular values can be tricky if not JSON object.
    # Our endpoint expects: token: str = Body(...), new_password: str = Body(...)
    # This means it expects a JSON body like: {"token": "...", "new_password": "..."}
    
    reset_response = client.post("/api/v1/auth/reset-password", json=payload)
    assert reset_response.status_code == 200
    
    # 3. Login with new password
    login_resp = client.post("/api/v1/auth/login", json={"email": email, "password": "resetpassword123"})
    assert login_resp.status_code == 200

if __name__ == "__main__":
    try:
        setup_module(None)
        test_change_password()
        test_refresh_token()
        test_logout()
        test_password_recovery_flow()
        print("\n🎉 All Auth Route tests passed!")
    except Exception as e:
        print(f"\n❌ Tests Failed: {e}")
        # raise e
