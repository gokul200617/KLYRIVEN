/* ============================================================
   KLYRIVEN — APP
   Application bootstrap — initializes shared behaviours
   across all pages.
   ============================================================ */

(function () {
  'use strict';

  // ── Page transition overlay ───────────────────────────────

  function initPageTransitions() {
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

    // Create transition element
    const transition = document.createElement('div');
    transition.className = 'page-transition';
    document.body.appendChild(transition);

    // On page link clicks
    document.querySelectorAll('a[href]').forEach(link => {
      const href = link.getAttribute('href');
      // Only handle same-origin internal links
      if (
        !href ||
        href.startsWith('#') ||
        href.startsWith('mailto:') ||
        href.startsWith('tel:') ||
        href.startsWith('http') ||
        link.target === '_blank'
      ) return;

      link.addEventListener('click', (e) => {
        e.preventDefault();
        transition.classList.add('is-entering');
        setTimeout(() => {
          window.location.href = href;
        }, 500);
      });
    });

    // On page load — animate out
    window.addEventListener('pageshow', () => {
      transition.classList.remove('is-entering');
      transition.classList.add('is-leaving');
      setTimeout(() => {
        transition.classList.remove('is-leaving');
      }, 600);
    });
  }

  // ── Lazy load images ──────────────────────────────────────

  function initLazyLoad() {
    if ('loading' in HTMLImageElement.prototype) {
      // Native lazy loading supported
      return;
    }

    // Fallback for browsers without native lazy loading
    const images = document.querySelectorAll('img[loading="lazy"]');
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const img = entry.target;
          if (img.dataset.src) {
            img.src = img.dataset.src;
          }
          observer.unobserve(img);
        }
      });
    });

    images.forEach(img => observer.observe(img));
  }

  // ── Smooth scroll for anchor links ────────────────────────

  function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(link => {
      link.addEventListener('click', (e) => {
        const target = document.querySelector(link.getAttribute('href'));
        if (!target) return;
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        // Update URL without triggering navigation
        history.pushState(null, '', link.getAttribute('href'));
      });
    });
  }

  // ── Year auto-update for copyright ────────────────────────

  function initCopyrightYear() {
    const yearEl = document.querySelector('.js-year');
    if (yearEl) yearEl.textContent = new Date().getFullYear();
  }

  // ── Filter tabs (shared utility) ─────────────────────────

  function initFilterTabs() {
    const tabs = document.querySelectorAll('.filter-tab');
    if (!tabs.length) return;

    tabs.forEach(tab => {
      tab.addEventListener('click', () => {
        tabs.forEach(t => t.classList.remove('is-active'));
        tab.classList.add('is-active');
        // Filtering logic is in portfolio.js
      });

      tab.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          tab.click();
        }
      });
    });
  }

  // ── Header skip link ──────────────────────────────────────

  function initSkipLink() {
    const skip = document.querySelector('.skip-link');
    const main = document.querySelector('#main-content');
    if (!skip || !main) return;

    skip.addEventListener('click', (e) => {
      e.preventDefault();
      main.tabIndex = -1;
      main.focus();
      main.scrollIntoView({ behavior: 'smooth' });
    });
  }

  // ── Init ─────────────────────────────────────────────────

  function init() {
    initLazyLoad();
    initSmoothScroll();
    initCopyrightYear();
    initFilterTabs();
    initSkipLink();

    // Defer page transitions slightly to ensure DOM is settled
    setTimeout(initPageTransitions, 100);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

})();

