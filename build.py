"""Builds archive.html, about.html and works/*.html for Melissa's site.
Edit WORKS below and run again, or edit the generated HTML files by hand."""
import html, os, sys
ROOT = sys.argv[1] if len(sys.argv) > 1 else "/home/claude/site"
E = html.escape

# slug, title, date, year-group, categories, one-line description, size, shown at, external link, selected?
WORKS = [
 ("master-in-training", "Master in Training", "Jan 2026", "2026", "Installation, AI",
  "Translating still-life with machine interpretation and internet photo archive.", "100 × 100 × 170 cm", "", "", True),
 ("hear-how-you-look", "Hear how you look, see how you sound", "Aug 2025", "2025", "Installation · LCD, CCTV, Arduino",
  "Converting live image footage into sound and glitching repeatedly.", "400 × 60 × 300 cm", "BitRot, Copeland Gallery", "", True),
 ("home-is-a-dwelling-path", "Home is a dwelling path", "Jun 2025", "2025", "Web Art, Installation, Performance",
  "Exploring fragmented memories of home.", "200 × 200 × 150 cm", "Camberwell Degree Show; V&A; APT; Peckham Digital", "https://newart.city/show/home-is-a-dwelling-path", True),
 ("flickring-home", "Flickring Home", "May 2025", "2025", "Web Art, Installation",
  "Make a home using Flickr photo archive.", "120 × 100 × 100 cm", "The Photographers' Gallery", "https://flickring.casa", True),
 ("write-a-word-in-the-air", "Write a word in the Air", "May 2025", "2025", "Web Art, Installation",
  "Language through movements.", "", "", "", False),
 ("farewell-to-my-old-pals", "Farewell to My Old Pals", "May 2025", "2025", "Robotics, Installation · robot plotter",
  "On the rich and complex colonial history of Millbank.", "", "Millbank", "", False),
 ("my-letter-2-you", "my-letter-2-you", "Feb 2025", "2025", "Web Art, Installation",
  "Unsent web letter on unrequited love.", "", "", "", False),
 ("southwark-park-stroll", "Southwark Park Stroll", "Dec 2024 – Feb 2025", "2024", "3D Scanning, UE5, Installation",
  "Site-specific installation exploring the interconnectedness and entanglement of species.", "50 × 50 × 180 cm",
  "Southwark Park Galleries, Dilston Gallery", "", True),
 ("waves-of-perception", "Waves of Perception", "Apr 2024", "2024", "Projection, Arduino, Installation",
  "Working with the observer effect: a live projection feed on a metal water plate, with distance sensing.", "plinth 40 × 40 × 90 cm, projection 100 × 200 cm", "", "", True),
 ("noisy-echos", "Noisy Echos", "Jul 2024", "2024", "Web Art, ml5.js, p5.js",
  "Conway's Game of Life, set moving by your own messages: on the noise between what is said and what is heard.", "", "", "https://melissayunzhi.github.io/NoisyEchos/", False),
 ("microcosm-of-identity", "Microcosm of Identity", "Dec 2023 – Feb 2024", "2023", "3D Scanning, UE5, AI, Installation",
  "An exploration of what makes up one's identity, with the surrounding bacteria cultures.", "", "", "", True),
 ("escapism-walls", "Escapism Walls", "2023", "2023", "TikTok, AI, Projection", "Projection built from TikTok imagery and AI.", "", "BargeHouse, Oxo Tower, 2023", "", False),
 ("luminescent-reverie", "Luminescent Reverie", "2023", "2023", "", "Shown at the launch of Wanted Zine.", "", "Launch Event Exhibition, \u201cWanted Zine\u201d, Greatorex Street Gallery, 2023", "", False),
 ("phreaking-collective", "Phreaking Collective", "Since Aug 2025", "Elsewhere", "Curation",
  "Co-founder, artist lead and co-curator of a collective of emerging computational artists.", "", "BitRot, Copeland Gallery; Can We Start Again?", "", False),
 ("cranberry-lemonade", "cranberry*lemonade", "Since Jul 2024", "Elsewhere", "Workshops, HTML",
  "Co-founder of a collective running workshops in HTML, CSS and JavaScript.", "", "SET Social; the Good Rice; Copeland Gallery", "", False),
 ("freelance", "freelance", "", "Elsewhere", "Design, Video",
  "Posters, handouts, reels and video for collectives, galleries and UAL.", "", "", "", False),
]
NAV = [("selected", "index.html"), ("archive", "archive.html"), ("workshops", "workshops.html"), ("writings", "writings.html"),
       ("about", "about.html"), ("cv", "works/cv.html")]
SOCIAL = [("instagram", "https://www.instagram.com/melissayunzhi/"), ("are.na", "https://www.are.na/melissayunzhi-li/channels"),
          ("linkedin", "https://www.linkedin.com/in/yunzhi-li-593503200/")]

def head(title, css):
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{E(title)}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=IBM+Plex+Sans+Condensed:ital,wght@0,400;0,500;1,400&family=IBM+Plex+Mono&display=swap">
<link rel="stylesheet" href="{css}">
</head>
<body>
"""

EMAIL = "melissayunzhi@gmail.com"
ICONS = {
 "instagram": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 8h3l2-2.5h6L17 8h3v11H4z"/><circle cx="12" cy="13.5" r="3.5"/></svg>',
 "are.na": '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="4" y="4" width="7" height="7"/><rect x="13" y="4" width="7" height="7"/><rect x="4" y="13" width="7" height="7"/><rect x="13" y="13" width="7" height="7"/></svg>',
 "linkedin": '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3.5" y="8" width="17" height="11.5"/><path d="M9 8V5.5h6V8M3.5 13h17"/></svg>',
}
MAIL_SVG = '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3.5" y="6" width="17" height="12"/><path d="M3.5 6.5 12 13l8.5-6.5"/></svg>'

ICON_FILE = {"instagram": "instagram", "are.na": "are-na", "linkedin": "linkedin"}
def reach(prefix=""):
    # official logos: drop instagram.png, are-na.png, linkedin.png into images/icons/ and they replace the drawn icons
    icons = [f'<a class="icon" href="{h}" aria-label="{n}" title="{n}" data-icon="{prefix}images/icons/{ICON_FILE[n]}.png">{ICONS[n]}</a>' for n, h in SOCIAL]
    return " ".join(icons) + f' <a class="mail" href="mailto:{EMAIL}">{MAIL_SVG}<span>email me</span></a>'

def nav(prefix, current, social=True):
    items = [f'<a href="{prefix}{h}"{" aria-current=\"page\"" if n == current else ""}>{n}</a>' for n, h in NAV]
    return '<nav class="site">' + "\n    ".join(items) + (" " + reach(prefix) if social else "") + "</nav>"

BANDS = ["b-pages", "b-sky", "b-terra", "b-bark"]

def footer(prefix, links):
    items = " ".join(f'<a href="{prefix}{h}">{n}</a>' if not h.startswith("#") else f'<a href="{h}">{n}</a>' for n, h in links)
    return f"""<footer class="masthead"><div class="wrap">
  <h2>computational art, tattoo, curation · london</h2>
  <h1><a href="{prefix}index.html">Yunzhi / Melissa Li</a></h1>
  <nav class="site">{items}</nav>
  <nav class="site reach">{reach(prefix)}</nav>
  <p class="addr">{EMAIL}</p>
