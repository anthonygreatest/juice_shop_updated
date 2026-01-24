import allure

from utils.assertions.base_assertions import assert_match
from utils.logger import get_logger
from utils.schemas.register_response_schema import RegisterResponseValidateSchema
from utils.schemas.saved_pics_resp_schema import SavedPicsRespSchema
from utils.schemas.upload_photo_resp_schema import UploadPhotoRespSchema

logger = get_logger("PHOTO_WALL_ASSERTIONS")

@allure.step('Checking user able to upload photo')
def assert_uploaded_photo_data_matches_actual_data(response: UploadPhotoRespSchema,
    expected_user_id: RegisterResponseValidateSchema,
    expected_caption: str):

    logger.info('Checking user able to upload photo')

    assert_match(response.data.user_id, expected_user_id.data.id, 'user id')
    assert_match(response.data.caption, expected_caption, 'caption')

@allure.step('Checking uploaded photo gets saved')
def assert_uploaded_photo_gets_saved(response: SavedPicsRespSchema,
    expected_user_data: RegisterResponseValidateSchema,
    expected_caption: str):

    logger.info('Checking uploaded photo gets saved')

    matched = next((post for post in response.data if post.user_id == expected_user_data.data.id),
        None)

    assert_match(matched.user_id, expected_user_data.data.id, 'user id')
    assert_match(matched.user.email, expected_user_data.data.email, 'email')
    assert_match(matched.caption, expected_caption, 'caption')