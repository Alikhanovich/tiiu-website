'use strict';

/* ═══ CSRF & API ═══════════════════════════════════════════════════════ */
function getCsrf() {
  const m = document.cookie.match(/csrftoken=([^;]+)/);
  return m ? m[1] : '';
}

async function api(url, opts = {}) {
  const headers = { 'X-CSRFToken': getCsrf(), ...(opts.headers || {}) };
  let body = opts.body;
  if (opts.json !== undefined) {
    headers['Content-Type'] = 'application/json';
    body = JSON.stringify(opts.json);
  }
  try {
    const res = await fetch(url, { method: opts.method || 'GET', headers, body, credentials: 'same-origin' });
    return res.json();
  } catch {
    return { success: false, error: 'Tarmoq xatosi' };
  }
}

/* ═══ Toast ════════════════════════════════════════════════════════════ */
function toast(msg, type = 'success') {
  const el = document.getElementById('toast');
  el.textContent = msg;
  el.className = `toast ${type}`;
  clearTimeout(el._t);
  el._t = setTimeout(() => el.classList.add('hidden'), 3200);
}

/* ═══ Confirm modal ════════════════════════════════════════════════════ */
let _confirmResolve = null;
function confirmAction(text) {
  return new Promise(resolve => {
    _confirmResolve = resolve;
    document.getElementById('confirm-text').textContent = text;
    document.getElementById('confirm-modal').classList.remove('hidden');
  });
}
document.getElementById('confirm-cancel').addEventListener('click', () => {
  document.getElementById('confirm-modal').classList.add('hidden');
  if (_confirmResolve) _confirmResolve(false);
});
document.getElementById('confirm-ok').addEventListener('click', () => {
  document.getElementById('confirm-modal').classList.add('hidden');
  if (_confirmResolve) _confirmResolve(true);
});

