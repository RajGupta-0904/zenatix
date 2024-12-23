# Blog Post Management System API

A Django REST API for managing blog posts with user roles (Admin and Blogger).

## Features

- User Authentication with JWT
- Role-based access control (Admin and Blogger)
- Blog post management
- Categories and Tags
- Comments system
- Search and filtering capabilities

## Setup and Installation

1. Clone the repository
2. Create and activate virtual environment
python -m venv authenv

3. Install dependencies
pip install -r requirements.txt

4. Apply migrations:
python manage.py makemigrations
python manage.py migrate


5. Create superuser:
python manage.py createsuperuser

6. Run server:
python manage.py runserver


