#!/usr/bin/env python3
"""
Test script to verify CSV handler functionality
"""
import os
from csv_handler import init_csv_files, add_user, get_user_by_email, add_reminder, get_reminders_by_user_id
from datetime import datetime, timedelta

def test_csv_handler():
    """Test CSV handler functionality"""
    print("Testing CSV Handler...")
    
    # Clean up any existing CSV files
    if os.path.exists('users.csv'):
        os.remove('users.csv')
    if os.path.exists('reminders.csv'):
        os.remove('reminders.csv')
    
    # Initialize CSV files
    init_csv_files()
    
    # Test user creation
    print("1. Testing user creation...")
    user_id = add_user('testuser', 'test@example.com', 'test_hash')
    print(f"   Created user with ID: {user_id}")
    
    # Test user retrieval
    print("2. Testing user retrieval...")
    user = get_user_by_email('test@example.com')
    if user:
        print(f"   Found user: {user['username']} ({user['email']})")
    else:
        print("   User not found!")
        return False
    
    # Test reminder creation
    print("3. Testing reminder creation...")
    reminder_time = datetime.now() + timedelta(hours=1)
    reminder_id = add_reminder(user_id, 'Test Reminder', 'This is a test reminder', reminder_time)
    print(f"   Created reminder with ID: {reminder_id}")
    
    # Test reminder retrieval
    print("4. Testing reminder retrieval...")
    reminders = get_reminders_by_user_id(user_id)
    if reminders:
        print(f"   Found {len(reminders)} reminders for user")
        for reminder in reminders:
            print(f"   - {reminder['title']} at {reminder['reminder_time']}")
    else:
        print("   No reminders found!")
        return False
    
    print("✅ All CSV handler tests passed!")
    return True

if __name__ == '__main__':
    test_csv_handler()
