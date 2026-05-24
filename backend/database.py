import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, '..', 'data', 'leetcode.db')

conn = sqlite3.connect(db_path)
c = conn.cursor()

c.execute('''
    CREATE TABLE IF NOT EXISTS problems (
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        slug TEXT NOT NULL UNIQUE,
        pattern TEXT,
        notes TEXT,
        confidence INTEGER CHECK(confidence >= 0 AND confidence <= 5) DEFAULT 0
    )
''')
conn.commit() # important

def add_problem(title, slug, notes, confidence):
    if confidence < 0 or confidence > 5:
        print(f"Error: Confidence value {confidence} is out of range (0-5).")
        return
    try:
        with conn:
            c.execute('''
                INSERT INTO problems (title, slug, notes, confidence)
                VALUES (?, ?, ?, ?)
            ''', (title, slug, notes, confidence))
    except sqlite3.IntegrityError:
        print(f"Problem with slug '{slug}' already exists. Skipping insert.")

def get_all_problems():
    c.execute('SELECT * FROM problems')
    return c.fetchall()

def update_problem(id, notes, confidence):
    if confidence < 0 or confidence > 5:
        print(f"Error: Confidence value {confidence} is out of range (0-5).")
        return
    with conn:
        c.execute('''
            UPDATE problems
            SET notes = ?, confidence = ?
            WHERE id = ?
        ''', (notes, confidence, id))

def delete_problem(id):
    with conn:
        c.execute('DELETE FROM problems WHERE id = ?', (id,))

def get_problems_by_confidence(level):
    c.execute('SELECT * FROM problems WHERE confidence = ?', (level,))
    return c.fetchall()

# ---------- Testing ----------

# For testing/demo: Clear table so repeat runs work without error
# c.execute('DELETE FROM problems')
# conn.commit()

print("Adding initial problems...")
add_problem('Two Sum', 'two-sum', 'Use a hash map to store indices.', 4)
add_problem('Reverse Linked List', 'reverse-linked-list', 'Iteratively reverse the pointers.', 3)
add_problem('Binary Tree Inorder Traversal', 'binary-tree-inorder-traversal', 'Use a stack to traverse the tree.', 5)
add_problem('Two Sum', 'two-sum', 'Duplicate slug test. Should not insert.', 1)  

print("\nAll problems after insert:")
p = get_all_problems()
for i in p:
    print(i)

print("\nUpdating problem with id=1...")
update_problem(1, 'Use a hash map to store indices for O(n) time complexity.', 5)

print("\nAll problems after update:")
p = get_all_problems()
for i in p:
    print(i)

print("\nDeleting problem with id=2...")
delete_problem(2)

print("\nAll problems after delete:")
p = get_all_problems()
for i in p:
    print(i)

print("\nProblems with confidence = 5:")
pc = get_problems_by_confidence(5)
for i in pc:
    print(i)

add_problem('Merge Intervals', 'merge-intervals', 'Sort intervals and merge overlapping ones.', 8)

# ---------- Testing Over ----------

c.close()
conn.close()