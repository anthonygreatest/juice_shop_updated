from http import HTTPStatus
import allure

from data.paths import FOR_COMPLAINT_PICTURE
from utils.assertions.base_assertions import assert_status_code
from utils.assertions.photo_wall_assertions import assert_uploaded_photo_data_matches_actual_data, \
    assert_uploaded_photo_gets_saved
from utils.schemas.upload_photo_resp_schema import UploadPhotoRespSchema
from utils.validators import validate_response


@allure.feature('Upload Photo')
@allure.story('Valid upload photo flow')
class TestPhotoWall:

    @allure.title('User able to upload photo')
    def test_user_able_to_upload_photo(self, upload_photo, register_response):

        file_name = 'for_complaint.png'
        caption_comment = 'Fix this mistake already'

        response = upload_photo(
            picture=FOR_COMPLAINT_PICTURE,
            file_name=file_name,
            caption_comment=caption_comment
        )

        validated_response = validate_response(UploadPhotoRespSchema, response.json())

        assert_status_code(response, HTTPStatus.OK)

        assert_uploaded_photo_data_matches_actual_data(
            response=validated_response,
            expected_user_id=register_response,
            expected_caption=caption_comment
        )

    @allure.title('Uploaded photo appears on photo wall')
    def test_uploaded_photo_gets_saved(self, upload_photo, headers_with_auth, photo_wall, register_response):

        file_name = 'for_complaint.png'
        caption_comment = 'Fix this mistake already'

        upload_photo(
            picture=FOR_COMPLAINT_PICTURE,
            file_name=file_name,
            caption_comment=caption_comment
        )

        all_photos = photo_wall.get_photos(
            headers=headers_with_auth
        )

        assert_uploaded_photo_gets_saved(
            response=all_photos,
            expected_user_data=register_response,
            expected_caption=caption_comment
        )

