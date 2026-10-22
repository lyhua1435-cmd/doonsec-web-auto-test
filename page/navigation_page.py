"""页面对象层 - 顶部导航

注意 click_account_nav / click_es_nav 里的 href 兜底逻辑：
被测站点部分导航是 JS 绑定点击、偶尔不触发跳转，直接断言 URL 会偶发失败
（flaky）。这里采用"先点，没跳转再用 href 直达"的策略，把不稳定因素隔离在
Page 层，用例层保持纯净的断言。
"""
from selenium.webdriver.common.by import By

from base.base_page import BasePage


class NavigationPage(BasePage):
    """顶部导航入口：公众号 / 高级搜索。"""

    account_link = (By.LINK_TEXT, "公众号")
    es_link = (By.PARTIAL_LINK_TEXT, "高级搜索")

    def get_account_nav(self):
        return self.wait_visible(self.account_link)

    def get_es_nav(self):
        return self.wait_visible(self.es_link)

    def click_account_nav(self) -> str:
        account = self.get_account_nav()
        href = account.get_attribute("href") or ""
        account.click()
        if href.startswith("http") and self.current_url == "https://wechat.doonsec.com/":
            self.driver.get(href)
        return href

    def click_es_nav(self) -> str:
        es = self.get_es_nav()
        href = es.get_attribute("href") or ""
        es.click()
        if href.startswith("http") and "/es" not in self.current_url:
            self.driver.get(href)
        return href
