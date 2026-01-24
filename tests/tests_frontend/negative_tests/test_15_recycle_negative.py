import allure
import pytest

from data.frontend_endpoints import PlaywrightEndpoints
from pages.recyle_page import RecyclePage
from tests.tests_frontend.frontend_helpers import generate_box_quantity

@pytest.mark.screenshot
@allure.feature('Recycle')
@allure.story('Invalid recycle flow')
@pytest.mark.usefixtures('close_cookies_banner')
@pytest.mark.delete_address
class TestRecycleNegative:

    @allure.title('User not able to recycle invalid quantity')
    @pytest.mark.parametrize('quantity, expected_error', [
        ('9', RecyclePage.INVALID_QUANTITY),
        ('1001', RecyclePage.INVALID_QUANTITY),
        ('', RecyclePage.EMPTY_QUANTITY)
    ])
    def test_recycle_invalid_quantity(self, recycle_page, quantity, expected_error, recycle):

        recycle(quantity=quantity)

        recycle_page.check_invalid_field_error_appears_on_page(expected_error=expected_error)
        recycle_page.check_submit_button_remains_disabled()

    @allure.title('User not able to recycle without address selected')
    def test_recycle_without_address(self, recycle_page):

        quantity = generate_box_quantity(quantity='small')

        recycle_page.open(PlaywrightEndpoints.RECYCLE)
        recycle_page.set_quantity(
            quantity
        )

        recycle_page.check_submit_button_remains_disabled()

    @allure.title('User not able to recycle with invalid pickup date')
    @pytest.mark.parametrize('pickup_date', [
        '13/12/2025',
        'December'
    ])
    def test_recycle_with_invalid_pickup_date(self, recycle_page, recycle, get_headers, pickup_date):

        quantity = generate_box_quantity(quantity='bulk')

        recycle(quantity=quantity)

        recycle_page.send_pickup()

        recycle_page.set_delivery_date(
            pickup_date
        )

        recycle_page.check_submit_button_remains_disabled()
        recycle_page.check_invalid_field_error_appears_on_page(expected_error=RecyclePage.INVALID_PICKUP_DATE)
