from components.calendar_component import CalendarComponent
from components.saved_address_component import SavedAddressComponent
from components.toast_component import ToastComponent
from data.dataclasses.delivery_date import DeliveryDate
from data.locators.recycle_page_locators import RecyclePageLocators
from elements.button import Button
from elements.input import Input
from elements.text import Text
from pages.base_page import BasePage
from pages.mixins import NegativeTestsMixin


class RecyclePage(BasePage, NegativeTestsMixin):

    TOAST_RESPONSE = 'Thank you for using our eco-friendly recycling self-service. We will send you a pomace recycling box asap.'
    EMPTY_QUANTITY = 'Please provide a quantity.'
    INVALID_QUANTITY = 'Quantity must be 10-1000 liters.'
    INVALID_PICKUP_DATE = 'Please provide a valid date.'

    def __init__(self, page):
        super().__init__(page)
        self.locators = RecyclePageLocators()
        self.quantity_input = Input(page, self.locators.quantity_field, 'Quantity')
        self.saved_address = SavedAddressComponent(page)
        self.submit_btn = Button(page, self.locators.submit_btn, 'Submit')
        self.toast = ToastComponent(page)
        self.pickup_checkbox = Button(page, self.locators.pickup_checkbox, 'Send pickup')
        self.calendar_btn = Button(page, self.locators.open_calendar_btn, 'Calendar')
        self.calendar = CalendarComponent(page)
        self.pickup_date_input = Input(page, self.locators.pickup_date_field, 'Pickup date')
        self.field_error = Text(page, self.ERROR, 'Field error')

    def set_quantity(self, quantity):
        self.quantity_input.fill(quantity)
        self.quantity_input.check_have_value(quantity)
        self.quantity_input.blur()

    def recycle_and_select_address(self, quantity):
        self.set_quantity(quantity)
        self.select_address()

    def select_address(self):
        self.saved_address.click_select_address()

    def click_submit(self):
        self.submit_btn.check_enabled()
        self.submit_btn.click()

    def check_thanks_for_recycle_toast_appears_on_page(self):
        self.toast.check_toast_text(self.TOAST_RESPONSE)

    def send_pickup(self):
        self.pickup_checkbox.check_enabled()
        self.pickup_checkbox.click()

    def click_calendar(self):
        self.calendar_btn.check_enabled()
        self.calendar_btn.click()

    def set_delivery_date_manually(self, data: DeliveryDate):
        self.click_calendar()
        self.page.wait_for_selector(self.locators.calendar, state='visible')
        self.calendar.set_delivery_date_manually(
            day=data.day,
            month=data.month,
            year=data.year
        )

    def submit_bulk_quantity_with_date_set_manually(self, data: DeliveryDate):
        self.send_pickup()
        self.set_delivery_date_manually(data)
        self.click_submit()

    def set_delivery_date(self, date):
        self.pickup_date_input.fill(date)
        self.pickup_date_input.check_have_value(date)
        self.pickup_date_input.blur()

    def submit_bulk_with_date_set_via_text(self, date):
        self.send_pickup()
        if date:
            self.set_delivery_date(date)
        self.click_submit()

    def check_submit_button_remains_disabled(self):
        self.submit_btn.check_disabled()

    def check_invalid_field_error_appears_on_page(self, expected_error):
        self.field_error.check_contain_text(expected_error)

