/* ================= TRỒNG VỊ TRÀ – script chung ================= */
const vndFmt = n => (Math.round(n) || 0).toLocaleString('vi-VN') + 'đ';
const reduceMotion = matchMedia('(prefers-reduced-motion: reduce)').matches;

/* ---------- Toast ---------- */
function toast(msg, type = 'ok', action) {
  const w = document.getElementById('toasts'); if (!w) return;
  const t = document.createElement('div'); t.className = 'toast toast-' + type; t.setAttribute('role', type === 'error' ? 'alert' : 'status');
  t.innerHTML = `<span>${type === 'error' ? '⚠' : '✓'}</span><p></p>`; t.querySelector('p').textContent = msg;
  if (action) { const a = document.createElement('a'); a.href = action.href; a.textContent = action.label; a.className = 'toast-act'; t.appendChild(a); }
  const x = document.createElement('button'); x.className = 'toast-x'; x.setAttribute('aria-label', 'Đóng'); x.textContent = '✕'; x.onclick = () => t.remove(); t.appendChild(x);
  w.appendChild(t); setTimeout(() => t.remove(), type === 'error' ? 7000 : 4500);
}
function setCartBadge(n) { const b = document.getElementById('cartBadge'); if (!b) return; b.textContent = n; b.hidden = !n;
  if (!reduceMotion) { b.classList.remove('bump'); void b.offsetWidth; b.classList.add('bump'); } }
async function copyText(t) {
  try { await navigator.clipboard.writeText(t); toast('Đã sao chép'); }
  catch (e) { const a = document.createElement('textarea'); a.value = t; document.body.appendChild(a); a.select(); document.execCommand('copy'); a.remove(); toast('Đã sao chép'); }
}

/* ---------- Giỏ hàng ---------- */
async function addMany(items, btn) {
  if (btn) { btn.disabled = true; btn.dataset.txt = btn.textContent; btn.textContent = 'Đang thêm…'; }
  try {
    const r = await fetch('/api/cart/add', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ items }) });
    const d = await r.json();
    if (d.ok) { setCartBadge(d.cart.count); toast(d.msg, 'ok', { href: '/gio-hang', label: 'Xem giỏ' }); }
    else toast(d.msg, 'error');
    return d;
  } catch (e) { toast('Mất kết nối, vui lòng thử lại.', 'error'); }
  finally { if (btn) { btn.disabled = false; btn.textContent = btn.dataset.txt; } }
}
function bindAdd(root = document) {
  root.querySelectorAll('[data-add]').forEach(b => { if (b._b) return; b._b = 1; b.onclick = e => { e.preventDefault(); addMany([{ sku: b.dataset.add, qty: 1 }], b); }; });
  root.querySelectorAll('[data-add-multi]').forEach(b => { if (b._b) return; b._b = 1; b.onclick = e => { e.preventDefault(); addMany(JSON.parse(b.dataset.addMulti), b); }; });
}
bindAdd();

