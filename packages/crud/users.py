import sqlite3
import bcrypt

DB_PATH = 'aid_academy.db'

def get_all_users():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        SELECT u.id, u.username, r.name as role
        FROM users u
        JOIN roles r ON u.role_id = r.id
        ORDER BY u.id
    ''')
    users = c.fetchall()
    conn.close()
    return users

def get_all_roles():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT id, name FROM roles')
    roles = c.fetchall()
    conn.close()
    return roles

def create_user(username, password, role_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    try:
        c.execute('INSERT INTO users (username, password, role_id) VALUES (?, ?, ?)', (username, hashed, role_id))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        conn.close()
        return False

def update_user(user_id, username, password, role_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    if password:
        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        c.execute('UPDATE users SET username=?, password=?, role_id=? WHERE id=?', (username, hashed, role_id, user_id))
    else:
        c.execute('UPDATE users SET username=?, role_id=? WHERE id=?', (username, role_id, user_id))
    conn.commit()
    conn.close()

def delete_user(user_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('DELETE FROM users WHERE id=?', (user_id,))
    conn.commit()
    conn.close()
