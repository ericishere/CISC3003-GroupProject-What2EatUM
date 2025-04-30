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
