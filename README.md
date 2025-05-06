# Finder Service
A Django REST API for connecting businesses with financial experts, featuring user authentication, expert search, quote requests, user preferences, and review management.

## Project Structure

finder-service/

├── backend/               # Project settings and URL routing

├── quote_requests/        # Logic for quote handling & user preferences

├── users/                 # Handles users, authentication, and reviews

├── manage.py              # Django management utility

├── requirements.txt

## Features
- User Registration & JWT Authentication: Businesses and financial experts can register and authenticate securely.

- Profile Management: Users can update profiles with location, expertise, and bio.

- Expert Search: Search and filter experts by location, expertise, and rating.

- Quote Requests: Businesses can request quotes from experts; experts manage incoming requests.

- User Preferences: Save and reuse search preferences.

- Reviews: Businesses can review experts, with rating aggregation and pagination.

## Setup
Clone the repo and install dependencies:

```bash
git clone https://github.com/VyshnaviMulakalapalli/finder-service.git
```

Create a virtual environment and activate it:

```bash
python -m venv venv
```

Activate the virtual environment

```bash
.\venv\Scripts\activate
```

Install the requirements

```bash
pip install -r requirements.txt
```

Configure PostgreSQL in backend/settings.py by adding up your database NAME, USER, and PASSWORD.

Run and apply migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```


Start the server:

```bash
python manage.py runserver
```

## API Overview

### Authentication

- POST /api/users/register/ – Register a new user

- POST /api/users/token/ – Obtain JWT token

### Profile

- GET /api/users/profile/ – Get current profile

- PUT /api/users/update-profile/ – Update profile

### Expert Search

- GET /api/users/search-experts/?location=&expertise=&min_rating= – Search experts

### Quote Requests

- POST /api/quote_requests/ – Create a quote request (business only)

### Reviews

- POST /api/users/submit-review/ – Submit a review

- GET /api/users/expert/<expert_id>/reviews/ – List expert reviews

## Tech Stack
- Django 5.1

- Django REST Framework

- PostgreSQL

- JWT Authentication

## Customization
User Model: Custom user with user_type (business/expert), phone, and email.

Profiles: Extended with expertise, location, and bio.

Permissions: Only businesses can request quotes; only authenticated users can review.

