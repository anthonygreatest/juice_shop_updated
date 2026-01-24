from pathlib import Path

import allure

from data.frontend_endpoints import PlaywrightEndpoints
from data.paths import PROFILE_PICTURE
from utils.assertions.profile_page_assertions import assert_profile_picture_gets_updated
from utils.helper import add_address_payload


@allure.feature('Change Profile Info')
@allure.story('Valid change profile info flow')
class TestUpdateProfileInfo:

    @allure.title('Changed profile name appears on page')
    def test_changed_profile_name_appears_on_profile_page(self, profile_page):

        name = add_address_payload().full_name

        profile_page.open(PlaywrightEndpoints.PROFILE_PAGE)
        profile_page.set_username(
            name
        )

        profile_page.check_set_username_appears_matches_expected(
            expected_username=name
        )

    @allure.title('Changed profile photo appears on page')
    def test_changed_photo_profile_appears_on_profile_page(self, profile_page):

        profile_page.open(PlaywrightEndpoints.PROFILE_PAGE)

        pic_src_before_update = profile_page.get_picture()

        profile_page.upload_picture(
            PROFILE_PICTURE
        )

        pic_src_after_update = profile_page.get_picture()

        assert_profile_picture_gets_updated(
            old_picture=pic_src_before_update,
            updated_picture=pic_src_after_update
        )
