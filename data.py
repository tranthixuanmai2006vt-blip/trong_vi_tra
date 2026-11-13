# -*- coding: utf-8 -*-
"""
DỮ LIỆU WEBSITE TRỒNG VỊ TRÀ  (Hằng Sơn Điền × Trà)
=====================================================
⚠️  Toàn bộ giá, tồn kho, SKU, thông tin liên hệ... trong file này là DỮ LIỆU MẪU
    để chạy demo. Khi doanh nghiệp xác nhận số liệu thật, chỉ cần sửa tại đây.
    Đặt DEMO_MODE = False để ẩn dải thông báo "Bản demo" trên website.
"""

DEMO_MODE = True

# -----------------------------------------------------------------
# THÔNG TIN CHUNG  (để trống "" → website tự hiện "Đang cập nhật")
# -----------------------------------------------------------------
SITE = {
    "name": "Trồng vị Trà",
    "partner": "Hằng Sơn Điền",
    "eyebrow": "TRỒNG VỊ TRÀ × HẰNG SƠN ĐIỀN",
    "company": "Công ty TNHH Sản xuất Thương mại Trà Hằng Sơn Điền",
    "tax_code": "",
    "address": "",
    "hotline": "",
    "email": "",
    "zalo": "",
    "facebook": "",
    "support_hours": "",
    "maps_url": "",
}

FREESHIP_THRESHOLD = 500_000          # đơn từ mức này được miễn phí giao tiêu chuẩn
COD_LIMIT = 2_000_000                 # COD chỉ áp dụng cho đơn ≤ mức này
COUPONS = {                           # mã giảm giá mẫu (không quảng bá trên web)
    "TRONGVITRA10": {"type": "percent", "value": 10, "min": 300_000, "label": "Giảm 10% đơn từ 300.000đ"},
    "CHAODUYEN": {"type": "fixed", "value": 30_000, "min": 200_000, "label": "Giảm 30.000đ đơn từ 200.000đ"},
}
BANK = {"bank": "[Ngân hàng – chờ xác nhận]", "account": "[Số tài khoản – chờ xác nhận]",
        "holder": "[Tên người thụ hưởng – chờ xác nhận]", "hours_valid": 24}

# -----------------------------------------------------------------
# TỈNH / THÀNH & GIAO HÀNG
# -----------------------------------------------------------------
PROVINCES = ["TP. Hồ Chí Minh", "Hà Nội", "Đà Nẵng", "Bình Dương", "Đồng Nai", "Cần Thơ",
             "Lâm Đồng", "Khánh Hòa", "Hải Phòng", "Tỉnh/thành khác"]
CAKE_ZONE = ["TP. Hồ Chí Minh"]        # bánh tươi chỉ giao trong khu vực này (mẫu)

SHIPPING_METHODS = {
    "standard": {"label": "Giao tiêu chuẩn", "desc": "2–4 ngày làm việc sau khi chuẩn bị xong",
                 "fee": {"TP. Hồ Chí Minh": 25_000, "_default": 35_000}, "days": (2, 4), "zones": None},
    "express": {"label": "Giao nhanh trong ngày", "desc": "Nhận trong ngày khi hàng đã sẵn sàng",
                "fee": {"TP. Hồ Chí Minh": 45_000}, "days": (0, 1), "zones": ["TP. Hồ Chí Minh"]},
}
PAYMENT_METHODS = {
    "cod": {"label": "Thanh toán khi nhận hàng (COD)",
            "desc": "Trả tiền mặt cho nhân viên giao hàng. Áp dụng cho đơn đến 2.000.000đ.",
            "button": "Đặt hàng – trả khi nhận"},
    "bank": {"label": "Chuyển khoản ngân hàng",
             "desc": "Sau khi đặt, bạn nhận thông tin chuyển khoản kèm nội dung là mã đơn.",
             "button": "Đặt hàng và thanh toán"},
}

