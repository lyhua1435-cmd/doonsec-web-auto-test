"""公众号内容分类展示模块（DJWX-AUTO-019 ~ 024）

其中 test_23 是从历史缺陷反推出来的回归用例：分类点击后页面内容区曾出现
渲染异常（链接塌陷），因此不能只断言"点击成功"，还要断言"点击后页面结构未损坏"。
"""
from page.category_page import CategoryPage
from page.home_page import HomePage


class TestCategoryDisplay:
    """公众号内容分类展示模块。"""

    def test_19_new_category_display(self, driver):
        """DJWX-AUTO-019：验证"最新"分类入口正常展示"""
        HomePage(driver).open_home()
        assert CategoryPage(driver).get_new_category().is_displayed()

    def test_20_new_category_text(self, driver):
        """DJWX-AUTO-020：验证"最新"分类文本正确"""
        HomePage(driver).open_home()
        assert "最新" in CategoryPage(driver).get_new_category().text

    def test_21_click_new_category(self, driver):
        """DJWX-AUTO-021：点击"最新"分类，验证分类点击功能可执行"""
        HomePage(driver).open_home()
        element = CategoryPage(driver).click_new_category()
        assert "最新" in element.text

    def test_22_category_list_not_empty(self, driver):
        """DJWX-AUTO-022：验证首页分类列表不为空"""
        HomePage(driver).open_home()
        assert CategoryPage(driver).get_category_count() > 0

    def test_23_home_links_after_category_click(self, driver):
        """DJWX-AUTO-023：点击分类后链接不塌陷（历史缺陷回归用例）"""
        home = HomePage(driver).open_home()
        CategoryPage(driver).click_new_category()
        assert len(home.get_all_links()) > 5

    def test_24_home_source_contains_new_text(self, driver):
        """DJWX-AUTO-024：验证首页内容包含"最新"分类信息"""
        home = HomePage(driver).open_home()
        assert "最新" in home.get_page_source()
