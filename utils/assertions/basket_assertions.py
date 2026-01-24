import allure

from utils.assertions.base_assertions import assert_match
from utils.logger import get_logger
from utils.schemas.add_to_basket_request_schema import AddToBasketRequestSchema
from utils.schemas.add_to_basket_resp_schema import AddToBasketRespSchema, ProductInBasketSchema
from utils.schemas.get_all_products_in_basket_schema import GetAllProductsInBasketSchema

logger = get_logger("BASKET_ASSERTIONS")

@allure.step('Checking product gets added to basket')
def assert_product_added_to_basket(response: AddToBasketRespSchema, expected: AddToBasketRequestSchema):

    logger.info('Checking product gets added to basket')

    assert_match(response.data.product_id, expected.product_id, 'product_id')
    assert_match(response.data.basket_id, expected.basket_id, 'basket_id')
    assert_match(response.data.quantity, expected.quantity, 'quantity')

@allure.step('Checking product appears in basket')
def assert_added_product_appears_among_others_in_basket(response: GetAllProductsInBasketSchema,
    expected: AddToBasketRespSchema):

    logger.info('Checking customer feedback on feedback page')

    matched_product = next(
        (product for product in response.data.products if product.id == expected.data.product_id),
        None
    )

    assert matched_product, f'Product with {expected.data.id} not found'

    assert_match(matched_product.basket_item.product_id, expected.data.product_id, 'product_id')
    assert_match(matched_product.basket_item.id, expected.data.id, 'id')
    assert_match(matched_product.basket_item.basket_id, expected.data.basket_id, 'basket_id')
    assert_match(matched_product.basket_item.quantity, expected.data.quantity, 'quantity')
    assert_match(matched_product.basket_item.created_at, expected.data.created_at, 'created_at')
    assert_match(matched_product.basket_item.updated_at, expected.data.updated_at, 'updated_at')


@allure.step('Checking deleted product no longer in basket')
def assert_deleted_product_no_longer_in_basket(response_schema: ProductInBasketSchema,
    product_quantity: int):

    logger.info('Checking deleted product no longer in basket')

    assert len(response_schema.data) == product_quantity, \
        f'Wrong number of products, expected {len(response_schema.data)}, got {product_quantity}'

@allure.step('Checking number of products in basket')
def assert_number_of_products_in_basket(response_schema: GetAllProductsInBasketSchema, product_quantity: int):

    logger.info('Checking number of products in basket')

    assert len(response_schema.data.products) == product_quantity, \
        f'Wrong number of products, expected {len(response_schema.data.products)}, got {product_quantity}'

@allure.step('Checking product quantity in basket')
def assert_product_quantity_in_basket(actual_quantity, quantity_expected):

    logger.info('Checking product quantity in basket')

    assert actual_quantity == quantity_expected, \
        f'Wrong product quantity, expected {quantity_expected}, got {actual_quantity}'

@allure.step('Checking product price changes for deluxe members')
def assert_price_changes_for_deluxe_member(normal_price, price_for_deluxe_member):

    logger.info('Checking product price changes for deluxe members')

    assert normal_price > price_for_deluxe_member, \
        f'Price for deluxe member not lower, normal price: {normal_price}, price for deluxe member: {price_for_deluxe_member}'
