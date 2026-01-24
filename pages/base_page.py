import allure
from playwright.sync_api import expect

from utils.logger import get_logger

logger = get_logger('BASE_PAGE')

class BasePage:

    TOAST_TEXT = 'simple-snack-bar .mat-mdc-snack-bar-label'
    CONFIRMATION = 'div.confirmation'
    DISMISS_BANNER_BTN = 'button[aria-label="Close Welcome Banner"]'

    def __init__(self, page):
        self.page = page

    def open(self, url: str):

        step = f'Opening url {url}'

        with allure.step(step):
            logger.info(step)
            self.page.goto(url)

    def close_welcome_banner(self):

        step = f'Closing welcome banner'

        with allure.step(step):
            logger.info(step)
            try:
                self.page.wait_for_selector(self.DISMISS_BANNER_BTN, timeout=500)
                self.page.click(self.DISMISS_BANNER_BTN)
            except:
                print('Welcome banner not found')

    def reload(self):

        step = f'Reloading page with url {self.page.url}'

        with allure.step(step):
            logger.info(step)
            self.page.reload(wait_until='domcontentloaded')

    def check_current_url(self, expected_url):

        step = f'Checking current url equals {expected_url}'

        with allure.step(step):
            logger.info(step)
            expect(self.page).to_have_url(expected_url)
