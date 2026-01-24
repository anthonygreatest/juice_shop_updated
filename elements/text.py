import allure

from elements.base_element import BaseElement
from utils.logger import get_logger

logger = get_logger('TEXT')

class Text(BaseElement):

    @property
    def type_of(self):
        return 'text'

    def get_text(self, nth: int = 0, **kwargs):

        step = f'Getting {self.type_of} {self.name}'

        with allure.step(step):
            locator = self.get_locator(nth, **kwargs)
            logger.info(step)
            return locator.text_content()
