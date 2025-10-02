"""
Debug booking to see what Start returns
"""
from perfectgym_client import PerfectGymClient
from datetime import datetime
import uuid

# Login
client = PerfectGymClient()
print("Logging in...")

if not client.login("sagameko@gmail.com", "Ha.Duong2000"):
    print("Login failed!")
    exit(1)

print("\nTesting Start endpoint...")

session_id = str(uuid.uuid4())
start_url = f"{client.base_url}/ClientPortal2/FacilityBookings/BookFacility/Start"
start_params = {
    "clubId": 1,
    "startDate": "2025-10-06T06:00:00",
    "zoneTypeId": 28,
    "RedirectUrl": f"https://statesportcentres.perfectgym.com.au/ClientPortal2/#/FacilityBooking?clubId=1&zoneTypeId=28&sessionId={session_id}"
}

response = client.session.get(start_url, params=start_params)

print(f"Status Code: {response.status_code}")
print(f"Cookies after Start: {dict(client.session.cookies)}")
print(f"\nResponse JSON:")
import json
print(json.dumps(response.json(), indent=2)[:1000])
