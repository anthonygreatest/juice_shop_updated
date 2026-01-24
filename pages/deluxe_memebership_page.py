from decimal import Decimal

from components.navbar_component import NavbarMenuComponent
from data.locators.deluxe_membership_locators import DeluxeMembershipLocators
from elements.button import Button
from elements.text import Text
from pages.base_page import BasePage


class DeluxeMembershipPage(BasePage):

    DELUXE_MEMBER_CONFIRMATION = 'You are already a deluxe member!'

    def __init__(self, page):
        super().__init__(page)
        self.locators = DeluxeMembershipLocators()
        self.fee = Text(page, self.locators.fee, 'Membership Fee')
        self.become_member_btn = Button(page, self.locators.become_member_btn, 'Become member')
        self.membership_text = Text(page, self.locators.membership_text, 'Membership activated')
        self.navbar = NavbarMenuComponent(page)

    def become_member(self):
        self.become_member_btn.check_enabled()
        self.become_member_btn.click()

    def check_membership_text_appears_on_page(self):
        self.membership_text.check_contain_text(self.DELUXE_MEMBER_CONFIRMATION)

    def see_membership_fee(self):
        return Decimal(self.fee.get_text(nth=1).strip()[:-1])