# -----------------------------------------------------------------
# SẢN PHẨM
#   type: tra | banh | gift
#   dna:  [ngọt, chua, đắng, đậm, hương(0=hoa → 100=trái cây)]  – dùng cho Tea DNA
#   avoid: thành phần để lọc theo câu 12 Tea DNA (milk, caffeine, honey, sour)
#   slots: số "ô" chiếm trong hộp quà tự tạo
# -----------------------------------------------------------------
PRODUCTS = [
    # ============================ TRÀ ============================
    {
        "id": "T01", "slug": "tra-dong-phuong-my-nhan", "type": "tra",
        "name": "Trà Đông Phương Mỹ Nhân", "brand": "Hằng Sơn Điền", "line": "Ô long",
        "group": "o-long", "region": "Vùng ô long cao nguyên", "art": "pouch", "color": "#B4762E",
        "taste_note": "Hương mật ong, trái chín, hậu ngọt sâu",
        "desc": "Dòng ô long lên men cao với hương mật ong và trái chín đặc trưng. Nước trà màu hổ phách, vị tròn, hậu ngọt kéo dài.",
        "variants": [{"sku": "HSD-DPMN-100", "label": "Gói 100g", "price": 280_000, "stock": 24, "slots": 2}],
        "profile": {"Loại trà": "Ô long lên men cao", "Sắc nước": "Hổ phách sáng", "Hương đầu": "Mật ong, trái chín",
                    "Vị chính": "Ngọt dịu, tròn vị", "Hậu vị": "Ngọt sâu", "Độ chát": "Thấp", "Độ đậm": "Vừa"},
        "brew": {"g": 5, "ml": 150, "temp": 90, "time_s": 45, "steeps": 5},
        "ingredients": "100% lá trà ô long.", "storage": "Bảo quản nơi khô ráo, kín, tránh ánh nắng và mùi mạnh.",
        "hsd": "24 tháng kể từ ngày sản xuất (xem trên bao bì).", "allergens": [],
        "prep_days": 0, "occasions": ["bieu-tang", "moi-ngay"], "flavor": ["hoa-qua", "ngot-hau"],
        "pair": ["B02", "B03"], "dna": [40, 20, 35, 55, 70], "avoid": ["caffeine"],
        "rank": 1, "new": False,
    },
    {
        "id": "T02", "slug": "tra-o-long-huong-thanh", "type": "tra",
        "name": "Trà Ô Long Hương Thanh", "brand": "Hằng Sơn Điền", "line": "Ô long",
        "group": "o-long", "region": "Vùng ô long cao nguyên", "art": "pouch", "color": "#7C8F3A",
        "taste_note": "Hương hoa tươi, vị thanh, hậu ngọt nhẹ",
        "desc": "Ô long lên men nhẹ, viên trà xoăn chặt, nước xanh vàng. Hương hoa tươi mát, vị thanh dễ uống cho người mới.",
        "variants": [{"sku": "HSD-OLHT-100", "label": "Gói 100g", "price": 180_000, "stock": 40, "slots": 2},
                     {"sku": "HSD-OLHT-250", "label": "Hộp 250g", "price": 420_000, "stock": 12, "slots": 3}],
        "profile": {"Loại trà": "Ô long lên men nhẹ", "Sắc nước": "Xanh vàng", "Hương đầu": "Hoa tươi",
                    "Vị chính": "Thanh, mát", "Hậu vị": "Ngọt nhẹ", "Độ chát": "Thấp", "Độ đậm": "Nhẹ – vừa"},
        "brew": {"g": 5, "ml": 150, "temp": 95, "time_s": 50, "steeps": 6},
        "ingredients": "100% lá trà ô long.", "storage": "Bảo quản nơi khô ráo, kín, tránh ánh nắng và mùi mạnh.",
        "hsd": "24 tháng kể từ ngày sản xuất (xem trên bao bì).", "allergens": [],
        "prep_days": 0, "occasions": ["moi-ngay", "bieu-tang"], "flavor": ["hoa", "thanh"],
        "pair": ["B03", "B01"], "dna": [25, 20, 30, 45, 15], "avoid": ["caffeine"],
        "rank": 2, "new": False,
    },
    {
        "id": "T03", "slug": "tra-o-long-rang", "type": "tra",
        "name": "Trà Ô Long Rang Củi", "brand": "Hằng Sơn Điền", "line": "Ô long",
        "group": "o-long", "region": "Vùng ô long cao nguyên", "art": "pouch", "color": "#6B3F22",
        "taste_note": "Hương rang ấm, vị đậm, hậu caramel",
        "desc": "Ô long được rang lửa nhỏ nhiều lần cho hương rang ấm, vị đậm và hậu caramel. Hợp người thích trà rõ vị, ít ngọt.",
        "variants": [{"sku": "HSD-OLR-100", "label": "Gói 100g", "price": 220_000, "stock": 18, "slots": 2}],
        "profile": {"Loại trà": "Ô long rang", "Sắc nước": "Nâu cam", "Hương đầu": "Rang, gỗ ấm",
                    "Vị chính": "Đậm, êm", "Hậu vị": "Caramel", "Độ chát": "Vừa", "Độ đậm": "Đậm"},
        "brew": {"g": 6, "ml": 150, "temp": 98, "time_s": 40, "steeps": 5},
        "ingredients": "100% lá trà ô long.", "storage": "Bảo quản nơi khô ráo, kín, tránh ánh nắng và mùi mạnh.",
        "hsd": "24 tháng kể từ ngày sản xuất (xem trên bao bì).", "allergens": [],
        "prep_days": 0, "occasions": ["moi-ngay", "doanh-nghiep"], "flavor": ["rang", "dam"],
        "pair": ["B02", "B04"], "dna": [15, 15, 65, 80, 35], "avoid": ["caffeine"],
        "rank": 4, "new": True,
    },
    {
        "id": "T04", "slug": "bot-matcha", "type": "tra",
        "name": "Bột Matcha Nguyên Chất", "brand": "Hằng Sơn Điền", "line": "Matcha",
        "group": "matcha", "region": "Vùng trà xanh che bóng", "art": "tin", "color": "#5E7D2A",
        "taste_note": "Xanh tươi, umami, đắng nhẹ dễ chịu",
        "desc": "Bột trà xanh xay mịn, màu xanh tươi, vị umami và đắng nhẹ. Dùng đánh trà truyền thống hoặc pha latte, làm bánh.",
        "variants": [{"sku": "HSD-MAT-50", "label": "Hũ 50g", "price": 190_000, "stock": 30, "slots": 1},
                     {"sku": "HSD-MAT-100", "label": "Hũ 100g", "price": 350_000, "stock": 0, "slots": 2}],
        "profile": {"Loại trà": "Trà xanh dạng bột", "Sắc nước": "Xanh ngọc", "Hương đầu": "Cỏ non, rong biển",
                    "Vị chính": "Umami", "Hậu vị": "Đắng nhẹ, ngọt lại", "Độ chát": "Vừa", "Độ đậm": "Đậm"},
        "brew": {"g": 2, "ml": 70, "temp": 75, "time_s": 20, "steeps": 1},
        "ingredients": "100% bột trà xanh.", "storage": "Đậy kín sau khi mở, bảo quản ngăn mát, dùng trong 1 tháng.",
        "hsd": "12 tháng kể từ ngày sản xuất (xem trên bao bì).", "allergens": [],
        "prep_days": 0, "occasions": ["moi-ngay", "bieu-tang"], "flavor": ["thao-moc", "dam"],
        "pair": ["B01", "B04"], "dna": [30, 15, 55, 70, 20], "avoid": ["caffeine"],
        "rank": 3, "new": False,
    },
    {
        "id": "T05", "slug": "tra-xanh-lai", "type": "tra",
        "name": "Trà Xanh Ướp Lài", "brand": "Hằng Sơn Điền", "line": "Trà xanh",
        "group": "tra-xanh", "region": "Vùng trà xanh trung du", "art": "pouch", "color": "#C9B458",
        "taste_note": "Hương nhài tươi, vị thanh, chát nhẹ",
        "desc": "Trà xanh ướp hoa nhài tự nhiên nhiều lớp. Hương lài thơm sáng, vị thanh, phù hợp pha nóng hoặc pha lạnh.",
        "variants": [{"sku": "HSD-XL-100", "label": "Gói 100g", "price": 120_000, "stock": 50, "slots": 2}],
        "profile": {"Loại trà": "Trà xanh ướp hoa", "Sắc nước": "Vàng chanh", "Hương đầu": "Hoa nhài",
                    "Vị chính": "Thanh", "Hậu vị": "Ngọt nhẹ", "Độ chát": "Nhẹ – vừa", "Độ đậm": "Nhẹ"},
        "brew": {"g": 3, "ml": 200, "temp": 80, "time_s": 90, "steeps": 3},
        "ingredients": "Lá trà xanh, hoa nhài.", "storage": "Bảo quản nơi khô ráo, kín, tránh ánh nắng và mùi mạnh.",
        "hsd": "18 tháng kể từ ngày sản xuất (xem trên bao bì).", "allergens": [],
        "prep_days": 0, "occasions": ["moi-ngay"], "flavor": ["hoa", "thanh"],
        "pair": ["B03", "B01"], "dna": [35, 30, 25, 30, 5], "avoid": ["caffeine"],
        "rank": 5, "new": False,
    },
    {
        "id": "T06", "slug": "hong-tra", "type": "tra",
        "name": "Hồng Trà Cổ Điển", "brand": "Hằng Sơn Điền", "line": "Hồng trà",
        "group": "hong-tra", "region": "Vùng ô long cao nguyên", "art": "pouch", "color": "#8E3B22",
        "taste_note": "Mật ong, mạch nha, vị đậm hợp pha sữa",
        "desc": "Hồng trà lên men toàn phần, nước đỏ nâu, hương mật ong và mạch nha. Uống nguyên bản hoặc pha trà sữa đều hợp.",
        "variants": [{"sku": "HSD-HT-100", "label": "Gói 100g", "price": 150_000, "stock": 35, "slots": 2}],
        "profile": {"Loại trà": "Hồng trà (trà đen)", "Sắc nước": "Đỏ nâu", "Hương đầu": "Mật ong, mạch nha",
                    "Vị chính": "Đậm, êm", "Hậu vị": "Ngọt ấm", "Độ chát": "Vừa", "Độ đậm": "Đậm"},
        "brew": {"g": 4, "ml": 200, "temp": 95, "time_s": 180, "steeps": 2},
        "ingredients": "100% lá trà.", "storage": "Bảo quản nơi khô ráo, kín, tránh ánh nắng và mùi mạnh.",
        "hsd": "24 tháng kể từ ngày sản xuất (xem trên bao bì).", "allergens": [],
        "prep_days": 0, "occasions": ["moi-ngay", "doanh-nghiep"], "flavor": ["dam", "ngot-hau"],
        "pair": ["B02", "B05"], "dna": [25, 15, 60, 80, 40], "avoid": ["caffeine"],
        "rank": 6, "new": True,
    },
    # ============================ BÁNH ============================
    {
        "id": "B01", "slug": "banh-quy-matcha", "type": "banh",
        "name": "Bánh Quy Matcha Bơ", "brand": "Trồng vị Trà", "line": "Bánh quy",
        "tea_used": "T04", "art": "cookie", "color": "#7C9A3F",
        "taste_note": "Giòn tan, thơm bơ, đắng nhẹ matcha",
        "desc": "Bánh quy bơ giòn tan dùng bột matcha Hằng Sơn Điền. Vị đắng nhẹ của matcha cân bằng vị ngọt của bơ.",
        "variants": [{"sku": "TVT-BQM-6", "label": "Túi 6 chiếc", "price": 65_000, "stock": 30, "slots": 1},
                     {"sku": "TVT-BQM-12", "label": "Hộp 12 chiếc", "price": 120_000, "stock": 15, "slots": 2}],
        "texture": "Giòn tan", "sweetness": "Ngọt vừa", "moment": "Trà chiều, ăn nhẹ cùng trà xanh hoặc ô long thanh.",
        "ingredients": "Bột mì, bơ lạt, đường, bột matcha, trứng gà, muối.",
        "allergens": ["Gluten (lúa mì)", "Sữa", "Trứng"], "shared_line": "Sản xuất chung khu vực có hạt và đậu nành.",
        "storage": "Hộp kín, nhiệt độ phòng, tránh ẩm.", "hsd": "14 ngày kể từ ngày sản xuất.",
        "prep_days": 1, "made_to_order": False, "occasions": ["moi-ngay", "bieu-tang"],
        "pair": ["T04", "T02"], "pair_reason": {"T04": "Matcha gặp matcha – đậm vị trà, bánh giúp dịu vị đắng.",
                                                 "T02": "Ô long thanh làm sạch vị bơ, cân bằng độ béo."},
        "dna": [55, 15, 40, 55, 25], "avoid": ["milk", "caffeine"], "rank": 3, "new": False,
    },
    {
        "id": "B02", "slug": "banh-o-long-mat-ong", "type": "banh",
        "name": "Bánh Bông Lan Ô Long Mật Ong", "brand": "Trồng vị Trà", "line": "Bông lan",
        "tea_used": "T01", "art": "cake", "color": "#C08A3E",
        "taste_note": "Mềm ẩm, hương ô long, ngọt mật ong",
        "desc": "Bông lan mềm ẩm ủ cùng nước cốt trà Đông Phương Mỹ Nhân, thêm mật ong cho vị ngọt tròn.",
        "variants": [{"sku": "TVT-BLO-4", "label": "Hộp 4 miếng", "price": 95_000, "stock": 10, "slots": 2}],
        "texture": "Mềm ẩm", "sweetness": "Ngọt vừa", "moment": "Bữa sáng nhẹ hoặc tiếp khách cùng ô long, hồng trà.",
        "ingredients": "Trứng gà, bột mì, đường, mật ong, sữa tươi, bơ, nước cốt trà ô long.",
        "allergens": ["Gluten (lúa mì)", "Sữa", "Trứng"], "shared_line": "",
        "storage": "Ngăn mát 2–6°C. Để nhiệt độ phòng 15 phút trước khi dùng.", "hsd": "5 ngày kể từ ngày làm bánh.",
        "prep_days": 2, "made_to_order": True, "occasions": ["bieu-tang"],
        "pair": ["T01", "T06"], "pair_reason": {"T01": "Cùng dòng trà làm bánh – hương mật ong được nhân đôi.",
                                                 "T06": "Hồng trà đậm cân bằng độ ngọt của bánh."},
        "dna": [70, 20, 20, 40, 65], "avoid": ["milk", "honey", "caffeine"], "rank": 2, "new": True,
    },
    {
        "id": "B03", "slug": "madeleine-tra-lai", "type": "banh",
        "name": "Madeleine Trà Lài", "brand": "Trồng vị Trà", "line": "Madeleine",
        "tea_used": "T05", "art": "madeleine", "color": "#D7B65A",
        "taste_note": "Viền giòn, ruột xốp, thơm hoa nhài",
        "desc": "Madeleine kiểu Pháp với lá trà xanh ướp lài xay mịn. Viền giòn nhẹ, ruột xốp, hương nhài thoảng.",
        "variants": [{"sku": "TVT-MDL-6", "label": "Hộp 6 chiếc", "price": 85_000, "stock": 0, "slots": 1}],
        "texture": "Viền giòn, ruột xốp", "sweetness": "Ngọt nhẹ", "moment": "Trà chiều với trà xanh, ô long thanh.",
        "ingredients": "Bột mì, bơ, trứng gà, đường, lá trà xanh ướp lài, vỏ chanh.",
        "allergens": ["Gluten (lúa mì)", "Sữa", "Trứng"], "shared_line": "",
        "storage": "Hộp kín, nhiệt độ phòng.", "hsd": "7 ngày kể từ ngày làm bánh.",
        "prep_days": 1, "made_to_order": False, "occasions": ["moi-ngay"],
        "pair": ["T05", "T02"], "pair_reason": {"T05": "Hương nhài lặp lại giữa bánh và trà – nhẹ nhàng, tinh tế.",
                                                 "T02": "Ô long hương hoa nâng vị bơ của madeleine."},
        "dna": [45, 25, 15, 25, 10], "avoid": ["milk", "caffeine"], "rank": 5, "new": False,
    },
    {
        "id": "B04", "slug": "banh-hanh-nhan-o-long-rang", "type": "banh",
        "name": "Bánh Hạnh Nhân Ô Long Rang", "brand": "Trồng vị Trà", "line": "Bánh quy",
        "tea_used": "T03", "art": "cookie", "color": "#7A4A28",
        "taste_note": "Giòn bùi hạnh nhân, hương rang ấm",
        "desc": "Bánh quy mỏng với hạnh nhân lát và trà ô long rang xay. Bùi, giòn, hậu vị rang ấm áp.",
        "variants": [{"sku": "TVT-HNR-8", "label": "Túi 8 chiếc", "price": 75_000, "stock": 22, "slots": 1}],
        "texture": "Giòn mỏng", "sweetness": "Ít ngọt", "moment": "Đi cùng trà đậm, cà phê hoặc làm quà biếu.",
        "ingredients": "Bột mì, hạnh nhân, bơ, đường nâu, trứng gà, trà ô long rang.",
        "allergens": ["Gluten (lúa mì)", "Hạt (hạnh nhân)", "Sữa", "Trứng"], "shared_line": "",
        "storage": "Hộp kín, nhiệt độ phòng, tránh ẩm.", "hsd": "20 ngày kể từ ngày sản xuất.",
        "prep_days": 1, "made_to_order": False, "occasions": ["bieu-tang", "doanh-nghiep"],
        "pair": ["T03", "T04"], "pair_reason": {"T03": "Rang gặp rang – vị bùi hạt hoà vào hương củi.",
                                                 "T04": "Matcha đắng nhẹ làm nổi vị bùi của hạnh nhân."},
        "dna": [35, 10, 45, 65, 40], "avoid": ["milk", "caffeine"], "rank": 6, "new": True,
    },
    {
        "id": "B05", "slug": "banh-tra-sua-hong-tra", "type": "banh",
        "name": "Bánh Cuộn Trà Sữa Hồng Trà", "brand": "Trồng vị Trà", "line": "Bánh cuộn",
        "tea_used": "T06", "art": "roll", "color": "#A8603F",
        "taste_note": "Mềm mịn, kem trà sữa béo nhẹ",
        "desc": "Bánh cuộn mềm, nhân kem tươi pha hồng trà. Vị trà sữa quen thuộc trong một chiếc bánh.",
        "variants": [{"sku": "TVT-BCT-1", "label": "Cuộn 18cm", "price": 145_000, "stock": 6, "slots": 3}],
        "texture": "Mềm mịn", "sweetness": "Ngọt vừa", "moment": "Tráng miệng, tiệc nhỏ cuối tuần.",
        "ingredients": "Trứng gà, bột mì, đường, kem tươi, sữa tươi, hồng trà.",
        "allergens": ["Gluten (lúa mì)", "Sữa", "Trứng"], "shared_line": "",
        "storage": "Ngăn mát 2–6°C, dùng ngay sau khi mở hộp.", "hsd": "3 ngày kể từ ngày làm bánh.",
        "prep_days": 2, "made_to_order": True, "occasions": ["moi-ngay"],
        "pair": ["T06", "T02"], "pair_reason": {"T06": "Cùng gốc hồng trà – trọn vị trà sữa.",
                                                 "T02": "Ô long thanh giúp bớt ngấy kem."},
        "dna": [70, 15, 20, 45, 50], "avoid": ["milk", "caffeine"], "rank": 7, "new": False,
    },
    # ========================== GIFT SET ==========================
    {
        "id": "G01", "slug": "hop-qua-chut-duyen", "type": "gift",
        "name": "Hộp Quà Chút Duyên", "brand": "Trồng vị Trà", "art": "giftbox", "color": "#3B630D",
        "taste_note": "Ô long Đông Phương Mỹ Nhân + bánh bông lan ô long",
        "desc": "Hộp quà nhỏ xinh cho người thương: một gói ô long hương mật ong và bánh bông lan làm từ chính dòng trà ấy.",
        "variants": [{"sku": "TVT-GS-CD", "label": "Hộp tiêu chuẩn", "price": 420_000, "stock": 8, "slots": 0}],
        "items": [("T01", 0, 1), ("B02", 0, 1)], "box": "Hộp giấy kraft nắp rời, lót giấy trà thủ công",
        "includes": ["Thiệp nhỏ viết tay", "Dây cói"], "recipient": "Người thân, bạn bè, đối tác thân thiết",
        "occasions": ["bieu-tang", "sinh-nhat"], "budget": "300-500", "prep_days": 2, "rank": 1, "new": False,
        "card_options": True, "dna": [55, 20, 30, 50, 65], "avoid": ["milk", "honey", "caffeine"],
    },
    {
        "id": "G02", "slug": "hop-qua-tra-chieu", "type": "gift",
        "name": "Hộp Quà Trà Chiều", "brand": "Trồng vị Trà", "art": "giftbox", "color": "#8C9A4B",
        "taste_note": "Ô long hương thanh + madeleine trà lài + bánh quy matcha",
        "desc": "Trọn một buổi trà chiều: ô long thanh mát, madeleine trà lài và bánh quy matcha giòn tan.",
        "variants": [{"sku": "TVT-GS-TC", "label": "Hộp tiêu chuẩn", "price": 390_000, "stock": 5, "slots": 0}],
        "items": [("T02", 0, 1), ("B03", 0, 1), ("B01", 0, 1)], "box": "Hộp giấy cứng màu kem, khay giấy định hình",
        "includes": ["Thiệp chúc mừng", "Ruy băng"], "recipient": "Bạn bè, đồng nghiệp",
        "occasions": ["bieu-tang", "cam-on"], "budget": "300-500", "prep_days": 1, "rank": 2, "new": False,
        "card_options": True, "dna": [40, 20, 25, 35, 15], "avoid": ["milk", "caffeine"],
    },
    {
        "id": "G03", "slug": "hop-qua-tri-an", "type": "gift",
        "name": "Hộp Quà Tri Ân", "brand": "Trồng vị Trà", "art": "giftbox", "color": "#503021",
        "taste_note": "Ô long rang + hồng trà + bánh hạnh nhân",
        "desc": "Bộ quà trang nhã cho đối tác, thầy cô, người lớn tuổi: hai dòng trà đậm vị và bánh hạnh nhân ô long rang.",
        "variants": [{"sku": "TVT-GS-TA", "label": "Hộp tiêu chuẩn", "price": 560_000, "stock": 10, "slots": 0},
                     {"sku": "TVT-GS-TA-L", "label": "Hộp gỗ cao cấp", "price": 790_000, "stock": 4, "slots": 0}],
        "items": [("T03", 0, 1), ("T06", 0, 1), ("B04", 0, 1)], "box": "Hộp giấy cứng nâu / hộp gỗ (bản cao cấp)",
        "includes": ["Thiệp tri ân", "Tag giấy trà"], "recipient": "Đối tác, thầy cô, người lớn tuổi",
        "occasions": ["doanh-nghiep", "cam-on", "tet"], "budget": "500-1000", "prep_days": 2, "rank": 3, "new": True,
        "card_options": True, "dna": [25, 15, 55, 75, 40], "avoid": ["milk", "caffeine"],
    },
    {
        "id": "G04", "slug": "hop-qua-matcha-mini", "type": "gift",
        "name": "Hộp Matcha Mini", "brand": "Trồng vị Trà", "art": "giftbox", "color": "#5E7D2A",
        "taste_note": "Matcha 50g + bánh quy matcha",
        "desc": "Hộp quà nhỏ cho tín đồ matcha: hũ matcha 50g và túi bánh quy matcha bơ.",
        "variants": [{"sku": "TVT-GS-MM", "label": "Hộp tiêu chuẩn", "price": 260_000, "stock": 12, "slots": 0}],
        "items": [("T04", 0, 1), ("B01", 0, 1)], "box": "Hộp giấy kraft nhỏ",
        "includes": ["Thiệp nhỏ"], "recipient": "Bạn bè, người yêu matcha",
        "occasions": ["sinh-nhat", "bieu-tang"], "budget": "duoi-300", "prep_days": 1, "rank": 4, "new": False,
        "card_options": True, "dna": [40, 15, 50, 65, 20], "avoid": ["milk", "caffeine"],
    },
]

