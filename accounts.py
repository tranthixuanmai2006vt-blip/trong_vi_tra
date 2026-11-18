# -*- coding: utf-8 -*-
"""
TÀI KHOẢN THÀNH VIÊN – đăng ký / đăng nhập (không bắt buộc), lịch sử mua hàng,
tích điểm, hạng thành viên và đổi điểm lấy voucher.

Khách vẫn mua được mà không cần tài khoản. Khi đã đăng nhập:
  • Mỗi đơn được gắn vào tài khoản, điểm ở trạng thái "chờ cộng".
  • Điểm được cộng khi đơn chuyển sang "Đã giao" (admin bấm bước cuối).
  • Tổng chi tiêu của đơn đã giao quyết định hạng; lên hạng được tặng voucher.
  • Điểm đổi được voucher giảm giá dùng ở giỏ hàng / thanh toán.
Quy tắc nằm trong data.LOYALTY để nhóm chỉnh không cần sửa code.
"""
import json
import random
import re
import string
import time
from datetime import datetime, timedelta
from functools import wraps

from flask import (Blueprint, abort, flash, g, redirect, render_template, request,
                   session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash

import data as D

bp = Blueprint("acc", __name__)
L = D.LOYALTY
_db = None          # gắn từ app.py qua init()
_get_order = None


def init(app, db_func, get_order_func):
    global _db, _get_order
    _db, _get_order = db_func, get_order_func
    app.register_blueprint(bp)
    app.context_processor(lambda: {"current_user": current_user(), "LOYALTY": L, "tier_of": tier_of,
                                   "accounts_vouchers": lambda: user_vouchers(current_user()["id"]) if current_user() else []})


def ensure_schema(c):
    c.executescript("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT, email TEXT UNIQUE NOT NULL, phone TEXT, name TEXT,
        pw TEXT NOT NULL, created TEXT, birthday TEXT, address TEXT,
        points INTEGER DEFAULT 0, spent INTEGER DEFAULT 0, tier TEXT DEFAULT 'mam');
    CREATE TABLE IF NOT EXISTS user_orders (
        order_code TEXT PRIMARY KEY, user_id INTEGER, base INTEGER, points INTEGER, status TEXT);
    CREATE TABLE IF NOT EXISTS points_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, created TEXT, delta INTEGER, note TEXT);
    CREATE TABLE IF NOT EXISTS vouchers (
        code TEXT PRIMARY KEY, user_id INTEGER, created TEXT, value INTEGER, min INTEGER,
        label TEXT, expires TEXT, used_order TEXT);
    """)


# ------------------------------------------------------------------ tiện ích
def vnd(n):
    return f"{int(n):,}".replace(",", ".") + "đ"


def now_str():
    return datetime.now().strftime("%d/%m/%Y %H:%M")


def current_user():
    if "user" not in g:
        uid = session.get("uid")
        row = _db().execute("SELECT * FROM users WHERE id=?", (uid,)).fetchone() if uid else None
        g.user = dict(row) if row else None
        if g.user:
            g.user["address"] = json.loads(g.user["address"] or "{}")
    return g.user


def login_required(f):
    @wraps(f)
    def w(*a, **k):
        if not current_user():
            return redirect(url_for("acc.login", next=request.full_path.rstrip("?")))
        return f(*a, **k)
    return w


def safe_next(n, default="acc.account"):
    return n if n and n.startswith("/") and not n.startswith("//") else url_for(default)


def tier_of(spent):
    t = L["tiers"][0]
    for x in L["tiers"]:
        if spent >= x["min"]:
            t = x
    return t


def next_tier(spent):
    return next((x for x in L["tiers"] if x["min"] > spent), None)


def points_for(base, spent):
    return int(base // L["earn_per"] * tier_of(spent)["mult"])


def _log(uid, delta, note):
    _db().execute("INSERT INTO points_log(user_id,created,delta,note) VALUES (?,?,?,?)", (uid, now_str(), delta, note))


def give_voucher(uid, value, minimum, label, days):
    code = "TVN-" + "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
    exp = (datetime.now() + timedelta(days=days)).strftime("%Y-%m-%d")
    _db().execute("INSERT INTO vouchers VALUES (?,?,?,?,?,?,?,NULL)", (code, uid, now_str(), value, minimum, label, exp))
    return code


def user_vouchers(uid, usable_only=True):
    q = "SELECT * FROM vouchers WHERE user_id=?" + (" AND used_order IS NULL AND expires>=?" if usable_only else "")
    args = (uid, datetime.now().strftime("%Y-%m-%d")) if usable_only else (uid,)
    return [dict(r) for r in _db().execute(q + " ORDER BY expires", args)]


# ------------------------------------------------------------------ móc vào giỏ / đơn
def coupon_def(code):
    """Mã chung (data.COUPONS) hoặc voucher riêng của thành viên đang đăng nhập."""
    if not code:
        return None
    if code in D.COUPONS:
        return D.COUPONS[code]
    u = current_user()
    if not u:
        return None
    r = _db().execute("SELECT * FROM vouchers WHERE code=? AND user_id=? AND used_order IS NULL AND expires>=?",
                      (code, u["id"], datetime.now().strftime("%Y-%m-%d"))).fetchone()
    return {"type": "fixed", "value": r["value"], "min": r["min"], "label": r["label"]} if r else None


def link_order(code, base, coupon):
    """Gọi ngay sau khi tạo đơn: gắn đơn vào tài khoản, khóa voucher đã dùng."""
    u = current_user()
    if not u:
        return
    pts = points_for(base, u["spent"])
    _db().execute("INSERT OR IGNORE INTO user_orders VALUES (?,?,?,?,?)", (code, u["id"], base, pts, "pending"))
    if coupon and coupon not in D.COUPONS:
        _db().execute("UPDATE vouchers SET used_order=? WHERE code=? AND user_id=?", (code, coupon, u["id"]))
    _db().commit()


def owns(code):
    u = current_user()
    return bool(u and _db().execute("SELECT 1 FROM user_orders WHERE order_code=? AND user_id=?", (code, u["id"])).fetchone())


def credit(code):
    """Cộng điểm khi đơn đã giao. Gọi lại nhiều lần cũng chỉ cộng một lần."""
    r = _db().execute("SELECT * FROM user_orders WHERE order_code=? AND status='pending'", (code,)).fetchone()
    if not r:
        return
    u = _db().execute("SELECT * FROM users WHERE id=?", (r["user_id"],)).fetchone()
    if not u:
        return
    old_tier = tier_of(u["spent"])
    spent = u["spent"] + r["base"]
    _db().execute("UPDATE users SET points=points+?, spent=?, tier=? WHERE id=?", (r["points"], spent, tier_of(spent)["id"], u["id"]))
    _db().execute("UPDATE user_orders SET status='credited' WHERE order_code=?", (code,))
    _log(u["id"], r["points"], f"Đơn {code} đã giao")
    new_tier = tier_of(spent)
    if new_tier["id"] != old_tier["id"] and new_tier.get("gift"):
        give_voucher(u["id"], new_tier["gift"], new_tier.get("gift_min", 0), f"Quà lên hạng {new_tier['name']}", L["voucher_days"])
    _db().commit()


def claim_session_orders(uid):
    """Đơn vừa mua trên trình duyệt này (khi chưa đăng nhập) được gắn vào tài khoản."""
    u = dict(_db().execute("SELECT * FROM users WHERE id=?", (uid,)).fetchone())
    for code in session.get("my_orders", []):
        if _db().execute("SELECT 1 FROM user_orders WHERE order_code=?", (code,)).fetchone():
            continue
        o = _get_order(code)
        if not o:
            continue
        base = o["data"]["subtotal"] - o["data"]["discount"]
        _db().execute("INSERT INTO user_orders VALUES (?,?,?,?,?)", (code, uid, base, points_for(base, u["spent"]), "pending"))
        if o["status_idx"] == len(D.ORDER_STEPS) - 1:
            credit(code)
    _db().commit()


# ------------------------------------------------------------------ đăng nhập / đăng ký
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
PHONE_RE = re.compile(r"^(0|\+84)[0-9]{9,10}$")


def _start_session(uid):
    keep = {k: session.get(k) for k in ("cart_id", "my_orders", "verified")}
    session.clear()
    session.update({k: v for k, v in keep.items() if v is not None})
    session["uid"] = uid
    session.permanent = True
    g.pop("user", None)
    claim_session_orders(uid)


@bp.route("/dang-nhap", methods=["GET", "POST"])
def login():
    nxt = request.values.get("next", "")
    if current_user():
        return redirect(safe_next(nxt))
    f, errors = {}, {}
    if request.method == "POST":
        f = request.form.to_dict()
        lock = session.get("login_lock", 0)
        if lock > time.time():
            errors["_"] = f"Bạn nhập sai nhiều lần. Thử lại sau {int(lock - time.time()) + 1} giây."
        else:
            r = _db().execute("SELECT * FROM users WHERE email=?", (f.get("email", "").strip().lower(),)).fetchone()
            if r and check_password_hash(r["pw"], f.get("password", "")):
                session.pop("login_fail", None)
                _start_session(r["id"])
                flash(f"Chào mừng {r['name'].split()[-1]} quay lại!")
                return redirect(safe_next(nxt))
            session["login_fail"] = session.get("login_fail", 0) + 1
            if session["login_fail"] >= 5:
                session["login_lock"], session["login_fail"] = time.time() + 30, 0
            errors["_"] = "Email hoặc mật khẩu chưa đúng."
    return render_template("auth.html", mode="login", f=f, errors=errors, nxt=nxt)


@bp.route("/dang-ky", methods=["GET", "POST"])
def register():
    nxt = request.values.get("next", "")
    if current_user():
        return redirect(safe_next(nxt))
    f, errors = {}, {}
    if request.method == "POST":
        f = request.form.to_dict()
        email = f.get("email", "").strip().lower()
        phone = f.get("phone", "").replace(" ", "")
        if not f.get("name", "").strip():
            errors["name"] = "Vui lòng nhập họ tên."
        if not EMAIL_RE.match(email):
            errors["email"] = "Email chưa đúng định dạng."
        elif _db().execute("SELECT 1 FROM users WHERE email=?", (email,)).fetchone():
            errors["email"] = "Email này đã có tài khoản. Bạn đăng nhập nhé."
        if phone and not PHONE_RE.match(phone):
            errors["phone"] = "Số điện thoại cần 10 số, bắt đầu bằng 0."
        if len(f.get("password", "")) < 8:
            errors["password"] = "Mật khẩu cần ít nhất 8 ký tự."
        elif f.get("password") != f.get("password2"):
            errors["password2"] = "Hai mật khẩu chưa khớp."
        if not f.get("agree"):
            errors["agree"] = "Vui lòng đồng ý với điều khoản và chính sách bảo mật."
        if not errors:
            cur = _db().execute("INSERT INTO users(email,phone,name,pw,created,address) VALUES (?,?,?,?,?,?)",
                                (email, phone, f["name"].strip(), generate_password_hash(f["password"]), now_str(), "{}"))
            uid = cur.lastrowid
            w = L["welcome"]
            give_voucher(uid, w["value"], w["min"], "Quà chào mừng thành viên mới", w["days"])
            _db().commit()
            _start_session(uid)
            flash("Tạo tài khoản thành công! Bạn vừa nhận voucher chào mừng " + vnd(w["value"]) + ".")
            return redirect(safe_next(nxt))
    return render_template("auth.html", mode="register", f=f, errors=errors, nxt=nxt)


@bp.post("/dang-xuat")
def logout():
    keep = {k: session.get(k) for k in ("cart_id",)}
    session.clear()
    session.update({k: v for k, v in keep.items() if v})
    flash("Bạn đã đăng xuất.")
    return redirect(url_for("home"))


# ------------------------------------------------------------------ trang cá nhân
def _orders_of(uid):
    out = []
    for r in _db().execute("SELECT * FROM user_orders WHERE user_id=?", (uid,)):
        o = _get_order(r["order_code"])
        if o:
            o["pts"], o["pts_status"] = r["points"], r["status"]
            out.append(o)
    out.sort(key=lambda o: datetime.strptime(o["created"], "%d/%m/%Y %H:%M"), reverse=True)
    return out


def _ctx(tab):
    u = current_user()
    t, nt = tier_of(u["spent"]), next_tier(u["spent"])
    prog = 100 if not nt else round((u["spent"] - t["min"]) / (nt["min"] - t["min"]) * 100)
    orders = _orders_of(u["id"])
    pending = sum(o["pts"] for o in orders if o["pts_status"] == "pending")
    log = [dict(r) for r in _db().execute("SELECT * FROM points_log WHERE user_id=? ORDER BY id DESC LIMIT 20", (u["id"],))]
    return dict(tab=tab, u=u, tier=t, ntier=nt, prog=prog, orders=orders, pending=pending, log=log,
                vouchers=user_vouchers(u["id"]), old_vouchers=[v for v in user_vouchers(u["id"], False) if v["used_order"]],
                steps=D.ORDER_STEPS, pay=D.PAYMENT_STATUS, provinces=D.PROVINCES, f={}, errors={},
                profile={"name": u["name"], "phone": u["phone"], "birthday": u["birthday"], **u["address"]})


@bp.route("/tai-khoan")
@login_required
def account():
    return render_template("account.html", **_ctx("overview"))


@bp.route("/tai-khoan/don-hang")
@login_required
def account_orders():
    return render_template("account.html", **_ctx("orders"))


@bp.route("/tai-khoan/uu-dai")
@login_required
def account_rewards():
    return render_template("account.html", **_ctx("rewards"))


@bp.post("/tai-khoan/doi-diem/<rid>")
@login_required
def redeem(rid):
    u = current_user()
    rw = next((r for r in L["rewards"] if r["id"] == rid), None)
    if not rw:
        abort(404)
    # trừ điểm có điều kiện để tránh bấm 2 lần bị âm điểm
    cur = _db().execute("UPDATE users SET points=points-? WHERE id=? AND points>=?", (rw["points"], u["id"], rw["points"]))
    if not cur.rowcount:
        flash(f"Bạn cần {rw['points']} điểm để đổi ưu đãi này.", "error")
    else:
        code = give_voucher(u["id"], rw["value"], rw["min"], f"Đổi {rw['points']} điểm", L["voucher_days"])
        _log(u["id"], -rw["points"], f"Đổi voucher {code}")
        _db().commit()
        flash(f"Đổi điểm thành công! Mã {code} giảm {vnd(rw['value'])} đã nằm trong Ưu đãi của bạn.")
    return redirect(url_for("acc.account_rewards"))


@bp.route("/tai-khoan/cai-dat", methods=["GET", "POST"])
@login_required
def account_settings():
    ctx = _ctx("settings")
    u = ctx["u"]
    if request.method == "POST":
        f = request.form.to_dict()
        errors = {}
        if f.get("form") == "profile":
            phone = f.get("phone", "").replace(" ", "")
            if not f.get("name", "").strip():
                errors["name"] = "Vui lòng nhập họ tên."
            if phone and not PHONE_RE.match(phone):
                errors["phone"] = "Số điện thoại cần 10 số, bắt đầu bằng 0."
            if f.get("province") and f["province"] not in D.PROVINCES:
                errors["province"] = "Chọn tỉnh/thành phố."
            if not errors:
                addr = {k: f.get(k, "").strip() for k in ("province", "district", "street")}
                _db().execute("UPDATE users SET name=?, phone=?, birthday=?, address=? WHERE id=?",
                              (f["name"].strip(), phone, f.get("birthday", ""), json.dumps(addr, ensure_ascii=False), u["id"]))
                _db().commit()
                flash("Đã lưu thông tin cá nhân.")
                return redirect(url_for("acc.account_settings"))
        elif f.get("form") == "password":
            r = _db().execute("SELECT pw FROM users WHERE id=?", (u["id"],)).fetchone()
            if not check_password_hash(r["pw"], f.get("old", "")):
                errors["old"] = "Mật khẩu hiện tại chưa đúng."
            if len(f.get("new", "")) < 8:
                errors["new"] = "Mật khẩu mới cần ít nhất 8 ký tự."
            elif f.get("new") != f.get("new2"):
                errors["new2"] = "Hai mật khẩu chưa khớp."
            if not errors:
                _db().execute("UPDATE users SET pw=? WHERE id=?", (generate_password_hash(f["new"]), u["id"]))
                _db().commit()
                flash("Đã đổi mật khẩu.")
                return redirect(url_for("acc.account_settings"))
        ctx.update(f=f, errors=errors)
    return render_template("account.html", **ctx)
