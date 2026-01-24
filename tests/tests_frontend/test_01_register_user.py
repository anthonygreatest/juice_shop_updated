import allure
import pytest

from data.frontend_endpoints import PlaywrightEndpoints
from tests.tests_frontend.frontend_helpers import formatted_register_payload_for_ui
from utils.helper import prepare_register_payload


@allure.feature('User Registration')
@allure.story('Valid registration flow')
@pytest.mark.screenshot
@pytest.mark.video
class TestRegisterPage:

    @allure.title("User able to register successfully")
    def test_user_able_to_register(self, register_page, login_page):

        user_data = formatted_register_payload_for_ui()

        register_page.open(PlaywrightEndpoints.REGISTER)
        register_page.registration_form.check_visible(
            email='',
            password='',
            repeat_password='',
            security_question='',
            answer=''
        )

        register_page.register(
            **user_data
        )

        login_page.check_user_registered_toast_appears_on_page()



