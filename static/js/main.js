// ── Navigation Toggle ────────────────────────────────────────────────────────
const navToggle = document.getElementById('navToggle');
const navLinks  = document.querySelector('.nav-links');

navToggle?.addEventListener('click', () => {
  navLinks.classList.toggle('open');
  const spans = navToggle.querySelectorAll('span');
  if (navLinks.classList.contains('open')) {
    spans[0].style.transform = 'translateY(7px) rotate(45deg)';
    spans[1].style.opacity   = '0';
    spans[2].style.transform = 'translateY(-7px) rotate(-45deg)';
  } else {
    spans.forEach(s => { s.style.transform = ''; s.style.opacity = ''; });
  }
});

// Close nav on outside click
document.addEventListener('click', e => {
  if (navLinks?.classList.contains('open') && !e.target.closest('.nav-inner')) {
    navLinks.classList.remove('open');
    navToggle.querySelectorAll('span').forEach(s => { s.style.transform = ''; s.style.opacity = ''; });
  }
});

// ── Skills Filter ────────────────────────────────────────────────────────────
const tabBtns   = document.querySelectorAll('.tab-btn');
const skillCards = document.querySelectorAll('.skill-card');

tabBtns.forEach(btn => {
  btn.addEventListener('click', () => {
    tabBtns.forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    const cat = btn.dataset.cat;
    skillCards.forEach(card => {
      if (cat === 'all' || card.dataset.cat === cat) {
        card.style.display = '';
        requestAnimationFrame(() => card.style.opacity = '1');
      } else {
        card.style.opacity = '0';
        setTimeout(() => card.style.display = 'none', 180);
      }
    });
  });
});

// ── Intersection Observer — Animate on Scroll ─────────────────────────────────
const observeEls = document.querySelectorAll(
  '.skill-card, .project-card, .proj-item, .value-card, .admin-stat-card'
);

if ('IntersectionObserver' in window) {
  const io = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.style.animationPlayState = 'running';
        entry.target.classList.add('visible');
        io.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1 });

  observeEls.forEach((el, i) => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(16px)';
    el.style.transition = `opacity .4s ease ${i * 40}ms, transform .4s ease ${i * 40}ms`;
    io.observe(el);
  });

  // Reuse mutation trick to trigger
  setTimeout(() => {
    observeEls.forEach(el => {
      const rect = el.getBoundingClientRect();
      if (rect.top < window.innerHeight) {
        el.style.opacity = '1';
        el.style.transform = '';
      }
    });
  }, 100);
}

// ── Flash Auto-dismiss ───────────────────────────────────────────────────────
document.querySelectorAll('.flash').forEach((flash, i) => {
  setTimeout(() => {
    flash.style.transition = 'opacity .4s, transform .4s';
    flash.style.opacity = '0';
    flash.style.transform = 'translateX(100%)';
    setTimeout(() => flash.remove(), 400);
  }, 4000 + i * 300);
});

// ── Smooth anchor scroll ─────────────────────────────────────────────────────
document.querySelectorAll('a[href^="#"]').forEach(a => {
  a.addEventListener('click', e => {
    const target = document.querySelector(a.getAttribute('href'));
    if (target) {
      e.preventDefault();
      target.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  });
});

// ── Scroll-reveal for hero elements ─────────────────────────────────────────
const heroEls = document.querySelectorAll('.hero-eyebrow, .hero-name, .hero-title, .hero-bio, .hero-actions, .hero-stats');
heroEls.forEach((el, i) => {
  el.style.opacity = '0';
  el.style.transform = 'translateY(20px)';
  el.style.transition = `opacity .6s ease ${i * 100 + 100}ms, transform .6s ease ${i * 100 + 100}ms`;
  setTimeout(() => {
    el.style.opacity = '1';
    el.style.transform = '';
  }, 50);
});
