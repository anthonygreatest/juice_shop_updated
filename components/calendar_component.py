import re

from playwright.sync_api import Page

from components.base_component import BaseComponent
from data.locators.recycle_page_locators import RecyclePageLocators


class CalendarComponent(BaseComponent):

    def __init__(self, page: Page):
        super().__init__(page)
        self.locators = RecyclePageLocators()

    def set_delivery_date_manually(self, day, month, year):
        self.page.wait_for_selector(self.locators.calendar, state='visible')
        calendar = self.page.locator(self.locators.calendar)
        calendar.locator(self.locators.choose_date).click()
        calendar.locator(self.locators.year_btn(year)).click()
        calendar.locator(self.locators.month_btn(month)).click()
        calendar.locator('button', has_text=re.compile(rf'^ {day} $')).click()