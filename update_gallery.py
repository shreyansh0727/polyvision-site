with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace gallery CSS
old_css_s = '  /* ── App Gallery ──────────────────────────── */'
old_css_e = '  /* ── CTA ─────────────────────────────────── */'
new_css = '  /* ── App Gallery (Sticky Scroll) ──────────── */\n  .gallery-scroll-section {\n    position: relative;\n    height: 450vh;\n  }\n  .gallery-sticky {\n    position: sticky;\n    top: 0;\n    height: 100vh;\n    display: flex;\n    align-items: center;\n    justify-content: center;\n    overflow: hidden;\n    background: radial-gradient(ellipse at center, rgba(14,216,107,0.03) 0%, transparent 70%);\n  }\n  .gallery-frame {\n    position: relative;\n    width: min(380px, 88vw);\n    height: min(680px, 84vh);\n  }\n  .gallery-slide {\n    position: absolute;\n    inset: 0;\n    display: flex;\n    flex-direction: column;\n    align-items: center;\n    justify-content: center;\n    will-change: transform, opacity, filter;\n  }\n  .gallery-slide img {\n    width: 100%;\n    height: 100%;\n    object-fit: contain;\n    border-radius: 24px;\n    box-shadow: 0 0 0 2px rgba(14,216,107,0.12), 0 8px 32px rgba(0,0,0,0.4);\n    background: rgba(14,20,32,0.8);\n    backdrop-filter: blur(20px);\n    -webkit-backdrop-filter: blur(20px);\n  }\n  .gallery-slide .gallery-label {\n    position: absolute;\n    bottom: -44px;\n    font-size: 13px;\n    font-weight: 700;\n    color: var(--green);\n    text-transform: uppercase;\n    letter-spacing: 1.5px;\n    font-family: "JetBrains Mono", monospace;\n    text-align: center;\n  }\n  .gallery-nav {\n    position: absolute;\n    bottom: 32px;\n    left: 50%;\n    transform: translateX(-50%);\n    display: flex;\n    gap: 10px;\n    z-index: 10;\n  }\n  .gallery-dot {\n    width: 8px;\n    height: 8px;\n    border-radius: 50%;\n    background: rgba(255,255,255,0.15);\n    transition: all 0.4s var(--ease);\n    cursor: pointer;\n  }\n  .gallery-dot.active {\n    background: var(--green);\n    box-shadow: 0 0 12px rgba(14,216,107,0.5);\n    width: 24px;\n    border-radius: 4px;\n  }\n\n  /* ── CTA ─────────────────────────────────── */\n'

idx1 = content.find(old_css_s)
idx2 = content.find(old_css_e, idx1)
if idx1 >= 0 and idx2 >= 0:
    content = content[:idx1] + new_css + content[idx2:]

# Replace gallery HTML
old_html_s = '<section class="gallery-section">'
old_html_e = '<section id="pricing" style="padding-top: 20px;">'

idx3 = content.find(old_html_s)
idx4 = content.find(old_html_e, idx3)

if idx3 >= 0 and idx4 >= 0:
    new_html = '<section class="gallery-scroll-section">\n  <div class="gallery-sticky" id="gallerySticky">\n    <div class="gallery-frame" id="galleryFrame"></div>\n    <div class="gallery-nav" id="galleryNav"></div>\n  </div>\n</section>\n\n<section id="pricing" style="padding-top: 20px;">\n'
    content = content[:idx3] + new_html + content[idx4 + len(old_html_e):]

# Replace gallery JS
slides_js = '['
for label, img in [
    ('Task Screen', '9e8892cc-d8e3-4122-9f98-207449e6e552.png'),
    ('Employee Tracking Screen', '112160d4-9853-4365-b7ee-a6302e130c81.png'),
    ('Employee Profile', '6d974acc-99d1-4b3c-b88b-48e1b5075696.png'),
    ('Geofence Management', '8c81e9ac-a6a8-48e3-9040-c99c9ee33964.png'),
    ('Send Notification', '31cffac3-717e-46b8-af80-b628f4c7265e.png'),
    ('LoginScreen', '4901dc51-abf1-488d-8d90-ee4f8d53da4a.png'),
]:
    slides_js += '        { label: "' + label + '", img: "/screenshots/' + img + '" },\n'
slides_js += '      ]'

old_js = '// Gallery cards \u2014 individual scroll-in with stagger\ndocument.querySelectorAll(\'.gallery-card\').forEach(el => observer.observe(el));\n\n// Hero is immediately visible'

new_js = '''// ── Sticky Scroll Gallery ────────────────────
const SLIDES = ''' + slides_js + ''';
const SECTION2 = document.getElementById('gallerySticky');
const FRAME = document.getElementById('galleryFrame');
const NAV = document.getElementById('galleryNav');
let slidesEls2 = [];

SLIDES.forEach((s, i) => {
  const el = document.createElement('div');
  el.className = 'gallery-slide';
  el.innerHTML = '<img src="' + s.img + '" alt="' + s.label + '" /><div class="gallery-label">' + s.label + '</div>';
  FRAME.appendChild(el);
  slidesEls2.push(el);
  
  const dot = document.createElement('div');
  dot.className = 'gallery-dot';
  (function(idx) {
    dot.addEventListener('click', function() {
      const section = SECTION2.parentElement;
      const top = section.offsetTop + (idx * section.offsetHeight / (SLIDES.length - 1));
      window.scrollTo({ top: top - 100, behavior: 'smooth' });
    });
  })(i);
  NAV.appendChild(dot);
});

const dots2 = NAV.querySelectorAll('.gallery-dot');
let ticking2 = false;

function updateGallery() {
  const section = SECTION2.parentElement;
  const rect = section.getBoundingClientRect();
  const sectionH = section.offsetHeight - window.innerHeight;
  const scrolled = -rect.top;
  const progress = Math.max(0, Math.min(1, scrolled / sectionH));
  const totalSlides = SLIDES.length;
  const rawIdx = progress * (totalSlides - 1);
  const idx = Math.floor(rawIdx);
  const frac = rawIdx - idx;

  slidesEls2.forEach((el, i) => {
    if (i === idx) {
      const s = 1 - frac * 0.15;
      const o = 1 - frac * 0.5;
      const b = frac * 4;
      el.style.transform = 'scale(' + s + ')';
      el.style.opacity = o;
      el.style.filter = 'blur(' + b + 'px)';
      el.style.zIndex = 10;
    } else if (i === idx + 1) {
      const s = 0.85 + frac * 0.15;
      const o = 0.5 + frac * 0.5;
      const b = 4 - frac * 4;
      el.style.transform = 'scale(' + s + ')';
      el.style.opacity = o;
      el.style.filter = 'blur(' + b + 'px)';
      el.style.zIndex = 9;
    } else {
      el.style.opacity = '0';
      el.style.zIndex = '0';
    }
  });

  dots2.forEach((d, i) => {
    d.classList.toggle('active', i === idx || (i === idx + 1 && frac > 0.5));
  });

  ticking2 = false;
}

window.addEventListener('scroll', function() {
  if (!ticking2) {
    requestAnimationFrame(updateGallery);
    ticking2 = true;
  }
}, { passive: true });

updateGallery();

// Hero is immediately visible'''

idx5 = content.find(old_js)
if idx5 >= 0:
    content = content[:idx5] + new_js + content[idx5 + len(old_js):]

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('Gallery replaced successfully!')
