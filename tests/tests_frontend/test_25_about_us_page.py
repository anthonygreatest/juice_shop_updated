import allure
import pytest

from data.frontend_endpoints import PlaywrightEndpoints
from data.locators.about_us_page_locators import AboutUsPageLocators
from pages.about_us_page import AboutUsPage
from utils.assertions.about_us_assertions import assert_outer_source_link_present_on_about_us_page


@allure.feature('About Us')
@allure.story('Valid about us flow')
@allure.title('User can access links to outer resources')
@pytest.mark.usefixtures('close_cookies_banner')
@pytest.mark.parametrize('locator, expected_link', [
    (AboutUsPageLocators.bluesky, AboutUsPage.BLUESKY_LINK),
    (AboutUsPageLocators.mastodon, AboutUsPage.MASTODON_LINK),
    (AboutUsPageLocators.facebook, AboutUsPage.FACEBOOK_LINK),
    (AboutUsPageLocators.twitter, AboutUsPage.TWITTER_LINK),
    (AboutUsPageLocators.reddit, AboutUsPage.REDDIT_LINK),
    (AboutUsPageLocators.press_kit, AboutUsPage.PRESS_KIT_LINK),
    (AboutUsPageLocators.nft, AboutUsPage.NFT_LINK),
    (AboutUsPageLocators.slack, AboutUsPage.SLACK_LINK),
    (AboutUsPageLocators.terms_of_use, AboutUsPage.TERMS_OF_USE_LINK)
])
def test_outer_source_links_available(about_us_page, locator, expected_link):

    about_us_page.open(PlaywrightEndpoints.ABOUT_US)
    link = about_us_page.get_outer_source_link(locator)

    assert_outer_source_link_present_on_about_us_page(
        actual_link=link,
        expected_link=expected_link
    )
