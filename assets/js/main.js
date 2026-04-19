// Minimal interactions for the portfolio
// - Footer year
// - Mobile navigation (accessible)
// - Reveal on scroll (IntersectionObserver)
// - Smooth scroll for internal anchors

(() => {
  // Footer year
  const yearEl = document.getElementById('year');
  if (yearEl) yearEl.textContent = String(new Date().getFullYear());

  // Mobile navigation
  const toggle = document.querySelector('.nav-toggle');
  const navList = document.getElementById('nav-list');

  function closeMenu() {
    if (!navList || !toggle) return;
    navList.classList.remove('open');
    toggle.setAttribute('aria-expanded', 'false');
  }

  function openMenu() {
    if (!navList || !toggle) return;
    navList.classList.add('open');
    toggle.setAttribute('aria-expanded', 'true');
  }

  if (toggle && navList) {
    toggle.addEventListener('click', () => {
      const isOpen = navList.classList.toggle('open');
      toggle.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
    });

    // Close on link click
    navList.addEventListener('click', (e) => {
      const target = e.target;
      if (target instanceof Element && target.closest('a')) {
        closeMenu();
      }
    });

    // Click outside to close
    document.addEventListener('click', (e) => {
      const target = e.target;
      const clickedToggle = target instanceof Element && target.closest('.nav-toggle');
      const clickedMenu = target instanceof Element && target.closest('#nav-list');
      if (!clickedToggle && !clickedMenu) {
        closeMenu();
      }
    });

    // Escape to close
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') closeMenu();
    });
  }

  // Reveal on scroll
  const prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)');
  const revealEls = Array.from(document.querySelectorAll('.reveal'));

  if (prefersReduced.matches) {
    revealEls.forEach((el) => el.classList.add('in-view'));
  } else if ('IntersectionObserver' in window) {
    const io = new IntersectionObserver((entries, obs) => {
      for (const entry of entries) {
        if (entry.isIntersecting) {
          entry.target.classList.add('in-view');
          obs.unobserve(entry.target);
        }
      }
    }, { root: null, rootMargin: '0px 0px -10% 0px', threshold: 0.15 });
    revealEls.forEach((el) => io.observe(el));
  } else {
    // Fallback: show all
    revealEls.forEach((el) => el.classList.add('in-view'));
  }

  // Letter-by-letter hero animation
  const heroTitle = document.querySelector('.hero-title[data-animate="letters"]');
  if (heroTitle && heroTitle.textContent) {
    const original = heroTitle.textContent;
    if (!prefersReduced.matches) {
      heroTitle.setAttribute('aria-label', original);
      const frag = document.createDocumentFragment();
      const text = original;
      let segments = [];
      if (typeof Intl !== 'undefined' && 'Segmenter' in Intl) {
        const seg = new Intl.Segmenter('fr', { granularity: 'grapheme' });
        segments = Array.from(seg.segment(text), (s) => s.segment);
      } else {
        segments = Array.from(text);
      }
      heroTitle.textContent = '';
      let idx = 0;
      for (const ch of segments) {
        if (/\s/.test(ch)) {
          frag.appendChild(document.createTextNode(ch));
        } else {
          const span = document.createElement('span');
          span.className = 'char';
          span.textContent = ch;
          span.setAttribute('aria-hidden', 'true');
          span.style.animationDelay = `${Math.min(idx * 0.025, 1.6)}s`;
          frag.appendChild(span);
          idx++;
        }
      }
      heroTitle.appendChild(frag);
    }
  }

  // Prevent reload when clicking current-page nav links
  const navLinks = Array.from(document.querySelectorAll('.nav-list a[href], .brand[href]'));
  navLinks.forEach((link) => {
    try {
      const href = link.getAttribute('href');
      if (!href) return;
      // Ignore external links and mailto
      if (/^https?:\/\//i.test(href) || href.startsWith('mailto:')) return;
      const linkUrl = new URL(href, window.location.origin);
      const current = new URL(window.location.href);
      // Compare pathnames (and optionally search/hash if needed)
      if (linkUrl.pathname === current.pathname) {
        link.setAttribute('aria-current', 'page');
        link.classList.add('is-current');
        link.addEventListener('click', (e) => {
          // Prevent reload/spam click
          e.preventDefault();
        });
      }
    } catch (_) {
      // ignore malformed URLs
    }
  });

  // Smooth scroll for internal anchors
  const anchorLinks = Array.from(document.querySelectorAll('a[href^="#"]'));
  anchorLinks.forEach((a) => {
    a.addEventListener('click', (e) => {
      const href = a.getAttribute('href');
      if (!href || href === '#' || href.length < 2) return;
      const target = document.querySelector(href);
      if (!target) return;
      e.preventDefault();
      const behavior = prefersReduced.matches ? 'auto' : 'smooth';
      target.scrollIntoView({ behavior, block: 'start' });
      // Optionally update hash without jumping
      if (history.replaceState) {
        history.replaceState(null, '', href);
      }
      // Close mobile menu after navigation
      closeMenu();
    });
  });
    // Header border on scroll
  const header = document.querySelector('.site-header');
  if (header) {
    const updateHeaderBorder = () => {
      if (window.scrollY > 0) header.classList.add('is-scrolled');
      else header.classList.remove('is-scrolled');
    };
    updateHeaderBorder(); // initialize on load (in case of refresh/hash)
    window.addEventListener('scroll', updateHeaderBorder, { passive: true });
  }

  // Copy buttons for code blocks in articles
  const codeBlocks = Array.from(document.querySelectorAll('article pre'));
  if (codeBlocks.length) {
    const getPreText = (pre) => {
      const clone = pre.cloneNode(true);
      const extras = clone.querySelectorAll('.copy-btn');
      extras.forEach((el) => el.remove());
      return (clone.textContent || '').replace(/\n\s*Copier\s*$/i, '');
    };

    codeBlocks.forEach((pre) => {
      // Avoid duplicating buttons if script runs twice
      if (pre.querySelector('.copy-btn')) return;
      const btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'copy-btn';
      btn.setAttribute('aria-label', 'Copier le code');
      btn.textContent = 'Copier';
      pre.style.position = pre.style.position || 'relative';
      pre.appendChild(btn);

      const setFeedback = (success) => {
        const original = 'Copier';
        btn.textContent = success ? 'Copié !' : 'Échec';
        btn.disabled = false;
        setTimeout(() => { btn.textContent = original; }, 1500);
      };

      btn.addEventListener('click', async () => {
        const text = getPreText(pre).trim();
        if (!text) { setFeedback(false); return; }
        try {
          if (navigator.clipboard && navigator.clipboard.writeText) {
            await navigator.clipboard.writeText(text);
          } else {
            throw new Error('Clipboard API not available');
          }
          setFeedback(true);
        } catch (_) {
          try {
            const ta = document.createElement('textarea');
            ta.value = text;
            // Make offscreen but still selectable
            ta.style.position = 'fixed';
            ta.style.top = '-1000px';
            document.body.appendChild(ta);
            ta.focus();
            ta.select();
            const ok = document.execCommand ? document.execCommand('copy') : false;
            document.body.removeChild(ta);
            setFeedback(!!ok);
          } catch (e) {
            setFeedback(false);
          }
        }
      });
    });
  }


})();

