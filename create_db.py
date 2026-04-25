from app import app, db

with app.app_context():
    db.create_all()
    print("Database created successfully!")
    
import sqlite3
conn = sqlite3.connect('instance/app.db')
c = conn.cursor()
c.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = [row[0] for row in c.fetchall()]
print(f"Tables in database: {tables}")
conn.close()
