"""pytest 全局配置：驱动管理、选项、失败截图、HTML 报告生成。

相比最初版本的三点改造
--------------------
1. 把阻塞式 ``input("按 Enter")`` 换成 ``--pause-login`` 开关，CI 里不会再卡死；
2. 新增 ``--headless``，无头模式下也能跑（用于流水线回归）；
3. 用例失败自动截图，并把截图路径写进报告，报告从"通过/失败"升级为"可追溯"。
"""
import time
from datetime import datetime
from html import escape
from pathlib import Path

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from base.base_page import screenshot_on_failure

ROOT_DIR = Path(__file__).resolve().parent
REPORT_DIR = ROOT_DIR / "reports"
REPORT_FILE = REPORT_DIR / "report.html"
HOME_URL = "https://wechat.doonsec.com/"


# ---------------------------------------------------------------- 命令行选项
def pytest_addoption(parser):
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="无头模式运行（CI 用），不弹出浏览器窗口",
    )
    parser.addoption(
        "--pause-login",
        action="store_true",
        default=False,
        help="打开浏览器后暂停，等待人工扫码/解锁，回车后继续",
    )
    parser.addoption(
        "--slow",
        type=float,
        default=0.0,
        help="每条用例结束后额外等待秒数，答辩演示时用 --slow 2",
    )


# ---------------------------------------------------------------- 浏览器 fixture
@pytest.fixture(scope="session")
def driver(request):
    """整个测试会话复用同一个浏览器实例。

    被测站点首次访问需要扫码解锁，因此默认提供 ``--pause-login`` 人工确认环节；
    该环节是显式开关而不是硬编码 input()，保证流水线环境可以无人值守运行。
    """
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-gpu")
    options.add_argument("--lang=zh-CN")
    if request.config.getoption("--headless"):
        options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080")

    drv = webdriver.Chrome(options=options)
    drv.implicitly_wait(5)
    drv.get(HOME_URL)

    if request.config.getoption("--pause-login"):
        print("\n[人工介入] 浏览器已打开，请在 Chrome 中完成扫码/解锁。")
        input("完成解锁后按 Enter 开始执行自动化测试 ...")

    yield drv

    time.sleep(1)
    drv.quit()


@pytest.fixture(autouse=True)
def observe_between_cases(request):
    """演示节奏控制：仅当显式传 --slow 时才等待，避免拖慢回归。"""
    yield
    slow = request.config.getoption("--slow")
    if slow:
        time.sleep(slow)


# ---------------------------------------------------------------- 结果采集
def pytest_configure(config):
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    config.test_results = []


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when != "call":
        return

    screenshot = ""
    if report.failed:
        driver = item.funcargs.get("driver")
        if driver is not None:
            screenshot = screenshot_on_failure(driver, item.name) or ""

    item.config.test_results.append(
        {
            "name": item.name,
            "doc": (item.function.__doc__ or "").strip(),
            "status": report.outcome,
            "duration": f"{report.duration:.2f}s",
            "screenshot": screenshot,
        }
    )


# ---------------------------------------------------------------- 报告生成
def _build_rows(results) -> str:
    rows = []
    for r in results:
        shot = (
            f"<a href='screenshots/{Path(r['screenshot']).name}'>查看</a>"
            if r["screenshot"]
            else "-"
        )
        rows.append(
            "<tr>"
            f"<td>{escape(r['name'])}</td>"
            f"<td>{escape(r['doc'])}</td>"
            f"<td class='{escape(r['status'])}'>{escape(r['status'])}</td>"
            f"<td>{escape(r['duration'])}</td>"
            f"<td>{shot}</td>"
            "</tr>"
        )
    return "".join(rows)


def pytest_sessionfinish(session, exitstatus):
    results = getattr(session.config, "test_results", [])
    if not results:
        return

    passed = sum(1 for r in results if r["status"] == "passed")
    failed = sum(1 for r in results if r["status"] == "failed")
    skipped = sum(1 for r in results if r["status"] == "skipped")
    total = len(results)
    pass_rate = passed / total * 100 if total else 0

    html = f"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<title>洞见微信 Web 自动化测试报告</title>
<style>
  body {{ font-family: 'Microsoft YaHei', Arial, sans-serif; margin: 32px; color: #1f2328; }}
  h1 {{ font-size: 22px; margin-bottom: 4px; }}
  .meta {{ color: #59636e; font-size: 13px; margin-bottom: 18px; }}
  .cards {{ display: flex; gap: 12px; margin: 18px 0 24px; }}
  .card {{ flex: 1; border: 1px solid #d1d9e0; border-radius: 8px; padding: 14px 16px; }}
  .card b {{ display: block; font-size: 24px; margin-top: 4px; }}
  .card span {{ color: #59636e; font-size: 12px; }}
  .ok b {{ color: #1a7f37; }} .ng b {{ color: #cf222e; }} .rate b {{ color: #0969da; }}
  table {{ border-collapse: collapse; width: 100%; font-size: 13px; table-layout: fixed; }}
  th, td {{ border: 1px solid #d1d9e0; padding: 8px 10px; text-align: left; word-wrap: break-word; }}
  th {{ background: #f6f8fa; font-weight: 600; }}
  tbody tr:nth-child(even) {{ background: #fbfcfd; }}
  .passed {{ color: #1a7f37; font-weight: 600; }}
  .failed {{ color: #cf222e; font-weight: 600; }}
  .skipped {{ color: #9a6700; font-weight: 600; }}
</style>
</head>
<body>
  <h1>洞见微信 Web 自动化测试报告</h1>
  <div class="meta">
    生成时间：{datetime.now():%Y-%m-%d %H:%M:%S} &nbsp;|&nbsp;
    被测站点：{escape(HOME_URL)} &nbsp;|&nbsp;
    框架：pytest + Selenium + Page Object
  </div>

  <div class="cards">
    <div class="card"><span>用例总数</span><b>{total}</b></div>
    <div class="card ok"><span>通过</span><b>{passed}</b></div>
    <div class="card ng"><span>失败</span><b>{failed}</b></div>
    <div class="card"><span>跳过</span><b>{skipped}</b></div>
    <div class="card rate"><span>通过率</span><b>{pass_rate:.1f}%</b></div>
  </div>

  <table>
    <thead>
      <tr><th style="width:26%">用例函数</th><th style="width:40%">测试说明</th>
          <th style="width:10%">状态</th><th style="width:10%">耗时</th><th style="width:14%">失败截图</th></tr>
    </thead>
    <tbody>{_build_rows(results)}</tbody>
  </table>
</body>
</html>"""
    REPORT_FILE.write_text(html, encoding="utf-8")
    print(f"\n[报告] 已生成: {REPORT_FILE}  (通过 {passed}/{total})")
