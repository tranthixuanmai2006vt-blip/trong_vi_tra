/* ================= TẠO HỘP QUÀ – 6 bước ================= */
(function () {
  const BX = window.BX, $ = id => document.getElementById(id);
  const KEY = 'tvt_giftbox_v1', TTL = 24 * 3600 * 1000;
  const STEPS = ['Chọn trà & bánh', 'Chọn hộp', 'Giấy gói', 'Thiệp & phụ kiện', 'Lời chúc', 'Xem lại'];
  const vnd = n => (Math.round(n) || 0).toLocaleString('vi-VN') + 'đ';
  const esc = s => String(s ?? '').replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const SKU = {}; BX.products.forEach(p => p.variants.forEach(v => SKU[v.sku] = { p, v }));
  const byId = (arr, id) => arr.find(x => x.id === id);
  const MAXCAP = Math.max(...BX.boxes.map(b => b.capacity));

  const fresh = () => ({ step: 1, maxStep: 1, items: {}, box: null, paper: null, card: null, acc: {},
    wish: { to: '', message: '', from: '' }, boxes: 1, reqId: null, emptyOk: false, type: 'tra' });
  let st = fresh(), notice = {};

  /* ---------- tính toán ---------- */
  const lines = () => Object.entries(st.items).filter(([, q]) => q > 0).map(([sku, q]) => ({ sku, q, ...SKU[sku] })).filter(l => l.p);
  const slots = () => lines().reduce((s, l) => s + l.v.slots * l.q, 0);
  const box = () => byId(BX.boxes, st.box), paper = () => byId(BX.papers, st.paper), card = () => byId(BX.cards, st.card);
  const accLines = () => Object.entries(st.acc).filter(([, q]) => q > 0).map(([id, q]) => ({ a: byId(BX.accessories, id), q })).filter(x => x.a);
  const price = () => {
    const it = lines().reduce((s, l) => s + l.v.price * l.q, 0);
    const b = box()?.price || 0, pa = paper()?.price || 0, c = card()?.price || 0;
    const ac = accLines().reduce((s, x) => s + x.a.price * x.q, 0);
    return { it, b, pa, c, ac, unit: it + b + pa + c + ac };
  };
  const prepDays = () => Math.max(0, ...lines().map(l => l.p.prep_days), box()?.prep_days || 0, paper()?.prep_days || 0, card()?.prep_days || 0) + BX.packing_days;
  const hasCard = () => st.card && st.card !== 'CD-NONE';

  function stepError(n) {
    if (n === 1) {
      if (!lines().length) return 'Chọn ít nhất một món để tiếp tục.';
      for (const l of lines()) if (l.q > l.v.stock) return `${l.p.name} chỉ còn ${l.v.stock}.`;
      if (slots() > MAXCAP) return `Các món cần ${slots()} ô, vượt hộp lớn nhất (${MAXCAP} ô). Hãy giảm món hoặc gửi yêu cầu thiết kế riêng.`;
    }
    if (n === 2) {
      const b = box(); if (!b) return 'Chọn một mẫu hộp.';
      if (b.stock <= 0) return `${b.name} đang tạm hết.`;
      if (slots() > b.capacity) return `${b.name} không đủ chỗ (${slots()}/${b.capacity} ô).`;
    }
    if (n === 3) {
      const p = paper(); if (!p) return 'Chọn giấy gói hoặc “Không thêm giấy gói”.';
      if (p.stock <= 0) return `${p.name} đang tạm hết.`;
      if (!p.fits.includes(st.box)) return `${p.name} không dùng được cho hộp đã chọn.`;
    }
    if (n === 4) {
      if (!card()) return 'Chọn một mẫu thiệp hoặc “Không dùng thiệp”.';
      for (const x of accLines()) { if (x.a.stock <= 0) return `${x.a.name} đang tạm hết.`; if (x.q > x.a.max) return `${x.a.name}: tối đa ${x.a.max} ${x.a.unit}.`; }
    }
    if (n === 5 && hasCard()) {
      const len = st.wish.message.length, mx = card().max_chars;
      if (len > mx) return `Lời chúc dài hơn ${len - mx} ký tự so với giới hạn của thiệp. Vui lòng rút gọn.`;
      if (!len && !st.emptyOk) return 'Thiệp đang để trống. Bấm “Tiếp tục” lần nữa nếu bạn muốn nhận thiệp trống.';
    }
    return null;
  }
  const firstInvalid = () => { for (let i = 1; i <= 5; i++) if (stepError(i)) return i; return 6; };

  /* ---------- lưu nháp ---------- */
  function save() {
    try {
      const snap = {}; lines().forEach(l => snap[l.sku] = l.v.price);
      localStorage.setItem(KEY, JSON.stringify({ st, snap, at: Date.now() }));
    } catch (e) { }
  }
  function clearDraft() { try { localStorage.removeItem(KEY); } catch (e) { } }

  /* ---------- render ---------- */
  function renderStepbar() {
    $('stepbar').innerHTML = STEPS.map((s, i) => {
      const n = i + 1, done = n < st.step && !stepError(n), cur = n === st.step;
      return `<li class="${cur ? 'current' : ''} ${done ? 'done' : ''}"><button ${n > st.maxStep ? 'disabled' : ''} data-go="${n}" aria-current="${cur ? 'step' : 'false'}"><span>${done ? '✓' : n}</span>${s}</button></li>`;
    }).join('');
    $('stepbar').querySelectorAll('[data-go]').forEach(b => b.onclick = () => go(+b.dataset.go));
    $('stepCount').textContent = `Bước ${st.step}/6 · ${STEPS[st.step - 1]}`;
  }

  function renderItems() {
    const q = ($('bxSearch').value || '').toLowerCase(), pr = $('bxPrice').value, onlyStock = $('bxStock').checked;
    const [lo, hi] = pr ? pr.split('-').map(Number) : [0, 1e12];
    const list = BX.products.filter(p => p.type === st.type && p.name.toLowerCase().includes(q)
      && p.variants.some(v => v.price >= lo && v.price < hi) && (!onlyStock || p.variants.some(v => v.stock > 0)));
    if (!list.length) { $('bxItems').innerHTML = `<div class="empty"><p>Không tìm thấy món phù hợp.</p><button class="btn btn-sm btn-secondary" id="clrF">Xóa bộ lọc</button></div>`;
      $('clrF').onclick = () => { $('bxSearch').value = ''; $('bxPrice').value = ''; $('bxStock').checked = false; renderItems(); }; return; }
    $('bxItems').innerHTML = list.map(p => {
      const opts = p.variants.map(v => `<option value="${v.sku}" ${v.stock <= 0 ? 'disabled' : ''}>${esc(v.label)} – ${vnd(v.price)}${v.stock <= 0 ? ' (tạm hết)' : ''}</option>`).join('');
      const chosen = p.variants.filter(v => st.items[v.sku] > 0);
      const allOut = p.variants.every(v => v.stock <= 0);
      return `<article class="bx-card ${chosen.length ? 'selected' : ''} ${allOut ? 'is-out' : ''}">
        <div class="bx-art ${p.image_url ? 'has-photo' : ''}" style="--c:${p.color}">${p.image_url ? `<img src="${esc(p.image_url)}" alt="${esc(p.name)}" loading="lazy">` : ''}</div>
        <div class="bx-body"><h4>${esc(p.name)}</h4><p class="small muted">${esc(p.taste_note)}</p>
          ${p.type === 'banh' ? `<p class="small"><span class="pill-warn">Dị ứng: ${esc(p.allergens.join(', '))}</span> · Chuẩn bị ${p.prep_days} ngày</p>` : ''}
          <button class="link-sm" data-detail="${p.id}">Xem chi tiết</button>
          ${allOut ? '<p class="err small">Tạm hết hàng</p>' : `<div class="bx-add"><select data-var="${p.id}" aria-label="Quy cách ${esc(p.name)}">${opts}</select>
          <button class="btn btn-sm" data-addbox="${p.id}">Thêm vào hộp</button></div>`}
          ${chosen.map(v => `<div class="bx-chosen"><span>${esc(v.label)}</span><div class="stepper stepper-sm"><button data-dec="${v.sku}" aria-label="Giảm">−</button><b>${st.items[v.sku]}</b><button data-inc="${v.sku}" aria-label="Tăng">+</button></div></div>`).join('')}
        </div></article>`;
    }).join('');
    $('bxItems').querySelectorAll('[data-addbox]').forEach(b => b.onclick = () => {
      const sku = $('bxItems').querySelector(`[data-var="${b.dataset.addbox}"]`).value; changeQty(sku, 1);
    });
    $('bxItems').querySelectorAll('[data-inc]').forEach(b => b.onclick = () => changeQty(b.dataset.inc, 1));
    $('bxItems').querySelectorAll('[data-dec]').forEach(b => b.onclick = () => changeQty(b.dataset.dec, -1));
    $('bxItems').querySelectorAll('[data-detail]').forEach(b => b.onclick = () => openDetail(b.dataset.detail, b));
  }
  function changeQty(sku, d) {
    const { v, p } = SKU[sku]; const cur = st.items[sku] || 0, n = Math.max(0, cur + d);
    if (n > v.stock) return toast(`${p.name} (${v.label}) chỉ còn ${v.stock}.`, 'error');
    if (d > 0 && slots() + v.slots > MAXCAP) return toast(`Hộp lớn nhất chứa tối đa ${MAXCAP} ô. Hãy giảm bớt món hoặc gửi yêu cầu thiết kế riêng.`, 'error');
    st.items[sku] = n; if (!n) delete st.items[sku];
    const b = box(); if (b && slots() > b.capacity) { notice.box = `Hộp “${b.name}” không còn vừa với số món mới – vui lòng chọn lại hộp.`; st.box = null; }
    update();
  }

  function optCard({ id, name, sel, disabled, reason, body, priceTxt, group, type = 'radio', swatch }) {
    return `<label class="opt ${sel ? 'selected' : ''} ${disabled ? 'is-out' : ''}">
      <input type="${type}" name="${group}" value="${id}" ${sel ? 'checked' : ''} ${disabled ? 'disabled' : ''}>
      ${swatch ? `<span class="swatch" style="background:${swatch}"></span>` : ''}
      <span class="opt-body"><b>${esc(name)}</b>${body}<span class="opt-price">${priceTxt}</span>${reason ? `<small class="err">${esc(reason)}</small>` : ''}</span>
      ${sel ? '<span class="tick" aria-hidden="true">✓</span>' : ''}</label>`;
  }
  function renderBoxes() {
    const s = slots();
    $('slotInfo').innerHTML = `Các món của bạn cần <b>${s} ô</b>. ` + (notice.box ? `<span class="err">${esc(notice.box)}</span>` : '');
    $('bxBoxes').innerHTML = BX.boxes.map(b => {
      const fits = s <= b.capacity, out = b.stock <= 0;
      return optCard({ id: b.id, group: 'box', name: b.name, sel: st.box === b.id, disabled: !fits || out,
        reason: out ? 'Tạm hết' : !fits ? `Không đủ chỗ (${s}/${b.capacity} ô)` : '',
        body: `<small>Ngoài ${b.outer} · Lòng hộp ${b.inner}</small><small>${esc(b.material)} · ${esc(b.color)} · Sức chứa ${b.capacity} ô</small>${fits && !out ? '<small class="ok">✓ Phù hợp với lựa chọn của bạn</small>' : ''}${b.prep_days ? `<small>+${b.prep_days} ngày chuẩn bị</small>` : ''}`,
        priceTxt: vnd(b.price) });
    }).join('');
    $('bxBoxes').querySelectorAll('input').forEach(i => i.onchange = () => {
      st.box = i.value; notice.box = null;
      const p = paper(); if (p && !p.fits.includes(st.box)) { notice.paper = `“${p.name}” không dùng được cho hộp mới – vui lòng chọn lại giấy gói.`; st.paper = null; }
      update();
    });
  }
  function renderPapers() {
    $('bxPapers').innerHTML = (notice.paper ? `<p class="err">${esc(notice.paper)}</p>` : '') + BX.papers.map(p => {
      const fits = p.fits.includes(st.box), out = p.stock <= 0;
      return optCard({ id: p.id, group: 'paper', name: p.name, sel: st.paper === p.id, disabled: !fits || out, swatch: p.color,
        reason: out ? 'Tạm hết' : !fits ? 'Không phù hợp với hộp đã chọn' : '',
        body: `<small>${esc(p.desc)}</small>${p.prep_days ? `<small>+${p.prep_days} ngày chuẩn bị</small>` : ''}`,
        priceTxt: p.price ? '+' + vnd(p.price) + ' / hộp' : 'Không phụ phí' });
    }).join('');
    $('bxPapers').querySelectorAll('input').forEach(i => i.onchange = () => { st.paper = i.value; notice.paper = null; update(); });
  }
  function renderCards() {
    $('bxCards').innerHTML = BX.cards.map(c => optCard({ id: c.id, group: 'card', name: c.name, sel: st.card === c.id,
      disabled: c.stock <= 0, reason: c.stock <= 0 ? 'Tạm hết' : '',
      body: c.size ? `<small>${esc(c.size)} · ${esc(c.print)} · tối đa ${c.max_chars} ký tự</small>` : '<small>Không kèm thiệp và lời chúc</small>',
      priceTxt: c.price ? '+' + vnd(c.price) : 'Miễn phí' })).join('');
    $('bxCards').querySelectorAll('input').forEach(i => i.onchange = () => {
      if (i.value === 'CD-NONE' && st.wish.message && hasCard()) toast('Đã bỏ thiệp – lời chúc sẽ không được in (vẫn giữ bản nháp nếu bạn chọn lại thiệp).');
      st.card = i.value; st.emptyOk = false; update();
    });
    const accs = BX.accessories;
    $('bxAcc').innerHTML = accs.length ? accs.map(a => {
      const q = st.acc[a.id] || 0, out = a.stock <= 0;
      return `<div class="acc-row ${out ? 'is-out' : ''} ${q ? 'selected' : ''}"><div><b>${esc(a.name)}</b><small> · ${vnd(a.price)}/${a.unit} · tối đa ${a.max}</small>${out ? ' <small class="err">Tạm hết</small>' : ''}</div>
        <div class="stepper stepper-sm"><button data-adec="${a.id}" ${out || !q ? 'disabled' : ''} aria-label="Giảm ${esc(a.name)}">−</button><b>${q}</b><button data-ainc="${a.id}" ${out || q >= a.max ? 'disabled' : ''} aria-label="Tăng ${esc(a.name)}">+</button></div></div>`;
    }).join('') : '<p class="muted">Hiện chưa có phụ kiện bổ sung.</p>';
    $('bxAcc').querySelectorAll('[data-ainc]').forEach(b => b.onclick = () => { st.acc[b.dataset.ainc] = (st.acc[b.dataset.ainc] || 0) + 1; update(); });
    $('bxAcc').querySelectorAll('[data-adec]').forEach(b => b.onclick = () => { st.acc[b.dataset.adec] = Math.max(0, (st.acc[b.dataset.adec] || 0) - 1); update(); });
  }
  function renderWish() {
    const on = hasCard();
    $('wishNoCard').hidden = on; $('wishForm').hidden = !on;
    if (!on) return;
    const mx = card().max_chars, len = st.wish.message.length;
    $('wMax').textContent = mx; $('wCount').textContent = len;
    $('wErr').hidden = len <= mx; $('wErr').textContent = len > mx ? `Vượt ${len - mx} ký tự so với vùng in của “${card().name}”.` : '';
    $('pvTo').textContent = st.wish.to ? 'Gửi ' + st.wish.to + ',' : '';
    $('pvMsg').textContent = st.wish.message || '(Thiệp để trống)';
    $('pvFrom').textContent = st.wish.from ? '— ' + st.wish.from : '';
  }
  function renderReview() {
    const pr = price(), b = box(), pa = paper(), c = card();
    const n = st.boxes;
    $('review').innerHTML = `
      <div class="rv-group"><div class="rv-head"><h3>Trà & bánh (${lines().reduce((s, l) => s + l.q, 0)} món)</h3><button class="link-sm" data-go="1">Chỉnh sửa</button></div>
        <ul>${lines().map(l => `<li>${esc(l.p.name)} – ${esc(l.v.label)} × ${l.q}<span>${vnd(l.v.price * l.q)}</span>${l.p.type === 'banh' ? `<small class="muted">HSD: ${esc(l.p.hsd)} · ${esc(l.p.storage)}</small>` : ''}</li>`).join('')}</ul></div>
      <div class="rv-group"><div class="rv-head"><h3>Hộp</h3><button class="link-sm" data-go="2">Chỉnh sửa</button></div><ul><li>${esc(b.name)}<span>${vnd(b.price)}</span></li></ul></div>
      <div class="rv-group"><div class="rv-head"><h3>Giấy gói</h3><button class="link-sm" data-go="3">Chỉnh sửa</button></div><ul><li>${esc(pa.name)}<span>${vnd(pa.price)}</span></li></ul></div>
      <div class="rv-group"><div class="rv-head"><h3>Thiệp & phụ kiện</h3><button class="link-sm" data-go="4">Chỉnh sửa</button></div>
        <ul><li>${esc(c.name)}<span>${vnd(c.price)}</span></li>${accLines().map(x => `<li>${esc(x.a.name)} × ${x.q}<span>${vnd(x.a.price * x.q)}</span></li>`).join('')}</ul></div>
      ${hasCard() ? `<div class="rv-group"><div class="rv-head"><h3>Lời chúc (in nguyên văn)</h3><button class="link-sm" data-go="5">Chỉnh sửa</button></div>
        <blockquote class="wish-quote">${st.wish.to ? 'Gửi ' + esc(st.wish.to) + ',<br>' : ''}${esc(st.wish.message || '(Thiệp trống)').replace(/\n/g, '<br>')}${st.wish.from ? '<br>— ' + esc(st.wish.from) : ''}</blockquote></div>` : ''}
      <div class="rv-price">
        <div><span>Trà & bánh</span><span>${vnd(pr.it)}</span></div><div><span>Hộp</span><span>${vnd(pr.b)}</span></div>
        <div><span>Giấy gói</span><span>${vnd(pr.pa)}</span></div><div><span>Thiệp</span><span>${vnd(pr.c)}</span></div>
        <div><span>Phụ kiện</span><span>${vnd(pr.ac)}</span></div>
        <div class="rv-unit"><span>Giá 1 hộp</span><b>${vnd(pr.unit)}</b></div>
        <div class="qty-row"><label>Số hộp cùng cấu hình</label><div class="stepper"><button type="button" id="nbDec" aria-label="Giảm số hộp">−</button><b id="nbVal">${n}</b><button type="button" id="nbInc" aria-label="Tăng số hộp">+</button></div></div>
        <div class="rv-total"><span>Tổng ${n} hộp</span><b>${vnd(pr.unit * n)}</b></div>
        <p class="small muted">Thời gian chuẩn bị: <b>${prepDays()} ngày làm việc</b> (chưa gồm vận chuyển). Phí vận chuyển được tính tại bước thanh toán. Muốn khác lời chúc hoặc món, hãy tạo một cấu hình khác.</p>
        <p class="err" id="addErr" role="alert" hidden></p>
        <button class="btn btn-lg btn-block" id="addCart">Thêm hộp quà vào giỏ · ${vnd(pr.unit * n)}</button>
      </div>`;
    $('review').querySelectorAll('[data-go]').forEach(b => b.onclick = () => go(+b.dataset.go));
    $('nbDec').onclick = () => { st.boxes = Math.max(1, st.boxes - 1); update(); };
    $('nbInc').onclick = () => {
      const lim = Math.min(...lines().map(l => Math.floor(l.v.stock / l.q)), box().stock);
      if (st.boxes + 1 > lim) return toast(`Chỉ đủ hàng cho tối đa ${lim} hộp cùng cấu hình.`, 'error');
      st.boxes++; update();
    };
    $('addCart').onclick = addToCart;
  }
  function renderSummary() {
    const pr = price(), b = box(), pa = paper(), c = card(), ls = lines();
    $('sumBody').innerHTML = `
      <div class="sum-row"><span>Món</span><span>${ls.length ? ls.map(l => `${esc(l.p.name)} ×${l.q}`).join('<br>') : '<em class="muted">Chưa chọn</em>'}</span></div>
      <div class="sum-row"><span>Hộp</span><span>${b ? esc(b.name) : '<em class="muted">Chưa chọn</em>'}</span></div>
      <div class="sum-row"><span>Giấy</span><span>${pa ? esc(pa.name) : '<em class="muted">Chưa chọn</em>'}</span></div>
      <div class="sum-row"><span>Thiệp</span><span>${c ? esc(c.name) : '<em class="muted">Chưa chọn</em>'}</span></div>
      <div class="sum-row"><span>Phụ kiện</span><span>${accLines().length ? accLines().map(x => esc(x.a.name) + ' ×' + x.q).join('<br>') : '—'}</span></div>
      <div class="sum-row"><span>Sức chứa</span><span>${slots()} ô${b ? ' / ' + b.capacity : ''}</span></div>`;
    $('sumPrice').textContent = vnd(pr.unit); $('mbPrice').textContent = vnd(pr.unit);
    $('sumPrep').textContent = ls.length ? `Thời gian chuẩn bị dự kiến: ${prepDays()} ngày làm việc` : '';
  }

  function update(skipSave) {
    renderStepbar();
    document.querySelectorAll('.step').forEach(s => s.hidden = +s.dataset.step !== st.step);
    ({ 1: renderItems, 2: renderBoxes, 3: renderPapers, 4: renderCards, 5: renderWish, 6: renderReview })[st.step]();
    renderSummary();
    const err = st.step < 6 ? stepError(st.step) : null;
    $('nextReason').textContent = err || '';
    $('nextBtn').hidden = st.step === 6; $('mbNext').hidden = st.step === 6;
    $('nextBtn').textContent = st.step < 6 ? `Tiếp tục: ${STEPS[st.step]}` : '';
    $('nextBtn').setAttribute('aria-disabled', err ? 'true' : 'false');
    $('nextBtn').classList.toggle('is-disabled', !!err && !(st.step === 5 && err.includes('thiệp trống')));
    $('prevBtn').disabled = st.step === 1;
    if (!skipSave) save();
  }
  function go(n, focus = true) {
    const fi = firstInvalid();
    if (n > fi) { n = fi; toast('Hoàn thành bước trước để tiếp tục.'); }
    st.step = n; st.maxStep = Math.max(st.maxStep, n);
    if (n === 6 && !st.reqId) st.reqId = (crypto.randomUUID ? crypto.randomUUID() : String(Date.now()) + Math.random());
    update();
    if (focus) { const h = document.querySelector(`.step[data-step="${n}"] h2`); h && h.focus({ preventScroll: true });
      document.getElementById('stepbar').scrollIntoView({ behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth', block: 'start' }); }
  }
  function next() {
    const err = stepError(st.step);
    if (err) {
      if (st.step === 5 && err.includes('thiệp trống')) { st.emptyOk = true; return go(6); }
      $('nextReason').textContent = err; toast(err, 'error'); return;
    }
    go(st.step + 1);
  }

  async function addToCart() {
    for (let i = 1; i <= 5; i++) { const e = stepError(i); if (e) { toast(e, 'error'); return go(i); } }
    const btn = $('addCart'); btn.disabled = true; btn.textContent = 'Đang thêm…';
    const cfg = { items: lines().map(l => ({ sku: l.sku, qty: l.q })), box: st.box, paper: st.paper, card: st.card,
      accessories: st.acc, wish: hasCard() ? st.wish : {}, boxes: st.boxes };
    try {
      const r = await fetch('/api/giftbox/add', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ config: cfg, request_id: st.reqId }) });
      const d = await r.json();
      if (!d.ok) { $('addErr').hidden = false; $('addErr').textContent = d.msg + ' Vui lòng kiểm tra và chỉnh lại.'; btn.disabled = false; btn.textContent = 'Thử lại'; return; }
      window.setCartBadge && setCartBadge(d.cart.count);
      clearDraft();
      document.querySelector('.step-nav').hidden = true; document.querySelectorAll('.step').forEach(s => s.hidden = true);
      $('successPanel').hidden = false; $('successPanel').focus();
    } catch (e) {
      $('addErr').hidden = false; $('addErr').textContent = 'Mất kết nối. Cấu hình của bạn vẫn được giữ – hãy thử lại.';
      btn.disabled = false; btn.textContent = 'Thử lại';
    }
  }

  function openDetail(pid, opener) {
    const p = BX.products.find(x => x.id === pid);
    $('ddBody').innerHTML = `<h3 id="ddTitle">${esc(p.name)}</h3><p>${esc(p.desc)}</p>
      <ul class="meta-list">${p.variants.map(v => `<li><span>${esc(v.label)}</span>${vnd(v.price)} · ${v.stock > 0 ? 'còn ' + v.stock : 'tạm hết'}</li>`).join('')}</ul>
      ${p.allergens.length ? `<p><b>Dị ứng:</b> ${esc(p.allergens.join(', '))}</p>` : ''}
      <p><b>Bảo quản:</b> ${esc(p.storage)}</p><p><b>Hạn dùng:</b> ${esc(p.hsd)}</p>
      <p><b>Chuẩn bị:</b> ${p.prep_days} ngày</p><a class="link" href="${p.url}" target="_blank" rel="noopener">Mở trang sản phẩm ↗</a>`;
    const dr = $('detailDrawer'); dr.hidden = false; $('ddClose').focus();
    const close = () => { dr.hidden = true; opener.focus(); document.removeEventListener('keydown', esc_); };
    const esc_ = e => { if (e.key === 'Escape') close(); };
    $('ddClose').onclick = close; dr.onclick = e => { if (e.target === dr) close(); };
    document.addEventListener('keydown', esc_);
  }

  /* ---------- sự kiện ---------- */
  $('nextBtn').onclick = next; $('mbNext').onclick = next;
  $('prevBtn').onclick = () => go(Math.max(1, st.step - 1));
  $('startBtn').onclick = e => { e.preventDefault(); go(st.step); };
  document.querySelectorAll('.step[data-step="1"] .tab').forEach(t => t.onclick = () => {
    document.querySelectorAll('.step[data-step="1"] .tab').forEach(x => { x.classList.toggle('active', x === t); x.setAttribute('aria-selected', x === t); });
    st.type = t.dataset.type; renderItems();
  });
  ['bxSearch', 'bxPrice', 'bxStock'].forEach(id => $(id).addEventListener('input', renderItems));
  $('wTo').oninput = e => { st.wish.to = e.target.value; renderWish(); update(); };
  $('wFrom').oninput = e => { st.wish.from = e.target.value; renderWish(); update(); };
  $('wMsg').oninput = e => { st.wish.message = e.target.value; st.emptyOk = false; renderWish(); renderStepbar(); $('nextReason').textContent = stepError(5) || ''; save(); };
  $('wSamples').innerHTML = BX.wishes.map((w, i) => `<button class="sample" data-w="${i}">${esc(w)}</button>`).join('');
  $('wSamples').querySelectorAll('[data-w]').forEach(b => b.onclick = () => {
    if (st.wish.message && !confirm('Thay lời chúc hiện tại bằng mẫu này?')) return;
    st.wish.message = BX.wishes[+b.dataset.w]; $('wMsg').value = st.wish.message; renderWish(); update();
  });
  $('newBox').onclick = () => { st = fresh(); notice = {}; $('successPanel').hidden = true; document.querySelector('.step-nav').hidden = false; syncWishInputs(); go(1); };
  $('toCustom').onclick = e => { if (lines().length && !confirm('Bạn đang có hộp quà chưa hoàn tất. Bản nháp sẽ được giữ trên trình duyệt này. Chuyển sang Thiết kế riêng?')) e.preventDefault(); };
  function syncWishInputs() { $('wTo').value = st.wish.to; $('wMsg').value = st.wish.message; $('wFrom').value = st.wish.from; }

  /* ---------- khởi động: khôi phục bản nháp ---------- */
  let draft = null;
  try { draft = JSON.parse(localStorage.getItem(KEY)); } catch (e) { }
  if (draft && Date.now() - draft.at < TTL && Object.keys(draft.st.items || {}).length) {
    $('restoreBox').hidden = false;
    const changed = Object.entries(draft.snap || {}).filter(([sku, pr]) => !SKU[sku] || SKU[sku].v.price !== pr || SKU[sku].v.stock <= 0);
    $('restoreNote').textContent = changed.length ? `Lưu ý: ${changed.length} món đã thay đổi giá hoặc tồn kho – vui lòng kiểm tra lại ở bước 1.` : 'Giá và tồn kho sẽ được kiểm tra lại.';
    $('restoreYes').onclick = () => { st = Object.assign(fresh(), draft.st); $('restoreBox').hidden = true; syncWishInputs(); go(Math.min(st.step, firstInvalid())); };
    $('restoreNo').onclick = () => { clearDraft(); $('restoreBox').hidden = true; update(); };
  } else if (draft) clearDraft();
  if (window.BX_PRESELECT && SKU[window.BX_PRESELECT] && SKU[window.BX_PRESELECT].v.stock > 0 && $('restoreBox').hidden) {
    st.items[window.BX_PRESELECT] = 1; st.type = SKU[window.BX_PRESELECT].p.type;
    document.querySelectorAll('.step[data-step="1"] .tab').forEach(x => { x.classList.toggle('active', x.dataset.type === st.type); });
  }
  update(true);
})();
