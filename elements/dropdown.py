import allure
from playwright.sync_api import expect

from elements.base_element import BaseElement
from utils.logger import get_logger

logger = get_logger('DROPDOWN')

class Dropdown(BaseElement):

    @property
    def type_of(self):
        return 'dropdown'

    def open_dropdown(self, nth: int = 0, **kwargs):

        step = f'Open {self.type_of} {self.name}'

        with allure.step(step):
            logger.info(step)
            self.click(nth, **kwargs)

    def choose_option(self, option):
        step = f'Selecting {option} in {self.type_of} {self.name}'

        with allure.step(step):
            self.open_dropdown()
            logger.info(step)
            self.page.get_by_text(option).click()

    def select_option_in_dropdown(self, option):
        step = f'Selecting {option} in {self.type_of} {self.name}'

        with allure.step(step):
            logger.info(step)
            self.page.select_option(self.locator, value=option)

    def blur(self, nth: int = 0, **kwargs):

        step = f'Blurring {self.type_of} {self.name}'

        with allure.step(step):
            logger.info(step)
            self.get_locator(nth=nth, **kwargs).blur()