TYPE_LABEL = {"tra": "Trà", "banh": "Bánh từ trà", "gift": "Gift set"}
TYPE_ROUTE = {"tra": "tra", "banh": "banh", "gift": "gift-set"}
ROUTE_TYPE = {v: k for k, v in TYPE_ROUTE.items()}

OCCASIONS = {"moi-ngay": "Thưởng trà mỗi ngày", "bieu-tang": "Biếu tặng", "doanh-nghiep": "Quà doanh nghiệp",
             "sinh-nhat": "Sinh nhật", "cam-on": "Cảm ơn", "tet": "Tết"}
TEA_GROUPS = {"o-long": "Ô long", "matcha": "Matcha", "tra-xanh": "Trà xanh", "hong-tra": "Hồng trà"}
FLAVORS = {"hoa": "Hương hoa", "hoa-qua": "Hương trái chín", "thanh": "Thanh nhẹ", "dam": "Đậm vị",
           "rang": "Hương rang", "thao-moc": "Thảo mộc / umami", "ngot-hau": "Hậu ngọt"}
PRICE_RANGES = {"duoi-150": ("Dưới 150.000đ", 0, 150_000), "150-300": ("150.000 – 300.000đ", 150_000, 300_000),
                "300-500": ("300.000 – 500.000đ", 300_000, 500_000), "tren-500": ("Trên 500.000đ", 500_000, 10**9)}

