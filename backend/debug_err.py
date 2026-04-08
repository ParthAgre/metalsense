import requests
API_URL = "http://127.0.0.1:8000/api/v1"
login_data = {"email": "researcher1@example.com", "password": "password"}
resp = requests.post(f"{API_URL}/auth/login", json=login_data)
token = resp.json().get("access_token")
headers = {"Authorization": f"Bearer {token}"} if token else {}
r = requests.get(f"{API_URL}/researcher/samples", headers=headers)
print(f"GET /samples -> {r.status_code}")
print(r.text)
