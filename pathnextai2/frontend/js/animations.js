// animations.js — scroll animations, navbar scroll effect

function initNavbar() {
  const nav = document.querySelector('.navbar');
  if (!nav) return;
  window.addEventListener('scroll', () => nav.classList.toggle('scrolled', window.scrollY > 50));
}

function initScrollFade() {
  const obs = new IntersectionObserver(entries => {
    entries.forEach(e => { if (e.isIntersecting) e.target.classList.add('visible'); });
  }, { threshold: 0.12 });
  document.querySelectorAll('.fade-up').forEach(el => obs.observe(el));
}

function showLoading() { const o=document.getElementById('loader'); if(o) o.classList.add('show'); }
function hideLoading() { const o=document.getElementById('loader'); if(o) o.classList.remove('show'); }

document.addEventListener('DOMContentLoaded', () => {
  initNavbar();
  initScrollFade();
  document.querySelectorAll('a[href^="#"]').forEach(a => {
    a.addEventListener('click', e => {
      const t = document.querySelector(a.getAttribute('href'));
      if (t) { e.preventDefault(); t.scrollIntoView({ behavior:'smooth' }); }
    });
  });
});
