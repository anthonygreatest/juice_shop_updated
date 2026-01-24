import allure
import pytest
from pathlib import Path
from playwright.sync_api import Playwright
from config_ui import SettingsUI
from data.dataclasses.set_order_data import SetOrderData
from data.frontend_endpoints import PlaywrightEndpoints
from data.locators.payment_options_page_locators import PaymentOptionsPageLocators
from pages.about_us_page import AboutUsPage
from pages.address_page import AddressPage
from pages.all_products_page import AllProductsPage
from pages.basket_page import BasketPage
from pages.change_password_page import ChangePasswordPage
from pages.chatbot_page import ChatbotPage
from pages.checkout_page import CheckoutPage
from pages.complaint_page import ComplaintPage
from pages.completion_page import CompletionPage
from pages.crypto_wallet_page import CryptoWalletPage
from pages.customer_feedback_page import CustomerFeedbackPage
from pages.delivery_options_page import DeliveryOptionsPage
from pages.deluxe_memebership_page import DeluxeMembershipPage
from pages.digital_wallet_page import DigitalWalletPage
from pages.login_page import LoginPage
from pages.order_history_page import OrderHistoryPage
from pages.payment_options_page import PaymentOptionsPage
from pages.payment_wallet_page import PaymentWalletPage
from pages.photo_wall_page import PhotoWallPage
from pages.profile_page import ProfilePage
from pages.recyle_page import RecyclePage
from pages.register_page import RegisterPage
from pages.request_data_export_page import RequestDataExportPage
from pages.request_erasure_page import RequestErasurePage
from pages.saved_addresses_page import SavedAddressesPage
from pages.saved_cards_page import SavedCardsPage
from pages.select_address_page import SelectAddressPage
from pages.tracking_order_page import TrackingOrderPage
from tests.tests_frontend.frontend_helpers import get_token, log_in_user, \
  find_product_by_id

from utils.helper import register_user_and_set_security_answer, \
    select_delivery_speed, prepare_review_payload, deposit_to_digital_wallet_payload, deposit_money_to_e_wallet, \
    prepare_change_password_in_acc_payload, add_address_basic_data, add_address_payload
from utils.schemas.login_response_schema import LoginResponseSchema


# -----------------------PLAYWRIGHT FIXTURES-------------------------


@pytest.fixture(scope='session')
def settings_ui():
    return SettingsUI.initialize()


@pytest.fixture
def unauth_page(playwright: Playwright, settings_ui: SettingsUI, request):

    browser = playwright.chromium.launch(headless=settings_ui.headless, slow_mo=settings_ui.slow_mo)
    context = browser.new_context(base_url=f'{settings_ui.app_url}', record_video_dir=settings_ui.videos_dir)
    page = context.new_page()
    yield page
    page.close()
    context.close()
    browser.close()

    allure.attach.file(
        page.video.path(),
        name='video',
        attachment_type=allure.attachment_type.WEBM
    )

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    #раним тест
    outcome = yield
    #получаем TestReport
    report = outcome.get_result()

    if report.when != 'call':
        return

    # item = test, funcargs = словарь всех фикстур, к-е были переданы в тест
    page = item.funcargs.get('unauth_page') or item.funcargs.get('auth_page')
    video_path = getattr(item, 'video_path', None)

    if isinstance(page, tuple):
        page = page[0]

    if page and not page.is_closed():
        if report.failed:
            screenshot = page.screenshot()
            allure.attach(
                screenshot,
                name='screenshot_on_failure',
                attachment_type=allure.attachment_type.PNG
            )

        elif report.passed and 'screenshot' in item.keywords:
            screenshot = page.screenshot()
            allure.attach(
                screenshot,
                name='screenshot',
                attachment_type=allure.attachment_type.PNG
            )

    # if video_path and (
    #     report.failed or 'video' in item.keywords
    # ):
    #     allure.attach.file(
    #         video_path,
    #         name='video',
    #         attachment_type=allure.attachment_type.MP4
    #     )

@pytest.fixture
def register_page(unauth_page):
    return RegisterPage(unauth_page)

@pytest.fixture
def login_page(unauth_page):
    return LoginPage(unauth_page)

@pytest.fixture
def main_page(unauth_page):
    return AllProductsPage(unauth_page)

@pytest.fixture
def forgot_your_password_page(unauth_page):
    return ChangePasswordPage(unauth_page)

@pytest.fixture
def change_password_after_login_page(register, unauth_page):

    register_response, new_user = register_user_and_set_security_answer(register)

    new_data = prepare_change_password_in_acc_payload(
        old_user_password=new_user.password,
        email=new_user.email,
        answer=new_user.security_answer
    )
    new_data['email'] = new_user.email

    login_page = LoginPage(unauth_page)
    login_page.open(PlaywrightEndpoints.LOGIN)
    login_page = log_in_user(
        new_user,
        login_page
    )
    login_page.click_login_btn()


    return ChangePasswordPage(login_page.page), new_data


