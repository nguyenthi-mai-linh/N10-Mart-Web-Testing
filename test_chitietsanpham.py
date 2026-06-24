"""
Test script: Chức năng Xem chi tiết sản phẩm
Web: N10-Mart | http://127.0.0.1:8000
Test cases: CTSP-01 
"""
import time
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from conftest import BASE_URL

URL_HOME     = f"{BASE_URL}/home/"
URL_DANHSACH = f"{BASE_URL}/thucphamkho/"  # Dùng trang danh mục có sản phẩm


def test_CTSP01_xem_chitiet_san_pham(driver):
    """Kiểm tra chuyển trang và hiển thị đầy đủ thông tin"""
    driver.get(URL_DANHSACH)
    time.sleep(1)

    san_pham = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".card-title"))
    )
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", san_pham)
    time.sleep(0.3)
    driver.execute_script("arguments[0].click();", san_pham)
    time.sleep(1.5)

    page_source = driver.page_source

    # Kiểm tra chuyển đúng trang
    assert "chitietsanpham" in driver.current_url

    # Kiểm tra tên sản phẩm
    assert driver.find_element(
        By.CSS_SELECTOR, ".price-foodname p").text.strip() != ""

    # Kiểm tra giá bán
    assert "đ" in page_source

    # Kiểm tra hình ảnh
    img = driver.find_element(By.CSS_SELECTOR, ".img-banner")
    assert img.get_attribute("src") != ""

    # Kiểm tra mô tả
    assert "Mô tả sản phẩm" in page_source