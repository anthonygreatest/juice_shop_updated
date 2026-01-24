import allure
import pytest

from data.frontend_endpoints import PlaywrightEndpoints
from data.paths import FOR_COMPLAINT_PICTURE
from tests.tests_frontend.frontend_helpers import generate_feedback


@allure.feature('Photo Wall')
@allure.story('Valid photo wall flow')
@pytest.mark.usefixtures('close_cookies_banner')
class TestPhotoWall:

    @allure.title('Photo posted success toast appears on page')
    def test_post_picture_on_photo_wall_success_toast(self, photo_wall_page):

        comment = generate_feedback().comment

        photo_wall_page.open(PlaywrightEndpoints.PHOTO_WALL)
        photo_wall_page.attach_photo(
            caption=comment,
            path=FOR_COMPLAINT_PICTURE
        )

        photo_wall_page.check_img_uploaded_toast_appears_on_page()

    @allure.title('Photo gets posted on photo wall')
    def test_post_appears_on_photo_wall(self, photo_wall_page):

        photo_wall_page.reload()

        comment = generate_feedback().comment
        photo_wall_page.attach_photo(
            caption=comment,
            path=FOR_COMPLAINT_PICTURE
        )

        photo_wall_page.check_post_appears_on_page(
            expected_comment=comment
        )