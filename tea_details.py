"""Nội dung chi tiết do nhóm cung cấp. Hiện mới áp dụng cho Ô Long Sữa T07."""


def apply_tea_details(products):
    tea = next(p for p in products if p['id'] == 'T07')
    tea.update({
        'page_title': 'Trà Ô Long Sữa Cao Cấp HSĐ 200G – Trà Ô Long Bảo Lộc',
        'origin_label': 'Trà Ô Long Bảo Lộc',
        'region': 'Bảo Lộc, Lâm Đồng, Việt Nam',
        'taste_note': 'Hương sữa dịu ngọt, vị thanh, chát nhẹ, hậu ngọt sâu.',
        'desc': 'Hương sữa dịu ngọt quyện cùng vị Ô Long thanh tao, chát nhẹ và hậu ngọt sâu. Một vị trà êm dịu, dễ uống cho những buổi thưởng trà hằng ngày.',
        'story': [
            'Trà Ô Long Sữa Cao Cấp HSĐ 200G được tuyển chọn từ những búp trà Ô Long chất lượng cao trên các đồi trà Hằng Sơn Điền – Bảo Lộc, Lâm Đồng. Nơi đây, cây trà được chăm sóc bền bỉ qua nhiều năm để tạo nên hương vị đặc trưng của vùng cao nguyên.',
            'Hương sữa dịu ngọt hòa quyện cùng vị trà thanh tao và hậu vị ngọt sâu, mang đến trải nghiệm thưởng trà êm dịu, dễ uống và phù hợp với nhiều đối tượng.',
        ],
        'highlights': [
            'Tuyển chọn từ búp trà Ô Long chất lượng cao của Hằng Sơn Điền.',
            'Vùng nguyên liệu Bảo Lộc – Lâm Đồng, chăm sóc kỹ lưỡng qua nhiều năm.',
            'Hương sữa dịu nhẹ, hòa quyện tự nhiên cùng hương trà.',
            'Nước trà vàng hổ phách sáng, trong và bền hương.',
            'Vị thanh ngọt, chát nhẹ, hậu vị kéo dài.',
            'Pha được 4–6 nước, hương vị vẫn hài hòa.',
        ],
        'profile': {
            'Hương': 'Hương sữa dịu ngọt, thanh thoát, quyện cùng hương trà Ô Long.',
            'Vị': 'Êm dịu, ngọt thanh, chát nhẹ và cân bằng.',
            'Màu nước': 'Vàng hổ phách trong sáng.',
            'Hậu vị': 'Ngọt sâu, mềm mại và lưu hương lâu.',
        },
        'suitable_for': [
            'Người yêu thích trà Ô Long hương sữa.',
            'Người mới bắt đầu thưởng thức trà.',
            'Thưởng trà hằng ngày, tiếp khách hoặc làm quà tặng.',
            'Người yêu thích hương vị nhẹ nhàng, dễ uống.',
        ],
        'brew': {'g': 8, 'ml': 150, 'temp': '90–95', 'time_s': '30–45', 'steeps': '4–6', 'timer_s': 30,
                 'note': 'Hãm 30–45 giây cho nước đầu, tăng dần thời gian ở các lần pha sau.'},
        'ingredients': '100% Trà Ô Long Sữa.',
        'product_info': [
            ('Tên sản phẩm', 'Trà Ô Long Sữa Cao Cấp HSĐ'),
            ('Khối lượng tịnh', '200g'),
            ('Thành phần', '100% Trà Ô Long Sữa.'),
            ('Xuất xứ', 'Bảo Lộc, Lâm Đồng, Việt Nam'),
            ('Sản xuất', 'Hằng Sơn Điền'),
            ('Phân phối độc quyền', 'Uniharvest Việt Nam'),
        ],
        'commitments': [
            'Tuyển chọn từ vùng nguyên liệu chất lượng cao.',
            'Đóng gói kín, giữ trọn hương thơm và chất lượng trà.',
            'Phù hợp sử dụng hằng ngày hoặc làm quà tặng.',
        ],
    })
