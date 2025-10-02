"""
PerfectGym API Client for interacting with the badminton booking website
"""
import requests
import uuid
import time
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta


class PerfectGymClient:
    """Client for PerfectGym API"""

    def __init__(self):
        self.base_url = "https://statesportcentres.perfectgym.com.au"
        self.club_id = 1  # From the URL
        self.zone_type_id = 28  # From the URL (badminton courts)
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'X-Requested-With': 'XMLHttpRequest',
            'cp-lang': 'en',
            'cp-mode': 'desktop'
        })
        self.access_token = None
        self.user_id = None
        self.email = None

    def login(self, email: str, password: str) -> bool:
        """
        Authenticate with PerfectGym
        Returns True if successful, False otherwise
        """
        try:
            login_url = f"{self.base_url}/ClientPortal2/Auth/Login"

            payload = {
                "RememberMe": False,
                "Login": email,
                "Password": password
            }

            response = self.session.post(login_url, json=payload)

            if response.status_code == 200:
                data = response.json()
                # Store user information from response
                if 'User' in data and 'Member' in data['User']:
                    member = data['User']['Member']
                    self.user_id = member.get('Id')
                    self.email = member.get('Email')

                    # Extract JWT token from cookies
                    if 'CpAuthToken' in self.session.cookies:
                        self.access_token = self.session.cookies['CpAuthToken']
                        # Add Authorization header for subsequent requests
                        self.session.headers.update({
                            'Authorization': f'Bearer {self.access_token}'
                        })

                    print(f"Successfully logged in as {member.get('FirstName')} {member.get('LastName')}")
                    return True
                else:
                    print("Login response missing expected user data")
                    return False
            else:
                print(f"Login failed with status code: {response.status_code}")
                return False

        except Exception as e:
            print(f"Login error: {e}")
            return False

    def get_schedule(self, date: Optional[datetime] = None, days: int = 7) -> List[Dict[str, Any]]:
        """
        Get badminton court availability schedule

        Args:
            date: Starting date (defaults to today)
            days: Number of days to fetch (default 7)

        Returns:
            List of available time slots (flattened)
        """
        try:
            schedule_url = f"{self.base_url}/ClientPortal2/FacilityBookings/FacilityCalendar/GetWeeklySchedule"

            payload = {
                "clubId": self.club_id,
                "zoneTypeId": str(self.zone_type_id),
                "zoneId": None,
                "daysInWeek": days
            }

            response = self.session.post(schedule_url, json=payload)

            if response.status_code == 200:
                data = response.json()
                # Flatten the nested structure into a simple list of slots
                slots = []

                if 'CalendarData' in data:
                    for hour_block in data['CalendarData']:
                        # Each hour_block has ClassesPerDay which is an array of 7 days
                        for day_index, day_slots in enumerate(hour_block.get('ClassesPerDay', [])):
                            for slot in day_slots:
                                # Only include bookable slots
                                if slot.get('Status') == 'Bookable':
                                    slots.append({
                                        'start_time': slot.get('StartTime'),
                                        'end_time': slot.get('EndTime'),
                                        'duration': slot.get('BookingDuration'),
                                        'status': slot.get('Status'),
                                        'id': slot.get('Id'),
                                        'available_durations': slot.get('Durations', [])
                                    })

                # Sort by start time
                slots.sort(key=lambda x: x['start_time'])
                return slots
            else:
                print(f"Failed to fetch schedule: {response.status_code}")
                return []

        except Exception as e:
            print(f"Schedule fetch error: {e}")
            return []

    def get_booking_url(self, start_time: datetime, zone_id: int = None) -> str:
        """
        Generate a direct URL to book a court in the browser
        Opens the facility booking page with pre-selected time

        Args:
            start_time: Start time for the booking
            zone_id: Optional specific court ID (87-98)

        Returns:
            URL string to open in browser
        """
        # Base URL with club and zone type
        params = {
            "clubId": self.club_id,
            "zoneTypeId": self.zone_type_id,
        }

        param_str = "&".join([f"{k}={v}" for k, v in params.items()])

        # Return the facility booking page
        # The user will need to click on the specific time slot (one click)
        # Then the modal you showed will appear automatically
        return f"{self.base_url}/ClientPortal2/#/FacilityBooking?{param_str}"

    def book_court(self, zone_id: int, start_time: datetime, duration_minutes: int = 30) -> dict:
        """
        Book a badminton court using PerfectGym's booking wizard

        Note: Booking is confirmed but payment must be completed via email instructions

        Args:
            zone_id: ID of the specific court (87-98 for courts 1-12)
            start_time: Start time of booking
            duration_minutes: Duration in minutes (default 30)

        Returns:
            dict with success status and booking details, or error info
        """
        try:
            # Step 1: Start the booking wizard (GET)
            start_url = f"{self.base_url}/ClientPortal2/FacilityBookings/BookFacility/Start"
            start_params = {
                "clubId": self.club_id,
                "startDate": start_time.strftime('%Y-%m-%dT%H:%M:%S'),
                "zoneTypeId": self.zone_type_id,
                "RedirectUrl": f"{self.base_url}/ClientPortal2/"
            }

            start_response = self.session.get(start_url, params=start_params)
            if start_response.status_code != 200:
                return {"success": False, "error": f"Failed to start booking: {start_response.status_code}"}

            # Small delay to mimic human interaction
            time.sleep(0.5)

            # Step 2: Set booking details (court, time, duration)
            details_url = f"{self.base_url}/ClientPortal2/FacilityBookings/WizardSteps/SetFacilityBookingDetailsWizardStep/Next"
            details_payload = {
                "UserId": self.user_id,
                "ZoneId": zone_id,
                "StartTime": start_time.strftime('%Y-%m-%dT%H:%M:%S'),
                "Duration": duration_minutes,
                "RequiredNumberOfSlots": None
            }

            details_response = self.session.post(details_url, json=details_payload)
            if details_response.status_code != 200:
                error_msg = details_response.text
                return {"success": False, "error": f"Failed to set booking details: {error_msg}"}

            # Extract rule ID from response
            details_data = details_response.json()
            if 'Data' not in details_data or 'RuleId' not in details_data['Data']:
                return {"success": False, "error": "No booking rule found"}

            rule_id = details_data['Data']['RuleId']

            # Small delay before confirmation
            time.sleep(0.5)

            # Step 3: Confirm booking with rule
            confirm_url = f"{self.base_url}/ClientPortal2/FacilityBookings/WizardSteps/ChooseBookingRuleStep/Next"
            confirm_payload = {
                "ruleId": rule_id,
                "OtherCalendarEventBookedAtRequestedTime": False,
                "HasUserRequiredProducts": False,
                "ShouldBuyRequiredProductOnDebit": True
            }

            confirm_response = self.session.post(confirm_url, json=confirm_payload)
            if confirm_response.status_code != 200:
                return {"success": False, "error": f"Failed to confirm booking: {confirm_response.status_code}"}

            # Check if booking was successful
            confirm_data = confirm_response.json()
            if 'Data' in confirm_data and 'FacilityBooking' in confirm_data['Data']:
                booking = confirm_data['Data']['FacilityBooking']
                return {
                    "success": True,
                    "start_time": booking.get('StartDate'),
                    "duration": booking.get('Duration'),
                    "user": booking.get('User', {}).get('FirstName', '') + ' ' + booking.get('User', {}).get('LastName', ''),
                    "message": "Booking confirmed! Check your email for payment instructions."
                }
            else:
                return {"success": False, "error": "Booking confirmation data missing"}

        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_my_bookings(self) -> List[Dict[str, Any]]:
        """
        Get user's current bookings

        Returns:
            List of user's bookings
        """
        try:
            bookings_url = f"{self.base_url}/Api/FacilityBooking/MyBookings"

            params = {
                "clubId": self.club_id,
                "userId": self.user_id
            }

            response = self.session.get(bookings_url, params=params)

            if response.status_code == 200:
                return response.json()
            else:
                return []

        except Exception as e:
            print(f"Error fetching bookings: {e}")
            return []

    def cancel_booking(self, booking_id: str) -> bool:
        """
        Cancel a booking

        Args:
            booking_id: ID of the booking to cancel

        Returns:
            True if cancellation successful, False otherwise
        """
        try:
            cancel_url = f"{self.base_url}/Api/FacilityBooking/Cancel"

            payload = {
                "bookingId": booking_id,
                "clubId": self.club_id
            }

            response = self.session.post(cancel_url, json=payload)

            return response.status_code in [200, 204]

        except Exception as e:
            print(f"Cancellation error: {e}")
            return False

    def logout(self) -> None:
        """Logout and clear session"""
        try:
            logout_url = f"{self.base_url}/Api/Users/Logout"
            self.session.post(logout_url)
        except:
            pass
        finally:
            self.access_token = None
            self.user_id = None
            self.session.headers.pop('Authorization', None)
