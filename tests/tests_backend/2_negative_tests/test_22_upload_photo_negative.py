from http import HTTPStatus
import allure
import pytest
from data.paths import FOR_COMPLAINT_PICTURE, DUMMY_IMAGE
from utils.assertions.base_assertions import assert_status_code
from utils.helper import prepare_file_for_upload


@allure.feature('Photo Wall')
@allure.story('Invalid photo wall flow')
class TestPhotoWallNegative:

    @allure.title('User not able to upload photo without caption')
    @pytest.mark.parametrize('field, value, expected', [
        ('image', (None, open(DUMMY_IMAGE, 'rb'), 'image/png'), HTTPStatus.BAD_REQUEST),
        ('image', (None, 'abc', 'image/png'), HTTPStatus.BAD_REQUEST),
        ('image', (None, 123, 'image/png'), HTTPStatus.BAD_REQUEST),
        ('image', (None, open(FOR_COMPLAINT_PICTURE, 'rb'), 'doc'), HTTPStatus.BAD_REQUEST),
        ('image', ('THE MISTAKE', open(FOR_COMPLAINT_PICTURE, 'rb'), 'image/png'), HTTPStatus.OK),
        ('caption', (None, True), HTTPStatus.BAD_REQUEST),
        ('caption', (None, 'a'*200), HTTPStatus.BAD_REQUEST),
        ('caption', (None, None), HTTPStatus.BAD_REQUEST),
        ('caption', (None, 'Fix this mistake already'), HTTPStatus.OK),
    ])
    def test_upload_photo_without_caption(self, photo_wall, headers_with_auth, field, value, expected):

        file_name = 'for_complaint.png'
        caption_comment = 'Fix this mistake already'

        file, new_headers, data = prepare_file_for_upload(
            picture=FOR_COMPLAINT_PICTURE,
            file_name=file_name,
            caption_comment=caption_comment,
            headers_with_auth=headers_with_auth
        )

        file[field] = value

        response = photo_wall.upload_photo(
            files=file,
            data=data,
            headers=new_headers
        )

        assert_status_code(response, expected)

    @allure.title('User not able to upload photo with missing fields')
    @pytest.mark.parametrize('missing_field, expected', [
        ('image', HTTPStatus.BAD_REQUEST),
        ('caption', HTTPStatus.BAD_REQUEST)
    ])
    def test_upload_photo_missing_fields(self, photo_wall, headers_with_auth, missing_field, expected):

        file_name = 'for_complaint.png'
        caption_comment = 'Fix this mistake already'

        file, new_headers, data = prepare_file_for_upload(
            picture=FOR_COMPLAINT_PICTURE,
            file_name=file_name,
            caption_comment=caption_comment,
            headers_with_auth=headers_with_auth
        )

        file.pop(missing_field)

        response = photo_wall.upload_photo(
            files=file,
            data=data,
            headers=new_headers
        )

        assert_status_code(response, expected)

    @allure.title('User not able to upload photo with missing auth header')
    def test_upload_photo_missing_auth(self, photo_wall, headers_with_auth):

        file_name = 'for_complaint.png'
        caption_comment = 'Fix this mistake already'

        file, new_headers, data = prepare_file_for_upload(
            picture=FOR_COMPLAINT_PICTURE,
            file_name=file_name,
            caption_comment=caption_comment,
            headers_with_auth=headers_with_auth
        )

        new_headers.pop('Authorization')

        response = photo_wall.upload_photo(
            files=file,
            data=data,
            headers=new_headers
        )

        assert_status_code(response, HTTPStatus.UNAUTHORIZED)
