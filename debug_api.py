"""
Debug script to help find the correct PerfectGym API endpoints
This script will attempt different common API patterns
"""
import requests
import json


def test_login_endpoints():
    """Test various common login endpoint patterns"""
    base_url = "https://statesportcentres.perfectgym.com.au"

    email = "sagameko@gmail.com"
    password = "Ha.Duong2000"
    club_id = 1

    # Common endpoint patterns to try
    endpoints = [
        "/Api/Users/Login",
        "/api/users/login",
        "/ClientPortal2/Api/Users/Login",
        "/Api/Account/Login",
        "/api/Account/Login",
        "/ClientPortal/Api/Users/Login",
        "/Api/Auth/Login",
        "/api/auth/login",
    ]

    # Common payload patterns
    payload_patterns = [
        {"email": email, "password": password, "clubId": club_id},
        {"username": email, "password": password, "clubId": club_id},
        {"email": email, "password": password},
        {"login": email, "password": password, "clubId": club_id},
        {"Email": email, "Password": password, "ClubId": club_id},
    ]

    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Content-Type': 'application/json',
        'Origin': 'https://statesportcentres.perfectgym.com.au',
        'Referer': 'https://statesportcentres.perfectgym.com.au/ClientPortal2/',
    })

    print("Testing different API endpoint patterns...\n")
    print("=" * 80)

    for endpoint in endpoints:
        for i, payload in enumerate(payload_patterns):
            url = f"{base_url}{endpoint}"

            try:
                response = session.post(url, json=payload, timeout=10)

                print(f"\n[TEST] {endpoint} | Payload Pattern {i+1}")
                print(f"Status: {response.status_code}")

                if response.status_code != 404:
                    print(f"Headers: {dict(response.headers)}")

                    try:
                        print(f"Response: {response.json()}")
                    except:
                        print(f"Response (text): {response.text[:200]}")

                    if response.status_code in [200, 201]:
                        print("\n" + "=" * 80)
                        print("✅ POTENTIAL SUCCESS!")
                        print(f"Endpoint: {endpoint}")
                        print(f"Payload: {json.dumps(payload, indent=2)}")
                        print("=" * 80)
                        return

            except requests.exceptions.Timeout:
                print(f"[TIMEOUT] {endpoint} | Payload Pattern {i+1}")
            except requests.exceptions.ConnectionError:
                print(f"[CONNECTION ERROR] {endpoint} | Payload Pattern {i+1}")
            except Exception as e:
                print(f"[ERROR] {endpoint} | Payload Pattern {i+1}: {str(e)}")

    print("\n" + "=" * 80)
    print("No successful endpoint found. You'll need to inspect network traffic manually.")
    print("=" * 80)


if __name__ == "__main__":
    print("PerfectGym API Endpoint Debugger")
    print("=" * 80)
    print("This script tests common API patterns to find the correct login endpoint.\n")

    test_login_endpoints()

    print("\n\nMANUAL INSPECTION GUIDE:")
    print("1. Open Chrome/Firefox and press F12 to open Developer Tools")
    print("2. Go to the Network tab")
    print("3. Navigate to: https://statesportcentres.perfectgym.com.au/ClientPortal2/")
    print("4. Login with your credentials")
    print("5. Look for a POST request (usually named 'Login' or similar)")
    print("6. Click on it and check:")
    print("   - Request URL (the endpoint)")
    print("   - Request Headers")
    print("   - Request Payload (the data sent)")
    print("   - Response (what comes back)")
    print("\nOnce you find it, update the perfectgym_client.py file accordingly.")
