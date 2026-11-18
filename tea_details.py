"""Nội dung chi tiết do nhóm cung cấp. Hiện mới áp dụng cho Ô Long Sữa T07."""


def _apply_milk_tea_details(products):
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


# Nội dung cho 10 trà còn lại: từ [THDAKD] BRIEF WEB (1).pdf do nhóm gửi.
EXTRA_DETAILS = {'T06': {'desc': 'Hương mật ong, trái cây chín và caramel nhẹ; vị đậm đà, ít chát, hậu ngọt sâu. Thưởng '
                 'thức nóng, pha lạnh hoặc kết hợp cùng sữa và trái cây.',
         'taste_note': 'Hương mật ong, trái cây chín và caramel nhẹ; vị đậm đà, ít chát, hậu ngọt sâu. '
                       'Thưởng thức nóng, pha lạnh hoặc kết hợp cùng sữa và trái cây.',
         'profile': {'Hương': 'Dịu nhẹ, ngọt thơm với nốt mật ong và caramel.',
                     'Vị': 'Đậm đà, cân bằng, ít chát và ngọt hậu.',
                     'Màu nước': 'Đỏ hổ phách trong sáng.',
                     'Hậu vị': 'Ngọt sâu, lưu hương lâu và dễ chịu.'},
         'highlights': ['Tuyển chọn từ búp trà chất lượng cao vùng Bảo Lộc.',
                        'Vùng nguyên liệu Hằng Sơn Điền được chăm sóc kỹ lưỡng trong nhiều năm.',
                        'Hương thơm tự nhiên với nốt mật ong, caramel và trái cây chín.',
                        'Màu nước đỏ hổ phách trong đẹp, vị đậm đà, hậu ngọt kéo dài.',
                        'Ít chát, dễ uống, phù hợp với nhiều phong cách thưởng trà.',
                        'Thích hợp pha trà nóng, trà sữa, trà trái cây hoặc cold brew.'],
         'suitable_for': ['Người yêu thích hồng trà nguyên lá chất lượng cao.',
                          'Pha trà nóng, trà đá, trà sữa hoặc trà trái cây.',
                          'Quán cà phê, quán trà, nhà hàng hoặc sử dụng tại gia đình.',
                          'Làm quà tặng cho người yêu trà.'],
         'commitments': ['Tuyển chọn từ vùng nguyên liệu chất lượng cao.',
                         'Đóng gói kín giúp giữ trọn hương thơm và chất lượng trà.',
                         'Không pha hương liệu, giữ hương vị đặc trưng của hồng trà Bảo Lộc.'],
         'brew': {'g': 8,
                  'ml': '180–200',
                  'temp': '95–100',
                  'time_s': '180–300',
                  'steeps': None,
                  'timer_s': 180,
                  'note': 'Có thể điều chỉnh lượng trà theo khẩu vị hoặc mục đích pha chế.',
                  'time_label': '3–5 phút'},
         'story': ['Hồng Trà Cao Cấp HSĐ 200G được tuyển chọn từ những búp trà chất lượng cao trên các '
                   'đồi trà Hằng Sơn Điền – Bảo Lộc, Lâm Đồng, nơi cây trà được chăm sóc bền bỉ qua '
                   'nhiều năm để tạo nên hương vị đậm đà và hậu vị ngọt tự nhiên.',
                   'Được chế biến theo quy trình kiểm soát nghiêm ngặt, hồng trà sở hữu màu nước đỏ hổ '
                   'phách, hương thơm dịu với những nốt hương mật ong, trái cây chín và caramel nhẹ. Vị '
                   'trà tròn đầy, ít chát, hậu ngọt sâu, thích hợp để thưởng thức nóng, pha lạnh hoặc '
                   'kết hợp với sữa và trái cây.'],
         'region': 'Bảo Lộc, Lâm Đồng, Việt Nam',
         'story_heading': 'Hương trà từ Bảo Lộc',
         'origin_label': 'Hồng Trà Bảo Lộc',
         'ingredients': '100% hồng trà nguyên lá.',
         '_distributor': True},
 'T08': {'desc': 'Hương gỗ, mật ngọt và trái cây chín nhẹ nhàng. Vị trà trầm ấm, đậm đà nhưng êm dịu, '
                 'chát rất nhẹ và hậu ngọt sâu.',
         'taste_note': 'Hương gỗ, mật ngọt và trái cây chín nhẹ nhàng. Vị trà trầm ấm, đậm đà nhưng êm '
                       'dịu, chát rất nhẹ và hậu ngọt sâu.',
         'profile': {'Hương': 'Trầm ấm, thanh lịch với nốt hương gỗ, mật ngọt và trái cây chín.',
                     'Vị': 'Đậm đà nhưng êm dịu, chát rất nhẹ, hậu vị ngọt sâu.',
                     'Màu nước': 'Vàng hổ phách đậm, trong sáng.',
                     'Hậu vị': 'Mượt mà, lưu hương lâu và mang cảm giác thư thái.'},
         'highlights': ['Tuyển chọn từ búp trà Ô Long chất lượng cao của Hằng Sơn Điền.',
                        'Vùng nguyên liệu Bảo Lộc được chăm sóc kỹ lưỡng trong nhiều năm.',
                        'Chế biến và ủ bảo quản giúp hương vị thêm trầm, sâu và hài hòa.',
                        'Hương thơm gỗ, mật ngọt và trái cây chín nhẹ nhàng.',
                        'Vị trà êm dịu, ít chát, hậu ngọt kéo dài.',
                        'Pha được nhiều lần nước, hương vị vẫn ổn định.'],
         'suitable_for': ['Người yêu thích trà có hương vị trầm ấm và chiều sâu.',
                          'Người thưởng trà lâu năm hoặc yêu thích trà Ô Long ủ.',
                          'Thưởng trà trong những buổi trò chuyện, thiền trà hoặc tiếp khách.',
                          'Làm quà tặng cao cấp cho người yêu trà.'],
         'commitments': ['Tuyển chọn từ vùng nguyên liệu chất lượng cao.',
                         'Đóng gói kín, giữ trọn hương thơm và chất lượng trà.',
                         'Không sử dụng hương liệu, lưu giữ hương vị tự nhiên của trà.'],
         'brew': {'g': 8,
                  'ml': 150,
                  'temp': '95–100',
                  'time_s': '30–45',
                  'steeps': '5–7',
                  'timer_s': 30,
                  'note': 'Hãm 30–45 giây cho nước đầu, tăng dần thời gian ở các lần pha sau.'},
         'story': ['Lão Trà Cao Cấp HSĐ 200G được tuyển chọn từ những búp trà Ô Long chất lượng cao '
                   'trên các đồi trà Hằng Sơn Điền – Bảo Lộc, Lâm Đồng, nơi cây trà được chăm sóc bền '
                   'bỉ qua nhiều năm. Sau quá trình chế biến và bảo quản theo phương pháp truyền thống, '
                   'trà phát triển hương thơm trầm ấm, vị ngọt sâu và hậu vị bền lâu – nét đặc trưng '
                   'của dòng Lão Trà được nhiều người yêu trà trân trọng.'],
         'region': 'Bảo Lộc, Lâm Đồng, Việt Nam',
         'story_heading': 'Hương trà từ Bảo Lộc',
         'origin_label': 'Trà Ô Long Bảo Lộc',
         'ingredients': '100% Lão Trà Ô Long.',
         '_distributor': True},
 'T01': {'desc': 'Hương mật ong tự nhiên, thoảng hương hoa và trái cây chín. Vị êm dịu, ít chát, hậu '
                 'ngọt sâu từ vùng trà Sa Pa.',
         'taste_note': 'Hương mật ong tự nhiên, thoảng hương hoa và trái cây chín. Vị êm dịu, ít chát, '
                       'hậu ngọt sâu từ vùng trà Sa Pa.',
         'profile': {'Hương': 'Mật ong tự nhiên, thoảng hương hoa và trái cây chín.',
                     'Vị': 'Êm dịu, ít chát.',
                     'Màu nước': 'Vàng hổ phách trong.',
                     'Hậu vị': 'Ngọt sâu.'},
         'highlights': ['Búp trà Ô Long tuyển chọn từ vùng núi Sa Pa.',
                        'Khí hậu mát mẻ, sương mù và biên độ nhiệt ngày đêm giúp búp trà tích lũy hương '
                        'thơm.',
                        'Hương mật ong tự nhiên, thoảng hương hoa và trái cây chín.',
                        'Nước trà vàng hổ phách trong, vị êm dịu, ít chát.',
                        'Pha được 4–6 nước vẫn giữ hương thơm.'],
         'suitable_for': ['Thưởng trà hằng ngày.', 'Tiếp khách.', 'Làm quà tặng cho người yêu trà.'],
         'commitments': ['Trà Ô Long chất lượng cao từ vùng nguyên liệu Sa Pa.',
                         'Hương vị tự nhiên, đóng gói cẩn thận.',
                         'Phù hợp thưởng trà, tiếp khách và làm quà tặng.'],
         'brew': {'g': '6–8',
                  'ml': 150,
                  'temp': '90–95',
                  'time_s': '40–60',
                  'steeps': '4–6',
                  'timer_s': 40,
                  'note': 'Hãm 40–60 giây cho nước đầu, tăng dần thời gian ở các nước sau.'},
         'story': ['Trà Đông Phương Mỹ Nhân HSĐ được làm từ những búp trà Ô Long tuyển chọn tại vùng '
                   'núi Sa Pa, nơi có khí hậu mát mẻ quanh năm, sương mù bao phủ và biên độ nhiệt lớn '
                   'giữa ngày và đêm. Điều kiện tự nhiên này giúp búp trà tích lũy hương thơm phong '
                   'phú, tạo nên dòng trà có hương vị thanh tao và hậu ngọt đặc trưng.',
                   'Trà nổi bật với hương mật ong, hương hoa và trái cây chín tự nhiên, nước trà vàng '
                   'hổ phách trong, vị êm dịu, ít chát và hậu vị ngọt sâu. Đây là dòng trà phù hợp để '
                   'thưởng thức hằng ngày hoặc làm quà tặng cho những người yêu trà.'],
         'region': 'Sa Pa, Lào Cai, Việt Nam',
         'story_heading': 'Hương trà từ Sa Pa',
         'origin_label': 'Trà Ô Long Sa Pa',
         'storage': 'Đậy kín sau khi mở bao bì. Bảo quản nơi khô ráo, thoáng mát, tránh ánh nắng trực '
                    'tiếp và mùi mạnh.',
         '_distributor': False},
 'T09': {'desc': 'Hương Ô Long thanh khiết, nguyên bản, không ướp hương. Vị đậm đà, chát nhẹ, hậu ngọt '
                 'sâu và lưu vị lâu.',
         'taste_note': 'Hương Ô Long thanh khiết, nguyên bản, không ướp hương. Vị đậm đà, chát nhẹ, hậu '
                       'ngọt sâu và lưu vị lâu.',
         'profile': {'Hương': 'Thanh khiết, tự nhiên; lớp hương thanh đa tầng.',
                     'Vị': 'Đậm đà, chát nhẹ.',
                     'Màu nước': 'Vàng xanh trong trẻo.',
                     'Hậu vị': 'Ngọt sâu, lưu vị lâu.'},
         'highlights': ['Ô Long Thuần từ giống trà Ô Long nguyên bản trồng tại vùng núi Sa Pa.',
                        'Búp trà phát triển chậm trong khí hậu mát mẻ và nhiều sương.',
                        'Không ướp hương, không tạo mùi, giữ bản sắc của lá trà Ô Long.',
                        'Nước trà vàng xanh trong, vị đậm đà, chát nhẹ và hậu ngọt sâu.',
                        'Pha được 4–6 nước vẫn giữ hương thơm.'],
         'suitable_for': ['Người yêu thích hương vị nguyên bản của trà Ô Long.',
                          'Thưởng trà hằng ngày hoặc tiếp khách.',
                          'Làm quà tặng cho người yêu trà.'],
         'commitments': ['Trà Ô Long nguyên bản, không ướp hương.',
                         'Hương vị tự nhiên, hậu ngọt sâu.',
                         'Phù hợp thưởng trà hằng ngày, tiếp khách và làm quà tặng.'],
         'brew': {'g': '6–8',
                  'ml': 150,
                  'temp': '90–95',
                  'time_s': '40–60',
                  'steeps': '4–6',
                  'timer_s': 40,
                  'note': 'Hãm 40–60 giây cho nước đầu, tăng dần thời gian ở các nước tiếp theo.'},
         'story': ['Trà Ô Long Tuyết Thượng Hạng HSĐ, hay còn gọi là Ô Long Thuần, được chế biến từ '
                   'giống trà Ô Long nguyên bản trồng tại vùng núi Sa Pa. Với khí hậu mát mẻ quanh năm, '
                   'nhiều sương và độ cao lý tưởng, những búp trà phát triển chậm, tích lũy hương thơm '
                   'tự nhiên và tạo nên hương vị mộc mạc, tinh khiết.',
                   'Không ướp hương, không tạo mùi, trà giữ trọn bản sắc của lá trà Ô Long. Nước trà '
                   'vàng xanh trong trẻo, vị đậm đà, chát nhẹ, hậu ngọt sâu cùng lớp hương thanh đa '
                   'tầng. Đây là dòng trà phù hợp cho những người yêu thích hương vị nguyên bản của trà '
                   'Ô Long.'],
         'region': 'Sa Pa, Lào Cai, Việt Nam',
         'story_heading': 'Hương trà từ Sa Pa',
         'origin_label': 'Trà Ô Long Sa Pa',
         'storage': 'Đậy kín sau khi mở bao bì. Bảo quản nơi khô ráo, thoáng mát, tránh ánh nắng trực '
                    'tiếp.',
         '_distributor': False},
 'T10': {'desc': 'Ô Long Kim Tuyên Bảo Lộc hòa quyện cùng hoa mộc quế tự nhiên. Hương hoa thanh tao, vị '
                 'ngọt dịu, chát nhẹ và hậu vị lưu hương dài lâu.',
         'taste_note': 'Ô Long Kim Tuyên Bảo Lộc hòa quyện cùng hoa mộc quế tự nhiên. Hương hoa thanh '
                       'tao, vị ngọt dịu, chát nhẹ và hậu vị lưu hương dài lâu.',
         'profile': {'Hương': 'Hoa mộc quế tinh tế, thanh sạch, thoang thoảng hương quế hoa tự nhiên.',
                     'Vị': 'Ngọt thanh, chát nhẹ, êm dịu và dễ uống.',
                     'Màu nước': 'Vàng sáng, trong trẻo.',
                     'Hậu vị': 'Hương hoa lưu lại lâu, mềm mại và tươi mát.'},
         'highlights': ['Trà Ô Long Kim Tuyên tuyển chọn từ vùng nguyên liệu Bảo Lộc.',
                        'Ướp cùng hoa mộc quế tự nhiên, hương thơm thanh tao, không nồng gắt.',
                        'Kết hợp hài hòa giữa vị trà và hương hoa, tạo cảm giác dễ uống.',
                        'Nước trà vàng sáng, trong, hương thơm bền qua nhiều lần pha.',
                        'Phù hợp thưởng trà hằng ngày hoặc làm quà tặng cao cấp.'],
         'suitable_for': ['Người yêu thích trà hương hoa tự nhiên.',
                          'Thưởng trà hằng ngày, trà chiều hoặc tiếp khách.',
                          'Quà tặng tinh tế dành cho người yêu trà.',
                          'Người thích phong cách thanh lịch, nhẹ nhàng.'],
         'commitments': [],
         'brew': {'g': 8,
                  'ml': 150,
                  'temp': '90–95',
                  'time_s': '30–45',
                  'steeps': '4–5',
                  'timer_s': 30,
                  'note': 'Hãm 30–45 giây cho nước đầu, tăng dần thời gian ở các lần pha sau.'},
         'story': ['Trà Ô Long Quế Hoa HSĐ là sự hòa quyện giữa trà Ô Long Kim Tuyên cao cấp Bảo Lộc và '
                   'hoa mộc (quế hoa) tự nhiên, mang đến hương thơm thanh khiết, vị trà ngọt dịu và hậu '
                   'vị lưu hương dài lâu. Đây là dòng trà thích hợp cho những ai yêu thích hương hoa tự '
                   'nhiên và phong cách thưởng trà nhẹ nhàng, tinh tế.'],
         'region': 'Bảo Lộc, Lâm Đồng, Việt Nam',
         'story_heading': 'Hương trà từ Bảo Lộc',
         'origin_label': 'Trà Ô Long Bảo Lộc',
         'ingredients': 'Trà Ô Long Kim Tuyên Bảo Lộc và hoa mộc quế tự nhiên.',
         '_distributor': False},
 'T11': {'desc': 'Hương hoa tự nhiên thanh thoát, nước trà vàng xanh trong. Vị thanh, ít chát, hậu ngọt '
                 'bền và dễ uống từ giống Ô Long Tứ Quý Bảo Lộc.',
         'taste_note': 'Hương hoa tự nhiên thanh thoát, nước trà vàng xanh trong. Vị thanh, ít chát, '
                       'hậu ngọt bền và dễ uống từ giống Ô Long Tứ Quý Bảo Lộc.',
         'profile': {'Hương': 'Hương hoa tự nhiên đặc trưng, thanh thoát.',
                     'Vị': 'Thanh, êm dịu, ít chát.',
                     'Màu nước': 'Vàng xanh trong trẻo.',
                     'Hậu vị': 'Ngọt bền, kéo dài và dễ uống.'},
         'highlights': ['Giống trà Ô Long Tứ Quý trồng tại Bảo Lộc, Lâm Đồng.',
                        'Chế biến truyền thống kết hợp công nghệ hiện đại bởi Hằng Sơn Điền.',
                        'Hương hoa tự nhiên đặc trưng, nước trà vàng xanh trong trẻo.',
                        'Vị thanh, ít chát, hậu ngọt bền.',
                        'Pha được 5–7 nước.'],
         'suitable_for': ['Thưởng trà hằng ngày.', 'Tiếp khách.', 'Làm quà tặng.'],
         'commitments': ['Trà Ô Long được tuyển chọn kỹ lưỡng.',
                         'Hương thơm tự nhiên, không ướp hương.',
                         'Phù hợp thưởng trà hằng ngày, tiếp khách và làm quà tặng.'],
         'brew': {'g': '6–8',
                  'ml': 150,
                  'temp': '90–95',
                  'time_s': '40–60',
                  'steeps': '5–7',
                  'timer_s': 40,
                  'note': 'Hãm 40–60 giây cho nước đầu, tăng dần thời gian ở các nước tiếp theo.'},
         'story': ['Trà Ô Long Tứ Quý HSĐ được sản xuất từ giống trà Ô Long Tứ Quý trồng tại Bảo Lộc – '
                   'vùng trà nổi tiếng với khí hậu mát mẻ quanh năm và điều kiện tự nhiên lý tưởng để '
                   'tạo nên những búp trà chất lượng cao.',
                   'Trà được chế biến theo quy trình truyền thống kết hợp công nghệ hiện đại bởi Hằng '
                   'Sơn Điền, giúp lưu giữ hương thơm tự nhiên đặc trưng của giống Tứ Quý. Nước trà '
                   'vàng xanh trong, hương hoa thanh thoát, vị trà êm dịu, hậu ngọt kéo dài và có thể '
                   'pha nhiều lần vẫn giữ được hương vị.'],
         'region': 'Bảo Lộc, Lâm Đồng, Việt Nam',
         'story_heading': 'Hương trà từ Bảo Lộc',
         'origin_label': 'Trà Ô Long Bảo Lộc',
         'storage': 'Đậy kín sau khi mở bao bì. Bảo quản nơi khô ráo, thoáng mát, tránh ánh nắng trực '
                    'tiếp và mùi mạnh.',
         '_distributor': False,
         '_variety': 'Ô Long Tứ Quý'},
 'T14': {'desc': 'Hương hoa tự nhiên thanh thoát, nước trà vàng xanh trong. Vị thanh, ít chát, hậu ngọt '
                 'bền và dễ uống từ giống Ô Long Tứ Quý Bảo Lộc.',
         'taste_note': 'Hương hoa tự nhiên thanh thoát, nước trà vàng xanh trong. Vị thanh, ít chát, '
                       'hậu ngọt bền và dễ uống từ giống Ô Long Tứ Quý Bảo Lộc.',
         'profile': {'Hương': 'Hương hoa tự nhiên đặc trưng, thanh thoát.',
                     'Vị': 'Thanh, êm dịu, ít chát.',
                     'Màu nước': 'Vàng xanh trong trẻo.',
                     'Hậu vị': 'Ngọt bền, kéo dài và dễ uống.'},
         'highlights': ['Giống trà Ô Long Tứ Quý trồng tại Bảo Lộc, Lâm Đồng.',
                        'Chế biến truyền thống kết hợp công nghệ hiện đại bởi Hằng Sơn Điền.',
                        'Hương hoa tự nhiên đặc trưng, nước trà vàng xanh trong trẻo.',
                        'Vị thanh, ít chát, hậu ngọt bền.',
                        'Pha được 5–7 nước.'],
         'suitable_for': ['Thưởng trà hằng ngày.', 'Tiếp khách.', 'Làm quà tặng.'],
         'commitments': ['Trà Ô Long cao cấp được tuyển chọn kỹ lưỡng.',
                         'Hương thơm tự nhiên, không ướp hương.',
                         'Phù hợp thưởng trà hằng ngày, tiếp khách và làm quà tặng.'],
         'brew': {'g': '6–8',
                  'ml': 150,
                  'temp': '90–95',
                  'time_s': '40–60',
                  'steeps': '5–7',
                  'timer_s': 40,
                  'note': 'Hãm 40–60 giây cho nước đầu, tăng dần thời gian ở các nước tiếp theo.'},
         'story': ['Trà Ô Long Tứ Quý Cao Cấp HSĐ được sản xuất từ giống trà Ô Long Tứ Quý trồng tại '
                   'Bảo Lộc – vùng trà nổi tiếng với khí hậu mát mẻ quanh năm và điều kiện tự nhiên lý '
                   'tưởng để tạo nên những búp trà chất lượng cao.',
                   'Trà được chế biến theo quy trình truyền thống kết hợp công nghệ hiện đại bởi Hằng '
                   'Sơn Điền, giúp lưu giữ hương thơm tự nhiên đặc trưng của giống Tứ Quý. Nước trà '
                   'vàng xanh trong, hương hoa thanh thoát, vị trà êm dịu, hậu ngọt kéo dài và có thể '
                   'pha nhiều lần vẫn giữ được hương vị.'],
         'region': 'Bảo Lộc, Lâm Đồng, Việt Nam',
         'story_heading': 'Hương trà từ Bảo Lộc',
         'origin_label': 'Trà Ô Long Bảo Lộc',
         'storage': 'Đậy kín sau khi mở bao bì. Bảo quản nơi khô ráo, thoáng mát, tránh ánh nắng trực '
                    'tiếp và mùi mạnh.',
         '_distributor': False,
         '_variety': 'Ô Long Tứ Quý'},
 'T12': {'desc': 'Hương sữa tự nhiên của giống Kim Tuyên (Jin Xuan), vị thanh ngọt, chát nhẹ và hậu '
                 'ngọt sâu. Nước trà vàng xanh trong sáng, sánh nhẹ.',
         'taste_note': 'Hương sữa tự nhiên của giống Kim Tuyên (Jin Xuan), vị thanh ngọt, chát nhẹ và '
                       'hậu ngọt sâu. Nước trà vàng xanh trong sáng, sánh nhẹ.',
         'profile': {'Hương': 'Hương sữa tự nhiên hòa quyện cùng hương trà thanh khiết.',
                     'Vị': 'Đậm đà vừa phải, ngọt hậu, chát nhẹ và cân bằng.',
                     'Màu nước': 'Vàng xanh trong sáng, sánh nhẹ.',
                     'Hậu vị': 'Ngọt sâu, lưu hương lâu và dễ chịu.'},
         'highlights': ['Tuyển chọn từ búp trà Ô Long Kim Tuyên.',
                        'Vùng nguyên liệu Hằng Sơn Điền – Bảo Lộc, Lâm Đồng.',
                        'Đồi trà được chăm sóc kỹ lưỡng và canh tác bền vững trong nhiều năm.',
                        'Hương sữa tự nhiên đặc trưng của giống Kim Tuyên, không sử dụng hương liệu.',
                        'Vị ngọt thanh, chát nhẹ, hậu vị sâu và bền.',
                        'Pha được 4–6 nước, hương vị vẫn hài hòa.'],
         'suitable_for': ['Người yêu thích trà Ô Long truyền thống.',
                          'Thưởng trà hằng ngày hoặc tiếp khách.',
                          'Làm quà tặng cho người yêu trà.',
                          'Người mới bắt đầu thưởng thức trà Ô Long.'],
         'commitments': [],
         'brew': {'g': 8,
                  'ml': 150,
                  'temp': '90–95',
                  'time_s': '30–45',
                  'steeps': '4–6',
                  'timer_s': 30,
                  'note': 'Hãm 30–45 giây cho nước đầu, tăng dần thời gian ở các lần pha sau.'},
         'story': ['Trà Ô Long Kim Tuyên HSĐ 250G được tuyển chọn từ những búp trà Kim Tuyên chất lượng '
                   'cao trên các đồi trà của Hằng Sơn Điền – Bảo Lộc, Lâm Đồng, nơi cây trà được chăm '
                   'sóc bền bỉ trong nhiều năm để tạo nên hương vị đặc trưng của vùng cao nguyên.',
                   'Giống trà Kim Tuyên (Jin Xuan) nổi tiếng với hương sữa tự nhiên, vị trà thanh ngọt, '
                   'chát nhẹ và hậu vị kéo dài. Khi pha, nước trà có màu vàng xanh trong trẻo, hương '
                   'thơm thanh khiết và có thể pha nhiều lần vẫn giữ được hương vị.'],
         'region': 'Bảo Lộc, Lâm Đồng, Việt Nam',
         'story_heading': 'Hương trà từ Bảo Lộc',
         'origin_label': 'Trà Ô Long Bảo Lộc',
         'ingredients': '100% Trà Ô Long Kim Tuyên.',
         '_distributor': True},
 'T15': {'desc': 'Hương sữa tự nhiên của giống Kim Tuyên (Jin Xuan), vị thanh ngọt, chát nhẹ và hậu '
                 'ngọt sâu. Nước trà vàng xanh trong sáng, sánh nhẹ.',
         'taste_note': 'Hương sữa tự nhiên của giống Kim Tuyên (Jin Xuan), vị thanh ngọt, chát nhẹ và '
                       'hậu ngọt sâu. Nước trà vàng xanh trong sáng, sánh nhẹ.',
         'profile': {'Hương': 'Hương sữa tự nhiên hòa quyện cùng hương trà thanh khiết.',
                     'Vị': 'Đậm đà vừa phải, ngọt hậu, chát nhẹ và cân bằng.',
                     'Màu nước': 'Vàng xanh trong sáng, sánh nhẹ.',
                     'Hậu vị': 'Ngọt sâu, lưu hương lâu và dễ chịu.'},
         'highlights': ['Tuyển chọn từ búp trà Ô Long Kim Tuyên cao cấp.',
                        'Vùng nguyên liệu Hằng Sơn Điền – Bảo Lộc, Lâm Đồng.',
                        'Đồi trà được chăm sóc kỹ lưỡng và canh tác bền vững trong nhiều năm.',
                        'Hương sữa tự nhiên đặc trưng của giống Kim Tuyên, không sử dụng hương liệu.',
                        'Vị ngọt thanh, chát nhẹ, hậu vị sâu và bền.',
                        'Pha được 4–6 nước, hương vị vẫn hài hòa.'],
         'suitable_for': ['Người yêu thích trà Ô Long truyền thống.',
                          'Thưởng trà hằng ngày hoặc tiếp khách.',
                          'Làm quà tặng cho người yêu trà.',
                          'Người mới bắt đầu thưởng thức trà Ô Long cao cấp.'],
         'commitments': [],
         'brew': {'g': 8,
                  'ml': 150,
                  'temp': '90–95',
                  'time_s': '30–45',
                  'steeps': '4–6',
                  'timer_s': 30,
                  'note': 'Hãm 30–45 giây cho nước đầu, tăng dần thời gian ở các lần pha sau.'},
         'story': ['Trà Ô Long Kim Tuyên Cao Cấp HSĐ 250G được tuyển chọn từ những búp trà Kim Tuyên '
                   'chất lượng cao trên các đồi trà của Hằng Sơn Điền – Bảo Lộc, Lâm Đồng, nơi cây trà '
                   'được chăm sóc bền bỉ trong nhiều năm để tạo nên hương vị đặc trưng của vùng cao '
                   'nguyên.',
                   'Giống trà Kim Tuyên (Jin Xuan) nổi tiếng với hương sữa tự nhiên, vị trà thanh ngọt, '
                   'chát nhẹ và hậu vị kéo dài. Khi pha, nước trà có màu vàng xanh trong trẻo, hương '
                   'thơm thanh khiết và có thể pha nhiều lần vẫn giữ được hương vị.'],
         'region': 'Bảo Lộc, Lâm Đồng, Việt Nam',
         'story_heading': 'Hương trà từ Bảo Lộc',
         'origin_label': 'Trà Ô Long Bảo Lộc',
         'ingredients': '100% Trà Ô Long Kim Tuyên.',
         '_distributor': True},
 'T13': {'desc': 'Hương hoa và hương trà thanh khiết, vị đậm vừa phải, chát nhẹ và ngọt hậu. Nước trà '
                 'vàng óng trong sáng, giữ hương qua nhiều lần pha.',
         'taste_note': 'Hương hoa và hương trà thanh khiết, vị đậm vừa phải, chát nhẹ và ngọt hậu. Nước '
                       'trà vàng óng trong sáng, giữ hương qua nhiều lần pha.',
         'profile': {'Hương': 'Thanh khiết với hương hoa và hương trà tự nhiên.',
                     'Vị': 'Đậm đà vừa phải, chát nhẹ, cân bằng và ngọt hậu.',
                     'Màu nước': 'Vàng óng trong sáng.',
                     'Hậu vị': 'Ngọt sâu, lưu hương lâu, mang cảm giác thư thái.'},
         'highlights': ['Tuyển chọn từ những búp trà Ô Long chất lượng cao.',
                        'Vùng nguyên liệu Hằng Sơn Điền – Bảo Lộc, Lâm Đồng.',
                        'Đồi trà được chăm sóc kỹ lưỡng và canh tác bền vững trong nhiều năm.',
                        'Hương thơm thanh tao, vị trà đậm vừa phải, ngọt hậu tự nhiên.',
                        'Nước trà vàng óng trong trẻo, hương thơm bền qua nhiều lần pha.',
                        'Pha được 4–6 nước, hương vị vẫn cân bằng và hài hòa.'],
         'suitable_for': ['Người yêu thích trà Ô Long nguyên vị.',
                          'Thưởng trà hằng ngày hoặc tiếp khách.',
                          'Người mới bắt đầu và người thưởng trà lâu năm.',
                          'Làm quà tặng cao cấp cho người yêu trà.'],
         'commitments': ['Tuyển chọn từ vùng nguyên liệu chất lượng cao.',
                         'Đóng gói kín giúp giữ trọn hương thơm và chất lượng trà.',
                         'Không sử dụng hương liệu, giữ nguyên hương vị tự nhiên của trà Ô Long.'],
         'brew': {'g': 8,
                  'ml': 150,
                  'temp': '90–95',
                  'time_s': '30–45',
                  'steeps': '4–6',
                  'timer_s': 30,
                  'note': 'Hãm 30–45 giây cho nước đầu, tăng dần thời gian ở các lần pha sau.'},
         'story': ['Trà Ô Long Cao Sơn HSĐ 250G được tuyển chọn từ những búp trà Ô Long chất lượng cao '
                   'trên các đồi trà Hằng Sơn Điền – Bảo Lộc, Lâm Đồng, nơi cây trà được chăm sóc bền '
                   'bỉ qua nhiều năm để tạo nên hương vị thanh khiết và đậm đà đặc trưng.',
                   'Nhờ điều kiện khí hậu mát mẻ quanh năm cùng quy trình chế biến tỉ mỉ, trà mang '
                   'hương thơm tự nhiên, vị thanh ngọt, hậu vị sâu và bền. Mỗi chén trà là sự kết tinh '
                   'của vùng trà cao nguyên Bảo Lộc và nghệ thuật chế biến trà của Hằng Sơn Điền.'],
         'region': 'Bảo Lộc, Lâm Đồng, Việt Nam',
         'story_heading': 'Hương trà từ Bảo Lộc',
         'origin_label': 'Trà Ô Long Bảo Lộc',
         'ingredients': '100% Trà Ô Long Cao Sơn.',
         '_distributor': True}}


def apply_tea_details(products):
    _apply_milk_tea_details(products)
    for product in products:
        if product['id'] not in EXTRA_DETAILS:
            continue
        detail = EXTRA_DETAILS[product['id']]
        product.update({key: value for key, value in detail.items() if not key.startswith('_')})
        weight = product['variants'][0]['label'].replace('Gói ', '')
        product['page_title'] = product['name'] + ' ' + weight + ' – ' + product['origin_label']
        info = [('Tên sản phẩm', product['name']), ('Khối lượng tịnh', weight)]
        if 'ingredients' in detail:
            info.append(('Thành phần', detail['ingredients']))
        if detail.get('_variety'):
            info.append(('Giống trà', detail['_variety']))
        info.extend([('Xuất xứ', detail['region']), ('Sản xuất', 'Hằng Sơn Điền')])
        if detail.get('_distributor'):
            info.append(('Phân phối độc quyền', 'Uniharvest Việt Nam'))
        product['product_info'] = info
