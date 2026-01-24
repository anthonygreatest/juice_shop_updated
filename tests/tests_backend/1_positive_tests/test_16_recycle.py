from http import HTTPStatus
import allure

from tests.conftest import recycle_factory
from utils.assertions.base_assertions import assert_status_code
from utils.assertions.recycle_assertions import assert_recycle_request_gets_sent
from utils.schemas.recycle_resp_schema import RecycleRespSchema
from utils.validators import validate_response


@allure.feature('Recycle')
@allure.story('Valid recycle flow')
class TestRecycle:

    @allure.title('User able to recycle without pickup')
    def test_user_able_to_recycle_without_pickup(self, recycle_factory, headers_with_auth, create_address):

        response, recycle_payload = recycle_factory(pickup_needed=False)

        validated_response = validate_response(RecycleRespSchema, response.json())

        assert_status_code(response, HTTPStatus.CREATED)

        assert_recycle_request_gets_sent(validated_response, recycle_payload)

    @allure.title('User able to recycle without pickup')
    def test_user_able_to_recycle_with_pickup(self, recycle_factory):

        response, recycle_payload = recycle_factory(pickup_needed=True)

        validated_response = validate_response(RecycleRespSchema, response.json())

        assert_status_code(response, HTTPStatus.CREATED)

        assert_recycle_request_gets_sent(validated_response, recycle_payload)