from http import HTTPStatus

import allure

from utils.assertions.base_assertions import assert_status_code
from utils.assertions.register_assertions import assert_user_registered, \
    assert_security_answer_gets_sent
from utils.helper import prepare_register_payload, security_answer_payload, security_answer_set, registered_user
from utils.schemas.register_response_schema import RegisterResponseValidateSchema
from utils.schemas.security_question_resp_schema import SecurityQuestionRespSchema
from utils.validators import validate_response


@allure.feature('User Registration')
@allure.story('Valid registration flow')
class TestRegisterUser:
    @allure.title('User gets registered successfully')
    def test_user_able_to_register(self, register):

        new_user = prepare_register_payload()

        resp = register.register_new_user(
            data=new_user
        )

        validated_response = validate_response(RegisterResponseValidateSchema, resp.json())

        security_answer_set(validated_response, new_user, register)

        assert_status_code(resp, HTTPStatus.CREATED)

        assert_user_registered(validated_response, new_user)

        # контрактное тестирование
        # validate.validate_response(validated_response.model_json_schema(), resp.json())

    @allure.title('Security answer from registered user gets saved')
    def test_security_answer_from_registered_user_gets_saved(self, register):

        formatted_response, new_user = registered_user(
            register=register
        )

        security_answer = security_answer_payload(
            user_id=formatted_response.data.id,
            answer=new_user.security_answer,
            security_question_id=new_user.security_question.id
        )

        set_security_answer_response = register.set_security_answer(security_answer)

        formatted_set_security_answer_response = validate_response(SecurityQuestionRespSchema, set_security_answer_response.json())

        assert_security_answer_gets_sent(formatted_set_security_answer_response, security_answer)


