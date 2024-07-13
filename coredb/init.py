import sqlite3

DATABASE = 'fan_tshirts.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    return conn

def startDb():
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")
    create_users_table(cursor)
    create_admins_table(cursor)
    create_products_table(cursor)
    db.commit()
    db.close()


def create_users_table(cursor):
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
    table_exists = cursor.fetchone()

    if table_exists:
        cursor.execute("DROP TABLE users")

    cursor.execute('''CREATE TABLE users (
        id TEXT PRIMARY KEY,
        email TEXT UNIQUE,
        password TEXT,
        first_name TEXT,
        last_name TEXT,
        phone_number TEXT
    )''')


def create_admins_table(cursor):
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='admins'")
    table_exists = cursor.fetchone()

    if table_exists:
        cursor.execute("DROP TABLE admins")

    cursor.execute('''CREATE TABLE admins (
        id TEXT PRIMARY KEY,
        email TEXT UNIQUE,
        password TEXT,
        first_name TEXT,
        last_name TEXT,
        phone_number REAL
    )''')


def create_products_table(cursor):
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='products'")
    table_exists = cursor.fetchone()

    if table_exists:
        cursor.execute("DROP TABLE products")

    cursor.execute('''CREATE TABLE products (
        id TEXT PRIMARY KEY,
        name TEXT,
        description TEXT,
        colour TEXT,
        type TEXT,
        images_location TEXT,
        price 
    )''')
