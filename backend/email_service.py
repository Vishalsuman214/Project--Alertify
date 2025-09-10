import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from csv_handler import get_all_reminders, mark_reminder_completed, get_user_by_id

# Email configuration (should be moved to environment variables in production)
# No default credentials, user must set their own
DEFAULT_SENDER_EMAIL = None
DEFAULT_APP_PASSWORD = None

def send_reminder_email(receiver_email, reminder_title, reminder_description, reminder_time, user_id=None):
    """Send a reminder email to the specified recipient"""
    try:
        # Get user-specific credentials, no defaults
        if user_id:
            user = get_user_by_id(user_id)
            sender_email = user.get('email') if user else None
            app_password = user.get('app_password') if user else None
        else:
            sender_email = None
            app_password = None

        # Check if credentials are set
        if not sender_email or not app_password:
            print(f"❌ Email credentials not set for user {user_id}. Please set email credentials in settings.")
            return False

        # Create email
        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = receiver_email
        msg["Subject"] = f"Reminder: {reminder_title}"

        body = f"""
        Hello!

        This is a reminder for: {reminder_title}

        Description: {reminder_description or 'No description provided'}

        Scheduled Time: {reminder_time.strftime('%Y-%m-%d %H:%M')}

        ---
        This is an automated reminder from the Reminder App.
        """

        msg.attach(MIMEText(body, "plain"))

        # Connect to Gmail SMTP server
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, app_password)

        # Send email
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()

        print(f"✅ Email sent successfully to {receiver_email}")
        return True

    except Exception as e:
        print(f"❌ Error sending email to {receiver_email}: {e}")
        return False

def check_and_send_reminders(app):
    """Check for reminders that are due and send emails"""
    with app.app_context():
        current_time = datetime.now()
        
        # Get all reminders
        all_reminders = get_all_reminders()
        
        for reminder in all_reminders:
            # Skip completed reminders
            if reminder['is_completed'] == 'True':
                continue
                
            # Parse reminder time
            try:
                reminder_time = datetime.strptime(reminder['reminder_time'], '%Y-%m-%d %H:%M:%S')
            except ValueError:
                continue
                
            # Check if reminder is due
            if reminder_time <= current_time:
                user = get_user_by_id(reminder['user_id'])
                if user:
                    # Check if user has set email credentials
                    if not user.get('email') or not user.get('app_password'):
                        print(f"⚠️  Skipping reminder '{reminder['title']}' - user {reminder['user_id']} has not set email credentials")
                        continue

                    # Use custom recipient email if provided, otherwise use user's email
                    recipient_email = reminder.get('recipient_email', '') or user['email']

                    # Send email
                    success = send_reminder_email(
                        recipient_email,
                        reminder['title'],
                        reminder['description'],
                        reminder_time,
                        reminder['user_id']
                    )

                    if success:
                        # Mark reminder as completed
                        mark_reminder_completed(reminder['id'])
                        print(f"✅ Reminder '{reminder['title']}' sent to {recipient_email} and marked as completed")
                    else:
                        print(f"❌ Failed to send reminder '{reminder['title']}' to {recipient_email}")
