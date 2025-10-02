"""
Test court booking
WARNING: This will actually book a court! Make sure to cancel it if you don't want it.
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
print("=" * 50)

# Try to book Court 03 (zone_id 89) for Oct 6 at 6:00 AM for 30 minutes
# Note: Zone IDs are 89-98 for courts 3-12 based on the API response you showed
zone_id = 89  # Court 03 - Accessible Court
start_time = datetime(2025, 10, 6, 6, 0, 0)
duration = 30

print(f"Court: Zone ID {zone_id}")
print(f"Start: {start_time}")
print(f"Duration: {duration} minutes")
print("=" * 50)

success = client.book_court(
    zone_id=zone_id,
    start_time=start_time,
    duration_minutes=duration
)

if success:
    print("\n" + "=" * 50)
    print("SUCCESS! Court booked!")
    print("=" * 50)
else:
    print("\nFailed to book court")
