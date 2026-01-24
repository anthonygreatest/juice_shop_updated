import allure
import pytest

from data.frontend_endpoints import PlaywrightEndpoints
from data.generators.order_generator import pick_product_to_purchase
from tests.tests_frontend.conftest import basket_page


@pytest.mark.screenshot
@allure.feature('Basket')
@allure.story('Invalid add to basket flow')
class TestAddToBasketNegative:

    @allure.title('User not able to proceed without product selected')
    def test_user_not_able_to_proceed_without_product_selected(self, basket_page):

        basket_page.open(PlaywrightEndpoints.BASKET)

        basket_page.check_checkout_button_remains_disabled()

    @allure.title('User not able to add unavailable product to basket')
    def test_add_unavailable_product_to_basket(self, search_page):

        selected_product = pick_product_to_purchase(available=False)

        search_page.find_and_add_product_to_basket(selected_product)

        search_page.check_out_of_stock_toast_appears_on_page()

    @pytest.mark.delete_product
    @allure.title('User not able to add more to product with one total item in stock')
    def test_add_more_to_product_with_one_total_item_in_stock(self, search_page, basket_page, put_product_into_basket):

        selected_product = pick_product_to_purchase(available='one_left')

        put_product_into_basket(selected_product)
        search_page.navbar.click_go_to_basket()

        basket_page.plus_one()

        basket_page.check_out_of_stock_toast_appears_on_page()



