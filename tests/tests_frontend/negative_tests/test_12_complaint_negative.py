import json
from pathlib import Path

import allure
import pytest

from data.frontend_endpoints import PlaywrightEndpoints
from data.paths import FOR_COMPLAINT_PICTURE, COMPLAINT_FILE
from tests.tests_frontend.frontend_helpers import generate_feedback


@pytest.mark.screenshot
@allure.feature('Complaint')
@allure.story('Invalid complaint flow')
class TestComplaintNegative:

    @allure.title('User not able to send complaint with wrong attached file format')
    def test_complaint_with_wrong_attached_file_format(self, complaint_page):
        complaint_message = generate_feedback()

        complaint_page.open(PlaywrightEndpoints.COMPLAINTS)
        complaint_page.write_message(
            complaint_message.comment
        )

        complaint_page.upload_complaint.upload(
            FOR_COMPLAINT_PICTURE
        )

        complaint_page.check_wrong_file_format_error_appears_on_page()

    @allure.title('User not able to send complaint without complaint text')
    def test_complaint_without_complaint_text(self, complaint_page):

        complaint_page.open(PlaywrightEndpoints.COMPLAINTS)
        complaint_page.write_message(
            ''
        )

        complaint_page.upload_complaint.upload(
            COMPLAINT_FILE
        )

        complaint_page.check_submit_button_remains_disabled()
        complaint_page.check_invalid_field_error_appears_on_page()