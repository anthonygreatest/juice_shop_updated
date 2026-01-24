from http import HTTPStatus

import allure

from utils.assertions.base_assertions import assert_status_code
from utils.helper import prepare_missing_headers

@allure.feature('Logout')
@allure.story('Invalid logout flow')
@allure.title('User not able to log out without auth header')
def test_logout_without_auth(raw_api_client, headers_with_auth):

    bad_headers = prepare_missing_headers(
        headers_with_auth=headers_with_auth,
        missing_header='Authorization'
    )

    response = raw_api_client.get(
        endpoint='logout',
        headers=bad_headers
    )

    assert_status_code(response, HTTPStatus.UNAUTHORIZED)