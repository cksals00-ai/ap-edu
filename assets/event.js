/* 체험단 신청 폼 → Supabase edu_event_applications (insert 전용, 공개 키만 사용) */
(function () {
  var f = document.getElementById('apply'); if (!f) return;
  var cfg = window.EVENT_CFG || {}; var msg = f.querySelector('.form-msg'); var btn = f.querySelector('button[type=submit]');
  if (!cfg.url || !cfg.anon || !window.supabase) { msg.textContent = f.dataset.err; msg.classList.add('err'); btn.disabled = true; return; }
  var sb = window.supabase.createClient(cfg.url, cfg.anon, { auth: { persistSession: false } });
  if (f.dataset.open && new Date().toISOString().slice(0, 10) < f.dataset.open) { f.classList.add('closed'); btn.disabled = true; btn.textContent = btn.dataset.soon || btn.textContent; }
  f.addEventListener('submit', async function (e) {
    e.preventDefault(); msg.className = 'form-msg'; msg.textContent = '…'; btn.disabled = true;
    var d = new FormData(f); var v = function (k) { var x = (d.get(k) || '').toString().trim(); return x || null; };
    var row = { event: f.dataset.event, lang: f.dataset.lang, name: v('name'), email: v('email'), learner: v('learner'), age_band: v('age_band'), country: v('country'), device: v('device'), channel: v('channel'), note: v('note'), consent: !!d.get('consent') };
    var r = await sb.from('edu_event_applications').insert(row);
    if (r.error) { msg.textContent = /too_many/.test(r.error.message) ? f.dataset.many : f.dataset.err; msg.classList.add('err'); btn.disabled = false; return; }
    msg.textContent = f.dataset.ok; f.reset(); btn.disabled = false;
  });
})();
