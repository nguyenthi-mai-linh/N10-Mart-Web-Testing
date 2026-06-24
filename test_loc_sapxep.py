"""
Test script: Chức năng Lọc và Sắp xếp sản phẩm
Web: N10-Mart | http://127.0.0.1:8000
Test cases: LS-01 đến LS-09
"""
import csv
import time
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from conftest import BASE_URL

# Dùng trang Thực phẩm khô để test lọc/sắp xếp
URL_DANH_MUC = f"{BASE_URL}/thucphamkho/"


# ── Helper: đọc CSV theo ket_qua_mong_doi ───────────────────────────────────
def doc_csv(ket_qua):
    rows = []
    with open("test_data/test_data_locsanpham.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get("ket_qua_mong_doi", "").strip() == ket_qua:
                rows.append(row)
    return rows   

# ── Helper: vào trang, nhập bộ lọc và click Lọc ────────────────────────────
def thuc_hien_loc(driver, gia_min="", gia_max="", sort=""):
    driver.get(URL_DANH_MUC)
    time.sleep(1)

    if gia_min:
        inp = driver.find_element(By.NAME, "gia_min")
        inp.clear()
        inp.send_keys(gia_min)
    if gia_max:
        inp = driver.find_element(By.NAME, "gia_max")
        inp.clear()
        inp.send_keys(gia_max)
    if sort:
        select = Select(driver.find_element(By.NAME, "sort"))
        select.select_by_value(sort)

    btn_loc = driver.find_element(By.CSS_SELECTOR, "button[type='submit'].btn-success")
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", btn_loc)
    time.sleep(0.3)
    driver.execute_script("arguments[0].click();", btn_loc)
    time.sleep(1.5)


# ── Helper: lấy danh sách giá từ trang ──────────────────────────────────────
def lay_danh_sach_gia(driver):
    gia_elements = driver.find_elements(By.CSS_SELECTOR, ".product-price")
    gia_list = []
    for el in gia_elements:
        text = el.text.replace("đ", "").replace(",", "").replace(".", "").strip()
        try:
            gia_list.append(float(text))
        except Exception:
            pass
    return gia_list


# ── LS-01: Lọc theo khoảng giá hợp lệ ──────────────────────────────────────
def test_LS01_loc_khoang_gia_hop_le(driver):
    """Hệ thống hiển thị sản phẩm thuộc khoảng giá đã nhập"""
    rows = doc_csv("success")

    for row in rows:
        thuc_hien_loc(driver, row["gia_min"], row["gia_max"])

        assert "gia_min" in driver.current_url or "gia_max" in driver.current_url, \
            "Tham số lọc không được truyền lên URL"

        assert "Hiện chưa có sản phẩm" not in driver.page_source


# ── LS-02: Lọc khi không có sản phẩm thỏa mãn ──────────────────────────────
def test_LS02_loc_khong_co_ket_qua(driver):
    rows = doc_csv("error_not_found")

    for row in rows:
        thuc_hien_loc(driver, row["gia_min"], row["gia_max"])

        assert "Hiện chưa có sản phẩm" in driver.page_source


# ── LS-03: Lọc với giá trị âm ───────────────────────────────────────────────
def test_LS03_loc_gia_tri_am(driver):
    rows = doc_csv("error_negative")

    for row in rows:
        driver.get(URL_DANH_MUC)

        inp_min = driver.find_element(By.NAME, "gia_min")
        inp_min.clear()
        inp_min.send_keys(row["gia_min"])

        btn_loc = driver.find_element(By.CSS_SELECTOR, "button[type='submit'].btn-success")
        driver.execute_script("arguments[0].click();", btn_loc)

        assert URL_DANH_MUC in driver.current_url


# ── LS-04: Sắp xếp giá tăng dần ────────────────────────────────────────────
def test_LS04_sapxep_gia_tang_dan(driver):
    rows = doc_csv("success_sort")

    for row in rows:
        thuc_hien_loc(driver, sort="gia_tang")

        assert "sort=gia_tang" in driver.current_url

        gia_list = lay_danh_sach_gia(driver)
        if len(gia_list) >= 2:
            assert gia_list == sorted(gia_list)


# ── LS-05: Sắp xếp giá giảm dần ────────────────────────────────────────────
def test_LS05_sapxep_gia_giam_dan(driver):
    rows = doc_csv("success_sort")

    for row in rows:
        thuc_hien_loc(driver, sort="gia_giam")

        gia_list = lay_danh_sach_gia(driver)
        if len(gia_list) >= 2:
            assert gia_list == sorted(gia_list, reverse=True)

# ── LS-06: Sắp xếp tên A-Z ─────────────────────────────────────────────────
def test_LS06_sapxep_ten_az(driver):
    """Hệ thống hiển thị sản phẩm theo tên từ A đến Z"""
    thuc_hien_loc(driver, sort="ten_az")

    assert "sort=ten_az" in driver.current_url, \
        "Tham số sort=ten_az không được truyền"

    ten_list = [el.text.strip() for el in driver.find_elements(By.CSS_SELECTOR, ".card-title")]
    if len(ten_list) >= 2:
        import locale
        locale.setlocale(locale.LC_ALL, '')
        assert ten_list == sorted(ten_list, key=locale.strxfrm), \
            f"Sản phẩm không được sắp xếp tên A-Z: {ten_list}"


# ── LS-07: Sắp xếp tên Z-A ─────────────────────────────────────────────────
def test_LS07_sapxep_ten_za(driver):
    """Hệ thống hiển thị sản phẩm theo tên từ Z đến A"""
    thuc_hien_loc(driver, sort="ten_za")

    assert "sort=ten_za" in driver.current_url, \
        "Tham số sort=ten_za không được truyền"

    ten_list = [el.text.strip() for el in driver.find_elements(By.CSS_SELECTOR, ".card-title")]
    if len(ten_list) >= 2:
        import locale
        locale.setlocale(locale.LC_ALL, '')
        assert ten_list == sorted(ten_list, key=locale.strxfrm, reverse=True), \
            f"Sản phẩm không được sắp xếp tên Z-A: {ten_list}"


# ── LS-08: Sắp xếp mới nhất ────────────────────────────────────────────────
def test_LS08_sapxep_moi_nhat(driver):
    """Hệ thống hiển thị sản phẩm theo thứ tự mới nhất"""
    thuc_hien_loc(driver, sort="moi_nhat")

    assert "sort=moi_nhat" in driver.current_url, \
        "Tham số sort=moi_nhat không được truyền"
    assert "Hiện chưa có sản phẩm" not in driver.page_source, \
        "Không hiển thị sản phẩm sau khi sắp xếp mới nhất"



# ── LS-9: Đặt lại bộ lọc ──────────────────────────────────────────────────
def test_LS09_dat_lai_bo_loc(driver):
    rows = doc_csv("success_reset")

    for row in rows:
        thuc_hien_loc(driver, gia_min=row["gia_min"], gia_max=row["gia_max"])
        time.sleep(1)

        btn_reset = driver.find_element(By.CSS_SELECTOR, "a.btn-outline-secondary")
        driver.execute_script("arguments[0].click();", btn_reset)

        assert "gia_min" not in driver.current_url
        assert "gia_max" not in driver.current_url