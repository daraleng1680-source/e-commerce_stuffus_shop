import sqlite3

def update_db():
    conn = sqlite3.connect('instance/app.db')
    cursor = conn.cursor()
    try:
        cursor.execute("ALTER TABLE customers ADD COLUMN password VARCHAR(255)")
        print("Column added successfully")
    except sqlite3.OperationalError as e:
        print("Error:", e)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    update_db()
