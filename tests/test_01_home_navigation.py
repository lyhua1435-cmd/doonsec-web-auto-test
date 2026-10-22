"""首页与导航模块（DJWX-AUTO-001 ~ 008）

覆盖点：站点可达性、页面标题、Logo/搜索入口渲染、公众号与高级搜索导航的
可见性、href 属性正确性、点击后页面跳转。
"""
import pytest

from page.home_page import HomePage
from page.navigation_page import NavigationPage


class TestHomeNavigation:
    """首页与导航模块。"""

    def test_01_open_home_url(self, driver):
        """DJWX-AUTO-001：打开首页，验证进入洞见微信站点"""
        page = HomePage(driver)
        page.open_home()
        assert "wechat.doonsec.com" in driver.current_url

    def test_02_home_title_contains_keyword(self, driver):
        """DJWX-AUTO-002：验证首页标题体现安全圈微信搜索功能"""
        page = HomePage(driver).open_home()
        assert "安全圈微信搜索" in page.title

    def test_03_home_logo_display(self, driver):
        """DJWX-AUTO-003：验证首页 Logo 正常展示"""
        page = HomePage(driver).open_home()
        assert page.get_logo().is_displayed()

    def test_04_home_search_icon_display(self, driver):
        """DJWX-AUTO-004：验证首页搜索入口图标正常展示"""
        page = HomePage(driver).open_home()
        assert page.get_search_icon().is_displayed()

    def test_05_account_nav_display(self, driver):
        """DJWX-AUTO-005：验证公众号导航入口可见"""
        HomePage(driver).open_home()
        nav = NavigationPage(driver)
        assert nav.get_account_nav().text == "公众号"

    def test_06_es_nav_display(self, driver):
        """DJWX-AUTO-006：验证高级搜索导航入口可见"""
        HomePage(driver).open_home()
        nav = NavigationPage(driver)
        assert "高级搜索" in nav.get_es_nav().text

    def test_07_es_nav_href(self, driver):
        """DJWX-AUTO-007：验证高级搜索入口链接指向全文搜索页面"""
        HomePage(driver).open_home()
        nav = NavigationPage(driver)
        assert "/es" in (nav.get_es_nav().get_attribute("href") or "")

    def test_08_click_es_nav_switch_page(self, driver):
        """DJWX-AUTO-008：点击高级搜索导航，验证页面切换成功"""
        HomePage(driver).open_home()
        nav = NavigationPage(driver)
        nav.click_es_nav()
        assert "/es" in driver.current_url
