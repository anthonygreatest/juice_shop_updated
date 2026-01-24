from unittest.mock import patch, MagicMock
from utils.clients.api_client import APIClient

def test_user_register_mock():

    client = APIClient()
    mock_response = MagicMock()

    mock_response.json.return_value = {"status": "success",
        "data": {
            "username": "",
            "role": "customer",
            "deluxeToken": "",
            "lastLoginIp": "0.0.0.0",
            "profileImage": "/assets/public/images/uploads/default.svg",
            "isActive": True,
            "id": 25,
            "email": "grig.2001@list.ru",
            "updatedAt": "2025-12-10T19:54:26.602Z",
            "createdAt": "2025-12-10T19:54:26.602Z",
            "deletedAt": None
        }
    }

    with patch.object(client.session, 'post', return_value=mock_response) as mock_post:

        user_data = {"email": "grig.2001@list.ru",
            "password": "tony1806",
            "passwordRepeat": "tony1806",
            "securityAnswer": "Infinite Jest",
            "securityQuestion": {
                "id": 11,
                "question": "Your favorite book?",
                "createdAt": "2025-12-10T19:21:27.593Z",
                "updatedAt": "2025-12-10T19:21:27.593Z"
            }
        }

        resp = client.register_user(user_data)

        assert resp.json()['status'] == 'success'
        assert resp.json()['data']['email'] == 'grig.2001@list.ru'

        mock_post.assert_called_once_with(
            url=client.endpoints.register,
            data=user_data,
            headers=None
        )

def test_login_mock():

    client = APIClient()
    mock_response = MagicMock()

    mock_response.json.return_value = {
    "authentication": {
        "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJzdGF0dXMiOiJzdWNjZXNzIiwiZGF0YSI6eyJpZCI6MjUsInVzZXJuYW1lIjoiIiwiZW1haWwiOiJncmlnLjIwMDFAbGlzdC5ydSIsInBhc3N3b3JkIjoiNTQzZTY3ODE0YmFjZDQwODQ5OTVjZTJkN2M4N2ZkYTMiLCJyb2xlIjoiY3VzdG9tZXIiLCJkZWx1eGVUb2tlbiI6IiIsImxhc3RMb2dpbklwIjoiMC4wLjAuMCIsInByb2ZpbGVJbWFnZSI6Ii9hc3NldHMvcHVibGljL2ltYWdlcy91cGxvYWRzL2RlZmF1bHQuc3ZnIiwidG90cFNlY3JldCI6IiIsImlzQWN0aXZlIjp0cnVlLCJjcmVhdGVkQXQiOiIyMDI1LTEyLTEwIDE5OjU0OjI2LjYwMiArMDA6MDAiLCJ1cGRhdGVkQXQiOiIyMDI1LTEyLTEwIDE5OjU0OjI2LjYwMiArMDA6MDAiLCJkZWxldGVkQXQiOm51bGx9LCJpYXQiOjE3NjU0MDMxNzV9.hlXnN-gQ9oawqxdHNv6zn4fkTsbOC8-vbqM_jd0MSGfvQSQPGA8UeQhz6jlnXzUPdMjU0UAtpOa9jlPst1CQTtiSW4ym4nQwFuJaAxQmzCRpMfDS_3SkFULdG66z8voQ3VADTOxV9Rt7ch1dtXnIEIW_s7FyQshqf-qZTOcX_Fg",
        "bid": 8,
        "umail": "grig.2001@list.ru"
        }
    }

    with patch.object(client.session, 'post', return_value=mock_response) as mock_post:

        data = {"email": "grig.2001@list.ru",
                "password": "tony1806"}

        rsp = client.login_user(data)

        assert rsp.json()['authentication']['umail'] == 'grig.2001@list.ru'

        mock_post.assert_called_once_with(
            url=client.endpoints.login,
            data=data,
            headers=None
        )

def test_product_in_basket():

    client = APIClient()
    mock_response = MagicMock()

    mock_response.json.return_value = {
    "status": "success",
    "data": {
        "id": 8,
        "coupon": None,
        "UserId": 25,
        "createdAt": "2025-12-10T21:46:14.559Z",
        "updatedAt": "2025-12-10T21:46:14.559Z",
        "Products": [
            {
                "id": 1,
                "name": "Apple Juice (1000ml)",
                "description": "The all-time classic.",
                "price": 1.99,
                "deluxePrice": 0.99,
                "image": "apple_juice.jpg",
                "createdAt": "2025-12-10T19:21:36.664Z",
                "updatedAt": "2025-12-10T19:21:36.664Z",
                "deletedAt": None,
                "BasketItem": {
                    "ProductId": 1,
                    "BasketId": 8,
                    "id": 13,
                    "quantity": 1,
                    "createdAt": "2025-12-10T21:59:32.650Z",
                    "updatedAt": "2025-12-10T21:59:32.650Z"
                }
            }
        ]
    }
}
    with patch.object(client.session, 'get', return_value=mock_response) as mock_get:

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJzdGF0dXMiOiJzdWNjZXNzIiwiZGF0YSI6eyJpZCI6MjUsInVzZXJuYW1lIjoiIiwiZW1haWwiOiJncmlnLjIwMDFAbGlzdC5ydSIsInBhc3N3b3JkIjoiNTQzZTY3ODE0YmFjZDQwODQ5OTVjZTJkN2M4N2ZkYTMiLCJyb2xlIjoiY3VzdG9tZXIiLCJkZWx1eGVUb2tlbiI6IiIsImxhc3RMb2dpbklwIjoiMC4wLjAuMCIsInByb2ZpbGVJbWFnZSI6Ii9hc3NldHMvcHVibGljL2ltYWdlcy91cGxvYWRzL2RlZmF1bHQuc3ZnIiwidG90cFNlY3JldCI6IiIsImlzQWN0aXZlIjp0cnVlLCJjcmVhdGVkQXQiOiIyMDI1LTEyLTEwIDE5OjU0OjI2LjYwMiArMDA6MDAiLCJ1cGRhdGVkQXQiOiIyMDI1LTEyLTEwIDE5OjU0OjI2LjYwMiArMDA6MDAiLCJkZWxldGVkQXQiOm51bGx9LCJpYXQiOjE3NjU0MDMxNzV9.hlXnN-gQ9oawqxdHNv6zn4fkTsbOC8-vbqM_jd0MSGfvQSQPGA8UeQhz6jlnXzUPdMjU0UAtpOa9jlPst1CQTtiSW4ym4nQwFuJaAxQmzCRpMfDS_3SkFULdG66z8voQ3VADTOxV9Rt7ch1dtXnIEIW_s7FyQshqf-qZTOcX_Fg'
        }
        resp = client.get_product_in_basket(headers)

        assert resp.json()['status'] == 'success'

        assert resp.json()['data']['Products'][0]['name'] == 'Apple Juice (1000ml)'

        mock_get.assert_called_once_with(
            url=client.endpoints.basket,
            headers=headers
        )
