import sqlite3
import os
import hashlib

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, '..', 'data', 'leetcode.db')
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    return conn

def hash_pw(password: str) -> str:
    # Simple SHA-256 for demo - for production use bcrypt!
    return hashlib.sha256(password.encode()).hexdigest()

def initialize_db():
    conn = get_connection()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password_hash TEXT NOT NULL
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS problems (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            problem_id INTEGER,
            title TEXT NOT NULL,
            slug TEXT NOT NULL,
            timestamp TEXT,
            pattern TEXT,
            notes TEXT,
            confidence INTEGER CHECK(confidence >= 0 AND confidence <= 5) DEFAULT 0,
            UNIQUE(username, slug),
            FOREIGN KEY (username) REFERENCES users(username)
        )
    ''')
    conn.commit()
    conn.close()

# --- User Management ---
def register_user(username, password):
    conn = get_connection()
    c = conn.cursor()
    try:
        c.execute(
            'INSERT INTO users (username, password_hash) VALUES (?, ?)',
            (username, hash_pw(password))
        )
        conn.commit()
        conn.close()
        return True, "Registration successful!"
    except sqlite3.IntegrityError:
        conn.close()
        return False, "Username already exists."

def check_login(username, password):
    conn = get_connection()
    c = conn.cursor()
    c.execute(
        'SELECT password_hash FROM users WHERE username=?', (username,)
    )
    row = c.fetchone()
    conn.close()
    if not row:
        return False
    return hash_pw(password) == row[0]

# --- Problem CRUD ---
def problem_exists(username, slug):
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT 1 FROM problems WHERE username=? AND slug=?', (username, slug))
    exists = c.fetchone() is not None
    conn.close()
    return exists

def add_problem(username, title, slug, problem_id=None, timestamp=None, notes='', confidence=0, pattern=''):
    if confidence < 0 or confidence > 5:
        print(f"Error: Confidence value {confidence} is out of range (0-5).")
        return
    try:
        conn = get_connection()
        with conn:
            conn.execute('''
                INSERT INTO problems (username, title, slug, problem_id, timestamp, notes, confidence, pattern)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (username, title, slug, problem_id, timestamp, notes, confidence, pattern))
        conn.close()
        return True
    except sqlite3.IntegrityError:
        print(f"Problem with slug '{slug}' for '{username}' already exists. Skipping insert.")
        return False

def get_all_problems(username):
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM problems WHERE username=?', (username,))
    rows = c.fetchall()
    conn.close()
    return rows

def update_problem_confidence(username, slug, pattern, notes, confidence):
    conn = get_connection()
    c = conn.cursor()
    c.execute('''
        UPDATE problems
        SET pattern=?, notes=?, confidence=?
        WHERE username=? AND slug=?
    ''', (pattern, notes, confidence, username, slug))
    conn.commit()
    conn.close()

def delete_problem(username, slug):
    conn = get_connection()
    c = conn.cursor()
    c.execute('DELETE FROM problems WHERE username=? AND slug=?', (username, slug))
    conn.commit()
    conn.close()

def search_problems_by_pattern(username, pattern):
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM problems WHERE username=? AND pattern=?', (username, pattern))
    rows = c.fetchall()
    conn.close()
    return rows

def search_problems_by_title(username, keyword):
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM problems WHERE username=? AND title LIKE ?', (username, f'%{keyword}%'))
    rows = c.fetchall()
    conn.close()
    return rows

def search_problems_by_confidence(username, confidence):
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM problems WHERE username=? AND confidence=?', (username, confidence))
    rows = c.fetchall()
    conn.close()
    return rows

if __name__ == "__main__":
    initialize_db()