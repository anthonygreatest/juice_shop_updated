from components.gallery_component import GalleryComponent
from data.locators.about_us_page_locators import AboutUsPageLocators
from elements.link import Link
from pages.base_page import BasePage
from pages.mixins import LinkAccessMixin


class AboutUsPage(BasePage, LinkAccessMixin):

    BLUESKY_LINK = 'https://bsky.app/profile/owasp-juice.shop'
    MASTODON_LINK = 'https://fosstodon.org/@owasp_juiceshop'
    TWITTER_LINK = 'https://twitter.com/owasp_juiceshop'
    FACEBOOK_LINK = 'https://www.facebook.com/owasp.juiceshop'
    SLACK_LINK = 'https://owasp.org/slack/invite'
    REDDIT_LINK = 'https://www.reddit.com/r/owasp_juiceshop'
    PRESS_KIT_LINK = 'https://github.com/OWASP/owasp-swag/tree/master/projects/juice-shop'
    NFT_LINK = 'https://opensea.io/collection/juice-shop'
    TERMS_OF_USE_LINK = 'ftp/legal.md'

    def __init__(self, page):
        super().__init__(page)
        self.locators = AboutUsPageLocators()
        self.gallery = GalleryComponent(page)

    def get_outer_source_link(self, link):
        link = Link(self.page, link, 'Outer resource Link')
        link.scroll_into_view_if_needed()
        return link.get_attribute('href')

    def check_comment_appears_among_others_on_page(self, comment):
        self.gallery.navigate_to_last_post()
        self.gallery.comment_under_pic.check_contain_text(comment)