from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pymysql
import enum
from flask_login import UserMixin

# Configure PyMySQL to be used with SQLAlchemy
pymysql.install_as_MySQLdb()

# Initialize Flask app
app = Flask(__name__)

# Configure the database connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost:3306/what2eat_um'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# --------------------------------------------------------------------------------
# ENUMS
# --------------------------------------------------------------------------------

# Enum for user roles
# This defines the three types of users in the system as specified in the README:
# - General Users (students, staff, visitors)
# - Restaurant Managers (can claim and manage restaurant profiles)
# - Admin (pre-defined account with full platform management capabilities)
class UserRole(enum.Enum):
    GENERAL_USER = 'general_user'
    RESTAURANT_MANAGER = 'restaurant_manager'
    ADMIN = 'admin'

# Enum for cuisine types
# This defines the pre-defined list of cuisine types mentioned in the README
# for restaurant categorization and filtering
class CuisineType(enum.Enum):
    CHINESE = 'chinese'
    CANTONESE = 'cantonese'
    WESTERN = 'western'
    ASIAN = 'asian'
    FAST_FOOD = 'fast_food'
    VEGETARIAN = 'vegetarian'
    DESSERT = 'dessert'
    BEVERAGE = 'beverage'
    OTHER = 'other'

# --------------------------------------------------------------------------------
# ASSOCIATION TABLES
# --------------------------------------------------------------------------------

# Association table for restaurant followers
# This implements the "Follow Button" feature mentioned in the README
# It creates a many-to-many relationship between users and restaurants they follow
# When a user follows a restaurant, they will receive notifications about promotions
restaurant_followers = db.Table('restaurant_followers',
    db.Column('user_id', db.String(50), db.ForeignKey('user.user_id'), primary_key=True),
    db.Column('restaurant_id', db.Integer, db.ForeignKey('restaurant.restaurant_id'), primary_key=True),
    db.Column('followed_at', db.DateTime, default=datetime.utcnow)
)

# --------------------------------------------------------------------------------
# USER MANAGEMENT MODELS
# --------------------------------------------------------------------------------

# User Model
# This table stores all user accounts in the system, including:
# - General users who can browse, leave reviews, and follow restaurants
# - Restaurant managers who can claim and manage restaurant profiles
# - Admin users who can manage the entire platform
# Update the User model
class User(db.Model, UserMixin):
    __tablename__ = 'user'
    
    user_id = db.Column(db.String(50), primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum(UserRole), default=UserRole.GENERAL_USER)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    is_email_verified = db.Column(db.Boolean, default=False)
    
    # Add this method for Flask-Login
    def get_id(self):
        return self.user_id
    
    # Relationships - specify foreign keys explicitly
    restaurant_claims = db.relationship('RestaurantClaim', 
                                       foreign_keys='RestaurantClaim.user_id',
                                       backref='claimant', lazy=True)
    processed_claims = db.relationship('RestaurantClaim',
                                      foreign_keys='RestaurantClaim.processed_by',
                                      backref='processor', lazy=True)
    # Other relationships remain the same
    reviews = db.relationship('Review', backref='user', lazy=True, cascade='all, delete-orphan')
    restaurants = db.relationship('Restaurant', secondary=restaurant_followers, 
                                  backref=db.backref('followers', lazy='dynamic'))
    notifications = db.relationship('Notification', backref='user', lazy=True, cascade='all, delete-orphan')
    replies = db.relationship('Reply', backref='user', lazy=True, cascade='all, delete-orphan')

# --------------------------------------------------------------------------------
# RESTAURANT MODELS
# --------------------------------------------------------------------------------

