"""
Debug exact payload we're sending
"""
from perfectgym_client import PerfectGymClient
from datetime import datetime
import json

# Login
client = PerfectGymClient()
if not client.login("sagameko@gmail.com", "Ha.Duong2000"):
    exit(1)

start_time = datetime(2025, 10, 7, 6, 0, 0)
zone_id = 87

# Step 1: Start
print("Step 1: Starting wizard...")
start_response = client.session.get(
    f"{client.base_url}/ClientPortal2/FacilityBookings/BookFacility/Start",
    params={
        "clubId": 1,
        "startDate": start_time.strftime('%Y-%m-%dT%H:%M:%S'),
        "zoneTypeId": 28,
        "RedirectUrl": f"{client.base_url}/ClientPortal2/"
    }
)
print(f"Start status: {start_response.status_code}")

# Step 2: Details
print("\nStep 2: Setting details...")
details_payload = {
    "UserId": client.user_id,
    "ZoneId": zone_id,
    "StartTime": start_time.strftime('%Y-%m-%dT%H:%M:%S'),
    "Duration": 30,
    "RequiredNumberOfSlots": None
}

print("\nPayload we're sending:")
print(json.dumps(details_payload, indent=2))

print("\nBrowser payload:")
print('{"UserId":287499,"ZoneId":87,"StartTime":"2025-10-07T06:00:00","RequiredNumberOfSlots":null,"Duration":30}')

print("\nAre they identical?")
browser_payload = {"UserId":287499,"ZoneId":87,"StartTime":"2025-10-07T06:00:00","RequiredNumberOfSlots":None,"Duration":30}
print(f"Our payload == Browser: {details_payload == browser_payload}")

print("\nSending request...")
details_response = client.session.post(
    f"{client.base_url}/ClientPortal2/FacilityBookings/WizardSteps/SetFacilityBookingDetailsWizardStep/Next",
    json=details_payload
)

print(f"Response status: {details_response.status_code}")
print(f"Response: {details_response.text[:500]}")
