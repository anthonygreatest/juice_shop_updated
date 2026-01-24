from playwright.sync_api import Locator


class FileUploader:

    def attach_file(self, locator, path):
        self.page.set_input_files(locator, path)

    def upload_and_submit(self, upload_locator, submit_locator, path):
        submit_btn = self.page.locator(submit_locator)
        self.attach_file(upload_locator, path)
        submit_btn.scroll_into_view_if_needed()
        submit_btn.click()

class LinkAccessMixin:

    def get_link(self, locator):
        link = self.page.locator(locator)
        link.scroll_into_view_if_needed()
        return link.get_attribute('href')

class LogoutMixin:

    MENU = ('button', 'Open Sidenav')
    ACCOUNT_MENU = 'button#navbarAccount'
    LOGOUT = 'button#navbarLogoutButton'

    def click_menu(self):
        self.get_by_role(*self.MENU).click()

    def click_account(self):
        self.click(self.ACCOUNT_MENU)

    def log_out(self):
        self.click_account()
        self.click(self.LOGOUT)


class LocalizationMixin:

    LANGUAGE_CHANGED_TOAST = lambda self, language: f'Language has been changed to {language}'

    def change_language(self, lang):
        self.click(self.locators.choose_language)
        self.fill_text(self.locators.search_language, lang)
        language_text = self.page.locator(self.locators.language_text).get_attribute('aria-label')
        self.click(self.locators.language)
        return language_text

    def get_text_on_page(self):
        return self.get_text(
            self.locators.all_products_heading
        )


class NegativeTestsMixin:

    ERROR = 'mat-error'
    FORM_ERROR = 'div.error'
    INACTIVE_BUTTON = 'true'
    UNFILLED_FIELD = 'true'

    def see_error_text(self):
        errors = self.count_elements_on_page(self.ERROR)
        errors_text = []
        for num in range(errors):
            error = self.get_locator(self.ERROR).nth(num)
            errors_text.append(self.get_text(
                error
            ).strip())
        return errors_text

    def see_button_inactive(self, locator):
        if isinstance(locator, Locator):
            btn = locator
        else:
            btn = self.get_locator(locator)
        btn.scroll_into_view_if_needed()
        return btn.get_attribute('disabled')

    def see_field_frame_red(self, locator):
        field = self.get_locator(locator)
        field.scroll_into_view_if_needed()
        return field.get_attribute('aria-invalid')

    def see_form_error_message(self):
        return self.get_text(
            self.FORM_ERROR
        ).strip()

    def blur_element(self, locator):
        element = self.get_locator(locator)
        self.click(element)
        element.blur()

    def clear_field(self, locator):
        field = self.get_locator(locator)
        field.clear()


class DismissBannerMixin:
    DISMISS_BANNER_BTN = 'button[aria-label="Close Welcome Banner"]'

    def dismiss_banner(self):
        self.page.wait_for_selector(self.DISMISS_BANNER_BTN, timeout=500)
        self.click(self.DISMISS_BANNER_BTN)

