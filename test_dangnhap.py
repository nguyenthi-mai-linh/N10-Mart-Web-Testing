"""
Test script: Chức năng Đăng nhập
Web: N10-Mart | http://127.0.0.1:8000
Test cases: DN-01 đến DN-05
"""
import csv
import time
import pytest
from selenium.webdriver.common.by import By
from conftest import BASE_URL, driver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

URL_DANGNHAP = f"{BASE_URL}/dangnhap/"


# ── Helper: đọc CSV theo ket_qua_mong_doi ───────────────────────────────────
def doc_csv(ket_qua):
    ds_du_lieu = []

    with open("test_data/test_data_dangnhap.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:

            if not row:
                continue

            ma_tc = str(row.get("ma_tc") or "").strip()

            if ma_tc == "#" or ma_tc == "":
                continue

            ket_qua_csv = str(row.get("ket_qua_mong_doi") or "").strip()

            if ket_qua_csv == ket_qua:
                ds_du_lieu.append(row)

    return ds_du_lieu

# ── Helper: điền form đăng nhập và click nút ────────────────────────────────


def dien_form_dangnhap(driver, username="", password=""):
    driver.delete_all_cookies()

    driver.get(URL_DANGNHAP)

    print("URL 1 =", driver.current_url)

    time.sleep(3)

    print("URL 2 =", driver.current_url)

    print(driver.page_source[:1000])

    if username:
        driver.find_element(By.NAME, "username").send_keys(username)

    if password:
        driver.find_element(By.NAME, "password").send_keys(password)

    btn = driver.find_element(By.CSS_SELECTOR, "button.btn-auth")
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", btn)
    time.sleep(0.3)
    driver.execute_script("arguments[0].click();", btn)

    time.sleep(1.5)

# ── DN-01: Đăng nhập thành công ─────────────────────────────────────────────
def test_DN01_dangnhap_thanh_cong(driver):

    ds_du_lieu = doc_csv("success")

    for row in ds_du_lieu:

        dien_form_dangnhap(
            driver,
            row["username"],
            row["password"]
        )

        assert "/dangnhap/" not in driver.current_url


# ── DN-02: Để trống Username ────────────────────────────────────────────────
def test_DN02_trong_username(driver):

    ds_du_lieu = doc_csv("error_empty_username")

    for row in ds_du_lieu:

        dien_form_dangnhap(
            driver,
            row["username"],
            row["password"]
        )

        assert "dangnhap" in driver.current_url


# ── DN-03: Để trống Password ────────────────────────────────────────────────
def test_DN03_trong_password(driver):

    ds_du_lieu = doc_csv("error_empty_password")

    for row in ds_du_lieu:

        dien_form_dangnhap(
            driver,
            row["username"],
            row["password"]
        )

        assert "dangnhap" in driver.current_url





# ── DN-04: Username không tồn tại ──────────────────────────────────────────
def test_DN04_username_khong_ton_tai(driver):

    ds_du_lieu = doc_csv("error_not_exist")

    for row in ds_du_lieu:

        dien_form_dangnhap(
            driver,
            row["username"],
            row["password"]
        )

        assert "không tồn tại" in driver.page_source

# ── DN-05: Password không chính xác ────────────────────────────────────────
def test_DN05_password_sai(driver):

    ds_du_lieu = doc_csv("error_wrong_password")

    for row in ds_du_lieu:

        driver.get(URL_DANGNHAP)

        dien_form_dangnhap(
            driver,
            row["username"],
            row["password"]
        )

        error_text = driver.find_element(By.CSS_SELECTOR, ".alert-danger").text

        assert "Mật khẩu không đúng" in error_text

