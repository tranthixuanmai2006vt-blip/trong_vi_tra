/* ================= TEA DNA ================= */
(function () {
  const DNA = window.DNA, $ = id => document.getElementById(id);
  const VER = DNA.version, KD = 'tvt_teadna_draft', KP = 'tvt_teadna_profile', TTL = 30 * 864e5;
  const AX = DNA.axes.map(a => a.key);
  const esc = s => String(s ?? '').replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const vnd = n => (Math.round(n) || 0).toLocaleString('vi-VN') + 'đ';
  const Q = {}; DNA.questions.forEach(q => Q[q.id] = q);
  let canStore = true;
  const ls = {
    get(k) { try { return JSON.parse(localStorage.getItem(k)); } catch (e) { return null; } },
    set(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); return true; } catch (e) { canStore = false; return false; } },
    del(k) { try { localStorage.removeItem(k); } catch (e) { } }
  };

  /* ---------- tính điểm ---------- */
  const scaleVal = v => (v - 1) * 25;
  const optVal = (qid, oid) => { const o = (Q[qid].options || []).find(x => x[0] === oid); return o ? o[2] : null; };
  function wavg(parts) {
    const ok = parts.filter(p => p[0] !== null && p[0] !== undefined);
    if (!ok.length) return null;
    return Math.round(ok.reduce((s, p) => s + p[0] * p[1], 0) / ok.reduce((s, p) => s + p[1], 0));
  }
  function compute(ans) {
    const sv = id => ans[id] ? scaleVal(+ans[id]) : null, ov = id => ans[id] ? optVal(id, ans[id]) : null;
    const axes = {
      sweet: wavg([[sv('q1'), 2], [ov('q2'), 1]]),
      sour: wavg([[sv('q3'), 2], [ov('q4'), 1]]),
      bitter: wavg([[sv('q5'), 2], [sv('q6'), 1]]),
      strength: sv('q7'),
      aroma: ov('q9'),
    };
    const ctx = { aroma_tag: ans.q9 || null, mode: ans.q8 || null, creamy: sv('q10'), temp: ans.q11 || null,
      astringency: sv('q6'), avoid: (ans.q12 || []).filter(x => x !== 'none') };
    const answered = DNA.questions.filter(q => q.type === 'multi' ? (ans[q.id] || []).length : ans[q.id]).length;
    return { axes, ctx, completeness: Math.round(answered / 12 * 100), answered };
  }
  function matchGroups(axes, ctx) {
    const known = AX.filter(k => axes[k] !== null && axes[k] !== undefined);
    if (!known.length) return [];
    return DNA.groups.map((g, gi) => {
      let D = known.reduce((s, k) => s + Math.abs(axes[k] - g.proto[AX.indexOf(k)]), 0) / known.length;
      let score = 100 - D;
      if (g.tag && ctx.aroma_tag && (g.tag === ctx.aroma_tag || (g.tag === 'herbal' && ctx.aroma_tag === 'floral' && false))) score = Math.min(100, score + 5);
      if (ctx.creamy !== null && ctx.creamy >= 75 && g.id === 'creamy-cloud') score += 3;
      if (ctx.mode === 'original' && ['tea-minimalist', 'amber-classic', 'roasted-soul'].includes(g.id)) score += 2;
      if (ctx.mode === 'mixed' && ['sugar-muse', 'honey-bloom', 'tropical-soul', 'creamy-cloud'].includes(g.id)) score += 2;
      return { g, score: Math.max(0, Math.min(100, score)), gi };
    }).sort((a, b) => b.score - a.score || a.gi - b.gi);
  }
  function buildProfile(ans, prev) {
    const c = compute(ans);
    const override = prev && prev.override ? prev.override : null;
    const axes = override ? override : c.axes;
    const ranked = matchGroups(axes, c.ctx);
    const manualGroup = prev && prev.manualGroup || null;
    return { version: VER, answers: ans, testAxes: c.axes, axes, override, ctx: c.ctx, completeness: c.completeness,
      answered: c.answered, group: manualGroup || (ranked[0] && ranked[0].g.id), manualGroup,
      second: ranked[1] && ranked[0] && ranked[0].score - ranked[1].score <= 3 ? ranked[1].g.id : null,
      ranked: ranked.slice(0, 13).map(r => ({ id: r.g.id, score: Math.round(r.score) })), updated: new Date().toISOString() };
  }

  /* =============== TRANG CÂU HỎI =============== */
  if (window.DNA_PAGE !== 'result') {
    let ans = {};
    const form = $('dnaForm');
    function readForm() {
      ans = {};
      DNA.questions.forEach(q => {
        if (q.type === 'multi') { const v = [...form.querySelectorAll(`[name="${q.id}"]:checked`)].map(i => i.value); if (v.length) ans[q.id] = v; }
        else { const i = form.querySelector(`[name="${q.id}"]:checked`); if (i) ans[q.id] = i.value; }
      });
    }
    function writeForm() {
      form.querySelectorAll('input').forEach(i => {
        const v = ans[i.name]; i.checked = Array.isArray(v) ? v.includes(i.value) : v === i.value;
      });
    }
    function paint() {
      const n = DNA.questions.filter(q => q.type === 'multi' ? (ans[q.id] || []).length : ans[q.id]).length;
      $('dpCount').textContent = n; $('dpFill').style.width = (n / 12 * 100) + '%'; $('dpBar').setAttribute('aria-valuenow', n);
      DNA.questions.forEach(q => {
        const has = q.type === 'multi' ? (ans[q.id] || []).length : !!ans[q.id];
        form.querySelector(`[data-clear="${q.id}"]`).hidden = !has;
        $(q.id).classList.toggle('answered', has);
      });
    }
    function persist() { if (!ls.set(KD, { version: VER, answers: ans, at: Date.now() })) $('dnaStorageWarn').hidden = false; }
    form.addEventListener('change', e => {
      if (e.target.name === 'q12') {                      // "Không có" loại trừ lựa chọn khác
        const boxes = form.querySelectorAll('[name="q12"]');
        if (e.target.value === 'none' && e.target.checked) boxes.forEach(b => { if (b.value !== 'none') b.checked = false; });
        else if (e.target.checked) form.querySelector('[name="q12"][value="none"]').checked = false;
      }
      readForm(); paint(); persist();
    });
    form.querySelectorAll('[data-clear]').forEach(b => b.onclick = () => {
      form.querySelectorAll(`[name="${b.dataset.clear}"]`).forEach(i => i.checked = false); readForm(); paint(); persist();
    });
    $('clearAll').onclick = () => {
      if (!confirm('Xóa tất cả câu trả lời? Kết quả Tea DNA cũ trên thiết bị này cũng sẽ bị xóa.')) return;
      ans = {}; writeForm(); paint(); ls.del(KD); ls.del(KP);
    };
    form.onsubmit = e => {
      e.preventDefault(); readForm();
      const c = compute(ans), hasTaste = AX.some(k => c.axes[k] !== null);
      if (!hasTaste) {
        $('dnaErr').hidden = false;
        $('dnaErr').innerHTML = (ans.q12 ? 'Đã lưu phần bạn muốn tránh, nhưng chưa đủ để tính hồ sơ vị. ' : '') + 'Hãy trả lời ít nhất một câu về vị (câu 1, 3, 5, 7 hoặc 9). <button type="button" class="link-sm" id="toQ1">Đi đến câu đầu</button>';
        $('toQ1').onclick = () => { $('q1').scrollIntoView({ behavior: 'smooth' }); $('q1').querySelector('input').focus(); };
        persist(); return;
      }
      const prev = ls.get(KP);
      const prof = buildProfile(ans, prev && prev.version === VER && prev.override ? null : null);
      persist();
      if (!ls.set(KP, prof)) sessionStorage.setItem(KP, JSON.stringify(prof));
      location.href = '/tea-dna/ket-qua';
    };
    // khôi phục nháp
    const d = ls.get(KD);
    if (d && d.version === VER && Date.now() - d.at < TTL && Object.keys(d.answers || {}).length) {
      if (new URLSearchParams(location.search).get('giu') === '1') { ans = d.answers; writeForm(); paint(); }
      else {
        $('dnaRestore').hidden = false; $('drCount').textContent = Object.keys(d.answers).length;
        $('drYes').onclick = () => { ans = d.answers; writeForm(); paint(); $('dnaRestore').hidden = true; };
        $('drNo').onclick = () => { ls.del(KD); $('dnaRestore').hidden = true; };
      }
    } else if (d) { ls.del(KD); if (d.version !== VER) { $('dnaErr').hidden = false; $('dnaErr').textContent = 'Bộ câu hỏi đã được cập nhật nên câu trả lời cũ không còn dùng được. Mời bạn làm lại.'; } }
    paint();
    return;
  }

  /* =============== TRANG KẾT QUẢ =============== */
  let prof = ls.get(KP);
  if (!prof) try { prof = JSON.parse(sessionStorage.getItem(KP)); } catch (e) { }
  if (!prof || prof.version !== VER || !prof.axes) {
    if (prof && prof.version !== VER) { const d = ls.get(KD); if (d && d.version === VER) { prof = buildProfile(d.answers); ls.set(KP, prof); } else prof = null; }
    else prof = null;
  }
  if (!prof) { $('noProfile').hidden = false; return; }

  const G = id => DNA.groups.find(g => g.id === id);
  const level = v => v === null || v === undefined ? null : v < 40 ? 'left' : v <= 60 ? 'mid' : 'right';

  function render() {
    // re-rank based on current axes
    const ranked = matchGroups(prof.axes, prof.ctx);
    if (!prof.manualGroup) { prof.group = ranked[0] && ranked[0].g.id; prof.second = ranked[1] && ranked[0].score - ranked[1].score <= 3 ? ranked[1].g.id : null; }
    const g = G(prof.group);
    const known = AX.filter(k => prof.axes[k] !== null && prof.axes[k] !== undefined);
    $('result').hidden = false; ['recSec', 'prodSec', 'groupsSec'].forEach(id => $(id).hidden = false);
    $('dnaCard').style.setProperty('--gc', g.color);
    $('gName').textContent = g.name;
    $('gTagline').textContent = g.tagline;
    $('gDesc').textContent = g.desc + ' Đây là gu uống hiện tại của bạn, không phải nhận định tính cách.';
    $('gSecond').textContent = prof.second ? `Có nét gần ${G(prof.second).name}` : '';
    const chips = [g.level];
    if (known.length <= 2) chips.unshift('Sơ bộ · ít dữ liệu');
    if (prof.override) chips.push('Đã điều chỉnh thủ công');
    if (prof.manualGroup) chips.push('Đã chọn thủ công');
    $('gChips').innerHTML = chips.map(c => `<span>${esc(c)}</span>`).join('');
    $('gConf').textContent = prof.completeness + '%'; $('gConfBar').style.width = prof.completeness + '%';
    $('gUpdated').textContent = `Cập nhật lần cuối: ${new Date(prof.updated).toLocaleString('vi-VN')} · Hồ sơ lưu trên trình duyệt này.`;
    // axes
    $('axes').innerHTML = DNA.axes.map(a => {
      const v = prof.axes[a.key], lv = level(v);
      const word = lv === 'left' ? a.left : lv === 'right' ? a.right : lv === 'mid' ? 'Cân bằng' : '';
      return `<div class="axis"><div class="ax-top"><b>${a.label}</b><span>${v === null || v === undefined ? 'Chưa có dữ liệu' : v + '/100'}</span></div>
        <div class="ax-track ${v === null || v === undefined ? 'na' : ''}">${v === null || v === undefined ? '' : `<i style="left:${v}%"></i>`}</div>
        <div class="ax-lbl"><span>${a.left}</span><b>${word}</b><span>${a.right}</span></div></div>`;
    }).join('');
    const tagName = { fruity: 'Trái cây', floral: 'Hoa', roasted: 'Rang', herbal: 'Thảo mộc' }, tempName = { cold: 'Thích uống lạnh', hot: 'Thích uống nóng', both: 'Nóng hay lạnh đều được' };
    const modeName = { original: 'Trà nguyên bản', flexible: 'Nguyên bản & pha chế', mixed: 'Trà pha chế' }, avName = { milk: 'Sữa bò', caffeine: 'Caffeine', honey: 'Mật ong', sour: 'Vị quá chua' };
    const ctx = prof.ctx;
    $('ctx').innerHTML = [ctx.aroma_tag && `Hương ưa thích: <b>${tagName[ctx.aroma_tag]}</b>`, ctx.temp && tempName[ctx.temp], ctx.mode && modeName[ctx.mode],
      ctx.creamy !== null && `Độ béo: ${ctx.creamy}/100`, ctx.astringency !== null && `Hậu chát: ${ctx.astringency}/100`,
      ctx.avoid.length && `Tránh: <b>${ctx.avoid.map(a => avName[a]).join(', ')}</b>`].filter(Boolean).map(x => `<span class="chip chip-static">${x}</span>`).join('');
    renderManual(); renderRecipes(g); renderProducts(g); renderGroups(ranked);
  }

  function renderManual() {
    $('manual').innerHTML = DNA.axes.map(a => {
      const v = prof.axes[a.key];
      return `<div class="man-row"><label for="m-${a.key}">${a.label}</label>
        <input type="range" min="0" max="100" step="1" id="m-${a.key}" value="${v ?? 50}" ${v === null || v === undefined ? 'data-na="1"' : ''}>
        <input type="number" min="0" max="100" value="${v ?? ''}" data-num="${a.key}" placeholder="—" aria-label="${a.label} (0–100)"></div>`;
    }).join('') + '<p class="small muted">Trục để trống = chưa có dữ liệu. Phần thành phần muốn tránh được giữ nguyên.</p>';
    $('manReset').hidden = !prof.override;
    DNA.axes.forEach(a => {
      const r = $('m-' + a.key), n = $('manual').querySelector(`[data-num="${a.key}"]`);
      r.oninput = () => { n.value = r.value; }; n.oninput = () => { if (n.value !== '') r.value = n.value; };
    });
  }
  $('manSave').onclick = () => {
    const o = {}; let bad = null;
    DNA.axes.forEach(a => { const n = $('manual').querySelector(`[data-num="${a.key}"]`).value.trim();
      if (n === '') o[a.key] = null; else { const x = Number(n); if (!Number.isFinite(x) || x < 0 || x > 100) bad = a.label; o[a.key] = Math.round(x); } });
    if (bad) { $('manErr').hidden = false; $('manErr').textContent = `${bad}: nhập số từ 0 đến 100 hoặc để trống.`; return; }
    if (!AX.some(k => o[k] !== null)) { $('manErr').hidden = false; $('manErr').textContent = 'Cần ít nhất một trục có điểm.'; return; }
    $('manErr').hidden = true; prof.override = o; prof.axes = o; prof.updated = new Date().toISOString(); prof.manualGroup = null;
    ls.set(KP, prof); $('manualBox').open = false; render(); toast('Đã lưu điều chỉnh hồ sơ.');
  };
  $('manCancel').onclick = () => { renderManual(); $('manErr').hidden = true; $('manualBox').open = false; };
  $('manReset').onclick = () => { prof.override = null; prof.axes = prof.testAxes; prof.updated = new Date().toISOString(); ls.set(KP, prof); render(); toast('Đã khôi phục kết quả bài test.'); };

  function dist(a, vec) {
    const known = AX.filter(k => a[k] !== null && a[k] !== undefined);
    return known.length ? known.reduce((s, k) => s + Math.abs(a[k] - vec[AX.indexOf(k)]), 0) / known.length : 100;
  }
  function renderRecipes(g) {
    const av = prof.ctx.avoid;
    let list = DNA.recipes.filter(r => {
      if (av.includes('caffeine') && !r.caffeine_free_verified) return false;
      return !r.avoid.some(x => x !== 'caffeine' && av.includes(x));
    }).map(r => {
      let s = 100 - dist(prof.axes, r.vec);
      if (prof.ctx.temp && prof.ctx.temp !== 'both' && r.temp !== 'both' && r.temp !== prof.ctx.temp) s -= 8;
      return { r, s: Math.max(0, Math.round(s)) };
    }).sort((a, b) => b.s - a.s).slice(0, 4);
    $('recTitle').textContent = 'Công thức hợp với ' + g.name;
    if (!list.length) { $('recipes').innerHTML = '<div class="empty"><p>Chưa có công thức phù hợp với các thành phần bạn muốn tránh.</p><a class="btn btn-sm btn-secondary" href="/tea-dna?giu=1#q12">Sửa tiêu chí</a></div>'; return; }
    const tempName = { cold: 'Lạnh', hot: 'Nóng', both: 'Nóng / lạnh' };
    $('recipes').innerHTML = list.map(({ r, s }) => `<article class="recipe">
      <div class="rc-img" style="--rc:${r.color}"><span class="rc-pct">${s}% hợp vị</span><svg viewBox="0 0 120 120" aria-hidden="true"><path d="M38 30h44l-6 70H44z" fill="#fff" opacity=".55" stroke="#2F3B2A" stroke-width="2"/><path d="M41 52h38l-4 46H45z" fill="var(--rc)"/><path d="M70 18 62 98" stroke="#2F3B2A" stroke-width="4" stroke-linecap="round"/></svg></div>
      <div class="rc-body"><p class="eyebrow">${esc(r.kind)} · ${tempName[r.temp]}</p><h3>${esc(r.name)}</h3><p class="small muted">${esc(r.en)}</p>
        <div class="dc-chips light">${r.tags.map(t => `<span>${esc(t)}</span>`).join('')}</div>
        <dl class="rc-meta"><div><dt>Thời gian</dt><dd>${esc(r.time)}</dd></div><div><dt>Độ khó</dt><dd>${esc(r.level)}</dd></div><div><dt>Chi phí</dt><dd>${esc(r.cost)}</dd></div></dl>
        <button class="btn btn-sm btn-secondary" data-recipe="${r.id}">Xem công thức</button></div></article>`).join('');
    $('recipes').querySelectorAll('[data-recipe]').forEach(b => b.onclick = () => openRecipe(b.dataset.recipe, b));
  }
  function openRecipe(id, opener) {
    const r = DNA.recipes.find(x => x.id === id);
    $('rdBody').innerHTML = `<p class="eyebrow">${esc(r.kind)}</p><h3 id="rdTitle">${esc(r.name)}</h3>
      <h4>Nguyên liệu</h4><ul>${r.ingredients.map(i => `<li>${esc(i)}</li>`).join('')}</ul>
      <h4>Cách pha</h4><ol>${r.steps.map(i => `<li>${esc(i)}</li>`).join('')}</ol>
      <p class="small muted">Đây là công thức tự pha tại nhà, không phải món nước đang bán.${r.caffeine_free_verified ? ' Công thức không dùng lá trà (không caffeine).' : ''}</p>
      ${r.tea_url ? `<a class="btn btn-sm" href="${r.tea_url}">Xem loại trà dùng trong công thức: ${esc(r.tea_name)}</a>` : ''}`;
    modal($('recipeDrawer'), $('rdClose'), opener);
  }
  function modal(dr, closeBtn, opener) {
    dr.hidden = false; (closeBtn || dr.querySelector('button')).focus();
    const close = () => { dr.hidden = true; opener && opener.focus(); document.removeEventListener('keydown', k); };
    const k = e => { if (e.key === 'Escape') close(); };
    if (closeBtn) closeBtn.onclick = close; dr.onclick = e => { if (e.target === dr) close(); };
    document.addEventListener('keydown', k); return close;
  }
  function renderProducts(g) {
    const av = prof.ctx.avoid;
    const allergenOf = p => (p.allergens || []).join(' ').toLowerCase();
    let note = [];
    let list = DNA.products.filter(p => {
      if (av.includes('milk') && allergenOf(p).includes('sữa')) return false;
      if (av.includes('honey') && p.avoid.includes('honey')) return false;
      return true;
    });
    if (av.includes('caffeine')) { note.push('Bạn chọn tránh caffeine: các sản phẩm trà và bánh từ trà đều có thể chứa caffeine, nên chúng tôi chưa gợi ý sản phẩm nào. Xem công thức thảo mộc ở trên.'); list = []; }
    if (av.includes('milk')) note.push('Đã ẩn bánh có sữa.');
    const ranked = list.map(p => ({ p, d: dist(prof.axes, p.dna) })).sort((a, b) => a.d - b.d);
    const pick = []; ['tra', 'banh', 'gift'].forEach(t => {
      const inT = ranked.filter(x => x.p.type === t);
      const best = inT.find(x => x.p.stock) ; if (best) pick.push(best.p);
    });
    const extra = ranked.find(x => x.p.type === 'tra' && x.p.stock && !pick.includes(x.p)); if (extra) pick.splice(1, 0, extra.p);
    $('prodTitle').textContent = 'Dành riêng cho ' + g.name;
    $('prodNote').textContent = note.join(' ');
    $('prods').innerHTML = pick.length ? pick.map(p => `<article class="pcard"><a class="pcard-img" href="${p.url}">${p.art_html}</a>
      <div class="pcard-body"><p class="pcard-type">${{ tra: 'Trà', banh: 'Bánh từ trà', gift: 'Gift set' }[p.type]}</p><h3 class="pcard-name"><a href="${p.url}">${esc(p.name)}</a></h3>
      <p class="pcard-taste">${esc(p.taste)}</p><div class="pcard-foot"><span class="price">${vnd(p.price)}</span><button class="btn btn-sm" data-add="${p.sku}" data-name="${esc(p.name)}">Thêm vào giỏ</button></div></div></article>`).join('')
      : '<p class="muted">Chưa có sản phẩm phù hợp với tiêu chí của bạn.</p>';
    $('prodAll').innerHTML = pick.length > 1 ? `<button class="btn btn-secondary" id="addAll">Thêm tất cả gợi ý vào giỏ</button>` : '';
    if (pick.length > 1) $('addAll').onclick = () => addMany(pick.map(p => ({ sku: p.sku, qty: 1 })));
    if (window.bindAdd) bindAdd($('prods'));
  }
  function renderGroups(ranked) {
    const sc = {}; ranked.forEach(r => sc[r.g.id] = Math.round(r.score));
    $('groups').innerHTML = DNA.groups.map(g => `<button class="gcard ${g.id === prof.group ? 'current' : ''}" style="--gc:${g.color}" data-g="${g.id}" aria-pressed="${g.id === prof.group}">
      <b>${esc(g.name)}</b><span>${esc(g.desc)}</span>${g.id === prof.group ? '<em>Gu của bạn</em>' : `<small>${sc[g.id] ?? '—'}% gần</small>`}</button>`).join('');
    $('groups').querySelectorAll('[data-g]').forEach(b => b.onclick = () => {
      const g = G(b.dataset.g);
      $('groupDetail').hidden = false;
      $('groupDetail').innerHTML = `<h3>${esc(g.name)} – ${esc(g.tagline)}</h3><p>${esc(g.desc)}</p>
        <p class="small">Hồ sơ vị tham chiếu: ${DNA.axes.map((a, i) => `${a.label} ${g.proto[i]}`).join(' · ')}</p>
        ${g.id !== prof.group ? `<button class="btn btn-sm btn-secondary" id="useG">Dùng gu này làm gợi ý</button>` : '<p class="small muted">Đây là gu hiện tại của bạn.</p>'}
        ${prof.manualGroup ? `<button class="btn btn-sm btn-ghost" id="autoG">Quay về gu theo bài test</button>` : ''}`;
      const u = $('useG'); if (u) u.onclick = () => { prof.manualGroup = g.id; prof.group = g.id; prof.second = null; ls.set(KP, prof); render(); scrollTo({ top: 0, behavior: 'smooth' }); };
      const a = $('autoG'); if (a) a.onclick = () => { prof.manualGroup = null; ls.set(KP, prof); render(); };
    });
  }

  /* ----- chia sẻ ----- */
  $('shareBtn').onclick = () => {
    const g = G(prof.group);
    const text = `Tea DNA của mình là ${g.name} – ${g.tagline}. ${g.desc} Khám phá gu trà của bạn tại Trồng vị Trà:`;
    const url = location.origin + '/tea-dna';
    $('dlgBody').innerHTML = `<h3 id="dlgTitle">Chia sẻ kết quả</h3><p class="small muted">Xem trước nội dung – không kèm email, thành phần muốn tránh hay câu trả lời.</p>
      <blockquote class="wish-quote">${esc(text)} ${url}</blockquote>
      <label class="check"><input type="checkbox" id="shScore"> Kèm điểm 5 trục trong ảnh</label>
      <div class="cta-row">${navigator.share ? '<button class="btn btn-sm" id="shNative">Chia sẻ qua thiết bị</button>' : ''}
        <button class="btn btn-sm btn-secondary" id="shCopy">Sao chép nội dung</button><button class="btn btn-sm btn-secondary" id="shImg">Tải thẻ ảnh</button>
        <button class="btn btn-sm btn-ghost" id="shClose">Đóng</button></div>`;
    const close = modal($('dlg'), $('shClose'), $('shareBtn'));
    if ($('shNative')) $('shNative').onclick = () => navigator.share({ title: 'Tea DNA', text, url }).catch(() => { });
    $('shCopy').onclick = () => copyText(text + ' ' + url);
    $('shImg').onclick = () => downloadCard(g, $('shScore').checked);
  };
  function downloadCard(g, withScore) {
    try {
      const c = document.createElement('canvas'); c.width = 1080; c.height = 1350; const x = c.getContext('2d');
      x.fillStyle = '#2F3B2A'; x.fillRect(0, 0, 1080, 1350);
      x.fillStyle = g.color; x.globalAlpha = .5; x.beginPath(); x.arc(980, 120, 300, 0, 7); x.fill(); x.globalAlpha = 1;
      x.fillStyle = '#EDD4AB'; x.font = '600 34px "Be Vietnam Pro", Arial'; x.fillText('MY TEA DNA', 90, 200);
      x.fillStyle = '#FAF7F0'; x.font = '600 120px Lora, Georgia, serif'; x.fillText(g.name, 90, 360);
      x.font = 'italic 500 48px Lora, Georgia, serif'; x.fillText(g.tagline, 90, 440);
      x.font = '400 40px "Be Vietnam Pro", Arial'; wrap(x, g.desc, 90, 540, 900, 56);
      if (withScore) DNA.axes.forEach((a, i) => { const v = prof.axes[a.key]; const y = 720 + i * 90;
        x.fillStyle = '#EDD4AB'; x.font = '500 34px "Be Vietnam Pro", Arial'; x.fillText(a.label + (v === null ? ': —' : `: ${v}/100`), 90, y);
        x.fillStyle = 'rgba(255,255,255,.2)'; x.fillRect(90, y + 18, 900, 12); if (v !== null) { x.fillStyle = '#8C9A4B'; x.fillRect(90, y + 18, 9 * v, 12); } });
      x.fillStyle = '#EDD4AB'; x.font = '500 34px "Be Vietnam Pro", Arial'; x.fillText('Trồng vị Trà × Hằng Sơn Điền · Explore Tea. Create Your Way.', 90, 1260);
      const a = document.createElement('a'); a.download = 'tea-dna-' + g.id + '.png'; a.href = c.toDataURL('image/png'); a.click();
    } catch (e) { toast('Không tạo được ảnh. Bạn có thể sao chép nội dung thay thế.', 'error'); }
  }
  function wrap(x, t, X, Y, W, L) { let line = ''; t.split(' ').forEach(w => { if (x.measureText(line + w).width > W) { x.fillText(line, X, Y); Y += L; line = ''; } line += w + ' '; }); x.fillText(line, X, Y); }

  /* ----- làm lại / xóa ----- */
  $('redoBtn').onclick = () => {
    $('dlgBody').innerHTML = `<h3 id="dlgTitle">Làm lại bài test</h3>${prof.override ? '<p class="small">Lưu ý: điều chỉnh thủ công sẽ được thay bằng kết quả mới.</p>' : ''}
      <div class="cta-row"><a class="btn btn-sm" href="/tea-dna?giu=1">Giữ câu trả lời để sửa</a><button class="btn btn-sm btn-secondary" id="rdNew">Bắt đầu mới</button><button class="btn btn-sm btn-ghost" id="rdCancel">Hủy</button></div>`;
    modal($('dlg'), $('rdCancel'), $('redoBtn'));
    $('rdNew').onclick = () => { ls.del(KD); location.href = '/tea-dna'; };
  };
  $('delBtn').onclick = () => {
    $('dlgBody').innerHTML = `<h3 id="dlgTitle">Bạn muốn xóa hồ sơ Tea DNA trên thiết bị này?</h3><p class="small muted">Chỉ xóa câu trả lời, điểm và điều chỉnh Tea DNA. Giỏ hàng và đơn hàng không bị ảnh hưởng.</p>
      <div class="cta-row"><button class="btn btn-sm btn-secondary" id="dlCancel">Hủy</button><button class="btn btn-sm btn-danger" id="dlYes">Xóa hồ sơ</button></div>`;
    modal($('dlg'), $('dlCancel'), $('delBtn'));
    $('dlYes').onclick = () => { ls.del(KP); ls.del(KD); try { sessionStorage.removeItem(KP); } catch (e) { } location.reload(); };
  };
  window.addEventListener('storage', e => { if (e.key === KP && !e.newValue) location.reload(); });
  render();
})();
