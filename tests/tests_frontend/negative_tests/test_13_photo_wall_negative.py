import allure
import pytest

from data.frontend_endpoints import PlaywrightEndpoints
from data.paths import FOR_COMPLAINT_PICTURE, COMPLAINT_FILE
from tests.tests_frontend.frontend_helpers import generate_feedback


@pytest.mark.screenshot
@allure.feature('Photo Wall')
@allure.story('Invalid photo wall flow')
@pytest.mark.usefixtures('close_cookies_banner')
class TestPhotoWallNegative:

    @allure.title('User not able to post without caption')
    def test_post_without_caption(self, photo_wall_page):

        photo_wall_page.open(PlaywrightEndpoints.PHOTO_WALL)

        photo_wall_page.write_caption(
            ''
        )
        photo_wall_page.pick_image.upload(
            FOR_COMPLAINT_PICTURE
        )

        photo_wall_page.check_send_button_remains_disabled()
        photo_wall_page.check_invalid_field_error_appears_on_page()

    @allure.title('User not able to post without photo')
    def test_post_without_photo(self, photo_wall_page):

        caption = generate_feedback().comment
        photo_wall_page.open(PlaywrightEndpoints.PHOTO_WALL)

        photo_wall_page.write_caption(
            caption
        )
        photo_wall_page.check_send_button_remains_disabled()

    @allure.title('User not able to post wrong photo format')
    def test_post_with_wrong_photo_format(self, photo_wall_page):

        caption = generate_feedback().comment
        photo_wall_page.open(PlaywrightEndpoints.PHOTO_WALL)

        photo_wall_page.write_caption(
            caption
        )
        photo_wall_page.pick_image.upload(
            COMPLAINT_FILE
        )

        photo_wall_page.check_send_button_remains_disabled()

