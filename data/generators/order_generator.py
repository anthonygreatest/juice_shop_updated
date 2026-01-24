import random

from data.constants2 import NEW_PRODUCTS



def order_generator(basket_id):

    products = [
        x for x in NEW_PRODUCTS
        if x['quantity'] > 1 and 'name' in x and (x['limit_per_user'] is None or x['limit_per_user'] >= 1)
    ]
    product = random.choice(products)
    if not products:
        raise ValueError("Нет товаров в наличии!")
        # products = list(filter(lambda x: x['quantity'] > 0, PRODUCTS_LIST))
        # product = random.choice(products)

    return {
        'product_id': product['id'],
        'quantity': 1,
        'basket_id': basket_id
    }

def pick_product_to_purchase(available):

    if available == 'one_left' or available == 'expensive_product':
        products = [
            x for x in NEW_PRODUCTS if x['quantity'] == 1 and 'name' in x
        ]

    elif not available:
        products = [
            x for x in NEW_PRODUCTS if x['quantity'] == 0 and 'name' in x
        ]

    elif available == 'sale':
        products = [
            x for x in NEW_PRODUCTS if x['id'] == 1 or x['id'] == 5
        ]
    else:
        products = [
            x for x in NEW_PRODUCTS
            if x['quantity'] > 1 and (x['limit_per_user'] is None or x['limit_per_user'] >= 1) \
            and x.get('name')
        ]
    product = random.choice(products)

    return product['name']