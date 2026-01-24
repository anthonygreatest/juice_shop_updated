from http import HTTPStatus

import allure
from utils.assertions.base_assertions import assert_status_code
from utils.assertions.complaint_assertions import assert_user_complaint_gets_sent
from utils.helper import prepare_user_message
from utils.schemas.send_complaint_resp_schema import SendComplaintRespSchema
from utils.validators import validate_response


@allure.feature('Complaint')
@allure.story('Valid complaint flow')
@allure.title('User able to file a complaint')
def test_user_able_to_file_a_complaint(complaints, headers_with_auth, register_response):

    complaint_to_send = prepare_user_message(
        user_id=register_response.data.id,
        message_type='complaint'
    )

    response = complaints.file_a_complaint(
        data=complaint_to_send,
        headers=headers_with_auth
    )

    validated_response = validate_response(SendComplaintRespSchema, response.json())

    assert_status_code(response, HTTPStatus.CREATED)
    assert_user_complaint_gets_sent(validated_response, complaint_to_send)

