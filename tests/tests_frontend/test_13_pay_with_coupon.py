import allure
import pytest
from data.frontend_endpoints import PlaywrightEndpoints
from tests.tests_frontend.frontend_helpers import calculate_final_price

@allure.feature('Coupon')
@allure.story('Valid coupon flow')
@pytest.mark.usefixtures('close_cookies_banner')
@pytest.mark.delete_address
@pytest.mark.delete_product
@pytest.mark.delete_card
class TestCoupon:

    @allure.title('Coupon applied toast appears on page')
    def test_coupon_applied_toast(self, payment_options_page):

        payment_options_page.open(PlaywrightEndpoints.PAYMENT_OPTIONS)

        sale = payment_options_page.activate_coupon()

        payment_options_page.check_coupon_applied_text_matches_expected(
            expected_sale=sale
        )

    def test_final_sum_changes_with_coupon(self, payment_options_page, checkout_page, user_at_checkout):

        payment_options_page.open(PlaywrightEndpoints.PAYMENT_OPTIONS)

        payment_options_page.card_form.select_card()

        sale = payment_options_page.activate_coupon()

        payment_options_page.proceed_to_checkout()

        sale_sum, expected_final_price = calculate_final_price(
            sale=sale,
            price=user_at_checkout.selected_product_data.product_price,
            delivery_fee=user_at_checkout.delivery_data.delivery_price
        )

        checkout_page.check_calculated_sale_and_final_price_match_expected(
            expected_sale=sale_sum,
            expected_final_price=expected_final_price
        )