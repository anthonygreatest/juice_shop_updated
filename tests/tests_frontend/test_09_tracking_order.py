import allure
import pytest

from data.frontend_endpoints import PlaywrightEndpoints
from utils.helper import prepare_checkout_response


@allure.feature('Tracking Order')
@allure.story('Valid tracking order flow')
@allure.title('Order data appears in tracking order')
@pytest.mark.usefixtures('close_cookies_banner')
@pytest.mark.delete_address
@pytest.mark.delete_card
def test_tracking_order(order_completion_page, tracking_order_page, checkout_factory, get_headers, basket_id):

    checkout_data = checkout_factory(e_wallet=False, headers=get_headers, login_response=basket_id)
    order_confirmation = prepare_checkout_response(checkout_data).order_confirmation

    order_completion_page.open(PlaywrightEndpoints().ORDER_COMPLETION(order_confirmation))
    order_completion_page.click_track_order()

    tracking_order_page.check_tracking_data_matches_expected(
        selected_product_data=checkout_data.product_name_and_price,
        delivery_data=checkout_data.delivery_selected,
        tracking_num=order_confirmation
    )