/* ---------- Khối mua hàng trang chi tiết ---------- */
document.querySelectorAll('[data-buybox]').forEach(form => {
  const qty = form.querySelector('[name=qty]'), msg = form.querySelector('[data-msg]');
  const priceOut = form.querySelector('[data-price-out]'), stockOut = form.querySelector('[data-stock-out]');
  const skuOut = document.querySelector('[data-sku-out]');
  const sel = () => form.querySelector('[name=sku]:checked');
  const cardSel = () => form.querySelector('[name=card]:checked');
  const wish = form.querySelector('[data-wish]'), ta = form.querySelector('[name=message]');
  function refresh() {
    const s = sel(); if (!s) return;
    const extra = cardSel() ? +cardSel().dataset.price : 0;
    priceOut.textContent = vndFmt((+s.dataset.price + extra) * Math.max(1, +qty.value || 1));
    const st = +s.dataset.stock; stockOut.textContent = st > 0 ? (st < 5 ? `Chỉ còn ${st}` : 'Còn hàng') : 'Tạm hết';
    qty.max = st; if (+qty.value > st) qty.value = Math.max(1, st);
    if (skuOut) skuOut.textContent = s.value;
    form.querySelectorAll('[data-action]').forEach(b => b.disabled = st <= 0);
    if (wish) {
      const c = cardSel(), mx = c ? +c.dataset.max : 0; wish.hidden = !mx;
      form.querySelector('[data-max]').textContent = mx; const len = ta.value.length;
      form.querySelector('[data-count]').textContent = len; form.querySelector('[data-count]').parentElement.classList.toggle('err', len > mx);
      form.querySelector('[data-preview]').textContent = ta.value || '(Thiệp để trống)';
    }
  }
  form.addEventListener('change', refresh); qty.addEventListener('input', refresh); if (ta) ta.addEventListener('input', refresh);
  form.querySelectorAll('[data-step]').forEach(b => b.onclick = () => { qty.value = Math.max(1, Math.min(+qty.max || 99, (+qty.value || 1) + +b.dataset.step)); refresh(); });
  let action = 'add';
  form.querySelectorAll('[data-action]').forEach(b => b.addEventListener('click', () => action = b.dataset.action));
  form.onsubmit = async e => {
    e.preventDefault(); msg.textContent = ''; msg.className = 'form-msg';
    const s = sel(); if (!s) { msg.textContent = 'Vui lòng chọn quy cách.'; msg.classList.add('err'); return; }
    const q = +qty.value; if (!(q >= 1)) { msg.textContent = 'Số lượng không hợp lệ.'; msg.classList.add('err'); return; }
    if (q > +s.dataset.stock) { msg.textContent = `Chỉ còn ${s.dataset.stock} sản phẩm.`; msg.classList.add('err'); return; }
    const item = { sku: s.value, qty: q };
    if (cardSel() && cardSel().value !== 'CD-NONE') {
      if (ta.value.length > +cardSel().dataset.max) { msg.textContent = `Lời chúc tối đa ${cardSel().dataset.max} ký tự.`; msg.classList.add('err'); ta.focus(); return; }
      item.opts = { card: cardSel().value, message: ta.value };
    }
    const d = await addMany([item], form.querySelector(`[data-action="${action}"]`));
    if (d && d.ok && action === 'buy') location.href = '/thanh-toan';
  };
  refresh();
});

/* ---------- Header: menu, dropdown, tìm kiếm ---------- */
(function () {
  const nav = document.getElementById('nav'), burger = document.getElementById('burger'), ov = document.getElementById('navOverlay');
  const open = () => { nav.classList.add('open'); ov.hidden = false; burger.setAttribute('aria-expanded', 'true'); document.getElementById('navClose').focus(); };
  const close = () => { nav.classList.remove('open'); ov.hidden = true; burger.setAttribute('aria-expanded', 'false'); burger.focus(); };
  burger.onclick = open; document.getElementById('navClose').onclick = close; ov.onclick = close;
  document.addEventListener('keydown', e => { if (e.key === 'Escape') { if (nav.classList.contains('open')) close(); document.querySelectorAll('.dd.open').forEach(d => { d.classList.remove('open'); d.querySelector('.dd-btn').setAttribute('aria-expanded', 'false'); }); } });
  document.querySelectorAll('.dd-btn').forEach(b => b.onclick = e => {
    e.stopPropagation(); const dd = b.parentElement, isOpen = dd.classList.toggle('open'); b.setAttribute('aria-expanded', isOpen);
    document.querySelectorAll('.dd').forEach(o => { if (o !== dd) { o.classList.remove('open'); o.querySelector('.dd-btn').setAttribute('aria-expanded', 'false'); } });
  });
  document.addEventListener('click', e => { if (!e.target.closest('.dd')) document.querySelectorAll('.dd.open').forEach(d => d.classList.remove('open')); });
  const sb = document.getElementById('searchBtn'), sp = document.getElementById('searchPanel');
  sb.onclick = () => { sp.hidden = !sp.hidden; sb.setAttribute('aria-expanded', !sp.hidden); if (!sp.hidden) document.getElementById('q').focus(); };
  const h = document.getElementById('header'); addEventListener('scroll', () => h.classList.toggle('scrolled', scrollY > 8), { passive: true });
})();

