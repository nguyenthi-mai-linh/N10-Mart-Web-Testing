"""
Test script: Chức năng Quản lý giỏ hàng
Web: N10-Mart | http://127.0.0.1:8000
Test cases: GH-01 đến GH-09
"""
import time
import json
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from conftest import BASE_URL

URL_GIO_HANG    = f"{BASE_URL}/giohang/"
URL_CHITIET_SP1 = f"{BASE_URL}/chitietsanpham/1/"
URL_CHITIET_SP2 = f"{BASE_URL}/chitietsanpham/2/"
URL_HOME        = f"{BASE_URL}/home/"


# ── Helper: xóa sạch giỏ hàng cookie ───────────────────────────────────────
def xoa_sach_gio_hang(driver):
    driver.get(URL_HOME)
    time.sleep(1)
    driver.execute_script(
        "document.cookie = 'cart={}; path=/; domain=;';"
    )
    driver.refresh()
    time.sleep(1)


# ── Helper: thêm sản phẩm vào giỏ qua cookie ────────────────────────────────
def them_san_pham(driver, url=None):
    driver.get(url or URL_CHITIET_SP1)
    time.sleep(2)
    btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "btn-them-gio"))
    )
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", btn)
    time.sleep(0.3)
    driver.execute_script("arguments[0].click();", btn)
    time.sleep(2)


# ── Helper: lấy số lượng hiện tại trong giỏ ────────────────────────────────
def lay_so_luong(driver):
    qty = driver.find_element(By.CSS_SELECTOR, ".qty-input")
    return int(qty.get_attribute("value"))


# ── GH-01: Xem giỏ hàng có sản phẩm ───────────────────────────────────────
def test_GH01_xem_gio_hang_co_san_pham(driver):
    xoa_sach_gio_hang(driver)
    them_san_pham(driver)
    driver.get(URL_GIO_HANG)
    time.sleep(1)

    page_source = driver.page_source
    assert "Giỏ hàng" in page_source
    assert "Số lượng" in page_source
    assert "TỔNG" in page_source
    assert "đ" in page_source


# ── GH-02: Tăng số lượng bằng nút (+) ──────────────────────────────────────
def test_GH02_tang_so_luong(driver):
    xoa_sach_gio_hang(driver)
    them_san_pham(driver)
    driver.get(URL_GIO_HANG)
    time.sleep(1)

    so_luong_truoc = lay_so_luong(driver)

    btn_plus = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".fa-square-plus"))
    )
    driver.execute_script("arguments[0].click();", btn_plus)
    time.sleep(2)

    so_luong_sau = lay_so_luong(driver)
    assert so_luong_sau == so_luong_truoc + 1, \
        f"Số lượng không tăng đúng: trước={so_luong_truoc}, sau={so_luong_sau}"


# ── GH-03: Giảm số lượng bằng nút (-) ──────────────────────────────────────
def test_GH03_giam_so_luong(driver):
    xoa_sach_gio_hang(driver)
    them_san_pham(driver)
    them_san_pham(driver)
    driver.get(URL_GIO_HANG)
    time.sleep(1)

    so_luong_truoc = lay_so_luong(driver)

    btn_minus = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".fa-square-minus"))
    )
    driver.execute_script("arguments[0].click();", btn_minus)
    time.sleep(2)

    so_luong_sau = lay_so_luong(driver)
    assert so_luong_sau == so_luong_truoc - 1, \
        f"Số lượng không giảm đúng: trước={so_luong_truoc}, sau={so_luong_sau}"


# ── GH-04: Thay đổi số lượng bằng bàn phím ─────────────────────────────────
def test_GH04_nhap_so_luong_bang_ban_phim(driver):
    xoa_sach_gio_hang(driver)
    them_san_pham(driver)
    driver.get(URL_GIO_HANG)
    time.sleep(1)

    qty_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".qty-input"))
    )
    driver.execute_script("arguments[0].value = '';", qty_input)
    qty_input.send_keys("5")
    qty_input.send_keys(Keys.ENTER)
    time.sleep(2)

    qty_sau = driver.find_element(By.CSS_SELECTOR, ".qty-input")
    assert qty_sau.get_attribute("value") == "5", \
        f"Số lượng không cập nhật đúng: {qty_sau.get_attribute('value')}"


# ── GH-05: Xóa một sản phẩm bằng checkbox ──────────────────────────────────
def test_GH05_xoa_mot_san_pham(driver):
    xoa_sach_gio_hang(driver)
    them_san_pham(driver)
    driver.get(URL_GIO_HANG)
    time.sleep(1)

    chk = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".row-chk"))
    )
    driver.execute_script("arguments[0].click();", chk)
    time.sleep(0.5)

    btn_xoa = driver.find_element(By.ID, "btn-delete-selected")
    driver.execute_script("arguments[0].click();", btn_xoa)

    WebDriverWait(driver, 5).until(EC.alert_is_present())
    driver.switch_to.alert.accept()
    time.sleep(3)

    assert "Giỏ hàng" in driver.page_source


# ── GH-06: Xóa nhiều sản phẩm bằng checkbox ───────────────────────────────
def test_GH06_xoa_nhieu_san_pham(driver):
    xoa_sach_gio_hang(driver)
    them_san_pham(driver, URL_CHITIET_SP1)
    them_san_pham(driver, URL_CHITIET_SP2)
    driver.get(URL_GIO_HANG)
    time.sleep(1)

    checkboxes = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".row-chk"))
    )
    for c in checkboxes:
        driver.execute_script("arguments[0].click();", c)
    time.sleep(0.5)

    btn = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "btn-delete-selected"))
    )
    driver.execute_script("arguments[0].click();", btn)

    WebDriverWait(driver, 5).until(EC.alert_is_present())
    driver.switch_to.alert.accept()
    time.sleep(4)

    assert "Giỏ hàng" in driver.page_source


# ── GH-07: Giảm số lượng xuống 0 → tự xóa sản phẩm ───────────────────────
def test_GH07_giam_so_luong_xuong_0(driver):
    xoa_sach_gio_hang(driver)
    them_san_pham(driver)
    driver.get(URL_GIO_HANG)
    time.sleep(1)

    btn_minus = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".fa-square-minus"))
    )
    driver.execute_script("arguments[0].click();", btn_minus)
    time.sleep(2)

    tong_el = driver.find_element(By.CSS_SELECTOR, ".cart-items strong")
    assert tong_el.text.strip() == "0", \
        f"Sản phẩm không bị xóa khi số lượng về 0: {tong_el.text}"


# ── GH-08: Chuyển sang trang đặt hàng ──────────────────────────────────────
def test_GH08_chuyen_sang_dat_hang(driver):
    xoa_sach_gio_hang(driver)
    them_san_pham(driver)
    driver.get(URL_GIO_HANG)
    time.sleep(1)

    btn_dathang = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "btn-dathang"))
    )
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", btn_dathang)
    time.sleep(1)
    driver.execute_script("arguments[0].click();", btn_dathang)
    time.sleep(2)

    assert "thongtinmuahang" in driver.current_url, \
        "Không chuyển sang trang đặt hàng"


# ── GH-09: Truy cập giỏ hàng khi không có sản phẩm ────────────────────────
def test_GH09_gio_hang_trong(driver):
    xoa_sach_gio_hang(driver)
    driver.get(URL_GIO_HANG)
    time.sleep(1)

    assert "Giỏ hàng" in driver.page_source
    btn_dathang = driver.find_element(By.ID, "btn-dathang")
    assert btn_dathang.get_attribute("disabled") is not None, \
        "Nút Đặt hàng không bị vô hiệu khi giỏ hàng trống"