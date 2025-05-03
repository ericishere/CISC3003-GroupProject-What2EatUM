from app import app, db
from models import User, UserRole
from werkzeug.security import generate_password_hash
import secrets
from datetime import datetime

# List of users to add
users_to_add = [
    {"username": "Popping", "email": "1@lric.xyz", "password": "1@lric.xyz"},
    {"username": "Eric", "email": "2@lric.xyz", "password": "2@lric.xyz"},
    {"username": "Sam", "email": "3@lric.xyz", "password": "3@lric.xyz"},
    {"username": "Angus", "email": "4@lric.xyz", "password": "4@lric.xyz"}
]

# Add users to database with email verification
with app.app_context():
    for user_data in users_to_add:
        # Check if user already exists
        existing_user = User.query.filter_by(email=user_data["email"]).first()
        if existing_user:
            print(f"User {user_data['email']} already exists. Skipping.")
            continue
        
        # Create new user with verification already set to True
        new_user = User(
            user_id=secrets.token_hex(16),
            username=user_data["username"],
            email=user_data["email"],
            password=generate_password_hash(user_data["password"]),
            role=UserRole.GENERAL_USER,
            created_at=datetime.utcnow(),
            is_email_verified=True  # Bypass email verification
        )
        
        db.session.add(new_user)
        print(f"Added user: {user_data['username']} ({user_data['email']})")
    
    # Commit all changes
    db.session.commit()
    print("All users added successfully!")