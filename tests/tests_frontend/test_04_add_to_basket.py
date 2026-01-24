import allure
import pytest

from data.generators.order_generator import pick_product_to_purchase


@pytest.mark.usefixtures('close_cookies_banner')
@pytest.mark.delete_product
@allure.feature('Basket')
@allure.story('Valid add product to basket flow')
class TestAddProduct:

    @allure.title('Added product appears in basket')
    def test_added_product_appears_in_basket(self, search_page, basket_page, put_product_into_basket):

        selected_product = pick_product_to_purchase(available=True)

        put_product_into_basket(selected_product)

        search_page.navbar.click_go_to_basket()
        basket_page.check_product_in_basket_matches_added(selected_product)

    @allure.title('Product added to basket success toast appears on page')
    def test_product_added_to_basket_toast_appears_on_page(self, search_page, basket_page, put_product_into_basket):

        selected_product = pick_product_to_purchase(available=True)

        put_product_into_basket(selected_product)

        search_page.check_product_added_toast_appears_on_page(selected_product)

