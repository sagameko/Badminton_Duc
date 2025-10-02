# Quick Start Guide

## First Time Setup

1. **Install dependencies** (if not already done):
   ```bash
   pip install -r requirements.txt
   ```

2. **Get Gemini API Key** (for AI chat - optional but recommended):
   - Visit: https://makersuite.google.com/app/apikey
   - Sign in with Google
   - Click "Create API Key"
   - Copy your key

3. **Run setup**:
   ```bash
   python setup.py
   ```
   - You'll be prompted to enter your Gemini API key
   - Paste it when asked (or skip to use basic chat)

4. **Start the app**:
   ```bash
   streamlit run app.py
   ```

## Using the App

### 1. Create Your Account
- Click the "Register" tab
- Choose a username and password (for the app)
- Click "Register"

### 2. Login
- Enter your app username and password
- Click "Login"

### 3. Setup PerfectGym Credentials
- Enter your PerfectGym email: `sagameko@gmail.com`
- Enter your PerfectGym password: `Ha.Duong2000`
- Click "Save & Test Credentials"

### 4. Use AI Chat (Recommended!)
- Go to "Chat" tab
- Ask naturally: "What's available tomorrow?"
- Or: "Show me courts on Friday at 6pm"
- The AI will understand and show available slots
- Click the booking link to reserve

### 5. View Available Courts (Alternative)
- Go to "View Schedule"
- Select how many days to show (1, 3, 7, or 14 days)
- Click "Fetch Schedule"
- Browse available time slots organized by date

### 6. Book a Court
- Find a time slot you want
- Click the "Book" button next to it
- This opens the PerfectGym website in your browser
- Complete the booking there
- Check your email for payment instructions

### 7. Manage Bookings
- Go to "My Bookings"
- Click "Open My Bookings in Browser"
- View/cancel bookings on the PerfectGym website

## Tips

- The app saves your PerfectGym credentials securely (encrypted)
- You only need to enter them once
- Schedule data is fetched in real-time from PerfectGym
- Booking opens in your browser for security and payment

## Troubleshooting

**Can't see any schedules?**
- Check your PerfectGym credentials in Settings
- Make sure you're connected to the internet

**Book button doesn't work?**
- Make sure pop-ups are allowed in your browser
- The booking page should open in a new tab

**Need to change credentials?**
- Go to Settings → Update Credentials
