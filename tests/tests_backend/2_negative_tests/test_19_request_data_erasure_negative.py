import json
from unittest.mock import MagicMock, patch

import allure

from utils.clients.api_client import APIClient

@allure.feature('Data Erasure')
@allure.story('Invalid data erasure flow')
@allure.title('User not able to erase other user data')
def test_erase_other_user_data(headers_with_auth, registered_user_data, login_response, data_erasure):
    client = data_erasure

    CORRECT_ANSWER = "Tony"

    def post_side_effect(url, data=None, headers=None, *args, **kwargs):
        mock_resp = MagicMock()

        # data приходит в виде dict -> сравниваем
        if data.get("securityAnswer") == CORRECT_ANSWER:
            mock_resp.status_code = 200
            mock_resp.json.return_value = {"status": "success"}
        else:
            mock_resp.status_code = 401
            mock_resp.json.return_value = {"error": "invalid security answer"}

        return mock_resp

    with patch.object(client, 'post', side_effect=post_side_effect):

        headers = headers_with_auth.copy()
        headers['Content-Type'] = "application/x-www-form-urlencoded"

        data = {
            'email': login_response.authentication.umail,
            'securityAnswer': registered_user_data.security_answer
        }

        resp = client.request_data_erasure(
            data=data,
            headers=headers
        )

        if registered_user_data.security_answer == CORRECT_ANSWER:
            assert resp.status_code == 200
        else:
            assert resp.status_code == 401