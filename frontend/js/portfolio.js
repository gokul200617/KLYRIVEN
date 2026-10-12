/* ============================================================
   KLYRIVEN — PORTFOLIO
   Dynamic project loading and category filtering
   ============================================================ */

(function () {
  'use strict';

  // Static project data — fallback when API is unavailable or loading
  const STATIC_PROJECTS = [
    {
      id: 'static-0',
      slug: 'smart-evacuation-system',
      name: 'Smart Evac Command',
      category: 'Smart Systems & IoT',
      summary: 'We built an entire smart evacuation system for the entire building which tracks the building evacuation status continuously in real time with multi-floor telemetry and emergency controls.',
      live_url: 'https://smart-evacuation-system-zf1z.onrender.com',
      image_urls: [],
      display_order: 1,
    },
    {
      id: 'static-1',
      slug: 'meridian',
      name: 'Meridian',
      category: 'Brand Identity',
      summary: 'A comprehensive visual identity for an international architecture firm, built around precision and spatial clarity.',
      image_urls: [],
      display_order: 2,
    },
    {
      id: 'static-2',
      slug: 'crestline',
      name: 'Crestline',
      category: 'E-commerce',
      summary: 'A bespoke luxury e-commerce platform with editorial product presentation and seamless checkout.',
      image_urls: [],
      display_order: 3,
    },
    {
      id: 'static-3',
      slug: 'solance',
      name: 'Solance',
      category: 'Digital Strategy',
      summary: 'Strategic repositioning and digital growth for a premium wellness brand entering international markets.',
      image_urls: [],
      display_order: 4,
    },
    {
      id: 'static-4',
      slug: 'apex-bureau',
      name: 'Apex Bureau',
      category: 'Web Design',
      summary: 'A refined digital presence for a professional services firm, combining authority with approachability.',
      image_urls: [],
      display_order: 5,
    },
    {
      id: 'static-5',
      slug: 'verdant',
      name: 'Verdant',
      category: 'Brand Identity',
      summary: 'A considered identity system for a sustainable goods brand, rooted in material honesty and craft.',
      image_urls: [],
      display_order: 6,
    },
    {
      id: 'static-6',
      slug: 'omnis',
      name: 'Omnis',
      category: 'E-commerce',
      summary: 'An editorial-led online store for a lifestyle brand, where shopping feels as considered as the product.',
      image_urls: [],
      display_order: 7,
    },
  ];

  // SVG placeholders — unique geometric compositions per project
  const SVG_PLACEHOLDERS = {
    'smart-evacuation-system': `<svg viewBox="0 0 600 400" xmlns="http://www.w3.org/2000/svg" width="100%" height="100%">
      <rect width="600" height="400" fill="#111328"/>
      <!-- Multi-Floor Building Structure -->
      <rect x="70" y="50" width="460" height="300" rx="4" fill="none" stroke="#AFAEA2" stroke-width="0.8" opacity="0.3"/>
      <!-- Floor 2 -->
      <line x1="70" y1="150" x2="530" y2="150" stroke="#AFAEA2" stroke-width="0.8" stroke-dasharray="4 4" opacity="0.4"/>
      <!-- Floor 1 -->
      <line x1="70" y1="250" x2="530" y2="250" stroke="#AFAEA2" stroke-width="0.8" stroke-dasharray="4 4" opacity="0.4"/>
      <!-- Floor labels -->
      <text x="85" y="85" font-family="monospace" font-size="11" fill="#AFAEA2" opacity="0.7">FLOOR 02 // SENSORS ONLINE</text>
      <text x="85" y="185" font-family="monospace" font-size="11" fill="#AFAEA2" opacity="0.7">FLOOR 01 // EVAC STATUS: ACTIVE</text>
      <text x="85" y="285" font-family="monospace" font-size="11" fill="#AFAEA2" opacity="0.7">FLOOR 00 // GROUND EXIT CLEAR</text>
      <!-- Floor 2 nodes & signal waves -->
      <rect x="85" y="105" width="80" height="28" rx="3" fill="#1B1E4A" stroke="#AFAEA2" stroke-width="0.5" opacity="0.9"/>
      <circle cx="100" cy="119" r="4" fill="#2ECC71"/>
      <text x="112" y="123" font-family="monospace" font-size="9" fill="#F2F0E8">ZONE 2A</text>
      <rect x="180" y="105" width="80" height="28" rx="3" fill="#1B1E4A" stroke="#AFAEA2" stroke-width="0.5" opacity="0.9"/>
      <circle cx="195" cy="119" r="4" fill="#2ECC71"/>
      <text x="207" y="123" font-family="monospace" font-size="9" fill="#F2F0E8">ZONE 2B</text>
      <!-- Telemetry Sparkline on Floor 2 -->
      <path d="M 280 119 Q 310 95, 340 120 T 400 115 T 450 125 T 510 110" fill="none" stroke="#2ECC71" stroke-width="1.5" opacity="0.85"/>
      <!-- Floor 1 Alert Nodes & Dynamic Evacuation Vector -->
      <rect x="85" y="205" width="80" height="28" rx="3" fill="#1B1E4A" stroke="#D21319" stroke-width="1" opacity="0.95"/>
      <circle cx="100" cy="219" r="4" fill="#D21319"/>
      <text x="112" y="223" font-family="monospace" font-size="9" fill="#F2F0E8">ZONE 1A</text>
      <rect x="180" y="205" width="80" height="28" rx="3" fill="#1B1E4A" stroke="#AFAEA2" stroke-width="0.5" opacity="0.9"/>
      <circle cx="195" cy="219" r="4" fill="#E67E22"/>
      <text x="207" y="223" font-family="monospace" font-size="9" fill="#F2F0E8">ZONE 1B</text>
      <!-- Telemetry anomaly spike -->
      <path d="M 280 225 L 320 220 L 350 190 L 370 230 L 410 215 L 450 225 L 510 220" fill="none" stroke="#D21319" stroke-width="1.8"/>
      <circle cx="350" cy="190" r="3" fill="#D21319"/>
      <!-- Evacuation Arrow path down to ground floor -->
      <path d="M 480 120 L 480 315 L 430 315" fill="none" stroke="#2ECC71" stroke-width="2" stroke-dasharray="6 3"/>
      <polygon points="430,311 420,315 430,319" fill="#2ECC71"/>
      <text x="340" y="320" font-family="monospace" font-size="10" fill="#2ECC71" letter-spacing="1">EGRESS ROUTE</text>
      <!-- Ground Floor status -->
      <rect x="85" y="305" width="100" height="28" rx="3" fill="#1B1E4A" stroke="#2ECC71" stroke-width="0.8"/>
      <circle cx="100" cy="319" r="4" fill="#2ECC71"/>
      <text x="112" y="323" font-family="monospace" font-size="9" fill="#2ECC71">MAIN EXIT</text>
      <!-- Realtime Telemetry Pulse Badge -->
      <rect x="410" y="65" width="105" height="20" rx="10" fill="#13163A" stroke="#D21319" stroke-width="0.8"/>
      <circle cx="422" cy="75" r="3" fill="#D21319"/>
      <text x="432" y="79" font-family="monospace" font-size="8" fill="#F2F0E8" letter-spacing="1">LIVE TELEMETRY</text>
    </svg>`,
    'meridian': `<svg viewBox="0 0 600 400" xmlns="http://www.w3.org/2000/svg" width="100%" height="100%">
      <rect width="600" height="400" fill="#13163A"/>
      <rect x="80" y="60" width="180" height="280" fill="none" stroke="#AFAEA2" stroke-width="1" opacity="0.4"/>
      <rect x="100" y="80" width="140" height="240" fill="none" stroke="#AFAEA2" stroke-width="0.5" opacity="0.25"/>
      <line x1="80" y1="200" x2="440" y2="200" stroke="#D21319" stroke-width="1" opacity="0.6"/>
      <circle cx="380" cy="180" r="80" fill="none" stroke="#AFAEA2" stroke-width="1" opacity="0.3"/>
      <circle cx="380" cy="180" r="55" fill="none" stroke="#AFAEA2" stroke-width="0.5" opacity="0.2"/>
      <rect x="300" y="240" width="160" height="100" fill="#1B1E4A" opacity="0.8"/>
      <text x="340" y="300" font-family="serif" font-size="12" fill="#AFAEA2" opacity="0.5" letter-spacing="4">MERIDIAN</text>
    </svg>`,
    'crestline': `<svg viewBox="0 0 600 400" xmlns="http://www.w3.org/2000/svg" width="100%" height="100%">
      <rect width="600" height="400" fill="#1B1E4A"/>
      <polygon points="300,40 520,360 80,360" fill="none" stroke="#AFAEA2" stroke-width="1" opacity="0.3"/>
      <polygon points="300,100 460,340 140,340" fill="none" stroke="#F2F0E8" stroke-width="0.5" opacity="0.12"/>
      <circle cx="300" cy="220" r="60" fill="#D21319" opacity="0.15"/>
      <circle cx="300" cy="220" r="40" fill="none" stroke="#D21319" stroke-width="1" opacity="0.4"/>
      <line x1="0" y1="320" x2="600" y2="320" stroke="#AFAEA2" stroke-width="0.5" opacity="0.3"/>
      <rect x="260" y="340" width="80" height="1" fill="#D21319"/>
    </svg>`,
    'solance': `<svg viewBox="0 0 600 400" xmlns="http://www.w3.org/2000/svg" width="100%" height="100%">
      <rect width="600" height="400" fill="#13163A"/>
      <ellipse cx="300" cy="200" rx="200" ry="150" fill="none" stroke="#AFAEA2" stroke-width="1" opacity="0.25"/>
      <ellipse cx="300" cy="200" rx="140" ry="105" fill="none" stroke="#F2F0E8" stroke-width="0.5" opacity="0.15"/>
      <ellipse cx="300" cy="200" rx="80" ry="60" fill="#1B1E4A" opacity="0.9"/>
      <line x1="100" y1="50" x2="500" y2="350" stroke="#D21319" stroke-width="0.75" opacity="0.5"/>
      <line x1="500" y1="50" x2="100" y2="350" stroke="#AFAEA2" stroke-width="0.5" opacity="0.2"/>
      <circle cx="300" cy="200" r="8" fill="#D21319" opacity="0.8"/>
    </svg>`,
    'apex-bureau': `<svg viewBox="0 0 600 400" xmlns="http://www.w3.org/2000/svg" width="100%" height="100%">
      <rect width="600" height="400" fill="#1B1E4A"/>
      <rect x="60" y="60" width="480" height="280" fill="none" stroke="#AFAEA2" stroke-width="0.5" opacity="0.2"/>
      <rect x="60" y="60" width="200" height="280" fill="#13163A" opacity="0.6"/>
      <line x1="260" y1="60" x2="260" y2="340" stroke="#D21319" stroke-width="1" opacity="0.5"/>
      <rect x="280" y="100" width="220" height="80" fill="none" stroke="#AFAEA2" stroke-width="0.5" opacity="0.3"/>
      <rect x="280" y="200" width="140" height="1" fill="#F2F0E8" opacity="0.4"/>
      <rect x="280" y="220" width="180" height="1" fill="#AFAEA2" opacity="0.25"/>
      <rect x="280" y="240" width="100" height="1" fill="#AFAEA2" opacity="0.25"/>
    </svg>`,
    'verdant': `<svg viewBox="0 0 600 400" xmlns="http://www.w3.org/2000/svg" width="100%" height="100%">
      <rect width="600" height="400" fill="#13163A"/>
      <path d="M 80 380 Q 200 80 300 200 Q 400 320 520 80" fill="none" stroke="#AFAEA2" stroke-width="1.5" opacity="0.4"/>
      <path d="M 80 380 Q 200 120 300 200 Q 400 280 520 80" fill="none" stroke="#F2F0E8" stroke-width="0.5" opacity="0.15"/>
      <circle cx="300" cy="200" r="4" fill="#D21319"/>
      <circle cx="200" cy="240" r="2" fill="#AFAEA2" opacity="0.5"/>
      <circle cx="400" cy="160" r="2" fill="#AFAEA2" opacity="0.5"/>
      <rect x="40" y="340" width="520" height="1" fill="#AFAEA2" opacity="0.15"/>
    </svg>`,
    'omnis': `<svg viewBox="0 0 600 400" xmlns="http://www.w3.org/2000/svg" width="100%" height="100%">
      <rect width="600" height="400" fill="#1B1E4A"/>
      <rect x="80" y="80" width="160" height="240" fill="#13163A"/>
      <rect x="360" y="80" width="160" height="240" fill="#13163A"/>
      <rect x="80" y="80" width="160" height="240" fill="none" stroke="#AFAEA2" stroke-width="0.5" opacity="0.3"/>
      <rect x="360" y="80" width="160" height="240" fill="none" stroke="#AFAEA2" stroke-width="0.5" opacity="0.3"/>
      <line x1="240" y1="80" x2="360" y2="80" stroke="#D21319" stroke-width="1.5" opacity="0.6"/>
      <line x1="240" y1="320" x2="360" y2="320" stroke="#D21319" stroke-width="1.5" opacity="0.6"/>
      <circle cx="300" cy="200" r="50" fill="none" stroke="#F2F0E8" stroke-width="0.5" opacity="0.2"/>
    </svg>`,
  };

  function getSVG(slug) {
    return SVG_PLACEHOLDERS[slug] || SVG_PLACEHOLDERS['meridian'];
  }

  function renderProjectCard(project, index) {
    const card = document.createElement('a');
    card.className = 'project-card reveal';
    card.setAttribute('data-category', project.category);
    card.style.transitionDelay = `${index * 0.08}s`;

    const projectLink = project.live_url || (project.slug === 'smart-evacuation-system' ? 'https://smart-evacuation-system-zf1z.onrender.com' : '#');
    card.href = projectLink;
    if (projectLink.startsWith('http')) {
      card.target = '_blank';
      card.rel = 'noopener noreferrer';
    }

    const hasImage = project.image_urls && project.image_urls.length > 0;
    const imageHTML = hasImage
      ? `<img src="${project.image_urls[0]}" alt="${project.name}" class="project-card__image img-fill" loading="lazy"/>`
      : `<div class="project-card__placeholder">${getSVG(project.slug)}</div>`;

    const liveBadge = projectLink.startsWith('http')
      ? `<span style="display:inline-flex;align-items:center;gap:4px;font-size:0.68rem;letter-spacing:0.06em;color:var(--color-crimson);text-transform:uppercase;font-weight:600;margin-left:auto;">Live System ↗</span>`
      : '';

    card.innerHTML = `
      <div class="project-card__visual aspect-3-2">
        ${imageHTML}
        <div class="project-card__overlay"></div>
      </div>
      <div class="project-card__info">
        <div style="display:flex;align-items:center;justify-content:space-between;gap:8px;">
          <span class="project-card__category label">${project.category}</span>
          ${liveBadge}
        </div>
        <h3 class="project-card__name">${project.name}</h3>
        <p class="project-card__desc">${project.summary}</p>
      </div>
    `;

    return card;
  }

  function renderGrid(projects) {
    const grid = document.getElementById('portfolio-grid');
    if (!grid) return;

    grid.innerHTML = '';

    if (!projects.length) {
      grid.innerHTML = `<p class="portfolio-empty">No projects found in this category.</p>`;
      return;
    }

    projects.forEach((project, i) => {
      grid.appendChild(renderProjectCard(project, i));
    });

    // Trigger reveal for newly added elements
    const anim = window.KlyrivenAnimations || window.AddWorkAnimations;
    if (anim && anim.refreshReveal) {
      anim.refreshReveal();
    } else {
      // Manually trigger IntersectionObserver if animations.js didn't register hook
      const newReveals = grid.querySelectorAll('.reveal');
      const observer = new IntersectionObserver(
        (entries) => {
          entries.forEach(entry => {
            if (entry.isIntersecting) {
              entry.target.classList.add('is-visible');
              observer.unobserve(entry.target);
            }
          });
        },
        { threshold: 0.1, rootMargin: '0px 0px -40px 0px' }
      );
      newReveals.forEach(el => observer.observe(el));
    }
  }

  function initFilters(allProjects) {
    const tabs = document.querySelectorAll('.filter-tab');
    if (!tabs.length) return;

    tabs.forEach(tab => {
      tab.addEventListener('click', () => {
        // Update active state
        tabs.forEach(t => t.classList.remove('is-active'));
        tab.classList.add('is-active');

        const category = tab.getAttribute('data-filter');

        const filtered = category === 'all'
          ? allProjects
          : allProjects.filter(p => {
              const cat = (p.category || '').toLowerCase();
              const catSlug = cat.replace(/\s+/g, '-');
              const filterNormalized = category.toLowerCase().replace(/-/g, ' ');
              return cat.includes(filterNormalized) ||
                     catSlug.includes(category.toLowerCase()) ||
                     (category === 'smart-systems' && (cat.includes('smart') || cat.includes('iot')));
            });

        renderGrid(filtered);
      });
    });
  }

  async function initPortfolio() {
    const grid = document.getElementById('portfolio-grid');
    if (!grid) return;

    // Show loading state
    grid.innerHTML = `<div class="portfolio-loading">
      <div class="spinner" style="margin:auto;"></div>
    </div>`;

    let projects = [];

    try {
      const apiClient = window.KlyrivenAPI || window.AddWorkAPI;
      if (apiClient) {
        projects = await apiClient.getProjects();
      }
    } catch {
      projects = [];
    }

    // Fall back to static data if API returns nothing
    if (!projects || !projects.length) {
      projects = STATIC_PROJECTS;
    }

    renderGrid(projects);
    initFilters(projects);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initPortfolio);
  } else {
    initPortfolio();
  }

})();

