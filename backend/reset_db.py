import os, sqlite3

# Build absolute path to your database
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "db", "users.db")

print("📁 Database file:", DB_PATH)

# Recreate the users table
os.makedirs(os.path.join(BASE_DIR, "db"), exist_ok=True)
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()
cursor.execute("DROP TABLE IF EXISTS users;")
cursor.execute("""
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);
""")
conn.commit()
conn.close()
print("✅ Database reset successfully — empty users table ready.")
