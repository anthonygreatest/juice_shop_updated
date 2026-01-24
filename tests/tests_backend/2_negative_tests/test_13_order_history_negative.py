import allure
import pytest

from utils.assertions.base_assertions import assert_status_code_among_expected
from utils.helper import prepare_missing_headers


@allure.feature('Order History')
@allure.story('Invalid order history flow')
@allure.title('User not able to see order history with missing headers')
@pytest.mark.delete_address
@pytest.mark.delete_card
@pytest.mark.parametrize('missing_header, codes', [
    ('Content-Type', [400, 415, 500, 200]),
    ('Authorization', [401, 500])
])
def test_order_history_missing_headers(order_history, headers_with_auth, missing_header, codes):

    bad_headers = prepare_missing_headers(
        headers_with_auth=headers_with_auth,
        missing_header=missing_header
    )

    response = order_history.get_order_history(
        headers=bad_headers
    )

    assert_status_code_among_expected(response, codes)