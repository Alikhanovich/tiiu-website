/* ════════════════════════════════════════════════════════════════
   TIIU — Main JavaScript
   Three.js 3D Scene + GSAP Animations + UI Logic
   ════════════════════════════════════════════════════════════════ */

/* ── GSAP setup (agar CDN yuklanmagan bo'lsa ham ishlaydi) ─── */
if (typeof gsap !== 'undefined' && typeof ScrollTrigger !== 'undefined') {
  gsap.registerPlugin(ScrollTrigger);
}

/* ── PRELOADER — CSS fallback bilan (GSAP kerak emas) ───────── */
(function () {
  const pre = document.getElementById('preloader');
  if (!pre) return;

  function hidePre() {
    pre.style.transition = 'opacity 0.6s ease';
    pre.style.opacity = '0';
    setTimeout(() => { pre.style.display = 'none'; }, 650);
  }

  if (typeof gsap !== 'undefined') {
    gsap.to(pre, {
      opacity: 0, duration: .7, delay: .5, ease: 'power2.inOut',
      onComplete() { pre.style.display = 'none'; }
    });
  } else {
    // GSAP yo'q — oddiy JS bilan yashir
    setTimeout(hidePre, 600);
  }

  // Har qanday holatda 2 soniyadan keyin majburiy yashir
  setTimeout(() => {
    if (pre.style.display !== 'none') hidePre();
  }, 2000);
})();

/* ── REVEAL ANIMATION — sahifa ochilganda ham ishlaydi ──────── */
function setupReveal() {
  const selector = '.reveal, .reveal-l, .reveal-r, .reveal-s';
  const els = document.querySelectorAll(selector);

  els.forEach(el => {
    const rect = el.getBoundingClientRect();
    // Agar element hoziroq viewport ichida bo'lsa — darhol ko'rsat
    if (rect.top < window.innerHeight * 0.95) {
      setTimeout(() => el.classList.add('vis'), 80);
    } else {
      // Viewport'ga kirganida ko'rsat
      const obs = new IntersectionObserver(entries => {
        entries.forEach(e => {
          if (e.isIntersecting) {
            e.target.classList.add('vis');
            obs.unobserve(e.target);
          }
        });
      }, { threshold: 0.05, rootMargin: '0px 0px -30px 0px' });
      obs.observe(el);
    }
  });

  // 600ms dan keyin barcha narsani ko'rsat (tez fallback)
  setTimeout(() => {
    document.querySelectorAll(selector + ':not(.vis)').forEach(el => el.classList.add('vis'));
  }, 600);
}

// DOM tayyor bo'lganda darhol ishga tushir
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', setupReveal);
} else {
  setupReveal();
}

/* ── Hero animatsiyasi (faqat bosh sahifada) ─────────────────── */
window.addEventListener('load', () => {
  // Preloader yashirish (yana bir kafolat)
  const pre = document.getElementById('preloader');
  if (pre && pre.style.display !== 'none') {
    pre.style.opacity = '0';
    setTimeout(() => { pre.style.display = 'none'; }, 600);
  }

  if (typeof gsap === 'undefined') return;

  // Hero elementlari mavjudmi tekshir
  if (!document.querySelector('.hero-title')) return;

  const tl = gsap.timeline({ delay: .7 });
  tl.from('.hero-badge', { opacity: 0, y: 20, duration: .6 })
    .from('.hero-title',  { opacity: 0, y: 30, duration: .7 }, '-=.3')
    .from('.hero-sub',    { opacity: 0, y: 20, duration: .6 }, '-=.4')
    .from('.hero-btns',   { opacity: 0, y: 20, duration: .5 }, '-=.3')
    .from('.hero-stats',  { opacity: 0, y: 20, duration: .5 }, '-=.3')
    .from('.hfc',         { opacity: 0, scale: .85, duration: .6, stagger: .12 }, '-=.25');

  // Hero hisoblagichlar
  document.querySelectorAll('.hstat .num').forEach(el => {
    const target = +el.dataset.count || 0;
    const suf = el.dataset.suffix || '';
    if (!target) return;
    gsap.to({ v: 0 }, {
      v: target, duration: 2, delay: 1.5, ease: 'power2.out',
      onUpdate() { el.textContent = Math.round(this.targets()[0].v) + suf; }
    });
  });
});

