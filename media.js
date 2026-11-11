// Photos on work / writings / workshops pages.
// 1. Click a photo to see it large; click anywhere to close. Only photos that would get bigger open.
// 2. <div class="gallery erode"> plays its photos as one sequence, each step moshing into the next
//    (add data-mode="fade" to that div for a plain cross-fade instead).
(() => {
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- erosion sequences ---------- */
  document.querySelectorAll('.gallery.erode').forEach(gal => {
    const imgs = [...gal.querySelectorAll('img')];
    if (imgs.length < 2 || reduce) return;          // reduced motion: keep the plain photo grid
    const mode = gal.dataset.mode === 'fade' ? 'fade' : 'mosh';
    const first = imgs[0];
    const W = 720, H = Math.round(W * (first.getAttribute('height') / first.getAttribute('width') || 0.75));

    const box = document.createElement('figure');
    box.className = 'erode-player';
    box.style.aspectRatio = `${W}/${H}`;
    const cv = document.createElement('canvas');
    cv.width = W; cv.height = H;
    cv.setAttribute('role', 'img');
    cv.setAttribute('aria-label', `sequence of ${imgs.length} photos`);
    const dots = document.createElement('div');
    dots.className = 'erode-dots';
    box.append(cv, dots);
    gal.after(box);
    gal.hidden = true;                               // the photos stay in the page for the large view

    const ctx = cv.getContext('2d');
    const frames = [];                               // each photo drawn once at the player's size
    let idx = 0, timer = null, raf = null, visible = false;

    const dotEls = imgs.map((_, i) => {
      const b = document.createElement('button');
      b.type = 'button';
      b.setAttribute('aria-label', `photo ${i + 1} of ${imgs.length}`);
      b.addEventListener('click', e => { e.stopPropagation(); go(i, true); });
      dots.append(b);
      return b;
    });
    const mark = () => dotEls.forEach((b, i) => b.classList.toggle('on', i === idx));

    const toCanvas = img => {
      const c = document.createElement('canvas'); c.width = W; c.height = H;
      const g = c.getContext('2d'), r = Math.max(W / img.naturalWidth, H / img.naturalHeight);
      const w = img.naturalWidth * r, h = img.naturalHeight * r;
      g.drawImage(img, (W - w) / 2, (H - h) / 2, w, h);
      return c;
    };
    const ready = img => img.complete && img.naturalWidth ? Promise.resolve() :
      new Promise(res => { img.loading = 'eager'; img.addEventListener('load', res, { once: true }); img.addEventListener('error', res, { once: true }); });

    // one transition from frame a to frame b
    const transition = (a, b, done) => {
      cancelAnimationFrame(raf);
      const T = mode === 'fade' ? 900 : 1500, t0 = performance.now(), B = 16;
      // a slow "motion field": each block row/column drifts a little, like broken motion vectors
      const vx = Array.from({ length: Math.ceil(H / B) }, () => (Math.random() - .5) * 18);
      const vy = Array.from({ length: Math.ceil(W / B) }, () => (Math.random() - .5) * 10);
      const step = now => {
        const p = Math.min(1, (now - t0) / T);
        if (mode === 'fade') {
          ctx.globalAlpha = 1; ctx.drawImage(a, 0, 0);
          ctx.globalAlpha = p; ctx.drawImage(b, 0, 0); ctx.globalAlpha = 1;
        } else {
          const n = 40 + Math.floor(p * 260);
          for (let k = 0; k < n; k++) {
            const bx = Math.floor(Math.random() * W / B) * B, by = Math.floor(Math.random() * H / B) * B;
            const dx = vx[by / B | 0] * (1 - p), dy = vy[bx / B | 0] * (1 - p);
            if (Math.random() < .35 + p * .6) {
              // a block of the new photo arrives, slightly displaced
              ctx.drawImage(b, bx, by, B, B, bx + dx, by + dy, B, B);
            } else {
              // the old picture smears along the motion field
              ctx.drawImage(cv, bx, by, B * 2, B, bx + dx * 1.6, by + dy * 1.6, B * 2, B);
            }
          }
        }
        if (p < 1) raf = requestAnimationFrame(step);
        else { ctx.drawImage(b, 0, 0); done && done(); }
      };
      raf = requestAnimationFrame(step);
    };

    const schedule = () => {
      clearTimeout(timer);
      if (!visible) return;
      timer = setTimeout(() => go((idx + 1) % frames.length), idx === frames.length - 1 ? 2600 : 1500);
    };
    const go = (i, user) => {
      if (!frames.length || i === idx) return;
      const from = frames[idx]; idx = i; mark();
      clearTimeout(timer);
      transition(from, frames[idx], schedule);
    };

    Promise.all(imgs.map(ready)).then(() => {
      imgs.forEach(img => frames.push(toCanvas(img)));
      ctx.drawImage(frames[0], 0, 0); mark();
      new IntersectionObserver(es => es.forEach(e => {
        visible = e.isIntersecting;
        if (visible) schedule(); else { clearTimeout(timer); }
      }), { threshold: .3 }).observe(box);
    });

  });

  /* ---------- large view: click a photo, click anywhere to close ---------- */
  // Only photos that would actually get bigger can be opened. The main photo at the top of a
  // work page and photos already shown at (nearly) full size stay as they are.
  const PAD_W = 32, PAD_H = 48;                       // space left around the large photo
  const largeWidth = img => {
    const nw = img.naturalWidth, nh = img.naturalHeight;
    if (!nw || !nh) return 0;
    const s = Math.min(1, (innerWidth - PAD_W * 2) / nw, (innerHeight - PAD_H * 2) / nh);
    return nw * s;
  };
  const canZoom = img => !img.closest('a, .doorway') && !img.classList.contains('logo') && img.getBoundingClientRect().width > 0 &&
    largeWidth(img) > img.getBoundingClientRect().width * 1.15;
  const markAll = () => document.querySelectorAll('.flow img').forEach(img => img.classList.toggle('zoomable', canZoom(img)));
  document.querySelectorAll('.flow img').forEach(img => { if (!img.complete) img.addEventListener('load', () => img.classList.toggle('zoomable', canZoom(img)), { once: true }); });
  let rt; addEventListener('resize', () => { clearTimeout(rt); rt = setTimeout(markAll, 150); });
  markAll();

  let lb = null, big = null;
  const close = () => { lb.classList.remove('on'); removeEventListener('scroll', close); };
  const openAt = img => {
    if (!lb) {
      lb = document.createElement('div');
      lb.className = 'lightbox';
      lb.innerHTML = '<img alt="">';
      document.body.append(lb);
      big = lb.querySelector('img');
      lb.addEventListener('click', close);
    }
    big.src = img.currentSrc || img.src;
    big.alt = img.alt || '';
    lb.classList.add('on');
    addEventListener('scroll', close, { passive: true });  // the page stays visible; scrolling it closes the photo
  };
  document.addEventListener('click', e => {
    const img = e.target.closest('.flow img');
    if (!img || !canZoom(img)) return;
    openAt(img);
  });
})();
