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
    create_address_table(cursor)
    create_orders_table(cursor)
    create_order_items_table(cursor)
    create_order_track_table(cursor)
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

def create_address_table(cursor) :
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='address'")
    table_exists = cursor.fetchone()

    if table_exists:
        cursor.execute("DROP TABLE address")

    cursor.execute('''CREATE TABLE address (
        id TEXT PRIMARY KEY,
        user_id TEXT,
        street TEXT,
        state TEXT,
        zip TEXT,
        country TEXT,
        type TEXT
    )''')

def create_orders_table(cursor) :
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='orders'")
    table_exists = cursor.fetchone()

    if table_exists:
        cursor.execute("DROP TABLE orders")

    cursor.execute('''CREATE TABLE orders (
        id TEXT PRIMARY KEY,
        user_id TEXT,
        payment_method TEXT,
        address_id TEXT
    )''')

def create_order_items_table(cursor) :
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='order_items'")
    table_exists = cursor.fetchone()

    if table_exists:
        cursor.execute("DROP TABLE order_items")

    cursor.execute('''CREATE TABLE order_items (
        id TEXT PRIMARY KEY,
        order_id TEXT,
        user_id TEXT,
        product_id TEXT
    )''')

def create_order_track_table(cursor) :
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='order_track'")
    table_exists = cursor.fetchone()

    if table_exists:
        cursor.execute("DROP TABLE order_track")

    cursor.execute('''CREATE TABLE order_track (
        id TEXT PRIMARY KEY,
        order_id TEXT,
        order_item_id TEXT,
        user_id TEXT,
        product_id TEXT,
        status TEXT,
        Time TEXT
    )''')
