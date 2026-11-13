# -*- coding: utf-8 -*-
"""
TRỒNG VỊ TRÀ — Hằng Sơn Điền × Trà
Website bán trà, bánh từ trà, gift set + dịch vụ tạo hộp quà, thiết kế riêng, Tea DNA.

Chạy trong PyCharm:   Run 'app.py'   →  mở http://127.0.0.1:8000
(Dùng cổng 8000 vì macOS chiếm cổng 5000 cho AirPlay.)
"""
import json
import os
import random
import re
import sqlite3
import string
import time
import uuid
from datetime import datetime, timedelta

from flask import (Flask, abort, g, jsonify, redirect, render_template, request,
                   session, url_for)
from werkzeug.utils import secure_filename

import data as D

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "trongvitra_v2.db")
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "trong-vi-tra-dev-key")
app.config["MAX_CONTENT_LENGTH"] = 32 * 1024 * 1024
ALLOWED_EXT = {"jpg", "jpeg", "png", "pdf"}

# ------------------------------------------------------------------
# Tra cứu nhanh sản phẩm
# ------------------------------------------------------------------
ALL_ITEMS = D.PRODUCTS + D.ADDONS
BY_ID = {p["id"]: p for p in ALL_ITEMS}
BY_SLUG = {p["slug"]: p for p in ALL_ITEMS}
BY_SKU = {}
for _p in ALL_ITEMS:
    for _v in _p["variants"]:
        BY_SKU[_v["sku"]] = (_p, _v)
BOX = {b["id"]: b for b in D.BOXES}
PAPER = {p["id"]: p for p in D.PAPERS}
CARD = {c["id"]: c for c in D.CARDS}
ACC = {a["id"]: a for a in D.ACCESSORIES}


def product_url(p):
    if p["type"] == "addon":
        return url_for("cart_page")
    return url_for("product_detail", cat=D.TYPE_ROUTE[p["type"]], slug=p["slug"])


def min_price(p):
    return min(v["price"] for v in p["variants"])


def in_stock(p):
    return any(v["stock"] > 0 for v in p["variants"])


def vnd(n):
    try:
        return f"{int(round(n)):,}".replace(",", ".") + "đ"
    except (TypeError, ValueError):
        return "—"


app.jinja_env.filters["vnd"] = vnd
app.jinja_env.globals.update(product_url=product_url, min_price=min_price, in_stock=in_stock, D=D, BY_ID=BY_ID)


@app.template_filter("vndate")
def vndate(s):
    try:
        return datetime.strptime(s, "%Y-%m-%d").strftime("%d/%m/%Y")
    except Exception:
        return s


@app.template_filter("mask_phone")
def mask_phone(s):
    s = s or ""
    return s[:3] + "****" + s[-3:] if len(s) >= 7 else s


@app.template_filter("mask_email")
def mask_email(s):
    if not s or "@" not in s:
        return s or ""
    a, b = s.split("@", 1)
    return a[:2] + "***@" + b


# ------------------------------------------------------------------
# DATABASE
# ------------------------------------------------------------------
def db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def _close(_e):
    d = g.pop("db", None)
    if d:
        d.close()


def init_db():
    with sqlite3.connect(DB_PATH) as c:
        c.executescript("""
        CREATE TABLE IF NOT EXISTS carts (id TEXT PRIMARY KEY, data TEXT, updated REAL);
        CREATE TABLE IF NOT EXISTS orders (
            code TEXT PRIMARY KEY, token TEXT UNIQUE, created TEXT, data TEXT,
            status_idx INTEGER DEFAULT 0, payment TEXT, history TEXT, total INTEGER,
            phone TEXT, email TEXT);
        CREATE TABLE IF NOT EXISTS design_requests (code TEXT PRIMARY KEY, created TEXT, data TEXT, status TEXT);
        CREATE TABLE IF NOT EXISTS messages (code TEXT PRIMARY KEY, created TEXT, data TEXT, status TEXT);
        CREATE TABLE IF NOT EXISTS tickets (code TEXT PRIMARY KEY, order_code TEXT, created TEXT, data TEXT, status TEXT);
        CREATE TABLE IF NOT EXISTS subscribers (email TEXT PRIMARY KEY, created TEXT, source TEXT);
        """)


def gen_code(prefix, n=6):
    return f"{prefix}-{datetime.now():%y%m%d}-" + "".join(random.choices(string.ascii_uppercase + string.digits, k=n))


def now_str():
    return datetime.now().strftime("%d/%m/%Y %H:%M")


# ------------------------------------------------------------------
# GIỎ HÀNG  (lưu SQLite theo cart_id trong session)
# ------------------------------------------------------------------
def cart_id():
    if "cart_id" not in session:
        session["cart_id"] = uuid.uuid4().hex
        session.permanent = True
    return session["cart_id"]


def load_cart():
    row = db().execute("SELECT data FROM carts WHERE id=?", (cart_id(),)).fetchone()
    cart = json.loads(row["data"]) if row else {}
    cart.setdefault("lines", [])
    cart.setdefault("note", "")
    cart.setdefault("coupon", None)
    cart.setdefault("vat", None)
    return cart


def save_cart(cart):
    db().execute("INSERT OR REPLACE INTO carts(id,data,updated) VALUES (?,?,?)",
                 (cart_id(), json.dumps(cart, ensure_ascii=False), time.time()))
    db().commit()


