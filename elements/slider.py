import allure

from elements.base_element import BaseElement
from utils.logger import get_logger

logger = get_logger('SLIDER')

class Slider(BaseElement):

    @property
    def type_of(self):
        return 'slider'

    def press_right(self, nth: int = 0, **kwargs):
        step = f'Press Right'

        with allure.step(step):
            logger.info(step)
            self.get_locator(nth, **kwargs).press('ArrowRight')

    def press_left(self, nth: int = 0, **kwargs):
        step = f'Press Left'

        with allure.step(step):
            logger.info(step)
            self.get_locator(nth, **kwargs).press('ArrowLeft')

    def focus(self, nth: int = 0, **kwargs):
        step = f'Focus slider'

        with allure.step(step):
            logger.info(step)
            self.get_locator(nth, **kwargs).focus()