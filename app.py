from flask import Flask, render_template, redirect, url_for, flash, request, session, abort, send_from_directory, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from flask_login import LoginManager, current_user, login_user, logout_user, login_required, UserMixin
from flask_migrate import Migrate
import os
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from flask.cli import with_appcontext
import secrets
import string
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from models import db, User, UserRole, Restaurant, BusinessHour, RestaurantPhoto, CuisineType, Review, ReviewPhoto, Promotion, Reply, RestaurantClaim, Notification
import sys
from werkzeug.exceptions import Forbidden

# Load environment variables
load_dotenv()

# Create Flask app
app = Flask(__name__)

# Configure app
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-for-testing')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', "mysql+pymysql://root@localhost:3306/what2eat_um")
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload size
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static/uploads')

# Email configuration
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', 587))
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME', 'what2eatatum@gmail.com')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER', 'what2eatatum@gmail.com')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD', None)
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

# Initialize extensions
mail = Mail(app)
db.init_app(app)
migrate = Migrate(app, db)

# Initialize login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

def send_email(subject, recipients, body, html=None):
    try:
        msg = Message(subject=subject, recipients=recipients, body=body, html=html)
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

def generate_verification_code(length=6):
    """Generate a random verification code"""
    characters = string.ascii_letters + string.digits
    return ''.join(secrets.choice(characters) for _ in range(length))

