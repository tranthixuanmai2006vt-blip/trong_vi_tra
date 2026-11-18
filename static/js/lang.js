/* Chuyển ngôn ngữ Việt / English / 繁體中文 (Đài Loan).
   Bản gốc là tiếng Việt; EN và 繁中 dùng Google Dịch tự động (dịch máy). */
(function () {
  const LANGS = { vi: 'VI', en: 'EN', 'zh-TW': '繁中' };
  const BRANDS = ['Trồng Vị Nhà', 'Hằng Sơn Điền', 'Tea DNA'];
  const m = document.cookie.match(/(?:^|;\s*)googtrans=\/vi\/([^;]+)/);
  const cur = m && LANGS[decodeURIComponent(m[1])] ? decodeURIComponent(m[1]) : 'vi';

  function setCookie(v) {
    const host = location.hostname, exp = v ? '' : ';expires=Thu, 01 Jan 1970 00:00:00 GMT';
    const val = v ? '/vi/' + v : '';
    document.cookie = `googtrans=${val};path=/${exp}`;
    if (host.includes('.')) document.cookie = `googtrans=${val};path=/;domain=.${host}${exp}`;
  }
  window.setSiteLang = code => {
    if (code === cur) return;
    try { localStorage.setItem('tvn_lang', code); } catch (e) { }
    setCookie(code === 'vi' ? null : code);
    location.reload();
  };

  // nút chọn ngôn ngữ
  document.querySelectorAll('[data-lang-switch]').forEach(box => {
    const btn = box.querySelector('[data-lang-btn]'), menu = box.querySelector('[data-lang-menu]');
    if (btn) btn.querySelector('b').textContent = LANGS[cur];
    box.querySelectorAll('[data-lang]').forEach(a => {
      a.classList.toggle('on', a.dataset.lang === cur); a.setAttribute('aria-current', a.dataset.lang === cur);
      a.addEventListener('click', e => { e.preventDefault(); window.setSiteLang(a.dataset.lang); });
    });
    if (btn && menu) {
      btn.addEventListener('click', e => { e.stopPropagation(); const o = menu.hidden; menu.hidden = !o; btn.setAttribute('aria-expanded', o); });
      document.addEventListener('click', e => { if (!box.contains(e.target)) { menu.hidden = true; btn.setAttribute('aria-expanded', false); } });
      document.addEventListener('keydown', e => { if (e.key === 'Escape') { menu.hidden = true; btn.setAttribute('aria-expanded', false); } });
    }
  });
  if (cur === 'vi') return;

  // giữ nguyên tên thương hiệu khi dịch
  // gồm cả khoảng trắng hai bên để bản dịch không dính chữ; không phân biệt hoa thường (vd. TRỒNG VỊ NHÀ)
  const re = new RegExp('(\\s?(?:' + BRANDS.sort((a, b) => b.length - a.length).join('|') + ')\\s?)', 'gi');
  const walk = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, {
    acceptNode: n => (re.lastIndex = 0, re.test(n.nodeValue)) && !n.parentElement.closest('script,style,textarea,.notranslate') ? NodeFilter.FILTER_ACCEPT : NodeFilter.FILTER_REJECT });
  const nodes = []; while (walk.nextNode()) nodes.push(walk.currentNode);
  nodes.forEach(n => {
    re.lastIndex = 0;
    const f = document.createDocumentFragment();
    n.nodeValue.split(re).forEach((part, i) => {
      if (i % 2) { const s = document.createElement('span'); s.className = 'notranslate'; s.translate = false; s.textContent = part; f.appendChild(s); }
      else if (part) f.appendChild(document.createTextNode(part));
    });
    n.replaceWith(f);
  });
  document.documentElement.lang = cur;
  document.documentElement.classList.add('is-translated');
  const holder = document.createElement('div'); holder.id = 'gtEl'; holder.hidden = true; document.body.appendChild(holder);
  window.gtInit = () => new google.translate.TranslateElement({ pageLanguage: 'vi', includedLanguages: 'en,zh-TW', autoDisplay: false }, 'gtEl');
  const s = document.createElement('script'); s.src = 'https://translate.google.com/translate_a/element.js?cb=gtInit'; s.async = true;
  s.onerror = () => { if (window.toast) toast('Chưa tải được bản dịch. Vui lòng kiểm tra kết nối và thử lại.', 'error'); };
  document.body.appendChild(s);
})();
