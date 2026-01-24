


class BasketLocators:

    products_in_basket = "mat-table"
    random_product_in_basket = 'mat-row'
    item_quantity_btn = 'mat-cell button.mat-mdc-icon-button'
    notification_basket = 'button[aria-label="Show the shopping cart"] span.fa-layers-counter'
    product_info = 'mat-cell'
    price = 'mat-row mat-cell'
    total_price = 'div#price'

    plus_one_btn = 'button[data-icon="plus-square"]'
    minus_one_btn = 'button[data-icon="minus-square"]'
    remove_btn = 'button[data-icon="trash-alt"]'
    checkout_btn = 'button#checkoutButton'
    cnt_text = lambda self, number: f'button.span:has-text(" {number}")'
    toast = 'simple-snack-bar .mat-mdc-snack-bar-label'


print(float('99.99'))