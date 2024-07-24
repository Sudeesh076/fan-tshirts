from helpers.Users import User
from coredb.init import get_db_connection


def validate_unique_email_phone(user):
    db = get_db_connection()
    cursor = db.cursor()

    cursor.execute('SELECT COUNT(*) FROM users WHERE email = ?', (user.email,))
    result = cursor.fetchone()[0]
    email_exists = result > 0

    cursor.execute('SELECT COUNT(*) FROM users WHERE phone_number = ?', (user.phone_number,))
    result = cursor.fetchone()[0]
    phone_exists = result > 0

    db.close()

    if email_exists or phone_exists:
        raise ValueError('Email or phone number already exists in the database.')

    return email_exists, phone_exists


def add_user(user):
    try:
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute('''
            INSERT INTO users (id, email, password, first_name, last_name, phone_number)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (user.id, user.email, user.password, user.first_name, user.last_name, user.phone_number))
        db.commit()
        db.close()
        return user

    except:
        db.rollback()
        raise ValueError('Error While creating User')


def get_user_by_email(email):
    db = get_db_connection()
    cursor = db.cursor()

    cursor.execute('SELECT id, email, password, first_name, last_name, phone_number FROM users WHERE email = ?', (email,))
    result = cursor.fetchone()

    cursor.close()

    if result:
        return User(*result)
    else:
        raise ValueError('Authentication Failed')


def get_admin_by_email(email):
    db = get_db_connection()
    cursor = db.cursor()

    cursor.execute('SELECT id, email, password, first_name, last_name, phone_number FROM admin WHERE email = ?', (email,))
    result = cursor.fetchone()

    cursor.close()

    if result:
        return User(*result)
    else:
        raise ValueError('Authentication Failed')


def get_user_by_id(id):
    db = get_db_connection()
    cursor = db.cursor()

    cursor.execute('SELECT id, email, password, first_name, last_name, phone_number FROM users WHERE id = ?', (id,))
    result = cursor.fetchone()

    db.close()

    if result:
        return User(*result)
    else:
        raise ValueError('Error While finding User')