/* ── Navbar scroll ───────────────────────────────────────────── */
window.addEventListener('scroll', () => {
  const nav = document.getElementById('navbar');
  if (nav) nav.classList.toggle('scrolled', scrollY > 60);
});

/* ── Mobile menu ─────────────────────────────────────────────── */
window.toggleMenu = function () {
  const m = document.getElementById('mob-menu');
  if (m) m.classList.toggle('open');
};

/* ── Nav sub-panel (Kafedralar hover) ────────────────────────── */
document.querySelectorAll('.has-sub[data-panel]').forEach(link => {
  link.addEventListener('mouseenter', function () {
    const dropdown = this.closest('.dropdown');
    if (!dropdown) return;
    dropdown.querySelectorAll('.split-panel').forEach(p => p.classList.remove('visible'));
    dropdown.querySelectorAll('.has-sub').forEach(l => l.classList.remove('sub-active'));
    const panel = document.getElementById(this.dataset.panel);
    if (panel) panel.classList.add('visible');
    dropdown.classList.add('panel-open');
    this.classList.add('sub-active');
  });
});
document.querySelectorAll('.split-col a:not(.has-sub)').forEach(link => {
  link.addEventListener('mouseenter', function () {
    const dropdown = this.closest('.dropdown');
    if (!dropdown) return;
    dropdown.querySelectorAll('.split-panel').forEach(p => p.classList.remove('visible'));
    dropdown.querySelectorAll('.has-sub').forEach(l => l.classList.remove('sub-active'));
    dropdown.classList.remove('panel-open');
  });
});
document.querySelectorAll('.drop-split').forEach(dropdown => {
  dropdown.addEventListener('mouseleave', function () {
    this.classList.remove('panel-open');
  });
});

/* ── Mega dropdown side panel hover logic ─────────────────────── */
document.querySelectorAll('.drop-mega').forEach(dropdown => {
  const headLink = dropdown.querySelector('.mega-head-link');
  const sideLinks = dropdown.querySelectorAll('.mega-side a:not(.mega-head-link)');
  if (headLink) {
    headLink.addEventListener('mouseenter', function () {
      dropdown.classList.add('panel-open');
      headLink.classList.add('sub-active');
    });
  }
  sideLinks.forEach(link => {
    link.addEventListener('mouseenter', function () {
      dropdown.classList.remove('panel-open');
      if (headLink) headLink.classList.remove('sub-active');
    });
  });
  dropdown.addEventListener('mouseleave', function () {
    this.classList.remove('panel-open');
    if (headLink) headLink.classList.remove('sub-active');
  });
});

/* ── Stats counter (scroll trigger) ─────────────────────────── */
if (typeof gsap !== 'undefined' && typeof ScrollTrigger !== 'undefined') {
  document.querySelectorAll('[data-target]').forEach(span => {
    const target = +span.getAttribute('data-target') || 0;
    const suf = span.getAttribute('data-suffix') || '';
    ScrollTrigger.create({
      trigger: span, start: 'top 90%', once: true,
      onEnter() {
        gsap.to({ v: 0 }, {
          v: target, duration: 1.8, ease: 'power2.out',
          onUpdate() { span.textContent = Math.round(this.targets()[0].v) + suf; }
        });
      }
    });
  });

  // Karta animatsiyalari
  gsap.utils.toArray('.why-card').forEach((c, i) => {
    gsap.from(c, {
      scrollTrigger: { trigger: c, start: 'top 90%' },
      opacity: 0, y: 35, duration: .6, delay: i * .06, ease: 'power2.out'
    });
  });

  // Stats bar parallax
  const sg = document.querySelector('#stats-bar .stats-grid');
  if (sg) {
    gsap.to(sg, {
      scrollTrigger: { trigger: '#stats-bar', start: 'top bottom', end: 'bottom top', scrub: 1 },
      y: -15
    });
  }
}

/* ── FAQ ─────────────────────────────────────────────────────── */
window.toggleFaq = function (btn) {
  const item = btn.closest('.faq-item');
  const wasOpen = item.classList.contains('open');
  document.querySelectorAll('.faq-item.open').forEach(i => i.classList.remove('open'));
  if (!wasOpen) item.classList.add('open');
};

