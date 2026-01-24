import allure
import pytest

from data.frontend_endpoints import PlaywrightEndpoints
from utils.helper import deposit_to_digital_wallet_payload


@pytest.mark.screenshot
@allure.feature('Deluxe Membership')
@allure.story('Invalid deluxe membership flow')
@pytest.mark.usefixtures('close_cookies_banner')
class TestDeluxeMembershipNegative:

    @allure.title('User not able to activate membership with insufficient balance')
    @pytest.mark.delete_card
    def test_activate_deluxe_membership_with_insufficient_balance(self, deluxe_membership_page, get_headers,
        create_credit_card, payment_options_page):

        card_data = create_credit_card(headers=get_headers)

        deposit_to_digital_wallet_payload(
            payment_id=card_data.added_card.data.id,
            balance='deluxe membership'
        )

        deluxe_membership_page.open(PlaywrightEndpoints.DELUXE_MEMBERSHIP)
        deluxe_membership_page.become_member()

        payment_options_page.check_e_wallet_button_remains_disabled()
        payment_options_page.check_proceed_to_checkout_button_remains_disabled()