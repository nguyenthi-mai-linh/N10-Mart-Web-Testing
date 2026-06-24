"""
Test script: Chức năng Đặt hàng
Web: N10-Mart | http://127.0.0.1:8000
Test cases: DH-01 đến DH-06
"""
import csv
import time
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from conftest import BASE_URL, TEST_USERNAME, TEST_PASSWORD

URL_DANGNHAP  = f"{BASE_URL}/dangnhap/"
URL_CHITIET   = f"{BASE_URL}/chitietsanpham/1/"
URL_GIO_HANG  = f"{BASE_URL}/giohang/"
URL_THONGTIN  = f"{BASE_URL}/thongtinmuahang/"


# ── Helper: đọc CSV ─────────────────────────────────────────────────────────
def doc_csv(ten_file, ket_qua):
    rows = []
    with open(ten_file, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if (row.get("ket_qua_mong_doi") or "").strip() == ket_qua:
                rows.append(row)
    return rows


# ── Helper: đăng nhập ───────────────────────────────────────────────────────
def dang_nhap(driver):
    driver.get(URL_DANGNHAP)
    time.sleep(1)
    driver.find_element(By.NAME, "username").send_keys(TEST_USERNAME)
    driver.find_element(By.NAME, "password").send_keys(TEST_PASSWORD)
    btn = driver.find_element(By.CSS_SELECTOR, "button.btn-auth")
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", btn)
    time.sleep(0.3)
    driver.execute_script("arguments[0].click();", btn)
    time.sleep(2)


# ── Helper: xóa sạch giỏ hàng ───────────────────────────────────────────────
def xoa_sach_gio(driver):
    driver.get(URL_GIO_HANG)
    time.sleep(1)
    driver.execute_script("""
        var btns = document.querySelectorAll('.fa-square-minus');
        btns.forEach(function(btn) {
            var pid = btn.dataset.product;
            var csrf = document.cookie.split('csrftoken=')[1]?.split(';')[0] || '';
            fetch('/update_item/', {
                method: 'POST',
                headers: {'Content-Type': 'application/json', 'X-CSRFToken': csrf},
                body: JSON.stringify({productId: pid, action: 'set', quantity: 0})
            });
        });
    """)
    time.sleep(2)
    driver.refresh()
    time.sleep(1)


# ── Helper: thêm sản phẩm và vào trang đặt hàng ────────────────────────────
def vao_trang_dat_hang(driver):
    driver.get(URL_CHITIET)
    time.sleep(2)
    btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "btn-them-gio"))
    )
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", btn)
    time.sleep(0.3)
    driver.execute_script("arguments[0].click();", btn)
    time.sleep(3)

    driver.execute_script("window.location.href = '/thongtinmuahang/';")
    WebDriverWait(driver, 15).until(
        lambda d: "thongtinmuahang" in d.current_url
    )
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.ID, "name"))
    )


# ── Helper: điền form đặt hàng ──────────────────────────────────────────────
def dien_form(driver, ho_ten="", email="", dia_chi="", hinh_thuc="cod"):
    if ho_ten:
        driver.find_element(By.ID, "name").clear()
        driver.find_element(By.ID, "name").send_keys(ho_ten)
    if email:
        driver.find_element(By.ID, "email").clear()
        driver.find_element(By.ID, "email").send_keys(email)
    if dia_chi:
        driver.find_element(By.ID, "address").clear()
        driver.find_element(By.ID, "address").send_keys(dia_chi)

    if hinh_thuc == "bank":
        el = driver.find_element(By.ID, "thanhtoanonline")
    else:
        el = driver.find_element(By.ID, "thanhtoankhinhanhang")

    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
    time.sleep(0.3)
    driver.execute_script("arguments[0].click();", el)
    time.sleep(0.5)


# ── Helper: click nút Đặt hàng ──────────────────────────────────────────────
def click_dat_hang(driver):
    btn = driver.find_element(By.ID, "form-button")
    driver.execute_script("arguments[0].click();", btn)
    try:
        WebDriverWait(driver, 5).until(EC.alert_is_present())
        return driver.switch_to.alert
    except Exception:
        return None


