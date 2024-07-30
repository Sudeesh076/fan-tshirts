from coredb.init import get_db_connection
from typing import Optional
from helpers.Products import Product, ProductFilters


def add_product(product):
    try:
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute('''
            INSERT INTO products (id, name, description, colour, type, images_location, price)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (product.id, product.name, product.description, product.colour, product.type, product.images_location, product.price))
        db.commit()
        db.close()
        return product

    except Exception as e:
        db.rollback()
        raise ValueError(f'Error while adding product: {str(e)}')

def delete_product(product_id):
    try:
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute('''
            DELETE FROM products WHERE id = ?
        ''', (product_id,))
        db.commit()
        db.close()
        return "Product is Deleted"

    except Exception as e:
        db.rollback()
        db.close()
        raise ValueError(f'Error while deleting product: {str(e)}')



def fetch_products(filters: Optional[ProductFilters] = None):
    db = get_db_connection()
    cursor = db.cursor()

    base_query = 'SELECT id, name, description, colour, type, images_location, price FROM products'

    conditions = []
    params = []

    if filters:
        if filters.colours:
            conditions.append('colour IN ({})'.format(','.join(['?']*len(filters.colours))))
            params.extend(filters.colours)

        if filters.types:
            conditions.append('type IN ({})'.format(','.join(['?']*len(filters.types))))
            params.extend(filters.types)

        if filters.price_range[0] and filters.price_range[1]:
            min_price, max_price = filters.price_range
            conditions.append('price BETWEEN ? AND ?')
            params.extend([min_price, max_price])

        if filters.ids:
            conditions.append('id IN ({})'.format(','.join(['?']*len(filters.ids))))
            params.extend(filters.ids)

    if conditions:
        query = '{} WHERE {}'.format(base_query, ' AND '.join(conditions))
    else:
        query = base_query

    cursor.execute(query, tuple(params))
    results = cursor.fetchall()

    db.close()

    return [Product(*result).to_dict() for result in results]
