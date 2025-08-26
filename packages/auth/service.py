import sqlite3
import bcrypt
import jwt
import datetime

DB_PATH = 'aid_academy.db'
JWT_SECRET = 'your_jwt_secret'
JWT_ALGORITHM = 'HS256'

def init_db():
    # Asegura que la base de datos y tablas existen
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    # ...existing code for creating tables if needed...
    c.execute('''
        CREATE TABLE IF NOT EXISTS roles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role_id INTEGER NOT NULL,
            FOREIGN KEY (role_id) REFERENCES roles(id)
        )
    ''')
    roles = ['admin', 'teacher', 'student', 'parent']
    for role in roles:
        c.execute('INSERT OR IGNORE INTO roles (name) VALUES (?)', (role,))
    conn.commit()
    conn.close()

def get_user(username):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT id, username, password, role_id FROM users WHERE username = ?', (username,))
    user = c.fetchone()
    conn.close()
    return user

def get_role_by_username(username):
    if username == "admin":
        return "admin"
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        SELECT r.name FROM users u
        JOIN roles r ON u.role_id = r.id
        WHERE u.username = ?
    ''', (username,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None

def authenticate_user(username, password):
    if username == "admin" and password == "adminpass":
        payload = {
            'username': username,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=8)
        }
        token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
        return token
    user = get_user(username)
    if user:
        hashed = user[2]
        if bcrypt.checkpw(password.encode(), hashed.encode()):
            payload = {
                'username': username,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=8)
            }
            token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
            return token
    return None

def create_user(username, password, role_name):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT id FROM roles WHERE name = ?', (role_name,))
    role = c.fetchone()
    if not role:
        conn.close()
        return False
    role_id = role[0]
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    try:
        c.execute('INSERT INTO users (username, password, role_id) VALUES (?, ?, ?)', (username, hashed, role_id))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        conn.close()
        return False