def giftbox_quote(cfg):
    """Kiểm tra & tính giá một cấu hình hộp quà tự tạo. Trả (result, errors)."""
    errors, items, slots, sub_items, prep = [], [], 0, 0, 0
    for it in cfg.get("items", []):
        ref = BY_SKU.get(it.get("sku"))
        qty = int(it.get("qty", 0) or 0)
        if not ref or qty <= 0 or ref[0]["type"] not in ("tra", "banh"):
            continue
        p, v = ref
        if v["stock"] < qty:
            errors.append(f"{p['name']} ({v['label']}) chỉ còn {v['stock']}.")
        items.append({"sku": v["sku"], "pid": p["id"], "name": p["name"], "variant": v["label"], "qty": qty,
                      "price": v["price"], "type": p["type"]})
        slots += v["slots"] * qty
        sub_items += v["price"] * qty
        prep = max(prep, p.get("prep_days", 0))
    if not items:
        errors.append("Chọn ít nhất một món để tiếp tục.")
    box = BOX.get(cfg.get("box"))
    paper = PAPER.get(cfg.get("paper"))
    card = CARD.get(cfg.get("card"))
    if not box:
        errors.append("Chưa chọn hộp.")
    else:
        if slots > box["capacity"]:
            errors.append(f"Các món đã chọn cần {slots} ô, vượt sức chứa {box['capacity']} ô của {box['name']}.")
        if box["stock"] <= 0:
            errors.append(f"{box['name']} đang tạm hết.")
        prep = max(prep, box["prep_days"])
    if not paper:
        errors.append("Chưa chọn giấy gói (hoặc chọn \"Không thêm giấy gói\").")
    else:
        if box and box["id"] not in paper["fits"]:
            errors.append(f"{paper['name']} không dùng được cho {box['name']}.")
        if paper["stock"] <= 0:
            errors.append(f"{paper['name']} đang tạm hết.")
        prep = max(prep, paper["prep_days"])
    if not card:
        errors.append("Chưa chọn thiệp (hoặc chọn \"Không dùng thiệp\").")
    accs, sub_acc = [], 0
    for aid, q in (cfg.get("accessories") or {}).items():
        a = ACC.get(aid)
        q = int(q or 0)
        if not a or q <= 0:
            continue
        if a["stock"] <= 0:
            errors.append(f"{a['name']} đang tạm hết.")
        if q > a["max"]:
            errors.append(f"{a['name']}: tối đa {a['max']} {a['unit']} mỗi hộp.")
        accs.append({"id": aid, "name": a["name"], "qty": q, "price": a["price"]})
        sub_acc += a["price"] * q
    wish = cfg.get("wish") or {}
    msg = (wish.get("message") or "").strip()
    if card and card["id"] != "CD-NONE":
        if len(msg) > card["max_chars"]:
            errors.append(f"Lời chúc dài {len(msg)} ký tự, vượt {card['max_chars']} ký tự của mẫu thiệp. Vui lòng rút gọn.")
        prep = max(prep, card.get("prep_days", 0))
    else:
        wish = {}
    n_box = max(1, min(50, int(cfg.get("boxes", 1) or 1)))
    for it in items:
        ref = BY_SKU[it["sku"]][1]
        if ref["stock"] < it["qty"] * n_box:
            errors.append(f"Không đủ {it['name']} cho {n_box} hộp (còn {ref['stock']}).")
    unit = sub_items + (box["price"] if box else 0) + (paper["price"] if paper else 0) + \
        (card["price"] if card else 0) + sub_acc
    res = {
        "items": items, "slots": slots, "box": box, "paper": paper, "card": card, "accessories": accs,
        "wish": {"to": (wish.get("to") or "").strip()[:60], "message": msg if wish else "",
                 "from": (wish.get("from") or "").strip()[:60]} if wish else {},
        "breakdown": {"items": sub_items, "box": box["price"] if box else 0, "paper": paper["price"] if paper else 0,
                      "card": card["price"] if card else 0, "accessories": sub_acc},
        "unit_price": unit, "boxes": n_box, "total": unit * n_box,
        "prep_days": prep + D.GIFTBOX_PACKING_DAYS,
    }
    return res, errors


def cart_view(cart, province=None, method=None):
    """Mở rộng giỏ: tên, giá, cảnh báo; tính tạm tính, giảm giá, phí giao."""
    lines, subtotal, count, issues, has_cake, prep = [], 0, 0, [], False, 0
    for ln in cart["lines"]:
        if ln["kind"] == "giftbox":
            q, errs = giftbox_quote(dict(ln["config"], boxes=ln["qty"]))
            lines.append({**ln, "name": "Hộp quà tự tạo", "unit_price": q["unit_price"], "total": q["total"],
                          "quote": q, "errors": errs, "url": url_for("giftbox_page")})
            subtotal += q["total"]
            count += ln["qty"]
            has_cake = has_cake or any(i["type"] == "banh" for i in q["items"])
            prep = max(prep, q["prep_days"])
            if errs:
                issues.append("Hộp quà tự tạo: " + errs[0])
            continue
        ref = BY_SKU.get(ln["sku"])
        if not ref:
            continue
        p, v = ref
        err = None
        if v["stock"] <= 0:
            err = "Tạm hết hàng – vui lòng xóa hoặc đổi phân loại."
        elif ln["qty"] > v["stock"]:
            err = f"Chỉ còn {v['stock']} sản phẩm."
        extra = 0
        opts = ln.get("opts") or {}
        if opts.get("card") and opts["card"] in CARD:
            extra = CARD[opts["card"]]["price"]
        unit = v["price"] + extra
        lines.append({**ln, "name": p["name"], "variant": v["label"], "product": p, "variants": p["variants"],
                      "unit_price": unit, "total": unit * ln["qty"], "errors": [err] if err else [], "url": product_url(p)})
        if err:
            issues.append(f"{p['name']}: {err}")
        subtotal += unit * ln["qty"]
        count += ln["qty"]
        if p["type"] == "banh" or (p["type"] == "gift" and any(BY_ID[i[0]]["type"] == "banh" for i in p.get("items", []))):
            has_cake = True
        prep = max(prep, p.get("prep_days", 0))
    # giảm giá
    discount, coupon_msg = 0, None
    cp = cart.get("coupon")
    if cp and cp in D.COUPONS:
        c = D.COUPONS[cp]
        if subtotal >= c["min"]:
            discount = subtotal * c["value"] // 100 if c["type"] == "percent" else c["value"]
        else:
            coupon_msg = f"Mã {cp} áp dụng cho đơn từ {vnd(c['min'])}."
    # phí giao
    ship, ship_options = None, []
    if province:
        for mid, m in D.SHIPPING_METHODS.items():
            ok = m["zones"] is None or province in m["zones"]
            reason = None if ok else "Không hỗ trợ khu vực này"
            if ok and has_cake and province not in D.CAKE_ZONE:
                ok, reason = False, "Đơn có bánh tươi chỉ giao trong khu vực được hỗ trợ"
            fee = m["fee"].get(province, m["fee"].get("_default"))
            if mid == "standard" and subtotal - discount >= D.FREESHIP_THRESHOLD:
                fee = 0
            eta_from = datetime.now() + timedelta(days=prep + m["days"][0])
            eta_to = datetime.now() + timedelta(days=prep + m["days"][1])
            ship_options.append({"id": mid, "label": m["label"], "desc": m["desc"], "fee": fee, "ok": ok,
                                 "reason": reason, "eta": f"{eta_from:%d/%m} – {eta_to:%d/%m}"})
        sel = next((o for o in ship_options if o["id"] == method and o["ok"]), None)
        ship = sel["fee"] if sel else None
    total = subtotal - discount + (ship or 0)
    return {"lines": lines, "count": count, "subtotal": subtotal, "discount": discount, "coupon": cp,
            "coupon_msg": coupon_msg, "ship": ship, "ship_options": ship_options, "total": total,
            "issues": issues, "has_cake": has_cake, "prep_days": prep,
            "freeship_left": max(0, D.FREESHIP_THRESHOLD - (subtotal - discount))}


