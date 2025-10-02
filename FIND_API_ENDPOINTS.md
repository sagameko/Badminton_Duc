# How to Find the Correct API Endpoints

## Step-by-Step Guide

### 1. Open Browser Developer Tools

1. Open **Chrome** or **Firefox**
2. Press **F12** to open Developer Tools
3. Click on the **Network** tab
4. Make sure "Preserve log" is checked (important!)

### 2. Clear and Start Recording

1. Click the **Clear** button (🚫) in the Network tab to clear all entries
2. Make sure recording is enabled (red dot should be active)

### 3. Login to PerfectGym

1. Navigate to: https://statesportcentres.perfectgym.com.au/ClientPortal2/#/FacilityBooking?clubId=1&zoneTypeId=28
2. **If already logged in, logout first**
3. Enter your credentials:
   - Email: `sagameko@gmail.com`
   - Password: `Ha.Duong2000`
4. Click Login

### 4. Find the Login API Call

1. In the Network tab, look for a **POST** request (usually highlighted in red/pink)
2. Common names to look for:
   - `Login`
   - `Auth`
   - `Authenticate`
   - `SignIn`
   - Or something with "login" or "auth" in the name

3. Click on that request to see details

### 5. Extract Login Information

Once you find the login request, note down:

#### Request URL (Example):
```
https://statesportcentres.perfectgym.com.au/ClientPortal/Api/Users/Authenticate
```

#### Request Headers:
Look for important headers like:
- `Content-Type: application/json`
- Any custom headers (like `X-API-Key`, `Authorization`, etc.)

#### Request Payload (Body):
This shows what data was sent. Example:
```json
{
  "email": "sagameko@gmail.com",
  "password": "Ha.Duong2000",
  "clubId": 1
}
```

#### Response:
This shows what came back. Example:
```json
{
  "accessToken": "eyJhbGc...",
  "userId": 12345,
  "email": "sagameko@gmail.com",
  "firstName": "John"
}
```

### 6. Find Schedule/Booking API Calls

After logging in:

1. Keep the Network tab open
2. Navigate to the facility booking page
3. Look for XHR/Fetch requests that load the schedule
4. Common names:
   - `Schedule`
   - `Availability`
   - `Slots`
   - `FacilityBooking`

5. Click on these requests and note:
   - Request URL
   - Request Method (GET/POST)
   - Query parameters
   - Response structure

### 7. Find Booking API Call

1. Try to book a court (you can cancel it after)
2. Look for a POST request when you click the booking button
3. Note the:
   - Request URL
   - Request payload structure
   - Response

### 8. Update the Code

Once you have all the information, I'll help you update `perfectgym_client.py` with the correct endpoints.

## Quick Tips

- **Filter by XHR/Fetch**: In the Network tab, click "XHR" or "Fetch" to filter out images, CSS, etc.
- **Search**: Use Ctrl+F in the Network tab to search for keywords like "login", "auth", "book"
- **Right-click on request** → "Copy as cURL" or "Copy as fetch" to see the exact request

## Example Screenshot Locations

When you find the right request, take screenshots or copy:
1. The request URL
2. The Request Headers tab
3. The Request Payload/Body tab
4. The Response tab

## Need Help?

After you gather this information, send me:
1. The login endpoint URL
2. The request payload structure
3. The response structure
4. Any special headers needed

I'll update the code for you!
