

class CheckoutPageLocators:

    place_order_btn = 'button#checkoutButton'
    card_info = 'mat-card mat-card:has-text("Card Holder\\"")'
    delivery_info = 'mat-card mat-card'
    product_info = 'mat-row mat-cell'
    delivery_fee = 'table tr' #nth(1) .mat-cell price
    delivery_fee_sum = 'td.mat-cell.price'
    total_price = 'td.price'
    order_summary_data = 'div.mdc-card tr'

    side_menu_btn = 'button[aria-label="Show/hide account menu"]'
    orders_payment_btn = 'button[aria-label="Show Orders and Payment Menu"]'
    order_history_btn = 'button[aria-label="Go to order history page"]'


