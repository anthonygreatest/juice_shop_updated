

class PaymentOptionsPageLocators:

    #add new card locators
    open_card_form = 'mat-expansion-panel-header:has-text(" Add new card ")'
    name = 'mat-form-field:has-text("Name") input'
    card_number = 'mat-form-field:has-text("Card Number") input'
    expiry_month = 'mat-form-field:has-text("Expiry Month") select'
    expiry_year = 'mat-form-field:has-text("Expiry Year") select'
    submit_btn = 'button#submitButton'
    card_data = 'mat-cell'
    card_info = 'mat-card'

    #delete_card
    remove_card_btn = 'mat-cell.mat-column-Remove button'
    random_card_in_basket = 'mat-row'

    #toast
    toast = 'simple-snack-bar .mat-mdc-snack-bar-label'
    card_added_text = 'Your card ending with 1545 has been saved for your convenience.'

    #general
    # select_card_radio_btn = lambda self, name: f'mat-row:has-text("{name}") mat-radio-button'
    select_card_radio_btn = 'mat-row mat-radio-button'
    continue_btn = 'button[aria-label="Proceed to review"]'
    accept_cookies_btn = "a:has-text('Me want it!')"

    #pay using wallet
    wallet_balance_text = 'b span.confirmation card-title'
    pay_with_digital_wallet_btn = lambda self, amount: f'button span:has-text(" Pay {amount}¤ ")'
    pay_btn = 'div button[type="submit"]'

    #add a coupon
    open_coupon_form = 'mat-expansion-panel-header:has-text(" Add a coupon ")'
    coupon_field = 'input#coupon'
    reddit_link = 'a:has-text("Reddit")'
    first_post = 'article' #nth(0)
    coupon = 'shreddit-post-text-body code'
    sale = 'shreddit-post-text-body strong'
    redeem_btn = 'button#applyCouponButton'

    #other payment options
    open_other_payment_options_form = 'mat-expansion-panel-header:has-text(" Other payment options ")'
    stripe = 'a:has-text(" Credit Card")'
    spreadshirt_us = 'a:has-text(" Spreadshirt (US)")'
    spreadshirt_de = 'a:has-text(" Spreadshirt (DE)")'
    sticker_you = 'a:has-text(" StickerYou")'
    lean_pub = 'a:has-text(" Leanpub")'
    open_sea = 'a:has-text(" OpenSea")'



    success_text = '.confirmation.ng-star-inserted'