</div></footer>
"""

def masthead(kicker, prefix, current, tag="header"):
    return f"""<{tag} class="masthead"><div class="wrap">
  <h2>{kicker}</h2>
  <h1><a href="{prefix}index.html">Yunzhi / Melissa Li</a></h1>
  {nav(prefix, current)}
</div></{tag}>
"""

MISSING_JS = """<script>
// official platform logos replace the drawn icons when their files exist
document.querySelectorAll('a.icon[data-icon]').forEach(a => {
  const img = new Image();
  img.onload = () => { const g = document.createElement('span'); g.className = 'glyph'; g.style.setProperty('--g', `url("${a.dataset.icon}")`); a.replaceChildren(g); };
  img.src = a.dataset.icon;
});
// always open a page at the top
if ('scrollRestoration' in history) history.scrollRestoration = 'manual';
if (!location.hash) { scrollTo(0, 0); addEventListener('load', () => scrollTo(0, 0), { once: true }); }
document.querySelectorAll('[data-src] img').forEach(img => {
  const box = img.parentNode;
  const mark = () => box.classList.add('missing');
  if (img.complete && !img.naturalWidth) mark(); else img.addEventListener('error', mark);
});
</script>
"""

# ---------------- tags ----------------
# Tags come from each work's categories (split on commas and "·"). Every tag gets its own page,
# e.g. installation.html, web-art.html, which most hosts serve as /installation and /web-art.
import re as _re
def tag_slug(t): return _re.sub(r"[^a-z0-9]+", "-", t.lower()).strip("-")
def tags_of(cats): return [c.strip() for c in _re.split(r"[,·]", cats) if c.strip()]
RESERVED = {"index", "archive", "about", "writings", "workshops", "site"}
def all_tags():
    counts = {}
    for w in WORKS:
        for t in tags_of(w[4]):
            k = tag_slug(t)
            if k in RESERVED: k = k + "-tag"
            name, n = counts.get(k, (t, 0))
            counts[k] = (name, n + 1)
    return sorted(counts.items(), key=lambda kv: (-kv[1][1], kv[1][0].lower()))
def tag_href(t, prefix=""):
    k = tag_slug(t)
    return f"{prefix}{k + '-tag' if k in RESERVED else k}.html"

# ---------------- archive (and one page per tag) ----------------
def archive(tag=None):
    tags = all_tags()
    works = [w for w in WORKS if tag is None or any(tag_slug(t) == tag or tag_slug(t) + "-tag" == tag for t in tags_of(w[4]))]
    tag_name = dict((k, v[0]) for k, v in tags).get(tag, "")
    title = f"{tag_name} · Archive · Yunzhi / Melissa Li" if tag else "Archive · Yunzhi / Melissa Li"
    kicker = f"archive, {E(tag_name.lower())}" if tag else "archive, every work"
    out = [head(title, "site.css"), masthead(kicker, "", "archive")]
    chips = [f'<a class="chip{" on" if tag is None else ""}" href="archive.html"{" aria-current=\"page\"" if tag is None else ""}>all <span>{len(WORKS)}</span></a>']
    for k, (name, n) in tags:
        on = k == tag
        chips.append(f'<a class="chip{" on" if on else ""}" href="{k}.html"{" aria-current=\"page\"" if on else ""}>{E(name)} <span>{n}</span></a>')
    out.append('<nav class="tags wrap" aria-label="Sort by tag">' + " ".join(chips) + "</nav>\n")
    out.append('<p class="legend wrap" style="margin-bottom:28px"><span class="sel" aria-hidden="true"></span>also a room in the selected works</p>\n<main>\n')
    groups = []
    for w in works:
        if not groups or groups[-1][0] != w[3]: groups.append((w[3], []))
        groups[-1][1].append(w)
    for gi, (g, items) in enumerate(groups):
        out.append(f'<section class="band"><div class="wrap">\n<h3 class="year">{E(g)}</h3>\n<ul class="list">\n')
        for slug, t, date, _, cats, desc, *_rest, sel in items:
            mark = '<span class="sel" title="selected work"></span>' if sel else ""
            tl = ", ".join(f'<a href="{tag_href(c)}">{E(c)}</a>' for c in tags_of(cats))
            out.append(f'  <li data-slug="{slug}"><span class="when">{E(date)}</span>'
                       f'<a class="t" href="works/{slug}.html">{mark}{E(t)}</a>'
                       f'<span class="d">{E(desc)}</span><span class="c">{tl}</span></li>\n')
        out.append("</ul>\n</div></section>\n")
    out.append("</main>\n")
    out.append(footer("", [("selected", "index.html"), ("workshops", "workshops.html"), ("writings", "writings.html"), ("about", "about.html"), ("top", "#")]))
    out.append(ARCHIVE_JS)
    return "".join(out)

ARCHIVE_JS = """<div class="peek" aria-hidden="true"><img alt=""></div>
<script>
// official platform logos replace the drawn icons when their files exist
document.querySelectorAll('a.icon[data-icon]').forEach(a => {
  const img = new Image();
  img.onload = () => { const g = document.createElement('span'); g.className = 'glyph'; g.style.setProperty('--g', `url("${a.dataset.icon}")`); a.replaceChildren(g); };
  img.src = a.dataset.icon;
});
// always open a page at the top
if ('scrollRestoration' in history) history.scrollRestoration = 'manual';
if (!location.hash) { scrollTo(0, 0); addEventListener('load', () => scrollTo(0, 0), { once: true }); }
// hover a title: a small photo appears beside the cursor (images/<slug>.jpg; hidden if missing)
const peek = document.querySelector('.peek'), pimg = peek.querySelector('img');
const fine = matchMedia('(hover: hover)').matches;
document.querySelectorAll('.list li').forEach(li => {
  const a = li.querySelector('.t');
  a.addEventListener('pointerenter', () => {
    if (!fine) return;
    pimg.onload = () => peek.classList.add('on');
    pimg.onerror = () => peek.classList.remove('on');
    pimg.src = 'images/' + li.dataset.slug + '.jpg';
  });
  a.addEventListener('pointermove', e => {
    const w = peek.offsetWidth, h = peek.offsetHeight;
    const x = Math.min(innerWidth - w - 12, e.clientX + 24), y = Math.min(innerHeight - h - 12, Math.max(12, e.clientY - h / 2));
    peek.style.left = x + 'px'; peek.style.top = y + 'px';
  });
  a.addEventListener('pointerleave', () => peek.classList.remove('on'));
});
</script>
</body>
</html>
"""

# ---------------- extra detail per work (from the Cargo pages) ----------------
# body: paragraphs for the page. materials / shown / links add to the details list.
# video: paste a Vimeo link, e.g. "https://vimeo.com/123456789", and the page embeds it.
EXTRA = {
 "master-in-training": dict(
   body=["A four-screen still life that keeps translating itself. A staged scene is described by an OpenAI vision model; the description becomes a new image through generative AI, and that image is passed through image-to-image processing again and again, so the drift accumulates. The last screen searches online for a real photograph that matches.",
         "It begins from a habit of trusting cloud storage with memory, and asks what happens when remembering becomes retrieval, and mastery moves from the Renaissance master to training datasets and models."],
   materials="LCD screens, steel tubing, still life set-up",
   shown=["CVPR 2026, shortlisted", "ANNEX by the Koppel Project, <i>Does Cloud Compute (ever) Precipitate?</i>, Phreaking Collective, Aug 2025"],
   links=[("CVPR 2026 project page", "https://thecvf-art.com/project.php?year=2026&artist=yunzhi-li&id=1029")], video=""),
 "flickring-home": dict(
   body=["A virtual home built from the Flickr archive. Photos tagged \u201chome\u201d, uploaded between 2004 and 2015, become the textures of a generic 3D room and change as you move through it. Visitors can type their own tags to furnish the space.",
         "The work looks at how old personal photographs resurface or disappear, and which moments become the background of a personal history."],
   materials="Interactive web art", shown=["<i>Flickr Foundation x Computational Arts Takeover</i>, The Photographers' Gallery, 9 May 2025"],
   links=[("flickring.casa", "https://flickring.casa/")], video=""),
 "southwark-park-stroll": dict(
   body=["<i>Microcosm of Identity</i>, grown into a site-specific installation for Southwark Park Galleries. Drawing on Donna Haraway's <i>Tentacular Thinking</i>, it traces the ties between people, their surroundings and the unseen ecosystems around them.",
         "Bacteria were cultivated from soil, leaves and the surfaces people touch in the gallery and park, grown in petri dishes, scanned with PolyCam, and laid out as a landscape to walk through in Unreal Engine."],
   materials="Petri dishes, bacterial cultures, PolyCam, Unreal Engine", shown=["Southwark Park Galleries, Dilston Gallery, 8\u20139 Feb 2025"], links=[], video=""),
 "waves-of-perception": dict(
   body=["Built around the double-slit experiment. A live webcam captures viewers and projects their moving image onto a metal plate. As people come closer, an ultrasonic sensor sets the plate vibrating through contact speakers, and the rippling reflections spill across the gallery walls."],
   materials="Metal plate, contact speakers, ultrasonic sensor, wooden plinth, projector",
   shown=["Camberwell Drawing and Computational Arts Year 2 Group Show, Copeland Gallery, Apr 2024", "<i>Liminal Entities</i>, Millbank Podium, May 2024", "<i>Water, Oil, Honey</i>, The Crypt Gallery, May 2024"],
   links=[], video=""),
 "microcosm-of-identity": dict(
   body=["It began with fallen hair collected from a shared bathroom, and a question: what makes up one's identity? The hair was cultivated in petri dishes and the bacterial growth documented over a month.",
         "The mature cultures were scanned with PolyCam into forms that read like foreign landscapes, then navigated in Unreal Engine and morphed with AI."],
   materials="Fallen hair, bacterial cultures, petri dishes, PolyCam, Unreal Engine, AI",
   shown=["<i>Ascertain</i>, Espacio Art Gallery, 18\u201321 Jul", "<i>Sensations</i>, Something 2 Chew On, the Bath House, 10 Nov 2024", "<i>InterAct</i>, Cornerstone Studios / Hypha Studios, Feb\u2013Mar 2025"],
   links=[("InterAct exhibition", "https://hyphastudios.com/interact-exhibition/")], video="", credit="Photos: Carlo Zambon"),
}

# exhibition history from the CV (overrides "shown at")
CV_SHOWN = {
 "master-in-training": ["CVPR 2026, shortlisted", "<i>Does Cloud Compute (ever) Precipitate?</i>, ANNEX by the Koppel Project, Phreaking Collective, London, 2026"],
 "home-is-a-dwelling-path": ["<i>Echoes and Returns</i>, On The Fringe NYC Gallery, New York, 2026", "Peckham Digital 2025, Copeland Gallery", "Digital Design Weekend 2025, Victoria and Albert Museum",
   "<i>APT: Threshold</i>, APT, 2025", "Cheeky London Launchpad, Tradestar Islington, 2025", "Developed on the Hybrid-Reality-Lab2 residency, Six Minutes Past Nine, Mar\u2013May 2025, as a New Art City piece"],
 "hear-how-you-look": ["<i>BitRot</i>, Copeland Gallery, 2025"],
 "flickring-home": ["<i>Comp Arts x Flickr Takeover</i>, The Photographers' Gallery, 9 May 2025"],
 "farewell-to-my-old-pals": ["<i>Folder_02</i>, Millbank Tower, 2025"],
 "my-letter-2-you": ["<i>Love Shack</i>, hARTsLane, 2025"],
 "southwark-park-stroll": ["<i>Momentarily Here</i>, Dilston Gallery / Southwark Park Galleries, 8\u20139 Feb 2025"],
 "microcosm-of-identity": ["<i>rehearsing embodied ecologies</i>, Fringe Arts Bath, 2025", "<i>InterAct</i>, Cornerstone Studios / Hypha Studios, Feb\u2013Mar 2025",
   "<i>Senstations</i>, Something 2 Chew On, the Bath House, 10 Nov 2024", "<i>Ascertain</i>, Espacio Art Gallery, 2024"],
 "noisy-echos": ["\u201cActually\u201d Attainable Art Fair, ST.Art Gallery, 2024"],
 "waves-of-perception": ["<i>Water, Oil, Honey</i>, The Crypt Gallery, May 2024", "<i>Liminal Entities</i>, Millbank Podium, May 2024", "Fine Art: Drawing and Fine Art: Computational Arts, Copeland Gallery, Apr 2024"],
}
for _k, _v in CV_SHOWN.items(): EXTRA.setdefault(_k, {})["shown"] = _v


# ---------------- page texts (from the Cargo pages, the CV and the Our Culture interview) ----------------
def _set(slug, **kw): EXTRA.setdefault(slug, {}).update(kw)

_set("hear-how-you-look",
  body=["Six LCD screens hang on the wall, their cables falling together to a single plinth. A CCTV camera watches the room. Its live footage is converted into sound, and the translation runs again and again, glitching a little further with every pass.",
        "Stand in front of it and you hear how you look. Stay, and you see how you sound."],
  materials="LCD screens, CCTV camera, Arduino, speakers, plinth",
  shown=["<i>BitRot</i>, Copeland Gallery, 2025, co-curated with Phreaking Collective"])

_set("home-is-a-dwelling-path",
  body=["An explorative 3D world and a room that echoes its textures. Visitors play through fragmented virtual homes, stitched together from 3D-scanned objects, reconstructed buildings, personal photographs and images found in public archives, while recollections of home play along the way.",
        "The game spills into the room as a bunk bed and a ceramic bowl. After playing, visitors climb to the top bunk for <i>Pillow Talk</i>, a one-to-one conversation where they share their own home stories. Those stories feed back into the digital space, so the work is never finished: it keeps being built, lost and rebuilt, the way a sense of home is.",
        "Developed as a New Art City piece on the Hybrid-Reality-Lab2 residency with Six Minutes Past Nine."],
  materials="Interactive 3D game, bunk-bed structure, ceramic bowl, live one-to-one performance",
  links=[("Walk through it on New Art City", "https://newart.city/show/home-is-a-dwelling-path"),
         ("Our Culture: “Yunzhi Li's art is where physical memory meets digital creativity”, Tabish Khan, Nov 2025", "https://ourculturemag.com/2025/11/23/yunzhi-lis-art-is-where-physical-memory-meets-digital-creativity/")],
  shown=["<i>Echoes and Returns</i>, On The Fringe NYC Gallery, New York, 2026",
         "Digital Design Weekend 2025, Victoria and Albert Museum, with <i>Pillow Talk</i> (Eye Compute)",
         "Peckham Digital 2025, Copeland Gallery", "<i>Some kind of home</i>, Noiascape, 2025", "<i>APT: Threshold</i>, APT, 2025",
         "Cheeky London Launchpad, Tradestar Islington, 2025", "Camberwell College of Arts Degree Show, 2025"])

_set("write-a-word-in-the-air",
  body=["Writing, lifted off the page. Visitors draw words in the air with a finger, and each gesture leaves a trace that keeps moving after the hand has gone.",
        "The work draws on Chinese calligraphy and on dyslexic ways of thinking, both of which treat a mark as more than a carrier of fixed meaning. What stays is the rhythm of writing: the body in the letter."],
  materials="Interactive web art, gesture tracking",
  shown=["<i>The Linking Line</i>, hARTslane, 8 May 2025, as part of José Abad Lorente's <i>The Linking Line</i>"])

_set("farewell-to-my-old-pals",
  body=["Made for Millbank, where convicted prisoners were once held before transportation to Australia. A small robot car crosses a canvas laid on the floor, a pen trailing behind it.",
        "Its route is written by “Botany Bay”, a ballad sung by convicts in the penal colony. Each word becomes a movement: a steady step, a gentle turn, a pause on farewell, on captains and convicts, on wings, on Botany Bay. Over the days the ink gathers into looping ribbons, the journeys out of Millbank, and the shifting balance of power the site still holds."],
  materials="Robot plotter car, canvas, ink",
  shown=["<i>Folder_02</i>, Millbank Tower, 8–9 May 2025"])

_set("my-letter-2-you",
  body=["An unsent web letter, on love and unrequited feeling. Written, addressed, and kept: a message that lives online and never arrives."],
  materials="Interactive web art",
  links=[("Read the letter", "https://my-letter-2-you.glitch.me/"), ("GitHub Pages version", "https://melissayunzhi.github.io/my-letter-to-you/")],
  shown=["<i>Love Shack</i>, hARTsLane, 14–17 Feb 2025"])

_set("noisy-echos",
  body=["Conway's Game of Life, set in motion by the body. Visitors write a message, a drawing or a word with their own movement, tracked by ml5's bodyPose model, and then let the cells take over.",
        "The work grows out of everyday conversation, and the way a message never arrives exactly as it was sent: the “noise” in Shannon and Weaver's model of communication. Only the next three generations can be saved and shared to an Are.na channel. After that, the message belongs to the noise."],
  materials="ml5.js bodyPose, p5.js, web",
  links=[("Try Noisy Echos", "https://melissayunzhi.github.io/NoisyEchos/"), ("Are.na", "https://www.are.na/melissayunzhi-li/channels")],
  shown=["“Actually” Attainable Art Fair, ST.ART Gallery, London, 25–28 Jul 2024"])

_set("escapism-walls",
  body=["An early projection work, built from TikTok imagery and AI, on the walls we scroll into when we want to be somewhere else."],
  materials="TikTok footage, AI, projection", shown=["BargeHouse, Oxo Tower, 2023"])

_set("luminescent-reverie",
  body=["Shown at the launch exhibition of <i>Wanted Zine</i>."],
  shown=["Launch Event Exhibition, “Wanted Zine”, Greatorex Street Gallery, 2023"])

_set("phreaking-collective",
  body=["A group of emerging computational artists, co-founded in 2025. Phreaking organises self-initiated exhibitions, film nights, open projector evenings and talks with guest speakers.",
        "As artist lead and co-curator, Melissa has taken exhibitions from first idea through install and deinstall: <i>BitRot</i> at Copeland Gallery, <i>Does Cloud Compute (ever) Precipitate?</i> at ANNEX by the Koppel Project, and <i>Can We Start Again?</i> at the old Archbishop Tenison's School site near The Oval, a show threading digital ecology, technological acceleration and the history of the site."],
  materials="Curation, production, visual identity",
  shown=["<i>BitRot</i>, Copeland Gallery, 2025", "<i>Does Cloud Compute (ever) Precipitate?</i>, ANNEX by the Koppel Project, 2026", "<i>Can We Start Again?</i>, old Archbishop Tenison's School, the Oval"],
  links=[("@phreaking_collective", "https://www.instagram.com/phreaking_collective/")])

_set("cranberry-lemonade",
  body=["A collective co-founded by Melissa that runs workshops in HTML, CSS and JavaScript. Each session takes a different theme, and the aim stays the same: take the mystery out of making for the web, so people can put their own stories online.",
        "Workshops have run at SET Social, the Good Rice and Copeland Gallery since July 2024."],
  materials="Workshops in HTML, CSS, JavaScript",
  links=[("@cranberry_lemonade", "https://www.instagram.com/cranberry_lemonade/"), ("All workshops and talks", "../workshops.html")])

_set("freelance",
  body=["Design, video and social content for collectives, galleries and the university.",
        "<ul class=\"plain\"><li>Open Projector poster, Phreaking Collective</li><li>Film night handouts, Phreaking Collective</li><li>Workshop poster, Cranberry Lemonade</li><li>Berlin Transmediale 2024, video</li><li><i>Voices of UAL</i>: a video exploration of student identity</li><li>UAL Inflatable Workshop, promotion reel</li><li>Viral TikTok videos, in collaboration with PhotoRoom</li><li>LDF Peckham Levels exhibition</li></ul>",
        "For commissions, <a href=\"mailto:melissayunzhi@gmail.com\">email me</a>."],
  materials="Graphic design, video, social media")

def vimeo_embed(url, title):
    import re
    m = re.search(r"vimeo\.com/(?:video/)?(\d+)", url or "")
    if not m: return ""
    vid = m.group(1)
    return f"""  <section class="band"><div class="wrap">
    <div class="video"><iframe src="https://player.vimeo.com/video/{vid}?dnt=1&amp;title=0&amp;byline=0&amp;portrait=0" title="{E(title)}, video" allow="autoplay; fullscreen; picture-in-picture" loading="lazy"></iframe></div>
    <p class="vlink"><a href="{E(url)}">watch on Vimeo</a></p>
  </div></section>
