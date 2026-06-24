import pytest
import os
import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

BASE_URL = "http://127.0.0.1:8000"

# Tài khoản test 
TEST_USERNAME = "mi"
TEST_PASSWORD = "Test@123456"

@pytest.fixture(scope="function")
def driver():
    """Khởi tạo Chrome, chạy xong mỗi test thì đóng lại"""
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    # Bỏ comment dòng dưới nếu muốn chạy ẩn (không hiện cửa sổ Chrome)
    #options.add_argument("--headless")
    service = Service(
        r"C:\Users\admin\.wdm\drivers\chromedriver\win64\148.0.7778.178\chromedriver-win64\chromedriver.exe"
    )
    d = webdriver.Chrome(service=service, options=options)
    d.implicitly_wait(5)
    d.execute_script("window.scrollTo(0, 0);")
    yield d
    d.quit()

@pytest.fixture(scope="function")
def driver_loggedin(driver):
    """Driver đã đăng nhập sẵn - dùng cho test cần đăng nhập"""
    driver.get(f"{BASE_URL}/dangnhap/")
    driver.find_element("name", "username").send_keys(TEST_USERNAME)
    driver.find_element("name", "password").send_keys(TEST_PASSWORD)
    driver.find_element("css selector", "button.btn-auth").click()
    return driver

def pytest_configure():
    sys.stdout.reconfigure(encoding="utf-8")


os.environ["PYTHONIOENCODING"] = "utf-8"
os.environ["PYTHONUTF8"] = "1"

