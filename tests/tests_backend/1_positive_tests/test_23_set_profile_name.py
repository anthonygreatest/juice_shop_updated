from http import HTTPStatus

import allure

from utils.assertions.base_assertions import assert_status_code


@allure.feature('Profile Photo')
@allure.story('Valid profile photo flow')
@allure.title('User able to change profile name')
def test_set_profile_name_status_code(stub_profile_name):

    response = stub_profile_name

    assert_status_code(response, HTTPStatus.OK)
    assert response.json()['username']
