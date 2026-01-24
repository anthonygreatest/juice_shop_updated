import re

import allure
from playwright.sync_api import Page, expect

from utils.logger import get_logger

logger = get_logger('BASE_ELEMENT')

class BaseElement:

    def __init__(self, page: Page, locator: str, name: str):

        self.page = page
        self.locator = locator
        self.name = name
        #name элемента для логирования и алюра

    @property
    def type_of(self):
        #возвращает тип элемента, переопределяется в потомках

        return 'base element'

    def get_locator(self, nth: int = 0, **kwargs):

        locator = self.locator.format(**kwargs)
        step = f'Getting locator {locator} at index {nth}'

        with allure.step(step):
            logger.info(step)
            return self.page.locator(locator).nth(nth)

    def click(self, nth: int = 0, specified_name: str = '', **kwargs):

        step = f'Clicking {self.type_of} {self.name}{specified_name}'

        with allure.step(step):
            locator = self.get_locator(nth, **kwargs)
            logger.info(step)
            locator.click()

    def count_elements(self, nth: int = 0, **kwargs):

        step = f'Counting {self.type_of} {self.name} on page'

        with allure.step(step):
            locator = self.get_locator(nth, **kwargs)
            logger.info(step)
            return locator.count()

    def scroll_into_view_if_needed(self, nth: int = 0, **kwargs):
        step = f'Scrolling into view of {self.type_of} {self.name}'

        with allure.step(step):
            locator = self.get_locator(nth, **kwargs)
            logger.info(step)
            locator.scroll_into_view_if_needed()

    def wait_for_selector(self, locator):

        step = f'Waiting for {locator} to become visible'

        with allure.step(step):
            logger.info(step)
            self.page.wait_for_selector(locator, state='visible')

    def hover(self):
        step = f'Hovering over {self.locator}'

        with allure.step(step):
            logger.info(step)
            self.page.hover(self.locator)

    def get_attribute(self, attribute, nth: int = 0, **kwargs):
        step = f'Getting attribute {attribute} of {self.type_of} {self.name}'

        with allure.step(step):
            locator = self.get_locator(nth, **kwargs)
            logger.info(step)
            return locator.get_attribute(name=attribute)

    def check_visible(self, nth: int = 0, **kwargs):

        step = f'Checking that {self.type_of} {self.name} is visible'

        with allure.step(step):
            locator = self.get_locator(nth, **kwargs)
            logger.info(step)
            expect(locator).to_be_visible()

    def check_have_text(self, text: str, specified_name: str = '', nth: int = 0, **kwargs):

        step = f'Checking that {self.type_of} {self.name}{specified_name} has text {text}'

        with allure.step(step):
            locator = self.get_locator(nth, **kwargs)
            logger.info(step)
            expect(locator).to_have_text(text)


    def check_contain_text(self, text: str, specified_name: str = '', nth: int = 0, **kwargs):

        step = f'Checking that {self.type_of} {self.name}{specified_name} contains text {text}'

        with allure.step(step):
            locator = self.get_locator(nth, **kwargs)
            logger.info(step)
            expect(locator).to_contain_text(text)

    def check_have_attribute(self, attribute: str, value, specified_name: str = '', nth: int = 0, **kwargs):
        step = f'Checking that {self.type_of} {self.name}{specified_name} has attribute {attribute} with value {value}'

        with allure.step(step):
            locator = self.get_locator(nth, **kwargs)
            logger.info(step)
            expect(locator).to_have_attribute(name=attribute, value=value)

    def check_attribute_exists(self, attribute: str, specified_name: str = '', nth: int = 0, **kwargs):
        step = f'Checking that {self.type_of} {self.name}{specified_name} has attribute {attribute}'

        with allure.step(step):
            locator = self.get_locator(nth, **kwargs)
            logger.info(step)
            expect(locator).to_have_attribute(name=attribute, value=re.compile(r'.*'))