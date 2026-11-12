melissayunzhi.li

Every page is plain HTML: edit the file and save. There is no build step.

PAGES
index.html       SELECTED WORKS: the corridor of rooms. Each <article class="room"> is one room, front to back.
archive.html     every work, as a plain index by year. Hover a row to see its preview photo.
works/*.html     one page per work, plus the freelance sub-pages and the CV (works/cv.html).
about.html       about page.
writings.html    the journal ("Don't look in here" room), one <article class="entry"> per note.
workshops.html   workshops and talks, one <article class="entry"> each.
installation.html, web-art.html, ...   tag pages: the archive filtered to one tag.
404.html         shown for any address that doesn't exist.

LOOK
site.css         shared look for every page except the landing page. Colours at the top:
                   --head-bg / --head-ink   header (matches the landing page)
                   --foot-bg / --foot-ink   footer (matches the landing page's floor)
index.html       the landing page has its own colours at the top of its <style>:
                   --pages (background), --bark (text), --terracotta (floor)
                 If you change those, update --head-* and --foot-* in site.css to match.
media.js         on work / writings / workshops pages: click a photo to see it larger (only photos
                 that would actually get bigger), and the moshing photo sequences
                 (<div class="gallery erode">; add data-mode="fade" for a plain cross-fade).

PHOTOS
images/<slug>.jpg              the PREVIEW photo: landing-page room hover and archive hover.
images/works/<slug>/01.jpg ... the work page's photos. 01 is the main photo at the top of the page.
images/writings/, images/workshops/   photos for those pages.
images/writings.png            the "Don't look in here" room image (shown inside the room: data-fit="inside").
files/                         PDFs (CV and others) linked from the pages.

To add a photo to a work page, put it in images/works/<slug>/ and copy a <figure> inside one of
the page's <div class="gallery"> blocks. Keep width="" height="" and style="--r:width/height" right,
so the gallery rows line up. Write what the photo shows in alt="".

VIDEO
Vimeo: copy an existing <figure class="clip"><div class="video" style="--ar:1920/1080"><iframe ...>
block and change the video number and --ar (the video's width/height). Vimeo videos autoplay muted.

SHARING
Each page's <head> has a description and a preview image for link previews (og:description, og:image).
favicon.ico is the tab icon.

VISITOR STATS
Google Analytics (G-Y7ZRDY07BQ, the same account as the old Cargo site) is in every page's <head>,
between <!-- analytics --> and <!-- /analytics -->. It runs cookie-free (consent mode, analytics_storage
denied), so there is no cookie notice. To remove Analytics, delete that block from each page.

PUBLISHING
Drag this folder into Netlify, or push it to a GitHub Pages repo, then point melissayunzhi.li at it.
_redirects (Netlify) sends old Cargo addresses (/spg, /bacteria, /cv-1 ...) to the new pages.
