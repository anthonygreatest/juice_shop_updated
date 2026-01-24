import allure
import pytest

from data.frontend_endpoints import PlaywrightEndpoints

@pytest.mark.usefixtures('close_cookies_banner')
@allure.feature('Localization')
@allure.story('Valid localization flow')
@allure.title('User can change language in shop')
@pytest.mark.parametrize('language, expected_heading_text', [
    ('ru', 'Все товары'),
    ('fr', 'Tous les produits'),
    ('eng', 'All Products')
])
def test_language_on_all_products_page_changes(search_page, language, expected_heading_text):

    search_page.open(PlaywrightEndpoints.ALL_PRODUCTS)
    search_page.reload()

    language_selected = search_page.navbar.change_language(
        language
    )

    search_page.check_language_switched_toast_appears_on_page(language_selected)
    search_page.check_heading_language_gets_switched_to_another_language(expected_heading_text)
