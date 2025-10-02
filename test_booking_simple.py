"""
Simplified booking test - minimal headers
"""
from perfectgym_client import PerfectGymClient
from datetime import datetime

# Login
client = PerfectGymClient()
if not client.login("sagameko@gmail.com", "Ha.Duong2000"):
    exit(1)

print("Step 1: Start wizard")
start_response = client.session.get(
    f"{client.base_url}/ClientPortal2/FacilityBookings/BookFacility/Start",
    params={
        "clubId": 1,
        "startDate": "2025-10-06T06:00:00",
        "zoneTypeId": 28,
        "RedirectUrl": "https://statesportcentres.perfectgym.com.au/ClientPortal2/"
    }
)
print(f"Start: {start_response.status_code}")

print("\nStep 2: Set details")
details_response = client.session.post(
    f"{client.base_url}/ClientPortal2/FacilityBookings/WizardSteps/SetFacilityBookingDetailsWizardStep/Next",
    json={
        "UserId": client.user_id,
        "ZoneId": 87,
        "StartTime": "2025-10-06T06:00:00",
        "Duration": 30,
        "RequiredNumberOfSlots": None
    }
)
print(f"Details: {details_response.status_code}")
if details_response.status_code != 200:
    print(f"Error: {details_response.text}")
else:
    print("Success!")
    rule_id = details_response.json()['Data']['RuleId']
    print(f"Rule ID: {rule_id}")

    print("\nStep 3: Confirm booking")
    confirm_response = client.session.post(
        f"{client.base_url}/ClientPortal2/FacilityBookings/WizardSteps/ChooseBookingRuleStep/Next",
        json={
            "ruleId": rule_id,
            "OtherCalendarEventBookedAtRequestedTime": False,
            "HasUserRequiredProducts": False,
            "ShouldBuyRequiredProductOnDebit": True
        }
    )
    print(f"Confirm: {confirm_response.status_code}")
    if confirm_response.status_code == 200:
        print("BOOKING SUCCESSFUL!")
        print(confirm_response.json())
    else:
        print(f"Error: {confirm_response.text}")
