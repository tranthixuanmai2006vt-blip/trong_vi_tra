# 🍵 Trồng Vị Nhà — Hằng Sơn Điền × Trà

**Cập nhật danh mục trà 18/11/2026:** xem `HUONG_DAN_CAP_NHAT_TRA.md` để biết 11 giá/quy cách đã sửa và tên file ảnh trong `static/img/products/`. Giá trà đã theo ảnh nhóm gửi; các dữ liệu khác vẫn là demo.

**Ảnh banner và danh mục trang chủ:** xem `HUONG_DAN_ANH_BANNER.md`. Ảnh banner đặt trực tiếp trong `static/img/`; ảnh từng sản phẩm vẫn ở `static/img/products/`.

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
| `/ve-chung-toi` | Về Hằng Sơn Điền |
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

## Thay ảnh & font (bản nâng cấp)
Web tự dùng ảnh thật nếu thấy file trong `static/img/`, chưa có thì hiện ảnh minh họa SVG:
`cover-desktop.jpg` (16:7) · `cover-mobile.jpg` (4:5) · `cat-tra.jpg` `cat-banh.jpg` `cat-hopqua.jpg` (4:5) · `svc-tu-tao.jpg` `svc-theo-yeu-cau.jpg` (4:3) ·
`doi-tra-bao-loc.jpg` · `giay-tra.jpg` · `story-1..4.jpg` · `region-olong.jpg` `region-matcha.jpg` `region-traxanh.jpg` · `qt-tra-1..4.jpg` `qt-banh-1..4.jpg` ·
`team-main.jpg` `team-1.jpg` `team-2.jpg` · `cover-tra.jpg` `cover-banh.jpg` `cover-hopqua.jpg`.
Font tiêu đề: bỏ `DFVN-Basteleur.woff2` (hoặc .ttf/.otf) vào `static/fonts/`; chưa có thì dùng Lora.
