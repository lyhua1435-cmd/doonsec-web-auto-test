"""页面对象层 - 全文搜索（/es/）

被测站点支撑 70 万+ 安全文章的全文检索，是本次自动化覆盖的核心业务模块。
"""
from selenium.webdriver.common.by import By

from base.base_page import BasePage


class SearchPage(BasePage):
    """全文搜索页。"""

    es_url = "https://wechat.doonsec.com/es/"

    keyword_input = (By.NAME, "keyword")
    search_button = (By.CSS_SELECTOR, ".search_form button")

    def open_search_page(self):
        self.open_url(self.es_url)
        return self

    def get_keyword_input(self):
        return self.wait_visible(self.keyword_input)

    def input_keyword(self, keyword: str):
        return self.input_text(self.keyword_input, keyword)

    def get_search_button(self):
        return self.wait_visible(self.search_button)

    def submit(self):
        return self.click(self.search_button)

    def search_keyword(self, keyword: str):
        """输入关键词并提交，返回输入框元素（便于断言 value）。"""
        element = self.input_keyword(keyword)
        self.submit()
        return element

    def is_on_search_result_page(self) -> bool:
        return "/es" in self.current_url or "keyword" in self.current_url
