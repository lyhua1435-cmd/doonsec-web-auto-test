"""全文搜索模块（DJWX-AUTO-009 ~ 018）

覆盖点：搜索页可达性、输入框属性、关键词输入与回填、按钮状态、
提交搜索后的页面状态、关键词二次编辑。
"""
import pytest

from page.search_page import SearchPage


class TestFullTextSearch:
    """全文搜索模块。"""

    def test_09_open_full_text_search_page(self, driver):
        """DJWX-AUTO-009：打开全文搜索页面，验证 URL 包含 /es"""
        SearchPage(driver).open_search_page()
        assert "/es" in driver.current_url

    def test_10_keyword_input_display(self, driver):
        """DJWX-AUTO-010：验证全文搜索输入框正常展示"""
        page = SearchPage(driver).open_search_page()
        assert page.get_keyword_input().is_displayed()

    def test_11_keyword_input_name(self, driver):
        """DJWX-AUTO-011：验证全文搜索输入框 name 属性为 keyword"""
        page = SearchPage(driver).open_search_page()
        assert page.get_keyword_input().get_attribute("name") == "keyword"

    def test_12_input_cve_keyword(self, driver):
        """DJWX-AUTO-012：输入 CVE 关键字，验证输入内容正确"""
        page = SearchPage(driver).open_search_page()
        assert page.input_keyword("CVE").get_attribute("value") == "CVE"

    def test_13_input_vulnerability_keyword(self, driver):
        """DJWX-AUTO-013：输入漏洞复现关键字，验证输入内容正确"""
        page = SearchPage(driver).open_search_page()
        assert page.input_keyword("漏洞复现").get_attribute("value") == "漏洞复现"

    def test_14_search_button_display(self, driver):
        """DJWX-AUTO-014：验证全文搜索按钮正常展示"""
        page = SearchPage(driver).open_search_page()
        assert page.get_search_button().is_displayed()

    def test_15_search_button_enabled(self, driver):
        """DJWX-AUTO-015：验证全文搜索按钮可以点击"""
        page = SearchPage(driver).open_search_page()
        assert page.get_search_button().is_enabled()

    def test_16_submit_cve_search(self, driver):
        """DJWX-AUTO-016：提交 CVE 搜索，验证搜索动作执行成功"""
        page = SearchPage(driver).open_search_page()
        page.search_keyword("CVE")
        assert page.is_on_search_result_page()

    def test_17_submit_vulnerability_search(self, driver):
        """DJWX-AUTO-017：提交漏洞复现搜索，验证全文搜索功能可执行"""
        page = SearchPage(driver).open_search_page()
        page.search_keyword("漏洞复现")
        assert page.is_on_search_result_page()

    def test_18_change_search_keyword(self, driver):
        """DJWX-AUTO-018：修改搜索关键字，验证输入框可以重新输入"""
        page = SearchPage(driver).open_search_page()
        page.input_keyword("CVE")
        assert page.input_keyword("POC").get_attribute("value") == "POC"
