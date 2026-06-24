# Hướng dẫn chạy kiểm thử N10-Mart

## Cấu trúc thư mục
```
N10Mart_KiemThu/
├── conftest.py              ← Cấu hình chung, tài khoản test
├── pytest.ini               ← Cấu hình pytest
├── test_dangky.py           ← TC Đăng ký
├── test_dangnhap.py         ← TC Đăng nhập
├── test_timkiem.py          ← TC Tìm kiếm
├── test_chitietsanpham.py   ← TC Chi tiết sản phẩm
├── test_loc_sapxep.py       ← TC Lọc & Sắp xếp
├── test_giohang.py          ← TC Giỏ hàng
├── test_dathang.py          ← TC Đặt hàng
├── test_data/               ← File dữ liệu CSV
│   ├── test_data_dangky.csv
│   ├── test_data_dangnhap.csv
│   └── test_data_dathang.csv
└── reports/                 ← Báo cáo HTML xuất ra đây
    └── bao_cao_ket_qua.html
```

## Chuẩn bị trước khi chạy

1. Chạy web N10-Mart lên: `python manage.py runserver`
2. Tạo tài khoản test trên web (đăng ký thủ công):
   - Username: testuser
   - Password: test123456
   - Email: test@gmail.com
3. Mở file `conftest.py`, đổi TEST_USERNAME / TEST_PASSWORD nếu khác
4. Mở file `test_chitietsanpham.py` và `test_giohang.py`, đổi ID_SANPHAM = ID sản phẩm có trong DB

## Chạy toàn bộ test

```
cd N10Mart_KiemThu
pytest
```

## Chạy từng chức năng

```
pytest test_dangky.py
pytest test_dangnhap.py
pytest test_timkiem.py
pytest test_chitietsanpham.py
pytest test_loc_sapxep.py
pytest test_giohang.py
pytest test_dathang.py
```

## Xem báo cáo

Sau khi chạy xong, mở file: `reports/bao_cao_ket_qua.html`
