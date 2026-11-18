# Thay ảnh phần Sản phẩm và Tạo hộp quà

Đặt các ảnh dưới đây trực tiếp vào **static/img/**. Không đặt vào static/img/products/ (thư mục đó dành cho ảnh từng sản phẩm trà).

| Vị trí | Tên ảnh ví dụ JPG | Tỷ lệ gợi ý |
|---|---|---|
| Banner đầu trang Trà | cover-tra.jpg | 16:5, khoảng 1920×600px |
| Banner đầu trang Bánh từ trà | cover-banh.jpg | 16:5, khoảng 1920×600px |
| Banner đầu trang Hộp quà trong ảnh bạn gửi | cover-hopqua.jpg | 16:5, khoảng 1920×600px |

## Phạm vi thay đổi

Các ảnh cover-tra, cover-banh và cover-hopqua chỉ dùng ở banner trang danh mục Sản phẩm. Trang chủ giữ nguyên template và cách nhận ảnh riêng của bản bạn gửi; không tự lấy ảnh banner sản phẩm. Không thay file cat-tra, cat-banh, cat-hopqua, cover-desktop hay cover-mobile của trang chủ.

Ảnh từng trà đặt ở static/img/products/ theo bảng trong HUONG_DAN_CAP_NHAT_TRA.md. Bộ ảnh này dùng chung cho danh sách, trang chi tiết, giỏ và các thẻ chọn món trong dịch vụ Tạo hộp quà. Tên ảnh banner không dùng làm ảnh của từng món.

Code nhận cả .jpg, .jpeg, .png và .webp viết thường. Giữ đúng định dạng gốc, chỉ đổi tên trước dấu chấm. Ví dụ ảnh PNG đặt **cover-hopqua.png**, không đổi đuôi PNG thành JPG. Mỗi tên chỉ giữ một định dạng; thứ tự ưu tiên khi trùng là WebP, JPG, JPEG, PNG.

## Bố cục ảnh

- Banner danh mục dùng ảnh phủ toàn bộ khung, tiêu đề và câu dẫn vẫn là chữ web, dễ sửa. Ảnh nên tập trung sản phẩm ở giữa lệch phải, chừa phía trái ít chi tiết cho chữ. Không chèn lại chữ Hộp quà vào ảnh để tránh trùng tiêu đề.
- Điện thoại đưa ảnh lên trên, chữ xuống dưới để dễ đọc. Có thể thêm ảnh riêng cover-tra-mobile.jpg, cover-banh-mobile.jpg, cover-hopqua-mobile.jpg; nếu không có, web vẫn dùng ảnh ngang.
- Chưa có ảnh: khu vực danh mục hiện nền chờ ảnh với dòng thông báo, không còn ba icon hộp/thiệp trong banner đó. Bộ code không chứa ảnh chụp mới; bạn thêm ảnh theo tên ở bảng.

## Đưa lên website

Giải nén code mới → chép vào repo hiện tại → thêm ảnh đúng thư mục → commit và push GitHub → chờ Render deploy thành công → tải lại web. Thay ảnh sau này vẫn giữ nguyên tên; đường dẫn ảnh có phiên bản theo thời gian sửa file để hạn chế cache cũ. Giữ database và cấu hình môi trường của bản đang chạy.

Bản này giữ toàn bộ cập nhật 11 sản phẩm trà và giá ở bản ZIP trước. Không cập nhật giao diện trang chủ. Chưa tự push GitHub hoặc deploy Render.
