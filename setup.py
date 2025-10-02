"""
Setup script for the Badminton Booking Application
Run this to automatically setup the environment
"""
import os
import sys
from pathlib import Path
from cryptography.fernet import Fernet


def create_env_file():
    """Create .env file with encryption key and Gemini API key"""
    env_file = Path(".env")

    if env_file.exists():
        print("[OK] .env file already exists")
        # Check if GEMINI_API_KEY exists
        with open(env_file, 'r') as f:
            content = f.read()
            if 'GEMINI_API_KEY' not in content:
                print("[INFO] GEMINI_API_KEY not found in .env")
                add_gemini_key = input("Would you like to add Gemini API key for AI chat? (y/n): ").lower()
                if add_gemini_key == 'y':
                    api_key = input("Enter your Gemini API key (or press Enter to skip): ").strip()
                    if api_key:
                        with open(env_file, 'a') as f:
                            f.write(f"\nGEMINI_API_KEY={api_key}\n")
                        print("[OK] Gemini API key added to .env")
                    else:
                        print("[SKIP] You can add GEMINI_API_KEY to .env later for AI features")
        return

    # Generate encryption key
    encryption_key = Fernet.generate_key().decode()

    print("\n[SETUP] Gemini API Configuration")
    print("=" * 50)
    print("For AI-powered chat, you need a Google Gemini API key.")
    print("Get your free key at: https://makersuite.google.com/app/apikey")
    print("=" * 50)

    api_key = input("\nEnter your Gemini API key (or press Enter to skip): ").strip()

    # Create .env file
    with open(env_file, 'w') as f:
        f.write(f"ENCRYPTION_KEY={encryption_key}\n")
        if api_key:
            f.write(f"GEMINI_API_KEY={api_key}\n")

    print("[OK] Created .env file with encryption key")
    if api_key:
        print("[OK] Gemini API key configured - AI chat enabled!")
    else:
        print("[INFO] Gemini API key skipped - AI chat will be disabled")
        print("      You can add GEMINI_API_KEY to .env later")


def check_dependencies():
    """Check if all dependencies are installed"""
    print("Checking dependencies...")

    required = [
        'streamlit',
        'requests',
        'cryptography',
        'bcrypt',
        'dotenv'
    ]

    missing = []

    for package in required:
        try:
            __import__(package)
        except ImportError:
            missing.append(package)

    if missing:
        print(f"[ERROR] Missing dependencies: {', '.join(missing)}")
        print("        Install with: pip install -r requirements.txt")
        return False
    else:
        print("[OK] All dependencies installed")
        return True


def main():
    """Main setup function"""
    print("=" * 50)
    print("Badminton Booking App - Setup")
    print("=" * 50)
    print()

    # Check dependencies
    if not check_dependencies():
        print("\nPlease install dependencies first:")
        print("  pip install -r requirements.txt")
        sys.exit(1)

    # Create .env file
    create_env_file()

    print()
    print("=" * 50)
    print("Setup complete!")
    print("=" * 50)
    print()
    print("Next steps:")
    print("  1. Run the app: streamlit run app.py")
    print("  2. Register a new account")
    print("  3. Setup your PerfectGym credentials")
    print("  4. Start viewing and booking courts!")
    print()


if __name__ == "__main__":
    main()