# Admin required decorator
def admin_required(f):
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != UserRole.ADMIN:
            flash('You do not have permission to access this page.', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

# File upload helper functions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_image(file, folder_name):
    """Save an image to the specified folder and return the filename"""
    if file and file.filename and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # Generate a unique filename to prevent overwriting
        unique_filename = f"{uuid.uuid4().hex}_{filename}"
        # Create the folder if it doesn't exist
        folder_path = os.path.join(app.config['UPLOAD_FOLDER'], folder_name)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        file_path = os.path.join(folder_path, unique_filename)
        file.save(file_path)
        return f"{folder_name}/{unique_filename}"
    return None

# Routes
@app.route('/')
def index():
    # Get a few random restaurants to display on the homepage
    restaurants = Restaurant.query.order_by(db.func.random()).limit(6).all()
    return render_template('index.html', restaurants=restaurants, now=utc_to_local(datetime.utcnow()))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        
        if not user or not check_password_hash(user.password, password):
            flash('Please check your login details and try again.', 'danger')
            return redirect(url_for('login'))
            
        # Check if user has verified their email
        if not user.is_email_verified:
            flash('Please verify your email before logging in.', 'warning')
            session['unverified_user_id'] = user.user_id
            return redirect(url_for('verify_email'))
            
        login_user(user)
        user.last_login = datetime.utcnow()
        db.session.commit()
        
        next_page = request.args.get('next')
        
        # Redirect admin to dashboard
        if user.role == UserRole.ADMIN:
            return redirect(url_for('admin_dashboard'))
            
        return redirect(next_page or url_for('index'))
        
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Form validation
        if not all([username, email, password, confirm_password]):
            flash('All fields are required', 'danger')
            return redirect(url_for('register'))
            
        if len(password) < 8:
            flash('Password must be at least 8 characters long', 'danger')
            return redirect(url_for('register'))
            
        if password != confirm_password:
            flash('Passwords do not match', 'danger')
            return redirect(url_for('register'))
            
        # Check if email or username already exists
        if User.query.filter_by(email=email).first():
            flash('Email already exists', 'danger')
            return redirect(url_for('register'))
            
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'danger')
            return redirect(url_for('register'))
        
        # Create new user
        user_id = secrets.token_hex(16)  # Generate a random user ID
        hashed_password = generate_password_hash(password)
        
        new_user = User(
            user_id=user_id,
            username=username,
            email=email,
            password=hashed_password,
            role=UserRole.GENERAL_USER
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        # Generate and store verification code
        verification_code = generate_verification_code()
        session[f'verification_{user_id}'] = {
            'code': verification_code,
            'expires': (datetime.utcnow() + timedelta(minutes=30)).isoformat()
        }
        session['unverified_user_id'] = user_id
        
        # Send verification email
        subject = "Verify your What2Eat@UM account"
        body = f"""
        Hello {username},
        
        Thank you for registering with What2Eat@UM!
        
        Your verification code is: {verification_code}
        
        Please enter this code on the verification page to complete your registration.
        This code will expire in 30 minutes.
        
        Best regards,
        The What2Eat@UM Team
        """
        
        send_email(subject, [email], body)
        
        flash('Registration successful! Please check your email for verification code.', 'success')
        return redirect(url_for('verify_email'))
    
    return render_template('register.html')

@app.route('/verify-email', methods=['GET', 'POST'])
def verify_email():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    user_id = session.get('unverified_user_id')
    if not user_id:
        flash('No pending verification found', 'danger')
        return redirect(url_for('login'))
    
    user = User.query.get(user_id)
    if not user:
        flash('User not found', 'danger')
        session.pop('unverified_user_id', None)
        return redirect(url_for('register'))
    
    if request.method == 'POST':
        verification_info = session.get(f'verification_{user_id}')
        if not verification_info:
            flash('Verification code expired. Please request a new one.', 'warning')
            return redirect(url_for('resend_verification'))
        
        # Check if verification code has expired
        if datetime.utcnow() > datetime.fromisoformat(verification_info['expires']):
            session.pop(f'verification_{user_id}', None)
            flash('Verification code expired. Please request a new one.', 'warning')
            return redirect(url_for('resend_verification'))
        
        # Verify the code
        submitted_code = request.form.get('verification_code')
        if submitted_code != verification_info['code']:
            flash('Invalid verification code', 'danger')
            return redirect(url_for('verify_email'))
        
        # Mark user as verified and clean up session
        user.is_email_verified = True
        db.session.commit()
        session.pop(f'verification_{user_id}', None)
        
        flash('Email verification successful! You can now log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('verify_email.html', email=user.email)

@app.route('/resend-verification', methods=['GET'])
def resend_verification():
    user_id = session.get('unverified_user_id')
    if not user_id:
        flash('No pending verification found', 'danger')
        return redirect(url_for('login'))
    
    user = User.query.get(user_id)
    if not user:
        flash('User not found', 'danger')
        session.pop('unverified_user_id', None)
        return redirect(url_for('register'))
    
    # Generate and store a new verification code
    verification_code = generate_verification_code()
    session[f'verification_{user_id}'] = {
        'code': verification_code,
        'expires': (datetime.utcnow() + timedelta(minutes=30)).isoformat()
    }
    
    # Send new verification email
    subject = "Your New Verification Code for What2Eat@UM"
    body = f"""
    Hello {user.username},
    
    You requested a new verification code for your What2Eat@UM account.
    
    Your new verification code is: {verification_code}
    
    Please enter this code on the verification page to complete your registration.
    This code will expire in 30 minutes.
    
    Best regards,
    The What2Eat@UM Team
    """
    
    send_email(subject, [user.email], body)
    
    flash('A new verification code has been sent to your email', 'info')
    return redirect(url_for('verify_email'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out', 'info')
    return redirect(url_for('login'))

@app.route('/request-password-reset', methods=['GET', 'POST'])
def request_password_reset():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        
        if user:
            # Generate password reset token
            token = secrets.token_hex(16)
            expiration = (datetime.utcnow() + timedelta(hours=1)).isoformat()
            
            # Store token in session
            session[f'pwd_reset_{token}'] = {
                'user_id': user.user_id,
                'expires': expiration
            }
            
            # Send password reset email
            reset_url = url_for('reset_password', token=token, _external=True)
            subject = "Reset Your What2Eat@UM Password"
            body = f"""
            Hello {user.username},
            
            You requested to reset your What2Eat@UM password.
            
            Please click on the following link to reset your password:
            {reset_url}
            
            This link will expire in 1 hour.
            
            If you did not request a password reset, please ignore this email.
            
            Best regards,
            The What2Eat@UM Team
            """
            
            send_email(subject, [user.email], body)
        
        # Always show the same message even if user doesn't exist for security
        flash('If your email is registered, you will receive password reset instructions', 'info')
        return redirect(url_for('login'))
    
    return render_template('request_password_reset.html')

@app.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    # Verify token
    reset_info = session.get(f'pwd_reset_{token}')
    if not reset_info:
        flash('Invalid or expired password reset link', 'danger')
        return redirect(url_for('login'))
    
    # Check if token has expired
    if datetime.utcnow() > datetime.fromisoformat(reset_info['expires']):
        session.pop(f'pwd_reset_{token}', None)
        flash('Password reset link has expired', 'danger')
        return redirect(url_for('request_password_reset'))
    
    user = User.query.get(reset_info['user_id'])
    if not user:
        session.pop(f'pwd_reset_{token}', None)
        flash('User not found', 'danger')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if not password or not confirm_password:
            flash('All fields are required', 'danger')
            return redirect(url_for('reset_password', token=token))
        
        if len(password) < 8:
            flash('Password must be at least 8 characters long', 'danger')
            return redirect(url_for('reset_password', token=token))
        
        if password != confirm_password:
            flash('Passwords do not match', 'danger')
            return redirect(url_for('reset_password', token=token))
        
        # Update user's password
        user.password = generate_password_hash(password)
        db.session.commit()
        
        # Clean up session
        session.pop(f'pwd_reset_{token}', None)
        
        flash('Your password has been reset successfully. You can now log in with your new password.', 'success')
        return redirect(url_for('login'))
    
    return render_template('reset_password.html')

# Add admin template context helper function
def get_admin_template_context(**kwargs):
    """Get common context variables for admin templates"""
    context = {
        'pending_claims_count': RestaurantClaim.query.filter_by(status='pending').count()
    }
    # Add any additional kwargs to the context
    context.update(kwargs)
    return context

@app.route('/admin')
@admin_required
def admin_dashboard():
    restaurant_count = Restaurant.query.count()
    user_count = User.query.count()
    review_count = Review.query.count()
    
    context = get_admin_template_context(
        restaurant_count=restaurant_count,
        user_count=user_count,
        review_count=review_count,
        datetime=datetime
    )
    
    return render_template('admin/dashboard.html', **context)

@app.route('/admin/restaurants')
@admin_required
def admin_restaurants():
    restaurants = Restaurant.query.all()
    context = get_admin_template_context(restaurants=restaurants)
    return render_template('admin/restaurants.html', **context)

@app.route('/admin/restaurants/new', methods=['GET', 'POST'])
@admin_required
def admin_add_restaurant():
    if request.method == 'POST':
        name = request.form.get('name')
        location = request.form.get('location')
        address = request.form.get('address')
        cuisine_type = request.form.get('cuisine_type')
        description = request.form.get('description')
        
        # Validate the form
        if not all([name, location, address, cuisine_type]):
            flash('Required fields are missing.', 'danger')
            return redirect(url_for('admin_add_restaurant'))
        
        # Create new restaurant
        new_restaurant = Restaurant(
            name=name,
            location=location,
            address=address,
            cuisine_type=getattr(CuisineType, cuisine_type),
            description=description,
            is_verified=False,  # All new restaurants are not verified by default
        )
        
        db.session.add(new_restaurant)
        db.session.commit()
        
        # Handle restaurant photos
        if 'photos' in request.files:
            photos = request.files.getlist('photos')
            for photo in photos:
                if photo and photo.filename and allowed_file(photo.filename):
                    # Save the image
                    file_path = save_image(photo, 'restaurants')
                    if file_path:
                        restaurant_photo = RestaurantPhoto(
                            restaurant_id=new_restaurant.restaurant_id,
                            file_path=file_path,
                            uploaded_by=current_user.user_id,
                            is_approved=True  # Admin uploads are auto-approved
                        )
                        db.session.add(restaurant_photo)
        
        # Handle business hours
        days = request.form.getlist('day_of_week')
        open_times = request.form.getlist('open_time')
        close_times = request.form.getlist('close_time')
        
        for i in range(len(days)):
            if days[i] and open_times[i] and close_times[i]:
                business_hour = BusinessHour(
                    restaurant_id=new_restaurant.restaurant_id,
                    day_of_week=int(days[i]),
                    open_time=datetime.strptime(open_times[i], '%H:%M').time(),
                    close_time=datetime.strptime(close_times[i], '%H:%M').time()
                )
                db.session.add(business_hour)
        
        db.session.commit()
        flash('Restaurant added successfully.', 'success')
        return redirect(url_for('admin_restaurants'))
    
    context = get_admin_template_context(cuisine_types=CuisineType)
    return render_template('admin/add_restaurant.html', **context)

@app.route('/admin/restaurants/<int:restaurant_id>/edit', methods=['GET', 'POST'])
@admin_required
def admin_edit_restaurant(restaurant_id):
    restaurant = Restaurant.query.get_or_404(restaurant_id)
    
    if request.method == 'POST':
        # Get form data
        restaurant.name = request.form.get('name')
        restaurant.location = request.form.get('location')
        restaurant.address = request.form.get('address')
        restaurant.cuisine_type = getattr(CuisineType, request.form.get('cuisine_type', 'OTHER'))
        restaurant.description = request.form.get('description')
        
        # Validate the form
        if not all([restaurant.name, restaurant.location, restaurant.address]):
            flash('Required fields are missing.', 'danger')
            return redirect(url_for('admin_edit_restaurant', restaurant_id=restaurant_id))
        
        # Handle business hours
        # First, delete existing hours
        BusinessHour.query.filter_by(restaurant_id=restaurant_id).delete()
        
        # Then add new hours
        days = request.form.getlist('day_of_week')
        open_times = request.form.getlist('open_time')
        close_times = request.form.getlist('close_time')
        
        for i in range(len(days)):
            if days[i] and open_times[i] and close_times[i]:
                try:
                    business_hour = BusinessHour(
                        restaurant_id=restaurant_id,
                        day_of_week=int(days[i]),
                        open_time=datetime.strptime(open_times[i], '%H:%M').time(),
                        close_time=datetime.strptime(close_times[i], '%H:%M').time()
                    )
                    db.session.add(business_hour)
                except ValueError:
                    flash(f'Invalid time format for day {days[i]}', 'danger')
        
        # Handle restaurant photos
        if 'photos' in request.files:
            photos = request.files.getlist('photos')
            for photo in photos:
                if photo and photo.filename and allowed_file(photo.filename):
                    # Save the image
                    file_path = save_image(photo, 'restaurants')
                    if file_path:
                        restaurant_photo = RestaurantPhoto(
                            restaurant_id=restaurant_id,
                            file_path=file_path,
                            uploaded_by=current_user.user_id,
                            is_approved=True  # Admin uploads are auto-approved
                        )
                        db.session.add(restaurant_photo)
        
        db.session.commit()
        flash('Restaurant updated successfully.', 'success')
        return redirect(url_for('admin_restaurants'))
    
    # Prepare current business hours for the template
    business_hours = BusinessHour.query.filter_by(restaurant_id=restaurant_id).all()
    
    context = get_admin_template_context(
        restaurant=restaurant,
        business_hours=business_hours,
        cuisine_types=CuisineType
    )
    
    return render_template('admin/edit_restaurant.html', **context)

@app.route('/admin/restaurants/<int:restaurant_id>/delete', methods=['POST'])
@admin_required
def admin_delete_restaurant(restaurant_id):
    restaurant = Restaurant.query.get_or_404(restaurant_id)
    
    # Delete associated photos from filesystem
    for photo in restaurant.photos:
        if photo.file_path:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], photo.file_path)
            if os.path.exists(file_path):
                os.remove(file_path)
    
    db.session.delete(restaurant)
    db.session.commit()
    
    flash('Restaurant deleted successfully.', 'success')
    return redirect(url_for('admin_restaurants'))

@app.route('/admin/restaurants/<int:restaurant_id>/photos/<int:photo_id>/delete', methods=['POST'])
@admin_required
def admin_delete_restaurant_photo(restaurant_id, photo_id):
    photo = RestaurantPhoto.query.get_or_404(photo_id)
    
    # Basic check to ensure the photo belongs to the restaurant (optional but good practice)
    if photo.restaurant_id != restaurant_id:
        return jsonify({'success': False, 'message': 'Photo not found for this restaurant.'}), 404
        
    try:
        # Delete the file from filesystem
        if photo.file_path:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], photo.file_path)
            if os.path.exists(file_path):
                os.remove(file_path)
        
        db.session.delete(photo)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Photo deleted successfully.'})
    except Exception as e:
        db.session.rollback()
        print(f"Error deleting photo {photo_id}: {e}") # Log the error
        return jsonify({'success': False, 'message': 'Failed to delete photo.'}), 500

