import allure
from playwright.sync_api import expect

from elements.base_element import BaseElement
from utils.logger import get_logger

logger = get_logger('INPUT')


class Input(BaseElement):

    @property
    def type_of(self):
        return 'input'

    def get_locator(self, nth: int = 0, **kwargs):
        return super().get_locator(nth, **kwargs)

    def fill(self, value: str, nth: int = 0, **kwargs):

        step = f'Fill {self.type_of} {self.name} with {value}'

        with allure.step(step):
            locator = self.get_locator(nth, **kwargs)
            logger.info(step)
            locator.fill(value)

    def press_enter(self, nth: int = 0, **kwargs):
        step = f'Press Enter'

        with allure.step(step):
            logger.info(step)
            self.get_locator(nth, **kwargs).press('Enter')

    def blur(self, nth: int = 0, **kwargs):

        step = f'Blurring {self.type_of} {self.name}'

        with allure.step(step):
            logger.info(step)
            self.get_locator(nth=nth, **kwargs).blur()

    def check_have_value(self, value: str, nth: int = 0, **kwargs):

        step = f'Checking that {self.type_of} {self.name} has value {value}'

        with allure.step(step):
            locator = self.get_locator(nth, **kwargs)
            logger.info(step)
            expect(locator).to_have_value(value)