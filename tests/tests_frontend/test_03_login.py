import allure
import pytest

from data.frontend_endpoints import PlaywrightEndpoints
from tests.tests_frontend.frontend_helpers import log_in_user
from utils.helper import register_user_and_set_security_answer


@allure.feature('Login')
@allure.story('Valid login flow')
@pytest.mark.screenshot
@pytest.mark.video
class TestLogin:

    @allure.title('Registered user able to log in')
    def test_user_able_to_log_in(self, login_page, main_page, register):

        validated_response, registered_user = register_user_and_set_security_answer(register)

        login_page.open(PlaywrightEndpoints.LOGIN)

        login_page = log_in_user(
            registered_user,
            login_page
        )
        login_page.click_login_btn()

        main_page.check_account_name_matches_email(registered_user.email)


