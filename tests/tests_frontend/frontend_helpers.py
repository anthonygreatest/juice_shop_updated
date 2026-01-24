import random
from dataclasses import asdict
from decimal import Decimal
import allure
import requests
from data.constants2 import NEW_PRODUCTS
from data.dataclasses.delivery_date import DeliveryDate
from data.dataclasses.e_wallet_deposit_data import EWalletDepositData
from data.dataclasses.exported_data import ExportedData
from data.dataclasses.feedback_data import FeedbackData
from data.factory import DataFactory
from data.frontend_endpoints import PlaywrightEndpoints
from pages.login_page import LoginPage
from utils.helper import prepare_register_payload
from utils.schemas.data_export_resp_schema import DataExportRespSchemaInside
from data.dataclasses.selected_product_data import SelectedProductData

@allure.step('Preparing card payload for UI')
def prepare_card_payload_for_ui():

    data = DataFactory.get_generator('credit_card').create_credit_card()

    return asdict(data)

def calculate_current_balance(deposit_data: EWalletDepositData):
    current_balance = deposit_data.deposit_payload.balance + deposit_data.balance_before_deposit.data
    return current_balance

@allure.step('Formatting register payload for UI')
def formatted_register_payload_for_ui() -> dict:
    new_user = prepare_register_payload()

    data = new_user.model_dump(mode='json')
    data['security_question'] = new_user.security_question.question

    return data

def log_in_user(data, login_page: LoginPage):

    try:
        login_page.dismiss_banner()
    except:
        print('Welcome banner not found')

    if isinstance(data, dict):
        payload = data
    else:
        payload = data.model_dump()

    login_page.login_form.fill(
       **payload
    )

    return login_page

def increase_product_quantity(basket_page, expected_num):
    for _ in range(expected_num - 1):
        basket_page.plus_one()

def find_product_by_id(product_id):
    for product in NEW_PRODUCTS:
        if product['id'] == product_id:
            return SelectedProductData(
                product_name=product['name'],
                product_price=Decimal(str(product['price']))
            )

def get_token(state):
    for origin in state["origins"]:
        for item in origin.get('localStorage', []):
            if item["name"] == 'token':
                token = item["value"]
                return token

def generate_box_quantity(quantity):
    if quantity == 'bulk':
        return str(random.randint(101, 1000))
    elif quantity == 'small':
        return str(random.randint(10, 100))
    else:
        return Exception('Quantity not supported')

def get_items_per_page(page_num: int, total_pages: int, search_page):

    items_per_page = search_page.count_products_on_page()
    last_item = page_num * items_per_page
    first_item = last_item - items_per_page + 1

    return f'{first_item} – {last_item} of {total_pages}'

def calculate_final_price(sale, price, delivery_fee):

    sale_sum = round(Decimal(int(sale)/100) * Decimal(price), 2)

    expected_final_price = round(Decimal(price) - sale_sum + Decimal(delivery_fee), 2)

    return sale_sum, expected_final_price

def selected_delivery_date() -> DeliveryDate:
    selected_date = DataFactory.get_generator('date_generator').date_generator()

    return selected_date

def compile_list_of_orders(exported_user_data: DataExportRespSchemaInside):

    list_of_orders = []
    for order in exported_user_data.orders:
        for item in order.products:
            list_of_orders.append(ExportedData(
                name=item.name,
                total_price=Decimal(str(order.total_price)),
                order_id=order.order_id,
                delivery_date=int(order.eta)
            ))

    return list_of_orders

def get_captcha_text(request_data_export_page):
    with request_data_export_page.page.expect_response('**/rest/image-captcha/') as response_info:
        request_data_export_page.page.reload()

    response = response_info.value
    captcha_answer = response.json()['answer']

    return captcha_answer

def generate_feedback() -> FeedbackData:

    feedback = DataFactory.get_generator('feedback_generator').generate_feedback()

    return feedback

def log_out_and_log_in(current_page, login_data):
    current_page.navbar.log_out()

    login_page = LoginPage(current_page.page)
    login_page.open(PlaywrightEndpoints.LOGIN)
    login_page = log_in_user(
        login_data,
        login_page
    )
    login_page.click_login_btn()

def find_out_product_price(product_name):
    for product in NEW_PRODUCTS:
        if product['name'] == product_name:
            return Decimal(str(product['price']))

def get_ids_of_products(page):

    context = page.context
    state = context.storage_state()

    headers = {
        'Authorization': f'Bearer {get_token(state)}',
        'Content-Type': 'application/json'
    }

    resp = requests.get(
        url='http://localhost:3000/api/Quantitys',
        headers=headers
    )

    products = resp.json()['data']

    resp2 = requests.get(
        url='http://127.0.0.1:3000/rest/products/search?q=',
        headers=headers
    )
    product_names = {i['id']: i['name'] for i in resp2.json()['data']}


    with open(r'C:\Users\user\PycharmProjects\PythonProject10\data\constants2.py', 'w', encoding='utf-8') as f:
        products_list = []
        for i in products:
            products_list.append({'id': (i['ProductId']), 'quantity': i['quantity'], 'limit_per_user': i['limitPerUser']})

        for item in products_list:
            if item['id'] in product_names:
                item['name'] = product_names[item['id']]

        f.write(f'NEW_PRODUCTS = {products_list}')

    print('DONE')

