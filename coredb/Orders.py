from datetime import datetime
from coredb.init import get_db_connection
import uuid

def add_order(order):
    try:
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute('''
            INSERT INTO orders (id, user_id, payment_method, address_id)
            VALUES (?, ?, ?, ?)
        ''', (order.id, order.user_id, order.payment_method, order.address_id))
        db.commit()
        db.close()
        return order

    except Exception as e:
        db.rollback()
        raise ValueError(f'Error while adding order: {str(e)}')

def add_order_item(items):
    try:
        db = get_db_connection()
        cursor = db.cursor()

        for item in items:
            cursor.execute('''
                INSERT INTO order_items (id, order_id, user_id, product_id)
                VALUES (?, ?, ?, ?)
            ''', (item.id, item.order_id, item.user_id, item.product_id))

        db.commit()
        db.close()

        return items

    except Exception as e:
        db.rollback()
        raise ValueError(f'Error while adding order items: {str(e)}')

def add_order_track(tracks):
    try:
        db = get_db_connection()
        cursor = db.cursor()

        for track in tracks:
            cursor.execute('''
                INSERT INTO order_track (id, order_id, order_item_id, user_id, product_id, status, Time)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (track.id, track.order_id, track.order_item_id, track.user_id, track.product_id, track.status, track.Time))

        db.commit()
        db.close()

        return tracks

    except Exception as e:
        db.rollback()
        raise ValueError(f'Error while adding order tracks: {str(e)}')

def add_old_order_track(order_item_id, status):
    try:
        db = get_db_connection()
        cursor = db.cursor()

        cursor.execute('''
            SELECT id, order_id, order_item_id, user_id, product_id, status, Time
            FROM order_track
            WHERE order_item_id = ?
            ORDER BY Time DESC
            LIMIT 1
        ''', (order_item_id,))

        latest_record = cursor.fetchone()

        if latest_record:
            new_status = status
            new_time = datetime.now().strftime('%d/%m/%Y %H:%M')

            # Generate a new UUID for the new record
            new_id = str(uuid.uuid4())

            # Insert a new record based on the latest record found
            cursor.execute('''
                INSERT INTO order_track (id, order_id, order_item_id, user_id, product_id, status, Time)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (new_id, latest_record[1], latest_record[2], latest_record[3], latest_record[4], new_status, new_time))

            db.commit()
            db.close()

            return "Status order_track record added successfully."

        else:
            db.close()
            return "No existing record found for the given order_item_id."

    except Exception as e:
        return f"Error: {str(e)}"

from collections import defaultdict

def get_orders(user_id=None, order_id=None):
    try:
        db = get_db_connection()
        cursor = db.cursor()

        base_query = '''
            SELECT o.id as order_id, o.user_id, o.payment_method, o.address_id,
                   a.street, a.state, a.zip, a.country, a.type as address_type,
                   oi.id as order_item_id, oi.product_id,
                   p.name as product_name, p.description as product_description, p.colour as product_colour,
                   ot.id as order_track_id, ot.status, ot.Time,
                   u.id, u.email, u.first_name, u.last_name, u.phone_number ,  p.images_location as images_location
            FROM orders o
            JOIN order_items oi ON o.id = oi.order_id
            JOIN (
                SELECT *
                FROM order_track
                ORDER BY Time DESC
            ) ot ON oi.id = ot.order_item_id
            LEFT JOIN products p ON oi.product_id = p.id
            LEFT JOIN address a ON o.address_id = a.id
            LEFT JOIN users u ON o.user_id = u.id
        '''

        where_clause = ''
        params = ()

        if user_id:
            where_clause = 'WHERE o.user_id = ?'
            params = (user_id,)
        elif order_id:
            where_clause = 'WHERE o.id = ?'
            params = (order_id,)

        order = "ORDER BY ot.Time DESC, ot.id DESC"  # Sort orders by latest tracking time

        final_query = base_query + ' ' + where_clause + ' ' + order
        cursor.execute(final_query, params)

        rows = cursor.fetchall()
        orders_dict = defaultdict(lambda: {
            'items': []
        })

        for row in rows:
            order_id = row[0]
            orders_dict[order_id]['id'] = row[0]
            orders_dict[order_id]['user'] = {
                'user_id':  row[17],
                'email': row[18],
                'first_name': row[19],
                'last_name': row[20],
                'phone_number': row[21],
            }
            orders_dict[order_id]['payment_method'] = row[2]
            orders_dict[order_id]['address'] = {
                'address_id': row[3],
                'street': row[4],
                'state': row[5],
                'zip': row[6],
                'country': row[7],
                'type': row[8]
            }

            items_list = orders_dict[order_id]['items']
            item_found = False
            for item in items_list:
                if item['order_item_id'] == row[9]:
                    item['tracks'].append({
                        'order_track_id': row[14],
                        'status': row[15],
                        'Time': row[16]
                    })
                    item_found = True
                    break

            if not item_found:
                items_list.append({
                    'order_item_id': row[9],
                    'product': {
                        'product_id': row[10],
                        'name': row[11],
                        'description': row[12],
                        'colour': row[13],
                        'images_location' : row[22],
                    },
                    'tracks': [{
                        'order_track_id': row[14],
                        'status': row[15],
                        'Time': row[16]
                    }]
                })

        db.close()

        orders_list = list(orders_dict.values())

        for order in orders_list:
            for item in order['items']:
                item['tracks'] = sorted(item['tracks'], key=lambda x: x['Time'], reverse=True)

        orders_list = sorted(orders_list, key=lambda x: x['items'][0]['tracks'][0]['Time'], reverse=True)

        return orders_list

    except Exception as e:
        raise ValueError(f'Error while fetching orders: {str(e)}')


