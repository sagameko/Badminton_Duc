"""
Test with ALL the exact headers from browser
"""
from perfectgym_client import PerfectGymClient
from datetime import datetime
import uuid

# Login
client = PerfectGymClient()
if not client.login("sagameko@gmail.com", "Ha.Duong2000"):
    exit(1)

start_time = datetime(2025, 10, 7, 6, 0, 0)
zone_id = 87
session_id = str(uuid.uuid4())

# Add ALL the headers from browser
wizard_url = f"https://statesportcentres.perfectgym.com.au/ClientPortal2/#/FacilityBooking?clubId=1&zoneTypeId=28&sessionId={session_id}"
client.session.headers.update({
    'baf-wizard-currenturl': wizard_url,
    'cp-book-facility-session-id': session_id,
    'x-hash': '#/FacilityBooking?clubId=1&zoneTypeId=28',
    'Origin': 'https://statesportcentres.perfectgym.com.au',
    'Referer': 'https://statesportcentres.perfectgym.com.au/ClientPortal2/',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin'
})

print(f"Session ID: {session_id}")
print("\nStep 1: Starting wizard...")
start_response = client.session.get(
    f"{client.base_url}/ClientPortal2/FacilityBookings/BookFacility/Start",
    params={
        "clubId": 1,
        "startDate": start_time.strftime('%Y-%m-%dT%H:%M:%S'),
        "zoneTypeId": 28,
        "RedirectUrl": wizard_url
    }
)
print(f"Start status: {start_response.status_code}")

print("\nStep 2: Setting details...")
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
    print("✓ SUCCESS on step 2!")
    data = details_response.json()
    rule_id = data['Data']['RuleId']
    print(f"Rule ID: {rule_id}")

    print("\nStep 3: Confirming booking...")
    confirm_response = client.session.post(
        f"{client.base_url}/ClientPortal2/FacilityBookings/WizardSteps/ChooseBookingRuleStep/Next",
        json={
            "ruleId": rule_id,
            "OtherCalendarEventBookedAtRequestedTime": False,
            "HasUserRequiredProducts": False,
            "ShouldBuyRequiredProductOnDebit": True
        }
    )
    print(f"Confirm status: {confirm_response.status_code}")
    if confirm_response.status_code == 200:
        print("\n🎉🎉🎉 BOOKING SUCCESSFUL! 🎉🎉🎉")
        result = confirm_response.json()
        booking = result['Data']['FacilityBooking']
        print(f"Start: {booking['StartDate']}")
        print(f"Duration: {booking['Duration']}")
        print(f"\n✉️ Check your email for payment instructions!")
    else:
        print(f"Confirm failed: {confirm_response.text}")
else:
    print(f"Details failed: {details_response.text}")
