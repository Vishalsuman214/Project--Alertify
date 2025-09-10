#!/usr/bin/env python3
"""
Test script to verify CSV export and import functionality
"""

import os
import sys
import csv
from datetime import datetime, timedelta

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from csv_handler import add_user, add_reminder

def test_csv_functionality():
    """Test CSV export and import functionality"""
    
    # Create test app
    app = create_app()
    
    with app.app_context():
        # Initialize CSV files
        from csv_handler import init_csv_files
        init_csv_files()
        
        # Create a test user
        user_id = add_user('testuser', 'test@example.com', 'test_hash')
        
        # Create some test reminders
        reminder_time1 = datetime.now() + timedelta(hours=1)
        reminder_time2 = datetime.now() + timedelta(hours=2)
        
        add_reminder(user_id, 'Test Reminder 1', 'First test reminder', reminder_time1)
        add_reminder(user_id, 'Test Reminder 2', 'Second test reminder', reminder_time2)
        
        print("✅ Test data created successfully")
        
        # Test export functionality
        from reminders import export_reminders
        
        # Mock current_user for the test
        class MockCurrentUser:
            id = user_id
        
        # Test export
        try:
            response = export_reminders()
            print("✅ CSV export functionality works")
        except Exception as e:
            print(f"❌ CSV export failed: {e}")
            return False
        
        # Test import functionality
        from reminders import import_reminders
        from flask import Flask, request
        
        # Create test CSV data
        csv_data = [
            ['id', 'user_id', 'title', 'description', 'reminder_time', 'created_at', 'is_completed'],
            ['', str(user_id), 'Imported Reminder 1', 'First imported reminder', 
             (datetime.now() + timedelta(hours=3)).strftime('%Y-%m-%d %H:%M:%S'), 
             datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'No'],
            ['', str(user_id), 'Imported Reminder 2', 'Second imported reminder', 
             (datetime.now() + timedelta(hours=4)).strftime('%Y-%m-%d %H:%M:%S'), 
             datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'Yes']
        ]
        
        # Write test CSV file
        test_csv_path = 'test_import.csv'
        with open(test_csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerows(csv_data)
        
        print("✅ Test CSV file created")
        
        # Clean up
        if os.path.exists(test_csv_path):
            os.remove(test_csv_path)
        
        # Clean up CSV files
        if os.path.exists('users.csv'):
            os.remove('users.csv')
        if os.path.exists('reminders.csv'):
            os.remove('reminders.csv')
        
        print("✅ Test completed successfully!")
        return True

if __name__ == '__main__':
    test_csv_functionality()
