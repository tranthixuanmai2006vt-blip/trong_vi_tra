/* Thanh gạch chân menu trượt theo mục đang trỏ / đang mở, và trượt từ trang cũ sang trang mới */
(function () {
  const nav = document.getElementById('nav'), ink = document.getElementById('navInk');
  if (!nav || !ink) return;
  const mq = matchMedia('(min-width: 1024px)');
  const items = [...nav.querySelectorAll(':scope > a:not(.nav-mobile-only), :scope > .dd')];
  const active = items.find(i => i.classList.contains('active'));
  const KEY = 'tvn_nav_ink';
  function box(el) {
    const t = el.classList.contains('dd') ? (el.querySelector('.dd-product-heading') || el.querySelector('.dd-btn')) : el;
    const n = nav.getBoundingClientRect(), r = t.getBoundingClientRect();
    return { x: r.left - n.left + 8, w: Math.max(0, r.width - 16) };
  }
  function set(b, instant) {
    if (instant) ink.classList.add('no-anim');
    if (b) { ink.style.width = b.w + 'px'; ink.style.transform = `translateX(${b.x}px)`; ink.style.opacity = 1; }
    else ink.style.opacity = 0;
    if (instant) { void ink.offsetWidth; ink.classList.remove('no-anim'); }
  }
  const place = (el, instant) => set(mq.matches && el ? box(el) : null, instant);

  // trang mới: bắt đầu từ vị trí gạch chân của trang trước rồi trượt tới mục hiện tại
  let from = null;
  try { const s = JSON.parse(sessionStorage.getItem(KEY) || 'null'); if (s && Date.now() - s.t < 4000) from = s; sessionStorage.removeItem(KEY); } catch (e) { }
  if (from && mq.matches && !matchMedia('(prefers-reduced-motion: reduce)').matches) {
    set(from.on ? from : null, true);
    requestAnimationFrame(() => requestAnimationFrame(() => place(active)));
  } else place(active, true);

  items.forEach(el => el.addEventListener('mouseenter', () => place(el)));
  nav.addEventListener('mouseleave', () => place(active));
  nav.addEventListener('focusin', e => { const el = items.find(i => i.contains(e.target)); if (el) place(el); });
  nav.addEventListener('focusout', () => setTimeout(() => { if (!nav.contains(document.activeElement)) place(active); }, 0));
  const keep = () => {
    try {
      const m = /translateX\(([-\d.]+)px\)/.exec(ink.style.transform || '');
      sessionStorage.setItem(KEY, JSON.stringify({ x: m ? +m[1] : 0, w: parseFloat(ink.style.width) || 0, on: ink.style.opacity !== '0', t: Date.now() }));
    } catch (e) { }
  };
  // bấm mục menu: gạch chân trượt ngay tới mục đó trước khi rời trang
  nav.addEventListener('click', e => { const a = e.target.closest('a'); if (!a) return; const el = items.find(i => i.contains(a)); if (el) place(el); });
  addEventListener('pagehide', keep);
  addEventListener('resize', () => place(active, true));
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(() => place(active, true));
})();
