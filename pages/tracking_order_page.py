from components.basket_component import BasketComponent
from data.dataclasses.delivery_data import DeliveryData
from data.dataclasses.selected_product_data import SelectedProductData
from data.locators.tracking_order_page_locators import TrackingOrderPageLocators
from elements.text import Text
from pages.base_page import BasePage
from utils.schemas.delivery_options_resp_schema import DeliveryOptionsRespSchema


class TrackingOrderPage(BasePage):

    def __init__(self, page):
        super().__init__(page)
        self.locators = TrackingOrderPageLocators()
        self.basket = BasketComponent(page)
        self.delivery_date = Text(page, self.locators.delivery_date, 'Delivery Date Text')
        self.tracking_num = Text(page, self.locators.tracking_num, 'Tracking Num Text')

    def check_tracking_data_matches_expected(self, selected_product_data: SelectedProductData,
        delivery_data: DeliveryOptionsRespSchema, tracking_num: str):

        self.basket.product_info.check_have_text(selected_product_data.product_name, nth=0)
        self.basket.product_info.check_contain_text(str(selected_product_data.product_price), nth=3)
        self.delivery_date.check_have_text(f'{str(delivery_data.data.eta)} Days')
        self.tracking_num.check_have_text(tracking_num, nth=1)

