from components.card_form_component import CardFormComponent
from data.locators.payment_options_page_locators import PaymentOptionsPageLocators
from elements.button import Button
from elements.text import Text
from pages.base_page import BasePage
from utils.schemas.add_credit_card_request import AddCreditCardRequest


class SavedCardsPage(BasePage):

    def __init__(self, page):
        super().__init__(page)
        self.locators = PaymentOptionsPageLocators()
        self.card_info = Text(page, self.locators.card_data, 'Card Info')
        self.card = Text(page, self.locators.random_card_in_basket, 'Card')
        self.remove_card_btn = Button(page, self.locators.remove_card_btn, 'Remove card Button')
        self.card_form = CardFormComponent(page)

    def check_card_data_on_saved_cards_page_matches_expected(self, expected_card_data: AddCreditCardRequest):
        self.card_info.check_have_text(expected_card_data.full_name, nth=1, specified_name=' (card holder)')
        self.card_info.check_have_text('*' * 12 + str(expected_card_data.card_num)[12:], nth=0, specified_name=' (card num)')
        self.card_info.check_have_text(f'{expected_card_data.exp_month}/{expected_card_data.exp_year}', nth=2, specified_name=' (card exp date)')

    def remove_card(self):
        self.remove_card_btn.check_enabled()
        self.remove_card_btn.click()

    def get_num_of_cards_on_page(self):
        return self.card.count_elements()