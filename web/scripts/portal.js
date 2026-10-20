/**
 * Python Practical Lab — Portal JavaScript
 * Minimal: smooth scroll, active nav highlighting, copy-to-clipboard
 */

(function () {
  'use strict';

  // ── Active nav link on scroll ──────────────────────────────────────────
  function initNavHighlight() {
    const sections = document.querySelectorAll('[data-section]');
    const navLinks = document.querySelectorAll('.nav-links a[href^="#"]');

    if (!sections.length || !navLinks.length) return;

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            const id = entry.target.id;
            navLinks.forEach((link) => {
              const active = link.getAttribute('href') === '#' + id;
              link.setAttribute('aria-current', active ? 'page' : 'false');
            });
          }
        });
      },
      { rootMargin: '-20% 0px -70% 0px' }
    );

    sections.forEach((el) => observer.observe(el));
  }

  // ── Copy command to clipboard ──────────────────────────────────────────
  function initCopyButtons() {
    document.querySelectorAll('[data-copy]').forEach((btn) => {
      btn.addEventListener('click', () => {
        const text = btn.getAttribute('data-copy');
        navigator.clipboard.writeText(text).then(() => {
          const original = btn.textContent;
          btn.textContent = 'Copied!';
          setTimeout(() => { btn.textContent = original; }, 1800);
        }).catch(() => {
          // Clipboard API unavailable — silent fail
        });
      });
    });
  }

  // ── Entry ──────────────────────────────────────────────────────────────
  document.addEventListener('DOMContentLoaded', () => {
    initNavHighlight();
    initCopyButtons();
  });
})();