# Sản phẩm mua kèm giá thấp (gợi ý ở giỏ hàng)
ADDONS = [
    {"id": "A01", "slug": "tui-giay-qua", "type": "addon", "name": "Túi giấy quà tặng", "art": "bag", "color": "#B79868",
     "variants": [{"sku": "TVT-TUI", "label": "1 chiếc", "price": 15_000, "stock": 200, "slots": 0}]},
    {"id": "A02", "slug": "tui-loc-tra", "type": "addon", "name": "Túi lọc trà giấy (50 cái)", "art": "filter", "color": "#D8C7A4",
     "variants": [{"sku": "TVT-LOC", "label": "50 cái", "price": 25_000, "stock": 120, "slots": 0}]},
    {"id": "A03", "slug": "thiep-chuc-mung", "type": "addon", "name": "Thiệp chúc mừng giấy trà", "art": "card", "color": "#8C9A4B",
     "variants": [{"sku": "TVT-THIEP", "label": "1 thiệp", "price": 20_000, "stock": 150, "slots": 0}]},
]

# -----------------------------------------------------------------
# TẠO HỘP QUÀ – hộp, giấy gói, thiệp, phụ kiện
# -----------------------------------------------------------------
BOXES = [
    {"id": "BX-S", "name": "Hộp Duyên nhỏ", "outer": "18 × 14 × 7 cm", "inner": "17 × 13 × 6 cm",
     "material": "Giấy kraft cứng", "color": "Nâu kraft", "capacity": 3, "price": 35_000, "stock": 40, "prep_days": 0},
    {"id": "BX-M", "name": "Hộp Duyên vừa", "outer": "25 × 20 × 8 cm", "inner": "24 × 19 × 7 cm",
     "material": "Giấy cứng bọc giấy mỹ thuật", "color": "Kem", "capacity": 6, "price": 55_000, "stock": 25, "prep_days": 0},
    {"id": "BX-L", "name": "Hộp Duyên lớn nắp gỗ", "outer": "32 × 24 × 10 cm", "inner": "31 × 23 × 9 cm",
     "material": "Thân giấy cứng, nắp gỗ thông", "color": "Nâu gỗ", "capacity": 10, "price": 120_000, "stock": 6, "prep_days": 1},
]
PAPERS = [
    {"id": "PP-NONE", "name": "Không thêm giấy gói", "desc": "Giữ nguyên vẻ mộc của hộp.", "price": 0, "stock": 999,
     "color": "#FAF7F0", "fits": ["BX-S", "BX-M", "BX-L"], "prep_days": 0},
    {"id": "PP-TEA", "name": "Giấy trà thủ công", "desc": "Làm từ phụ phẩm trà, mỗi tờ có sắc độ và vân hơi khác nhau.",
     "price": 25_000, "stock": 30, "color": "#C9B98F", "fits": ["BX-S", "BX-M"], "prep_days": 1, "handmade": True},
    {"id": "PP-KEM", "name": "Giấy mỹ thuật màu kem", "desc": "Bề mặt vân mịn, sang nhẹ.", "price": 15_000, "stock": 50,
     "color": "#EDD4AB", "fits": ["BX-S", "BX-M", "BX-L"], "prep_days": 0},
    {"id": "PP-MATCHA", "name": "Giấy kraft xanh matcha", "desc": "Xanh dịu, hợp hộp quà trà xanh.", "price": 15_000,
     "stock": 0, "color": "#8C9A4B", "fits": ["BX-S", "BX-M", "BX-L"], "prep_days": 0},
]
CARDS = [
    {"id": "CD-NONE", "name": "Không dùng thiệp", "size": "", "print": "", "price": 0, "stock": 999, "max_chars": 0},
    {"id": "CD-MINI", "name": "Thiệp mini giấy trà", "size": "9 × 5,5 cm", "print": "In lời chúc", "price": 15_000,
     "stock": 60, "max_chars": 120},
    {"id": "CD-FOLD", "name": "Thiệp gập họa tiết lá trà", "size": "10 × 15 cm (gập đôi)", "print": "In lời chúc mặt trong",
     "price": 25_000, "stock": 40, "max_chars": 250},
    {"id": "CD-HAND", "name": "Thiệp viết tay thư pháp", "size": "10 × 15 cm", "print": "Viết tay", "price": 45_000,
     "stock": 10, "max_chars": 150, "prep_days": 1},
]
ACCESSORIES = [
    {"id": "AC-COI", "name": "Dây cói buộc hộp", "unit": "sợi", "price": 5_000, "stock": 100, "max": 2},
    {"id": "AC-RUYBANG", "name": "Ruy băng lụa xanh đậm", "unit": "sợi", "price": 10_000, "stock": 60, "max": 2},
    {"id": "AC-TAG", "name": "Tag giấy trà ghi tên", "unit": "chiếc", "price": 8_000, "stock": 80, "max": 3},
    {"id": "AC-NHANH", "name": "Nhành trà khô trang trí", "unit": "nhành", "price": 12_000, "stock": 0, "max": 1},
]
WISH_SAMPLES = [
    "Gửi bạn một chút trà, thêm chút duyên. Chúc bạn luôn bình an!",
    "Cảm ơn vì đã luôn đồng hành. Mong mỗi tách trà mang đến cho bạn một khoảng lặng dễ chịu.",
    "Chúc mừng sinh nhật! Mong tuổi mới của bạn thơm như trà và ngọt như bánh.",
    "Năm mới an khang, vạn sự như ý. Kính chúc gia đình nhiều sức khỏe!",
]
GIFTBOX_PACKING_DAYS = 1

# -----------------------------------------------------------------
# THIẾT KẾ RIÊNG
# -----------------------------------------------------------------
CUSTOM_SCOPES = [
    {"icon": "logo", "title": "In tên, logo lên hộp & thiệp",
     "desc": "In logo doanh nghiệp, tên người nhận hoặc thông điệp riêng lên nắp hộp, tag và thiệp."},
    {"icon": "leaf", "title": "Chọn món theo ngân sách",
     "desc": "Phối trà, bánh từ trà và phụ kiện theo ngân sách, khẩu vị và số lượng quà."},
    {"icon": "paper", "title": "Bao bì & giấy trà thủ công",
     "desc": "Chọn chất liệu hộp, màu giấy, giấy trà thủ công và cách sắp xếp lòng hộp."},
    {"icon": "card", "title": "Thiệp & lời nhắn riêng",
     "desc": "Thiết kế thiệp theo nhận diện, lời nhắn khác nhau cho từng người nhận (theo danh sách)."},
]
CUSTOM_IDEAS = [
    {"title": "Quà Tết doanh nghiệp", "tag": "doanh-nghiep", "desc": "Hộp gỗ, in logo nắp, 2 dòng trà + bánh hạnh nhân.", "color": "#503021"},
    {"title": "Quà tri ân khách hàng", "tag": "doanh-nghiep", "desc": "Hộp kraft, thiệp in tên khách, ô long + bánh quy.", "color": "#3B630D"},
    {"title": "Quà cưới – hồi môn trà", "tag": "cuoi", "desc": "Giấy trà thủ công, tag tên cô dâu chú rể, trà lài.", "color": "#B4762E"},
    {"title": "Quà sự kiện / hội thảo", "tag": "su-kien", "desc": "Túi giấy mini in logo, trà túi lọc và bánh nhỏ.", "color": "#8C9A4B"},
    {"title": "Quà Trung thu", "tag": "le-tet", "desc": "Hộp tròn, hồng trà + bánh trà, thiệp họa tiết trăng.", "color": "#8E3B22"},
    {"title": "Quà 20/11 tặng thầy cô", "tag": "le-tet", "desc": "Hộp nhỏ, thiệp viết tay, ô long hương thanh.", "color": "#7C8F3A"},
]
CUSTOM_IDEA_TAGS = {"doanh-nghiep": "Doanh nghiệp", "cuoi": "Cưới hỏi", "su-kien": "Sự kiện", "le-tet": "Lễ, Tết"}
CUSTOM_STEPS = [
    ("Gửi yêu cầu", "Bạn điền biểu mẫu với nhu cầu, số lượng, ngân sách và thời gian. Hệ thống cấp mã yêu cầu."),
    ("Tư vấn & báo giá", "Trồng vị Trà liên hệ qua kênh bạn chọn để làm rõ nhu cầu và gửi báo giá, phạm vi công việc."),
    ("Chốt phạm vi & đặt cọc", "Hai bên thống nhất phạm vi, điều kiện thanh toán. Đơn chỉ bắt đầu khi phạm vi được chấp thuận."),
    ("Thiết kế & duyệt mẫu", "Bạn nhận bản thiết kế, góp ý theo số vòng sửa đã thống nhất và duyệt mẫu cuối."),
    ("Sản xuất & giao quà", "Sản xuất theo mẫu đã duyệt, đóng gói và giao đến địa chỉ hoặc danh sách người nhận."),
]
CUSTOM_TERMS = [
    ("Số lượng tối thiểu", "Áp dụng theo loại tùy chỉnh (in logo, hộp riêng…). Mức cụ thể sẽ được báo trong báo giá."),
    ("Thời gian thực hiện", "Tính từ khi duyệt mẫu, tùy số lượng và mùa cao điểm. Hãy gửi yêu cầu sớm cho dịp lễ, Tết."),
    ("Đặt cọc & thanh toán", "Chỉ thanh toán khi đã có báo giá và phạm vi được chấp thuận. Tỷ lệ cọc ghi rõ trong báo giá."),
    ("Chỉnh sửa & hủy", "Số vòng sửa mẫu, điều kiện thay đổi hoặc hủy sau khi sản xuất theo Quy định quà cá nhân hóa."),
]
CUSTOM_FAQ = [
    ("Gửi yêu cầu có mất phí không?", "Không. Gửi yêu cầu và nhận tư vấn, báo giá đều miễn phí."),
    ("Mã yêu cầu có phải mã đơn hàng không?", "Không. Mã yêu cầu (YC-…) dùng để trao đổi báo giá. Mã đơn hàng chỉ được tạo khi bạn chốt phạm vi và thanh toán."),
    ("Tôi chỉ cần vài hộp quà có in tên thì sao?", "Với số lượng nhỏ, bạn có thể dùng Tạo hộp quà và thêm tag/thiệp có tên. Nếu cần in riêng, hãy gửi yêu cầu để được tư vấn."),
    ("Tôi có thể gửi logo ở định dạng nào?", "Ưu tiên file PDF, PNG nền trong suốt hoặc AI/SVG (có thể gửi sau qua email khi được tư vấn)."),
]

