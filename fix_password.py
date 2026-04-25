#!/usr/bin/env python
from app import app, db, User
from werkzeug.security import generate_password_hash

with app.app_context():
    # Generate hash for 123456
    correct_hash = generate_password_hash("123456")
    print(f"Generated hash for '123456': {correct_hash}")
    
    # Update the user
    user = User.query.filter_by(username='mann').first()
    if user:
        user.password = correct_hash
        db.session.commit()
        print(f"Updated user 'mann' with new password hash")
    else:
        print("User not found")