def cart_count():
    try:
        return sum(l["qty"] for l in load_cart()["lines"])
    except Exception:
        return 0


@app.context_processor
def inject():
    return {"SITE": D.SITE, "cart_count": cart_count(), "year": datetime.now().year, "endpoint": request.endpoint}


# ------------------------------------------------------------------
# TRANG CHỦ & GIỚI THIỆU
# ------------------------------------------------------------------
@app.route("/")
def home():
    prods = [p for p in D.PRODUCTS]
    tabs = {
        "ban-chay": sorted(prods, key=lambda p: p["rank"])[:8],
        "tra": [p for p in prods if p["type"] == "tra"],
        "banh": [p for p in prods if p["type"] == "banh"],
        "gift": [p for p in prods if p["type"] == "gift"],
    }
    arts = sorted(D.ARTICLES, key=lambda a: a["date"], reverse=True)
    feat = next((a for a in arts if a["featured"]), arts[0])
    others = [a for a in arts if a is not feat][:3]
    return render_template("index.html", tabs=tabs, feat=feat, others=others)


@app.route("/ve-hang-son-dien")
def about():
    return render_template("about.html")


# ------------------------------------------------------------------
# SẢN PHẨM
# ------------------------------------------------------------------
@app.route("/san-pham")
@app.route("/san-pham/<cat>")
def catalog(cat=None):
    if cat and cat not in D.ROUTE_TYPE:
        abort(404)
    a = request.args
    loai = D.ROUTE_TYPE.get(cat) if cat else a.get("loai")
    q = (a.get("q") or "").strip()
    gia = a.getlist("gia")
    dip = a.getlist("dip")
    nhom = a.getlist("nhom")
    vi = a.getlist("vi")
    tranh = a.getlist("tranh")          # bánh: tránh chất dị ứng
    con_hang = a.get("con-hang") == "1"
    goi_y = a.get("goi-y")
    sort = a.get("sap-xep", "pho-bien")

    items = [p for p in D.PRODUCTS]
    if loai in D.TYPE_LABEL:
        items = [p for p in items if p["type"] == loai]
    if goi_y == "pairing":
        items = [p for p in items if p["type"] in ("tra", "banh")]
    if q:
        ql = strip_accents(q.lower())
        items = [p for p in items if ql in strip_accents((p["name"] + " " + p.get("taste_note", "") + " " +
                                                          p.get("line", "")).lower())]
    if gia:
        items = [p for p in items if any(D.PRICE_RANGES[x][1] <= min_price(p) < D.PRICE_RANGES[x][2]
                                         for x in gia if x in D.PRICE_RANGES)]
    if dip:
        items = [p for p in items if set(dip) & set(p.get("occasions", []))]
    if nhom:
        items = [p for p in items if p.get("group") in nhom]
    if vi:
        items = [p for p in items if set(vi) & set(p.get("flavor", []))]
    if tranh:
        def has_allergen(p, key):
            al = " ".join(p.get("allergens", [])).lower()
            return {"gluten": "gluten", "sua": "sữa", "trung": "trứng", "hat": "hạt"}[key] in al
        items = [p for p in items if not any(has_allergen(p, k) for k in tranh)]
    if con_hang:
        items = [p for p in items if in_stock(p)]
    if sort == "gia-tang":
        items.sort(key=min_price)
    elif sort == "gia-giam":
        items.sort(key=min_price, reverse=True)
    elif sort == "moi-nhat":
        items.sort(key=lambda p: (not p.get("new"), p["rank"]))
    else:
        items.sort(key=lambda p: (p["type"] != "tra", p["rank"]) if not loai else p["rank"])
    counts = {k: sum(1 for p in D.PRODUCTS if p["type"] == k) for k in D.TYPE_LABEL}
    chips = []
    for key, label_map in (("gia", {k: v[0] for k, v in D.PRICE_RANGES.items()}), ("dip", D.OCCASIONS),
                           ("nhom", D.TEA_GROUPS), ("vi", D.FLAVORS),
                           ("tranh", {"gluten": "Không gluten", "sua": "Không sữa", "trung": "Không trứng", "hat": "Không hạt"})):
        for v in a.getlist(key):
            if v in label_map:
                args = request.args.to_dict(flat=False)
                args[key] = [x for x in args[key] if x != v]
                chips.append((label_map[v], url_for("catalog", cat=cat, **args)))
    if con_hang:
        args = request.args.to_dict(flat=False)
        args.pop("con-hang", None)
        chips.append(("Còn hàng", url_for("catalog", cat=cat, **args)))
    return render_template("catalog.html", items=items, cat=cat, loai=loai, q=q, sel=a, counts=counts,
                           chips=chips, sort=sort, goi_y=goi_y)


def strip_accents(s):
    import unicodedata
    s = s.replace("đ", "d").replace("Đ", "D")
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")


