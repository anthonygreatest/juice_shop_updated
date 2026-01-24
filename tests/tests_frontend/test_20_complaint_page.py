import allure

from data.frontend_endpoints import PlaywrightEndpoints
from data.paths import COMPLAINT_FILE
from tests.tests_frontend.frontend_helpers import generate_feedback


@allure.feature('Complaint')
@allure.story('Valid complaint flow')
@allure.title('User able to send complaint')
def test_complaint_sent_toast(complaint_page):

    complaint_message = generate_feedback()

    complaint_page.open(PlaywrightEndpoints.COMPLAINTS)
    complaint_page.write_message(
        complaint_message.comment
    )

    complaint_page.attach_complaint(
        COMPLAINT_FILE
    )

    complaint_page.check_complaint_filed_confirmation_text_appears_on_page()