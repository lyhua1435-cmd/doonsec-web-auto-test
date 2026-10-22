"""数据驱动补充用例（DJWX-AUTO-031 ~ 035）

原始 30 条用例是"一功能一脚本"的线性写法。这里把"关键词输入→提交→结果页可达"
抽成参数化用例：新增一个关键词只需加一行数据，不必复制函数。

这是把脚本升级成框架的关键一步 —— 用例数据与用例逻辑分离。
"""
import pytest

from page.search_page import SearchPage

# 安全垂直领域的高频检索词，覆盖英文缩写、中文、混合三类输入
SEARCH_KEYWORDS = [
    pytest.param("CVE", id="english-abbr"),
    pytest.param("漏洞复现", id="chinese-phrase"),
    pytest.param("POC", id="shorthand"),
    pytest.param("SQL注入", id="mixed-input"),
    pytest.param("弱口令", id="security-term"),
]


class TestSearchKeywordDataDriven:
    """全文搜索关键词数据驱动用例。"""

    @pytest.mark.parametrize("keyword", SEARCH_KEYWORDS)
    def test_31_search_keyword_matrix(self, driver, keyword):
        """DJWX-AUTO-031~035：多关键词检索矩阵，验证输入回填与结果页可达"""
        page = SearchPage(driver).open_search_page()
        element = page.search_keyword(keyword)

        assert element.get_attribute("value") == keyword, "输入框未正确回填关键词"
        assert page.is_on_search_result_page(), f"关键词「{keyword}」提交后未进入结果页"