# -----------------------------------------------------------------
# CHUYỆN TRÀ (bài viết)
# -----------------------------------------------------------------
ARTICLE_CATS = {"kien-thuc": "Kiến thức trà", "nguoi-trong": "Chuyện người trồng", "tin-tuc": "Tin tức",
                "huong-dan": "Hướng dẫn pha", "tra-banh": "Trà & bánh", "qua-tang": "Gợi ý quà tặng"}
ARTICLES = [
    {
        "slug": "huong-dan-chon-tra", "cat": "kien-thuc", "featured": True,
        "title": "Người mới bắt đầu nên chọn trà gì?", "date": "2026-11-10", "author": "Góc thưởng trà",
        "summary": "Ô long thanh, trà xanh ướp hoa hay hồng trà? Gợi ý cách chọn trà đầu tiên theo khẩu vị và thói quen của bạn.",
        "color": "#7C8F3A", "tags": ["nguoimoi", "chontra"], "products": ["T02", "T05"],
        "body": [
            ("h2", "Bắt đầu từ khẩu vị bạn đã quen"),
            ("p", "Nếu bạn quen uống trà sữa hay trà trái cây, đừng vội chuyển sang những dòng trà đậm, chát. Hãy bắt đầu với các dòng có hương thơm rõ và vị dịu như ô long lên men nhẹ hoặc trà xanh ướp hoa. Hương thơm giúp bạn dễ \"làm quen\" với vị trà nguyên bản mà không cần đường."),
            ("p", "Ngược lại, nếu bạn thích cà phê đen hay sô-cô-la đắng, hồng trà và ô long rang sẽ cho cảm giác quen thuộc hơn: đậm, ấm và có hậu vị rõ."),
            ("product", "T02"),
            ("h2", "Ba dòng trà dễ uống cho người mới"),
            ("p", "Ô long hương thanh: viên trà xoăn, nước xanh vàng, hương hoa tươi. Pha được nhiều nước, mỗi nước một chút khác biệt – rất thú vị để khám phá."),
            ("p", "Trà xanh ướp lài: hương nhài thơm sáng, vị thanh. Có thể pha nóng hoặc ủ lạnh qua đêm cho một bình trà mát."),
            ("p", "Hồng trà: vị đậm, êm, hương mật ong. Uống nguyên bản hoặc thêm chút sữa để có ly trà sữa tự làm."),
            ("h2", "Đừng quên nhiệt độ nước"),
            ("p", "Nhiều người nghĩ trà \"đắng\" vì pha bằng nước sôi quá lâu. Trà xanh nên pha ở khoảng 75–80°C, ô long khoảng 90–95°C và hồng trà khoảng 95°C. Thời gian hãm ngắn cho nước đầu, tăng dần cho các nước sau. Mỗi sản phẩm của chúng tôi đều có bảng hướng dẫn pha riêng – hãy xem tại trang chi tiết."),
            ("h2", "Chưa chắc gu của mình?"),
            ("p", "Hãy thử Tea DNA – 12 câu hỏi vui về độ ngọt, chua, đắng, độ đậm và hương bạn thích. Kết quả là hồ sơ khẩu vị trên 5 trục cùng gợi ý trà, bánh phù hợp. Không cần email, không cần tài khoản."),
        ],
    },
    {
        "slug": "cold-brew-tra-va-banh", "cat": "huong-dan", "featured": False,
        "title": "Bí kíp pha trà lạnh Cold Brew dùng kèm bánh", "date": "2026-11-02", "author": "Góc thưởng trà",
        "summary": "Ủ trà lạnh qua đêm cho vị ngọt dịu, ít chát. Cách làm đơn giản và gợi ý bánh ăn kèm.",
        "color": "#5E8C6A", "tags": ["coldbrew", "trabanh"], "products": ["T05", "B03"],
        "body": [
            ("h2", "Vì sao trà ủ lạnh dịu hơn?"),
            ("p", "Khi ủ ở nhiệt độ thấp, các hợp chất tạo vị chát được chiết ra chậm hơn, nên nước trà ngọt dịu và thơm hơn. Đây là cách dễ nhất để uống trà mỗi ngày mà không cần canh nhiệt độ nước."),
            ("h2", "Công thức cơ bản"),
            ("p", "Cho khoảng 8–10g trà vào bình 1 lít nước lọc, đậy kín và để ngăn mát 6–8 tiếng. Lọc bỏ bã và dùng trong 2 ngày. Trà xanh ướp lài và ô long hương thanh là hai lựa chọn cho kết quả thơm nhất."),
            ("product", "T05"),
            ("h2", "Ăn kèm bánh gì?"),
            ("p", "Trà lạnh hương hoa rất hợp với madeleine trà lài hoặc bánh quy matcha. Vị bơ của bánh được trà làm sạch, còn hương nhài lặp lại giữa trà và bánh tạo cảm giác liền mạch, nhẹ nhàng cho buổi chiều hè."),
            ("p", "Mẹo nhỏ: thêm vài lát cam hoặc một nhánh bạc hà vào bình trước khi ủ để có biến tấu mới."),
        ],
    },
    {
        "slug": "y-nghia-qua-tang-tra", "cat": "qua-tang", "featured": False,
        "title": "Ý nghĩa của món quà trà trong dịp Tết", "date": "2026-10-25", "author": "Góc thưởng trà",
        "summary": "Vì sao trà luôn có mặt trong giỏ quà Tết, và cách chọn hộp quà hợp với từng người nhận.",
        "color": "#8E3B22", "tags": ["tet", "quatang"], "products": ["G03", "G01"],
        "body": [
            ("p", "Với người Việt, mời nhau chén trà là mở đầu cho một cuộc trò chuyện. Tặng trà vì thế không chỉ là tặng một món đồ uống, mà là gửi đi lời mời gặp gỡ, sự trân trọng và mong ước bình an."),
            ("h2", "Chọn quà theo người nhận"),
            ("p", "Người lớn tuổi thường thích trà đậm vị, truyền thống như ô long rang hay hồng trà. Bạn bè trẻ có thể thích matcha, trà ướp hoa hoặc các hộp có bánh đi kèm. Với đối tác, một hộp quà trang nhã có thiệp tri ân sẽ ghi điểm hơn những món quá phô trương."),
            ("product", "G03"),
            ("h2", "Một lời nhắn nhỏ"),
            ("p", "Đừng quên một tấm thiệp. Vài dòng viết riêng cho người nhận luôn là phần được nhớ lâu nhất của món quà."),
        ],
    },
    {
        "slug": "giay-tra-thu-cong", "cat": "nguoi-trong", "featured": False,
        "title": "Lá trà được tiếp tục câu chuyện: giấy trà thủ công", "date": "2026-10-15", "author": "Hằng Sơn Điền",
        "summary": "Hành trình phụ phẩm trà trở thành giấy thủ công dùng trang trí hộp quà, thiệp và tag.",
        "color": "#B79868", "tags": ["phupham", "giaytra"], "products": ["G01"],
        "body": [
            ("p", "Sau khi sàng lọc, một phần lá và cọng trà không dùng để đóng gói. Thay vì bỏ đi, chúng tôi đang thử nghiệm biến phần phụ phẩm phù hợp thành giấy thủ công để trang trí hộp quà và thiệp."),
            ("h2", "Từ phụ phẩm đến tờ giấy"),
            ("p", "Phụ phẩm được xử lý, sàng lọc, phối cùng sợi giấy rồi ép và phơi khô. Mỗi tờ giấy vì thế có vân và sắc độ hơi khác nhau. Giấy trà dùng cho trang trí bên ngoài, không tiếp xúc trực tiếp với bánh. Quy trình và ứng dụng cụ thể đang được tiếp tục hoàn thiện."),
        ],
    },
    {
        "slug": "thuat-ngu-tra-de-hieu", "cat": "kien-thuc", "featured": False,
        "title": "Hậu vị, độ chát, nước đầu… thuật ngữ trà dễ hiểu", "date": "2026-10-05", "author": "Góc thưởng trà",
        "summary": "Giải thích ngắn gọn những từ hay gặp khi đọc mô tả trà để bạn chọn trà tự tin hơn.",
        "color": "#C9B458", "tags": ["kienthuc"], "products": ["T01"],
        "body": [
            ("h2", "Hậu vị"),
            ("p", "Cảm giác còn đọng lại trong miệng và cổ họng sau khi nuốt ngụm trà – có thể là ngọt, thơm hoặc se nhẹ."),
            ("h2", "Độ chát"),
            ("p", "Cảm giác se, khô nhẹ trên lưỡi. Chát khác với đắng: đắng là vị, còn chát là cảm giác."),
            ("h2", "Nước đầu, nước hai"),
            ("p", "Mỗi lần rót nước vào ấm là một \"nước\". Với ô long, nước hai và nước ba thường thơm và tròn vị nhất."),
            ("product", "T01"),
        ],
    },
    {
        "slug": "ra-mat-trong-vi-tra", "cat": "tin-tuc", "featured": False,
        "title": "Trồng vị Trà ra mắt: trà, bánh từ trà và hộp quà theo cách của bạn", "date": "2026-09-28",
        "author": "Trồng vị Trà", "summary": "Không gian giới thiệu trà Hằng Sơn Điền, bánh mang hương trà và dịch vụ tạo hộp quà.",
        "color": "#3B630D", "tags": ["tintuc"], "products": ["G02"],
        "body": [
            ("p", "Trồng vị Trà là không gian trực tuyến giới thiệu trà tuyển chọn của Hằng Sơn Điền, những chiếc bánh mang hương trà và dịch vụ tạo hộp quà theo lời bạn muốn gửi."),
            ("p", "Bạn có thể tự tay chọn trà, bánh, hộp, giấy gói và thiệp, hoặc gửi yêu cầu thiết kế riêng cho doanh nghiệp, sự kiện."),
            ("product", "G02"),
        ],
    },
    {
        "slug": "ket-hop-tra-va-banh", "cat": "tra-banh", "featured": False,
        "title": "3 nguyên tắc ghép trà với bánh", "date": "2026-09-20", "author": "Góc thưởng trà",
        "summary": "Đậm đi với ngọt, chát đi với béo, hương đi với hương – bí quyết để trà và bánh nâng nhau lên.",
        "color": "#A8603F", "tags": ["trabanh"], "products": ["B02", "T06"],
        "body": [
            ("h2", "Đậm – ngọt"),
            ("p", "Trà đậm như hồng trà hay ô long rang cân bằng tốt với bánh ngọt nhiều như bông lan mật ong."),
            ("h2", "Chát – béo"),
            ("p", "Độ chát nhẹ của trà xanh giúp làm sạch vị bơ, kem của bánh quy, bánh cuộn."),
            ("h2", "Hương – hương"),
            ("p", "Khi bánh dùng chính loại trà đang uống, hương trà được lặp lại và kéo dài – một cặp đôi an toàn mà tinh tế."),
            ("product", "B02"),
        ],
    },
]

