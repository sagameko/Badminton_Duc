# 🏸 Badminton Court Booking Application

A Streamlit-based application for viewing badminton court availability at State Sport Centres (PerfectGym platform) with quick browser booking access.

## Features

- ✅ User authentication and account management
- ✅ Secure credential storage (encrypted)
- ✅ View badminton court availability in real-time
- ✅ One-click "Book in Browser" for quick booking
- ✅ Clean, organized schedule view grouped by date
- ✅ Direct links to manage bookings on PerfectGym

## Installation

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Setup encryption key:**
   ```bash
   # Generate an encryption key
   python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
   ```

3. **Create .env file:**
   - Copy `.env.example` to `.env`
   - Add the generated encryption key to the `ENCRYPTION_KEY` variable

4. **Run the application:**
   ```bash
   streamlit run app.py
   ```

## Usage

### First Time Setup

1. **Register an account:**
   - Open the app and go to the "Register" tab
   - Create a username and password for the app

2. **Login:**
   - Use your newly created credentials to login

3. **Setup PerfectGym credentials:**
   - Enter your badminton website email and password
   - Click "Save & Test Credentials"

### Viewing and Booking Courts

1. **View Schedule:**
   - Navigate to "View Schedule"
   - Select date range and click "Fetch Schedule"
   - Browse available time slots organized by date

2. **Book a Court:**
   - Find your preferred time slot
   - Click "📱 Book" button
   - Complete booking on the PerfectGym website (opens in new tab)
   - Check your email for payment instructions

3. **Manage Bookings:**
   - Go to "My Bookings"
   - Click "Open My Bookings in Browser" to view/cancel on PerfectGym

## Security

- User passwords are hashed using bcrypt
- PerfectGym credentials are encrypted using Fernet (symmetric encryption)
- All data is stored locally in JSON files
- Never commit `.env`, `users.json`, or `credentials.json` to version control

## Important Notes

⚠️ **Booking Process:** The app displays available courts and provides quick access to book via the PerfectGym website. Automated booking is not supported due to platform restrictions.

⚠️ **Payment:** After booking, you'll receive an email with payment instructions. Payment must be completed to confirm your booking.

⚠️ **Credentials:** Your PerfectGym credentials are encrypted and stored locally. Never share your credentials or commit them to version control.

## Troubleshooting

### Login fails with "Failed to authenticate"

The API endpoints in `perfectgym_client.py` may need to be updated. To find the correct endpoints:

1. Open your browser's Developer Tools (F12)
2. Go to the Network tab
3. Login to the PerfectGym website manually
4. Look for API calls and update the endpoints in `perfectgym_client.py`

### Schedule not loading

Similar to login issues, you may need to inspect the network traffic to find the correct API endpoint for fetching schedules.

## Project Structure

```
.
├── app.py                  # Main Streamlit application
├── auth.py                 # User authentication module
├── storage.py              # Secure credential storage
├── perfectgym_client.py    # PerfectGym API client
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (create this)
├── .env.example           # Environment variables template
├── users.json             # User data (auto-generated)
└── credentials.json       # Encrypted credentials (auto-generated)
```

## License

This is a personal project for educational purposes.
