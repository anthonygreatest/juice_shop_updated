from elements.base_element import BaseElement


class File(BaseElement):

    @property
    def type_of(self):
        return 'file'

    def upload(self, path):
        self.page.set_input_files(self.locator, path)