@app.route('/admin/users')
@admin_required
def admin_users():
    users = User.query.all()
    context = get_admin_template_context(users=users)
    return render_template('admin/users.html', **context)

@app.route('/admin/reviews')
@admin_required
def admin_reviews():
    reviews = Review.query.order_by(Review.created_at.desc()).all()
    context = get_admin_template_context(reviews=reviews)
    return render_template('admin/reviews.html', **context)

@app.route('/admin/reviews/<int:review_id>/delete', methods=['POST'])
@admin_required
def admin_delete_review(review_id):
    review = Review.query.get_or_404(review_id)
    
    # Delete review photos from filesystem
    for photo in review.photos:
        if photo.file_path:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], photo.file_path)
            if os.path.exists(file_path):
                os.remove(file_path)
    
    # Store restaurant_id for redirect
    restaurant_id = review.restaurant_id
    
    db.session.delete(review)
    db.session.commit()
    
    # Check if request came from restaurant detail page
    redirect_url = request.referrer
    if redirect_url and 'restaurant/' + str(restaurant_id) in redirect_url:
        flash('Review deleted successfully.', 'success')
        return redirect(url_for('restaurant_detail', restaurant_id=restaurant_id))
    else:
        flash('Review deleted successfully.', 'success')
        return redirect(url_for('admin_reviews'))

