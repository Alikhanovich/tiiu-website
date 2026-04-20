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
    this.classList.add('sub-active');
  });
});
document.querySelectorAll('.split-col a:not(.has-sub)').forEach(link => {
  link.addEventListener('mouseenter', function () {
    const dropdown = this.closest('.dropdown');
    if (!dropdown) return;
    dropdown.querySelectorAll('.split-panel').forEach(p => p.classList.remove('visible'));
    dropdown.querySelectorAll('.has-sub').forEach(l => l.classList.remove('sub-active'));
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
  scene.fog = new THREE.FogExp2(0x030710, 0.028);

  const camera = new THREE.PerspectiveCamera(50, 1, 0.1, 300);
  camera.position.set(0, 4, 16);

  function onResize() {
    const W = canvas.offsetWidth, H = canvas.offsetHeight;
    renderer.setSize(W, H, false);
    camera.aspect = W / H; camera.updateProjectionMatrix();
  }
  onResize();
  window.addEventListener('resize', onResize);

  scene.add(new THREE.AmbientLight(0x1a2a5a, 2.2));
  const dir = new THREE.DirectionalLight(0xffffff, .8);
  dir.position.set(8, 16, 8); scene.add(dir);
  const bL = new THREE.PointLight(0x006933, 5, 24);
  const pL = new THREE.PointLight(0x0b3d2b, 3.5, 20);
  const cL = new THREE.PointLight(0x125875, 2.5, 18);
  cL.position.set(0, 9, 0);
  scene.add(bL, pL, cL);

  const grid = new THREE.GridHelper(40, 40, 0x1a3a8a, 0x0d1f4a);
  grid.position.y = -4.5; scene.add(grid);

  function edges(mesh, col, op) {
    mesh.add(new THREE.LineSegments(
      new THREE.EdgesGeometry(mesh.geometry),
      new THREE.LineBasicMaterial({ color: col, transparent: true, opacity: op || .85 })
    ));
  }

  const G = new THREE.Group();
  const bM = new THREE.MeshPhongMaterial({ color:0x0d1a0d,emissive:0x0a2a12,emissiveIntensity:.5,shininess:70,transparent:true,opacity:.96 });
  const gM = new THREE.MeshPhongMaterial({ color:0x0a3d1a,emissive:0x006933,emissiveIntensity:.3,shininess:200,transparent:true,opacity:.55 });

  const tower = new THREE.Mesh(new THREE.BoxGeometry(3.2, 9, 2.4), bM);
  edges(tower, 0x006933); G.add(tower);

  [[-3,-2.4,0],[3,-2.4,0]].forEach(p => {
    const w = new THREE.Mesh(new THREE.BoxGeometry(2.8,4.2,2.4), bM.clone());
    w.position.set(...p); edges(w, 0x125875, .65); G.add(w);
  });

  const roof = new THREE.Mesh(new THREE.BoxGeometry(3.2,.4,2.4), gM);
  roof.position.y = 4.7; edges(roof, 0x00a550); G.add(roof);

  const ant = new THREE.Mesh(new THREE.CylinderGeometry(.04,.04,3.8,8), new THREE.MeshBasicMaterial({color:0x125875}));
  ant.position.y = 6.3; G.add(ant);
  const tip = new THREE.Mesh(new THREE.SphereGeometry(.2,16,16), new THREE.MeshBasicMaterial({color:0x125875}));
  tip.position.y = 8.2; G.add(tip);

  const wMat = new THREE.MeshBasicMaterial({color:0x00a550,transparent:true});
  for(let r=0;r<7;r++) for(let c=0;c<3;c++){
    const wm=wMat.clone(); wm.opacity=.3+Math.random()*.5;
    const wp=new THREE.Mesh(new THREE.PlaneGeometry(.3,.42),wm);
    wp.position.set((c-1)*.78,r*1.05-2.5,1.21); G.add(wp);
  }
  G.position.y = -4.5; scene.add(G);

  const r1=new THREE.Mesh(new THREE.TorusGeometry(7,.055,8,100),new THREE.MeshBasicMaterial({color:0x006933,transparent:true,opacity:.3}));
  r1.rotation.x=Math.PI/2; r1.position.y=2; scene.add(r1);
  const r2=new THREE.Mesh(new THREE.TorusGeometry(5,.04,8,80),new THREE.MeshBasicMaterial({color:0x0b3d2b,transparent:true,opacity:.25}));
  r2.rotation.set(Math.PI/3,0,Math.PI/6); r2.position.y=4.5; scene.add(r2);
  const r3=new THREE.Mesh(new THREE.TorusGeometry(9,.03,8,120),new THREE.MeshBasicMaterial({color:0x125875,transparent:true,opacity:.15}));
  r3.rotation.set(Math.PI/6,Math.PI/4,0); scene.add(r3);

  const OC=[0x006933,0x0b3d2b,0x125875,0x00a550,0x0b3d2b,0x00c96a];
  const orbs=OC.map((c,i)=>{
    const m=new THREE.Mesh(new THREE.OctahedronGeometry(.25+i*.04,0),new THREE.MeshPhongMaterial({color:c,emissive:c,emissiveIntensity:.55}));
    const a=(i/OC.length)*Math.PI*2;
    m.position.set(Math.cos(a)*6,1+i*.7,Math.sin(a)*6);
    m.userData={a,r:6,s:.22+i*.06,y:1+i*.7}; scene.add(m); return m;
  });

  const pp=new Float32Array(4000*3);
  for(let i=0;i<pp.length;i++) pp[i]=(Math.random()-.5)*60;
  const pg=new THREE.BufferGeometry();
  pg.setAttribute('position',new THREE.BufferAttribute(pp,3));
  scene.add(new THREE.Points(pg,new THREE.PointsMaterial({color:0x006933,size:.06,transparent:true,opacity:.45})));

  if(typeof gsap!=='undefined'){
    gsap.from(G.position,{y:-14,duration:2.6,ease:'elastic.out(1,.55)',delay:.9});
    gsap.from(G.rotation,{y:Math.PI*.65,duration:2.6,ease:'power3.out',delay:.9});
  }

  let mx=0,my=0;
  document.addEventListener('mousemove',e=>{mx=(e.clientX/innerWidth-.5)*2;my=(e.clientY/innerHeight-.5)*2;});

  const clock=new THREE.Clock();
  const pts=scene.children.find(c=>c instanceof THREE.Points);
  (function loop(){
    requestAnimationFrame(loop);
    const t=clock.getElapsedTime();
    G.rotation.y=Math.sin(t*.13)*.1+mx*.055;
    r1.rotation.z=t*.17; r2.rotation.y=t*.12; r3.rotation.x=t*.08;
    orbs.forEach(o=>{
      const d=o.userData; d.a+=d.s*.01;
      o.position.set(Math.cos(d.a)*d.r,d.y+Math.sin(t+d.a)*.55,Math.sin(d.a)*d.r);
      o.rotation.x+=.018; o.rotation.y+=.024;
    });
    if(pts){pts.rotation.y=t*.022;pts.rotation.x=t*.007;}
    bL.position.set(Math.cos(t*.42)*9,4,Math.sin(t*.42)*9);
    pL.position.set(Math.cos(t*.33+Math.PI)*8,3,Math.sin(t*.33+Math.PI)*8);
    camera.position.y=4+Math.sin(t*.27)*.3-my*.28;
    camera.position.x=mx*1.3;
    camera.lookAt(0,1,0);
    renderer.render(scene,camera);
  })();
})();