@app.route("/san-pham/<cat>/<slug>")
def product_detail(cat, slug):
    p = BY_SLUG.get(slug)
    if not p or p["type"] == "addon" or D.TYPE_ROUTE[p["type"]] != cat:
        abort(404)
    pairs = [BY_ID[x] for x in p.get("pair", []) if x in BY_ID]
    if p["type"] == "tra":
        sets = [s for s in D.PRODUCTS if s["type"] == "gift" and any(i[0] == p["id"] for i in s["items"])]
        return render_template("product_tea.html", p=p, pairs=pairs, sets=sets)
    if p["type"] == "banh":
        sets = [s for s in D.PRODUCTS if s["type"] == "gift" and any(i[0] == p["id"] for i in s["items"])]
        tea_used = BY_ID.get(p.get("tea_used"))
        return render_template("product_cake.html", p=p, pairs=pairs, sets=sets, tea_used=tea_used)
    contents = [(BY_ID[pid], BY_ID[pid]["variants"][vi], qty) for pid, vi, qty in p["items"]]
    shelf = min(((c[0].get("hsd") or "") for c in contents if c[0]["type"] == "banh"), default="", key=len)
    similar = [s for s in D.PRODUCTS if s["type"] == "gift" and s["id"] != p["id"] and in_stock(s)][:3]
    prep = max([p["prep_days"]] + [c[0].get("prep_days", 0) for c in contents])
    return render_template("product_gift.html", p=p, contents=contents, similar=similar, prep=prep,
                           cake_hsd=[c for c in contents if c[0]["type"] == "banh"])


# ------------------------------------------------------------------
# API GIỎ HÀNG
# ------------------------------------------------------------------
def cart_json(cart):
    v = cart_view(cart)
    return {"count": v["count"], "subtotal": v["subtotal"], "discount": v["discount"], "total": v["total"],
            "freeship_left": v["freeship_left"], "coupon": v["coupon"], "coupon_msg": v["coupon_msg"],
            "lines": [{"key": l["key"], "qty": l["qty"], "total": l["total"], "unit": l["unit_price"],
                       "errors": l["errors"]} for l in v["lines"]],
            "skus": [l.get("sku") for l in cart["lines"] if l.get("sku")]}


@app.post("/api/cart/add")
def api_cart_add():
    d = request.get_json(force=True)
    adds = d.get("items") or [{"sku": d.get("sku"), "qty": d.get("qty", 1), "opts": d.get("opts")}]
    cart = load_cart()
    added = []
    for it in adds:
        ref = BY_SKU.get(it.get("sku"))
        qty = max(1, int(it.get("qty") or 1))
        if not ref:
            return jsonify({"ok": False, "msg": "Không tìm thấy sản phẩm."}), 400
        p, v = ref
        if v["stock"] <= 0:
            return jsonify({"ok": False, "msg": f"{p['name']} ({v['label']}) đang tạm hết."}), 400
        opts = it.get("opts") or None
        if opts:
            msg = (opts.get("message") or "").strip()
            cd = CARD.get(opts.get("card"))
            if cd and cd["id"] != "CD-NONE" and len(msg) > cd["max_chars"]:
                return jsonify({"ok": False, "msg": f"Lời chúc tối đa {cd['max_chars']} ký tự."}), 400
            opts = {"card": cd["id"] if cd and cd["id"] != "CD-NONE" else None,
                    "message": msg if cd and cd["id"] != "CD-NONE" else ""}
            if not opts["card"]:
                opts = None
        same = next((l for l in cart["lines"] if l["kind"] == "product" and l["sku"] == v["sku"]
                     and (l.get("opts") or None) == opts), None)
        cur = same["qty"] if same else 0
        if cur + qty > v["stock"]:
            return jsonify({"ok": False, "msg": f"Chỉ còn {v['stock']} {p['name']} ({v['label']})."}), 400
        if same:
            same["qty"] += qty
        else:
            cart["lines"].append({"key": uuid.uuid4().hex[:10], "kind": "product", "sku": v["sku"], "qty": qty, "opts": opts})
        added.append(f"{p['name']} ({v['label']}) × {qty}")
    save_cart(cart)
    return jsonify({"ok": True, "msg": "Đã thêm " + ", ".join(added), "cart": cart_json(cart)})


@app.post("/api/cart/update")
def api_cart_update():
    d = request.get_json(force=True)
    cart = load_cart()
    ln = next((l for l in cart["lines"] if l["key"] == d.get("key")), None)
    if not ln:
        return jsonify({"ok": False, "msg": "Dòng hàng không còn trong giỏ."}), 404
    if "sku" in d and ln["kind"] == "product":
        new = BY_SKU.get(d["sku"])
        if new and new[0]["id"] == BY_SKU[ln["sku"]][0]["id"]:
            ln["sku"] = d["sku"]
    if "qty" in d:
        q = int(d["qty"])
        if q <= 0:
            cart["lines"].remove(ln)
        else:
            if ln["kind"] == "product":
                stock = BY_SKU[ln["sku"]][1]["stock"]
                if q > stock:
                    save_cart(cart)
                    return jsonify({"ok": False, "msg": f"Chỉ còn {stock} sản phẩm.", "cart": cart_json(cart)}), 400
            ln["qty"] = q
    save_cart(cart)
    return jsonify({"ok": True, "cart": cart_json(cart)})


@app.post("/api/cart/remove")
def api_cart_remove():
    key = request.get_json(force=True).get("key")
    cart = load_cart()
    cart["lines"] = [l for l in cart["lines"] if l["key"] != key]
    save_cart(cart)
    return jsonify({"ok": True, "cart": cart_json(cart)})


@app.post("/api/cart/coupon")
def api_coupon():
    code = (request.get_json(force=True).get("code") or "").strip().upper()
    cart = load_cart()
    if not code:
        cart["coupon"] = None
        save_cart(cart)
        return jsonify({"ok": True, "msg": "Đã bỏ mã giảm giá.", "cart": cart_json(cart)})
    if code not in D.COUPONS:
        return jsonify({"ok": False, "msg": "Mã giảm giá không hợp lệ hoặc đã hết hạn."}), 400
    sub = cart_view(cart)["subtotal"]
    if sub < D.COUPONS[code]["min"]:
        return jsonify({"ok": False, "msg": f"Mã {code} áp dụng cho đơn từ {vnd(D.COUPONS[code]['min'])}."}), 400
    cart["coupon"] = code
    save_cart(cart)
    return jsonify({"ok": True, "msg": f"Đã áp dụng: {D.COUPONS[code]['label']}", "cart": cart_json(cart)})