@app.route('/admin/replies/<int:reply_id>/delete', methods=['POST'])
@admin_required
def admin_delete_reply(reply_id):
    reply = Reply.query.get_or_404(reply_id)
    
    # Store restaurant_id for redirect
    restaurant_id = reply.review.restaurant_id
    
    db.session.delete(reply)
    db.session.commit()
    
    # Check if request came from restaurant detail page
    redirect_url = request.referrer
    if redirect_url and 'restaurant/' + str(restaurant_id) in redirect_url:
        flash('Reply deleted successfully.', 'success')
        return redirect(url_for('restaurant_detail', restaurant_id=restaurant_id))
    else:
        flash('Reply deleted successfully.', 'success')
        return redirect(url_for('admin_reviews'))

# Restaurant routes
@app.route('/restaurant/<int:restaurant_id>')
def restaurant_detail(restaurant_id):
    restaurant = Restaurant.query.get_or_404(restaurant_id)
    # Get restaurant reviews ordered by most recent
    reviews = Review.query.filter_by(restaurant_id=restaurant_id).order_by(Review.created_at.desc()).all()
    # Check for active promotions
    now_utc = datetime.utcnow()
    active_promotions = Promotion.query.filter(
        Promotion.restaurant_id == restaurant_id,
        Promotion.start_date <= now_utc,
        Promotion.end_date >= now_utc
    ).order_by(Promotion.end_date).all()
    
    # Check if ANY active promotion exists for the badge
    has_active_promotion = len(active_promotions) > 0 
    
    return render_template('restaurant_detail.html', 
                          restaurant=restaurant,
                          reviews=reviews,
                          has_active_promotion=has_active_promotion,
                          active_promotions=active_promotions, # Pass the list of active promotions
                          now=utc_to_local(now_utc))

@app.route('/restaurants')
def restaurant_list():
    # Get search parameters from query string
    search_query = request.args.get('q', '')
    cuisine_type = request.args.get('cuisine', '')
    min_rating = request.args.get('min_rating', '')
    sort_by = request.args.get('sort', 'name')  # Default sort by name
    page = request.args.get('page', 1, type=int)  # Get current page, default is 1
    per_page = 12  # 12 restaurants per page (4 in a row, 3 rows)
    
    # Start with base query
    query = Restaurant.query
    
    # Apply search filter if provided
    if search_query:
        query = query.filter(Restaurant.name.like(f'%{search_query}%'))
    
    # Apply cuisine type filter if provided
    if cuisine_type and cuisine_type != 'all':
        query = query.filter(Restaurant.cuisine_type == getattr(CuisineType, cuisine_type.upper(), None))
    
    # Get all restaurants that match the filters so far
    all_restaurants = query.all()
    
    # Filter by rating if specified (done in Python since it requires avg calculation)
    if min_rating and min_rating.isdigit():
        min_rating = int(min_rating)
        filtered_restaurants = []
        
        for restaurant in all_restaurants:
            # Calculate average rating
            if restaurant.reviews:
                avg_rating = sum(review.rating for review in restaurant.reviews) / len(restaurant.reviews)
                if avg_rating >= min_rating:
                    # Add rating to restaurant object for sorting
                    restaurant.avg_rating = avg_rating
                    filtered_restaurants.append(restaurant)
            elif min_rating == 0:  # Include unrated restaurants if min_rating is 0
                restaurant.avg_rating = 0
                filtered_restaurants.append(restaurant)
        
        all_restaurants = filtered_restaurants
    else:
        # Add avg_rating attribute to all restaurants for sorting
        for restaurant in all_restaurants:
            if restaurant.reviews:
                restaurant.avg_rating = sum(review.rating for review in restaurant.reviews) / len(restaurant.reviews)
            else:
                restaurant.avg_rating = 0
    
    # Sort restaurants
    if sort_by == 'rating':
        all_restaurants.sort(key=lambda x: x.avg_rating, reverse=True)
    elif sort_by == 'name':
        all_restaurants.sort(key=lambda x: x.name)
    
    # Check for active promotions and tag restaurants
    now_utc = datetime.utcnow()
    for restaurant in all_restaurants:
        restaurant.has_active_promotion = Promotion.query.filter(
            Promotion.restaurant_id == restaurant.restaurant_id,
            Promotion.start_date <= now_utc,
            Promotion.end_date >= now_utc
        ).first() is not None
    
    # Sort by active promotions if specified
    if sort_by == 'promo':
        all_restaurants.sort(key=lambda x: (not x.has_active_promotion, x.name))
    
    # Calculate total pages
    total_restaurants = len(all_restaurants)
    total_pages = (total_restaurants + per_page - 1) // per_page  # Ceiling division
    
    # Paginate the results
    start_idx = (page - 1) * per_page
    end_idx = min(start_idx + per_page, total_restaurants)
    restaurants = all_restaurants[start_idx:end_idx]
    
    # Prepare pagination info
    pagination = {
        'page': page,
        'per_page': per_page,
        'total_pages': total_pages,
        'total_restaurants': total_restaurants,
        'has_prev': page > 1,
        'has_next': page < total_pages
    }
    
    return render_template(
        'all_restaurant.html',
        restaurants=restaurants,
        search_query=search_query,
        cuisine_type=cuisine_type,
        min_rating=min_rating,
        sort_by=sort_by,
        cuisine_types=CuisineType,
        pagination=pagination,
        now=utc_to_local(now_utc)
    )

@app.route('/restaurant/<int:restaurant_id>/review', methods=['POST'])
@login_required
def add_review(restaurant_id):
    restaurant = Restaurant.query.get_or_404(restaurant_id)
    
    # Get form data
    rating = request.form.get('rating')
    comment = request.form.get('comment')
    
    if not rating or not comment:
        flash('Rating and comment are required', 'danger')
        return redirect(url_for('restaurant_detail', restaurant_id=restaurant_id))
    
    # Create new review
    new_review = Review(
        restaurant_id=restaurant_id,
        user_id=current_user.user_id,
        rating=rating,
        comment=comment
    )
    
    db.session.add(new_review)
    db.session.commit()
    
    # Handle review photos
    if 'photos' in request.files:
        photos = request.files.getlist('photos')
        for photo in photos:
            if photo and photo.filename and allowed_file(photo.filename):
                # Save the image
                file_path = save_image(photo, 'reviews')
                if file_path:
                    review_photo = ReviewPhoto(
                        review_id=new_review.review_id,
                        file_path=file_path
                    )
                    db.session.add(review_photo)
        db.session.commit()
    
    flash('Your review has been added successfully', 'success')
    return redirect(url_for('restaurant_detail', restaurant_id=restaurant_id))

