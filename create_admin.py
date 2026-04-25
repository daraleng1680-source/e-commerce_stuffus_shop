#!/usr/bin/env python
from app import app
from extensions import db
from model import User
from werkzeug.security import generate_password_hash

with app.app_context():
    # Check if user exists
    user = User.query.filter_by(username='admin').first()
    
    if user:
        print("Admin user already exists")
    else:
        # Create new admin user
        password_hash = generate_password_hash('admin123')
        new_user = User(
            username='admin',
            password=password_hash,
            profile='admin.jpg'
        )
        db.session.add(new_user)
        db.session.commit()
        print("Admin user created successfully!")
        print("Username: admin")
        print("Password: admin123")
