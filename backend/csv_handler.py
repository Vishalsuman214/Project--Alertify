import csv
import os
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

# File paths - use /tmp for Vercel deployment
TMP_DIR = '/tmp'
USERS_CSV = os.path.join(TMP_DIR, 'users.csv')
REMINDERS_CSV = os.path.join(TMP_DIR, 'reminders.csv')

# Ensure CSV files exist with headers
def init_csv_files():
    # Users CSV
    if not os.path.exists(USERS_CSV):
        with open(USERS_CSV, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['id', 'username', 'email', 'password_hash', 'app_password'])
    
    # Reminders CSV
    if not os.path.exists(REMINDERS_CSV):
        with open(REMINDERS_CSV, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['id', 'user_id', 'title', 'description', 'reminder_time', 'created_at', 'is_completed', 'recipient_email'])

# User management functions
def get_next_user_id():
    if not os.path.exists(USERS_CSV):
        return 1
    
    with open(USERS_CSV, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        users = list(reader)
        
    if not users:
        return 1
    return max(int(user['id']) for user in users) + 1

def add_user(username, email, password_hash, app_password=''):
    init_csv_files()
    user_id = get_next_user_id()

    with open(USERS_CSV, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([user_id, username, email, password_hash, app_password])

    return user_id

def get_user_by_email(email):
    if not os.path.exists(USERS_CSV):
        return None
    
    with open(USERS_CSV, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for user in reader:
            if user['email'] == email:
                return user
    return None

def get_user_by_id(user_id):
    if not os.path.exists(USERS_CSV):
        return None

    with open(USERS_CSV, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for user in reader:
            if user['id'] == str(user_id):
                return user
    return None

def update_user_email_credentials(user_id, new_email, new_app_password):
    if not os.path.exists(USERS_CSV):
        return False

    users = []
    updated = False

    with open(USERS_CSV, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        for user in reader:
            if user['id'] == str(user_id):
                user['email'] = new_email
                user['app_password'] = new_app_password
                updated = True
            users.append(user)

    if updated:
        with open(USERS_CSV, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(users)

    return updated



# Reminder management functions
def get_next_reminder_id():
    if not os.path.exists(REMINDERS_CSV):
        return 1
    
    with open(REMINDERS_CSV, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        reminders = list(reader)
        
    if not reminders:
        return 1
    return max(int(reminder['id']) for reminder in reminders) + 1

def add_reminder(user_id, title, description, reminder_time, recipient_email=None):
    init_csv_files()
    reminder_id = get_next_reminder_id()
    created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    with open(REMINDERS_CSV, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            reminder_id,
            user_id,
            title,
            description or '',
            reminder_time.strftime('%Y-%m-%d %H:%M:%S'),
            created_at,
            'False',
            recipient_email or ''
        ])
    
    return reminder_id

def get_reminders_by_user_id(user_id):
    if not os.path.exists(REMINDERS_CSV):
        return []
    
    reminders = []
    with open(REMINDERS_CSV, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for reminder in reader:
            if reminder['user_id'] == str(user_id):
                reminders.append(reminder)
    
    return reminders

def get_reminder_by_id(reminder_id):
    if not os.path.exists(REMINDERS_CSV):
        return None
    
    with open(REMINDERS_CSV, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for reminder in reader:
            if reminder['id'] == str(reminder_id):
                return reminder
    return None

def update_reminder(reminder_id, title, description, reminder_time, recipient_email=None):
    if not os.path.exists(REMINDERS_CSV):
        return False
    
    reminders = []
    updated = False
    
    with open(REMINDERS_CSV, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for reminder in reader:
            if reminder['id'] == str(reminder_id):
                reminder['title'] = title
                reminder['description'] = description or ''
                reminder['reminder_time'] = reminder_time.strftime('%Y-%m-%d %H:%M:%S')
                reminder['recipient_email'] = recipient_email or ''
                updated = True
            reminders.append(reminder)
    
    if updated:
        with open(REMINDERS_CSV, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['id', 'user_id', 'title', 'description', 'reminder_time', 'created_at', 'is_completed', 'recipient_email'])
            for reminder in reminders:
                writer.writerow([
                    reminder['id'],
                    reminder['user_id'],
                    reminder['title'],
                    reminder['description'],
                    reminder['reminder_time'],
                    reminder['created_at'],
                    reminder['is_completed'],
                    reminder.get('recipient_email', '') or ''
                ])
    
    return updated

def delete_reminder(reminder_id):
    if not os.path.exists(REMINDERS_CSV):
        return False
    
    reminders = []
    deleted = False
    
    with open(REMINDERS_CSV, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for reminder in reader:
            if reminder['id'] != str(reminder_id):
                reminders.append(reminder)
            else:
                deleted = True
    
    if deleted:
        with open(REMINDERS_CSV, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['id', 'user_id', 'title', 'description', 'reminder_time', 'created_at', 'is_completed', 'recipient_email'])
            for reminder in reminders:
                writer.writerow([
                    reminder['id'],
                    reminder['user_id'],
                    reminder['title'],
                    reminder['description'],
                    reminder['reminder_time'],
                    reminder['created_at'],
                    reminder['is_completed'],
                    reminder.get('recipient_email', '') or ''
                ])
    
    return deleted

def get_all_reminders():
    if not os.path.exists(REMINDERS_CSV):
        return []
    
    with open(REMINDERS_CSV, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)

def mark_reminder_completed(reminder_id):
    if not os.path.exists(REMINDERS_CSV):
        return False
    
    reminders = []
    updated = False
    
    with open(REMINDERS_CSV, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for reminder in reader:
            if reminder['id'] == str(reminder_id):
                reminder['is_completed'] = 'True'
                updated = True
            reminders.append(reminder)
    
    if updated:
        with open(REMINDERS_CSV, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['id', 'user_id', 'title', 'description', 'reminder_time', 'created_at', 'is_completed', 'recipient_email'])
            for reminder in reminders:
                writer.writerow([
                    reminder['id'],
                    reminder['user_id'],
                    reminder['title'],
                    reminder['description'],
                    reminder['reminder_time'],
                    reminder['created_at'],
                    reminder['is_completed'],
                    reminder.get('recipient_email', '') or ''
                ])
    
    return updated
