from http import HTTPStatus

import allure

from utils.assertions.base_assertions import assert_status_code
from utils.helper import prepare_chatbot_query
from utils.schemas.robot_resp_schema import RobotRespSchema
from utils.validators import validate_response


@allure.feature('Chat Robot')
@allure.story('Valid chat robot flow')
@allure.title('User able to send message to chatbot')
def test_ask_robot(chatbot, login_response, headers_with_auth):

    name = login_response.authentication.umail

    chatbot_query = prepare_chatbot_query(name)

    response = chatbot.ask_robot(
        data=chatbot_query,
        headers=headers_with_auth
    )

    validate_response(RobotRespSchema, response.json())

    assert_status_code(response, HTTPStatus.OK)