/* ═══ Helpers ══════════════════════════════════════════════════════════ */
function esc(s) {
  return String(s ?? '').replace(/&/g,'&amp;').replace(/"/g,'&quot;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
}

function previewImg(input, previewId) {
  const file = input.files[0];
  if (!file) return;
  const reader = new FileReader();
  reader.onload = e => {
    let el = document.getElementById(previewId);
    if (!el) return;
    if (el.tagName === 'IMG') { el.src = e.target.result; }
    else {
      const img = document.createElement('img');
      img.src = e.target.result;
      img.className = 'img-thumb-preview';
      img.id = previewId;
      el.replaceWith(img);
    }
  };
  reader.readAsDataURL(file);
}

/* ═══ Page configs ═════════════════════════════════════════════════════ */
const PAGES = {
  dashboard: { title: 'Dashboard', special: 'dashboard' },
  settings:  { title: 'Sayt sozlamalari', special: 'settings' },

  sliders: {
    title: 'Sliderlar', endpoint: '/panel/api/sliders/',
    cols: [
      { key: 'image',     label: 'Rasm',    img: true },
      { key: 'title',     label: 'Sarlavha' },
      { key: 'order',     label: 'Tartib' },
      { key: 'is_active', label: 'Holat',   bool: true },
    ],
    fields: [
      { n: 'title',     l: 'Sarlavha',        t: 'text', req: true },
      { n: 'subtitle',  l: 'Kichik sarlavha', t: 'text' },
      { n: 'btn_text',  l: 'Tugma matni',     t: 'text' },
      { n: 'btn_url',   l: 'Tugma URL',       t: 'text' },
      { n: 'order',     l: 'Tartib',          t: 'number' },
      { n: 'is_active', l: 'Faol',            t: 'toggle', def: true },
      { n: 'image',     l: 'Rasm',            t: 'image' },
    ],
  },

  faculty: {
    title: "Yo'nalishlar", endpoint: '/panel/api/faculty/',
    cols: [
      { key: 'image',      label: 'Rasm',   img: true },
      { key: 'name',       label: 'Nomi' },
      { key: 'short_name', label: 'Qisqa' },
      { key: 'degree',     label: 'Daraja' },
      { key: 'is_active',  label: 'Holat',  bool: true },
    ],
    fields: [
      { n: 'name',        l: 'Nomi',             t: 'text', req: true },
      { n: 'short_name',  l: 'Qisqa nomi',       t: 'text' },
      { n: 'icon',        l: 'Ikonka (emoji)',   t: 'text' },
      { n: 'description', l: 'Tavsif',           t: 'textarea' },
      { n: 'degree', l: 'Daraja', t: 'select', opts: [
        { v: 'bachelor', lbl: 'Bakalavr' },
        { v: 'master',   lbl: 'Magistr' },
        { v: 'both',     lbl: 'Ikkalasi' },
      ]},
      { n: 'study_forms', l: "O'qish shakllari", t: 'text' },
      { n: 'duration',    l: 'Davomiyligi (yil)',t: 'number' },
      { n: 'order',       l: 'Tartib',           t: 'number' },
      { n: 'is_active',   l: 'Faol',             t: 'toggle', def: true },
      { n: 'image',       l: 'Rasm',             t: 'image' },
    ],
  },

  teachers: {
    title: "O'qituvchilar", endpoint: '/panel/api/teachers/',
    cols: [
      { key: 'photo',        label: 'Foto',    img: true },
      { key: 'full_name',    label: 'F.I.O.' },
      { key: 'position',     label: 'Lavozim' },
      { key: 'kafedra_name', label: 'Kafedra' },
      { key: 'is_active',    label: 'Holat',   bool: true },
    ],
    fields: [
      { n: 'full_name',  l: 'F.I.O.',       t: 'text', req: true },
      { n: 'position',   l: 'Lavozim',      t: 'text' },
      { n: 'kafedra_id', l: 'Kafedra',      t: 'select', loadFrom: '/panel/api/departments-select/' },
      { n: 'bio',        l: 'Bio',          t: 'textarea' },
      { n: 'email',      l: 'Email',        t: 'text' },
      { n: 'phone',      l: 'Telefon',      t: 'text' },
      { n: 'linkedin',   l: 'LinkedIn',     t: 'text' },
      { n: 'experience', l: 'Tajriba (yil)',t: 'number' },
      { n: 'order',      l: 'Tartib',       t: 'number' },
      { n: 'is_active',  l: 'Faol',         t: 'toggle', def: true },
      { n: 'photo',      l: 'Foto',         t: 'image' },
    ],
  },

  departments: {
    title: 'Kafedralar', endpoint: '/panel/api/departments/',
    cols: [
      { key: 'name',      label: 'Nomi' },
      { key: 'head',      label: 'Mudiri' },
      { key: 'order',     label: 'Tartib' },
      { key: 'is_active', label: 'Holat', bool: true },
    ],
    fields: [
      { n: 'name',        l: 'Nomi',   t: 'text', req: true },
      { n: 'head',        l: 'Mudiri', t: 'text' },
      { n: 'description', l: 'Tavsif', t: 'textarea' },
      { n: 'order',       l: 'Tartib', t: 'number' },
      { n: 'is_active',   l: 'Faol',   t: 'toggle', def: true },
      { n: 'image',       l: 'Rasm',   t: 'image' },
    ],
  },

  leadership: {
    title: 'Rahbariyat', endpoint: '/panel/api/leadership/',
    cols: [
      { key: 'photo',     label: 'Foto',    img: true },
      { key: 'full_name', label: 'F.I.O.' },
      { key: 'position',  label: 'Lavozim' },
      { key: 'rank',      label: 'Unvon' },
      { key: 'is_active', label: 'Holat',   bool: true },
    ],
    fields: [
      { n: 'full_name',      l: 'F.I.O.',         t: 'text', req: true },
      { n: 'rank',           l: 'Unvon',           t: 'text' },
      { n: 'position',       l: 'Lavozim',         t: 'text' },
      { n: 'qualification',  l: 'Malaka',          t: 'text' },
      { n: 'bio',            l: 'Bio',             t: 'textarea' },
      { n: 'email',          l: 'Email',           t: 'text' },
      { n: 'phone',          l: 'Telefon',         t: 'text' },
      { n: 'reception_days', l: 'Qabul kunlari',   t: 'text' },
      { n: 'reception_time', l: 'Qabul vaqti',     t: 'text' },
      { n: 'order',          l: 'Tartib',          t: 'number' },
      { n: 'is_active',      l: 'Faol',            t: 'toggle', def: true },
      { n: 'photo',          l: 'Foto',            t: 'image' },
    ],
  },

  centers: {
    title: 'Markazlar', endpoint: '/panel/api/centers/',
    cols: [
      { key: 'name',      label: 'Nomi' },
      { key: 'head',      label: 'Rahbar' },
      { key: 'order',     label: 'Tartib' },
      { key: 'is_active', label: 'Holat', bool: true },
    ],
    fields: [
      { n: 'name',       l: 'Nomi',              t: 'text', req: true },
      { n: 'icon',       l: 'Ikonka (emoji)',    t: 'text' },
      { n: 'head',       l: 'Rahbar',            t: 'text' },
      { n: 'head_role',  l: 'Rahbar lavozimi',   t: 'text' },
      { n: 'head_phone', l: 'Rahbar telefoni',   t: 'text' },
      { n: 'head_email', l: 'Rahbar emaili',     t: 'text' },
      { n: 'work_hours', l: 'Ish vaqti',         t: 'text' },
      { n: 'description',l: 'Tavsif',            t: 'textarea' },
      { n: 'order',      l: 'Tartib',            t: 'number' },
      { n: 'is_active',  l: 'Faol',              t: 'toggle', def: true },
      { n: 'image',      l: 'Rasm',              t: 'image' },
    ],
  },

  /* ── News & Events use full detail pages ─── */
  news: {
    title: 'Yangiliklar', endpoint: '/panel/api/news/', hasDetail: true, hasImages: true,
    cols: [
      { key: 'image',         label: 'Rasm',       img: true },
      { key: 'title',         label: 'Sarlavha' },
      { key: 'category_name', label: 'Kategoriya' },
      { key: 'is_active',     label: 'Holat',      bool: true },
      { key: 'created_at',    label: 'Sana' },
    ],
    fields: [
      { n: 'title',       l: 'Sarlavha',    t: 'text', req: true },
      { n: 'category_id', l: 'Kategoriya',  t: 'select', loadFrom: '/panel/api/news-categories/' },
      { n: 'author',      l: 'Muallif',     t: 'text' },
      { n: 'is_active',   l: 'Faol',        t: 'toggle', def: true },
      { n: 'is_featured', l: 'Tanlangan',   t: 'toggle', def: false },
      { n: 'short_text',  l: 'Qisqa matn',  t: 'textarea', rows: 3 },
      { n: 'body',        l: 'Asosiy matn', t: 'textarea', rows: 10 },
      { n: 'image',       l: 'Muqova rasmi',t: 'image' },
    ],
  },

  events: {
    title: 'Tadbirlar', endpoint: '/panel/api/events/', hasDetail: true, hasImages: true,
    cols: [
      { key: 'image',      label: 'Rasm', img: true },
      { key: 'title',      label: 'Sarlavha' },
      { key: 'location',   label: 'Joy' },
      { key: 'event_date', label: 'Sana' },
      { key: 'is_active',  label: 'Holat', bool: true },
    ],
    fields: [
      { n: 'title',       l: 'Sarlavha',     t: 'text', req: true },
      { n: 'location',    l: 'Joy',          t: 'text' },
      { n: 'event_date',  l: 'Sana va vaqt', t: 'datetime-local', req: true },
      { n: 'is_active',   l: 'Faol',         t: 'toggle', def: true },
      { n: 'description', l: 'Tavsif',       t: 'textarea', rows: 8 },
      { n: 'image',       l: 'Muqova rasmi', t: 'image' },
    ],
  },

  faq: {
    title: 'FAQ', endpoint: '/panel/api/faqs/', useJSON: true,
    cols: [
      { key: 'question', label: 'Savol' },
      { key: 'order',    label: 'Tartib' },
      { key: 'is_active',label: 'Holat', bool: true },
    ],
    fields: [
      { n: 'question', l: 'Savol',  t: 'text',     req: true },
      { n: 'answer',   l: 'Javob',  t: 'textarea', rows: 5, req: true },
      { n: 'order',    l: 'Tartib', t: 'number' },
      { n: 'is_active',l: 'Faol',   t: 'toggle', def: true },
    ],
  },

  partners: {
    title: 'Hamkorlar', endpoint: '/panel/api/partners/',
    cols: [
      { key: 'logo',      label: 'Logo',    img: true },
      { key: 'name',      label: 'Nomi' },
      { key: 'website',   label: 'Vebsayt' },
      { key: 'is_active', label: 'Holat',   bool: true },
    ],
    fields: [
      { n: 'name',      l: 'Nomi',     t: 'text', req: true },
      { n: 'website',   l: 'Vebsayt',  t: 'text' },
      { n: 'order',     l: 'Tartib',   t: 'number' },
      { n: 'is_active', l: 'Faol',     t: 'toggle', def: true },
      { n: 'logo',      l: 'Logo',     t: 'image' },
    ],
  },

  pages: {
    title: 'Statik Sahifalar', endpoint: '/panel/api/pages/', hasDetail: true,
    cols: [
      { key: 'title',      label: 'Sarlavha' },
      { key: 'slug',       label: 'URL Slug' },
      { key: 'updated_at', label: 'Yangilangan' },
      { key: 'is_active',  label: 'Holat', bool: true },
    ],
    fields: [],
  },

  messages: {
    title: 'Xabarlar', endpoint: '/panel/api/messages/', readOnly: true,
    cols: [
      { key: 'name',       label: 'Ism' },
      { key: 'phone',      label: 'Telefon' },
      { key: 'direction',  label: "Yo'nalish" },
      { key: 'status',     label: 'Holat',  status: true },
      { key: 'created_at', label: 'Sana' },
    ],
  },

  /* ── NEW CONTENT MODELS ─────────────────────────────────────────────── */
  article_categories: {
    title: 'Maqola kategoriyalari', endpoint: '/panel/api/article-categories/', useJSON: true,
    cols: [
      { key: 'name',      label: 'Nomi' },
      { key: 'slug',      label: 'Slug' },
      { key: 'is_active', label: 'Holat', bool: true },
    ],
    fields: [
      { n: 'name',      l: 'Nomi', t: 'text', req: true },
      { n: 'is_active', l: 'Faol', t: 'toggle', def: true },
    ],
  },

  articles: {
    title: 'Ilmiy maqolalar', endpoint: '/panel/api/articles/',
    cols: [
      { key: 'title',         label: 'Sarlavha' },
      { key: 'authors',       label: 'Mualliflar' },
      { key: 'category_name', label: 'Kategoriya' },
      { key: 'published_date',label: 'Sana' },
      { key: 'is_active',     label: 'Holat', bool: true },
    ],
    fields: [
      { n: 'title',          l: 'Sarlavha',      t: 'text', req: true },
      { n: 'authors',        l: 'Mualliflar',    t: 'text' },
      { n: 'journal_name',   l: 'Jurnal nomi',   t: 'text' },
      { n: 'category_id',    l: 'Kategoriya',    t: 'select', loadFrom: '/panel/api/article-categories-select/' },
      { n: 'language', l: 'Til', t: 'select', opts: [
        { v: 'uz', lbl: "O'zbek" }, { v: 'ru', lbl: 'Rus' }, { v: 'en', lbl: 'Ingliz' },
      ]},
      { n: 'published_date', l: 'Chiqarilgan sana', t: 'date' },
      { n: 'doi_url',        l: 'DOI URL',        t: 'text' },
      { n: 'abstract',       l: 'Annotatsiya',    t: 'textarea', rows: 5 },
      { n: 'is_active',      l: 'Faol',           t: 'toggle', def: true },
      { n: 'cover_image',    l: 'Muqova rasmi',   t: 'image' },
      { n: 'pdf_file',       l: 'PDF fayl',       t: 'file' },
    ],
  },

  dissertations: {
    title: 'Dissertatsiyalar', endpoint: '/panel/api/dissertations/',
    cols: [
      { key: 'title',        label: 'Mavzu' },
      { key: 'author',       label: 'Muallif' },
      { key: 'degree',       label: 'Daraja' },
      { key: 'defense_date', label: 'Himoya sana' },
      { key: 'is_active',    label: 'Holat', bool: true },
    ],
    fields: [
      { n: 'title',       l: 'Mavzu',         t: 'text', req: true },
      { n: 'author',      l: 'Muallif',       t: 'text', req: true },
      { n: 'supervisor',  l: 'Ilmiy rahbar',  t: 'text' },
      { n: 'specialty',   l: 'Mutaxassislik', t: 'text' },
      { n: 'degree', l: 'Daraja', t: 'select', opts: [
        { v: 'phd',       lbl: 'PhD' },
        { v: 'dsc',       lbl: 'DSc (Doctor of Science)' },
        { v: 'candidate', lbl: 'Fan nomzodi' },
      ]},
      { n: 'faculty_id',   l: "Yo'nalish",    t: 'select', loadFrom: '/panel/api/faculty-select/' },
      { n: 'defense_date', l: 'Himoya sanasi',t: 'date' },
      { n: 'abstract',     l: 'Annotatsiya',  t: 'textarea', rows: 5 },
      { n: 'is_active',    l: 'Faol',         t: 'toggle', def: true },
      { n: 'cover_image',  l: 'Muqova rasmi', t: 'image' },
      { n: 'pdf_file',     l: 'PDF fayl',     t: 'file' },
    ],
  },

  conferences: {
    title: 'Konferensiyalar', endpoint: '/panel/api/conferences/',
    cols: [
      { key: 'title',      label: 'Sarlavha' },
      { key: 'location',   label: 'Joy' },
      { key: 'start_date', label: 'Boshlanish' },
      { key: 'is_active',  label: 'Holat', bool: true },
    ],
    fields: [
      { n: 'title',            l: 'Sarlavha',          t: 'text', req: true },
      { n: 'location',         l: 'Joy',               t: 'text' },
      { n: 'start_date',       l: 'Boshlanish sanasi', t: 'date' },
      { n: 'end_date',         l: 'Tugash sanasi',     t: 'date' },
      { n: 'registration_url', l: "Ro'yxatdan o'tish URL", t: 'text' },
      { n: 'description',      l: 'Tavsif',            t: 'textarea', rows: 5 },
      { n: 'is_active',        l: 'Faol',              t: 'toggle', def: true },
      { n: 'poster_image',     l: 'Poster rasmi',      t: 'image' },
      { n: 'cover_image',      l: 'Muqova rasmi',      t: 'image' },
      { n: 'pdf_file',         l: 'PDF dastur',        t: 'file' },
    ],
  },

  contests: {
    title: 'Tanlovlar', endpoint: '/panel/api/contests/',
    cols: [
      { key: 'title',     label: 'Sarlavha' },
      { key: 'deadline',  label: 'Muddat' },
      { key: 'is_active', label: 'Holat', bool: true },
    ],
    fields: [
      { n: 'title',       l: 'Sarlavha',  t: 'text', req: true },
      { n: 'deadline',    l: 'Muddat',    t: 'date' },
      { n: 'description', l: 'Tavsif',   t: 'textarea', rows: 5 },
      { n: 'is_active',   l: 'Faol',     t: 'toggle', def: true },
      { n: 'cover_image', l: 'Rasm',     t: 'image' },
      { n: 'pdf_file',    l: 'Shartlar (PDF)', t: 'file' },
    ],
  },

  videos: {
    title: 'Video darslar', endpoint: '/panel/api/videos/',
    cols: [
      { key: 'cover_image',  label: 'Rasm', img: true },
      { key: 'title',        label: 'Sarlavha' },
      { key: 'faculty_name', label: "Yo'nalish" },
      { key: 'duration',     label: 'Davomiyligi' },
      { key: 'is_active',    label: 'Holat', bool: true },
    ],
    fields: [
      { n: 'title',       l: 'Sarlavha',     t: 'text', req: true },
      { n: 'youtube_url', l: 'YouTube URL',  t: 'text' },
      { n: 'duration',    l: 'Davomiyligi (masalan: 12:34)', t: 'text' },
      { n: 'faculty_id',  l: "Yo'nalish",    t: 'select', loadFrom: '/panel/api/faculty-select/' },
      { n: 'description', l: 'Tavsif',       t: 'textarea', rows: 4 },
      { n: 'is_active',   l: 'Faol',         t: 'toggle', def: true },
      { n: 'cover_image', l: 'Muqova rasmi', t: 'image' },
    ],
  },

  talented: {
    title: 'Iqtidorli talabalar', endpoint: '/panel/api/talented/',
    cols: [
      { key: 'photo',        label: 'Foto', img: true },
      { key: 'full_name',    label: 'F.I.O.' },
      { key: 'achievement',  label: 'Yutuq' },
      { key: 'year',         label: 'Yil' },
      { key: 'is_active',    label: 'Holat', bool: true },
    ],
    fields: [
      { n: 'full_name',   l: 'F.I.O.',       t: 'text', req: true },
      { n: 'achievement', l: 'Yutuq/unvon',  t: 'text', req: true },
      { n: 'year',        l: 'Yil',          t: 'number' },
      { n: 'faculty_id',  l: "Yo'nalish",    t: 'select', loadFrom: '/panel/api/faculty-select/' },
      { n: 'description', l: "Qo'shimcha ma'lumot", t: 'textarea', rows: 3 },
      { n: 'is_active',   l: 'Faol',         t: 'toggle', def: true },
      { n: 'photo',       l: 'Foto',         t: 'image' },
    ],
  },

  journals: {
    title: 'Ilmiy jurnal sonlari', endpoint: '/panel/api/journals/',
    cols: [
      { key: 'cover_image',  label: 'Muqova', img: true },
      { key: 'title',        label: 'Sarlavha' },
      { key: 'year',         label: 'Yil' },
      { key: 'issue_number', label: 'Son raqami' },
      { key: 'is_active',    label: 'Holat', bool: true },
    ],
    fields: [
      { n: 'title',        l: 'Sarlavha',    t: 'text', req: true },
      { n: 'year',         l: 'Yil',         t: 'number', req: true },
      { n: 'issue_number', l: 'Son raqami',  t: 'number', req: true },
      { n: 'description',  l: 'Tavsif',      t: 'textarea', rows: 4 },
      { n: 'is_active',    l: 'Faol',        t: 'toggle', def: true },
      { n: 'cover_image',  l: 'Muqova rasmi',t: 'image' },
      { n: 'pdf_file',     l: 'PDF fayl',    t: 'file' },
    ],
  },

  schedules: {
    title: 'Dars jadvallari', endpoint: '/panel/api/schedules/',
    cols: [
      { key: 'title',         label: 'Sarlavha' },
      { key: 'faculty_name',  label: "Yo'nalish" },
      { key: 'academic_year', label: "O'quv yili" },
      { key: 'semester',      label: 'Semestr' },
      { key: 'is_active',     label: 'Holat', bool: true },
    ],
    fields: [
      { n: 'title',         l: 'Sarlavha',    t: 'text', req: true },
      { n: 'academic_year', l: "O'quv yili (masalan: 2024-2025)", t: 'text', req: true },
      { n: 'semester', l: 'Semestr', t: 'select', opts: [
        { v: '1', lbl: '1-semestr' }, { v: '2', lbl: '2-semestr' },
      ]},
      { n: 'faculty_id',    l: "Yo'nalish",   t: 'select', loadFrom: '/panel/api/faculty-select/' },
      { n: 'is_active',     l: 'Faol',        t: 'toggle', def: true },
      { n: 'file',          l: 'Jadval fayli',t: 'file', req: true },
    ],
  },

  library: {
    title: 'Elektron kutubxona', endpoint: '/panel/api/library/',
    cols: [
      { key: 'cover_image',    label: 'Muqova', img: true },
      { key: 'title',          label: 'Sarlavha' },
      { key: 'authors',        label: 'Mualliflar' },
      { key: 'resource_type',  label: 'Turi' },
      { key: 'is_active',      label: 'Holat', bool: true },
    ],
    fields: [
      { n: 'title',         l: 'Sarlavha',   t: 'text', req: true },
      { n: 'authors',       l: 'Mualliflar', t: 'text' },
      { n: 'resource_type', l: 'Tur', t: 'select', opts: [
        { v: 'book',    lbl: 'Kitob' },
        { v: 'manual',  lbl: "Qo'llanma" },
        { v: 'article', lbl: 'Maqola' },
        { v: 'thesis',  lbl: 'Dissertatsiya' },
        { v: 'other',   lbl: 'Boshqa' },
      ]},
      { n: 'external_url',  l: 'Tashqi havola', t: 'text' },
      { n: 'description',   l: 'Tavsif',        t: 'textarea', rows: 4 },
      { n: 'is_active',     l: 'Faol',          t: 'toggle', def: true },
      { n: 'cover_image',   l: 'Muqova rasmi',  t: 'image' },
      { n: 'file',          l: 'Fayl (PDF/DOC)',t: 'file' },
    ],
  },
};

/* ═══ State ════════════════════════════════════════════════════════════ */
let _curPage    = 'dashboard';
let _curPageNum = 1;
let _curFilter  = '';

/* ═══ Router ═══════════════════════════════════════════════════════════ */
function parseHash(hash) {
  const path = (hash || '#dashboard').replace(/^#/, '');
  const slash = path.indexOf('/');
  if (slash === -1) return { page: path || 'dashboard', id: null };
  return { page: path.slice(0, slash), id: path.slice(slash + 1) };
}

async function routeTo(hash) {
  const { page, id } = parseHash(hash);
  const cfg = PAGES[page];
  if (!cfg) return;

  _curPage = page;
  document.querySelectorAll('.nav-item').forEach(a => a.classList.toggle('active', a.dataset.page === page));
  document.getElementById('topbar-title').textContent = cfg.title;
  const content = document.getElementById('content');

  if (id && cfg.hasDetail) return renderDetailPage(content, page, cfg, id);
  if (cfg.special === 'dashboard') return renderDashboard(content);
  if (cfg.special === 'settings')  return renderSettings(content);
  if (page === 'messages')         return renderMessages(content);
  return renderList(content, page, cfg, 1);
}

window.addEventListener('hashchange', () => routeTo(location.hash));

/* ═══ Dashboard ════════════════════════════════════════════════════════ */
async function renderDashboard(el) {
  el.innerHTML = '<div class="loader"><div class="spinner"></div></div>';
  const r = await api('/panel/api/stats/');
  if (!r.success) { el.innerHTML = '<p style="padding:24px;color:var(--text2)">Xato</p>'; return; }
  const d = r.data;
  el.innerHTML = `
    <div class="page-head"><h1>Dashboard</h1></div>
    <div class="stats-grid">
      ${sc('Yangiliklar', d.news, '#news', '📰')}
      ${sc("O'qituvchilar", d.teachers, '#teachers', '👨‍🏫')}
      ${sc("Yo'nalishlar", d.faculty, '#faculty', '🎓')}
      ${sc('Yangi xabarlar', d.new_msgs, '#messages', '✉️')}
      ${sc('Tadbirlar', d.events, '#events', '📅')}
      ${sc('Rahbariyat', d.leadership, '#leadership', '👤')}
      ${sc('Kafedralar', d.departments, '#departments', '🏫')}
      ${sc('Markazlar', d.centers, '#centers', '🏢')}
      ${sc('Sahifalar', d.pages, '#pages', '📄')}
    </div>`;
}

function sc(label, val, href, icon) {
  return `<a class="stat-card" href="${href}">
    <div class="stat-icon">${icon}</div>
    <div class="stat-val">${val ?? 0}</div>
    <div class="stat-label">${label}</div>
  </a>`;
}

/* ═══ Settings ═════════════════════════════════════════════════════════ */
async function renderSettings(el) {
  el.innerHTML = '<div class="loader"><div class="spinner"></div></div>';
  const r = await api('/panel/api/settings/');
  if (!r.success) { el.innerHTML = '<p style="padding:24px;color:var(--text2)">Xato</p>'; return; }
  const d = r.data;
  el.innerHTML = `
    <div class="page-head"><h1>Sayt sozlamalari</h1></div>
    <form id="settings-form">
      <div class="form-card">
        <h3>Asosiy</h3>
        <div class="form-grid">
          ${si('site_name', "Sayt nomi (qisqa)", d.site_name)}
          ${si('site_name_full', "Sayt nomi (to'liq)", d.site_name_full)}
          ${si('address', 'Manzil', d.address)}
          ${si('phone1', 'Telefon 1', d.phone1)}
          ${si('phone2', 'Telefon 2', d.phone2)}
          ${si('email', 'Email', d.email)}
          ${si('work_hours', 'Ish vaqti', d.work_hours)}
        </div>
      </div>
      <div class="form-card">
        <h3>Ijtimoiy tarmoqlar</h3>
        <div class="form-grid">
          ${si('facebook', 'Facebook', d.facebook)}
          ${si('instagram', 'Instagram', d.instagram)}
          ${si('telegram', 'Telegram', d.telegram)}
          ${si('youtube', 'YouTube', d.youtube)}
        </div>
      </div>
      <div class="form-card">
        <h3>Statistika</h3>
        <div class="form-grid">
          ${si('founded_year',    'Tashkil etilgan yil',   d.founded_year,    'number')}
          ${si('student_count',   'Talabalar soni',         d.student_count,   'number')}
          ${si('teacher_count',   "O'qituvchilar soni",     d.teacher_count,   'number')}
          ${si('direction_count', "Yo'nalishlar soni",      d.direction_count, 'number')}
        </div>
      </div>
      <div class="form-card">
        <h3>Bosh sahifa</h3>
        <div class="form-grid">
          ${si('hero_title',    'Hero sarlavha',         d.hero_title)}
          ${si('hero_subtitle', 'Hero kichik sarlavha',  d.hero_subtitle)}
        </div>
        <div class="field" style="margin-top:16px">
          <label>Haqida matn</label>
          <textarea name="about_text" rows="5">${esc(d.about_text || '')}</textarea>
        </div>
      </div>
      <div class="form-card">
        <h3>Logotip va Favicon</h3>
        <div class="form-grid">
          <div class="field">
            <label>Logo</label>
            ${d.logo ? `<img src="${d.logo}" class="img-thumb-preview" id="logo-preview" style="max-height:70px;width:auto">` : `<div id="logo-preview" class="img-empty-preview">Rasm yo'q</div>`}
            <input type="file" name="logo" accept="image/*" style="margin-top:6px" onchange="previewImg(this,'logo-preview')">
          </div>
          <div class="field">
            <label>Favicon</label>
            ${d.favicon ? `<img src="${d.favicon}" class="img-thumb-preview" id="favicon-preview" style="max-height:70px;width:auto">` : `<div id="favicon-preview" class="img-empty-preview">Rasm yo'q</div>`}
            <input type="file" name="favicon" accept="image/*" style="margin-top:6px" onchange="previewImg(this,'favicon-preview')">
          </div>
        </div>
      </div>
      <div class="form-actions" style="margin-bottom:40px">
        <button type="submit" class="btn-primary">Saqlash</button>
      </div>
    </form>`;
  document.getElementById('settings-form').addEventListener('submit', async e => {
    e.preventDefault();
    const btn = e.target.querySelector('[type=submit]');
    btn.disabled = true;
    const r = await api('/panel/api/settings/', { method: 'POST', body: new FormData(e.target) });
    btn.disabled = false;
    if (r.success) toast('Saqlandi');
    else toast(r.error || 'Xato', 'error');
  });
}

function si(name, label, value = '', type = 'text') {
  return `<div class="field">
    <label>${esc(label)}</label>
    <input type="${type}" name="${name}" value="${esc(String(value ?? ''))}">
  </div>`;
}

/* ═══ List page ════════════════════════════════════════════════════════ */
async function renderList(el, page, cfg, pageNum = 1) {
  el.innerHTML = '<div class="loader"><div class="spinner"></div></div>';
  const r = await api(`${cfg.endpoint}?page=${pageNum}`);
  if (!r.success) { el.innerHTML = '<p style="padding:24px;color:var(--text2)">Xato</p>'; return; }
  _curPageNum = pageNum;

  const addAction = cfg.hasDetail
    ? `<a class="btn-primary" href="#${page}/new">+ Qo'shish</a>`
    : `<button class="btn-primary" id="add-btn">+ Qo'shish</button>`;

  el.innerHTML = `
    <div class="page-head">
      <h1>${cfg.title}</h1>
      ${cfg.readOnly ? '' : addAction}
    </div>
    <div class="table-wrap">
      <table>
        <thead><tr>
          ${cfg.cols.map(c => `<th>${c.label}</th>`).join('')}
          ${cfg.readOnly ? '' : '<th style="width:160px">Amallar</th>'}
        </tr></thead>
        <tbody>
          ${r.data.length
            ? r.data.map(row => buildRow(row, cfg, page)).join('')
            : `<tr><td colspan="${cfg.cols.length + 1}"><div class="empty-state">Ma'lumot topilmadi</div></td></tr>`}
        </tbody>
      </table>
    </div>
    ${buildPagination(pageNum, r.pages || 1)}`;

  if (!cfg.readOnly && !cfg.hasDetail) {
    document.getElementById('add-btn').addEventListener('click', () => openForm(page, cfg, null));
    el.querySelectorAll('.btn-edit').forEach(btn => {
      const item = r.data.find(x => String(x.id) === btn.dataset.id);
      btn.addEventListener('click', () => openForm(page, cfg, item));
    });
  }

  el.querySelectorAll('.btn-del').forEach(btn => {
    btn.addEventListener('click', async () => {
      const ok = await confirmAction("Bu yozuv o'chiriladi. Davom etasizmi?");
      if (!ok) return;
      const dr = await api(`${cfg.endpoint}${btn.dataset.id}/`, { method: 'DELETE' });
      if (dr.success) { toast("O'chirildi"); renderList(el, page, cfg, _curPageNum); }
      else toast(dr.error || 'Xato', 'error');
    });
  });

  el.querySelectorAll('.pg-btn').forEach(btn => {
    btn.addEventListener('click', () => renderList(el, page, cfg, +btn.dataset.p));
  });
}

function buildRow(row, cfg, page) {
  const cells = cfg.cols.map(c => {
    if (c.img) {
      const src = row[c.key];
      return `<td>${src ? `<img src="${src}" class="thumb">` : '—'}</td>`;
    }
    if (c.bool) {
      const on = row[c.key];
      return `<td><span class="badge-active ${on ? 'yes' : 'no'}">${on ? 'Faol' : 'Nofaol'}</span></td>`;
    }
    if (c.status) {
      const s = row[c.key];
      const lbl = { new: 'Yangi', read: "O'qilgan", answered: 'Javob berilgan' };
      return `<td><span class="status-badge status-${s}">${lbl[s] || s}</span></td>`;
    }
    const v = row[c.key];
    return `<td>${v != null ? esc(String(v)).substring(0, 60) : '—'}</td>`;
  }).join('');

  if (cfg.readOnly) return `<tr class="row-clickable" data-id="${row.id}">${cells}</tr>`;

  if (cfg.hasDetail) {
    return `<tr>${cells}<td class="tbl-actions">
      <a class="btn-edit" href="#${page}/${row.id}">
        <svg viewBox="0 0 24 24"><path d="M11 4H4a2 2 0 00-2 2v14a2 2 0 002 2h14a2 2 0 002-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 013 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>Batafsil
      </a>
      <button class="btn-del" data-id="${row.id}">
        <svg viewBox="0 0 24 24"><polyline points="3 6 5 6 21 6"/><path d="M19 6l-1 14H6L5 6"/><path d="M10 11v6M14 11v6"/><path d="M9 6V4h6v2"/></svg>O'chir
      </button>
    </td></tr>`;
  }

  return `<tr>${cells}<td class="tbl-actions">
    <button class="btn-edit" data-id="${row.id}">
      <svg viewBox="0 0 24 24"><path d="M11 4H4a2 2 0 00-2 2v14a2 2 0 002 2h14a2 2 0 002-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 013 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>Tahrir
    </button>
    <button class="btn-del" data-id="${row.id}">
      <svg viewBox="0 0 24 24"><polyline points="3 6 5 6 21 6"/><path d="M19 6l-1 14H6L5 6"/><path d="M10 11v6M14 11v6"/><path d="M9 6V4h6v2"/></svg>O'chir
    </button>
  </td></tr>`;
}

function buildPagination(page, pages) {
  if (pages <= 1) return '';
  let btns = '';
  for (let i = 1; i <= pages; i++) {
    btns += `<button class="pg-btn ${i === page ? 'active' : ''}" data-p="${i}">${i}</button>`;
  }
  return `<div class="pagination">${btns}</div>`;
}

/* ═══ Detail page (News / Events) — CMS editor ══════════════════════════ */
async function renderDetailPage(el, page, cfg, id) {
  el.innerHTML = '<div class="loader"><div class="spinner"></div></div>';
  const isNew   = id === 'new';
  const isNews  = page === 'news';
  const isPage  = page === 'pages';

  const remote = {};
  for (const f of cfg.fields || []) {
    if (f.loadFrom) { const r = await api(f.loadFrom); remote[f.n] = r.data || []; }
  }

  let item = null, images = [];
  if (!isNew) {
    const reqs = [api(`${cfg.endpoint}${id}/`)];
    if (cfg.hasImages) reqs.push(api(`/panel/api/${page}/${id}/images/`));
    const [itemR, imgR] = await Promise.all(reqs);
    if (!itemR.success) { el.innerHTML = '<p style="padding:24px;color:var(--text2)">Topilmadi</p>'; return; }
    item   = itemR.data;
    images = (imgR && imgR.success) ? imgR.data : [];
  }

  const bodyRaw  = item?.body || item?.description || '';
  const bodyHtml = bodyRaw.includes('<') ? bodyRaw : bodyRaw.replace(/&/g,'&amp;').replace(/\n/g,'<br>');
  const isActive = item?.is_active ?? true;
  const catOpts  = (remote.category_id || []).map(c =>
    `<option value="${c.id}" ${String(item?.category_id) === String(c.id) ? 'selected' : ''}>${esc(c.name)}</option>`
  ).join('');

  el.innerHTML = `
    <div class="cms-crumb">
      <button class="cms-back" id="cms-back">← ${cfg.title}</button>
      <span class="cms-sep">›</span>
      <span class="cms-cur">${isNew ? "Yangi qo'shish" : esc(item?.title || 'Tahrirlash')}</span>
      ${!isNew ? `<button class="btn-danger cms-del-btn" id="det-del">O'chirish</button>` : ''}
    </div>

    <form id="detail-form">
      <input type="hidden" name="body" id="body-hidden">
      <div class="editor-layout">

        <!-- ── LEFT: content ── -->
        <div class="editor-main">
          <div class="editor-title-wrap">
            <input type="text" name="title" class="editor-title"
                   placeholder="Sarlavhani kiriting..." value="${esc(item?.title || '')}" required>
          </div>

          <div class="editor-area">
            <div class="editor-toolbar" id="et">
              <button type="button" data-cmd="bold"          class="tb-btn"><b>B</b></button>
              <button type="button" data-cmd="italic"        class="tb-btn"><em>I</em></button>
              <button type="button" data-cmd="underline"     class="tb-btn"><u>U</u></button>
              <span class="tb-sep"></span>
              <button type="button" data-cmd="insertUnorderedList" class="tb-btn" title="Ro'yxat">
                <svg viewBox="0 0 20 16" width="16" height="13" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round">
                  <line x1="7" y1="2"  x2="19" y2="2"/><line x1="7" y1="8"  x2="19" y2="8"/><line x1="7" y1="14" x2="19" y2="14"/>
                  <circle cx="2.5" cy="2"  r="1.5" fill="currentColor" stroke="none"/>
                  <circle cx="2.5" cy="8"  r="1.5" fill="currentColor" stroke="none"/>
                  <circle cx="2.5" cy="14" r="1.5" fill="currentColor" stroke="none"/>
                </svg>
              </button>
              <button type="button" data-cmd="insertOrderedList" class="tb-btn" title="Raqamli ro'yxat">
                <svg viewBox="0 0 20 16" width="16" height="13" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round">
                  <line x1="7" y1="2"  x2="19" y2="2"/><line x1="7" y1="8"  x2="19" y2="8"/><line x1="7" y1="14" x2="19" y2="14"/>
                  <text x="0" y="4"  font-size="5.5" fill="currentColor" stroke="none">1.</text>
                  <text x="0" y="10" font-size="5.5" fill="currentColor" stroke="none">2.</text>
                  <text x="0" y="16" font-size="5.5" fill="currentColor" stroke="none">3.</text>
                </svg>
              </button>
              <span class="tb-sep"></span>
              <button type="button" data-cmd="removeFormat" class="tb-btn" title="Formatlashni tozalash">✕</button>
            </div>
            <div class="editor-body" id="body-editor" contenteditable="true"
                 data-ph="${isNews ? 'Yangilik matnini yozing...' : isPage ? 'Sahifa mazmunini yozing...' : 'Tadbir tavsifini yozing...'}">${bodyHtml}</div>
          </div>

          ${isNews ? `
          <div class="editor-short-wrap">
            <label class="editor-short-lbl">Qisqa matn</label>
            <textarea name="short_text" class="editor-short" rows="3"
                      placeholder="Qisqa tavsif (asosiy sahifa uchun)...">${esc(item?.short_text || '')}</textarea>
          </div>` : ''}
        </div>

        <!-- ── RIGHT: sidebar ── -->
        <div class="editor-sidebar">

          <!-- Publish card -->
          <div class="ed-card pub-card">
            <div class="pub-head">
              <span class="pub-status-badge ${isActive ? 'pub-on' : 'pub-off'}" id="pub-badge">
                ${isActive ? '● Faol' : '○ Nofaol'}
              </span>
            </div>
            <div class="pub-toggle-row">
              <span>Holat</span>
              <label class="toggle">
                <input type="checkbox" name="is_active" id="pub-active" ${isActive ? 'checked' : ''}>
                <span class="toggle-slider"></span>
              </label>
            </div>
            ${isNews ? `
            <div class="pub-toggle-row">
              <span>Asosiy yangilik</span>
              <label class="toggle">
                <input type="checkbox" name="is_featured" ${item?.is_featured ? 'checked' : ''}>
                <span class="toggle-slider"></span>
              </label>
            </div>` : ''}
            <div class="pub-actions">
              <button type="submit" class="btn-primary pub-save-btn">
                ${isNew ? "Saqlash →" : '💾 Saqlash'}
              </button>
            </div>
          </div>

          <!-- Organization / Details card -->
          <div class="ed-card">
            <h4 class="ed-card-title">${isNews ? 'Tashkilot' : isPage ? 'Manzil' : 'Tafsilotlar'}</h4>
            ${isNews ? `
            <div class="field">
              <label>Kategoriya</label>
              <select name="category_id">
                <option value="">— Tanlang —</option>${catOpts}
              </select>
            </div>
            <div class="field" style="margin-top:10px">
              <label>Muallif</label>
              <input type="text" name="author" value="${esc(item?.author || '')}">
            </div>` : isPage ? `
            <div class="field">
              <label>URL Slug</label>
              <input type="text" name="slug" value="${esc(item?.slug || '')}" placeholder="masalan: ilmiy-faoliyat">
            </div>` : `
            <div class="field">
              <label>Joy</label>
              <input type="text" name="location" value="${esc(item?.location || '')}">
            </div>
            <div class="field" style="margin-top:10px">
              <label>Sana va vaqt <span style="color:var(--red)">*</span></label>
              <input type="datetime-local" name="event_date" value="${esc(item?.event_date || '')}" required>
            </div>`}
          </div>

          ${!isPage ? `<!-- Featured image card -->
          <div class="ed-card">
            <h4 class="ed-card-title">Muqova rasmi</h4>
            <div class="featured-area" id="feat-area">
              ${item?.image
                ? `<img src="${item.image}" class="featured-img" id="feat-preview">`
                : `<div class="featured-drop" id="feat-preview">
                     <svg viewBox="0 0 24 24" width="32" height="32" fill="none" stroke="currentColor" stroke-width="1.4"><rect x="3" y="3" width="18" height="18" rx="3"/><circle cx="8.5" cy="8.5" r="1.5"/><path d="M21 15l-5-5L5 21"/></svg>
                     <span>Yuklash uchun bosing</span>
                     <small>PNG, JPG — 5 MB gacha</small>
                   </div>`}
            </div>
            <input type="file" name="image" id="feat-file" accept="image/*" style="display:none">
            ${item?.image ? `<button type="button" class="feat-change-btn" id="feat-change">Rasmni o'zgartirish</button>` : ''}
          </div>` : ''}

        </div>
      </div>
    </form>

    <!-- Gallery section (edit mode) -->
    ${(!isNew && cfg.hasImages) ? `
    <div class="gallery-section">
      <div class="gallery-section-head">
        <h3>Galereya rasmlari <span class="gallery-count">${images.length} ta rasm</span></h3>
      </div>
      <div class="gallery-grid" id="gallery-grid">
        ${images.length
          ? images.map(img => galleryItem(img, page)).join('')
          : '<div class="gallery-empty">Hali rasm qo\'shilmagan</div>'}
      </div>
      <div class="gallery-add">
        <div class="gallery-add-preview" id="gal-preview">+</div>
        <div class="gallery-add-fields">
          <input type="file" id="gal-file" accept="image/*">
          <input type="text" id="gal-caption" placeholder="Rasm izohi (ixtiyoriy)">
        </div>
        <button type="button" class="btn-primary" id="gal-add-btn">Rasm qo'shish</button>
      </div>
    </div>` : ''}
    <div style="height:48px"></div>`;

  /* ── Events ── */
  document.getElementById('cms-back').addEventListener('click', () => { location.hash = `#${page}`; });

  if (!isNew) {
    document.getElementById('det-del').addEventListener('click', async () => {
      const ok = await confirmAction("Bu yozuv va barcha rasmlari o'chiriladi. Davom etasizmi?");
      if (!ok) return;
      const dr = await api(`${cfg.endpoint}${id}/`, { method: 'DELETE' });
      if (dr.success) { toast("O'chirildi"); location.hash = `#${page}`; }
      else toast(dr.error || 'Xato', 'error');
    });
  }

  // Toolbar
  document.getElementById('et').addEventListener('mousedown', e => {
    const btn = e.target.closest('[data-cmd]');
    if (!btn) return;
    e.preventDefault();
    document.execCommand(btn.dataset.cmd, false, null);
    document.getElementById('body-editor').focus();
  });

  // Toggle label
  document.getElementById('pub-active').addEventListener('change', function () {
    const badge = document.getElementById('pub-badge');
    badge.textContent = this.checked ? '● Faol' : '○ Nofaol';
    badge.className = `pub-status-badge ${this.checked ? 'pub-on' : 'pub-off'}`;
  });

  // Featured image
  if (!isPage) {
  const featArea = document.getElementById('feat-area');
  const featFile = document.getElementById('feat-file');
  featArea.addEventListener('click', () => featFile.click());
  document.getElementById('feat-change')?.addEventListener('click', e => { e.stopPropagation(); featFile.click(); });
  featFile.addEventListener('change', function () {
    const file = this.files[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = ev => {
      let prev = document.getElementById('feat-preview');
      if (prev.tagName === 'IMG') { prev.src = ev.target.result; }
      else {
        const img = Object.assign(document.createElement('img'), { src: ev.target.result, className: 'featured-img', id: 'feat-preview' });
        prev.replaceWith(img);
        if (!document.getElementById('feat-change')) {
          featArea.insertAdjacentHTML('afterend', `<button type="button" class="feat-change-btn" id="feat-change">Rasmni o'zgartirish</button>`);
          document.getElementById('feat-change').addEventListener('click', e => { e.stopPropagation(); featFile.click(); });
        }
      }
    };
    reader.readAsDataURL(file);
  });
  } // end if (!isPage)

  // Form submit
  document.getElementById('detail-form').addEventListener('submit', async e => {
    e.preventDefault();
    document.getElementById('body-hidden').value = document.getElementById('body-editor').innerHTML;
    const btn = e.target.querySelector('[type=submit]');
    if (btn) btn.disabled = true;
    const fd = new FormData(e.target);
    ['is_active', 'is_featured'].forEach(name => {
      const inp = e.target.querySelector(`[name="${name}"]`);
      if (inp) fd.set(name, inp.checked ? 'true' : 'false');
    });
    const url = isNew ? cfg.endpoint : `${cfg.endpoint}${id}/`;
    const result = await api(url, { method: 'POST', body: fd });
    if (btn) btn.disabled = false;
    if (result.success) {
      if (isNew) { toast("Qo'shildi! Endi rasm qo'shishingiz mumkin."); location.hash = `#${page}/${result.data.id}`; }
      else toast('Saqlandi');
    } else {
      toast(result.error || 'Xato', 'error');
    }
  });

  // Gallery
  if (!isNew && cfg.hasImages) {
    document.getElementById('gal-file').addEventListener('change', function () {
      const file = this.files[0];
      if (!file) return;
      const reader = new FileReader();
      reader.onload = ev => { document.getElementById('gal-preview').innerHTML = `<img src="${ev.target.result}" style="width:100%;height:100%;object-fit:cover;border-radius:8px">`; };
      reader.readAsDataURL(file);
    });

    document.getElementById('gal-add-btn').addEventListener('click', async () => {
      const file = document.getElementById('gal-file').files[0];
      if (!file) { toast('Rasm tanlang', 'error'); return; }
      const caption = document.getElementById('gal-caption').value.trim();
      const fd = new FormData();
      fd.append('image', file);
      if (caption) fd.append('caption', caption);
      const addBtn = document.getElementById('gal-add-btn');
      addBtn.disabled = true;
      const r = await api(`/panel/api/${page}/${id}/images/`, { method: 'POST', body: fd });
      addBtn.disabled = false;
      if (r.success) {
        toast("Rasm qo'shildi");
        const grid = document.getElementById('gallery-grid');
        grid.querySelector('.gallery-empty')?.remove();
        const div = document.createElement('div');
        div.innerHTML = galleryItem(r.data, page);
        const newItem = div.firstElementChild;
        grid.appendChild(newItem);
        newItem.querySelector('.gal-del').addEventListener('click', makeDelHandler(el, page, id));
        const countEl = el.querySelector('.gallery-count');
        if (countEl) countEl.textContent = `${grid.querySelectorAll('.gallery-item').length} ta rasm`;
        document.getElementById('gal-file').value = '';
        document.getElementById('gal-caption').value = '';
        document.getElementById('gal-preview').innerHTML = '+';
      } else {
        toast(r.error || 'Xato', 'error');
      }
    });

    el.querySelectorAll('.gal-del').forEach(btn => {
      btn.addEventListener('click', makeDelHandler(el, page, id));
    });
  }
}

function galleryItem(img, page) {
  return `<div class="gallery-item" id="gimg-${img.id}">
    <img src="${img.image}" class="gallery-thumb" loading="lazy">
    <div class="gallery-item-foot">
      <span class="gallery-caption">${esc(img.caption || '')}</span>
      <button class="gal-del btn-icon" data-id="${img.id}" title="O'chirish">
        <svg viewBox="0 0 24 24"><polyline points="3 6 5 6 21 6"/><path d="M19 6l-1 14H6L5 6"/><path d="M10 11v6M14 11v6"/><path d="M9 6V4h6v2"/></svg>
      </button>
    </div>
  </div>`;
}

function makeDelHandler(el, page, itemId) {
  return async function () {
    const imgId = this.dataset.id;
    const ok = await confirmAction("Rasmni o'chirasizmi?");
    if (!ok) return;
    const dr = await api(`/panel/api/${page}/images/${imgId}/`, { method: 'DELETE' });
    if (dr.success) {
      document.getElementById(`gimg-${imgId}`)?.remove();
      toast("O'chirildi");
      const grid = document.getElementById('gallery-grid');
      const countEl = el.querySelector('.gallery-count');
      if (countEl) {
        const n = grid.querySelectorAll('.gallery-item').length;
        countEl.textContent = `${n} ta rasm`;
        if (n === 0) grid.innerHTML = '<div class="gallery-empty">Hali rasm qo\'shilmagan</div>';
      }
    } else {
      toast(dr.error || 'Xato', 'error');
    }
  };
}

/* ═══ Form modal (for non-detail pages) ════════════════════════════════ */
async function openForm(page, cfg, item) {
  const remote = {};
  for (const f of cfg.fields || []) {
    if (f.loadFrom) {
      const r = await api(f.loadFrom);
      remote[f.n] = r.data || [];
    }
  }

  const isEdit = !!item;
  const modal = document.createElement('div');
  modal.className = 'modal-overlay';
  modal.innerHTML = `
    <div class="modal-box modal-form">
      <div class="modal-hd">
        <span>${isEdit ? 'Tahrirlash' : "Qo'shish"}: ${cfg.title}</span>
        <button class="modal-x" id="fm-x">✕</button>
      </div>
      <form id="item-form" autocomplete="off">
        <div class="form-fields">
          ${cfg.fields.map(f => buildField(f, item, remote)).join('')}
        </div>
        <div class="fm-actions">
          <button type="button" class="btn-secondary" id="fm-cancel">Bekor qilish</button>
          <button type="submit" class="btn-primary">${isEdit ? 'Saqlash' : "Qo'shish"}</button>
        </div>
      </form>
    </div>`;

  document.body.appendChild(modal);
  const close = () => modal.remove();
  document.getElementById('fm-x').addEventListener('click', close);
  document.getElementById('fm-cancel').addEventListener('click', close);
  modal.addEventListener('click', e => { if (e.target === modal) close(); });
  modal.querySelectorAll('input[type=file]').forEach(inp => {
    inp.addEventListener('change', () => previewImg(inp, inp.dataset.prev));
  });

  document.getElementById('item-form').addEventListener('submit', async e => {
    e.preventDefault();
    const btn = e.target.querySelector('[type=submit]');
    btn.disabled = true;
    const url = isEdit ? `${cfg.endpoint}${item.id}/` : cfg.endpoint;
    let result;
    if (cfg.useJSON) {
      const data = {};
      new FormData(e.target).forEach((v, k) => { data[k] = v; });
      cfg.fields.forEach(f => {
        if (f.t === 'toggle') data[f.n] = !!e.target.querySelector(`[name="${f.n}"]`)?.checked;
        if (f.t === 'number') data[f.n] = Number(data[f.n] ?? 0);
      });
      result = await api(url, { method: 'POST', json: data });
    } else {
      const fd = new FormData(e.target);
      cfg.fields.forEach(f => {
        if (f.t === 'toggle') fd.set(f.n, e.target.querySelector(`[name="${f.n}"]`)?.checked ? 'true' : 'false');
      });
      result = await api(url, { method: 'POST', body: fd });
    }
    if (result.success) {
      toast(isEdit ? 'Yangilandi' : "Qo'shildi");
      close();
      renderList(document.getElementById('content'), page, cfg, _curPageNum);
    } else {
      toast(result.error || 'Xato', 'error');
      btn.disabled = false;
    }
  });
}

function buildField(f, item, remote) {
  const val = item ? (item[f.n] ?? '') : (f.def ?? '');

  if (f.t === 'toggle') {
    const checked = item ? !!item[f.n] : (f.def !== false);
    return `<div class="field">
      <label style="display:flex;align-items:center;gap:10px;cursor:pointer">
        <label class="toggle" style="flex-shrink:0">
          <input type="checkbox" name="${f.n}" ${checked ? 'checked' : ''}>
          <span class="toggle-slider"></span>
        </label>
        ${esc(f.l)}
      </label>
    </div>`;
  }

  if (f.t === 'image') {
    const src = item ? item[f.n] : null;
    const pid = `prev-${f.n}`;
    return `<div class="field">
      <label>${esc(f.l)}</label>
      ${src ? `<img src="${src}" class="img-thumb-preview" id="${pid}" style="margin-bottom:6px">` : `<div id="${pid}" class="img-empty-preview">Rasm yo'q</div>`}
      <input type="file" name="${f.n}" accept="image/*" data-prev="${pid}">
    </div>`;
  }

  if (f.t === 'file') {
    const existing = item ? item[f.n] : null;
    return `<div class="field field-full">
      <label>${esc(f.l)}${f.req ? ' <span style="color:var(--red)">*</span>' : ''}</label>
      ${existing ? `<div style="margin-bottom:6px;font-size:.82rem;color:var(--accent)">📎 <a href="${existing}" target="_blank" style="color:var(--accent)">Mavjud fayl</a></div>` : ''}
      <input type="file" name="${f.n}" ${f.req && !existing ? 'required' : ''}>
    </div>`;
  }

  if (f.t === 'textarea') {
    return `<div class="field field-full">
      <label>${esc(f.l)}${f.req ? ' <span style="color:var(--red)">*</span>' : ''}</label>
      <textarea name="${f.n}" rows="${f.rows || 4}" ${f.req ? 'required' : ''}>${esc(String(val))}</textarea>
    </div>`;
  }

  if (f.t === 'select') {
    let opts;
    if (f.loadFrom) {
      opts = '<option value="">— Tanlang —</option>' +
        (remote[f.n] || []).map(o =>
          `<option value="${o.id}" ${String(val) === String(o.id) ? 'selected' : ''}>${esc(o.name)}</option>`
        ).join('');
    } else {
      opts = (f.opts || []).map(o =>
        `<option value="${o.v}" ${val === o.v ? 'selected' : ''}>${esc(o.lbl)}</option>`
      ).join('');
    }
    return `<div class="field">
      <label>${esc(f.l)}</label>
      <select name="${f.n}">${opts}</select>
    </div>`;
  }

  return `<div class="field">
    <label>${esc(f.l)}${f.req ? ' <span style="color:var(--red)">*</span>' : ''}</label>
    <input type="${f.t || 'text'}" name="${f.n}" value="${esc(String(val))}" ${f.req ? 'required' : ''}>
  </div>`;
}

/* ═══ Messages ═════════════════════════════════════════════════════════ */
async function renderMessages(el, filter, pageNum) {
  filter  = filter  ?? _curFilter;
  pageNum = pageNum ?? 1;
  el.innerHTML = '<div class="loader"><div class="spinner"></div></div>';
  const qs = new URLSearchParams({ page: pageNum });
  if (filter) qs.set('status', filter);
  const r = await api(`/panel/api/messages/?${qs}`);
  if (!r.success) { el.innerHTML = '<p style="padding:24px;color:var(--text2)">Xato</p>'; return; }
  _curFilter = filter;

  const tabs = [
    { v: '', l: 'Barchasi' },
    { v: 'new', l: 'Yangi' },
    { v: 'read', l: "O'qilgan" },
    { v: 'answered', l: 'Javob berilgan' },
  ];

  el.innerHTML = `
    <div class="page-head"><h1>Xabarlar</h1></div>
    <div class="filter-tabs">
      ${tabs.map(t => `<button class="filter-tab${filter === t.v ? ' active' : ''}" data-v="${t.v}">${t.l}</button>`).join('')}
    </div>
    <div class="table-wrap">
      <table>
        <thead><tr><th>Ism</th><th>Telefon</th><th>Yo'nalish</th><th>Holat</th><th>Sana</th></tr></thead>
        <tbody>
          ${r.data.length
            ? r.data.map(m => {
                const lbl = { new: 'Yangi', read: "O'qilgan", answered: 'Javob berilgan' };
                return `<tr class="row-clickable" data-id="${m.id}">
                  <td>${esc(m.name)}</td><td>${esc(m.phone || '')}</td>
                  <td>${esc(m.direction || '')}</td>
                  <td><span class="status-badge status-${m.status}">${lbl[m.status] || m.status}</span></td>
                  <td>${esc(m.created_at || '')}</td>
                </tr>`;
              }).join('')
            : `<tr><td colspan="5"><div class="empty-state">Xabar topilmadi</div></td></tr>`}
        </tbody>
      </table>
    </div>
    ${buildPagination(pageNum, r.pages || 1)}`;

  el.querySelectorAll('.filter-tab').forEach(btn => {
    btn.addEventListener('click', () => renderMessages(el, btn.dataset.v, 1));
  });
  el.querySelectorAll('.row-clickable').forEach(tr => {
    tr.addEventListener('click', () => openMsgDetail(el, tr.dataset.id));
  });
  el.querySelectorAll('.pg-btn').forEach(btn => {
    btn.addEventListener('click', () => renderMessages(el, _curFilter, +btn.dataset.p));
  });
}

async function openMsgDetail(contentEl, id) {
  const r = await api(`/panel/api/messages/${id}/`);
  if (!r.success) { toast('Xato', 'error'); return; }
  const m = r.data;
  if (m.status === 'new') {
    await api(`/panel/api/messages/${id}/`, { method: 'POST', json: { status: 'read' } });
    updateMsgBadge();
  }
  const modal = document.createElement('div');
  modal.className = 'modal-overlay';
  modal.innerHTML = `
    <div class="modal-box modal-form" style="max-width:520px">
      <div class="modal-hd">
        <span>Xabar #${m.id}</span>
        <button class="modal-x" id="md-x">✕</button>
      </div>
      <div style="padding:20px 22px">
        <div class="msg-meta">
          <span><b>Ism:</b> ${esc(m.first_name)} ${esc(m.last_name)}</span>
          <span><b>Telefon:</b> ${esc(m.phone || '—')}</span>
          <span><b>Email:</b> ${esc(m.email || '—')}</span>
          <span><b>Yo'nalish:</b> ${esc(m.direction || '—')}</span>
          <span><b>Sana:</b> ${esc(m.created_at || '—')}</span>
        </div>
        <div class="msg-body">${esc(m.message || '')}</div>
      </div>
      <div class="fm-actions">
        <select id="md-status">
          <option value="new" ${m.status==='new'?'selected':''}>Yangi</option>
          <option value="read" ${m.status==='read'?'selected':''}>O'qilgan</option>
          <option value="answered" ${m.status==='answered'?'selected':''}>Javob berilgan</option>
        </select>
        <button class="btn-primary" id="md-save">Saqlash</button>
        <button class="btn-secondary" id="md-close">Yopish</button>
      </div>
    </div>`;
  document.body.appendChild(modal);
  const close = () => { modal.remove(); renderMessages(contentEl, _curFilter); };
  document.getElementById('md-x').addEventListener('click', close);
  document.getElementById('md-close').addEventListener('click', close);
  modal.addEventListener('click', e => { if (e.target === modal) close(); });
  document.getElementById('md-save').addEventListener('click', async () => {
    const status = document.getElementById('md-status').value;
    const r = await api(`/panel/api/messages/${id}/`, { method: 'POST', json: { status } });
    if (r.success) { toast('Saqlandi'); close(); }
    else toast(r.error || 'Xato', 'error');
  });
}

/* ═══ Badge ════════════════════════════════════════════════════════════ */
async function updateMsgBadge() {
  const r = await api('/panel/api/stats/');
  const badge = document.getElementById('msg-badge');
  if (!badge) return;
  const n = r.data?.new_msgs || 0;
  badge.textContent = n;
  badge.style.display = n > 0 ? '' : 'none';
}

/* ═══ Auth ═════════════════════════════════════════════════════════════ */
function showLogin() {
  document.getElementById('login-screen').classList.remove('hidden');
  document.getElementById('app').classList.add('hidden');
}
function showApp(username) {
  document.getElementById('login-screen').classList.add('hidden');
  document.getElementById('app').classList.remove('hidden');
  document.getElementById('topbar-username').textContent = username;
  updateMsgBadge();
}

async function doLogin() {
  const username = document.getElementById('login-username').value.trim();
  const password = document.getElementById('login-password').value;
  const errEl = document.getElementById('login-error');
  errEl.classList.add('hidden');
  if (!username || !password) {
    errEl.textContent = 'Login va parolni kiriting';
    errEl.classList.remove('hidden');
    return;
  }
  const r = await api('/panel/api/login/', { method: 'POST', json: { username, password } });
  if (r.success) { showApp(r.username); routeTo(location.hash || '#dashboard'); }
  else { errEl.textContent = r.error || 'Xato'; errEl.classList.remove('hidden'); }
}

document.getElementById('login-btn').addEventListener('click', doLogin);
document.getElementById('login-password').addEventListener('keydown', e => { if (e.key === 'Enter') doLogin(); });
document.getElementById('logout-btn').addEventListener('click', async () => {
  await api('/panel/api/logout/', { method: 'POST' });
  showLogin();
});

/* ═══ Sidebar toggle ═══════════════════════════════════════════════════ */
document.getElementById('menu-btn').addEventListener('click', () => {
  document.getElementById('sidebar').classList.toggle('open');
});

/* ═══ Init ═════════════════════════════════════════════════════════════ */
(async () => {
  const r = await api('/panel/api/me/');
  if (r.auth) { showApp(r.username); routeTo(location.hash || '#dashboard'); }
  else showLogin();
})();
