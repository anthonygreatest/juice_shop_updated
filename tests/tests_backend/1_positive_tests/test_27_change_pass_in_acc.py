from http import HTTPStatus

import allure

from utils.assertions.base_assertions import assert_status_code
from utils.helper import change_password_in_account, user_logged_in


@allure.feature('Change Password')
@allure.story('Valid change password flow')
@allure.title('User able to change password in acc and log in with new password')
def test_user_able_to_log_in_after_changing_password_in_acc(headers_with_auth,
    change_password, registered_user_data, logout, login):

    _, pass_changed_data = change_password_in_account(
        change_password=change_password,
        headers=headers_with_auth,
        old_user_password=registered_user_data.password,
        email=registered_user_data.email,
        answer=registered_user_data.security_answer
    )

    logout.log_out_user(
        headers=headers_with_auth
    )

    _, response_after_login_with_old_data = user_logged_in(
        email=registered_user_data.email,
        password=registered_user_data.password,
        login=login
    )

    _, response_after_login_with_new_data = user_logged_in(
        email=registered_user_data.email,
        password=pass_changed_data.new,
        login=login
    )

    assert_status_code(response_after_login_with_old_data, HTTPStatus.UNAUTHORIZED)
    assert_status_code(response_after_login_with_new_data, HTTPStatus.OK)