@app.route('/review/<int:review_id>/edit', methods=['POST'])
@login_required
def edit_review(review_id):
    review = Review.query.get_or_404(review_id)
    
    # Check if the current user is the author of the review
    if review.user_id != current_user.user_id:
        flash('You can only edit your own reviews', 'danger')
        return redirect(url_for('restaurant_detail', restaurant_id=review.restaurant_id))
    
    # Get form data
    rating = request.form.get('rating')
    comment = request.form.get('comment')
    
    if not rating or not comment:
        flash('Rating and comment are required', 'danger')
        return redirect(url_for('restaurant_detail', restaurant_id=review.restaurant_id))
    
    # Update review
    review.rating = rating
    review.comment = comment
    review.updated_at = datetime.utcnow()
    
    db.session.commit()
    
    flash('Your review has been updated', 'success')
    return redirect(url_for('restaurant_detail', restaurant_id=review.restaurant_id))

@app.route('/review/<int:review_id>/delete', methods=['POST'])
@login_required
def delete_review(review_id):
    review = Review.query.get_or_404(review_id)
    
    # Check if the current user is the author of the review
    if review.user_id != current_user.user_id:
        flash('You can only delete your own reviews', 'danger')
        return redirect(url_for('restaurant_detail', restaurant_id=review.restaurant_id))
    
    restaurant_id = review.restaurant_id
    
    # Delete review photos from filesystem
    for photo in review.photos:
        if photo.file_path:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], photo.file_path)
            if os.path.exists(file_path):
                os.remove(file_path)
    
    db.session.delete(review)
    db.session.commit()
    
    flash('Your review has been deleted', 'success')
    return redirect(url_for('restaurant_detail', restaurant_id=restaurant_id))

@app.route('/review/<int:review_id>/reply', methods=['POST'])
@login_required
def add_reply(review_id):
    review = Review.query.get_or_404(review_id)
    
    content = request.form.get('content')
    
    if not content:
        flash('Reply content is required', 'danger')
        return redirect(url_for('restaurant_detail', restaurant_id=review.restaurant_id))
    
    # Create new reply
    new_reply = Reply(
        review_id=review_id,
        user_id=current_user.user_id,
        content=content
    )
    
    db.session.add(new_reply)
    db.session.commit()
    
    flash('Your reply has been added', 'success')
    return redirect(url_for('restaurant_detail', restaurant_id=review.restaurant_id))

@app.route('/reply/<int:reply_id>/edit', methods=['POST'])
@login_required
def edit_reply(reply_id):
    reply = Reply.query.get_or_404(reply_id)
    
    # Check if the current user is the author of the reply
    if reply.user_id != current_user.user_id:
        flash('You can only edit your own replies', 'danger')
        return redirect(url_for('restaurant_detail', restaurant_id=reply.review.restaurant_id))
    
    content = request.form.get('content')
    
    if not content:
        flash('Reply content is required', 'danger')
        return redirect(url_for('restaurant_detail', restaurant_id=reply.review.restaurant_id))
    
    # Update reply
    reply.content = content
    reply.updated_at = datetime.utcnow()
    
    db.session.commit()
    
    flash('Your reply has been updated', 'success')
    return redirect(url_for('restaurant_detail', restaurant_id=reply.review.restaurant_id))

@app.route('/reply/<int:reply_id>/delete', methods=['POST'])
@login_required
def delete_reply(reply_id):
    reply = Reply.query.get_or_404(reply_id)
    
    # Check if the current user is the author of the reply
    if reply.user_id != current_user.user_id:
        flash('You can only delete your own replies', 'danger')
        return redirect(url_for('restaurant_detail', restaurant_id=reply.review.restaurant_id))
    
    restaurant_id = reply.review.restaurant_id
    
    db.session.delete(reply)
    db.session.commit()
    
    flash('Your reply has been deleted', 'success')
    return redirect(url_for('restaurant_detail', restaurant_id=restaurant_id))

# User Profile Route
@app.route('/profile')
@login_required
def user_profile():
    # Get all reviews by the current user, ordered by most recent
    user_reviews = Review.query.filter_by(user_id=current_user.user_id).order_by(Review.created_at.desc()).all()
    
    return render_template('profile.html', user=current_user, reviews=user_reviews)

# Make UserRole available to all templates
@app.context_processor
def inject_user_role():
    return dict(UserRole=UserRole, utc_to_local=utc_to_local)

def utc_to_local(utc_dt):
    local_tz = timezone(timedelta(hours=8))
    return utc_dt.replace(tzinfo=timezone.utc).astimezone(local_tz)

# Test route for timezone functionality
@app.route('/test-timezone')
def test_timezone():
    now_utc = datetime.utcnow()
    now_local = utc_to_local(now_utc)
    return f"""
    <h1>Timezone Test</h1>
    <p>UTC time: {now_utc.strftime('%Y-%m-%d %H:%M:%S')}</p>
    <p>Local time (UTC+8): {now_local.strftime('%Y-%m-%d %H:%M:%S')}</p>
    """

