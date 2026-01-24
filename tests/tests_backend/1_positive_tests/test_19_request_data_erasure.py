from unittest.mock import MagicMock, patch

import allure
from utils.helper import prepare_data_erasure, user_logged_in


@allure.feature('Data Erasure')
@allure.story('Valid data erasure flow')
@allure.title('User able to erase their data')
def test_user_able_to_erase_data(headers_with_auth, registered_user_data, login, data_erasure):

    client = data_erasure
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {
        'status': 'success'
    }

    with patch.object(client, 'post', return_value=mock_resp) as mock_post:

        headers = headers_with_auth.copy()
        headers['Content-Type'] = "application/x-www-form-urlencoded"

        register_data = registered_user_data
        user_logged_in(register_data.email, register_data.password, login)

        data = prepare_data_erasure(register_data.email, register_data.security_answer)

        resp = client.request_data_erasure(
            data=data,
            headers=headers
        )

        assert resp.status_code == 200

        mock_post.assert_called_once_with(
            url=client.endpoints.data_erasure,
            data=data,
            headers=headers
        )