# ── DH-01: Đặt hàng thành công ─────────────────────────────────────────────
def test_DH01_dat_hang_thanh_cong(driver):
    rows = doc_csv("test_data/test_data_dathang.csv", "success_cod")
    dang_nhap(driver)
    xoa_sach_gio(driver)

    for row in rows:
        vao_trang_dat_hang(driver)
        dien_form(driver,
                  row["ho_ten"],
                  row["email"],
                  row["dia_chi"],
                  row["hinh_thuc_thanh_toan"])
        alert = click_dat_hang(driver)
        assert alert is not None
        assert "Đặt hàng thành công" in alert.text
        alert.accept()


# ── DH-02: Chưa đăng nhập → chuyển đến trang đăng nhập ────────────────────
def test_DH02_chua_dang_nhap(driver):
    driver.delete_all_cookies()
    driver.get(URL_CHITIET)
    time.sleep(2)

    btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "btn-them-gio"))
    )
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", btn)
    time.sleep(0.3)
    driver.execute_script("arguments[0].click();", btn)
    time.sleep(2)

    driver.get(URL_GIO_HANG)
    time.sleep(1)

    btn_dh = driver.find_element(By.ID, "btn-dathang")
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", btn_dh)
    time.sleep(0.3)
    driver.execute_script("arguments[0].click();", btn_dh)
    time.sleep(2)

    assert "dangnhap" in driver.current_url, \
        "Không chuyển đến trang đăng nhập khi chưa đăng nhập"


# ── DH-03: Để trống Họ và tên ──────────────────────────────────────────────
def test_DH03_trong_ho_ten(driver):
    rows = doc_csv("test_data/test_data_dathang.csv", "error_empty_hoten")
    dang_nhap(driver)
    xoa_sach_gio(driver)

    for row in rows:
        vao_trang_dat_hang(driver)
        dien_form(driver, "", row["email"], row["dia_chi"])
        driver.execute_script("document.getElementById('form-button').click();")
        time.sleep(0.5)

        name_input = driver.find_element(By.ID, "name")
        assert "is-invalid" in name_input.get_attribute("class"), \
            "Không hiển thị lỗi khi để trống Họ và tên"
        assert "thongtinmuahang" in driver.current_url


# ── DH-04: Để trống Email ───────────────────────────────────────────────────
def test_DH04_trong_email(driver):
    rows = doc_csv("test_data/test_data_dathang.csv", "error_empty_email")
    dang_nhap(driver)
    xoa_sach_gio(driver)

    for row in rows:
        vao_trang_dat_hang(driver)
        dien_form(driver, row["ho_ten"], "", row["dia_chi"])
        driver.execute_script("document.getElementById('form-button').click();")
        time.sleep(0.5)

        email_input = driver.find_element(By.ID, "email")
        assert "is-invalid" in email_input.get_attribute("class"), \
            "Không hiển thị lỗi khi để trống Email"
        assert "thongtinmuahang" in driver.current_url


# ── DH-05: Để trống Địa chỉ giao hàng ─────────────────────────────────────
def test_DH05_trong_dia_chi(driver):
    rows = doc_csv("test_data/test_data_dathang.csv", "error_empty_diachi")
    dang_nhap(driver)
    xoa_sach_gio(driver)

    for row in rows:
        vao_trang_dat_hang(driver)
        dien_form(driver, row["ho_ten"], row["email"], "")
        driver.execute_script("document.getElementById('form-button').click();")
        time.sleep(0.5)

        address_input = driver.find_element(By.ID, "address")
        assert "is-invalid" in address_input.get_attribute("class"), \
            "Không hiển thị lỗi khi để trống Địa chỉ"
        assert "thongtinmuahang" in driver.current_url


# ── DH-06: Email sai định dạng ─────────────────────────────────────────────
def test_DH06_email_sai_dinh_dang(driver):
    rows = doc_csv("test_data/test_data_dathang.csv", "error_email_format")
    dang_nhap(driver)
    xoa_sach_gio(driver)

    for row in rows:
        vao_trang_dat_hang(driver)
        dien_form(driver, row["ho_ten"], row["email"], row["dia_chi"])
        driver.execute_script("document.getElementById('form-button').click();")
        time.sleep(0.5)

        email_input = driver.find_element(By.ID, "email")
        assert "is-invalid" in email_input.get_attribute("class"), \
            "Không hiển thị lỗi khi email sai định dạng"
        assert "thongtinmuahang" in driver.current_url