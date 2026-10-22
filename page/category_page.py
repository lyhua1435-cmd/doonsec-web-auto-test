"""页面对象层 - 首页内容分类

历史缺陷背景：早期版本点击"最新"分类后，页面偶尔出现内容区被清空的渲染异常。
因此本模块除了正向断言，还专门保留了 test_23（点击后链接数量不塌陷）这条
"异常兼容"用例作为回归保护。
"""
from selenium.webdriver.common.by import By

from base.base_page import BasePage


class CategoryPage(BasePage):
    """首页分类导航条。"""

    new_category = (By.XPATH, "//li[@id='new']")
    category_items = (By.CSS_SELECTOR, "li")

    def get_new_category(self):
        return self.wait_visible(self.new_category)

    def click_new_category(self):
        element = self.get_new_category()
        self.scroll_to_element(element)
        element.click()
        return element

    def get_all_categories(self):
        return self.driver.find_elements(*self.category_items)

    def get_category_count(self) -> int:
        return len(self.get_all_categories())
