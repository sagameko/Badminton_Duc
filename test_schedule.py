"""
Test schedule fetching
"""
from perfectgym_client import PerfectGymClient
from datetime import datetime

# Login first
client = PerfectGymClient()
print("Logging in...")

if not client.login("sagameko@gmail.com", "Ha.Duong2000"):
    print("Login failed!")
    exit(1)

print("\nFetching schedule...")
slots = client.get_schedule(days=7)

print(f"\nFound {len(slots)} available slots")

if slots:
    print("\nFirst 10 slots:")
    for i, slot in enumerate(slots[:10]):
        start = datetime.fromisoformat(slot['start_time'])
        end = datetime.fromisoformat(slot['end_time'])
        print(f"{i+1}. {start.strftime('%a %d %b, %I:%M %p')} - {end.strftime('%I:%M %p')} ({slot['duration']})")
else:
    print("No slots found")