@pytest.fixture(scope='session')
def logged_in(playwright: Playwright, settings_ui: SettingsUI, register):
    browser = playwright.chromium.launch(headless=settings_ui.headless, slow_mo=settings_ui.slow_mo)
    context = browser.new_context(base_url=f'{settings_ui.app_url}', record_video_dir=settings_ui.videos_dir)
    page = context.new_page()

    register_response, new_user = register_user_and_set_security_answer(register)

    login_page = LoginPage(page)
    login_page.open(PlaywrightEndpoints.LOGIN)
    login_page = log_in_user(
        new_user,
        login_page
    )
    with page.expect_response('**/rest/user/login') as response_info:
        login_page.click_login_btn()

    response = response_info.value
    bid = response.json()

    context.storage_state(path='auth.json')

    # get_ids_of_products(login_page.page)

    yield page, bid, register_response, new_user

    page.close()
    context.close()
    browser.close()

    allure.attach.file(
        page.video.path(),
        name='video',
        attachment_type=allure.attachment_type.WEBM
    )

@pytest.fixture(scope='session')
def auth_page(logged_in):

    page, _, _, _ = logged_in

    return page

@pytest.fixture
def basket_id(logged_in):

    _, bid, _, _ = logged_in

    return LoginResponseSchema(**bid)

@pytest.fixture
def register_response_via_ui(logged_in):

    _, _, register_response, _ = logged_in

    return register_response

@pytest.fixture
def user_register_data_via_ui(logged_in):

    _, _, _, new_user = logged_in

    return new_user

@pytest.fixture
def get_headers(auth_page):

    context = auth_page.context
    state = context.storage_state()

    headers = {
        'Authorization': f'Bearer {get_token(state)}',
        'Content-Type': 'application/json'
    }

    return headers

# @pytest.fixture
# def open_page(auth_page):
#     # page, user = auth_page
#     def _open(page_class, url):
#         class_page = page_class(auth_page, url)
#         class_page.open()
#         return class_page
#     return _open

@pytest.fixture
def search_page(auth_page):
    return AllProductsPage(auth_page)

@pytest.fixture
def basket_page(auth_page):
    return BasketPage(auth_page)

@pytest.fixture
def put_product_into_basket(request, get_headers, basket, basket_page, search_page):

    orders = []

    def _product_added_into_basket(product):

        with search_page.page.expect_response('**/api/BasketItems/') as response_info:
            search_page.find_and_add_product_to_basket(product)

        response = response_info.value
        order_id = response.json()['data']['id']
        orders.append(order_id)

        return

    yield _product_added_into_basket

    if 'delete_product' in request.keywords:
        for order_id in orders:
            basket.delete_product_from_basket(
                order_id=order_id,
                headers=get_headers
            )
        basket_page.reload()

@pytest.fixture
def select_address_page(auth_page):
    return SelectAddressPage(auth_page)

@pytest.fixture
def address_page(auth_page):
    return AddressPage(auth_page)

@pytest.fixture
def delivery_options_page(auth_page):
    return DeliveryOptionsPage(auth_page)

@pytest.fixture
def add_new_address(request, address, select_address_page, auth_page, get_headers):

    addresses = []

    def _add_new_address(address_page, address_data):

        address_page.address_form.fill(
            **address_data
        )
        with auth_page.expect_response('**/api/Addresss/**') as response_info:
            address_page.click_submit()

        response = response_info.value
        order_id = response.json()['data']['id']
        addresses.append(order_id)

        return

    yield _add_new_address

    if 'delete_address' in request.keywords:
        for address_id in addresses:
            address.delete_address(
                address_id=address_id,
                headers=get_headers
            )

@pytest.fixture
def digital_wallet_page(auth_page):
    return DigitalWalletPage(auth_page)

@pytest.fixture
def close_cookies_banner(auth_page):

    try:
        auth_page.wait_for_selector(PaymentOptionsPageLocators.accept_cookies_btn, timeout=500)
        auth_page.click(PaymentOptionsPageLocators.accept_cookies_btn)
    except:
        print('Cookies banner not found')

@pytest.fixture
def payment_options_page(auth_page):
    return PaymentOptionsPage(auth_page)

@pytest.fixture
def checkout_page(auth_page):
    return CheckoutPage(auth_page)

@pytest.fixture
def crypto_wallet_page(auth_page):
    return CryptoWalletPage(auth_page)

@pytest.fixture
def saved_cards_page(auth_page):
    return SavedCardsPage(auth_page)

@pytest.fixture
def add_credit_card(request, auth_page, credit_card, get_headers):

    created_cards = []

    def _credit_card(payment_options_page: PaymentOptionsPage):

        with auth_page.expect_response('**/api/Cards/') as response_info:
            payment_options_page.card_form.click_submit()

        response = response_info.value

        card_id = response.json()['data']['id']
        created_cards.append(card_id)

        return

    yield _credit_card

    if 'delete_card' in request.keywords:
        for card_id in created_cards:
            credit_card.delete_credit_card(
                card_id=card_id,
                headers=get_headers
            )

