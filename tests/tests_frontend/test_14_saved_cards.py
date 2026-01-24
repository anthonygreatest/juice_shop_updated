import allure
import pytest

from data.frontend_endpoints import PlaywrightEndpoints
from utils.assertions.credit_card_assertions import check_num_of_cards_on_page_matches_expected


@allure.feature('Credit Card')
@allure.story('Valid credit card flow')
@pytest.mark.usefixtures('close_cookies_banner')
class TestSavedCards:

    @pytest.mark.delete_card
    @allure.title('Added card appears on saved cards page')
    def test_newly_added_card_appears_on_saved_cards_page(self, saved_cards_page, create_credit_card, get_headers):

        added_card = create_credit_card(get_headers)

        saved_cards_page.open(PlaywrightEndpoints.SAVED_CARDS)

        saved_cards_page.check_card_data_on_saved_cards_page_matches_expected(
            expected_card_data=added_card.card_payload
        )

    @allure.title('Deleted card appears on saved cards page')
    def test_deleted_card_no_longer_appears_on_page(self, credit_card, get_headers, create_credit_card,
                                                    saved_cards_page):
        create_credit_card(get_headers)

        saved_cards_page.reload()

        cnt_before = saved_cards_page.get_num_of_cards_on_page()

        saved_cards_page.remove_card()

        cnt_after = saved_cards_page.get_num_of_cards_on_page()

        check_num_of_cards_on_page_matches_expected(
            actual_num=cnt_after,
            expected_num=cnt_before - 1
        )