@app.post("/api/cart/meta")
def api_cart_meta():
    d = request.get_json(force=True)
    cart = load_cart()
    if "note" in d:
        cart["note"] = (d["note"] or "")[:500]
    if "vat" in d:
        cart["vat"] = d["vat"]
    save_cart(cart)
    return jsonify({"ok": True})


@app.get("/api/cart")
def api_cart():
    return jsonify(cart_json(load_cart()))


@app.post("/api/giftbox/add")
def api_giftbox_add():
    d = request.get_json(force=True)
    cfg = d.get("config") or {}
    req_id = d.get("request_id")
    cart = load_cart()
    if req_id and any(l.get("request_id") == req_id for l in cart["lines"]):   # chống gửi trùng
        return jsonify({"ok": True, "duplicate": True, "msg": "Hộp quà đã có trong giỏ.", "cart": cart_json(cart)})
    q, errs = giftbox_quote(cfg)
    if errs:
        return jsonify({"ok": False, "msg": errs[0], "errors": errs}), 400
    clean = {"items": [{"sku": i["sku"], "qty": i["qty"]} for i in q["items"]], "box": q["box"]["id"],
             "paper": q["paper"]["id"], "card": q["card"]["id"],
             "accessories": {a["id"]: a["qty"] for a in q["accessories"]}, "wish": q["wish"]}
    cart["lines"].append({"key": uuid.uuid4().hex[:10], "kind": "giftbox", "config": clean, "qty": q["boxes"],
                          "request_id": req_id, "snapshot_price": q["unit_price"]})
    save_cart(cart)
    return jsonify({"ok": True, "msg": "Đã thêm hộp quà vào giỏ", "cart": cart_json(cart)})


@app.post("/api/newsletter")
def api_newsletter():
    d = request.get_json(force=True)
    email = (d.get("email") or "").strip().lower()
    if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
        return jsonify({"ok": False, "msg": "Email chưa đúng định dạng, vui lòng kiểm tra lại."}), 400
    try:
        db().execute("INSERT INTO subscribers VALUES (?,?,?)", (email, now_str(), d.get("source", "")))
        db().commit()
    except sqlite3.IntegrityError:
        return jsonify({"ok": True, "msg": "Email này đã đăng ký rồi. Cảm ơn bạn!"})
    return jsonify({"ok": True, "msg": "Đăng ký thành công! Hẹn gặp bạn trong những câu chuyện trà sắp tới."})


# ------------------------------------------------------------------
# DỊCH VỤ
# ------------------------------------------------------------------
@app.route("/dich-vu/tao-hop-qua")
def giftbox_page():
    pool = [p for p in D.PRODUCTS if p["type"] in ("tra", "banh")]
    bx = {"products": [{**{k: p[k] for k in ("id", "name", "type", "taste_note", "color", "art")},
                        "brand": p.get("brand"), "url": product_url(p), "allergens": p.get("allergens", []),
                        "prep_days": p.get("prep_days", 0), "hsd": p.get("hsd", ""), "storage": p.get("storage", ""),
                        "desc": p.get("desc", ""), "variants": p["variants"]} for p in pool],
          "boxes": D.BOXES, "papers": D.PAPERS, "cards": D.CARDS, "accessories": D.ACCESSORIES,
          "wishes": D.WISH_SAMPLES, "packing_days": D.GIFTBOX_PACKING_DAYS}
    pre = request.args.get("sku")
    if pre and pre not in BY_SKU:
        p = BY_SLUG.get(pre) or BY_ID.get(pre)
        pre = p["variants"][0]["sku"] if p and p["type"] in ("tra", "banh") else None
    faq = [f for f in D.FAQS if f[0] == "qua"]
    return render_template("giftbox.html", bx=bx, preselect=pre, faq=faq)


@app.route("/dich-vu/thiet-ke-rieng", methods=["GET", "POST"])
def custom_design():
    done, errors, form = None, {}, {}
    if request.method == "POST":
        form = request.form.to_dict()
        req = ["name", "phone", "need", "quantity", "deadline", "description"]
        for k in req:
            if not form.get(k, "").strip():
                errors[k] = "Vui lòng điền thông tin này."
        if form.get("email") and not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", form["email"]):
            errors["email"] = "Email chưa đúng định dạng."
        if form.get("phone") and not re.match(r"^[0-9 +().-]{9,15}$", form["phone"]):
            errors["phone"] = "Số điện thoại chưa đúng định dạng."
        if not form.get("agree"):
            errors["agree"] = "Vui lòng xác nhận đã đọc thông tin sử dụng dữ liệu."
        files = [f for f in request.files.getlist("files") if f and f.filename]
        if len(files) > 3:
            errors["files"] = "Tối đa 3 tệp."
        for f in files:
            ext = f.filename.rsplit(".", 1)[-1].lower()
            if ext not in ALLOWED_EXT:
                errors["files"] = "Chỉ nhận JPG, PNG hoặc PDF."
        if not errors:
            code = gen_code("YC", 4)
            saved = []
            for f in files:
                fn = f"{code}_{secure_filename(f.filename)}"
                f.save(os.path.join(UPLOAD_DIR, fn))
                saved.append(fn)
            form.pop("agree", None)
            form["files"] = saved
            db().execute("INSERT INTO design_requests VALUES (?,?,?,?)",
                         (code, now_str(), json.dumps(form, ensure_ascii=False), "Chờ tiếp nhận"))
            if form.get("marketing") and form.get("email"):
                try:
                    db().execute("INSERT INTO subscribers VALUES (?,?,?)", (form["email"], now_str(), "design"))
                except sqlite3.IntegrityError:
                    pass
            db().commit()
            done = {"code": code, "name": form["name"], "channel": form.get("channel", "phone"),
                    "contact": form.get("email") if form.get("channel") == "email" else form.get("phone"),
                    "created": now_str()}
    ref = request.args.get("tham-chieu")
    return render_template("custom_design.html", done=done, errors=errors, form=form, ref=ref)


