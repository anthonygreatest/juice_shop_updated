from components.toast_component import ToastComponent
from data.locators.digital_wallet_page_locators import DigitalWalletPageLocators
from elements.button import Button
from pages.base_page import BasePage


class CryptoWalletPage(BasePage):

    PLEASE_INSTALL_TEXT = 'Please install a Web3 wallet like MetaMask to proceed.'

    def __init__(self, page):
        super().__init__(page)
        self.locators = DigitalWalletPageLocators()
        self.metamask_toast = ToastComponent(page)
        self.connect_metamask = Button(page, self.locators.connect_metamask_btn, 'Connect MetaMask Button')

    def click_connect_metamask(self):
        self.connect_metamask.check_enabled()
        self.connect_metamask.click()

    def check_metamask_requires_installation_toast_appears(self):
        self.metamask_toast.check_toast_text(self.PLEASE_INSTALL_TEXT)
