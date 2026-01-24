


class OrderHistoryPageLocators:

    write_review_btn = 'button[aria-label="Print order confirmation"] mat-icon:has-text("rate_review")'
    track_order_btn = 'button[aria-label="Track Your Order"]'
    print_order_confirmation_btn = 'button[aria-label="Print order confirmation"]'
    order_id = 'div.heading-row div'#nth(0)
    product = 'mat-row mat-cell'#nth(0)
    item = 'div.orders-container div.ng-star-inserted'
    twitter = 'a[aria-label="Tweet"]'
    order_info = 'div.heading-row div'


    review_field = 'textarea[aria-label="Text field to review a product"]'
    submit_review_btn = 'button#submitButton'
    close_review_btn = 'button[aria-label="Close Dialog"]'
    expand_review_btn = 'mat-expansion-panel-header[role="button"]'
    like_a_review_btn = 'button[aria-label="Rate a helpful review"]'
    comment = 'div.comment'
    comments = 'div.mat-expansion-panel-body div'
    review_text = 'div.review-text p'
    like_counter = 'span.like-counter'

    toast = 'simple-snack-bar .mat-mdc-snack-bar-label'

    track_order_link = 'a:has-text("Track Orders")'

    write_review_container = 'mat-dialog-container'