# ------------------------------------------------------------------
# CHUYỆN TRÀ
# ------------------------------------------------------------------
@app.route("/chuyen-tra")
def stories():
    arts = sorted(D.ARTICLES, key=lambda a: a["date"], reverse=True)
    feat = next((a for a in arts if a["featured"]), arts[0])
    rest = [a for a in arts if a is not feat]
    feature_prods = [p for p in sorted(D.PRODUCTS, key=lambda p: p["rank"]) if in_stock(p) and p["type"] != "gift"][:3]
    return render_template("stories.html", feat=feat, rest=rest, feature_prods=feature_prods)


@app.route("/chuyen-tra/<slug>")
def article(slug):
    a = next((x for x in D.ARTICLES if x["slug"] == slug), None)
    if not a:
        abort(404)
    words = sum(len(t.split()) for k, t in a["body"] if k != "product")
    toc = [(f"muc-{i}", t) for i, (k, t) in enumerate(a["body"]) if k == "h2"] if words >= 300 else []
    related = [x for x in D.ARTICLES if x is not a and (x["cat"] == a["cat"] or set(x["tags"]) & set(a["tags"]))][:3]
    if not related:
        related = [x for x in D.ARTICLES if x is not a][:2]
    return render_template("article.html", a=a, toc=toc, related=related, words=words)


# ------------------------------------------------------------------
# TEA DNA
# ------------------------------------------------------------------
def dna_payload():
    from flask import get_template_attribute
    art = get_template_attribute("macros.html", "art")
    prods = [{"art_html": str(art(p["art"], p["color"], p["name"], note=False)),"id": p["id"], "name": p["name"], "type": p["type"], "url": product_url(p), "dna": p["dna"],
              "avoid": p.get("avoid", []), "allergens": p.get("allergens", []), "price": min_price(p),
              "sku": next((v["sku"] for v in p["variants"] if v["stock"] > 0), None), "stock": in_stock(p),
              "taste": p.get("taste_note", ""), "color": p.get("color"), "art": p.get("art")}
             for p in D.PRODUCTS]
    for r in D.DNA_RECIPES:
        r["tea_url"] = product_url(BY_ID[r["tea"]]) if r.get("tea") else None
        r["tea_name"] = BY_ID[r["tea"]]["name"] if r.get("tea") else None
    return {"questions": D.DNA_QUESTIONS, "axes": D.DNA_AXES, "groups": D.DNA_GROUPS,
            "recipes": D.DNA_RECIPES, "products": prods, "version": 2}


@app.route("/tea-dna")
def tea_dna():
    return render_template("tea_dna.html", dna=dna_payload())


@app.route("/tea-dna/ket-qua")
def tea_dna_result():
    return render_template("tea_dna_result.html", dna=dna_payload())


# ------------------------------------------------------------------
# GIỎ HÀNG & THANH TOÁN
# ------------------------------------------------------------------
@app.route("/gio-hang")
def cart_page():
    cart = load_cart()
    v = cart_view(cart)
    in_cart = {l.get("sku") for l in cart["lines"]}
    addons = [a for a in D.ADDONS if a["variants"][0]["sku"] not in in_cart]
    return render_template("cart.html", v=v, cart=cart, addons=addons)


def validate_checkout(f, v):
    e = {}
    if not f.get("buyer_name", "").strip():
        e["buyer_name"] = "Vui lòng nhập họ tên người đặt."
    if not re.match(r"^(0|\+84)[0-9]{9,10}$", f.get("buyer_phone", "").replace(" ", "")):
        e["buyer_phone"] = "Số điện thoại cần 10 số, bắt đầu bằng 0 (vd 0901234567)."
    if f.get("buyer_email") and not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", f["buyer_email"]):
        e["buyer_email"] = "Email chưa đúng định dạng."
    if not f.get("same_recipient"):
        if not f.get("rcv_name", "").strip():
            e["rcv_name"] = "Vui lòng nhập tên người nhận."
        if not re.match(r"^(0|\+84)[0-9]{9,10}$", f.get("rcv_phone", "").replace(" ", "")):
            e["rcv_phone"] = "Số điện thoại người nhận chưa đúng."
    if f.get("province") not in D.PROVINCES:
        e["province"] = "Chọn tỉnh/thành phố."
    if not f.get("district", "").strip():
        e["district"] = "Nhập quận/huyện, phường/xã."
    if not f.get("street", "").strip():
        e["street"] = "Nhập số nhà, tên đường."
    opt = next((o for o in v["ship_options"] if o["id"] == f.get("ship")), None)
    if not opt or not opt["ok"]:
        e["ship"] = "Chọn phương thức giao hàng khả dụng."
    pm = f.get("payment")
    if pm not in D.PAYMENT_METHODS:
        e["payment"] = "Chọn cách thanh toán."
    elif pm == "cod" and v["total"] > D.COD_LIMIT:
        e["payment"] = f"COD chỉ áp dụng cho đơn đến {vnd(D.COD_LIMIT)}."
    if f.get("invoice") and not f.get("tax_code", "").strip():
        e["tax_code"] = "Nhập mã số thuế để xuất hóa đơn."
    if not f.get("agree"):
        e["agree"] = "Vui lòng đồng ý với điều kiện mua hàng."
    if v["issues"]:
        e["_cart"] = "Giỏ hàng có sản phẩm cần xử lý: " + v["issues"][0]
    return e


