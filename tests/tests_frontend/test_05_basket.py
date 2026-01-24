import allure
import pytest

from data.frontend_endpoints import PlaywrightEndpoints
from data.generators.order_generator import pick_product_to_purchase
from tests.tests_frontend.frontend_helpers import increase_product_quantity
from utils.assertions.basket_assertions import assert_product_quantity_in_basket


@allure.feature('Basket')
@allure.story('Valid basket flow')
@pytest.mark.usefixtures('close_cookies_banner')
class TestBasket:

    @pytest.mark.delete_product
    @allure.title('Notifications and number of products in basket match')
    def test_notifications_cnt_changes_with_product_added(self, basket, basket_page, search_page, put_product_into_basket):

        selected_product = pick_product_to_purchase(available=True)

        put_product_into_basket(selected_product)

        search_page.navbar.click_go_to_basket()

        products_cnt = basket_page.basket.count_products_in_basket()

        basket_page.check_num_of_products_in_basket_matches_notifications_cnt(
            num_of_products_in_basket=products_cnt
        )

    @allure.title('Deleted from basket product no longer appears there')
    def test_user_able_to_delete_product_from_basket(self, basket, basket_id, basket_page, get_headers,
        add_product_to_basket):

        add_product_to_basket(
            headers=get_headers,
            login_response=basket_id
        )
        basket_page.open(PlaywrightEndpoints.BASKET)

        products_cnt_before = basket_page.basket.count_products_in_basket()

        basket_page.delete_product_from_basket()

        products_cnt_after = basket_page.basket.count_products_in_basket()

        assert_product_quantity_in_basket(
            actual_quantity=products_cnt_after,
            quantity_expected=products_cnt_before - 1
        )

    @allure.title('One more (+1) item can be added to product in basket')
    @pytest.mark.delete_product
    def test_plus_one_more_product_in_basket(self, basket, basket_id, get_headers, basket_page, add_product_to_basket):

        add_product_to_basket(
            headers=get_headers,
            login_response=basket_id
        )
        basket_page.reload()

        cnt_before = basket_page.basket.get_product_quantity()

        basket_page.plus_one()

        cnt_after = basket_page.basket.get_product_quantity()

        assert_product_quantity_in_basket(
            actual_quantity=cnt_after,
            quantity_expected=cnt_before + 1
        )


    @allure.title('One item (-1) can be removed from product in basket')
    @pytest.mark.delete_product
    def test_minus_one_product_from_basket(self, basket_id, basket, get_headers, basket_page, add_product_to_basket):

        add_product_to_basket(
            headers=get_headers,
            login_response=basket_id
        )
        basket_page.reload()

        basket_page.plus_one()

        cnt_before = basket_page.basket.get_product_quantity()

        basket_page.minus_one()

        cnt_after = basket_page.basket.get_product_quantity()

        assert_product_quantity_in_basket(
            actual_quantity=cnt_after,
            quantity_expected=cnt_before - 1
        )

    @allure.title('Total order price in basket is accurately calculated')
    @pytest.mark.delete_product
    def test_calculate_product_price(self, basket, basket_page, get_headers, basket_id, add_product_to_basket):

        add_product_to_basket(
            headers=get_headers,
            login_response=basket_id
        )

        basket_page.reload()

        single_product_price = basket_page.basket.get_product_price()

        increase_product_quantity(basket_page, expected_num=3)

        basket_page.check_total_price(
            expected_price=single_product_price * 3
        )




