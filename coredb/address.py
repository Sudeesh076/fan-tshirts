from coredb.init import get_db_connection
from helpers.address import Address


def add_address(address):
    try:
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute('''
            INSERT INTO address (id, user_id, street, state, zip, country,type)
            VALUES (?, ?, ?, ?, ?, ?,?)
        ''', (address.id, address.user_id, address.street, address.state, address.zip, address.country,address.type))
        db.commit()
        db.close()
        return address

    except Exception as e:
        db.rollback()
        raise ValueError(f'Error while adding address: {str(e)}')

def delete_address(address_id):
    try:
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute('''
            DELETE FROM address WHERE id = ?
        ''', (address_id,))
        db.commit()
        db.close()
        return "Address is Deleted"

    except Exception as e:
        raise ValueError(f'Error while deleting address: {str(e)}')



def get_addresses_by_user_id(user_id):
    try:
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute('''
            SELECT id, user_id, street, state, zip, country, type
            FROM address
            WHERE user_id = ?
        ''', (user_id,))

        records =  cursor.fetchall()
        db.close()
        return [Address(*result).to_dict() for result in records]

    except Exception as e:
        raise ValueError(f'Error while fetching addresses: {str(e)}')

