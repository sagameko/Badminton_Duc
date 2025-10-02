"""
Debug what headers we're sending
"""
from perfectgym_client import PerfectGymClient
from datetime import datetime

# Login
client = PerfectGymClient()
if not client.login("sagameko@gmail.com", "Ha.Duong2000"):
    exit(1)

print("Session headers after login:")
for key, value in client.session.headers.items():
    if key == 'Authorization':
        print(f"  {key}: {value[:50]}...")
    else:
        print(f"  {key}: {value}")

print(f"\nSession cookies:")
for cookie in client.session.cookies:
    print(f"  {cookie.name}: {cookie.value[:50]}...")

print(f"\nAccess token stored: {client.access_token[:50] if client.access_token else 'None'}...")
