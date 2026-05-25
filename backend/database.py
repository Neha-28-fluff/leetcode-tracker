import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, '..', 'data', 'leetcode.db')

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    return conn

def initialize_db():
    conn = get_connection()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS problems (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            problem_id INTEGER,
            title TEXT NOT NULL,
            slug TEXT NOT NULL UNIQUE,
            timestamp TEXT,
            pattern TEXT,
            notes TEXT,
            confidence INTEGER CHECK(confidence >= 0 AND confidence <= 5) DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

def problem_exists(slug):
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT 1 FROM problems WHERE slug=?', (slug,))
    exists = c.fetchone() is not None
    conn.close()
    return exists

def add_problem(title, slug, problem_id=None, timestamp=None, notes='', confidence=0, pattern=''):
    if confidence < 0 or confidence > 5:
        print(f"Error: Confidence value {confidence} is out of range (0-5).")
        return
    try:
        conn = get_connection()
        with conn:
            conn.execute('''
                INSERT INTO problems (title, slug, problem_id, timestamp, notes, confidence, pattern)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (title, slug, problem_id, timestamp, notes, confidence, pattern))
        conn.close()
        return True
    except sqlite3.IntegrityError:
        # Unique constraint failed (already exists)
        print(f"Problem with slug '{slug}' already exists. Skipping insert.")
        return False

def get_all_problems():
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM problems')
    rows = c.fetchall()
    conn.close()
    return rows

def update_problem_confidence(slug, pattern,notes, confidence):
    conn = get_connection()
    c = conn.cursor()
    c.execute('''
        UPDATE problems
        SET pattern = ?, notes=?, confidence=?
        WHERE slug=?
    ''', (pattern,notes, confidence, slug))
    conn.commit()
    conn.close()

def delete_problem(slug):
    conn = get_connection()
    c = conn.cursor()
    c.execute('DELETE FROM problems WHERE slug=?', (slug,))
    conn.commit()
    conn.close()

def search_problems_by_pattern(pattern):
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM problems WHERE pattern=?', (pattern,))
    rows = c.fetchall()
    conn.close()
    return rows

def search_problems_by_title(keyword):
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM problems WHERE title LIKE ?', (f'%{keyword}%',))
    rows = c.fetchall()
    conn.close()
    return rows

def search_problems_by_confidence(confidence):
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM problems WHERE confidence=?', (confidence,))
    rows = c.fetchall()
    conn.close()
    return rows

if __name__ == "__main__":
    # Demo/test code (runs only when file is executed directly)
    for row in get_all_problems():
        print(row)