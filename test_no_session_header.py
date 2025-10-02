"""
Test WITHOUT cp-book-facility-session-id header
"""
from perfectgym_client import PerfectGymClient
from datetime import datetime

# Login
client = PerfectGymClient()
if not client.login("sagameko@gmail.com", "Ha.Duong2000"):
    exit(1)

start_time = datetime(2025, 10, 7, 6, 0, 0)
zone_id = 87

# Minimal headers - let server manage the session
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
print(f"Cookies after Start: {list(client.session.cookies.keys())}")

print("\nStep 2: Setting details (immediately after Start)...")
details_payload = {
    "UserId": client.user_id,
    "ZoneId": zone_id,
    "StartTime": start_time.strftime('%Y-%m-%dT%H:%M:%S'),
    "Duration": 30,
    "RequiredNumberOfSlots": None
}

details_response = client.session.post(
    f"{client.base_url}/ClientPortal2/FacilityBookings/WizardSteps/SetFacilityBookingDetailsWizardStep/Next",
    json=details_payload
)

print(f"Details status: {details_response.status_code}")
if details_response.status_code == 200:
    print("✓ SUCCESS!")
    data = details_response.json()
    rule_id = data['Data']['RuleId']

    print(f"\nStep 3: Confirming...")
    confirm_response = client.session.post(
        f"{client.base_url}/ClientPortal2/FacilityBookings/WizardSteps/ChooseBookingRuleStep/Next",
        json={
            "ruleId": rule_id,
            "OtherCalendarEventBookedAtRequestedTime": False,
            "HasUserRequiredProducts": False,
            "ShouldBuyRequiredProductOnDebit": True
        }
    )
    if confirm_response.status_code == 200:
        print("\n🎉 BOOKING SUCCESSFUL!")
        print(confirm_response.json())
    else:
        print(f"Confirm failed: {confirm_response.text[:200]}")
else:
    print(f"Details failed: {details_response.text[:200]}")
