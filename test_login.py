"""
Quick test script to verify login works
"""
from perfectgym_client import PerfectGymClient

# Test login
client = PerfectGymClient()
print("Testing login...")

success = client.login("sagameko@gmail.com", "Ha.Duong2000")

if success:
    print("\n✅ LOGIN SUCCESSFUL!")
    print(f"User ID: {client.user_id}")
    print(f"Email: {client.email}")
    print("\nSession cookies:")
    for cookie in client.session.cookies:
        print(f"  {cookie.name}: {cookie.value[:50]}...")
else:
    print("\n❌ LOGIN FAILED!")