/* ---------- Tabs (trang chủ, về chúng tôi) ---------- */
document.querySelectorAll('.tabs[role=tablist]').forEach(tl => {
  const tabs = tl.querySelectorAll('[data-tab]'); if (!tabs.length) return;
  const scope = tl.parentElement;
  tabs.forEach(t => t.addEventListener('click', () => {
    tabs.forEach(x => { x.classList.toggle('active', x === t); x.setAttribute('aria-selected', x === t); });
    scope.querySelectorAll('.tabpanel').forEach(p => p.hidden = p.dataset.panel !== t.dataset.tab);
  }));
});

/* ---------- Copy, lightbox, tooltip, newsletter ---------- */
document.addEventListener('click', e => { const c = e.target.closest('[data-copy]'); if (c) { e.preventDefault(); copyText(c.dataset.copy); } });
function openLightbox(el) {
  const d = document.createElement('div'); d.className = 'lightbox'; d.setAttribute('role', 'dialog'); d.setAttribute('aria-modal', 'true');
  d.innerHTML = '<button class="nav-close" aria-label="Đóng">✕</button>'; d.appendChild(el.cloneNode(true)); document.body.appendChild(d);
  const close = () => { d.remove(); document.removeEventListener('keydown', k); }; const k = e => e.key === 'Escape' && close();
  d.onclick = close; document.addEventListener('keydown', k); d.querySelector('button').focus();
}
document.querySelectorAll('.article-cover .art').forEach(el => { el.style.cursor = 'zoom-in'; el.onclick = () => openLightbox(el); });

document.querySelectorAll('#nlForm').forEach(f => f.onsubmit = async e => {
  e.preventDefault(); const inp = f.querySelector('input'), m = f.parentElement.querySelector('#nlMsg');
  if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(inp.value)) { m.textContent = 'Email chưa đúng định dạng, vui lòng kiểm tra lại.'; m.className = 'small err'; inp.focus(); return; }
  const r = await fetch('/api/newsletter', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ email: inp.value, source: 'chuyen-tra' }) });
  const d = await r.json(); m.textContent = d.msg; m.className = 'small ' + (d.ok ? 'ok' : 'err'); if (d.ok) { inp.value = ''; toast(d.msg); }
});

/* ---------- Nút đang gửi ---------- */
document.querySelectorAll('form').forEach(f => f.addEventListener('submit', () => {
  const b = f.querySelector('[data-loading]'); if (b && !f.hasAttribute('data-buybox')) setTimeout(() => { b.disabled = true; b.textContent = b.dataset.loading; }, 0);
}));

/* ---------- Hẹn giờ pha ---------- */
const bt = document.getElementById('brewTimer');
if (bt) { let t = null; bt.onclick = () => {
  if (t) { clearInterval(t); t = null; bt.textContent = `⏱ Hẹn giờ ${bt.dataset.sec} giây`; return; }
  let s = +bt.dataset.sec; bt.textContent = `⏹ ${s}s – bấm để dừng`;
  t = setInterval(() => { s--; bt.textContent = `⏹ ${s}s – bấm để dừng`; if (s <= 0) { clearInterval(t); t = null; bt.textContent = '✓ Rót trà thôi!'; toast('Đã đủ thời gian hãm – rót trà thôi!'); } }, 1000);
}; }

/* ---------- Hiệu ứng xuất hiện ---------- */
if (!reduceMotion && 'IntersectionObserver' in window) {
  const io = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } }), { threshold: .1 });
  document.querySelectorAll('.reveal').forEach(el => io.observe(el));
} else document.querySelectorAll('.reveal').forEach(el => el.classList.add('in'));
