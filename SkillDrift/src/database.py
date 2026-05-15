import sqlite3
import os
import bcrypt
import pandas as pd

def create_connection():
    if not os.path.exists('data'):
        os.makedirs('data')
    return sqlite3.connect('data/users.db', check_same_thread=False)

def create_tables():
    conn = create_connection()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users 
                 (username TEXT UNIQUE, email TEXT UNIQUE, password TEXT, 
                  full_name TEXT, college_id TEXT, year TEXT, bio TEXT)''')
    
    # Migration: Add missing columns if table already exists
    try:
        c.execute("ALTER TABLE users ADD COLUMN full_name TEXT")
    except sqlite3.OperationalError:
        pass # Column already exists
    
    try:
        c.execute("ALTER TABLE users ADD COLUMN college_id TEXT")
    except sqlite3.OperationalError:
        pass
        
    try:
        c.execute("ALTER TABLE users ADD COLUMN year TEXT")
    except sqlite3.OperationalError:
        pass
        
    try:
        c.execute("ALTER TABLE users ADD COLUMN bio TEXT")
    except sqlite3.OperationalError:
        pass

    c.execute('''CREATE TABLE IF NOT EXISTS scores 
                 (username TEXT, domain TEXT, score REAL, status TEXT, 
                  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

def add_user(username, email, password):
    conn = create_connection()
    c = conn.cursor()
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    try:
        c.execute('INSERT INTO users (username, email, password) VALUES (?,?,?)', (username, email, hashed))
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()

def login_user_db(email, password):
    conn = create_connection()
    c = conn.cursor()
    c.execute('SELECT username, password FROM users WHERE email=?', (email,))
    user = c.fetchone()
    conn.close()
    if user and bcrypt.checkpw(password.encode(), user[1].encode()):
        return user[0]
    return None

def update_password(email, new_password):
    conn = create_connection()
    c = conn.cursor()
    hashed = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()
    c.execute('UPDATE users SET password=? WHERE email=?', (hashed, email))
    conn.commit()
    rows = c.rowcount
    conn.close()
    return rows > 0

def update_user_profile(username, full_name, college_id, year, bio):
    conn = create_connection()
    c = conn.cursor()
    c.execute('''UPDATE users SET full_name=?, college_id=?, year=?, bio=? 
                 WHERE username=?''', (full_name, college_id, year, bio, username))
    conn.commit()
    conn.close()

def get_user_data(username):
    conn = create_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE username=?', (username,))
    data = c.fetchone()
    conn.close()
    return data

def save_score(user, domain, score, status):
    conn = create_connection()
    c = conn.cursor()
    c.execute('INSERT INTO scores (username, domain, score, status) VALUES (?,?,?,?)', (user, domain, score, status))
    conn.commit()
    conn.close()

def get_user_scores(user):
    conn = create_connection()
    df = pd.read_sql(f"SELECT * FROM scores WHERE username='{user}'", conn)
    conn.close()
    return df
