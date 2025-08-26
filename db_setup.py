import sqlite3

def create_db():
    conn = sqlite3.connect('aid_academy.db')
    c = conn.cursor()

    # Crear tabla de roles
    c.execute('''
        CREATE TABLE IF NOT EXISTS roles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        )
    ''')

    # Crear tabla de usuarios
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role_id INTEGER NOT NULL,
            FOREIGN KEY (role_id) REFERENCES roles(id)
        )
    ''')

    # Insertar roles por defecto si no existen
    roles = ['admin', 'teacher', 'student', 'parent']
    for role in roles:
        c.execute('INSERT OR IGNORE INTO roles (name) VALUES (?)', (role,))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_db()
