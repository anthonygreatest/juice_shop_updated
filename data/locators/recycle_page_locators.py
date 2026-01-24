

class RecyclePageLocators:


    quantity_field = 'input[placeholder="...in liters"]'
    random_address = 'mat-row'
    address_radio_btn = 'mat-radio-button'
    submit_btn = 'button#recycleButton'
    pickup_checkbox= 'mat-checkbox'
    pickup_date_field = 'input.mat-datepicker-input'
    pickup_date_field_label = 'Pickup Date'
    open_calendar_btn = 'button[aria-label="Open calendar"]'
    calendar = 'mat-datepicker-content'

    next_month_btn = 'button[aria-label="Next month"]'
    previous_month_btn = 'button[aria-label="Previous month"]'
    choose_date = 'button[aria-label="Choose month and year"]'
    year_btn = lambda self, year: f'button:has-text(" {year} ")'
    month_btn = lambda self, month: f'button:has-text(" {month} ")'
    day_btn = lambda self, day: f'button:text-is(" {day} ")'


    toast = 'simple-snack-bar .mat-mdc-snack-bar-label'




