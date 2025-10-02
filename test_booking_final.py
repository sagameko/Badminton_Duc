"""
Final booking test with simplified approach
"""
from perfectgym_client import PerfectGymClient
from datetime import datetime

# Login
client = PerfectGymClient()
print("Logging in...")

if not client.login("sagameko@gmail.com", "Ha.Duong2000"):
    print("Login failed!")
    exit(1)

print("\nAttempting to book a court...")
print("=" * 60)

# Try to book Court (zone_id 87) for Oct 6 at 6:00 AM for 30 minutes
zone_id = 87
start_time = datetime(2025, 10, 6, 6, 0, 0)
duration = 30

print(f"Court Zone ID: {zone_id}")
print(f"Start: {start_time}")
print(f"Duration: {duration} minutes")
print("=" * 60)

result = client.book_court(
    zone_id=zone_id,
    start_time=start_time,
    duration_minutes=duration
)

print("\n" + "=" * 60)
if result["success"]:
    print("SUCCESS! COURT BOOKED!")
    print("=" * 60)
    print(f"User: {result.get('user')}")
    print(f"Start Time: {result.get('start_time')}")
    print(f"Duration: {result.get('duration')}")
    print("\n" + result.get('message'))
else:
    print("BOOKING FAILED")
    print("=" * 60)
    print(f"Error: {result.get('error')}")
print("=" * 60)
