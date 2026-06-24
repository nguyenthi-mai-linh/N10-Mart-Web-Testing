"""
Test script: Chức năng Đăng ký
Web: N10-Mart | http://127.0.0.1:8000
Test cases: DK-01 đến DK-10
"""
import csv
import time
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from conftest import BASE_URL, driver

URL_DANGKY  = f"{BASE_URL}/dangky/"
URL_DANGNHAP = f"{BASE_URL}/dangnhap/"


# ── Helper: đọc CSV theo ket_qua_mong_doi ───────────────────────────────────
def doc_csv(ket_qua):
    ds_du_lieu = []

    with open("test_data/test_data_dangky.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:

            ma_tc = row.get("ma_tc", "").strip()

            # bỏ dòng phân cách #
            if ma_tc == "#" or ma_tc == "":
                continue

            if (row.get("ket_qua_mong_doi") or "").strip() == ket_qua:
                ds_du_lieu.append(row)

    return ds_du_lieu


# ── Helper: điền form đăng ký và submit ─────────────────────────────────────
def dien_form_dangky(driver, username="", email="", password1="", password2=""):
    driver.get(URL_DANGKY)
    time.sleep(1)
    if username:
        driver.find_element(By.NAME, "username").send_keys(username)
    if email:
        driver.find_element(By.NAME, "email").send_keys(email)
    if password1:
        driver.find_element(By.NAME, "password1").send_keys(password1)
    if password2:
        driver.find_element(By.NAME, "password2").send_keys(password2)
    btn = driver.find_element(By.CSS_SELECTOR, "button.btn-auth")
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", btn)
    time.sleep(0.3)
    driver.execute_script("arguments[0].click();", btn)
    time.sleep(1.5)


# ── DK-01: Đăng ký thành công ───────────────────────────────────────────────

def test_DK01_dangky_thanh_cong(driver):
    ds_du_lieu = doc_csv("success")
    for row in ds_du_lieu:
        dien_form_dangky(
            driver,
            row["username"],
            row["email"],
            row["password1"],
            row["password2"]
        )
        print("\n>>> URL sau submit:", driver.current_url)
        assert "dangnhap" in driver.current_url
        assert "Đăng ký thành công" in driver.page_source

# ── DK-02: Để trống Username ────────────────────────────────────────────────
def test_DK02_trong_username(driver):

    ds_du_lieu = doc_csv("error_empty_username")

    for row in ds_du_lieu:

        dien_form_dangky(
            driver,
            row["username"],
            row["email"],
            row["password1"],
            row["password2"]
        )

        assert "dangky" in driver.current_url

# ── DK-03: Để trống Email ───────────────────────────────────────────────────
def test_DK03_trong_email(driver):

    ds_du_lieu = doc_csv("error_empty_email")

    for row in ds_du_lieu:

        dien_form_dangky(
            driver,
            row["username"],
            row["email"],
            row["password1"],
            row["password2"]
        )

        assert "dangky" in driver.current_url

# ── DK-04: Để trống Mật khẩu ───────────────────────────────────────────────
def test_DK04_trong_matkhau(driver):

    ds_du_lieu = doc_csv("error_empty_password")

    for row in ds_du_lieu:

        dien_form_dangky(
            driver,
            row["username"],
            row["email"],
            row["password1"],
            row["password2"]
        )

        assert "dangky" in driver.current_url

# ── DK-05: Để trống Xác nhận mật khẩu ─────────────────────────────────────
def test_DK05_trong_xacnhan_matkhau(driver):

    ds_du_lieu = doc_csv("error_empty_confirm")

    for row in ds_du_lieu:

        dien_form_dangky(
            driver,
            row["username"],
            row["email"],
            row["password1"],
            row["password2"]
        )

        assert "dangky" in driver.current_url


# ── DK-06: Email sai định dạng ─────────────────────────────────────────────
def test_DK06_email_sai_dinh_dang(driver):

    ds_du_lieu = doc_csv("error_invalid_email")

    for row in ds_du_lieu:

        dien_form_dangky(
            driver,
            row["username"],
            row["email"],
            row["password1"],
            row["password2"]
        )

        assert "dangky" in driver.current_url


# ── DK-07: Mật khẩu xác nhận không khớp ───────────────────────────────────
def test_DK07_matkhau_khong_khop(driver):

    ds_du_lieu = doc_csv("error_password_mismatch")

    for row in ds_du_lieu:

        dien_form_dangky(
            driver,
            row["username"],
            row["email"],
            row["password1"],
            row["password2"]
        )

        assert "Mật khẩu xác nhận không khớp." in driver.page_source

# ── DK-08: Username đã tồn tại ─────────────────────────────────────────────
def test_DK08_username_da_ton_tai(driver):

    ds_du_lieu = doc_csv("error_username_exists")

    for row in ds_du_lieu:

        dien_form_dangky(
            driver,
            row["username"],
            row["email"],
            row["password1"],
            row["password2"]
        )

        assert "Tên đăng nhập đã được sử dụng." in driver.page_source

# ── DK-09: Email đã tồn tại ────────────────────────────────────────────────
def test_DK09_email_da_ton_tai(driver):

    ds_du_lieu = doc_csv("error_email_exists")

    for row in ds_du_lieu:

        dien_form_dangky(
            driver,
            row["username"],
            row["email"],
            row["password1"],
            row["password2"]
        )

        assert "Email đã được sử dụng." in driver.page_source


# ── DK-10: Mật khẩu quá ngắn (< 6 ký tự) ──────────────────────────────────
def test_DK10_matkhau_qua_ngan(driver):

    ds_du_lieu = doc_csv("error_password_short")

    for row in ds_du_lieu:

        dien_form_dangky(
            driver,
            row["username"],
            row["email"],
            row["password1"],
            row["password2"]
        )

        assert "Mật khẩu phải có ít nhất 6 ký tự." in driver.page_source