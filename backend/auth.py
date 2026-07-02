import os
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

# ✅ Set up absolute path for database
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_DIR = os.path.join(BASE_DIR, "db")
DB_PATH = os.path.join(DB_DIR, "users.db")

# ---------------------- DATABASE CONNECTION ---------------------- #
def _connect():
    """Establish SQLite connection (auto-creates /db folder if missing)."""
    os.makedirs(DB_DIR, exist_ok=True)
    return sqlite3.connect(DB_PATH, timeout=30)

# ---------------------- INITIALIZE DATABASE ---------------------- #
def init_db():
    """Creates the necessary tables if they don't exist."""
    conn = _connect()
    cur = conn.cursor()

    # Users table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        );
    """)

    # Predictions table (optional: stores all user predictions)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            emotion TEXT,
            text_input TEXT,
            stress_level TEXT,
            confidence REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        );
    """)

    conn.commit()
    conn.close()
    print(f"✅ Database initialized at: {DB_PATH}")

# ---------------------- USER REGISTRATION ---------------------- #
def register_user(username: str, password: str):
    """Registers a new user with a hashed password."""
    try:
        if not username or not password:
            return False, "Username and password are required."

        # ✅ Hash the password before storing
        hashed_pw = generate_password_hash(password)

        conn = _connect()
        cur = conn.cursor()
        cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_pw))
        conn.commit()
        conn.close()

        print(f"🟢 Registered new user: {username}")
        return True, "User registered successfully."

    except sqlite3.IntegrityError:
        # Unique constraint failed (username exists)
        print(f"⚠️ Username '{username}' already exists.")
        return False, "Username already exists."

    except Exception as e:
        print(f"❌ Error during registration: {e}")
        return False, "Internal server error."

# ---------------------- USER LOGIN ---------------------- #
def login_user(username: str, password: str) -> bool:
    """Checks if user credentials are valid."""
    try:
        conn = _connect()
        cur = conn.cursor()
        cur.execute("SELECT password FROM users WHERE username = ?", (username,))
        row = cur.fetchone()
        conn.close()

        # No user found
        if not row:
            print(f"🔴 No user found with username: {username}")
            return False

        stored_hash = row[0]
        is_valid = check_password_hash(stored_hash, password)
        print(f"🟢 Login attempt for '{username}' — {'SUCCESS' if is_valid else 'FAILED'}")
        return is_valid

    except Exception as e:
        print(f"❌ Login error: {e}")
        return False
