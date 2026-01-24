from pages.base_page import BasePage


class TrackingOrderPageLocators:

    delivery_date = 'div span.accent-notification' #nth(3)
    product_name = 'mat-row mat-cell' #nth(0)
    tracking_num = 'h1 span' #nth(1)