"""

# ---------------- work page ----------------
ALT = {
 "master-in-training": "A scaffold frame of monitors around a still life of fruit and flowers on a red cloth.",
 "hear-how-you-look": "Six screens and a CCTV camera on a gallery wall, cables falling to a white plinth.",
 "home-is-a-dwelling-path": "A 3D scene of scanned doorways, a bowl of mapo tofu and floating rocks along a dark path.",
 "southwark-park-stroll": "A visitor with a game controller at a screen, petri dishes on the table beside them.",
}

def work(i, seq):
    slug, t, date, _, cats, desc, size, shown, link, sel = seq[i]
    prev, nxt = seq[i - 1], seq[(i + 1) % len(seq)]
    x = EXTRA.get(slug, {})
    shown_list = x.get("shown") or [E(v.strip()) for v in shown.split(";") if v.strip()]
    links = x.get("links") or ([(link.replace("https://", ""), link)] if link else [])
    cat_links = ", ".join(f'<a href="{tag_href(c, "../")}">{E(c)}</a>' for c in tags_of(cats))
    facts = [("Date", E(date)), ("Tags", cat_links), ("Materials", E(x.get("materials", ""))), ("Size", E(size)),
             ("Shown at", "<br>".join(shown_list)),
             ("Links", "<br>".join(f'<a href="{u}">{E(n)}</a>' for n, u in links)),
             ("Credit", E(x.get("credit", "")))]
    body = "\n      ".join(para if para.startswith("<ul") else f"<p>{para}</p>" for para in x.get("body", [])) or '<p class="todo">Write about this work here.</p>'
    video = vimeo_embed(x.get("video"), t)
    dl = "\n".join(f"      <dt>{k}</dt><dd>{v}</dd>" for k, v in facts if v)
    back = f'../index.html#{slug}' if sel else "../archive.html"
    return head(f"{t} · Yunzhi / Melissa Li", "../site.css") + f"""<header class="top"><div class="wrap bar">
  <a class="name" href="../index.html">Yunzhi / Melissa Li</a>
  {nav("../", "", social=False)}
