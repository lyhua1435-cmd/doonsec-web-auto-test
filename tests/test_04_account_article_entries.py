"""公众号与文章入口模块（DJWX-AUTO-025 ~ 030）

覆盖点：公众号入口 href 有效性、点击后站点归属、页面内容关键字、
文章/功能链接数量与格式。
"""
from page.home_page import HomePage
from page.navigation_page import NavigationPage


class TestAccountArticleEntries:
    """公众号与文章入口模块。"""

    def test_25_account_nav_href_not_empty(self, driver):
        """DJWX-AUTO-025：验证公众号入口链接不为空"""
        HomePage(driver).open_home()
        nav = NavigationPage(driver)
        assert nav.get_account_nav().get_attribute("href") != ""

    def test_26_click_account_nav(self, driver):
        """DJWX-AUTO-026：点击公众号入口，验证页面仍在洞见微信站点内"""
        HomePage(driver).open_home()
        NavigationPage(driver).click_account_nav()
        assert "wechat.doonsec.com" in driver.current_url

    def test_27_page_contains_account_text(self, driver):
        """DJWX-AUTO-027：验证页面包含公众号相关内容"""
        home = HomePage(driver).open_home()
        assert "公众号" in home.get_page_source()

    def test_28_home_links_count(self, driver):
        """DJWX-AUTO-028：验证首页存在多个文章或功能链接"""
        home = HomePage(driver).open_home()
        assert len(home.get_all_links()) > 5

    def test_29_first_valid_link_exists(self, driver):
        """DJWX-AUTO-029：验证首页至少存在一个有效文章/功能链接"""
        home = HomePage(driver).open_home()
        assert home.get_first_link_with_href() is not None

    def test_30_first_valid_link_href(self, driver):
        """DJWX-AUTO-030：验证首页有效链接地址属于 http 链接"""
        home = HomePage(driver).open_home()
        link = home.get_first_link_with_href()
        assert link.get_attribute("href").startswith("http")