# Add restaurant claim routes
@app.route('/restaurant/<int:restaurant_id>/claim')
@login_required
def claim_restaurant(restaurant_id):
    restaurant = Restaurant.query.get_or_404(restaurant_id)
    
    # Check if the restaurant is already verified
    if restaurant.is_verified:
        flash('This restaurant has already been claimed and verified.', 'info')
        return redirect(url_for('restaurant_detail', restaurant_id=restaurant_id))
    
    # Check if the user is an admin (admins cannot claim restaurants)
    if current_user.role == UserRole.ADMIN:
        flash('Admins cannot claim restaurants.', 'warning')
        return redirect(url_for('restaurant_detail', restaurant_id=restaurant_id))
    
    # Check if there's already a pending claim for this restaurant
    existing_claim = RestaurantClaim.query.filter_by(
        restaurant_id=restaurant_id,
        status='pending'
    ).first()
    
    if existing_claim:
        flash('This restaurant already has a pending claim. Please wait for admin review.', 'info')
        return redirect(url_for('restaurant_detail', restaurant_id=restaurant_id))
    
    # Check if the user already has a pending or approved claim for this restaurant
    user_claim = RestaurantClaim.query.filter_by(
        restaurant_id=restaurant_id,
        user_id=current_user.user_id
    ).filter(RestaurantClaim.status.in_(['pending', 'approved'])).first()
    
    if user_claim:
        if user_claim.status == 'pending':
            flash('You already have a pending claim for this restaurant.', 'info')
        else:  # approved
            flash('You already own this restaurant.', 'info')
        return redirect(url_for('restaurant_detail', restaurant_id=restaurant_id))
    
    return render_template('claim_restaurant.html', restaurant=restaurant)

@app.route('/restaurant/<int:restaurant_id>/claim/submit', methods=['POST'])
@login_required
def submit_restaurant_claim(restaurant_id):
    restaurant = Restaurant.query.get_or_404(restaurant_id)
    
    # Check if the restaurant is already verified
    if restaurant.is_verified:
        flash('This restaurant has already been claimed and verified.', 'info')
        return redirect(url_for('restaurant_detail', restaurant_id=restaurant_id))
    
    # Check if the user is an admin (admins cannot claim restaurants)
    if current_user.role == UserRole.ADMIN:
        flash('Admins cannot claim restaurants.', 'warning')
        return redirect(url_for('restaurant_detail', restaurant_id=restaurant_id))
    
    # Get form data
    certification = request.form.get('certification')
    contact_info = request.form.get('contact_info')
    additional_notes = request.form.get('additional_notes')
    
    # Validate required fields
    if not certification or not contact_info:
        flash('Certification and contact information are required.', 'danger')
        return redirect(url_for('claim_restaurant', restaurant_id=restaurant_id))
    
    # Handle proof document
    if 'proof_document' not in request.files:
        flash('Proof document is required.', 'danger')
        return redirect(url_for('claim_restaurant', restaurant_id=restaurant_id))
    
    proof_document = request.files['proof_document']
    if not proof_document or not proof_document.filename:
        flash('Proof document is required.', 'danger')
        return redirect(url_for('claim_restaurant', restaurant_id=restaurant_id))
    
    # Create document folder if it doesn't exist
    document_folder = os.path.join(app.config['UPLOAD_FOLDER'], 'documents', 'claims')
    if not os.path.exists(document_folder):
        os.makedirs(document_folder)
    
    # Save the proof document
    proof_filename = secure_filename(proof_document.filename)
    unique_proof_filename = f"{uuid.uuid4().hex}_{proof_filename}"
    file_path = os.path.join(document_folder, unique_proof_filename)
    proof_document.save(file_path)
    saved_path = f"documents/claims/{unique_proof_filename}"
    
    # Combine form information into the notes field
    combined_notes = f"Certification: {certification}\nContact Information: {contact_info}"
    if additional_notes:
        combined_notes += f"\nAdditional Notes: {additional_notes}"
    
    # Create new claim
    new_claim = RestaurantClaim(
        restaurant_id=restaurant_id,
        user_id=current_user.user_id,
        proof_document=saved_path,
        status='pending',
        submitted_at=datetime.utcnow(),
        notes=combined_notes
    )
    
    db.session.add(new_claim)
    db.session.commit()
    
    # Send notification to admin
    admin_users = User.query.filter_by(role=UserRole.ADMIN).all()
    for admin in admin_users:
        notification = Notification(
            user_id=admin.user_id,
            title="New Restaurant Claim",
            message=f"A new claim for {restaurant.name} has been submitted by {current_user.username}. Please review it.",
        )
        db.session.add(notification)
    
    db.session.commit()
    
    flash('Your claim has been submitted successfully and is pending admin review.', 'success')
    return redirect(url_for('restaurant_detail', restaurant_id=restaurant_id))

@app.route('/admin/restaurant-claims')
@admin_required
def admin_restaurant_claims():
    # Get all claims, ordered by most recent first
    claims = RestaurantClaim.query.order_by(RestaurantClaim.submitted_at.desc()).all()
    pending_claims_count = RestaurantClaim.query.filter_by(status='pending').count()
    
    return render_template('admin/restaurant_claims.html', 
                          claims=claims,
                          pending_claims_count=pending_claims_count)

@app.route('/admin/restaurant-claims/<int:claim_id>/approve', methods=['POST'])
@admin_required
def admin_approve_claim(claim_id):
    claim = RestaurantClaim.query.get_or_404(claim_id)
    
    # Check if claim is not already processed
    if claim.status != 'pending':
        flash('This claim has already been processed.', 'warning')
        return redirect(url_for('admin_restaurant_claims'))
    
    # Get the restaurant and user
    restaurant = Restaurant.query.get(claim.restaurant_id)
    user = User.query.get(claim.user_id)
    
    if not restaurant or not user:
        flash('Restaurant or user not found.', 'danger')
        return redirect(url_for('admin_restaurant_claims'))
    
    # Update the claim
    claim.status = 'approved'
    claim.processed_at = datetime.utcnow()
    claim.processed_by = current_user.user_id
    claim.notes = request.form.get('notes', '')
    
    # Update the restaurant
    restaurant.is_verified = True
    restaurant.manager_id = claim.user_id
    
    # Update the user's role to restaurant manager if they're not already an admin
    if user.role == UserRole.GENERAL_USER:
        user.role = UserRole.RESTAURANT_MANAGER
    
    db.session.commit()
    
    # Notify the user via in-app notification
    notification = Notification(
        user_id=claim.user_id,
        title="Restaurant Claim Approved",
        message=f"Your claim for {restaurant.name} has been approved! You can now manage this restaurant."
    )
    db.session.add(notification)
    db.session.commit() # Commit notification separately or after email
    
    # Send email notification to the user
    subject = f"Your claim for {restaurant.name} has been approved!"
    body = f"""
    Hello {user.username},
    
    Good news! Your claim to manage the restaurant '{restaurant.name}' on What2Eat@UM has been approved by an administrator.
    
    You can now manage the restaurant's details, photos, business hours, and post promotions.
    
    Manage your restaurant here: {url_for('manage_restaurant', restaurant_id=restaurant.restaurant_id, _external=True)}
    
    Best regards,
    The What2Eat@UM Team
    """
    send_email(subject, [user.email], body)
    
    flash('Claim approved successfully. Restaurant ownership has been transferred.', 'success')
    return redirect(url_for('admin_restaurant_claims'))

