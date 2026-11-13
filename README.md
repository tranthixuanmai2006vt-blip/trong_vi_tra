# 🍵 Trồng vị Trà — Hằng Sơn Điền × Trà

Website bán trà, bánh từ trà, gift set + dịch vụ **Tạo hộp quà**, **Thiết kế riêng**, **Tea DNA**.
Viết bằng Python (Flask), dựng theo file *[THDAKD] BRIEF WEB* và *[THDAKD] CHI TIẾT WEB*.

## Chạy trong PyCharm (macOS)
```bash
cd ~/Downloads/trong_vi_tra
python3 -m venv .venv            # chỉ cần lần đầu
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```
Mở **http://127.0.0.1:8000** (dùng cổng 8000 vì macOS chiếm cổng 5000 cho AirPlay).
Trong PyCharm: Settings › Project › Python Interpreter › chọn `.venv/bin/python`, rồi bấm ▶ Run `app.py`.

## Các trang
| Đường dẫn | Trang |
|---|---|
| `/` | Trang chủ (9 khối theo spec) |
| `/ve-hang-son-dien` | Về Hằng Sơn Điền |
| `/san-pham`, `/san-pham/tra`, `/san-pham/banh`, `/san-pham/gift-set` | Danh mục + bộ lọc, sắp xếp, tìm kiếm |
| `/san-pham/<loai>/<slug>` | Chi tiết trà / bánh / gift set |
| `/dich-vu/tao-hop-qua` | Tạo hộp quà 6 bước (lưu nháp 24h trên trình duyệt) |
| `/dich-vu/thiet-ke-rieng` | Thiết kế riêng – form gửi yêu cầu, cấp mã YC-… |
| `/chuyen-tra`, `/chuyen-tra/<slug>` | Danh sách & bài viết, newsletter |
| `/tea-dna`, `/tea-dna/ket-qua` | 12 câu, 5 trục, 13 nhóm gu, công thức hợp gu |
| `/gio-hang`, `/thanh-toan` | Giỏ hàng, mã giảm giá, thanh toán COD / chuyển khoản |
| `/tra-cuu-don` | Tra cứu đơn bằng mã + SĐT/email, gửi yêu cầu hỗ trợ |
| `/lien-he` | Liên hệ, form lời nhắn, FAQ có tìm kiếm |
| `/chinh-sach/<slug>` | 8 trang hướng dẫn & chính sách |
| `/admin` | Quản trị demo: xem đơn, đổi trạng thái, xem yêu cầu/lời nhắn |

## Sửa nội dung
**Mọi dữ liệu nằm trong `data.py`**: sản phẩm, giá, tồn kho, hộp/giấy/thiệp/phụ kiện, bài viết,
câu hỏi Tea DNA, FAQ, chính sách, hotline/email/địa chỉ (`SITE`), phí giao, mã giảm giá…
Khi có số liệu thật, sửa ở đó rồi đặt `DEMO_MODE = False` để tắt dải "Bản demo".
Ảnh hiện là **ảnh minh họa SVG**; khi có ảnh thật, thay macro `art()` trong `templates/macros.html`.

Mã giảm giá mẫu để test: `TRONGVITRA10`, `CHAODUYEN`.
Dữ liệu đơn/yêu cầu lưu ở `trongvitra_v2.db` (xóa file để reset). Tệp khách tải lên lưu ở `uploads/`.