# -----------------------------------------------------------------
# TEA DNA
# -----------------------------------------------------------------
DNA_QUESTIONS = [
    {"id": "q1", "text": "Khi uống trà trái cây, bạn thích độ ngọt như thế nào?", "type": "scale", "left": "Ít ngọt", "right": "Rất ngọt"},
    {"id": "q2", "text": "Một ly trà sữa 100% đường ở quán, với bạn là…", "type": "single",
     "options": [("a", "Quá ngọt, mình thường gọi 30–50% đường", 0), ("b", "Vừa đủ", 50), ("c", "Có khi mình còn muốn ngọt hơn", 100)]},
    {"id": "q3", "text": "Bạn thích độ chua trong đồ uống ở mức nào?", "type": "scale", "left": "Ít chua", "right": "Rất chua"},
    {"id": "q4", "text": "Gọi trà chanh / trà tắc, bạn thường…", "type": "single",
     "options": [("a", "Dặn bớt chanh, sợ chua", 0), ("b", "Uống như quán pha", 50), ("c", "Xin thêm chanh / tắc", 100)]},
    {"id": "q5", "text": "Bạn chấp nhận vị đắng của trà đến mức nào?", "type": "scale", "left": "Không thích đắng", "right": "Đắng càng rõ càng hay"},
    {"id": "q6", "text": "Bạn có thích hậu vị chát (se đầu lưỡi) của trà không?", "type": "scale", "left": "Không thích", "right": "Rất thích"},
    {"id": "q7", "text": "Độ đậm trà bạn yêu thích?", "type": "scale", "left": "Nhẹ", "right": "Đậm"},
    {"id": "q8", "text": "Bạn thường uống trà nguyên bản hay trà pha chế?", "type": "single",
     "options": [("original", "Trà nguyên bản, không đường", None), ("flexible", "Cả hai tùy hôm", None),
                 ("mixed", "Chủ yếu trà pha chế, trà trái cây, trà sữa", None)]},
    {"id": "q9", "text": "Bạn thường thích hương nào hơn?", "type": "single", "grid": True,
     "options": [("fruity", "Trái cây: đào, vải, cam, dâu", 100), ("floral", "Hoa: nhài, hồng, lavender", 0),
                 ("roasted", "Rang: gạo rang, hạt, caramel", 50), ("herbal", "Thảo mộc: bạc hà, sả, rosemary", 0)]},
    {"id": "q10", "text": "Bạn thích sữa và độ béo trong đồ uống đến mức nào?", "type": "scale", "left": "Không cần sữa", "right": "Càng béo càng thích"},
    {"id": "q11", "text": "Bạn thích trà nóng hay lạnh?", "type": "single",
     "options": [("cold", "Lạnh", None), ("hot", "Nóng", None), ("both", "Cả hai", None)]},
    {"id": "q12", "text": "Có vị hoặc thành phần nào bạn muốn tránh? (có thể chọn nhiều)", "type": "multi",
     "options": [("milk", "Sữa bò"), ("caffeine", "Caffeine"), ("honey", "Mật ong"), ("sour", "Vị quá chua"), ("none", "Không có lựa chọn cần tránh")]},
]
DNA_AXES = [
    {"key": "sweet", "label": "Độ ngọt", "left": "Ít ngọt", "right": "Ngọt"},
    {"key": "sour", "label": "Độ chua", "left": "Dịu", "right": "Chua rõ"},
    {"key": "bitter", "label": "Độ đắng", "left": "Êm", "right": "Đắng rõ"},
    {"key": "strength", "label": "Độ đậm trà", "left": "Nhẹ", "right": "Đậm"},
    {"key": "aroma", "label": "Hương", "left": "Hoa", "right": "Trái cây"},
]
DNA_GROUPS = [
    {"id": "honey-bloom", "name": "Honey Bloom", "tagline": "Người yêu vị ngọt dịu", "desc": "Thích đồ uống ngọt, thơm trái cây, dễ uống.", "proto": [75, 45, 20, 35, 70], "tag": "fruity", "color": "#E4A05A", "level": "Cân bằng"},
    {"id": "citrus-spark", "name": "Citrus Spark", "tagline": "Tia nắng chua tươi", "desc": "Ưa vị chua tươi, thơm sáng, cảm giác sảng khoái.", "proto": [45, 80, 25, 45, 85], "tag": "fruity", "color": "#D9C53A", "level": "Tươi sáng"},
    {"id": "roasted-soul", "name": "Roasted Soul", "tagline": "Tâm hồn hương rang", "desc": "Thích vị trà rõ, ít ngọt, hậu vị rang.", "proto": [20, 20, 65, 80, 30], "tag": "roasted", "color": "#6B3F22", "level": "Đậm"},
    {"id": "petal-whisper", "name": "Petal Whisper", "tagline": "Thì thầm cánh hoa", "desc": "Ưa hương hoa dịu, vị nhẹ và thanh.", "proto": [30, 25, 20, 30, 10], "tag": "floral", "color": "#E3A9B8", "level": "Nhẹ"},
    {"id": "velvet-matcha", "name": "Velvet Matcha", "tagline": "Đậm mà mượt", "desc": "Thích độ đậm nhưng không muốn vị gắt.", "proto": [35, 20, 55, 65, 25], "tag": None, "color": "#7C9A3F", "level": "Đậm vừa"},
    {"id": "sugar-muse", "name": "Sugar Muse", "tagline": "Nàng thơ ngọt ngào", "desc": "Rất thích ngọt, thiên về dessert drinks.", "proto": [95, 35, 15, 35, 75], "tag": None, "color": "#E28AA8", "level": "Ngọt"},
    {"id": "berry-rebel", "name": "Berry Rebel", "tagline": "Nổi loạn vị berry", "desc": "Thích chua rõ, hương berry.", "proto": [45, 85, 25, 45, 95], "tag": "fruity", "color": "#C2405A", "level": "Chua rõ"},
    {"id": "lemon-theory", "name": "Lemon Theory", "tagline": "Lý thuyết của chanh", "desc": "Chua thanh, citrus, ít ngọt.", "proto": [15, 90, 30, 40, 85], "tag": "fruity", "color": "#A9C34A", "level": "Chua thanh"},
    {"id": "tea-minimalist", "name": "Tea Minimalist", "tagline": "Tối giản cùng trà", "desc": "Ít ngọt, thích vị trà nguyên bản.", "proto": [10, 20, 60, 70, 20], "tag": None, "color": "#6E7A5E", "level": "Nguyên bản"},
    {"id": "creamy-cloud", "name": "Creamy Cloud", "tagline": "Đám mây béo mịn", "desc": "Thích béo, mịn, êm.", "proto": [60, 15, 15, 40, 50], "tag": None, "color": "#D6B98A", "level": "Êm"},
    {"id": "garden-muse", "name": "Garden Muse", "tagline": "Người lữ hành thảo mộc", "desc": "Thích hương hoa và thảo mộc tự nhiên.", "proto": [30, 25, 25, 35, 5], "tag": "herbal", "color": "#5E8C6A", "level": "Dịu"},
    {"id": "tropical-soul", "name": "Tropical Soul", "tagline": "Hồn nhiệt đới", "desc": "Thích trái cây nhiệt đới, hương rõ.", "proto": [75, 65, 20, 45, 95], "tag": "fruity", "color": "#EDA43A", "level": "Rực rỡ"},
    {"id": "amber-classic", "name": "Amber Classic", "tagline": "Hổ phách cổ điển", "desc": "Thích trà đen, ô long, vị truyền thống.", "proto": [20, 15, 70, 85, 30], "tag": None, "color": "#A0522D", "level": "Truyền thống"},
]
DNA_RECIPES = [
    {"id": "r1", "name": "Trà vải lài", "en": "Lychee Jasmine Tea", "kind": "Trà trái cây", "temp": "cold",
     "vec": [70, 40, 20, 30, 80], "tags": ["Sweet", "Fruity"], "time": "10 phút", "level": "Dễ", "cost": "≈ 19.000đ",
     "avoid": ["caffeine"], "tea": "T05", "color": "#E7B9C0",
     "ingredients": ["3g Trà Xanh Ướp Lài", "150ml nước 80°C", "4 quả vải + 20ml nước đường vải", "Đá viên"],
     "steps": ["Hãm trà 2 phút rồi lọc, để nguội.", "Cho vải và nước đường vào ly, thêm đá.", "Rót trà, khuấy nhẹ."]},
    {"id": "r2", "name": "Trà tắc sả", "en": "Kumquat Lemongrass Tea", "kind": "Trà trái cây", "temp": "cold",
     "vec": [40, 85, 25, 35, 70], "tags": ["Sour"], "time": "10 phút", "level": "Dễ", "cost": "≈ 9.000đ",
     "avoid": ["caffeine", "sour"], "tea": "T05", "color": "#D7E3A0",
     "ingredients": ["3g Trà Xanh Ướp Lài", "150ml nước 80°C", "3 quả tắc", "1 nhánh sả đập dập", "15ml đường nước", "Đá"],
     "steps": ["Hãm trà cùng sả 3 phút, lọc.", "Vắt tắc, thêm đường, khuấy.", "Thêm đá và trà."]},
    {"id": "r3", "name": "Trà đào ô long", "en": "Peach Oolong Tea", "kind": "Trà trái cây", "temp": "cold",
     "vec": [65, 45, 25, 45, 85], "tags": ["Sweet", "Fruity"], "time": "10 phút", "level": "Dễ", "cost": "≈ 17.000đ",
     "avoid": ["caffeine"], "tea": "T02", "color": "#F1C49B",
     "ingredients": ["5g Trà Ô Long Hương Thanh", "150ml nước 95°C", "3 miếng đào ngâm + 30ml nước đào", "Đá"],
     "steps": ["Hãm trà 1 phút, lọc.", "Cho đào, nước đào, đá vào ly.", "Rót trà, trang trí lát đào."]},
    {"id": "r4", "name": "Matcha latte sữa yến mạch", "en": "Oat Matcha Latte", "kind": "Trà sữa", "temp": "both",
     "vec": [45, 10, 45, 60, 25], "tags": ["Creamy"], "time": "5 phút", "level": "Trung bình", "cost": "≈ 20.000đ",
     "avoid": ["caffeine"], "tea": "T04", "color": "#A9C07A",
     "ingredients": ["2g Bột Matcha", "40ml nước 75°C", "150ml sữa yến mạch", "10ml siro (tùy chọn)"],
     "steps": ["Rây matcha, đánh với nước nóng đến khi mịn bọt.", "Đun ấm hoặc thêm đá vào sữa yến mạch.", "Rót matcha lên sữa."]},
    {"id": "r5", "name": "Hồng trà sữa", "en": "Classic Milk Tea", "kind": "Trà sữa", "temp": "both",
     "vec": [65, 10, 35, 70, 45], "tags": ["Creamy", "Strong"], "time": "8 phút", "level": "Dễ", "cost": "≈ 12.000đ",
     "avoid": ["caffeine", "milk"], "tea": "T06", "color": "#C99A72",
     "ingredients": ["5g Hồng Trà", "150ml nước 95°C", "60ml sữa tươi", "15ml sữa đặc"],
     "steps": ["Hãm trà 4 phút, lọc.", "Khuấy cùng sữa tươi, sữa đặc.", "Uống nóng hoặc thêm đá."]},
    {"id": "r6", "name": "Ô long rang mật ong ấm", "en": "Honey Roasted Oolong", "kind": "Trà nóng", "temp": "hot",
     "vec": [40, 10, 55, 75, 40], "tags": ["Roasted"], "time": "5 phút", "level": "Dễ", "cost": "≈ 10.000đ",
     "avoid": ["caffeine", "honey"], "tea": "T03", "color": "#B07A4A",
     "ingredients": ["5g Trà Ô Long Rang Củi", "180ml nước 98°C", "10ml mật ong"],
     "steps": ["Tráng ấm và trà bằng nước sôi.", "Hãm 40 giây, rót ra chén.", "Thêm mật ong nếu thích."]},
    {"id": "r7", "name": "Đông Phương Mỹ Nhân nguyên bản", "en": "Oriental Beauty, straight", "kind": "Trà nóng", "temp": "hot",
     "vec": [30, 15, 35, 55, 65], "tags": ["Original"], "time": "5 phút", "level": "Trung bình", "cost": "≈ 14.000đ",
     "avoid": ["caffeine"], "tea": "T01", "color": "#D8A35C",
     "ingredients": ["5g Trà Đông Phương Mỹ Nhân", "150ml nước 90°C"],
     "steps": ["Tráng ấm, cho trà vào.", "Hãm 45 giây nước đầu, tăng 10 giây cho mỗi nước sau.", "Thưởng thức 4–5 nước."]},
    {"id": "r8", "name": "Trà bạc hà hoa cúc (không caffeine)", "en": "Mint Chamomile Infusion", "kind": "Trà thảo mộc", "temp": "both",
     "vec": [25, 15, 10, 20, 5], "tags": ["Herbal"], "time": "7 phút", "level": "Dễ", "cost": "≈ 8.000đ",
     "avoid": [], "tea": None, "color": "#C9DDB0", "caffeine_free_verified": True,
     "ingredients": ["2g hoa cúc khô", "5 lá bạc hà tươi", "200ml nước 90°C"],
     "steps": ["Cho hoa cúc và bạc hà vào ấm.", "Hãm 5 phút rồi lọc.", "Uống nóng hoặc để nguội thêm đá."]},
    {"id": "r9", "name": "Trà xanh lài nguyên bản", "en": "Jasmine Green Tea", "kind": "Trà nóng", "temp": "hot",
     "vec": [20, 20, 30, 35, 5], "tags": ["Floral"], "time": "4 phút", "level": "Dễ", "cost": "≈ 4.000đ",
     "avoid": ["caffeine"], "tea": "T05", "color": "#E3DB9B",
     "ingredients": ["3g Trà Xanh Ướp Lài", "200ml nước 80°C"],
     "steps": ["Tráng ấm.", "Hãm 90 giây.", "Rót ra chén, thưởng thức."]},
]