@pytest.fixture
def user_at_checkout(add_product_to_basket, create_address, get_headers, basket_id, create_credit_card,
                     basket_page, select_address_page, delivery_options_page, digital_wallet,
                     navigate_to_payment_options_page):

    added_product = add_product_to_basket(
        headers=get_headers,
        login_response=basket_id
    ).added_product
    selected_product_data = find_product_by_id(product_id=added_product.product_id)
    address_data = create_address(headers=get_headers)
    card_data = create_credit_card(headers=get_headers)
    deposit_data = deposit_money_to_e_wallet(
        card_data.added_card.data.id,
        get_headers,
        digital_wallet,
        'random'
    )
    delivery_data = select_delivery_speed()

    navigate_to_payment_options_page(delivery_data.delivery_date)

    return SetOrderData(
        selected_product_data=selected_product_data,
        address_data=address_data.address_payload,
        card_data=card_data.card_payload,
        delivery_data=delivery_data,
        deposit_data=deposit_data
    )

@pytest.fixture
def order_completion_page(auth_page):
    return CompletionPage(auth_page)

@pytest.fixture
def tracking_order_page(auth_page):
    return TrackingOrderPage(auth_page)

@pytest.fixture
def order_history_page(auth_page):
    return OrderHistoryPage(auth_page)

@pytest.fixture
def payment_wallet_page(auth_page):
    return PaymentWalletPage(auth_page)

@pytest.fixture
def write_review(basket_id, checkout_factory, get_headers):

    def _write_review(review_page, url):

        checkout_factory(e_wallet=False, headers=get_headers, login_response=basket_id)
        review_text = prepare_review_payload(basket_id.authentication.umail)

        review_page.open(url)
        review_page.write_review(review_text.message)

        return review_text

    return _write_review

@pytest.fixture
def recycle_page(auth_page):
    return RecyclePage(auth_page)

@pytest.fixture
def recycle(recycle_page, add_new_address, get_headers, create_address):
    def _recycle(quantity):

        create_address(headers=get_headers)

        recycle_page.open(PlaywrightEndpoints.RECYCLE)
        recycle_page.reload()

        recycle_page.recycle_and_select_address(
            quantity
        )

        return recycle_page

    return _recycle


@pytest.fixture
def saved_addresses_page(auth_page):
    return SavedAddressesPage(auth_page)

@pytest.fixture
def data_erasure_page(auth_page):
    return RequestErasurePage(auth_page)

@pytest.fixture
def request_data_export_page(auth_page):
    return RequestDataExportPage(auth_page)

@pytest.fixture
def order_for_data_export(request_data_export_page, checkout_factory, get_headers, basket_id):

    order_data = checkout_factory(
        e_wallet=False,
        headers=get_headers,
        login_response=basket_id
    )

    return order_data

@pytest.fixture
def customer_feedback_page(auth_page):
    return CustomerFeedbackPage(auth_page)

@pytest.fixture
def profile_page(auth_page):
    return ProfilePage(auth_page)


@pytest.fixture
def updated_profile(profile_page):

    picture_path = Path(__file__).parent / 'pictures' / 'profile_picture.jpg'
    profile_page.open(PlaywrightEndpoints.PROFILE_PAGE)

    profile_page.upload_picture(
        picture_path
    )
    pic_src_after_update = profile_page.get_picture()

    name = add_address_payload().full_name

    profile_page.set_username(
        name
    )

    return pic_src_after_update, name


@pytest.fixture
def chatbot_page(auth_page):
    return ChatbotPage(auth_page)

@pytest.fixture
def deluxe_membership_page(auth_page):
    return DeluxeMembershipPage(auth_page)


@pytest.fixture
def sum_deposited_into_e_wallet(get_headers, create_credit_card, digital_wallet):

    card_to_be_added = create_credit_card(get_headers).added_card

    e_wallet_data = deposit_money_to_e_wallet(
        payment_id=card_to_be_added.data.id,
        headers=get_headers,
        digital_wallet=digital_wallet,
        balance=49
    )

    deposit = e_wallet_data.deposit_payload.balance
    balance_before_deposit = e_wallet_data.balance_before_deposit.data

    return deposit, balance_before_deposit

@pytest.fixture
def photo_wall_page(auth_page):
    return PhotoWallPage(auth_page)

@pytest.fixture
def complaint_page(auth_page):
    return ComplaintPage(auth_page)

@pytest.fixture
def about_us_page(auth_page):
    return AboutUsPage(auth_page)

@pytest.fixture
def navigate_to_payment_options_page(basket_page, select_address_page, delivery_options_page, payment_options_page):
    def _navigate_to_payment_options_page(delivery_option):

        basket_page.open(PlaywrightEndpoints.BASKET)
        basket_page.click_checkout()
        select_address_page.select_address_and_continue()
        delivery_options_page.select_delivery_option_and_continue(days=delivery_option)

        return
    return _navigate_to_payment_options_page

