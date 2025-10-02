"""
Test court booking with zone 87
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

# Use zone 87 like in the browser example
zone_id = 87
start_time = datetime(2025, 10, 6, 6, 0, 0)
duration = 30

print(f"Zone ID: {zone_id}")
print(f"Start: {start_time}")
print(f"Duration: {duration} min")

success = client.book_court(
    zone_id=zone_id,
    start_time=start_time,
    duration_minutes=duration
)

if success:
    print("\nSUCCESS!")
else:
    print("\nFailed")