# Restaurant Model
# This is the core entity for dining locations on campus
# Stores basic information about each restaurant as specified in README
# Will be displayed on homepage and in search results
class Restaurant(db.Model):
    __tablename__ = 'restaurant'
    
    restaurant_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)  # Restaurant name
    location = db.Column(db.String(255), nullable=False)  # Building name or campus area
    address = db.Column(db.String(255), nullable=False)  # Detailed address information
    cuisine_type = db.Column(db.Enum(CuisineType), nullable=False)  # For filtering/categorization
    description = db.Column(db.Text)  # Additional details about the restaurant
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # When the listing was created
    is_verified = db.Column(db.Boolean, default=False)  # Whether the restaurant has been claimed and verified
    manager_id = db.Column(db.String(50), db.ForeignKey('user.user_id'), nullable=True)  # The user who manages this restaurant
    
    # Relationships
    # Links to restaurant hours, photos, reviews, promotions, and claim requests
    business_hours = db.relationship('BusinessHour', backref='restaurant', lazy=True, cascade='all, delete-orphan')
    photos = db.relationship('RestaurantPhoto', backref='restaurant', lazy=True, cascade='all, delete-orphan')
    reviews = db.relationship('Review', backref='restaurant', lazy=True, cascade='all, delete-orphan')
    promotions = db.relationship('Promotion', backref='restaurant', lazy=True, cascade='all, delete-orphan')
    restaurant_claims = db.relationship('RestaurantClaim', backref='restaurant', lazy=True)
    # followers relationship is defined in the User model via restaurant_followers table

# BusinessHour Model
# Stores operating hours for each restaurant by day of week
# This enables the auto-highlight feature for open/closed status mentioned in README
class BusinessHour(db.Model):
    __tablename__ = 'business_hour'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.restaurant_id'), nullable=False)
    day_of_week = db.Column(db.Integer, nullable=False)  # 0 = Monday, 6 = Sunday
    open_time = db.Column(db.Time, nullable=False)  # Opening time for this day
    close_time = db.Column(db.Time, nullable=False)  # Closing time for this day
    
    # Ensure each restaurant has only one entry per day of week
    __table_args__ = (
        db.UniqueConstraint('restaurant_id', 'day_of_week', name='_restaurant_day_uc'),
    )

# RestaurantPhoto Model
# Stores photos associated with restaurants
# These can be uploaded by restaurant managers or users (requiring approval)
# Listed as a feature in README under Restaurant Profile Page
class RestaurantPhoto(db.Model):
    __tablename__ = 'restaurant_photo'
    
    photo_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.restaurant_id'), nullable=False)
    file_path = db.Column(db.String(255), nullable=False)  # Path to the stored image file
    uploaded_by = db.Column(db.String(50), db.ForeignKey('user.user_id'), nullable=False)  # Who uploaded this photo
    is_approved = db.Column(db.Boolean, default=False)  # User submitted photos require approval
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)  # When the photo was uploaded

# --------------------------------------------------------------------------------
# REVIEW SYSTEM MODELS
# --------------------------------------------------------------------------------

# Review Model
# Stores user reviews and ratings for restaurants
# Core feature mentioned in README under Restaurant Profile Page
class Review(db.Model):
    __tablename__ = 'review'
    
    review_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.restaurant_id'), nullable=False)
    user_id = db.Column(db.String(50), db.ForeignKey('user.user_id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)  # 1-5 stars as mentioned in README
    comment = db.Column(db.Text, nullable=False)  # Text review
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # When the review was posted
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)  # Track if review was edited
    
    # Relationships
    # Links to photos added to the review and replies to the review
    photos = db.relationship('ReviewPhoto', backref='review', lazy=True, cascade='all, delete-orphan')
    replies = db.relationship('Reply', backref='review', lazy=True, cascade='all, delete-orphan')

# ReviewPhoto Model
# Stores photos associated with user reviews
# README mentions users can include photos with their reviews
class ReviewPhoto(db.Model):
    __tablename__ = 'review_photo'
    
    photo_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    review_id = db.Column(db.Integer, db.ForeignKey('review.review_id'), nullable=False)
    file_path = db.Column(db.String(255), nullable=False)  # Path to the stored image file
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)  # When the photo was uploaded

