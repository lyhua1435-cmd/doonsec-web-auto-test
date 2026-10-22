"""基础层：把最常用的 Selenium 操作收敛到一处。

设计目标
--------
1. 业务层（page/）不出现一行 ``find_element``、``time.sleep``、``WebDriverWait``；
2. 所有等待统一走显式等待，禁止隐式等待兜底式的"碰运气"写法；
3. 出错时自动留证据（截图 + 当前 URL），方便定位是元素变了还是页面没加载。
"""
import logging
import os
from datetime import datetime
from pathlib import Path

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

logger = logging.getLogger(__name__)

SCREENSHOT_DIR = Path(__file__).resolve().parent.parent / "reports" / "screenshots"


class BasePage:
    """所有页面对象的父类。"""

    def __init__(self, driver, timeout: int = 10):
        self.driver = driver
        self.timeout = timeout

    # ---------- 页面级操作 ----------
    def open_url(self, url: str):
        logger.info("打开页面: %s", url)
        self.driver.get(url)

    @property
    def current_url(self) -> str:
        return self.driver.current_url

    @property
    def title(self) -> str:
        return self.driver.title

    # ---------- 等待 ----------
    def wait_visible(self, locator, timeout: int | None = None):
        """显式等待：元素出现在 DOM 且可见。"""
        timeout = timeout or self.timeout
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )

    def wait_present(self, locator, timeout: int | None = None):
        """显式等待：元素存在于 DOM（不要求可见，适合隐藏域）。"""
        timeout = timeout or self.timeout
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(locator)
        )

    def wait_clickable(self, locator, timeout: int | None = None):
        """显式等待：元素可见且可点击（排除被遮挡、disabled）。"""
        timeout = timeout or self.timeout
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )

    def wait_url_contains(self, fragment: str, timeout: int | None = None) -> bool:
        """显式等待：URL 中出现指定片段，返回 True/False 而不抛异常。"""
        timeout = timeout or self.timeout
        try:
            WebDriverWait(self.driver, timeout).until(EC.url_contains(fragment))
            return True
        except Exception:
            return False

    # ---------- 元素操作 ----------
    def input_text(self, locator, text: str):
        element = self.wait_visible(locator)
        element.clear()
        element.send_keys(text)
        logger.info("输入文本: locator=%s text=%s", locator, text)
        return element

    def click(self, locator):
        element = self.wait_clickable(locator)
        element.click()
        logger.info("点击元素: locator=%s", locator)
        return element

    def scroll_to_element(self, element):
        """把元素滚动到视口中间后再操作，规避固定导航栏遮挡。"""
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", element
        )

    def get_text(self, locator) -> str:
        return self.wait_visible(locator).text.strip()

    # ---------- 断言辅助 ----------
    def is_visible(self, locator) -> bool:
        """不抛异常的可见性判断，适合"是否存在"这类软断言。"""
        try:
            return self.wait_visible(locator).is_displayed()
        except Exception:
            return False

    def count_elements(self, locator) -> int:
        return len(self.driver.find_elements(*locator))

    # ---------- 证据留存 ----------
    def save_screenshot(self, name: str) -> str:
        """截图落盘，返回文件路径。失败用例挂到报告里用。"""
        SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
        safe = "".join(c if c.isalnum() or c in "-_" else "_" for c in name)
        path = SCREENSHOT_DIR / f"{safe}_{datetime.now():%Y%m%d_%H%M%S}.png"
        self.driver.save_screenshot(str(path))
        logger.info("已保存截图: %s", path)
        return str(path)


def screenshot_on_failure(driver, case_name: str) -> str | None:
    """供 conftest 的失败钩子调用。截图本身失败不应影响用例结果。"""
    try:
        page = BasePage(driver)
        return page.save_screenshot(case_name)
    except Exception as exc:  # pragma: no cover - 兜底
        logger.warning("截图失败，忽略: %s", exc)
        return None
