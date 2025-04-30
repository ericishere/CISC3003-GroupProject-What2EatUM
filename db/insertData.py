"""
What2Eat @UM Database - Sample Data Insertion Script
This script populates all tables with sample data for testing and development.
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, time, timedelta
import pymysql
import uuid
import os
import sys
import random
from sqlalchemy.orm import sessionmaker

# Import your models (adjust import path as needed)
try:
    # Try to import from your main application file
    from What2EatUM_db import app, db, User, UserRole, Restaurant, CuisineType, BusinessHour, RestaurantPhoto, Review
    from What2EatUM_db import ReviewPhoto, Reply, Promotion, RestaurantClaim, Notification, restaurant_followers
except ImportError:
    print("Could not import models from main application. Make sure the import path is correct.")
    sys.exit(1)

# Function to hash passwords
def hash_password(password):
    """Hash a password for secure storage"""
    import hashlib
    import os
    salt = os.urandom(32)
    key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    return salt.hex() + ':' + key.hex()

# -------------------------------------------------------------------------
# User Insertion
# -------------------------------------------------------------------------
def insert_sample_users(session):
    """Insert sample users into the database"""
    
    print("Inserting sample users...")
    sample_users = [
        # Administrator
        {
            'username': 'admin_supervisor',
            'email': 'supervisor@what2eat.um.edu',
            'password': 'secure_admin_pass',
            'role': UserRole.ADMIN
        },
        # Restaurant Managers
        {
            'username': 'canteen_manager',
            'email': 'canteen@um.edu.mo',
            'password': 'canteen_pass',
            'role': UserRole.RESTAURANT_MANAGER
        },
        {
            'username': 'cafe_manager',
            'email': 'cafe@um.edu.mo',
            'password': 'cafe_pass',
            'role': UserRole.RESTAURANT_MANAGER
        },
        {
            'username': 'restaurant_owner',
            'email': 'owner@restaurant.mo',
            'password': 'owner_pass',
            'role': UserRole.RESTAURANT_MANAGER
        },
        # General Users - Students
        {
            'username': 'student_john',
            'email': 'john@student.um.edu.mo',
            'password': 'john_pass',
            'role': UserRole.GENERAL_USER
        },
        {
            'username': 'student_alice',
            'email': 'alice@student.um.edu.mo',
            'password': 'alice_pass',
            'role': UserRole.GENERAL_USER
        },
        {
            'username': 'student_mei',
            'email': 'mei@student.um.edu.mo',
            'password': 'mei_pass',
            'role': UserRole.GENERAL_USER
        },
        {
            'username': 'student_wang',
            'email': 'wang@student.um.edu.mo',
            'password': 'wang_pass',
            'role': UserRole.GENERAL_USER
        }
    ]
    
    # Dictionary to store created users for later reference
    created_users = {}
    
    # Insert each user
    for user_data in sample_users:
        # Check if user already exists
        user_exists = session.query(User).filter(
            User.username == user_data['username']
        ).first()
        
        if not user_exists:
            # Generate a new UUID for the user
            user_id = str(uuid.uuid4())
            
            # Create new user
            user = User(
                user_id=user_id,
                username=user_data['username'],
                email=user_data['email'],
                password=hash_password(user_data['password']),
                role=user_data['role'],
                created_at=datetime.utcnow()
            )
            
            # Add to session
            session.add(user)
            created_users[user_data['username']] = user
            print(f"Created user: {user_data['username']} with role {user_data['role'].value}")
    
    # Commit changes
    session.commit()
    print(f"Successfully inserted {len(created_users)} users into the database.")
    
    return created_users

# -------------------------------------------------------------------------
# Restaurant Insertion
# -------------------------------------------------------------------------
def insert_sample_restaurants(session, user_dict):
    """Insert sample restaurants into the database"""
    
    print("Inserting sample restaurants...")
    sample_restaurants = [
        {
            'name': 'UM Student Canteen',
            'location': 'Main Campus',
            'address': 'N22, University of Macau, Avenida da Universidade, Taipa',
            'cuisine_type': CuisineType.CHINESE,
            'description': 'The main student canteen serving affordable Chinese dishes.',
            'is_verified': True,
            'manager_username': 'canteen_manager'  # Links to user
        },
        {
            'name': 'Faculty Coffee Shop',
            'location': 'Faculty of Business',
            'address': 'E22, University of Macau, Avenida da Universidade, Taipa',
            'cuisine_type': CuisineType.BEVERAGE,
            'description': 'Premium coffee shop serving specialty coffees and light snacks.',
            'is_verified': True,
            'manager_username': 'cafe_manager'  # Links to user
        },
        {
            'name': 'Asian Fusion Restaurant',
            'location': 'Central Teaching Building',
            'address': 'E4, University of Macau, Avenida da Universidade, Taipa',
            'cuisine_type': CuisineType.ASIAN,
            'description': 'Modern restaurant serving a fusion of Asian cuisines.',
            'is_verified': False,
            'manager_username': None  # No manager yet
        },
        {
            'name': 'Quick Bites',
            'location': 'Research Building',
            'address': 'N21, University of Macau, Avenida da Universidade, Taipa',
            'cuisine_type': CuisineType.FAST_FOOD,
            'description': 'Fast food outlet for quick meals between classes.',
            'is_verified': False,
            'manager_username': None  # No manager yet
        },
        {
            'name': 'Green Garden',
            'location': 'Library',
            'address': 'E2, University of Macau, Avenida da Universidade, Taipa',
            'cuisine_type': CuisineType.VEGETARIAN,
            'description': 'Healthy vegetarian options using fresh ingredients.',
            'is_verified': False,
            'manager_username': None  # No manager yet
        }
    ]
    
    # Dictionary to store created restaurants for later reference
    created_restaurants = {}
    
    # Insert each restaurant
    for restaurant_data in sample_restaurants:
        # Check if restaurant already exists
        restaurant_exists = session.query(Restaurant).filter(
            Restaurant.name == restaurant_data['name']
        ).first()
        
        if not restaurant_exists:
            # Get manager if specified
            manager_id = None
            if restaurant_data['manager_username'] and restaurant_data['manager_username'] in user_dict:
                manager_id = user_dict[restaurant_data['manager_username']].user_id
            
            # Create new restaurant
            restaurant = Restaurant(
                name=restaurant_data['name'],
                location=restaurant_data['location'],
                address=restaurant_data['address'],
                cuisine_type=restaurant_data['cuisine_type'],
                description=restaurant_data['description'],
                created_at=datetime.utcnow(),
                is_verified=restaurant_data['is_verified'],
                manager_id=manager_id
            )
            
            # Add to session
            session.add(restaurant)
            session.flush()  # Flush to get the ID
            created_restaurants[restaurant_data['name']] = restaurant
            print(f"Created restaurant: {restaurant_data['name']}")
    
    # Commit changes
    session.commit()
    print(f"Successfully inserted {len(created_restaurants)} restaurants into the database.")
    
    return created_restaurants

# -------------------------------------------------------------------------
# Business Hours Insertion
# -------------------------------------------------------------------------
def insert_business_hours(session, restaurant_dict):
    """Insert business hours for restaurants"""
    
    print("Inserting business hours...")
    count = 0
    
    for restaurant_name, restaurant in restaurant_dict.items():
        # Default hours (can be customized for each restaurant)
        if restaurant_name == "UM Student Canteen":
            # Canteen is open all week with longer hours
            for day in range(7):
                # Different hours for weekends
                if day >= 5:  # Saturday and Sunday
                    open_time_value = time(9, 0)  # 9:00 AM
                    close_time_value = time(20, 0)  # 8:00 PM
                else:
                    open_time_value = time(7, 0)  # 7:00 AM
                    close_time_value = time(22, 0)  # 10:00 PM
                
                hour = BusinessHour(
                    restaurant_id=restaurant.restaurant_id,
                    day_of_week=day,
                    open_time=open_time_value,
                    close_time=close_time_value
                )
                session.add(hour)
                count += 1
        elif restaurant_name == "Faculty Coffee Shop":
            # Coffee shop is closed on weekends
            for day in range(5):  # Monday to Friday
                hour = BusinessHour(
                    restaurant_id=restaurant.restaurant_id,
                    day_of_week=day,
                    open_time=time(8, 0),  # 8:00 AM
                    close_time=time(18, 0)  # 6:00 PM
                )
                session.add(hour)
                count += 1
        else:
            # Standard hours for other restaurants
            for day in range(7):
                # Closed on Sunday for some restaurants
                if day == 6 and random.choice([True, False]):
                    continue
                    
                hour = BusinessHour(
                    restaurant_id=restaurant.restaurant_id,
                    day_of_week=day,
                    open_time=time(10, 0),  # 10:00 AM
                    close_time=time(21, 0)  # 9:00 PM
                )
                session.add(hour)
                count += 1
    
    # Commit changes
    session.commit()
    print(f"Successfully inserted {count} business hours into the database.")

# -------------------------------------------------------------------------
# Restaurant Photos Insertion
# -------------------------------------------------------------------------
def insert_restaurant_photos(session, restaurant_dict, user_dict):
    """Insert sample restaurant photos"""
    
    print("Inserting restaurant photos...")
    count = 0
    
    # Get a list of general users for photo uploads
    general_users = [user for user in user_dict.values() 
                    if user.role == UserRole.GENERAL_USER]
    
    # Sample photo paths (in a real app, these would be actual file paths)
    sample_paths = [
        "photos/restaurant/exterior_{}.jpg",
        "photos/restaurant/interior_{}.jpg",
        "photos/restaurant/food_{}.jpg",
        "photos/restaurant/menu_{}.jpg"
    ]
    
    for restaurant in restaurant_dict.values():
        # Add 2-4 photos for each restaurant
        num_photos = random.randint(2, 4)
        for i in range(num_photos):
            # Randomly select a photo path and user
            path = sample_paths[i % len(sample_paths)].format(restaurant.restaurant_id)
            uploader = random.choice(general_users)
            
            # Create photo entry
            photo = RestaurantPhoto(
                restaurant_id=restaurant.restaurant_id,
                file_path=path,
                uploaded_by=uploader.user_id,
                is_approved=random.choice([True, False]),
                uploaded_at=datetime.utcnow() - timedelta(days=random.randint(1, 30))
            )
            
            session.add(photo)
            count += 1
    
    # Commit changes
    session.commit()
    print(f"Successfully inserted {count} restaurant photos into the database.")

# -------------------------------------------------------------------------
# Reviews Insertion
# -------------------------------------------------------------------------
def insert_sample_reviews(session, restaurant_dict, user_dict):
    """Insert sample reviews for restaurants"""
    
    print("Inserting sample reviews...")
    count = 0
    
    # Sample review texts
    sample_comments = [
        "Great food and service! Highly recommended.",
        "The food was average, but the staff were friendly.",
        "Good value for money. Will come back again.",
        "The ambiance was nice, but the food took too long to arrive.",
        "Excellent menu options for vegetarians.",
        "Delicious food, but a bit pricey for students.",
        "Perfect place for a quick lunch between classes.",
        "Clean environment and tasty food.",
        "Would recommend the daily special - it's always good.",
        "Friendly staff and reasonable prices."
    ]
    
    # Get general users for reviews
    general_users = [user for user in user_dict.values() 
                    if user.role == UserRole.GENERAL_USER]
    
    created_reviews = []
    
    for restaurant in restaurant_dict.values():
        # Add 2-5 reviews for each restaurant
        num_reviews = random.randint(2, 5)
        for _ in range(num_reviews):
            # Randomly select a user and comment
            reviewer = random.choice(general_users)
            comment = random.choice(sample_comments)
            rating = random.randint(1, 5)
            
            # Create review
            review = Review(
                restaurant_id=restaurant.restaurant_id,
                user_id=reviewer.user_id,
                rating=rating,
                comment=comment,
                created_at=datetime.utcnow() - timedelta(days=random.randint(1, 60))
            )
            
            session.add(review)
            session.flush()  # To get the review ID
            created_reviews.append(review)
            count += 1
    
    # Commit changes
    session.commit()
    print(f"Successfully inserted {count} reviews into the database.")
    
    return created_reviews

# -------------------------------------------------------------------------
# Review Photos Insertion
# -------------------------------------------------------------------------
def insert_review_photos(session, reviews):
    """Insert sample photos for reviews"""
    
    print("Inserting review photos...")
    count = 0
    
    # Sample photo paths
    sample_paths = [
        "photos/review/food_{}.jpg",
        "photos/review/plate_{}.jpg",
        "photos/review/dish_{}.jpg"
    ]
    
    for review in reviews:
        # 30% chance of having a photo
        if random.random() < 0.3:
            # Add 1-2 photos
            num_photos = random.randint(1, 2)
            for i in range(num_photos):
                path = sample_paths[random.randint(0, len(sample_paths)-1)].format(review.review_id)
                
                photo = ReviewPhoto(
                    review_id=review.review_id,
                    file_path=path,
                    uploaded_at=review.created_at + timedelta(minutes=random.randint(1, 10))
                )
                
                session.add(photo)
                count += 1
    
    # Commit changes
    session.commit()
    print(f"Successfully inserted {count} review photos into the database.")

# -------------------------------------------------------------------------
# Replies Insertion
# -------------------------------------------------------------------------
def insert_sample_replies(session, reviews, user_dict):
    """Insert sample replies to reviews"""
    
    print("Inserting sample replies...")
    count = 0
    
    # Sample reply texts
    manager_replies = [
        "Thank you for your feedback! We're glad you enjoyed your experience.",
        "We appreciate your review and will work on improving our service.",
        "Thank you for dining with us. We hope to see you again soon!",
        "We're sorry to hear about your experience. We'll address these issues immediately.",
        "Thanks for your suggestions. We're constantly working to improve."
    ]
    
    user_replies = [
        "I agree with this review! Had the same experience.",
        "I think the food is better than described here.",
        "Did you try their special dish? It's amazing!",
        "I visited again and the service has improved.",
        "I had a completely different experience. The food was great!"
    ]
    
    # Get restaurant managers and general users
    managers = [user for user in user_dict.values() 
               if user.role == UserRole.RESTAURANT_MANAGER]
    general_users = [user for user in user_dict.values() 
                    if user.role == UserRole.GENERAL_USER]
    
    for review in reviews:
        # 40% chance of having a manager reply
        if random.random() < 0.4 and managers:
            # Randomly select a manager and reply
            manager = random.choice(managers)
            reply_text = random.choice(manager_replies)
            
            reply = Reply(
                review_id=review.review_id,
                user_id=manager.user_id,
                content=reply_text,
                created_at=review.created_at + timedelta(days=random.randint(1, 5))
            )
            
            session.add(reply)
            count += 1
        
        # 20% chance of having a user reply
        if random.random() < 0.2 and general_users:
            # Randomly select a user (different from reviewer) and reply
            possible_repliers = [user for user in general_users if user.user_id != review.user_id]
            if possible_repliers:
                replier = random.choice(possible_repliers)
                reply_text = random.choice(user_replies)
                
                reply = Reply(
                    review_id=review.review_id,
                    user_id=replier.user_id,
                    content=reply_text,
                    created_at=review.created_at + timedelta(days=random.randint(1, 10))
                )
                
                session.add(reply)
                count += 1
    
    # Commit changes
    session.commit()
    print(f"Successfully inserted {count} replies into the database.")

# -------------------------------------------------------------------------
# Promotions Insertion
# -------------------------------------------------------------------------
def insert_sample_promotions(session, restaurant_dict, user_dict):
    """Insert sample promotions for restaurants"""
    
    print("Inserting sample promotions...")
    count = 0
    
    # Sample promotion data
    sample_promotions = [
        {
            'title': 'Student Discount Week',
            'description': 'Show your student ID to get 15% off on all menu items. Valid for this week only!',
            'days_active': 7,
            'image_path': 'promotions/student_discount.jpg'
        },
        {
            'title': 'Buy One Get One Free',
            'description': 'Buy any main dish and get a free drink! Limited time offer.',
            'days_active': 14,
            'image_path': 'promotions/bogo.jpg'
        },
        {
            'title': 'Happy Hour Special',
            'description': '30% off on all beverages between 3PM and 5PM. Come enjoy a refreshing break!',
            'days_active': 30,
            'image_path': 'promotions/happy_hour.jpg'
        },
        {
            'title': 'New Menu Launch',
            'description': 'We\'ve added 10 new items to our menu! Come try them all with a 10% discount this month.',
            'days_active': 30,
            'image_path': 'promotions/new_menu.jpg'
        },
        {
            'title': 'Exam Week Energizer',
            'description': 'Free coffee refills for students during exam week. Stay caffeinated!',
            'days_active': 10,
            'image_path': 'promotions/exam_week.jpg'
        }
    ]
    
    # Get verified restaurants and their managers
    verified_restaurants = {r.restaurant_id: r for r in restaurant_dict.values() if r.is_verified}
    managers = [user for user in user_dict.values() if user.role == UserRole.RESTAURANT_MANAGER]
    
    # For restaurants without managers, use admin
    admin = next((user for user in user_dict.values() if user.role == UserRole.ADMIN), None)
    
    for restaurant_id, restaurant in verified_restaurants.items():
        # Add 1-3 promotions for each verified restaurant
        num_promotions = random.randint(1, 3)
        for _ in range(num_promotions):
            # Randomly select promotion data
            promo_data = random.choice(sample_promotions)
            
            # Determine creator (manager if available, otherwise admin)
            if restaurant.manager_id:
                creator_id = restaurant.manager_id
            elif admin:
                creator_id = admin.user_id
            elif managers:
                creator_id = random.choice(managers).user_id
            else:
                continue  # Skip if no suitable creator found
            
            # Set random start and end dates
            start_date = datetime.utcnow() - timedelta(days=random.randint(0, 15))
            end_date = start_date + timedelta(days=promo_data['days_active'])
            
            promotion = Promotion(
                restaurant_id=restaurant_id,
                title=promo_data['title'],
                description=promo_data['description'],
                start_date=start_date,
                end_date=end_date,
                image_path=promo_data['image_path'],
                created_at=start_date - timedelta(days=random.randint(1, 5)),
                created_by=creator_id
            )
            
            session.add(promotion)
            count += 1
    
    # Commit changes
    session.commit()
    print(f"Successfully inserted {count} promotions into the database.")

# -------------------------------------------------------------------------
# Restaurant Claims Insertion
# -------------------------------------------------------------------------
def insert_sample_claims(session, restaurant_dict, user_dict):
    """Insert sample restaurant claims"""
    
    print("Inserting sample restaurant claims...")
    count = 0
    
    # Get unverified restaurants and restaurant manager users
    unverified_restaurants = [r for r in restaurant_dict.values() if not r.is_verified]
    manager_users = [user for user in user_dict.values() if user.role == UserRole.RESTAURANT_MANAGER]
    
    # Get an admin for processing claims
    admin = next((user for user in user_dict.values() if user.role == UserRole.ADMIN), None)
    
    # Create claims for some unverified restaurants
    for restaurant in unverified_restaurants:
        # 70% chance of having a claim
        if random.random() < 0.7 and manager_users:
            # Randomly select a manager
            manager = random.choice(manager_users)
            
            # Create claim with random status
            status = random.choice(['pending', 'approved', 'rejected'])
            submitted_at = datetime.utcnow() - timedelta(days=random.randint(5, 30))
            
            claim = RestaurantClaim(
                restaurant_id=restaurant.restaurant_id,
                user_id=manager.user_id,
                proof_document=f"documents/claims/proof_{restaurant.restaurant_id}_{manager.user_id}.pdf",
                status=status,
                submitted_at=submitted_at
            )
            
            # Add processing details if not pending
            if status != 'pending' and admin:
                claim.processed_at = submitted_at + timedelta(days=random.randint(1, 5))
                claim.processed_by = admin.user_id
                
                if status == 'approved':
                    claim.notes = "Documentation verified. Approved."
                else:
                    claim.notes = "Documentation insufficient. Please provide additional proof."
            
            session.add(claim)
            count += 1
    
    # Commit changes
    session.commit()
    print(f"Successfully inserted {count} restaurant claims into the database.")

# -------------------------------------------------------------------------
# Restaurant Followers Insertion
# -------------------------------------------------------------------------
def insert_restaurant_followers(session, restaurant_dict, user_dict):
    """Insert relationships between users and restaurants they follow"""
    
    print("Inserting restaurant followers...")
    count = 0
    
    # Get general users
    general_users = [user for user in user_dict.values() if user.role == UserRole.GENERAL_USER]
    
    for user in general_users:
        # Each user follows 1-3 restaurants
        num_follows = random.randint(1, min(3, len(restaurant_dict)))
        restaurants = random.sample(list(restaurant_dict.values()), num_follows)
        
        for restaurant in restaurants:
            # Check if already following
            already_following = session.query(restaurant_followers).filter(
                restaurant_followers.c.user_id == user.user_id,
                restaurant_followers.c.restaurant_id == restaurant.restaurant_id
            ).first()
            
            if not already_following:
                # Add to followers
                followed_at = datetime.utcnow() - timedelta(days=random.randint(1, 60))
                
                # Use direct SQL insert since this is an association table
                session.execute(restaurant_followers.insert().values(
                    user_id=user.user_id,
                    restaurant_id=restaurant.restaurant_id,
                    followed_at=followed_at
                ))
                
                count += 1
    
    # Commit changes
    session.commit()
    print(f"Successfully inserted {count} restaurant follower relationships into the database.")

# -------------------------------------------------------------------------
# Notifications Insertion
# -------------------------------------------------------------------------
def insert_sample_notifications(session, user_dict):
    """Insert sample notifications for users"""
    
    print("Inserting sample notifications...")
    count = 0
    
    # Get all promotions
    promotions = session.query(Promotion).all()
    
    for promotion in promotions:
        # Get the restaurant info
        restaurant = session.query(Restaurant).filter(
            Restaurant.restaurant_id == promotion.restaurant_id
        ).first()
        
        if not restaurant:
            continue
        
        # Get followers of this restaurant
        followers_query = session.query(User).join(
            restaurant_followers,
            User.user_id == restaurant_followers.c.user_id
        ).filter(
            restaurant_followers.c.restaurant_id == restaurant.restaurant_id
        )
        
        followers = followers_query.all()
        
        # Create notification for each follower
        for follower in followers:
            notification = Notification(
                user_id=follower.user_id,
                title=f"New Promotion at {restaurant.name}",
                message=f"Check out the new '{promotion.title}' promotion! {promotion.description[:50]}...",
                is_read=random.choice([True, False]),
                created_at=promotion.created_at + timedelta(hours=random.randint(1, 24)),
                promotion_id=promotion.promotion_id
            )
            
            session.add(notification)
            count += 1
    
    # Commit changes
    session.commit()
    print(f"Successfully inserted {count} notifications into the database.")

# -------------------------------------------------------------------------
# Main Function
# -------------------------------------------------------------------------
def populate_database(db_username, db_password, host='localhost', db_name='what2eat_um'):
    """Populate the entire database with sample data"""
    
    print(f"Starting database population for {db_name}...")
    
    # Configure the database connection
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{db_username}:{db_password}@{host}/{db_name}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Create a connection to the database
    with app.app_context():
        # Create a session
        Session = sessionmaker(bind=db.engine)
        session = Session()
        
        try:
            # Insert data in the correct order to maintain relationships
            users = insert_sample_users(session)
            restaurants = insert_sample_restaurants(session, users)
            insert_business_hours(session, restaurants)
            insert_restaurant_photos(session, restaurants, users)
            reviews = insert_sample_reviews(session, restaurants, users)
            insert_review_photos(session, reviews)
            insert_sample_replies(session, reviews, users)
            insert_sample_promotions(session, restaurants, users)
            insert_sample_claims(session, restaurants, users)
            insert_restaurant_followers(session, restaurants, users)
            insert_sample_notifications(session, users)
            
            print("Database successfully populated with sample data!")
            
        except Exception as e:
            session.rollback()
            print(f"Error populating database: {e}")
            raise  # Re-raise the exception to see the full traceback
            
        finally:
            session.close()

if __name__ == "__main__":
    # Get database credentials from command line arguments or use defaults
    import argparse
    
    parser = argparse.ArgumentParser(description='Populate What2Eat database with sample data')
    parser.add_argument('--username', default='root', help='MySQL username')
    parser.add_argument('--password', default='', help='MySQL password')
    parser.add_argument('--host', default='localhost', help='MySQL host')
    parser.add_argument('--db', default='what2eat_um', help='Database name')
    
    args = parser.parse_args()
    
    # Populate the database
    populate_database(args.username, args.password, args.host, args.db)