</div></header>

<main>
  <div class="wrap">
    <div class="work-head">
      <p class="kicker">{E(date)}{" · selected work" if sel else ""}</p>
      <h1>{E(t)}</h1>
      {f'<p class="lede">{E(desc)}</p>' if desc else ''}
    </div>

    <!-- MAIN PHOTO: put the file at images/{slug}.jpg (or change the src). -->
    <div class="doorway">
      <div class="frame" data-src="images/{slug}.jpg">
        <span class="wall">{E(size or date)}</span>
        <img src="../images/{slug}.jpg" alt="{E(ALT.get(slug, t))}">
      </div>
    </div>
  </div>

  <section class="band"><div class="wrap body">
    <div class="text">
      {body}
    </div>
    <dl class="facts">
{dl}
    </dl>
  </div></section>

  <!-- VIDEO: add a Vimeo link for this work in EXTRA (build.py), or paste the <iframe> here. -->
{video}
  <!-- MORE PHOTOS: copy a <figure> per image. -->
  <section class="band"><div class="wrap more">
    <figure class="ph" data-src="images/{slug}-2.jpg"><img src="../images/{slug}-2.jpg" alt=""></figure>
    <figure class="ph" data-src="images/{slug}-3.jpg"><img src="../images/{slug}-3.jpg" alt=""></figure>
  </div></section>

  <section class="band"><div class="wrap">
    <nav class="pager" aria-label="More works">
      <a class="prev" href="{prev[0]}.html"><small>previous</small>{E(prev[1])}</a>
      <a class="next" href="{nxt[0]}.html"><small>next</small>{E(nxt[1])}</a>
    </nav>
    <p class="center"><a class="door" href="{back}">⇠ back to {"the rooms" if sel else "the archive"}</a></p>
  </div></section>