@app.route('/admin/restaurant-claims/<int:claim_id>/reject', methods=['POST'])
@admin_required
def admin_reject_claim(claim_id):
    claim = RestaurantClaim.query.get_or_404(claim_id)
    
    # Check if claim is not already processed
    if claim.status != 'pending':
        flash('This claim has already been processed.', 'warning')
        return redirect(url_for('admin_restaurant_claims'))
    
    # Get the restaurant for notification
    restaurant = Restaurant.query.get(claim.restaurant_id)
    
    if not restaurant:
        flash('Restaurant not found.', 'danger')
        return redirect(url_for('admin_restaurant_claims'))
    
    # Update the claim
    claim.status = 'rejected'
    claim.processed_at = datetime.utcnow()
    claim.processed_by = current_user.user_id
    claim.notes = request.form.get('notes', '')
    
    db.session.commit()
    
    # Notify the user
    notification = Notification(
        user_id=claim.user_id,
        title="Restaurant Claim Rejected",
        message=f"Your claim for {restaurant.name} has been rejected. Reason: {claim.notes}"
    )
    db.session.add(notification)
    db.session.commit()
    
    flash('Claim rejected successfully.', 'success')
    return redirect(url_for('admin_restaurant_claims'))

@app.route('/admin/restaurant-claims/<int:claim_id>/document')
@admin_required
def download_proof_document(claim_id):
    claim = RestaurantClaim.query.get_or_404(claim_id)
    
    if not claim.proof_document:
        flash('Document not found.', 'danger')
        return redirect(url_for('admin_restaurant_claims'))
    
    # Get the directory and filename
    directory = os.path.dirname(claim.proof_document)
    filename = os.path.basename(claim.proof_document)
    
    return send_from_directory(os.path.join(app.config['UPLOAD_FOLDER'], directory), filename)

# Restaurant manager route to edit their restaurant
@app.route('/restaurant/<int:restaurant_id>/manage', methods=['GET', 'POST'])
@login_required
def manage_restaurant(restaurant_id):
    restaurant = Restaurant.query.get_or_404(restaurant_id)
    
    # Check if the current user is the manager of this restaurant
    if restaurant.manager_id != current_user.user_id and current_user.role != UserRole.ADMIN:
        flash('You do not have permission to manage this restaurant.', 'danger')
        return redirect(url_for('restaurant_detail', restaurant_id=restaurant_id))
    
    if request.method == 'POST':
        # Get form data
        restaurant.name = request.form.get('name')
        restaurant.location = request.form.get('location')
        restaurant.address = request.form.get('address')
        restaurant.cuisine_type = getattr(CuisineType, request.form.get('cuisine_type', 'OTHER'))
        restaurant.description = request.form.get('description')
        
        # Validate the form
        if not all([restaurant.name, restaurant.location, restaurant.address]):
            flash('Required fields are missing.', 'danger')
            return redirect(url_for('manage_restaurant', restaurant_id=restaurant_id))
        
        # Handle business hours
        # First, delete existing hours
        BusinessHour.query.filter_by(restaurant_id=restaurant_id).delete()
        
        # Then add new hours
        days = request.form.getlist('day_of_week')
        open_times = request.form.getlist('open_time')
        close_times = request.form.getlist('close_time')
        
        for i in range(len(days)):
            if days[i] and open_times[i] and close_times[i]:
                try:
                    business_hour = BusinessHour(
                        restaurant_id=restaurant_id,
                        day_of_week=int(days[i]),
                        open_time=datetime.strptime(open_times[i], '%H:%M').time(),
                        close_time=datetime.strptime(close_times[i], '%H:%M').time()
                    )
                    db.session.add(business_hour)
                except ValueError:
                    flash(f'Invalid time format for day {days[i]}', 'danger')
        
        # Handle restaurant photos
        if 'photos' in request.files:
            photos = request.files.getlist('photos')
            for photo in photos:
                if photo and photo.filename and allowed_file(photo.filename):
                    # Save the image
                    file_path = save_image(photo, 'restaurants')
                    if file_path:
                        restaurant_photo = RestaurantPhoto(
                            restaurant_id=restaurant_id,
                            file_path=file_path,
                            uploaded_by=current_user.user_id,
                            is_approved=True  # Manager uploads are auto-approved
                        )
                        db.session.add(restaurant_photo)
        
        db.session.commit()
        flash('Restaurant updated successfully.', 'success')
        return redirect(url_for('restaurant_detail', restaurant_id=restaurant_id))
    
    # Prepare current business hours for the template
    business_hours = BusinessHour.query.filter_by(restaurant_id=restaurant_id).all()
    
    return render_template('manage_restaurant.html', 
                          restaurant=restaurant,
                          business_hours=business_hours,
                          cuisine_types=CuisineType)

# Helper function to check restaurant manager permission
def check_manager_permission(restaurant_id):
    restaurant = Restaurant.query.get_or_404(restaurant_id)
    if not current_user.is_authenticated or \
       (current_user.user_id != restaurant.manager_id and current_user.role != UserRole.ADMIN):
        flash('You do not have permission to manage promotions for this restaurant.', 'danger')
        raise Forbidden()
    return restaurant

