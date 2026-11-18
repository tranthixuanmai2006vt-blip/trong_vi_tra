# Cập nhật bánh và hình ảnh

## Danh mục đã có giá

Đã cập nhật đủ 5 loại bánh theo tên và giá nhóm cung cấp.

| Bánh | Quy cách và giá | Tên ảnh ví dụ PNG |
|---|---|---|
| CRACKER MERINGUE COOKIES VỊ TRUYỀN THỐNG | Pack 2 cái 2.500đ; Combo 2 pack (4 cái) 4.000đ | cracker-meringue-cookies-truyen-thong.png |
| CRACKER MERINGUE COOKIES VỊ MATCHA | Pack 2 cái 2.500đ; Combo 2 pack (4 cái) 4.000đ | cracker-meringue-cookies-matcha.png |
| CRACKER MERINGUE COOKIES VỊ OOLONG | Pack 2 cái 2.500đ; Combo 2 pack (4 cái) 4.000đ | cracker-meringue-cookies-oolong.png |
| MOCHI MATCHA MILK CHEESE | 7.500đ / 1 cái | mochi-matcha-milk-cheese.png |
| PAPAROTI MATCHA | 10.000đ / 1 cái | paparoti-matcha.png |

## Folder ảnh chính xác trong bộ code

Thư mục bạn gọi statics_img trong bộ này thực tế là **static/img/**. Ảnh từng bánh cần đặt trong **static/img/products/**, giống ảnh từng trà. Không tạo thêm folder statics_img vì app không đọc folder đó.

Hỗ trợ PNG, JPG, JPEG và WebP viết thường. Chỉ đổi tên trước đuôi; giữ định dạng gốc. Ví dụ ảnh JPG vị matcha là cracker-meringue-cookies-matcha.jpg. Mỗi bánh giữ một ảnh chính; ảnh dùng chung cho danh mục, chi tiết, giỏ hàng và thẻ chọn món Tạo hộp quà. Bộ code chưa chứa ảnh bánh mới.

Ảnh vuông khoảng 1200×1200px, thấy đủ chiếc bánh và nhân, nền phù hợp bộ nhận diện. Web hiển thị contain nên không cắt bánh. Đổi ảnh cùng tên → push GitHub và deploy Render → tải lại trang; URL có phiên bản để hạn chế ảnh cũ trong cache.

## Banner phần Bánh

Ảnh banner riêng đặt trực tiếp tại **static/img/cover-banh.jpg** (hoặc .png/.webp), không để trong products. Ảnh ngang khoảng 1920×600px, sản phẩm lệch phải, để vùng trống bên trái cho tiêu đề.

Banner Bánh dùng cùng cơ chế ảnh với Hộp quà. Riêng lớp phủ sáng bên trái đã giảm opacity từ 0.96/0.83 còn 0.84/0.70 cho dịu hơn và lộ ảnh rõ hơn. Giữ opacity ảnh gốc 1, không làm cả ảnh bạc màu; không đổi banner Hộp quà và trang chủ.

## Cách mua và tính tiền

- Mỗi vị cookie là một sản phẩm có hai quy cách. Chọn Pack 2 cái rồi số lượng 2 là 5.000đ; muốn giá combo 4.000đ phải chọn quy cách Combo 2 pack (4 cái). Không tự áp combo trộn vị vì chưa có yêu cầu đó.
- Mochi tính 7.500đ × số cái. Paparoti Matcha tính 10.000đ × số cái.
- Giá lấy từ server cho danh mục, chi tiết, giỏ và Tạo hộp quà; không tin giá do trình duyệt gửi lên.
- Tồn kho/sức chứa/thời gian chuẩn bị vẫn là demo. Thành phần, dị ứng, HSD và điểm Tea DNA chưa được tự suy đoán. Các bánh này chưa được chấm % hợp gu.
- Gift set demo còn chứa bánh cũ đã được tạm ẩn; không tự thay bánh hoặc giữ giá set cũ. Bạn vẫn tạo hộp riêng từ trà và bánh mới.

## Đưa code lên

Giải nén → chép nội dung thư mục trong_vi_tra vào repo → thêm ảnh đúng tên → commit/push GitHub → chờ Render deploy. Giữ database và cấu hình môi trường hiện tại. Trang chủ giữ nguyên template và ảnh riêng như bản bạn đã gửi. 11 trà và giá đã sửa ở bản trước vẫn giữ nguyên. Chưa tự deploy.