// === BTS additions: filtres veille + onglets parcours ===
(() => {
  const filterBtns = document.querySelectorAll('.filter-btn');
  const newsCards = document.querySelectorAll('.news-card');
  filterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const f = btn.dataset.filter;
      filterBtns.forEach(b => b.classList.toggle('active', b === btn));
      newsCards.forEach(c => {
        c.style.display = (f === 'all' || c.dataset.category === f) ? '' : 'none';
      });
    });
  });

  const tabBtns = document.querySelectorAll('.tab-btn');
  const tabPanels = document.querySelectorAll('.tab-panel');
  tabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const t = btn.dataset.tab;
      tabBtns.forEach(b => b.classList.toggle('active', b === btn));
      tabPanels.forEach(p => p.classList.toggle('active', p.id === t));
    });
  });
})();

// === Veille dynamique : chargement depuis assets/data/news.json ===
(() => {
  const grid = document.getElementById('veille-news');
  if (!grid) return;

  const CAT_LABELS = {
    cve:        'CVE',
    malware:    'Malware',
    ransomware: 'Ransomware',
    apt:        'APT',
    outil:      'Outil',
    actualite:  'Actualité',
  };

  const fmtDate = (iso) => {
    if (!iso) return '';
    try {
      const d = new Date(iso);
      return d.toLocaleDateString('fr-FR', { day: '2-digit', month: 'short', year: 'numeric' });
    } catch { return iso; }
  };

  const escape = (s) => String(s || '').replace(/[&<>"']/g, (c) => (
    { '&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;' }[c]
  ));

  const renderItem = (item, i) => {
    const cat = CAT_LABELS[item.category] ? item.category : 'actualite';
    const label = CAT_LABELS[cat];
    const delayClass = i % 3 === 1 ? ' delay-1' : i % 3 === 2 ? ' delay-2' : '';
    return `
      <article class="news-card reveal${delayClass}" data-category="${cat}">
        <div class="news-meta">
          <span class="news-date">${fmtDate(item.date_iso || item.date)}</span>
          <span class="news-tag ${cat}">${label}</span>
          <span class="news-date">· ${escape(item.source)}</span>
        </div>
        <h3>${escape(item.title)}</h3>
        <p>${escape(item.summary || '')}</p>
        <a class="news-source" href="${escape(item.url)}" target="_blank" rel="noopener noreferrer">Lire l'article →</a>
      </article>`;
  };

  const wireFilters = () => {
    const filterBtns = document.querySelectorAll('.filter-btn');
    const cards = document.querySelectorAll('.news-card');
    filterBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        const f = btn.dataset.filter;
        filterBtns.forEach(b => b.classList.toggle('active', b === btn));
        cards.forEach(c => {
          c.style.display = (f === 'all' || c.dataset.category === f) ? '' : 'none';
        });
      });
    });
  };

  const wireReveal = () => {
    if ('IntersectionObserver' in window) {
      const io = new IntersectionObserver((entries, obs) => {
        for (const e of entries) {
          if (e.isIntersecting) { e.target.classList.add('in-view'); obs.unobserve(e.target); }
        }
      }, { rootMargin: '0px 0px -10% 0px', threshold: 0.15 });
      grid.querySelectorAll('.reveal').forEach(el => io.observe(el));
    } else {
      grid.querySelectorAll('.reveal').forEach(el => el.classList.add('in-view'));
    }
  };

  fetch('assets/data/news.json', { cache: 'no-cache' })
    .then(r => { if (!r.ok) throw new Error('HTTP ' + r.status); return r.json(); })
    .then(data => {
      const items = (data && data.items) || [];
      if (!items.length) {
        grid.innerHTML = '<p class="news-date" style="grid-column:1/-1;">Aucune actualité disponible.</p>';
        return;
      }
      grid.innerHTML = items.map(renderItem).join('');
      const upd = document.getElementById('veille-last-update');
      if (upd && data.generated_at) upd.textContent = fmtDate(data.generated_at);
      wireFilters();
      wireReveal();
    })
    .catch(err => {
      grid.innerHTML = `
        <p class="news-date" style="grid-column:1/-1;">
          Impossible de charger la veille (${escape(err.message)}).
          Le flux est généré par GitHub Actions toutes les 6h.
        </p>`;
    });
})();