# Manage promotions route (GET to display, POST to add)
@app.route('/restaurant/<int:restaurant_id>/manage/promotions', methods=['GET', 'POST'])
@login_required
def manage_promotions(restaurant_id):
    try:
        restaurant = check_manager_permission(restaurant_id)
    except Forbidden:
        return redirect(url_for('restaurant_detail', restaurant_id=restaurant_id))
    
    if request.method == 'POST':
        # Handle adding a new promotion
        title = request.form.get('title')
        description = request.form.get('description')
        start_date_str = request.form.get('start_date')
        end_date_str = request.form.get('end_date')
        
        if not all([title, description, start_date_str, end_date_str]):
            flash('All promotion fields (except image) are required.', 'danger')
            return redirect(url_for('manage_promotions', restaurant_id=restaurant_id))
        
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%dT%H:%M')
            end_date = datetime.strptime(end_date_str, '%Y-%m-%dT%H:%M')
        except ValueError:
            flash('Invalid date format.', 'danger')
            return redirect(url_for('manage_promotions', restaurant_id=restaurant_id))

        if end_date <= start_date:
            flash('End date must be after start date.', 'danger')
            return redirect(url_for('manage_promotions', restaurant_id=restaurant_id))

        # Handle image upload
        image_path = None
        if 'image' in request.files:
            image_file = request.files['image']
            if image_file and image_file.filename:
                # Save the image to static/uploads/promotions
                image_path = save_image(image_file, 'promotions')
                if not image_path: # Check if save_image returned None due to invalid file type
                     flash('Invalid image file type. Allowed types: png, jpg, jpeg, gif.', 'danger')
                     return redirect(url_for('manage_promotions', restaurant_id=restaurant_id))

        new_promotion = Promotion(
            restaurant_id=restaurant_id,
            title=title,
            description=description,
            start_date=start_date,
            end_date=end_date,
            image_path=image_path, # Use the saved path or None
            created_by=current_user.user_id
        )
        
        db.session.add(new_promotion)
        db.session.commit()
        flash('Promotion added successfully.', 'success')
        return redirect(url_for('manage_promotions', restaurant_id=restaurant_id))

    # GET request: display existing promotions
    promotions = Promotion.query.filter_by(restaurant_id=restaurant_id).order_by(Promotion.start_date.desc()).all()
    return render_template('manage_promotions.html', restaurant=restaurant, promotions=promotions)

# Edit promotion route
@app.route('/promotion/<int:promotion_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_promotion(promotion_id):
    promotion = Promotion.query.get_or_404(promotion_id)
    try:
        # Ensure the user has permission for the promotion's restaurant
        restaurant = check_manager_permission(promotion.restaurant_id)
    except Forbidden:
        return redirect(url_for('restaurant_detail', restaurant_id=promotion.restaurant_id))

    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        start_date_str = request.form.get('start_date')
        end_date_str = request.form.get('end_date')

        if not all([title, description, start_date_str, end_date_str]):
            flash('All promotion fields (except image) are required.', 'danger')
            return redirect(url_for('edit_promotion', promotion_id=promotion_id))

        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%dT%H:%M')
            end_date = datetime.strptime(end_date_str, '%Y-%m-%dT%H:%M')
        except ValueError:
            flash('Invalid date format.', 'danger')
            return redirect(url_for('edit_promotion', promotion_id=promotion_id))
        
        if end_date <= start_date:
             flash('End date must be after start date.', 'danger')
             return redirect(url_for('edit_promotion', promotion_id=promotion_id))

        # Handle image upload (replace if new one is provided)
        if 'image' in request.files:
            image_file = request.files['image']
            if image_file and image_file.filename:
                # Delete old image if it exists
                if promotion.image_path:
                    old_file_path = os.path.join(app.config['UPLOAD_FOLDER'], promotion.image_path)
                    if os.path.exists(old_file_path):
                        os.remove(old_file_path)
                
                # Save the new image
                new_image_path = save_image(image_file, 'promotions')
                if new_image_path:
                    promotion.image_path = new_image_path
                else: # Check if save_image returned None due to invalid file type
                     flash('Invalid image file type. Allowed types: png, jpg, jpeg, gif.', 'danger')
                     return redirect(url_for('edit_promotion', promotion_id=promotion_id))
        
        promotion.title = title
        promotion.description = description
        promotion.start_date = start_date
        promotion.end_date = end_date
        
        db.session.commit()
        flash('Promotion updated successfully.', 'success')
        return redirect(url_for('manage_promotions', restaurant_id=promotion.restaurant_id))

    # GET request
    return render_template('edit_promotion.html', promotion=promotion)

# Delete promotion route
@app.route('/promotion/<int:promotion_id>/delete', methods=['POST'])
@login_required
def delete_promotion(promotion_id):
    promotion = Promotion.query.get_or_404(promotion_id)
    restaurant_id = promotion.restaurant_id # Store before potentially deleting
    try:
        # Ensure the user has permission for the promotion's restaurant
        check_manager_permission(restaurant_id)
    except Forbidden:
        return redirect(url_for('restaurant_detail', restaurant_id=restaurant_id))

    # Delete image file if it exists
    if promotion.image_path:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], promotion.image_path)
        if os.path.exists(file_path):
            os.remove(file_path)
            
    db.session.delete(promotion)
    db.session.commit()
    flash('Promotion deleted successfully.', 'success')
    return redirect(url_for('manage_promotions', restaurant_id=restaurant_id))

if __name__ == "__main__":
    with app.app_context():
        # Create tables if they don't exist
        db.create_all()
        
        # Create admin user if it doesn't exist
        admin_email = 'what2eatatum@gmail.com'
        admin = User.query.filter_by(email=admin_email).first()
        if not admin:
            admin = User(
                user_id=secrets.token_hex(16),
                username='Admin',
                email=admin_email,
                password=generate_password_hash(admin_email),  # Using email as password as specified
                role=UserRole.ADMIN,
                created_at=datetime.utcnow(),
                is_email_verified=True  # Ensure admin is verified
            )
            db.session.add(admin)
            db.session.commit()
            print(f"Admin user created: {admin_email}")
        elif not admin.is_email_verified:
            # Ensure existing admin is verified
            admin.is_email_verified = True
            db.session.commit()
            print(f"Admin user verification updated: {admin_email}")
            
        # Set all existing users as verified for migration
        users_updated = 0
        for user in User.query.filter_by(is_email_verified=False).all():
            user.is_email_verified = True
            users_updated += 1
        if users_updated > 0:
            db.session.commit()
            print(f"Updated {users_updated} existing users to verified status")       
    