@app.route("/thanh-toan", methods=["GET", "POST"])
def checkout():
    cart = load_cart()
    if request.method == "POST":                       # chống tạo đơn trùng (bấm 2 lần / F5)
        existing = db().execute("SELECT code FROM orders WHERE token=?", (request.form.get("token"),)).fetchone()
        if existing:
            return redirect(url_for("order_result", code=existing["code"]))
    if not cart["lines"]:
        return render_template("checkout.html", empty=True)
    f = request.form.to_dict() if request.method == "POST" else {"same_recipient": "1", "province": "", "ship": "standard"}
    if request.method == "GET" and cart.get("vat"):
        f.update({"invoice": "1", **{k: cart["vat"].get(k, "") for k in ("tax_code", "company", "company_addr")}})
    v = cart_view(cart, f.get("province"), f.get("ship"))
    errors = {}
    if request.method == "POST":
        token = f.get("token")
        existing = db().execute("SELECT code FROM orders WHERE token=?", (token,)).fetchone()
        if existing:                                   # chống tạo đơn trùng
            return redirect(url_for("order_result", code=existing["code"]))
        errors = validate_checkout(f, v)
        if not errors:
            code = gen_code("TVT", 5)
            snap = {"lines": [], "buyer": {k: f.get(k, "") for k in ("buyer_name", "buyer_phone", "buyer_email")},
                    "recipient": ({"name": f["buyer_name"], "phone": f["buyer_phone"]} if f.get("same_recipient")
                                  else {"name": f["rcv_name"], "phone": f["rcv_phone"]}),
                    "address": {k: f.get(k, "") for k in ("province", "district", "street", "addr_note")},
                    "ship": next(o for o in v["ship_options"] if o["id"] == f["ship"]),
                    "payment": f["payment"], "note": cart.get("note", ""), "delivery_note": f.get("delivery_note", ""),
                    "wish_date": f.get("wish_date", ""), "hide_price": bool(f.get("hide_price")),
                    "invoice": ({k: f.get(k, "") for k in ("tax_code", "company", "company_addr", "invoice_email")}
                                if f.get("invoice") else None),
                    "subtotal": v["subtotal"], "discount": v["discount"], "coupon": v["coupon"],
                    "shipping": v["ship"], "total": v["total"], "prep_days": v["prep_days"]}
            for l in v["lines"]:
                if l["kind"] == "giftbox":
                    q = l["quote"]
                    snap["lines"].append({"kind": "giftbox", "name": "Hộp quà tự tạo", "qty": l["qty"],
                                          "unit": l["unit_price"], "total": l["total"],
                                          "detail": {"items": q["items"], "box": q["box"]["name"], "paper": q["paper"]["name"],
                                                     "card": q["card"]["name"], "accessories": q["accessories"],
                                                     "wish": q["wish"]}})
                else:
                    snap["lines"].append({"kind": "product", "name": l["name"], "variant": l["variant"], "sku": l["sku"],
                                          "qty": l["qty"], "unit": l["unit_price"], "total": l["total"],
                                          "opts": l.get("opts"),
                                          "card_name": CARD[l["opts"]["card"]]["name"] if l.get("opts") and l["opts"].get("card") else None})
            pay = "cod_pending" if f["payment"] == "cod" else "bank_pending"
            hist = [{"step": 0, "time": now_str()}]
            db().execute("INSERT INTO orders VALUES (?,?,?,?,?,?,?,?,?,?)",
                         (code, token, now_str(), json.dumps(snap, ensure_ascii=False), 0, pay,
                          json.dumps(hist), v["total"], f["buyer_phone"].replace(" ", ""),
                          (f.get("buyer_email") or "").lower()))
            if f.get("marketing") and f.get("buyer_email"):
                try:
                    db().execute("INSERT INTO subscribers VALUES (?,?,?)", (f["buyer_email"].lower(), now_str(), "checkout"))
                except sqlite3.IntegrityError:
                    pass
            db().commit()
            cart.update({"lines": [], "coupon": None, "note": "", "vat": None})
            save_cart(cart)
            session.setdefault("my_orders", [])
            session["my_orders"] = (session["my_orders"] + [code])[-20:]
            return redirect(url_for("order_result", code=code))
    return render_template("checkout.html", empty=False, v=v, f=f, errors=errors, cart=cart,
                           token=f.get("token") or uuid.uuid4().hex)


@app.post("/api/checkout/quote")
def api_checkout_quote():
    d = request.get_json(force=True)
    v = cart_view(load_cart(), d.get("province"), d.get("ship"))
    return jsonify({"ship_options": v["ship_options"], "ship": v["ship"], "subtotal": v["subtotal"],
                    "discount": v["discount"], "total": v["total"], "cod_ok": v["total"] <= D.COD_LIMIT})


def get_order(code):
    r = db().execute("SELECT * FROM orders WHERE code=?", (code,)).fetchone()
    if not r:
        return None
    o = dict(r)
    o["data"] = json.loads(o["data"])
    o["history"] = json.loads(o["history"])
    return o


@app.route("/don-hang/<code>")
def order_result(code):
    if code not in session.get("my_orders", []) and code not in session.get("verified", {}):
        return redirect(url_for("track", ma=code))
    o = get_order(code)
    if not o:
        abort(404)
    return render_template("order_result.html", o=o)


@app.post("/don-hang/<code>/da-chuyen-khoan")
def order_paid_claim(code):
    if code not in session.get("my_orders", []) and code not in session.get("verified", {}):
        abort(403)
    o = get_order(code)
    if o and o["payment"] == "bank_pending":
        db().execute("UPDATE orders SET payment='verifying' WHERE code=?", (code,))
        db().commit()
    return redirect(url_for("order_result", code=code))


@app.route("/tra-cuu-don", methods=["GET", "POST"])
def track():
    err, o, f = None, None, {}
    verified = session.get("verified", {})
    code = request.args.get("ma", "").strip().upper()
    if request.method == "POST":
        f = request.form.to_dict()
        code = f.get("code", "").strip().upper()
        contact = f.get("contact", "").strip().lower().replace(" ", "")
        if not code or not contact:
            err = "Vui lòng nhập mã đơn và số điện thoại/email đã dùng khi đặt."
        else:
            r = get_order(code)
            if r and contact in (r["phone"], r["email"]) and contact:
                verified[code] = time.time()
                session["verified"] = verified
                return redirect(url_for("track", ma=code))
            err = "Chưa thể tra cứu với thông tin này. Vui lòng kiểm tra lại mã đơn và thông tin liên hệ."
    if code and (code in verified and time.time() - verified[code] < 1800 or code in session.get("my_orders", [])):
        o = get_order(code)
    tickets = []
    if o:
        tickets = [dict(t) | {"data": json.loads(t["data"])} for t in
                   db().execute("SELECT * FROM tickets WHERE order_code=? ORDER BY created DESC", (o["code"],))]
    return render_template("track.html", o=o, err=err, f=f, code=code, tickets=tickets,
                           ticket_done=request.args.get("yc"))