/* ── Contact form ────────────────────────────────────────────── */
const contactForm = document.getElementById('contact-form');
if (contactForm) {
  contactForm.addEventListener('submit', async e => {
    e.preventDefault();
    const btn = contactForm.querySelector('.form-submit');
    const orig = btn.textContent;
    btn.disabled = true;
    btn.textContent = 'Yuborilmoqda...';
    const fd = new FormData(contactForm);
    try {
      const res = await fetch(contactForm.action, {
        method: 'POST', body: fd,
        headers: { 'X-CSRFToken': fd.get('csrfmiddlewaretoken') },
      });
      const data = await res.json();
      if (data.ok) {
        btn.textContent = '✅ Yuborildi!';
        btn.style.background = 'linear-gradient(135deg,#16a34a,#22c55e)';
        contactForm.reset();
        setTimeout(() => { btn.textContent = orig; btn.style.background = ''; btn.disabled = false; }, 3000);
      }
    } catch {
      btn.textContent = '❌ Xato. Qayta urinib ko\'ring.';
      btn.style.background = 'linear-gradient(135deg,#dc2626,#ef4444)';
      setTimeout(() => { btn.textContent = orig; btn.style.background = ''; btn.disabled = false; }, 2500);
    }
  });
}

/* ── Smooth scroll ───────────────────────────────────────────── */
document.querySelectorAll('a[href^="#"]').forEach(a => {
  a.addEventListener('click', e => {
    const id = a.getAttribute('href').slice(1);
    const el = document.getElementById(id);
    if (el) { e.preventDefault(); el.scrollIntoView({ behavior: 'smooth' }); }
  });
});

/* ── Card 3D tilt ────────────────────────────────────────────── */
document.querySelectorAll('.why-card, .news-card, .cf-wrap, .teacher-card').forEach(card => {
  card.addEventListener('mousemove', e => {
    const r = card.getBoundingClientRect();
    const x = (e.clientX - r.left) / r.width - .5;
    const y = (e.clientY - r.top)  / r.height - .5;
    card.style.transform = `perspective(700px) rotateY(${x * 7}deg) rotateX(${-y * 7}deg) translateY(-6px)`;
  });
  card.addEventListener('mouseleave', () => { card.style.transform = ''; });
});

/* ════════════════════════════════════════════════════════════════
   THREE.JS HERO SCENE
   ════════════════════════════════════════════════════════════════ */
