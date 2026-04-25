import sqlite3

conn = sqlite3.connect('instance/app.db')
c = conn.cursor()
c.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = [row[0] for row in c.fetchall()]
print('Tables in database:', tables)

# Check user table structure
if 'user' in tables:
    c.execute("PRAGMA table_info(user)")
    columns = c.fetchall()
    print("\nUser table columns:")
    for col in columns:
        print(f"  - {col[1]}: {col[2]}")

conn.close()
