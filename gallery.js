// Builds the "more photos" sections on a work page from images/manifest.js (window.PHOTO_MANIFEST),
// which build_photo_manifest() in build.py writes by scanning images/ -- see readme.txt.
(() => {
  const host = document.getElementById('more-photos');
  if (!host) return;
  const entry = (window.PHOTO_MANIFEST || {})[host.dataset.slug];
  if (!entry) { host.remove(); return; }
  const prefix = host.dataset.prefix || '../images/';

  const label = cat => cat.replace(/[-_]/g, ' ').replace(/\b\w/g, c => c.toUpperCase());
  const section = (files, heading) => {
    const figs = files.map(f => `<figure class="ph"><img src="${prefix}${f}" alt=""></figure>`).join('');
    const h = heading ? `<div class="wrap"><h2 class="group">${heading}</h2></div>` : '';
    return `${h}<section class="band"><div class="wrap more">${figs}</div></section>`;
  };

  const parts = [];
  if (entry.general?.length) parts.push(section(entry.general));
  for (const [cat, files] of Object.entries(entry.categories || {})) {
    if (files.length) parts.push(section(files, label(cat)));
  }
  host.outerHTML = parts.join('\n');
})();
