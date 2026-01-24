import allure
import pytest

from data.frontend_endpoints import PlaywrightEndpoints
from pages.payment_options_page import PaymentOptionsPage


@pytest.mark.screenshot
@allure.feature('Coupon')
@allure.story('Invalid coupon flow')
@pytest.mark.usefixtures('close_cookies_banner')
@pytest.mark.delete_address
@pytest.mark.delete_product
@pytest.mark.delete_card
class TestUseCouponNegative:

    @allure.title('User not able to activate short coupon')
    @pytest.mark.parametrize('coupon', [
        '1' * 9,
        '1' * 11
    ])
    def test_activate_short_coupon(self, payment_options_page, coupon):

        payment_options_page.open(PlaywrightEndpoints.PAYMENT_OPTIONS)
        payment_options_page.reload()
        payment_options_page.open_coupon_form()

        payment_options_page.coupon_form.fill(coupon)

        payment_options_page.check_redeem_button_remains_disabled()
        payment_options_page.check_invalid_field_error_appears_on_page(
            expected_error=PaymentOptionsPage.WRONG_LENGTH_COUPON
        )

    @allure.title('User not able to activate invalid coupon')
    def test_activate_invalid_coupon(self, payment_options_page):

        payment_options_page.open(PlaywrightEndpoints.PAYMENT_OPTIONS)
        payment_options_page.open_coupon_form()

        payment_options_page.coupon_form.fill_and_redeem('1' * 10)

        payment_options_page.check_wrong_coupon_error_appears_on_page()