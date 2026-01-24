import allure
import pytest

from tests.tests_frontend.conftest import recycle
from tests.tests_frontend.frontend_helpers import generate_box_quantity, selected_delivery_date


@allure.feature('Recycle')
@allure.story('Valid recycle flow')
@pytest.mark.usefixtures('close_cookies_banner')
class TestRecycle:

    @allure.title('User able to recycle small quantity')
    def test_recycle_small_quantity(self, recycle, recycle_page):

        recycle_page = recycle(generate_box_quantity(quantity='small'))

        recycle_page.click_submit()

        recycle_page.check_thanks_for_recycle_toast_appears_on_page()

    @allure.title('User able to recycle bulk quantity and choose date in calendar')
    def test_recycle_bulk_quantity(self, recycle, recycle_page):

        recycle_page = recycle(generate_box_quantity(quantity='bulk'))

        delivery_date = selected_delivery_date()

        recycle_page.submit_bulk_quantity_with_date_set_manually(
            delivery_date
        )

        recycle_page.check_thanks_for_recycle_toast_appears_on_page()


    @allure.title('User able to recycle bulk quantity and set date via text')
    def test_recycle_bulk_quantity_set_date_via_text(self, recycle, recycle_page):
        recycle_page = recycle(generate_box_quantity(quantity='bulk'))

        delivery_date = selected_delivery_date()

        recycle_page.submit_bulk_with_date_set_via_text(
            delivery_date.date
        )

        recycle_page.check_thanks_for_recycle_toast_appears_on_page()




