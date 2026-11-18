# Cập nhật danh mục trà và ảnh Hằng Sơn Điền

## 1. Bộ code này đã sửa gì

- Thay 6 dòng trà demo bằng đúng 11 tên, khối lượng và giá theo ảnh danh mục bạn gửi. SKU là mã nội bộ web.
- Giá dùng chung từ data.py, nên danh mục, chi tiết, giỏ và cấu hình hộp quà cùng lấy giá mới. tea_catalog.json chỉ là bản đối chiếu, không phải file cấu hình đang chạy.
- Bỏ bộ lọc Matcha / Trà xanh vì không có trong danh mục trà mới; thêm Lão trà.
- Không tự tạo mô tả hương vị, vùng trồng, thành phần hoặc thông số pha chưa có dữ liệu. Trà mới chưa có điểm Tea DNA nên chưa được chấm % hợp gu.
- Tạm ẩn G02, G03, G04 (hộp quà chứa trà mẫu bị loại). Dữ liệu mẫu vẫn giữ trong data.py để nhóm biên tập; không tự đổi thành phần hoặc giá set. G01 và dữ liệu bánh vẫn là demo.
- Không đổi nguyên liệu bánh thành trà khác. Gỡ liên kết trà nguyên liệu và gợi ý không còn bán. Công thức blog/Tea DNA chỉ là tham khảo; nguyên liệu ngoài danh mục không có nút mua.
- Tồn kho 30 cho mỗi trà, sức chứa hộp và phí vẫn là demo, không phải số thực. Chỉ đổi giá bán lẻ trà theo bảng đã gửi; không gán giá này cho cả hộp quà.

## 2. Đặt ảnh vào đâu

Tạo hoặc mở thư mục **static/img/products/** (ngang cấp với các thư mục ảnh khác bên trong static/img). Đặt ảnh vào đúng thư mục này; không để ở templates hoặc uploads.

Chỉ đổi phần tên trước đuôi file. Hỗ trợ .webp, .jpg, .jpeg và .png viết thường; KHÔNG đổi đuôi .png thành .jpg nếu chưa chuyển định dạng. Ví dụ ảnh PNG của Ô Long Sữa đặt tên tra-o-long-sua-cao-cap.png. Mỗi sản phẩm chỉ giữ một file; nếu có nhiều định dạng, ưu tiên webp, jpg, jpeg rồi png.

| Sản phẩm | Quy cách | Giá | Tên ảnh (ví dụ JPG) |
|---|---:|---:|---|
| Trà Ô Long Sữa Cao Cấp HSĐ | Gói 200g | 180.000đ | `tra-o-long-sua-cao-cap.jpg` |
| Hồng Trà Cao Cấp HSĐ | Gói 200g | 180.000đ | `hong-tra-cao-cap.jpg` |
| Lão Trà Cao Cấp HSĐ | Gói 200g | 104.000đ | `lao-tra-cao-cap.jpg` |
| Trà Đông Phương Mỹ Nhân Thượng Hạng HSĐ | Gói 100g | 296.000đ | `tra-dong-phuong-my-nhan.jpg` |
| Trà Ô Long Tuyết Thượng Hạng HSĐ | Gói 100g | 370.000đ | `tra-o-long-tuyet-thuong-hang.jpg` |
| Trà Ô Long Quế Hoa Thượng Hạng HSĐ | Gói 100g | 222.000đ | `tra-o-long-que-hoa-thuong-hang.jpg` |
| Trà Ô Long Tứ Quý HSĐ | Gói 250g | 130.000đ | `tra-o-long-tu-quy.jpg` |
| Trà Ô Long Kim Tuyên HSĐ | Gói 250g | 110.000đ | `tra-o-long-kim-tuyen.jpg` |
| Trà Ô Long Cao Sơn HSĐ | Gói 250g | 130.000đ | `tra-o-long-cao-son.jpg` |
| Trà Ô Long Tứ Quý Cao Cấp HSĐ | Gói 250g | 225.000đ | `tra-o-long-tu-quy-cao-cap.jpg` |
| Trà Ô Long Kim Tuyên Cao Cấp HSĐ | Gói 250g | 225.000đ | `tra-o-long-kim-tuyen-cao-cap.jpg` |

Tên file phải khớp hoàn toàn, không dấu, không khoảng trắng, không thêm (1), không dùng chữ hoa. HSĐ trong tên sản phẩm không cần thêm vào tên ảnh. Khối lượng trong bảng lấy từ chữ trên ảnh bao bì.

Một ảnh chính được dùng tự động ở danh mục, trang chi tiết, giỏ, món gợi ý và chọn món tạo quà. Khi sản phẩm được bật lại cho Tea DNA, cùng bộ ảnh cũng dùng ở đó. Chưa có ảnh đúng tên thì web giữ hình minh họa thay vì hiện ảnh lỗi. Không có ảnh sản phẩm mới trong ZIP này.

Ảnh gợi ý: 1200×1200px, khung vuông, thấy đủ bao bì; JPG/WebP cho ảnh nền, PNG nếu cần nền trong. Web dùng contain để không cắt chữ hoặc bao bì. Cập nhật file ảnh và tải lại trang: đường dẫn có phiên bản theo thời gian sửa file để hạn chế cache cũ.

## 3. Chạy và cập nhật GitHub / Render

1. Giải nén ZIP. Mở thư mục trong_vi_tra có app.py, data.py, templates và static.
2. Copy file trong thư mục này vào repo hiện tại (không upload nguyên ZIP). Ưu tiên đồng bộ toàn bộ templates, static, app.py và data.py vì đường dẫn ảnh được dùng chung.
3. Đặt 11 ảnh vào static/img/products/ theo bảng. Commit và push lên GitHub. Nếu Render bật auto-deploy, chờ deploy xong; nếu không, chọn Manual Deploy / Deploy latest commit. Lưu ý upload ảnh ở máy cá nhân chưa làm ảnh xuất hiện trên Render cho đến khi push/deploy.
4. Mở /san-pham/tra: phải thấy 11 trà. Thử sắp giá tăng dần: Lão Trà 104.000đ đầu tiên, Ô Long Tuyết 370.000đ cuối cùng. Đông Phương Mỹ Nhân là 296.000đ / 100g.
5. Kiểm tra trang chi tiết, thêm giỏ và chọn trà tạo hộp quà. Nếu trình duyệt đang lưu hộp quà demo cũ, bắt đầu cấu hình mới. Các món đã bỏ không thể đặt tiếp bằng SKU cũ.

Chạy tại máy: python3 -m venv .venv, kích hoạt môi trường, pip install -r requirements.txt, python app.py, mở http://127.0.0.1:8000.

ZIP không kèm .venv, .git, database, uploads hay tệp hệ thống macOS. Khi chép vào bản đang chạy, GIỮ database hiện tại, SECRET_KEY và cấu hình môi trường; không xóa đơn hàng hoặc dữ liệu đã có. Code chưa tự đẩy lên GitHub/Render.

## 4. Nếu muốn sửa giá sau này

Chỉnh variants[0]['price'] của đúng trà trong data.py (số nguyên VND), commit và deploy lại. Không chỉnh giá trực tiếp trong HTML. Đổi ảnh không cần sửa data.py nếu tên file đã đúng bảng.
