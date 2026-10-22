"""页面对象层 - 首页

定位策略说明见 docs/测试用例设计说明.md 第 3 节。
"""
from selenium.webdriver.common.by import By

from base.base_page import BasePage


class HomePage(BasePage):
    """洞见微信首页（https://wechat.doonsec.com/）。"""

    url = "https://wechat.doonsec.com/"

    # 元素定位器统一收敛为类属性，改版时只改这一处
    logo_img = (By.CSS_SELECTOR, ".logo img")
    search_icon = (By.CLASS_NAME, "search_pic")
    all_links = (By.TAG_NAME, "a")
    page_body = (By.TAG_NAME, "body")

    def open_home(self):
        self.open_url(self.url)
        return self

    def get_logo(self):
        return self.wait_visible(self.logo_img)

    def get_search_icon(self):
        return self.wait_visible(self.search_icon)

    def get_all_links(self):
        return self.driver.find_elements(*self.all_links)

    def get_page_source(self) -> str:
        return self.driver.page_source

    def get_first_link_with_href(self):
        """返回第一个 href 以 http 开头的 a 元素，用于校验文章入口可访问性。"""
        for link in self.get_all_links():
            href = link.get_attribute("href") or ""
            if href.startswith("http"):
                return link
        return None

    def count_valid_links(self) -> int:
        return sum(
            1
            for link in self.get_all_links()
            if (link.get_attribute("href") or "").startswith("http")
        )