# -----------------------------------------------------------------
# FAQ (liên hệ + danh mục + tạo quà)
# -----------------------------------------------------------------
FAQ_GROUPS = {
    "chon-tra": "Chọn trà và cách pha", "banh": "Bánh, dị ứng và bảo quản", "qua": "Gift set / tạo quà",
    "thiet-ke": "Thiết kế riêng", "dat-hang": "Đặt và thanh toán", "giao-nhan": "Giao nhận", "doi-tra": "Đổi / hủy / hoàn",
}
FAQS = [
    ("chon-tra", "Trà nào dễ uống cho người mới?", "Ô long hương thanh và trà xanh ướp lài có hương thơm rõ, vị dịu. Bạn cũng có thể làm Tea DNA để nhận gợi ý theo khẩu vị.", "/chuyen-tra/huong-dan-chon-tra"),
    ("chon-tra", "Pha trà ở nhiệt độ bao nhiêu?", "Mỗi sản phẩm có bảng hướng dẫn pha riêng (lượng trà, nước, nhiệt độ, thời gian) tại trang chi tiết.", "/san-pham/tra"),
    ("banh", "Bánh có thành phần gây dị ứng không?", "Có thể có. Mỗi loại bánh ghi rõ thành phần và chất gây dị ứng (gluten, sữa, trứng, hạt…) ngay cạnh nút mua.", "/san-pham/banh"),
    ("banh", "Bánh bảo quản được bao lâu?", "Tùy loại: bánh quy khoảng 2 tuần, bánh bông lan, bánh cuộn cần bảo quản lạnh và dùng trong vài ngày. Xem mục Bảo quản trên từng sản phẩm.", "/san-pham/banh"),
    ("banh", "Bánh có giao toàn quốc không?", "Hiện bánh tươi chỉ giao trong khu vực được hỗ trợ (hiển thị tại bước thanh toán). Trà và bánh khô có thể giao xa hơn.", "/chinh-sach/giao-hang"),
    ("qua", "Gift set có thay đổi được thành phần không?", "Gift set có sẵn giữ nguyên thành phần. Nếu muốn tự chọn món, hãy dùng Tạo hộp quà.", "/dich-vu/tao-hop-qua"),
    ("qua", "Làm sao biết thời gian chuẩn bị?", "Thời gian chuẩn bị hiển thị trên từng sản phẩm và trong bước xem lại hộp quà, tách riêng với thời gian vận chuyển.", "/dich-vu/tao-hop-qua"),
    ("qua", "Giá hộp quà tự tạo đã gồm giấy và thiệp chưa?", "Giá được cộng theo từng lựa chọn: món + hộp + giấy + thiệp + phụ kiện. Phí vận chuyển tính ở bước thanh toán.", "/dich-vu/tao-hop-qua"),
    ("thiet-ke", "Muốn in logo lên hộp quà thì làm sao?", "Gửi yêu cầu tại trang Thiết kế riêng. Chúng tôi sẽ tư vấn và báo giá trước khi bạn thanh toán.", "/dich-vu/thiet-ke-rieng"),
    ("dat-hang", "Có cần tạo tài khoản để mua không?", "Không. Bạn chỉ cần nhập thông tin người đặt, người nhận và địa chỉ.", "/gio-hang"),
    ("dat-hang", "Có những cách thanh toán nào?", "Hiện hỗ trợ thanh toán khi nhận hàng (COD, theo điều kiện) và chuyển khoản ngân hàng.", "/chinh-sach/thanh-toan"),
    ("giao-nhan", "Tôi có thể gửi quà đến người khác không?", "Có. Tại bước thanh toán, tắt \"Người nhận là tôi\" và nhập thông tin người nhận.", "/chinh-sach/giao-hang"),
    ("giao-nhan", "Làm sao xem đơn đang ở đâu?", "Vào Tra cứu đơn, nhập mã đơn và số điện thoại/email đã dùng khi đặt.", "/tra-cuu-don"),
    ("doi-tra", "Nhận hàng bị hỏng thì làm sao?", "Hãy gửi yêu cầu hỗ trợ từ trang Tra cứu đơn kèm mô tả và ảnh (nếu có). Gửi yêu cầu chưa đồng nghĩa đơn đã được xử lý.", "/chinh-sach/doi-tra"),
    ("doi-tra", "Quà cá nhân hóa có đổi trả được không?", "Tùy tình huống cụ thể (lỗi sản xuất, sai mẫu đã duyệt…). Xem Quy định quà cá nhân hóa.", "/chinh-sach/qua-ca-nhan-hoa"),
]
CONTACT_TOPICS = {"chon-tra": "Chọn trà / bánh", "dat-hang": "Đặt hàng", "giao-hang": "Giao hàng",
                  "thanh-toan": "Thanh toán", "doi-tra": "Đổi trả", "thiet-ke": "Thiết kế / quà doanh nghiệp", "khac": "Khác"}

