import requests
import os

API_URL = "http://127.0.0.1:8000/api/v1"

# 1. Login as researcher
login_data = {"email": "researcher1@example.com", "password": "password"}
resp = requests.post(f"{API_URL}/auth/login", json=login_data)
if resp.status_code != 200:
    print(f"Login failed: {resp.text}")
    exit(1)
token = resp.json()["access_token"]
headers = {"Authorization": f"Bearer {token}"}

# 2. Create a dummy CSV
csv_content = """lat,lng,timestamp,source_type,metal,concentration
23.5,78.9,2026-04-08 12:00:00,Groundwater,Arsenic,0.05
24.1,79.2,2026-04-08 13:00:00,Surface Water,Lead,0.02
"""
with open("dummy.csv", "w") as f:
    f.write(csv_content)

# 3. Upload the CSV
with open("dummy.csv", "rb") as f:
    files = {"file": ("dummy.csv", f, "text/csv")}
    upload_resp = requests.post(f"{API_URL}/researcher/upload-csv", headers=headers, files=files)

print("Status:", upload_resp.status_code)
print("Response:", upload_resp.json())

# 4. Check if samples are accessible
try:
    samples = requests.get(f"{API_URL}/researcher/samples")
    print("Samples length:", len(samples.json()))
except Exception as e:
    print(e)
