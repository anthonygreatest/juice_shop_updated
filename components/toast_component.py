from components.base_component import BaseComponent
from elements.text import Text


class ToastComponent(BaseComponent):

    def __init__(self, page):
        super().__init__(page)
        self.toast = Text(page, 'simple-snack-bar .mat-mdc-snack-bar-label', 'Toast')

    def check_toast_text(self, text):
        self.toast.check_visible()
        self.toast.check_have_text(text)