# -----------------------------------------------------------------
# CHÍNH SÁCH (nội dung nháp – cần doanh nghiệp duyệt trước khi xuất bản)
# -----------------------------------------------------------------
POLICY_UPDATED = "14/11/2026"
POLICIES = {
    "huong-dan-dat-hang": {"title": "Hướng dẫn đặt hàng", "group": "support", "sections": [
        ("Chọn sản phẩm", "Chọn trà, bánh hoặc gift set tại trang Sản phẩm, chọn quy cách và số lượng rồi bấm Thêm vào giỏ. Muốn tự phối quà, dùng Tạo hộp quà."),
        ("Kiểm tra giỏ hàng", "Trong giỏ, bạn có thể đổi số lượng, phân loại, thêm ghi chú, yêu cầu xuất hóa đơn và nhập mã giảm giá (nếu có)."),
        ("Thanh toán", "Nhập thông tin người đặt, người nhận, địa chỉ; chọn cách giao và cách thanh toán; kiểm tra lại và bấm đặt hàng. Bạn sẽ nhận mã đơn để tra cứu."),
    ]},
    "thanh-toan": {"title": "Phương thức thanh toán", "group": "support", "sections": [
        ("Thanh toán khi nhận hàng (COD)", "Áp dụng cho đơn đến mức giá trị quy định và khu vực được hỗ trợ. Trạng thái đơn là \"chờ thanh toán khi nhận\" cho đến khi bạn trả tiền cho nhân viên giao hàng."),
        ("Chuyển khoản ngân hàng", "Sau khi đặt, trang kết quả hiển thị thông tin tài khoản, số tiền và nội dung chuyển khoản (mã đơn). Đơn được xác nhận sau khi chúng tôi đối soát."),
        ("Đơn thiết kế riêng", "Chỉ thanh toán khi đã có báo giá và phạm vi được chấp thuận. Tiền cọc và phần còn lại được ghi rõ trong báo giá."),
    ]},
    "dieu-khoan": {"title": "Điều khoản sử dụng", "group": "policy", "sections": [
        ("Đơn vị vận hành", "Website được vận hành bởi đơn vị bán hàng được nêu tại chân trang. Thông tin pháp nhân sẽ được cập nhật khi được xác nhận."),
        ("Thông tin sản phẩm và giá", "Chúng tôi cố gắng hiển thị chính xác thông tin, hình ảnh và giá. Ảnh minh họa có thể khác nhẹ với sản phẩm thực tế, đặc biệt với giấy thủ công."),
        ("Đặt và xác nhận đơn", "Đơn hàng được ghi nhận khi bạn nhận được mã đơn. Trạng thái thanh toán và xử lý đơn được hiển thị riêng."),
        ("Nội dung người dùng gửi", "Lời chúc, logo, tệp thiết kế bạn gửi chỉ dùng để thực hiện đơn/yêu cầu, không công khai hay tái sử dụng cho tiếp thị khi chưa có sự đồng ý."),
        ("Liên hệ", "Mọi thắc mắc vui lòng gửi qua trang Liên hệ."),
    ]},
    "bao-mat": {"title": "Chính sách bảo mật", "group": "policy", "sections": [
        ("Dữ liệu đặt hàng", "Họ tên, số điện thoại, email, địa chỉ nhận hàng – dùng để xử lý, giao đơn và hỗ trợ sau bán."),
        ("Dữ liệu thiết kế", "Logo, tệp tham khảo, danh sách người nhận – chỉ dùng cho yêu cầu thiết kế riêng tương ứng."),
        ("Dữ liệu trên trình duyệt", "Hồ sơ Tea DNA và bản nháp hộp quà được lưu trên trình duyệt của bạn, không gửi lên máy chủ. Bạn có thể xóa bất cứ lúc nào."),
        ("Bên nhận xử lý", "Đơn vị vận chuyển và thanh toán nhận phần dữ liệu cần thiết để thực hiện dịch vụ. Danh sách cụ thể sẽ được cập nhật."),
        ("Quyền của bạn", "Bạn có thể yêu cầu xem, sửa hoặc xóa dữ liệu qua trang Liên hệ. Một số dữ liệu cần lưu theo quy định đối soát, kế toán."),
        ("Nhận tin tiếp thị", "Đăng ký nhận tin là lựa chọn riêng, không bắt buộc để mua hàng, và có thể hủy bất cứ lúc nào."),
    ]},
    "giao-hang": {"title": "Chính sách giao hàng", "group": "policy", "sections": [
        ("Khu vực phục vụ", "Trà và bánh khô: giao các tỉnh thành được hỗ trợ. Bánh tươi (cần bảo quản lạnh): chỉ giao trong khu vực được hiển thị tại bước thanh toán."),
        ("Phí giao hàng", "Tính theo khu vực và phương thức giao, hiển thị trước khi đặt. Đơn đạt ngưỡng quy định được miễn phí giao tiêu chuẩn."),
        ("Thời gian chuẩn bị và vận chuyển", "Thời gian chuẩn bị (làm bánh, đóng hộp) được tính riêng với thời gian vận chuyển. Ngày nhận mong muốn là yêu cầu, chúng tôi sẽ cố gắng đáp ứng."),
        ("Giao không thành công / đổi địa chỉ", "Vui lòng liên hệ sớm qua Tra cứu đơn. Đơn đã bàn giao vận chuyển có thể không đổi địa chỉ được."),
    ]},
    "kiem-hang": {"title": "Chính sách kiểm hàng", "group": "policy", "sections": [
        ("Được kiểm gì", "Bạn được kiểm tra số lượng kiện, tình trạng bao bì vận chuyển bên ngoài trước khi nhận."),
        ("Bao bì thực phẩm", "Không mở bao kín thực phẩm (gói trà, hộp bánh niêm phong) trước khi nhận để đảm bảo vệ sinh."),
        ("Ghi nhận vấn đề", "Nếu có hư hỏng, hãy chụp ảnh/quay video và gửi yêu cầu hỗ trợ kèm mã đơn trong thời gian sớm nhất."),
    ]},
    "doi-tra": {"title": "Chính sách đổi / hủy / hoàn", "group": "policy", "sections": [
        ("Nhận sai, thiếu, hỏng", "Gửi yêu cầu kèm mã đơn, mô tả và ảnh (nếu có). Chúng tôi kiểm tra và phản hồi phương án đổi hoặc hoàn tiền."),
        ("Thay đổi ý định", "Trà nguyên niêm phong: có thể hỗ trợ đổi theo điều kiện. Bánh và thực phẩm tươi: không áp dụng đổi trả vì lý do vệ sinh, trừ lỗi từ phía chúng tôi."),
        ("Hủy đơn", "Có thể yêu cầu hủy trước khi đơn bắt đầu chuẩn bị. Gửi yêu cầu chưa đồng nghĩa đơn đã được hủy."),
        ("Hoàn tiền", "Trạng thái hoàn tiền được cập nhật theo các bước: Yêu cầu hoàn → Đã duyệt → Đang chuyển → Đã hoàn."),
    ]},
    "qua-ca-nhan-hoa": {"title": "Quy định quà cá nhân hóa & thiết kế riêng", "group": "policy", "sections": [
        ("Phạm vi", "Phạm vi tùy chỉnh (in logo, thiệp, hộp, món) được chốt trong báo giá trước khi bắt đầu."),
        ("Duyệt mẫu và lời chúc", "Sản xuất chỉ bắt đầu khi bạn duyệt mẫu cuối. Lời chúc được in nguyên văn theo nội dung bạn cung cấp."),
        ("Cọc và số vòng sửa", "Tỷ lệ cọc và số vòng sửa mẫu ghi trong báo giá."),
        ("Thay đổi / hủy", "Trước khi sản xuất: có thể điều chỉnh theo thỏa thuận. Sau khi sản xuất: xử lý theo từng tình huống; lỗi do sản xuất sẽ được chúng tôi chịu trách nhiệm."),
        ("Quyền sử dụng logo / thiết kế", "Bạn đảm bảo có quyền sử dụng logo, hình ảnh gửi cho chúng tôi. Chúng tôi không dùng lại cho mục đích khác khi chưa được đồng ý."),
    ]},
}

ORDER_STEPS = ["Đã nhận đơn", "Đã xác nhận", "Đang chuẩn bị", "Đã bàn giao vận chuyển", "Đang giao", "Đã giao"]
PAYMENT_STATUS = {"cod_pending": "Chờ thanh toán khi nhận", "bank_pending": "Chờ thanh toán",
                  "verifying": "Đang xác minh thanh toán", "paid": "Đã thanh toán", "failed": "Chưa thanh toán thành công",
                  "refund_requested": "Yêu cầu hoàn", "refunded": "Đã hoàn"}