@app.post("/tra-cuu-don/<code>/ho-tro")
def track_support(code):
    if code not in session.get("verified", {}) and code not in session.get("my_orders", []):
        return redirect(url_for("track", ma=code))
    f = request.form.to_dict()
    if not f.get("kind") or not f.get("desc", "").strip():
        return redirect(url_for("track", ma=code, loi="1") + "#ho-tro")
    dup = db().execute("SELECT code FROM tickets WHERE order_code=? AND data LIKE ? AND status='Chờ tiếp nhận'",
                       (code, f'%"kind": "{f["kind"]}"%')).fetchone()
    tcode = dup["code"] if dup else gen_code("HT", 4)
    if not dup:
        files = [x for x in request.files.getlist("files") if x and x.filename][:3]
        saved = []
        for x in files:
            if x.filename.rsplit(".", 1)[-1].lower() in ALLOWED_EXT:
                fn = f"{tcode}_{secure_filename(x.filename)}"
                x.save(os.path.join(UPLOAD_DIR, fn))
                saved.append(fn)
        f["files"] = saved
        db().execute("INSERT INTO tickets VALUES (?,?,?,?,?)",
                     (tcode, code, now_str(), json.dumps(f, ensure_ascii=False), "Chờ tiếp nhận"))
        db().commit()
    return redirect(url_for("track", ma=code, yc=tcode) + "#ho-tro")


# ------------------------------------------------------------------
# LIÊN HỆ, CHÍNH SÁCH
# ------------------------------------------------------------------
@app.route("/lien-he", methods=["GET", "POST"])
def contact():
    done, errors, f = None, {}, {"topic": request.args.get("chu-de", "")}
    if request.method == "POST":
        f = request.form.to_dict()
        for k in ("name", "topic", "channel", "content"):
            if not f.get(k, "").strip():
                errors[k] = "Vui lòng điền thông tin này."
        ch = f.get("channel")
        if ch == "email" and not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", f.get("email", "")):
            errors["email"] = "Nhập email hợp lệ để nhận phản hồi qua email."
        if ch in ("phone", "zalo") and not re.match(r"^(0|\+84)[0-9]{9,10}$", f.get("phone", "").replace(" ", "")):
            errors["phone"] = "Nhập số điện thoại hợp lệ để nhận phản hồi."
        if not f.get("agree"):
            errors["agree"] = "Vui lòng xác nhận đã đọc thông tin sử dụng dữ liệu."
        files = [x for x in request.files.getlist("files") if x and x.filename]
        if len(files) > 3 or any(x.filename.rsplit(".", 1)[-1].lower() not in ALLOWED_EXT for x in files):
            errors["files"] = "Tối đa 3 tệp JPG, PNG hoặc PDF."
        if not errors:
            code = gen_code("LH", 4)
            saved = []
            for x in files:
                fn = f"{code}_{secure_filename(x.filename)}"
                x.save(os.path.join(UPLOAD_DIR, fn))
                saved.append(fn)
            f["files"] = saved
            f.pop("agree", None)
            db().execute("INSERT INTO messages VALUES (?,?,?,?)", (code, now_str(), json.dumps(f, ensure_ascii=False), "Chờ tiếp nhận"))
            db().commit()
            done = {"code": code, "topic": D.CONTACT_TOPICS.get(f["topic"], f["topic"]), "created": now_str(),
                    "channel": {"email": "Email", "phone": "Điện thoại", "zalo": "Zalo"}.get(ch, ch),
                    "contact": f.get("email") if ch == "email" else f.get("phone")}
    return render_template("contact.html", done=done, errors=errors, f=f)


@app.route("/chinh-sach/<slug>")
def policy(slug):
    p = D.POLICIES.get(slug)
    if not p:
        abort(404)
    return render_template("policy.html", p=p, slug=slug)


# ------------------------------------------------------------------
# QUẢN TRỊ (demo – chưa có đăng nhập)
# ------------------------------------------------------------------

# Bảo vệ trang quản trị bằng mật khẩu khi đưa lên mạng (biến môi trường ADMIN_PASSWORD)
@app.before_request
def _admin_guard():
    pw = os.environ.get("ADMIN_PASSWORD")
    if pw and request.path.startswith("/admin"):
        auth = request.authorization
        if not auth or auth.password != pw:
            from flask import Response
            return Response("Cần đăng nhập quản trị", 401, {"WWW-Authenticate": 'Basic realm="Admin"'})

@app.route("/admin")
def admin():
    orders = [get_order(r["code"]) for r in db().execute("SELECT code FROM orders ORDER BY created DESC")]
    def rows(t):
        return [dict(r) | {"data": json.loads(r["data"])} for r in db().execute(f"SELECT * FROM {t} ORDER BY created DESC")]
    subs = [dict(r) for r in db().execute("SELECT * FROM subscribers ORDER BY created DESC")]
    return render_template("admin.html", orders=orders, designs=rows("design_requests"), msgs=rows("messages"),
                           tickets=rows("tickets"), subs=subs)


@app.post("/admin/don/<code>")
def admin_order(code):
    o = get_order(code)
    if not o:
        abort(404)
    act = request.form.get("act")
    if act == "next" and o["status_idx"] < len(D.ORDER_STEPS) - 1:
        o["history"].append({"step": o["status_idx"] + 1, "time": now_str()})
        db().execute("UPDATE orders SET status_idx=?, history=? WHERE code=?",
                     (o["status_idx"] + 1, json.dumps(o["history"]), code))
    elif act in D.PAYMENT_STATUS:
        db().execute("UPDATE orders SET payment=? WHERE code=?", (act, code))
    db().commit()
    return redirect(url_for("admin") + "#don")


@app.errorhandler(404)
def nf(_e):
    return render_template("404.html"), 404


@app.errorhandler(413)
def too_big(_e):
    return render_template("404.html", msg="Tệp tải lên quá lớn (tối đa 10 MB mỗi tệp)."), 413


init_db()

if __name__ == "__main__":
    app.run(debug=True, port=int(os.environ.get("PORT", 8000)))
