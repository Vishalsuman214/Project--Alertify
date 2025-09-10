# TODO: Add Email Credentials Management

## Tasks
- [x] Update users.csv to include email and app_password fields
- [x] Update csv_handler.py to add functions for getting/updating user email credentials
- [x] Create email_credentials.html template for the form
- [x] Add new route in auth.py for handling email credentials GET/POST
- [x] Add button on dashboard.html to access email credentials page
- [x] Modify email_service.py to use dynamic user credentials instead of hardcoded ones
- [x] Remove default email credentials - users must set their own
- [x] Reset CSV files to remove hardcoded email data
- [x] Add proper error handling for missing credentials
- [x] Test the email credentials update flow
- [x] Verify email sending still works with user-specific credentials