</main>

""" + footer("../", [("selected", "index.html"), ("archive", "archive.html"), ("writings", "writings.html"), ("about", "about.html")]) + MISSING_JS + "</body>\n</html>\n"

def simple(path_prefix, title, kicker, body_html, current):
    return head(f"{title} · Yunzhi / Melissa Li", f"{path_prefix}site.css") + masthead(kicker, path_prefix, current) + f"""<main class="band"><div class="wrap">
{body_html}
</div></main>
""" + footer(path_prefix, [("selected", "index.html"), ("archive", "archive.html"), ("workshops", "workshops.html"), ("writings", "writings.html")]) + MISSING_JS + "</body>\n</html>\n"

ABOUT = """  <div class="body" style="margin-top:8px">
    <div class="text">
      <p class="lede" style="margin:0 0 18px">A computational artist, born in Chengdu, raised partly in Tbilisi, based in South East London.</p>
      <p>Melissa makes interactive installations, web-based experiments and immersive 3D environments that ask how images, code and the people who meet them shape identity, memory and a sense of place. The aim, again and again, is to make intangible experience visible.</p>
      <p>Her material comes from public image archives, 3D scans of everyday objects and recorded personal stories, layered into rooms that are half physical, half digital. Furniture and screens become surfaces where virtual textures seem to settle onto real things, and visitors are asked to notice how their own histories and digital traces connect. Recurring threads: home, displacement, memory, cultural hybridity and ecology.</p>
      <p>Her work has been shown at the Victoria and Albert Museum, The Photographers' Gallery, Hypha Studios, Copeland Gallery, Peckham Digital and On The Fringe NYC, and was shortlisted for CVPR 2026.</p>
      <p>She co-founded <a href="works/phreaking-collective.html">Phreaking Collective</a>, a group of emerging computational artists who make their own exhibitions, events and talks, and <a href="works/cranberry-lemonade.html">Cranberry Lemonade</a>, which runs workshops in HTML, CSS and JavaScript so more people can tell their own stories online. She teaches on BA Fine Art: Computational Arts at Camberwell College of Arts, where she graduated with First Class Honours, works as a Research Assistant with UAL's AI Research Group, and is a trained tattoo artist.</p>
      <p>Next: sensor networks, community-sourced data, and site-responsive installations that fold personal histories into immersive space.</p>
      <dl class="facts" style="margin-top:24px">
        <dt>Contact</dt><dd><a href="mailto:melissayunzhi@gmail.com">melissayunzhi@gmail.com</a></dd>
        <dt>Elsewhere</dt><dd><a href="https://startgallery.co.uk/yunzhi-li">Start Gallery</a><br><a href="https://wedotart.com/melissayunzhi">we[dot]art</a><br><a href="https://ourculturemag.com/2025/11/23/yunzhi-lis-art-is-where-physical-memory-meets-digital-creativity/">Our Culture interview, Nov 2025</a></dd>
        <dt>More</dt><dd><a href="works/cv.html">CV</a> \u00b7 <a href="workshops.html">workshops and talks</a> \u00b7 <a href="writings.html">writings</a></dd>
      </dl>
    </div>
    <div class="doorway" style="margin:0"><div class="frame" data-src="images/about.jpg" style="aspect-ratio:4/5"><img src="images/about.jpg" alt="Melissa Li"></div></div>
  </div>"""

def cv_rows(rows):
    return "\n".join(f'    <div class="cv-row"><span class="when">{d}</span><div>{body}</div></div>' for d, body in rows)
def w(slug, title): return f'<a href="{slug}.html"><i>{title}</i></a>'

CV = f"""  <div class="work-head"><p class="kicker">2026</p><h1>CV</h1>
    <!-- put cv.pdf in the site folder and this link appears -->
    <p class="lede-intro" id="cvpdf" style="margin-top:14px" hidden><a href="../cv.pdf">Download as PDF</a></p>
    <script>fetch('../cv.pdf', {{ method: 'HEAD' }}).then(r => {{ if (r.ok) document.getElementById('cvpdf').hidden = false; }}).catch(() => {{}});</script></div>

  <section class="cv-block"><h2>Residencies</h2>
{cv_rows([
  ("04/2025 \u2013 06/2025", "<b>EcoFutures Digital Residency</b>, Videotage HK, online<br><span>A six-week programme on the intersection of digital media, environmental consciousness and emotional expression in arts and culture.</span>"),
  ("03/2025 \u2013 05/2025", "<b>Hybrid-Reality-Lab2</b>, Six Minutes Past Nine, online<br><span>Development of the New Art City piece " + w("home-is-a-dwelling-path", "Home is a dwelling path") + ".</span>"),
])}
  </section>

  <section class="cv-block"><h2>Group exhibitions</h2>
{cv_rows([
  ("2026", w("home-is-a-dwelling-path", "Home is a dwelling path") + ", <i>Echoes and Returns</i>, On The Fringe NYC Gallery, New York"),
  ("", w("master-in-training", "Master in Training") + ", <i>Does Cloud Compute (ever) Precipitate?</i>, London"),
  ("2025", w("home-is-a-dwelling-path", "Home is a dwelling path") + ", Peckham Digital 2025, Copeland Gallery"),
  ("", w("home-is-a-dwelling-path", "Home is a dwelling path") + ", Digital Design Weekend 2025, Victoria and Albert Museum"),
  ("", w("home-is-a-dwelling-path", "Home is a dwelling path") + ", <i>APT: Threshold</i>, APT"),
  ("", w("home-is-a-dwelling-path", "Home is a dwelling path") + ", Cheeky London Launchpad, Tradestar Islington"),
  ("", w("hear-how-you-look", "Hear how you look, see how you sound") + ", <i>BitRot</i>, Copeland Gallery"),
  ("", w("microcosm-of-identity", "Microcosm of Identity") + ", <i>rehearsing embodied ecologies</i>, Fringe Arts Bath"),
  ("", w("flickring-home", "Flickring Home") + ", <i>Comp Arts x Flickr Takeover</i>, The Photographers' Gallery"),
  ("", w("farewell-to-my-old-pals", "Farewell to my old pals") + ", <i>Folder_02</i>, Millbank Tower"),
  ("", w("my-letter-2-you", "my-letter-2-you") + ", <i>Love Shack</i>, hARTsLane"),
  ("", w("southwark-park-stroll", "Southwark Park Stroll") + ", <i>Momentarily Here</i>, Dilston Gallery / Southwark Park Galleries"),
  ("", w("microcosm-of-identity", "Microcosm of Identity") + ", <i>InterAct</i>, Cornerstone Studios / Hypha Studios"),
  ("2024", w("microcosm-of-identity", "Microcosm of Identity") + ", <i>Senstations</i>, Something 2 Chew On, the Bath House"),
  ("", w("noisy-echos", "Noisy Echos") + ", \u201cActually\u201d Attainable Art Fair, ST.Art Gallery"),
  ("", w("microcosm-of-identity", "Microcosm of Identity") + ", <i>Ascertain</i>, Espacio Art Gallery"),
  ("", w("waves-of-perception", "Waves of Perception") + ", <i>Water, Oil, Honey</i>, The Crypt Gallery"),
  ("", w("waves-of-perception", "Waves of Perception") + ", <i>Liminal Entities</i>, Millbank Podium"),
  ("", w("waves-of-perception", "Waves of Perception") + ", Fine Art: Drawing and Fine Art: Computational Arts, Copeland Gallery"),
  ("2023", w("luminescent-reverie", "Luminescent Reverie") + ", Launch Event Exhibition, \u201cWanted Zine\u201d, Greatorex Street Gallery"),
  ("", w("escapism-walls", "Escapism Walls") + ", BargeHouse, Oxo Tower"),
])}
  </section>

  <section class="cv-block"><h2>Talks and workshops</h2>
{cv_rows([
  ("10/2025 \u2013 now", "<b>Associate Lecturer</b>, London<br><span>Year 1 and Year 2 unit tutor, BA Fine Art: Computational Arts, Camberwell College of Arts.</span>"),
  ("07/2024 \u2013 now", "<b>Co-host, Cranberry Lemonade workshops</b>, London<br><span>Organised and facilitated workshops on different themes of HTML, at SET Social, the Good Rice and Copeland Gallery.</span>"),
  ("07/2024, 08/2025", "<b>Co-host, HTML Energy 2024 &amp; 2025</b>, London<br><span>Workshops on making a personal web page with HTML, CSS and JavaScript, designed so each participant leaves with a page of their own.</span>"),
  ("06/2024", "<b>Presenter, The New Ideas Exhibit: Creative Tech &amp; Digital Design</b>, London<br><span>Presented the bacteria project to industry professionals and fellow creatives.</span>"),
  ("02/2024", "<b>Artist talk, BOM Immersive Arts Meet-Up</b>, Birmingham<br><span>\u201cRebuild a World with Bacteria, from Micro to Macro\u201d.</span>"),
  ("01/2024", "<b>Workshop facilitator, Enhancing Engagement Forum</b>, UAL, London<br><span>Co-led a \u201cCulture and Identity\u201d workshop with Tutu Gbadamosi: video interviews on identity and belonging, then a collage-making session for university staff.</span>"),
])}
  </section>

  <section class="cv-block"><h2>Professional experience</h2>
{cv_rows([
  ("08/2025 \u2013 now", "<b>Artist lead and curatorial work</b>, Phreaking Collective, remote / London<br><span>Co-curated and produced exhibitions such as BitRot at Copeland Gallery, from concept to install and deinstall; ran the shared inbox and scheduling; helped with budgeting, fundraising and in-kind support; developed visual identity and marketing material.</span>"),
  ("01/2023 \u2013 now", "<b>Digital and Student Ambassador</b>, University of the Arts London<br><span>Created content for UAL's social media for prospective students.</span>"),
  ("04/2023 \u2013 now", "<b>Gallery Assistant</b>, Central Saint Martins, Front of House<br><span>Event logistics and safety, visitor guidance, opening and closing the Platform Bar.</span>"),
  ("04/2024", "<b>Student Producer</b>, Auto Italia Southeast, London<br><span>Helped plan and install the exhibition <i>Filo</i>, working with the artist, curators and production team.</span>"),
  ("04/2023 \u2013 12/2023", "<b>Art Assistant</b>, Art-K Dulwich, London<br><span>Assisted art sessions for students aged 6 to 16; managed studio materials and set-up.</span>"),
])}
  </section>

  <section class="cv-block"><h2>Education</h2>
{cv_rows([("09/2022 \u2013 06/2025", "<b>BA (Hons) Fine Art: Computational Arts</b>, First Class, Camberwell College of Arts, University of the Arts London")])}
  </section>

  <section class="cv-block"><h2>Languages</h2>
{cv_rows([("", "Mandarin Chinese, native \u00b7 English, proficient (C1)")])}
  </section>"""

# journal entries, newest first: (date, anchor, title, what it is about). Paste each entry's text into its <div class="entry-text">.
WRITINGS = [
 ("25 Aug 2026", "25-08-2026", "Scalfolding?", "a fragment on scaffolding, and temporary home"),
 ("5 Sep 2025", "05-09-2025", "Interview with Amy Dowrick", "an interview on practice, process, and the works of 2025"),
 ("2 May 2025", "02-05-2025", "DHS and his home sweet home", "on Do Ho Suh's <i>Walk the House</i>, Tate Modern"),
 ("16 Apr 2025", "16-04-2025", "my bunk bed vs Tracey Emin's <i>My Bed</i>", "on vulnerability and the bed as a site of transition"),
 ("15 Apr 2025", "15-04-2025", "Nostalgic Playground", "on Rupert Norfolk's <i>Playground</i>"),
 ("6 Apr 2025", "06-04-2025", "Object-orientated storytelling", "on Jasleen Kaur's <i>Alter Altar</i>"),
 ("29 Mar 2025", "29-03-2025", "On fluidity of home", "what friends said home is"),
 ("20 Mar 2025", "20-03-2025", "Technoskepticism: Between Possibility and Refusal", "on \u201cThe Longing for Home\u201d"),
 ("11 Mar 2025", "11-03-2025-a", "On Homesick, Sarabande and Material Memory", "on <i>Homesick</i> at Sarabande Foundation, and Yijia Wu's <i>Soap Tiles</i>"),
 ("11 Mar 2025", "11-03-2025-b", "On Intimacy and 1:1 Encounters", "on <i>Body-Phone-Complex</i> at Delfina Foundation, and Pillow Talk"),
]

def writings_body():
    idx = " ".join(f'<a href="#{a}">{d}</a>' for d, a, *_ in WRITINGS) + ' <a href="#bibliography">bibliography</a>'
    entries = "\n".join(f"""  <article class="entry" id="{a}">
    <p class="when">{d}</p>
    <h2>{t}</h2>
    <p class="about">{about}</p>
    <div class="entry-text"><p class="todo">Paste this entry's text here.</p></div>
  </article>""" for d, a, t, about in WRITINGS)
    return f"""  <p class="lede-intro">Notes, essays and an interview, newest first. You were told not to look.</p>
  <nav class="dates" aria-label="Entries">{idx}</nav>
{entries}
  <article class="entry" id="bibliography">
    <h2>Bibliography</h2>
    <div class="entry-text"><p class="todo">Paste the bibliography here.</p></div>
  </article>"""

WORKSHOPS = """  <p class="lede-intro">Workshops I run and co-host, and talks I have given.</p>
  <!-- ONE ENTRY: copy an <article> block, newest first. Add a photo with
       <figure class="ph" data-src="images/name.jpg"><img src="images/name.jpg" alt="what the photo shows"></figure> -->
  <article class="entry">
    <p class="when">since Jul 2024</p>
    <h2>Cranberry Lemonade workshops</h2>
    <p class="about">Co-host \u00b7 SET Social, the Good Rice, Copeland Gallery, London</p>
    <div class="entry-text"><p>Workshops on different themes of HTML, organised and facilitated with Cranberry Lemonade.</p></div>
  </article>
  <article class="entry">
    <p class="when">Jul 2024 \u00b7 Aug 2025</p>
    <h2>HTML Energy 2024 &amp; 2025</h2>
    <p class="about">Co-host \u00b7 London</p>
    <div class="entry-text"><p>Hands-on sessions making a personal web page with HTML, CSS and JavaScript, built so that every participant leaves with a page that is unmistakably their own.</p></div>
  </article>
  <article class="entry">
    <p class="when">Jun 2024</p>
    <h2>The New Ideas Exhibit</h2>
    <p class="about">Talk \u00b7 Creative Tech &amp; Digital Design, London</p>
    <div class="entry-text"><p>Presenting the bacteria project, <a href="works/microcosm-of-identity.html"><i>Microcosm of Identity</i></a>, to industry professionals and fellow creatives.</p></div>
  </article>
  <article class="entry">
    <p class="when">Feb 2024</p>
    <h2>Rebuild a World with Bacteria, from Micro to Macro</h2>
    <p class="about">Artist talk \u00b7 BOM Immersive Arts Meet-Up, Birmingham</p>
    <div class="entry-text"><p>A talk for artists and technologists on the process behind the bacteria work.</p></div>
  </article>
  <article class="entry">
    <p class="when">Jan 2024</p>
    <h2>Culture and Identity</h2>
    <p class="about">Workshop, with Tutu Gbadamosi \u00b7 Enhancing Engagement Forum, UAL, London</p>
    <div class="entry-text"><p>Video interviews with students on identity and belonging opened the session, followed by collage-making and discussion for university staff on community and inclusivity at UAL.</p></div>
  </article>"""

os.makedirs(f"{ROOT}/works", exist_ok=True)
open(f"{ROOT}/archive.html", "w").write(archive())
import glob
for old in glob.glob(f"{ROOT}/*.html"):                      # clear tag pages from an earlier build
    if open(old).read(3000).find('data-page="tag"') > -1: os.remove(old)
for k, (name, n) in all_tags():
    open(f"{ROOT}/{k}.html", "w").write(archive(k).replace("<body>", '<body data-page="tag">', 1))
open(f"{ROOT}/about.html", "w").write(simple("", "About", "about", ABOUT, "about"))
open(f"{ROOT}/works/cv.html", "w").write(simple("../", "CV", "cv", CV, "cv"))
open(f"{ROOT}/writings.html", "w").write(simple("", "Writings", "don't look in here", writings_body(), "writings"))
open(f"{ROOT}/workshops.html", "w").write(simple("", "Workshops", "workshops", WORKSHOPS, "workshops"))
if os.path.exists(f"{ROOT}/works/dont-look-in-here.html"): os.remove(f"{ROOT}/works/dont-look-in-here.html")
for i in range(len(WORKS)):
    open(f"{ROOT}/works/{WORKS[i][0]}.html", "w").write(work(i, WORKS))
print("built", len(WORKS), "work pages,", len(all_tags()), "tag pages + archive, about, cv, writings, workshops")
