"""Catalog regression checks. Run: python -m unittest test_tea_catalog -v."""
import base64
import os
import tempfile
import unittest
from pathlib import Path
import app as web


class TeaCatalogTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.old_static = web.app.static_folder
        web.app.static_folder = str(Path(self.tmp.name) / 'static')
        (Path(web.app.static_folder) / 'img/products').mkdir(parents=True)
        self.old_db = web.DB_PATH
        web.DB_PATH = str(Path(self.tmp.name) / 'test.db')
        web.init_db()
        web.app.config['TESTING'] = True
        self.client = web.app.test_client()

    def tearDown(self):
        web.DB_PATH = self.old_db
        web.app.static_folder = self.old_static
        self.tmp.cleanup()

    def test_exact_catalog_and_price(self):
        expected = {
            'Trà Ô Long Sữa Cao Cấp HSĐ': ('Gói 200g', 180000),
            'Hồng Trà Cao Cấp HSĐ': ('Gói 200g', 180000),
            'Lão Trà Cao Cấp HSĐ': ('Gói 200g', 104000),
            'Trà Đông Phương Mỹ Nhân Thượng Hạng HSĐ': ('Gói 100g', 296000),
            'Trà Ô Long Tuyết Thượng Hạng HSĐ': ('Gói 100g', 370000),
            'Trà Ô Long Quế Hoa Thượng Hạng HSĐ': ('Gói 100g', 222000),
            'Trà Ô Long Tứ Quý HSĐ': ('Gói 250g', 130000),
            'Trà Ô Long Kim Tuyên HSĐ': ('Gói 250g', 110000),
            'Trà Ô Long Cao Sơn HSĐ': ('Gói 250g', 130000),
            'Trà Ô Long Tứ Quý Cao Cấp HSĐ': ('Gói 250g', 225000),
            'Trà Ô Long Kim Tuyên Cao Cấp HSĐ': ('Gói 250g', 225000),
        }
        teas = [p for p in web.D.PRODUCTS if p['type'] == 'tra']
        actual = {p['name']: (p['variants'][0]['label'], p['variants'][0]['price']) for p in teas}
        self.assertEqual(expected, actual)
        self.assertEqual(11, len(teas))
        listing = self.client.get('/san-pham/tra').get_data(as_text=True)
        self.assertEqual(11, listing.count('class="pcard '))
        for p in teas:
            page = self.client.get('/san-pham/tra/' + p['slug'])
            self.assertEqual(200, page.status_code)
            self.assertIn(web.vnd(p['variants'][0]['price']), page.get_data(as_text=True))

    def test_all_pages_and_references(self):
        for p in web.D.PRODUCTS:
            with web.app.test_request_context():
                url = web.product_url(p)
            self.assertEqual(200, self.client.get(url).status_code, url)
            for pid in p.get('pair', []):
                self.assertIn(pid, web.BY_ID)
            for pid, vi, _ in p.get('items', []):
                self.assertIn(pid, web.BY_ID)
                self.assertLess(vi, len(web.BY_ID[pid]['variants']))
        for url in ['/', '/san-pham', '/san-pham/tra?nhom=lao-tra', '/dich-vu/tao-hop-qua',
                    '/tea-dna', '/tea-dna/ket-qua', '/chuyen-tra', '/gio-hang', '/thanh-toan']:
            self.assertLess(self.client.get(url).status_code, 400, url)
        for article in web.D.ARTICLES:
            self.assertEqual(200, self.client.get('/chuyen-tra/' + article['slug']).status_code)
        self.assertEqual(400, self.client.post('/api/cart/add', json={'sku': 'HSD-MAT-50'}).status_code)

    def test_server_prices_cart_and_gift(self):
        result = self.client.post('/api/cart/add', json={'sku': 'HSD-DPMN-100', 'qty': 2, 'price': 1})
        self.assertEqual(200, result.status_code)
        self.assertEqual(592000, result.json['cart']['subtotal'])
        cart = self.client.get('/gio-hang').get_data(as_text=True)
        self.assertIn('296.000đ', cart)
        self.assertIn('592.000đ', cart)
        with web.app.test_request_context():
            quote, errors = web.giftbox_quote({'items': [{'sku': 'HSD-DPMN-100', 'qty': 1}]})
            self.assertEqual(296000, quote['items'][0]['price'])
            _, errors = web.giftbox_quote({'items': [{'sku': 'HSD-MAT-50', 'qty': 1},
                                                    {'sku': 'HSD-DPMN-100', 'qty': 1}]})
            self.assertTrue(any('không còn trong danh mục' in x for x in errors))

    def test_photo_lookup_shared_surfaces_and_cache(self):
        product = web.BY_ID['T01']
        file = Path(web.app.static_folder) / 'img/products' / (product['slug'] + '.png')
        self.assertFalse(file.exists())
        try:
            with web.app.test_request_context():
                self.assertIsNone(web.product_photo_url(product))
            file.write_bytes(base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+aD1sAAAAASUVORK5CYII='))
            with web.app.test_request_context():
                first = web.product_photo_url(product)
                payload = web.dna_payload()
                self.assertIn(file.name, next(x['art_html'] for x in payload['products'] if x['id'] == 'T01'))
            for url in ['/san-pham/tra', '/san-pham/tra/' + product['slug'], '/dich-vu/tao-hop-qua']:
                self.assertIn(file.name, self.client.get(url).get_data(as_text=True), url)
            self.client.post('/api/cart/add', json={'sku': 'HSD-DPMN-100', 'qty': 1})
            self.assertIn(file.name, self.client.get('/gio-hang').get_data(as_text=True))
            os.utime(file, ns=(file.stat().st_atime_ns, file.stat().st_mtime_ns + 1000000))
            with web.app.test_request_context():
                self.assertNotEqual(first, web.product_photo_url(product))
        finally:
            file.unlink(missing_ok=True)

    def test_old_cart_can_be_removed_and_cannot_checkout(self):
        self.client.get('/gio-hang')
        with self.client.session_transaction() as session:
            cid = session['cart_id']
        with web.app.test_request_context():
            import json
            web.db().execute('INSERT OR REPLACE INTO carts VALUES (?,?,?)',
                (cid, json.dumps({'lines': [{'key': 'old', 'kind': 'product', 'sku': 'HSD-MAT-50', 'qty': 1}]}), 0))
            web.db().commit()
        page = self.client.get('/gio-hang')
        self.assertEqual(200, page.status_code)
        self.assertIn('Món này đã ngừng bán', page.get_data(as_text=True))
        self.assertEqual(400, self.client.post('/api/cart/update', json={'key': 'old', 'qty': 2}).status_code)
        with web.app.test_request_context():
            old_cart = {'lines': [{'key': 'old', 'kind': 'product', 'sku': 'HSD-MAT-50', 'qty': 1}]}
            self.assertIn('_cart', web.validate_checkout({}, web.cart_view(old_cart)))
        self.assertEqual(200, self.client.post('/api/cart/remove', json={'key': 'old'}).status_code)
        self.assertIn('Giỏ hàng đang trống', self.client.get('/gio-hang').get_data(as_text=True))

    def test_product_covers_do_not_change_home(self):
        image_root = Path(web.app.static_folder) / 'img'
        created = []
        home_before = self.client.get('/').get_data(as_text=True)
        png = base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+aD1sAAAAASUVORK5CYII=')
        try:
            for category, stem in [('tra', 'tra'), ('banh', 'banh'), ('gift-set', 'hopqua')]:
                target = image_root / ('cover-' + stem + '.png')
                self.assertFalse(target.exists())
                target.write_bytes(png); created.append(target)
                html = self.client.get('/san-pham/' + category).get_data(as_text=True)
                self.assertIn('class="cat-cover-photo"', html)
                self.assertIn(target.name, html)
                self.assertEqual(home_before, self.client.get('/').get_data(as_text=True))
            mobile = image_root / 'cover-hopqua-mobile.png'
            mobile.write_bytes(png); created.append(mobile)
            self.assertIn(mobile.name, self.client.get('/san-pham/gift-set').get_data(as_text=True))
            self.assertEqual(home_before, self.client.get('/').get_data(as_text=True))
            # Homepage retains its own image file and never substitutes the product cover.
            own = image_root / 'cat-hopqua.jpg'
            own.write_bytes(png); created.append(own)
            homepage = self.client.get('/').get_data(as_text=True)
            self.assertIn('img/cat-hopqua.jpg', homepage)
            self.assertNotIn('img/cover-hopqua', homepage)
        finally:
            for file in created:
                file.unlink(missing_ok=True)

    def test_catalog_copy_navigation_and_cookie_group(self):
        html = self.client.get('/san-pham').get_data(as_text=True)
        self.assertIn('Gói vị thân quen', html)
        self.assertIn('<br><span class="cover-question">Hôm nay, bạn thích vị nào?</span>', html)
        self.assertIn('Mỗi khoảnh khắc - mỗi vị riêng', html)
        self.assertNotIn('Tất cả sản phẩm</a>', html)
        self.assertIn('dd-product-link', html)
        for cat, heading, description in [
            ('tra', 'Vị trà thân quen', 'Trồng nên hương trà, lưu giữ vị nhà'),
            ('banh', 'Vị bánh ấm lòng', 'Ủ hương trà trong bánh, vun chút ngọt cho nhà'),
            ('gift-set', 'Gói vị nhà trao nhau', 'Gói hương trà, gom vị bánh, gửi chút tình nhà')]:
            body = self.client.get('/san-pham/' + cat).get_data(as_text=True)
            self.assertIn('<h1>' + heading + '</h1>', body)
            self.assertIn(description, body)
        body = self.client.get('/san-pham/banh').get_data(as_text=True)
        self.assertEqual(1, body.count('>Chọn vị bánh</a>'))
        for old in ('truyen-thong', 'matcha', 'oolong'):
            response = self.client.get('/san-pham/banh/cracker-meringue-cookies-' + old)
            self.assertEqual(301, response.status_code)
            self.assertTrue(response.location.endswith('/cracker-meringue-cookies'))
        body = self.client.get('/san-pham/banh/cracker-meringue-cookies').get_data(as_text=True)
        self.assertIn('data-flavor-select', body)
        self.assertEqual(6, body.count('name="sku"'))
        for flavor in ('Truyền thống', 'Matcha', 'Oolong'):
            self.assertIn('data-flavor-option="' + flavor + '"', body)

    def test_cookie_and_mochi_prices_in_cart_and_gift(self):
        cookies = [web.BY_ID['BC01']]
        mochi = web.BY_ID['BC04']
        self.assertEqual(3, sum(p['type'] == 'banh' for p in web.D.PRODUCTS))
        for product in cookies:
            self.assertEqual(3, len(product['flavors']))
            self.assertEqual([('Pack 2 cái', 2500), ('Combo 2 pack (4 cái)', 4000)] * 3,
                             [(v['size'], v['price']) for v in product['variants']])
        self.assertEqual(('1 cái', 7500), (mochi['variants'][0]['label'], mochi['variants'][0]['price']))
        paparoti = web.BY_ID['BC05']
        self.assertEqual(('1 cái', 10000), (paparoti['variants'][0]['label'], paparoti['variants'][0]['price']))
        for product in cookies + [mochi, paparoti]:
            for variant in product['variants']:
                client = web.app.test_client()
                result = client.post('/api/cart/add', json={'sku': variant['sku'], 'qty': 2, 'price': 1})
                self.assertEqual(200, result.status_code)
                self.assertEqual(variant['price'] * 2, result.json['cart']['subtotal'])
                self.assertIn(variant['label'], client.get('/gio-hang').get_data(as_text=True))
                with web.app.test_request_context():
                    quote, _ = web.giftbox_quote({'items': [{'sku': variant['sku'], 'qty': 1}]})
                    self.assertEqual(variant['price'], quote['items'][0]['price'])
        self.assertEqual(400, self.client.post('/api/cart/add', json={'sku': 'TVT-BQM-6'}).status_code)

    def test_bakery_photo_is_shared_and_home_unchanged(self):
        product = web.BY_ID['BC01']
        photo = Path(web.app.static_folder) / 'img/products' / (product['image_stem'] + '.png')
        self.assertFalse(photo.exists())
        before = self.client.get('/').get_data(as_text=True)
        try:
            photo.write_bytes(base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+aD1sAAAAASUVORK5CYII='))
            for url in ['/san-pham/banh', '/san-pham/banh/' + product['slug'], '/dich-vu/tao-hop-qua']:
                self.assertIn(photo.name, self.client.get(url).get_data(as_text=True))
            self.client.post('/api/cart/add', json={'sku': product['variants'][1]['sku'], 'qty': 1})
            self.assertIn(photo.name, self.client.get('/gio-hang').get_data(as_text=True))
            # Use a fresh empty-cart client to compare the homepage body without badge changes.
            self.assertEqual(before, web.app.test_client().get('/').get_data(as_text=True))
        finally:
            photo.unlink(missing_ok=True)


if __name__ == '__main__':
    unittest.main()
