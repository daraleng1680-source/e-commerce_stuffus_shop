#!/usr/bin/env python
from app import app, db, User
from werkzeug.security import check_password_hash, generate_password_hash

with app.app_context():
    # Check if user exists
    user = User.query.filter_by(username='mann').first()
    
    if user:
        print(f"User found: {user.username}")
        print(f"Password hash: {user.password}")
        print(f"Password hash type: {type(user.password)}")
        
        # Test password verification
        test_password = "123456"
        print(f"\nTesting password: {test_password}")
        
        try:
            hash_check = check_password_hash(user.password, test_password)
            print(f"Hash check result: {hash_check}")
        except Exception as e:
            print(f"Hash check error: {e}")
        
        # Test plaintext
        plaintext_check = user.password == test_password
        print(f"Plaintext check result: {plaintext_check}")
        
        print(f"\nUser profile: {user.profile}")
        print(f"User ID: {user.id}")
    else:
        print("User 'mann' not found in database")
        print(f"All users: {User.query.all()}")
