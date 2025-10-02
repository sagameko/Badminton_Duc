"""
Badminton Court Booking Application
"""
import streamlit as st
from datetime import datetime, timedelta
from auth import UserAuth
from storage import SecureStorage
from perfectgym_client import PerfectGymClient
from ai_chat_helper import AIChatHelper


# Initialize services
user_auth = UserAuth()
storage = SecureStorage()


def init_session_state():
    """Initialize session state variables"""
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'username' not in st.session_state:
        st.session_state.username = None
    if 'page' not in st.session_state:
        st.session_state.page = 'login'
    if 'perfectgym_client' not in st.session_state:
        st.session_state.perfectgym_client = None


def login_page():
    """Display login/register page"""
    st.title("🏸 Badminton Court Booking")

    tab1, tab2 = st.tabs(["Login", "Register"])

    with tab1:
        st.subheader("Login to your account")
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")

        if st.button("Login", type="primary"):
            if user_auth.authenticate(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.page = 'main'
                st.rerun()
            else:
                st.error("Invalid username or password")

    with tab2:
        st.subheader("Create a new account")
        new_username = st.text_input("Username", key="register_username")
        new_password = st.text_input("Password", type="password", key="register_password")
        confirm_password = st.text_input("Confirm Password", type="password", key="confirm_password")

        if st.button("Register", type="primary"):
            if not new_username or not new_password:
                st.error("Please fill in all fields")
            elif new_password != confirm_password:
                st.error("Passwords do not match")
            elif user_auth.register_user(new_username, new_password):
                st.success("Account created successfully! Please login.")
            else:
                st.error("Username already exists")


def setup_credentials_page():
    """Setup PerfectGym credentials"""
    st.subheader("⚙️ Setup PerfectGym Credentials")

    st.info("Enter your credentials for the badminton booking website")

    email = st.text_input("Email", key="perfectgym_email")
    password = st.text_input("Password", type="password", key="perfectgym_password")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Save & Test Credentials", type="primary"):
            if not email or not password:
                st.error("Please enter both email and password")
            else:
                # Test the credentials
                with st.spinner("Testing credentials..."):
                    client = PerfectGymClient()
                    if client.login(email, password):
                        # Save credentials
                        storage.save_credentials(st.session_state.username, email, password)
                        st.success("✅ Credentials saved successfully!")
                        st.session_state.page = 'main'
                        st.rerun()
                    else:
                        st.error("❌ Failed to authenticate with PerfectGym. Please check your credentials.")

    with col2:
        if st.button("Skip for now"):
            st.session_state.page = 'main'
            st.rerun()


def main_page():
    """Main application page"""
    st.title("🏸 Badminton Court Booking")

    # Sidebar
    with st.sidebar:
        st.write(f"👤 Logged in as: **{st.session_state.username}**")
        st.divider()

        # Check if user has PerfectGym credentials
        has_creds = storage.has_credentials(st.session_state.username)

        if has_creds:
            st.success("✅ PerfectGym connected")
        else:
            st.warning("⚠️ PerfectGym not connected")

        st.divider()

        # Navigation
        page_options = ["💬 Chat", "📅 View Schedule", "📋 My Bookings", "⚙️ Settings"]
        selected_page = st.radio("Navigation", page_options)

        st.divider()

        if st.button("Logout", type="secondary"):
            st.session_state.logged_in = False
            st.session_state.username = None
            st.session_state.perfectgym_client = None
            st.session_state.page = 'login'
            st.rerun()

    # Check credentials before showing main content
    if not has_creds:
        st.warning("⚠️ Please setup your PerfectGym credentials first")
        if st.button("Setup Credentials Now"):
            st.session_state.page = 'setup_credentials'
            st.rerun()
        return

    # Main content based on navigation
    if selected_page == "💬 Chat":
        chat_page()
    elif selected_page == "📅 View Schedule":
        view_schedule_page()
    elif selected_page == "📋 My Bookings":
        my_bookings_page()
    elif selected_page == "⚙️ Settings":
        settings_page()


def chat_page():
    """Interactive chat interface for booking courts"""
    st.header("💬 Chat with Booking Assistant")

    # Clear chat button
    col1, col2 = st.columns([4, 1])
    with col2:
        if st.button("🔄 Clear Chat"):
            st.session_state.chat_messages = [{
                "role": "assistant",
                "content": "Hi! I'm your badminton booking assistant. I can help you:\n\n"
                          "✅ Check court availability\n"
                          "✅ Find slots for specific days/times\n"
                          "✅ Get booking links\n\n"
                          "Try asking:\n"
                          "- 'What's available tomorrow?'\n"
                          "- 'Show me courts on Friday'\n"
                          "- 'I want to book at 6pm Monday'"
            }]
            st.rerun()

    # Initialize chat history
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = [
            {
                "role": "assistant",
                "content": "Hi! I'm your badminton booking assistant. I can help you:\n\n"
                          "✅ Check court availability\n"
                          "✅ Find slots for specific days/times\n"
                          "✅ Get booking links\n\n"
                          "Try asking:\n"
                          "- 'What's available tomorrow?'\n"
                          "- 'Show me courts on Friday'\n"
                          "- 'I want to book at 6pm Monday'"
            }
        ]

    # Display chat messages
    for message in st.session_state.chat_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("Ask about court availability..."):
        # Add user message to chat
        st.session_state.chat_messages.append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.markdown(prompt)

        # Process the message
        with st.chat_message("assistant"):
            with st.spinner("🤔 Processing your request..."):
                response = process_chat_message(prompt)
                st.markdown(response)

        # Add assistant response to chat
        st.session_state.chat_messages.append({"role": "assistant", "content": response})


def process_chat_message(message: str) -> str:
    """Process user message and return response using AI"""
    ai_helper = AIChatHelper()

    # Get chat history for context
    chat_history = st.session_state.get('chat_messages', [])

    # Use AI to parse the query with conversation context
    parsed = ai_helper.parse_query(message, chat_history)
    intent = parsed["intent"]
    date_str = parsed["date"]
    time_str = parsed["time"]
    friendly_response = parsed.get("friendly_response", "")

    # Handle greetings
    if intent == "greeting":
        return friendly_response or "Hello! 👋 How can I help you with badminton court bookings today?"

    # Handle help
    if intent == "help":
        return ("I can help you find and book badminton courts!\n\n"
                "**Try asking:**\n"
                "- 'What's available on Friday?'\n"
                "- 'Show me courts tomorrow at 6pm'\n"
                "- 'I want to book on Monday morning'\n"
                "- 'Check availability for next Tuesday'")

    # Handle availability/booking requests
    if intent in ["check_availability", "book"]:
        # Check if date was parsed
        if not date_str:
            return ("I couldn't determine which date you're asking about. Could you specify?\n\n"
                    "Examples: 'tomorrow', 'Friday', 'Monday', 'October 7th'")

        # Convert date string to datetime
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d')
        except:
            return "I had trouble parsing that date. Please try again!"

        # Get credentials and login
        creds = storage.get_credentials(st.session_state.username)
        client = PerfectGymClient()

        if not client.login(creds['email'], creds['password']):
            return "❌ Failed to connect to PerfectGym. Please check your credentials in Settings."

        # Fetch schedule
        schedule = client.get_schedule(days=14)

        if not schedule:
            return f"No available slots found around {date.strftime('%A, %B %d')}."

        # Filter slots for the requested date
        matching_slots = [
            slot for slot in schedule
            if slot['start_time'].startswith(date_str)
        ]

        # Filter by time if specified
        if time_str:
            # Match HH:MM format in the start_time
            matching_slots = [
                slot for slot in matching_slots
                if time_str in slot['start_time']
            ]

        if not matching_slots:
            if time_str:
                return f"No slots available on {date.strftime('%A, %B %d')} at {time_str}. Try a different time!"
            else:
                return f"No slots available on {date.strftime('%A, %B %d')}. Try another day!"

        # Format response with friendly AI message
        formatted_slots = ai_helper.format_slots_for_chat(matching_slots, max_slots=8)

        # Create booking link for first slot
        first_slot = matching_slots[0]
        slot_dt = datetime.fromisoformat(first_slot['start_time'])
        booking_url = client.get_booking_url(slot_dt)

        response = f"{friendly_response}\n\n" if friendly_response else ""
        response += f"**Available on {date.strftime('%A, %B %d')}:**\n\n{formatted_slots}\n\n"

        if intent == "book":
            response += f"👉 [Click here to book]({booking_url})"
        else:
            response += f"💡 Want to book? [Click here]({booking_url})"

        return response

    # Unknown intent
    return (friendly_response or
            "I'm not sure what you're asking. Try:\n"
            "- 'What's available on Friday?'\n"
            "- 'Show me courts for tomorrow'\n"
            "- 'I want to book on Monday'")


def view_schedule_page():
    """View and book court schedules"""
    st.header("📅 Court Schedule")

    st.info("💡 **How to book:** Click 'Book' → Find your time on the calendar → Click 'Book now' → See pricing and complete payment")

    # Date selector
    col1, col2 = st.columns([2, 1])
    with col1:
        selected_date = st.date_input(
            "Select Date",
            value=datetime.now(),
            min_value=datetime.now().date()
        )
    with col2:
        days_to_show = st.selectbox("Days to show", [1, 3, 7, 14], index=2)

    # Fetch schedule
    if st.button("🔍 Fetch Schedule", type="primary"):
        with st.spinner("Fetching available courts..."):
            # Get credentials
            creds = storage.get_credentials(st.session_state.username)

            # Login to PerfectGym
            client = PerfectGymClient()
            if client.login(creds['email'], creds['password']):
                st.session_state.perfectgym_client = client

                # Fetch schedule
                schedule = client.get_schedule(days=days_to_show)

                if schedule:
                    st.success(f"✅ Found {len(schedule)} available slots")

                    # Group by date
                    from collections import defaultdict
                    by_date = defaultdict(list)

                    for slot in schedule:
                        start_dt = datetime.fromisoformat(slot['start_time'])
                        date_key = start_dt.strftime('%A, %B %d, %Y')
                        by_date[date_key].append(slot)

                    # Display by date
                    for date_str in sorted(by_date.keys(), key=lambda x: datetime.strptime(x, '%A, %B %d, %Y')):
                        st.subheader(f"📆 {date_str}")

                        slots = by_date[date_str]

                        # Show first 10 slots per day, with option to show more
                        display_count = 10
                        if f"show_more_{date_str}" in st.session_state:
                            display_count = len(slots)

                        for slot in slots[:display_count]:
                            start_dt = datetime.fromisoformat(slot['start_time'])
                            end_dt = datetime.fromisoformat(slot['end_time'])

                            col1, col2, col3 = st.columns([3, 2, 1])

                            with col1:
                                st.write(f"⏰ **{start_dt.strftime('%I:%M %p')}** - {end_dt.strftime('%I:%M %p')}")

                            with col2:
                                st.write(f"⏱️ Duration: {slot['duration']}")

                            with col3:
                                booking_url = client.get_booking_url(start_dt)
                                st.link_button("📱 Book", booking_url, use_container_width=True)

                            st.divider()

                        # Show more button
                        if len(slots) > 10 and f"show_more_{date_str}" not in st.session_state:
                            if st.button(f"Show {len(slots) - 10} more slots", key=f"btn_more_{date_str}"):
                                st.session_state[f"show_more_{date_str}"] = True
                                st.rerun()

                else:
                    st.info("No available slots found for the selected date range")
            else:
                st.error("❌ Failed to connect to PerfectGym. Please check your credentials in Settings.")


def my_bookings_page():
    """View user's current bookings"""
    st.header("📋 My Bookings")

    st.info("💡 To view and manage your bookings, please visit the PerfectGym website.")

    # Direct link to bookings page
    bookings_url = "https://statesportcentres.perfectgym.com.au/ClientPortal2/#/MyBookings"

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.link_button("🌐 Open My Bookings in Browser", bookings_url, use_container_width=True, type="primary")

    st.divider()

    st.subheader("📧 Email Confirmation")
    st.write("After booking a court, you'll receive:")
    st.write("✅ Booking confirmation email")
    st.write("💳 Payment instructions")
    st.write("📅 Calendar invite (if applicable)")

    st.divider()

    st.subheader("📱 Quick Links")
    col1, col2 = st.columns(2)

    with col1:
        st.link_button("🏠 PerfectGym Home", "https://statesportcentres.perfectgym.com.au/ClientPortal2/", use_container_width=True)

    with col2:
        st.link_button("📊 My Activity", "https://statesportcentres.perfectgym.com.au/ClientPortal2/#/Activity", use_container_width=True)


def settings_page():
    """Settings page"""
    st.header("⚙️ Settings")

    st.subheader("PerfectGym Credentials")

    creds = storage.get_credentials(st.session_state.username)

    if creds:
        st.info(f"Current email: {creds['email']}")

        if st.button("Update Credentials"):
            st.session_state.page = 'setup_credentials'
            st.rerun()

        if st.button("Remove Credentials", type="secondary"):
            storage.delete_credentials(st.session_state.username)
            st.success("Credentials removed")
            st.rerun()
    else:
        st.warning("No credentials saved")
        if st.button("Setup Credentials"):
            st.session_state.page = 'setup_credentials'
            st.rerun()

    st.divider()

    st.subheader("Account Settings")

    with st.expander("Change Password"):
        old_password = st.text_input("Current Password", type="password")
        new_password = st.text_input("New Password", type="password")
        confirm_new = st.text_input("Confirm New Password", type="password")

        if st.button("Change Password"):
            if new_password != confirm_new:
                st.error("New passwords do not match")
            elif user_auth.change_password(st.session_state.username, old_password, new_password):
                st.success("Password changed successfully")
            else:
                st.error("Current password is incorrect")


def main():
    """Main application entry point"""
    st.set_page_config(
        page_title="Badminton Court Booking",
        page_icon="🏸",
        layout="wide"
    )

    init_session_state()

    # Route to appropriate page
    if not st.session_state.logged_in:
        login_page()
    elif st.session_state.page == 'setup_credentials':
        setup_credentials_page()
    else:
        main_page()


if __name__ == "__main__":
    main()