# Reply Model
# Enables users (including restaurant managers) to reply to reviews
# This adds interaction to the review system, particularly for restaurant managers
# to respond to customer feedback
class Reply(db.Model):
    __tablename__ = 'reply'
    
    reply_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    review_id = db.Column(db.Integer, db.ForeignKey('review.review_id'), nullable=False)  # The review being replied to
    user_id = db.Column(db.String(50), db.ForeignKey('user.user_id'), nullable=False)  # Who wrote the reply
    content = db.Column(db.Text, nullable=False)  # Text content of the reply
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # When the reply was posted
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)  # Track if reply was edited

# --------------------------------------------------------------------------------
# PROMOTION AND NOTIFICATION MODELS
# --------------------------------------------------------------------------------

# Promotion Model
# Stores restaurant promotions and announcements
# Core feature mentioned in README under Restaurant Profile Page
# These trigger notifications to followers when posted
class Promotion(db.Model):
    __tablename__ = 'promotion'
    
    promotion_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.restaurant_id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)  # Promotion title
    description = db.Column(db.Text, nullable=False)  # Detailed description
    start_date = db.Column(db.DateTime, nullable=False)  # When the promotion begins
    end_date = db.Column(db.DateTime, nullable=False)  # When the promotion ends
    image_path = db.Column(db.String(255))  # Optional image for the promotion
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # When the promotion was created
    created_by = db.Column(db.String(50), db.ForeignKey('user.user_id'), nullable=False)  # Restaurant manager who created it
    
    # Relationships
    # Links to notifications generated by this promotion
    notifications = db.relationship('Notification', backref='promotion', lazy=True, cascade='all, delete-orphan')

# RestaurantClaim Model
# Manages the process for restaurant managers to claim their listings
# Implements the restaurant claiming workflow mentioned in README
class RestaurantClaim(db.Model):
    __tablename__ = 'restaurant_claim'
    
    claim_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.restaurant_id'), nullable=False)  # Restaurant being claimed
    user_id = db.Column(db.String(50), db.ForeignKey('user.user_id'), nullable=False)  # User requesting ownership
    proof_document = db.Column(db.String(255), nullable=False)  # Path to uploaded ownership verification document
    status = db.Column(db.String(20), default='pending')  # Claim status: pending, approved, rejected
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)  # When the claim was submitted
    processed_at = db.Column(db.DateTime)  # When admin processed the claim
    processed_by = db.Column(db.String(50), db.ForeignKey('user.user_id'), nullable=True)  # Admin who processed the claim
    notes = db.Column(db.Text)  # Additional notes about the claim decision

# Notification Model
# Implements the in-app notification system mentioned in README
# Primarily used to notify users when followed restaurants post promotions
class Notification(db.Model):
    __tablename__ = 'notification'
    
    notification_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String(50), db.ForeignKey('user.user_id'), nullable=False)  # User receiving the notification
    title = db.Column(db.String(100), nullable=False)  # Notification title
    message = db.Column(db.Text, nullable=False)  # Notification content
    is_read = db.Column(db.Boolean, default=False)  # Whether user has read the notification
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # When the notification was created
    promotion_id = db.Column(db.Integer, db.ForeignKey('promotion.promotion_id'), nullable=True)  # Related promotion if applicable
    
    # This model can be extended to support other notification types as needed

# Function to create database and tables
def create_database(username, password, host='localhost', database_name='what2eat_um'):
    """Create the database and tables if they don't exist"""
    # Create connection
    conn = pymysql.connect(
        host=host,
        user=username,
        password=password
    )
    cursor = conn.cursor()
    
    # Create database if it doesn't exist
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")
    conn.commit()
    
    # Update app configuration with the provided credentials
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{username}:{password}@{host}/{database_name}'
    
    # Create all tables
    with app.app_context():
        db.create_all()
    
    cursor.close()
    conn.close()
    print("Database and tables created successfully!")

# Example usage
if __name__ == '__main__':
    create_database(
        username='root',
        password='',
        host='localhost',
        database_name='what2eat_um'
    )