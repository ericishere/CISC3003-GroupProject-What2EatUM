What2Eat @UM - Web App Specification

# Project Overview:
What2Eat @UM is a web app that provides the University of Macau community (students, staff, and visitors) with an easy-to-navigate platform for finding dining options, viewing restaurant details, and discovering promotions. Restaurant managers can also claim their restaurant listings, post updates, and manage promotions.

# Tech Stack:
- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, Bootstrap, jQuery
- **Database**: MySQL
- **Authentication**: Email + Password (Password reset via email)
- **Media Storage**: Use local storage for any media/photos

# User Types and Authentication

## User Types:
- **General Users** (Students, Staff, Visitors)
- **Restaurant/Canteen Managers**
- **Admin** (Pre-defined account with full platform management capabilities)

## Authentication:
- Users register via email + password
- **General Users**: Can browse, leave reviews, and follow restaurants
- **Restaurant Managers**: Can claim and manage their restaurant profiles (with proof of ownership)
- **Admin**: Pre-defined account with access to review restaurant claims and manage the platform

## Login Process:
- Email + Password authentication
- Password reset functionality via email
- Users can edit or delete their own reviews at any time

# User Profiles
- Minimal functionality focused on user's interaction history
- Users can view their own past reviews and ratings
- No extensive profile customization needed

# Core Features

## Restaurant Profile Page
Each restaurant has a profile with the following sections:

### Basic Info:
- Name + Location (building name or general campus area)
- Address information (map integration optional)
- Business Hours (auto-highlight if open/closed)
- Photos (uploaded by managers, possibly user-submitted but reviewed first)
- Cuisine Type (from pre-defined list)

### Reviews:
- Star rating (1–5)
- Text reviews with options to include photos
- Average rating displayed

### Promotions/Announcements:
- Active promotions posted by the manager (title, description, start/end time, image)
- Red dot indicator in the corner of the restaurant profile to show an active promotion

### Follow Button:
- Subscribe/follow the restaurant for updates and in-app notifications

## Homepage
The homepage displays randomly selected restaurants, each with:
- Restaurant name and location
- One recent review (with the rating and a short comment)
- Red dot if there's an active promotion

## Search, Filtering and Sorting

### Search: 
- Users can search by restaurant name

### Filtering:
- By cuisine type (from pre-defined list)
- By rating range

### Sorting: 
Results can be sorted by:
- Highest Rated
- Promo Active (restaurants with active promotions)

## Notification System
- In-app notification inbox for users
- Notifications sent when followed restaurants post promotions or updates

## Restaurant Claiming and Management (for Managers)
- Managers first sign up as general users
- Once logged in, they can claim an existing restaurant by submitting a request form with their certificate to verify ownership
- Admin reviews and approves restaurant claims
- Once approved, managers get access to manage their restaurant's profile:
  - Post promotions
  - Update business hours
  - Upload photos
  - Update basic information

# Implementation Details

## Database Structure
The database structure is defined in `models.py` and includes the following main entities:
- Users: Stores user accounts with roles and authentication info
- Restaurants: Core entity for dining locations
- Reviews: User feedback on restaurants
- Promotions: Time-limited special offers
- Restaurant Claims: Ownership verification requests
- Notifications: In-app messages to users

## Authentication System
The authentication system includes:
- User registration with email verification
- Secure login with password hashing
- Password reset via email
- Role-based access control

## Email Verification Process
New users must verify their email before accessing their account:
1. User registers and provides email
2. System sends verification code to email
3. User enters code to verify account
4. Upon verification, user gains access to account features

# Setup and Installation

## Prerequisites
- Python 3.10+
- MySQL Server
- SMTP account for sending emails

## Installation Steps

1. Clone the repository:
```
git clone https://github.com/your-repo/what2eat-um.git
cd what2eat-um
```

2. Create and activate a virtual environment:
```
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

3. Install dependencies:
```
pip install -r requirements.txt
```

4. Create a MySQL database named `what2eat_um`

5. Create a `.env` file with the following variables:
```
SECRET_KEY=your_secret_key
DATABASE_URL=mysql+pymysql://username:password@localhost:3306/what2eat_um
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your_email@gmail.com
MAIL_DEFAULT_SENDER=your_email@gmail.com
MAIL_PASSWORD=your_app_password
```

6. Initialize the database:
```
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

7. Run the application:
```
python app.py
```