(function initThree() {
  if (typeof THREE === 'undefined') return;
  const canvas = document.getElementById('hero-canvas');
  if (!canvas) return;

  const renderer = new THREE.WebGLRenderer({ canvas, alpha: true, antialias: true });
  renderer.setPixelRatio(Math.min(devicePixelRatio, 2));

  const scene = new THREE.Scene();
  scene.fog = new THREE.FogExp2(0x0b0f0b, 0.018);

  const camera = new THREE.PerspectiveCamera(55, 1, 0.1, 300);
  camera.position.set(0, 0, 26);

  function onResize() {
    const W = canvas.offsetWidth, H = canvas.offsetHeight;
    renderer.setSize(W, H, false);
    camera.aspect = W / H; camera.updateProjectionMatrix();
  }
  onResize();
  window.addEventListener('resize', onResize);

  // ══ Ijtimoiy tarmoq: ulangan tugunlar ══════════════════════════
  // "Ijtimoiy innovatsiya" — odamlar/bilim tugunlari bir-biriga ulanib
  // sekin suzadi; sichqoncha yaqinlashsa ular unga cho'ziladi.
  const GREEN_A = new THREE.Color(0x2fae6a);
  const GREEN_B = new THREE.Color(0x0f7a42);
  const GOLD    = new THREE.Color(0xe4b363);
  const BX = 40, BY = 24, BZ = 12;                  // tarqalish hajmi (yarim)
  const LINK = 6.4;                                 // ulanish masofasi
  const COUNT = innerWidth < 768 ? 60 : 120;
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;

  // yumshoq dumaloq nuqta sprite'i (glow effekti uchun)
  function dotTexture() {
    const s = 64, cv = document.createElement('canvas'); cv.width = cv.height = s;
    const g = cv.getContext('2d');
    const grd = g.createRadialGradient(s/2, s/2, 0, s/2, s/2, s/2);
    grd.addColorStop(0,   'rgba(255,255,255,1)');
    grd.addColorStop(0.4, 'rgba(255,255,255,0.75)');
    grd.addColorStop(1,   'rgba(255,255,255,0)');
    g.fillStyle = grd; g.beginPath(); g.arc(s/2, s/2, s/2, 0, Math.PI*2); g.fill();
    return new THREE.CanvasTexture(cv);
  }

  const nodes = [];
  const nPos = new Float32Array(COUNT * 3);
  const nCol = new Float32Array(COUNT * 3);
  for (let i = 0; i < COUNT; i++) {
    const gold = Math.random() < 0.14;              // oltin urg'u ~14%
    const c = gold ? GOLD : (Math.random() < 0.5 ? GREEN_A : GREEN_B);
    const p = new THREE.Vector3((Math.random()-.5)*BX*2, (Math.random()-.5)*BY*2, (Math.random()-.5)*BZ*2);
    const v = new THREE.Vector3((Math.random()-.5)*0.022, (Math.random()-.5)*0.02, (Math.random()-.5)*0.014);
    nodes.push({ p, v, gold });
    p.toArray(nPos, i*3); c.toArray(nCol, i*3);
  }

  const nodeGeo = new THREE.BufferGeometry();
  nodeGeo.setAttribute('position', new THREE.BufferAttribute(nPos, 3).setUsage(THREE.DynamicDrawUsage));
  nodeGeo.setAttribute('color',    new THREE.BufferAttribute(nCol, 3));
  const points = new THREE.Points(nodeGeo, new THREE.PointsMaterial({
    size: 1.15, map: dotTexture(), vertexColors: true, transparent: true,
    opacity: 0.95, depthWrite: false, blending: THREE.AdditiveBlending
  }));
  scene.add(points);

  // ulanish chiziqlari — har kadrda masofaga qarab qayta quriladi
  const MAX_LINKS = COUNT * 18;
  const lPos = new Float32Array(MAX_LINKS * 6);
  const lCol = new Float32Array(MAX_LINKS * 6);
  const linkGeo = new THREE.BufferGeometry();
  linkGeo.setAttribute('position', new THREE.BufferAttribute(lPos, 3).setUsage(THREE.DynamicDrawUsage));
  linkGeo.setAttribute('color',    new THREE.BufferAttribute(lCol, 3).setUsage(THREE.DynamicDrawUsage));
  const links = new THREE.LineSegments(linkGeo, new THREE.LineBasicMaterial({
    vertexColors: true, transparent: true, opacity: 0.62, depthWrite: false, blending: THREE.AdditiveBlending
  }));
  scene.add(links);

  const mAnchor = new THREE.Vector3(0, 0, 3);        // sichqoncha "tuguni"
  const MOUSE_R = 10;                                // ta'sir radiusi

  let mx=0,my=0;
  document.addEventListener('mousemove',e=>{mx=(e.clientX/innerWidth-.5)*2;my=(e.clientY/innerHeight-.5)*2;});
  let scrollT = 0;
  let scrollYNorm = 0;
  function updateScrollProgress() {
    const max = Math.max(1, document.documentElement.scrollHeight - window.innerHeight);
    scrollYNorm = Math.min(1, Math.max(0, window.scrollY / max));
  }
  updateScrollProgress();
  window.addEventListener('scroll', () => {
    updateScrollProgress();
  }, { passive: true });

  const clock = new THREE.Clock();

  // Tugunlar orasidagi (va sichqoncha bilan) ulanishlarni qayta chizadi.
  function buildLinks() {
    let n = 0;                                        // yozilgan vertex soni
    for (let i = 0; i < COUNT; i++) {
      const a = nodes[i].p;
      for (let j = i + 1; j < COUNT; j++) {
        const b = nodes[j].p;
        const dx = a.x-b.x, dy = a.y-b.y, dz = a.z-b.z;
        const d2 = dx*dx + dy*dy + dz*dz;
        if (d2 > LINK*LINK) continue;
        const s  = (1 - Math.sqrt(d2) / LINK) * 0.9;  // yaqinroq = yorqinroq
        const warm = nodes[i].gold || nodes[j].gold;  // oltin tugun tegsa iliqroq
        const r = (warm ? 0.52 : 0.10) * s;
        const g = (warm ? 0.40 : 0.42) * s;
        const bl= (warm ? 0.20 : 0.28) * s;
        lPos[n*3]=a.x; lPos[n*3+1]=a.y; lPos[n*3+2]=a.z;
        lCol[n*3]=r;   lCol[n*3+1]=g;   lCol[n*3+2]=bl;  n++;
        lPos[n*3]=b.x; lPos[n*3+1]=b.y; lPos[n*3+2]=b.z;
        lCol[n*3]=r;   lCol[n*3+1]=g;   lCol[n*3+2]=bl;  n++;
        if (n >= MAX_LINKS*2 - 2) { i = COUNT; break; }
      }
      // sichqoncha tuguniga ulanish (iliq oltin-yashil)
      const mdx=a.x-mAnchor.x, mdy=a.y-mAnchor.y, mdz=a.z-mAnchor.z;
      const md2 = mdx*mdx + mdy*mdy + mdz*mdz;
      if (md2 < MOUSE_R*MOUSE_R && n < MAX_LINKS*2 - 2) {
        const s = 1 - Math.sqrt(md2) / MOUSE_R;
        lPos[n*3]=a.x; lPos[n*3+1]=a.y; lPos[n*3+2]=a.z;
        lCol[n*3]=0.60*s; lCol[n*3+1]=0.48*s; lCol[n*3+2]=0.22*s;  n++;
        lPos[n*3]=mAnchor.x; lPos[n*3+1]=mAnchor.y; lPos[n*3+2]=mAnchor.z;
        lCol[n*3]=0.60*s; lCol[n*3+1]=0.48*s; lCol[n*3+2]=0.22*s;  n++;
      }
    }
    linkGeo.setDrawRange(0, n);
    linkGeo.attributes.position.needsUpdate = true;
    linkGeo.attributes.color.needsUpdate = true;
  }

  if (reduce) {                                       // harakat kamaytirilgan: bitta statik kadr
    buildLinks();
    camera.lookAt(0, 0, 0);
    renderer.render(scene, camera);
    return;
  }

  (function loop() {
    requestAnimationFrame(loop);
    scrollT += (scrollYNorm - scrollT) * 0.06;

    // sichqoncha tugunini kamera oldida joylashtiramiz
    mAnchor.set(camera.position.x + mx * 22, camera.position.y - my * 13, 3);

    for (let i = 0; i < COUNT; i++) {
      const p = nodes[i].p, v = nodes[i].v;
      const mdx = mAnchor.x-p.x, mdy = mAnchor.y-p.y, mdz = mAnchor.z-p.z;
      const md2 = mdx*mdx + mdy*mdy + mdz*mdz;
      if (md2 < MOUSE_R*MOUSE_R) {                    // sichqonchaga yumshoq intilish
        const f = 0.00016 * (1 - Math.sqrt(md2) / MOUSE_R);
        v.x += mdx*f; v.y += mdy*f; v.z += mdz*f;
      }
      p.x += v.x; p.y += v.y; p.z += v.z;
      if (p.x >  BX) { p.x =  BX; v.x*=-1; } else if (p.x < -BX) { p.x = -BX; v.x*=-1; }
      if (p.y >  BY) { p.y =  BY; v.y*=-1; } else if (p.y < -BY) { p.y = -BY; v.y*=-1; }
      if (p.z >  BZ) { p.z =  BZ; v.z*=-1; } else if (p.z < -BZ) { p.z = -BZ; v.z*=-1; }
      v.multiplyScalar(0.995);                        // damping
      p.toArray(nPos, i*3);
    }
    nodeGeo.attributes.position.needsUpdate = true;
    buildLinks();

    camera.position.x += (mx * 3.2 - camera.position.x) * 0.03;
    camera.position.y += ((-my * 2.4 + scrollT * 8) - camera.position.y) * 0.03;
    camera.lookAt(camera.position.x * 0.4, camera.position.y * 0.5, 0);
    renderer.render(scene, camera);
  })();
})();


