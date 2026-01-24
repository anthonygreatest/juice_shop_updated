import allure
import pytest
from data.frontend_endpoints import PlaywrightEndpoints
from data.paths import COMPLAINT_FILE, LARGE_PICTURE
from pages.profile_page import ProfilePage

@pytest.mark.screenshot
@allure.feature('Change profile info')
@allure.story('Invalid change profile info flow')
class TestChangeProfileInfoNegative:

    @pytest.mark.parametrize('profile_picture, expected_error', [
        (COMPLAINT_FILE, ProfilePage.WRONG_FILE_FORMAT),
        (LARGE_PICTURE, ProfilePage.FILE_TOO_LARGE)
    ])
    @allure.title('User not able to upload invalid picture')
    def test_upload_invalid_profile_picture(self, profile_page, profile_picture, expected_error):

        profile_page.open(PlaywrightEndpoints.PROFILE_PAGE)
        profile_page.reload()

        profile_page.upload_picture(
            profile_picture
        )

        profile_page.check_invalid_picture_error_appears_on_page(expected_error=expected_error)
