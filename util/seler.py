from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from undetected_chromedriver import Chrome


def init_driver(url, headless=False, keep_open=False, args=None):
    # 配置浏览器选项

    options = Options()
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

    if headless:
        options.add_argument("--headless")  # 启用无头模式
        options.add_argument("--disable-gpu")  # 禁用 GPU 加速
        options.add_argument("--no-sandbox")  # 禁用沙盒模式

    if args:
        for arg in args:
            options.add_argument(arg)

    if not keep_open:
        # 保持浏览器窗口打开
        options.add_argument("--disable-dev-shm-usage")

    # 启动浏览器
    driver = webdriver.Chrome(options=options)
    # driver = Chrome(options=options)

    # 隐藏 webdriver 属性
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    # 伪造插件列表
    driver.execute_script('''
        Object.defineProperty(navigator, 'plugins', {
            get: () => [{
                description: 'PDF Viewer',
                filename: 'internal-pdf-viewer'
            }]
        })
    ''')

    # 访问目标页面
    driver.get(url)
    return driver
