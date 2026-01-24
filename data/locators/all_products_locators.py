


class AllProductsLocators:

    side_menu = 'button[aria-label="Open Sidenav"]'
    account_menu = 'button#navbarAccount'
    account_name = 'button[aria-label="Go to user profile"] span.mat-mdc-menu-item-text span'
    menu_sections = 'div[role="menu"] button'


    add_to_basket_btn = 'button[aria-label="Add to Basket"]'
    go_to_basket_btn = 'button[aria-label="Show the shopping cart"]'
    notification_basket = 'button[aria-label="Show the shopping cart"] span.fa-layers-counter'
    product = lambda self, name: f'mat-grid-tile:has-text("{name}") button[aria-label="Add to Basket"]'
    product_in_basket = lambda self, name: f'mat-row:has-text("{name}")'
    price = 'mat-row mat-cell'
    unavailable_product = lambda self, name: f'mat-grid-tile:has-text("") button[aria-label="Add to Basket"]'


    toast = 'simple-snack-bar .mat-mdc-snack-bar-label'
    success_added_text = lambda self, name: f'Placed {name} into basket.'
    success_added_another_text = lambda self, name: f'Added another {name} to basket.'

    search_icon = 'app-mat-search-bar:has-text(" search ")'
    search_input = 'input[type="text"]'
    search_language_input = 'input[type="search"]'
    close_search_icon = 'app-mat-search-bar:has-text(" close ")'

    #sections
    orders_and_payment = 'button[aria-label="Show Orders and Payment Menu"]'
    order_history = 'button[aria-label="Go to order history page"]'
    recycle = 'button[aria-label="Go to recycling page"]'
    my_saved_addresses = 'button[aria-label="Go to saved address page"]'
    my_payment_options = 'button[aria-label="Go to saved payment methods page"]'
    digital_wallet = 'button[aria-label="Go to wallet page"]'

    privacy_and_security = 'button[aria-label="Show Privacy and Security Menu"]'
    privacy_policy = 'button[aria-label="Go to privacy policy page"]'
    request_data_export = 'button[aria-label="Go to data export page"]'
    request_data_erasure = 'button[aria-label="Go to data subject page"]'
    change_password = 'button[aria-label="Go to change password page"]'
    two_fa_configuration = 'button[aria-label="Go to two factor authentication page"]'
    last_login_ip = 'button[aria-label="Go to last login ip page"]'

    logout = 'button#navbarLogoutButton'
    profile = 'button[aria-label="Go to user profile"]'

    #menu
    customer_feedback = 'a[aria-label="Go to contact us page"]'
    complaint = 'a[aria-label="Go to complain page"]'
    support_chat = 'a[aria-label="Go to chatbot page"]'
    about_us = 'a[aria-label="Go to about us page"]'
    photo_wall = 'a[aria-label="Go to photo wall"]'
    deluxe_membership = 'a[aria-label="Go to deluxe membership page"]'

    #pages
    pagination_dropdown = 'div.mat-mdc-paginator-touch-target'
    next_page_btn = 'button[aria-label="Next page"]'
    previous_page_btn = 'button[aria-label="Previous page"]'
    number_on_page = lambda self, num: f'mat-option:has-text("{num}")'
    items_on_page = 'mat-grid-tile'
    page_number = 'div.mat-mdc-paginator-range-actions'

    #localization
    choose_language = 'button#navbarLanguageButton'
    search_language = 'input[type="search"]'
    language = 'mat-radio-button'
    language_text = 'mat-radio-button input' #area-label
    all_products_heading = 'div.heading'























