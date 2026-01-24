import allure

from data.frontend_endpoints import PlaywrightEndpoints


@allure.feature('Data Erasure')
@allure.story('Valid data erasure flow')
class TestDataErasure:

    @allure.title('Email and security question on data erasure page match those of user')
    def test_data_erasure_page_email_and_security_question_match(self, data_erasure_page,
        user_register_data_via_ui):

        data = user_register_data_via_ui

        data_erasure_page.open(PlaywrightEndpoints.DATA_ERASURE)
        data_erasure_page.check_email_and_security_question_in_placeholder_match_expected(
            expected_email=data.email,
            expected_sec_question=data.security_question.question
        )

    @allure.title('User able to send data erasure request')
    def test_data_erasure_request_sent(self, data_erasure_page, search_page, user_register_data_via_ui):

        data = user_register_data_via_ui

        data_erasure_page.open(PlaywrightEndpoints.DATA_ERASURE)
        data_erasure_page.request_data_erasure(
            email=data.email,
            answer=data.security_answer
        )

        data_erasure_page.check_goodbye_message_appears_on_page()

        unlogged_page = data_erasure_page.go_to_homepage()

        unlogged_page.navbar.click_account_menu()

        unlogged_page.check_account_menu_shows_only_login_for_unlogged_user(
            expected_text='Login'
        )










