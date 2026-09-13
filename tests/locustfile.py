"""
Locust load test for OWASP Juice Shop.
Based on the API flow in this project's utils/helper.py and data/endpoints.py.

Run:
  locust -f locustfile.py --host=http://127.0.0.1:3000
  # then open http://localhost:8089
"""

import random
from datetime import datetime, timezone

from faker import Faker
from locust import HttpUser, task, between

fake = Faker()

# Mirrors data/constants.py (pick one stable question for load tests)
SECURITY_QUESTIONS = [
    "Your eldest siblings middle name?",
    "Mother's maiden name?",
    "Name of your favorite pet?",
]

DELIVERY_OPTION_IDS = [1, 2, 3]  # data/constants.py DELIVERY_OPTIONS

# Safe products with stock (from your order_generator logic)
PRODUCT_IDS = [1, 2, 3, 4, 5, 6, 7, 8]


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")


def auth_headers(token: str) -> dict:
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }


class JuiceShopUser(HttpUser):
    """
    Each virtual user = one registered Juice Shop customer.
    Setup runs once per user in on_start (like your logged_in_user fixture).
    """

    wait_time = between(1, 3)  # seconds between tasks

    def on_start(self):
        self.token = None
        self.basket_id = None
        self.email = None
        self.password = fake.password(length=12)
        self.security_answer = fake.first_name()

        self._register_and_login()

    def _register_and_login(self):
        question_id = random.randint(1, len(SECURITY_QUESTIONS))
        question_text = SECURITY_QUESTIONS[question_id - 1]
        now = utc_now_iso()

        register_payload = {
            "email": fake.unique.email(),
            "password": self.password,
            "passwordRepeat": self.password,
            "securityQuestion": {
                "id": question_id,
                "question": question_text,
                "createdAt": now,
                "updatedAt": now,
            },
            "securityAnswer": self.security_answer,
        }

        with self.client.post(
            "/api/Users",
            json=register_payload,
            name="POST /api/Users (register)",
            catch_response=True,
        ) as resp:
            if resp.status_code != 201:
                resp.failure(f"Register failed: {resp.status_code} {resp.text}")
                return
            user_id = resp.json()["data"]["id"]
            self.email = register_payload["email"]

        security_payload = {
            "UserId": user_id,
            "SecurityQuestionId": question_id,
            "answer": self.security_answer,
        }

        with self.client.post(
            "/api/SecurityAnswers",
            json=security_payload,
            name="POST /api/SecurityAnswers",
            catch_response=True,
        ) as resp:
            if resp.status_code not in (200, 201):
                resp.failure(f"Security answer failed: {resp.status_code} {resp.text}")
                return

        login_payload = {
            "email": self.email,
            "password": self.password,
        }

        with self.client.post(
            "/rest/user/login",
            json=login_payload,
            name="POST /rest/user/login",
            catch_response=True,
        ) as resp:
            if resp.status_code != 200:
                resp.failure(f"Login failed: {resp.status_code} {resp.text}")
                return
            auth = resp.json()["authentication"]
            self.token = auth["token"]
            self.basket_id = auth["bid"]

    @property
    def headers(self):
        return auth_headers(self.token)

    # --- lightweight read tasks ---

    @task(2)
    def get_delivery_options(self):
        if not self.token:
            return
        self.client.get(
            "/api/Deliverys",
            headers=self.headers,
            name="GET /api/Deliverys",
        )

    @task(2)
    def get_basket(self):
        if not self.token:
            return
        self.client.get(
            f"/rest/basket/{self.basket_id}",
            headers=self.headers,
            name="GET /rest/basket/{bid}",
        )

    @task(2)
    def get_order_history(self):
        if not self.token:
            return
        self.client.get(
            "/rest/order-history",
            headers=self.headers,
            name="GET /rest/order-history",
        )

    @task(3)
    def add_product_to_basket(self):
        if not self.token:
            return

        payload = {
            "ProductId": random.choice(PRODUCT_IDS),
            "BasketId": self.basket_id,
            "quantity": 1,
        }

        with self.client.post(
            "/api/BasketItems",
            json=payload,
            headers=self.headers,
            name="POST /api/BasketItems",
            catch_response=True,
        ) as resp:
            if resp.status_code != 200:
                resp.failure(f"Add to basket failed: {resp.status_code} {resp.text}")

    # --- heavier task: mirrors checkout_factory (lower weight) ---

    @task(1)
    def checkout_flow(self):
        """
        Mirrors your checkout_factory:
        add product -> address -> card -> checkout
        """
        if not self.token:
            return

        # 1) add product
        product_payload = {
            "ProductId": random.choice(PRODUCT_IDS),
            "BasketId": self.basket_id,
            "quantity": 1,
        }
        with self.client.post(
            "/api/BasketItems",
            json=product_payload,
            headers=self.headers,
            name="POST /api/BasketItems (checkout flow)",
            catch_response=True,
        ) as resp:
            if resp.status_code != 200:
                resp.failure(f"Checkout/add product failed: {resp.status_code}")
                return

        # 2) address (mirrors add_address_payload / address_generator_raw)
        address_payload = {
            "fullName": fake.name(),
            "streetAddress": fake.street_address(),
            "mobileNum": int(fake.numerify("##########")),
            "zipCode": fake.postcode()[:8],
            "country": random.choice(["USA", "Germany", "France"]),
            "city": fake.city(),
        }
        with self.client.post(
            "/api/Addresss",
            json=address_payload,
            headers=self.headers,
            name="POST /api/Addresss",
            catch_response=True,
        ) as resp:
            if resp.status_code != 200:
                resp.failure(f"Create address failed: {resp.status_code}")
                return
            address_id = resp.json()["data"]["id"]

        # 3) credit card (mirrors CardGenerator / AddCreditCardRequest)
        card_payload = {
            "fullName": fake.name().upper(),
            "cardNum": int(fake.credit_card_number(card_type="visa").replace("-", "")),
            "expMonth": str(random.randint(1, 12)),
            "expYear": str(random.randint(2080, 2099)),
        }
        with self.client.post(
            "/api/Cards",
            json=card_payload,
            headers=self.headers,
            name="POST /api/Cards",
            catch_response=True,
        ) as resp:
            if resp.status_code != 200:
                resp.failure(f"Create card failed: {resp.status_code}")
                return
            card_id = resp.json()["data"]["id"]

        # 4) checkout (mirrors CheckoutRequestSchema)
        checkout_payload = {
            "couponData": None,
            "orderDetails": {
                "addressId": str(address_id),
                "deliveryMethodId": str(random.choice(DELIVERY_OPTION_IDS)),
                "paymentId": str(card_id),
            },
        }
        with self.client.post(
            f"/rest/basket/{self.basket_id}/checkout",
            json=checkout_payload,
            headers=self.headers,
            name="POST /rest/basket/{bid}/checkout",
            catch_response=True,
        ) as resp:
            if resp.status_code != 200:
                resp.failure(f"Checkout failed: {resp.status_code} {resp.text}")