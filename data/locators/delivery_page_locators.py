

class DeliveryPageLocators:

    delivery_info = 'div.addressCont div'
    # delivery_option = lambda self, days: f'mat-row:has-text("{days} Days") mat-radio-button'
    delivery_option = 'mat-row mat-radio-button'

    continue_to_payment = 'button[aria-label="Proceed to delivery method selection"]'
