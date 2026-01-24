
class CompletionPageLocators:

    thanks_locator = 'h1.confirmation' #nth(0)
    delivery_date = 'span div.confirmation' #nth(1)
    delivery_address = 'div:has-text("Phone Number")'
    product = 'mat-row mat-cell' #nth(0)
    track_order_link = 'a:has-text("Track Orders")'
    print_order_confirmation_btn = 'button[aria-label="Print order confirmation"]'
    price = 'mat-row mat-cell'

    twitter = 'a[aria-label="Tweet"]'
    order_summary_data = 'table.price-align tr'
    delivery_data = 'div.order-completion-header div.ng-star-inserted'

