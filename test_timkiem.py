"""
Test script: Chức năng Tìm kiếm sản phẩm
Web: N10-Mart | http://127.0.0.1:8000
Test cases: TK-01 đến TK-03
"""
import os
import csv
import time
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from conftest import BASE_URL

URL_HOME = f"{BASE_URL}/home/"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, "test_data", "test_data_timkiem.csv")


# ── Helper: đọc CSV theo ket_qua_mong_doi ───────────────────────────────────


def doc_csv(ket_qua):
    rows = []

    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            if (row.get("ket_qua_mong_doi") or "").strip() == ket_qua:
                rows.append(row)

    return rows

# ── Helper: thực hiện tìm kiếm ──────────────────────────────────────────────
def tim_kiem(driver, tu_khoa):
    driver.get(URL_HOME)
    
    time.sleep(1)
    search_input = driver.find_element(By.CSS_SELECTOR, "input[name='searched']")
    search_input.clear()
    if tu_khoa:
        search_input.send_keys(tu_khoa)
    search_input.send_keys(Keys.ENTER)
    time.sleep(1.5)


# ── TK-01: Tìm kiếm thành công với từ khóa hợp lệ ─────────────────────────
def test_TK01_timkiem_tu_khoa_hop_le(driver):
    """Hệ thống hiển thị danh sách sản phẩm phù hợp với từ khóa"""

    rows = doc_csv("success")

    for row in rows:

        tim_kiem(driver, row["tu_khoa"])

        assert "search" in driver.current_url, \
            f"Không chuyển đến trang kết quả tìm kiếm với từ khóa: {row['tu_khoa']}"

        page_source = driver.page_source

        assert "Đã tìm thấy" in page_source, \
            f"Không hiển thị kết quả tìm kiếm hợp lệ với từ khóa: {row['tu_khoa']}"


# ── TK-02: Tìm kiếm với từ khóa để trống ───────────────────────────────────
def test_TK02_timkiem_tu_khoa_trong(driver):
    """Hệ thống hiển thị thông báo Vui lòng nhập từ khóa tìm kiếm"""
    tim_kiem(driver, "")

    page_source = driver.page_source
    assert "Vui lòng nhập từ khóa" in page_source, \
        "Không hiển thị thông báo khi để trống từ khóa"


# ── TK-03: Tìm kiếm với từ khóa không tồn tại ─────────────────────────────
def test_TK03_timkiem_khong_co_ket_qua(driver):
    """Hệ thống hiển thị thông báo Không tìm thấy sản phẩm nào"""

    rows = doc_csv("error_not_found")

    for row in rows:

        tim_kiem(driver, row["tu_khoa"])

        page_source = driver.page_source

        assert "Không tìm thấy" in page_source, \
            f"Không hiển thị thông báo khi từ khóa không tồn tại: {row['tu_khoa']}"


