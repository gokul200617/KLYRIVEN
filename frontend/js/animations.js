/* ============================================================
   KLYRIVEN — ANIMATIONS
   IntersectionObserver scroll reveals, hero entrance,
   marquee, and subtle motion enhancements.
   Respects prefers-reduced-motion.
   ============================================================ */

(function () {
  'use strict';

  const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  let revealObserver = null;

  // ── Scroll Reveal ─────────────────────────────────────────

  function refreshReveal() {
    if (prefersReducedMotion) {
      document.querySelectorAll('.reveal:not(.is-visible)').forEach(el => el.classList.add('is-visible'));
      return;
    }
    if (revealObserver) {
      document.querySelectorAll('.reveal:not(.is-visible)').forEach(el => revealObserver.observe(el));
    }
  }

  function initScrollReveal() {
    const elements = document.querySelectorAll('.reveal');
    if (!elements.length) return;

    if (prefersReducedMotion) {
      elements.forEach(el => el.classList.add('is-visible'));
      return;
    }

    revealObserver = new IntersectionObserver(
      (entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            entry.target.classList.add('is-visible');
            revealObserver.unobserve(entry.target);
          }
        });
      },
      {
        threshold: 0.12,
        rootMargin: '0px 0px -60px 0px',
      }
    );

    elements.forEach(el => revealObserver.observe(el));
  }

  // ── Hero Entrance ─────────────────────────────────────────

  function initHeroEntrance() {
    if (prefersReducedMotion) {
      document.querySelectorAll('.hero__label, .hero__title, .hero__footer, .hero__mark, .hero__scroll, .hero__preview-card')
        .forEach(el => el.classList.add('is-visible'));
      return;
    }

    const label = document.querySelector('.hero__label');
    const title = document.querySelector('.hero__title');
    const footer = document.querySelector('.hero__footer');
    const mark = document.querySelector('.hero__mark');
    const scroll = document.querySelector('.hero__scroll');
    const previewCard = document.querySelector('.hero__preview-card');

    // Staggered entrance
    const sequence = [
      { el: label, delay: 200 },
      { el: title, delay: 350 },
      { el: footer, delay: 550 },
      { el: mark, delay: 300 },
      { el: scroll, delay: 1200 },
      { el: previewCard, delay: 1000 },
    ];

    sequence.forEach(({ el, delay }) => {
      if (!el) return;
      setTimeout(() => el.classList.add('is-visible'), delay);
    });
  }

  // ── Service row hover expansion ───────────────────────────

  function initServiceRows() {
    const rows = document.querySelectorAll('.service-row');
    rows.forEach(row => {
      // Already handled by CSS — this ensures keyboard focus also triggers
      row.addEventListener('focus', () => row.classList.add('is-focused'));
      row.addEventListener('blur', () => row.classList.remove('is-focused'));
    });
  }

  // ── Filter tabs (portfolio page) ──────────────────────────
  // NOTE: See portfolio.js for full filter logic.

  // ── Cursor dot (desktop only) ─────────────────────────────

  function initCursor() {
    if (prefersReducedMotion) return;
    if (window.innerWidth < 1024) return;

    const cursor = document.querySelector('.cursor');
    if (!cursor) return;

    let mouseX = 0, mouseY = 0;
    let cursorX = 0, cursorY = 0;

    document.addEventListener('mousemove', (e) => {
      mouseX = e.clientX;
      mouseY = e.clientY;
      cursor.classList.add('is-visible');
    });

    document.addEventListener('mouseleave', () => {
      cursor.classList.remove('is-visible');
    });

    function animateCursor() {
      cursorX += (mouseX - cursorX) * 0.18;
      cursorY += (mouseY - cursorY) * 0.18;
      cursor.style.left = cursorX + 'px';
      cursor.style.top = cursorY + 'px';
      requestAnimationFrame(animateCursor);
    }

    animateCursor();
  }

  // ── Parallax subtle on hero ───────────────────────────────

  function initHeroParallax() {
    if (prefersReducedMotion) return;
    const mark = document.querySelector('.hero__mark');
    if (!mark) return;

    window.addEventListener('scroll', () => {
      const scrolled = window.scrollY;
      mark.style.transform = `rotate(-12deg) translateY(${scrolled * 0.15}px) scale(1)`;
    }, { passive: true });
  }

  // ── Stat counter animation ────────────────────────────────

  function animateCounter(el, target, suffix) {
    if (prefersReducedMotion) {
      el.textContent = target + suffix;
      return;
    }

    const start = 0;
    const duration = 1500;
    const startTime = performance.now();

    function update(currentTime) {
      const elapsed = currentTime - startTime;
      const progress = Math.min(elapsed / duration, 1);
      // Ease out quad
      const eased = 1 - (1 - progress) * (1 - progress);
      const current = Math.floor(eased * target);
      el.textContent = current + suffix;
      if (progress < 1) requestAnimationFrame(update);
    }

    requestAnimationFrame(update);
  }

  function initStats() {
    const statValues = document.querySelectorAll('.stat-item__value');
    if (!statValues.length) return;

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            const el = entry.target;
            const text = el.textContent.trim();
            const match = text.match(/^(\d+)(.*)$/);
            if (match) {
              const num = parseInt(match[1], 10);
              const suffix = match[2];
              animateCounter(el, num, suffix);
            }
            observer.unobserve(el);
          }
        });
      },
      { threshold: 0.5 }
    );

    statValues.forEach(el => observer.observe(el));
  }

  // ── Project card tilt ─────────────────────────────────────

  function initCardTilt() {
    if (prefersReducedMotion) return;
    if (window.innerWidth < 1024) return;

    const cards = document.querySelectorAll('.project-card__visual');
    cards.forEach(card => {
      card.addEventListener('mousemove', (e) => {
        const rect = card.getBoundingClientRect();
        const x = (e.clientX - rect.left) / rect.width - 0.5;
        const y = (e.clientY - rect.top) / rect.height - 0.5;

        card.style.transform = `
          perspective(600px)
          rotateY(${x * 4}deg)
          rotateX(${-y * 4}deg)
          scale(1.02)
        `;
      });

      card.addEventListener('mouseleave', () => {
        card.style.transform = '';
        card.style.transition = 'transform 0.5s cubic-bezier(0.16, 1, 0.3, 1)';
        setTimeout(() => {
          card.style.transition = '';
        }, 500);
      });
    });
  }

  // ── Init all ──────────────────────────────────────────────

  function init() {
    initScrollReveal();
    initHeroEntrance();
    initServiceRows();
    initCursor();
    initHeroParallax();
    initStats();
    initCardTilt();
  }

  window.KlyrivenAnimations = {
    refreshReveal,
  };
  window.AddWorkAnimations = window.KlyrivenAnimations;

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

})();

