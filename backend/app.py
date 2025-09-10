from flask import Flask, redirect, url_for
from flask_login import LoginManager
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from auth import User
from csv_handler import get_user_by_id

# Initialize extensions
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    
    @login_manager.user_loader
    def load_user(user_id):
        user_data = get_user_by_id(user_id)
        if user_data:
            return User(
                id=user_data['id'],
                username=user_data['username'],
                email=user_data['email'],
                password_hash=user_data['password_hash']
            )
        return None
    
    # Configuration
    app.config['SECRET_KEY'] = 'your-secret-key-change-this-in-production'
    
    # Initialize extensions with app
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    
    @app.route('/')
    def home():
        return redirect(url_for('auth.login'))
    
    # Register blueprints
    from auth import auth_bp
    from reminders import reminders_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(reminders_bp)
    
    # Initialize scheduler for email notifications
    scheduler = BackgroundScheduler()
    
    # Import and setup email job
    from email_service import check_and_send_reminders
    scheduler.add_job(
        func=check_and_send_reminders,
        trigger='interval',
        minutes=1,  # Check every minute
        args=[app]  # Pass app context
    )
    scheduler.start()
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
