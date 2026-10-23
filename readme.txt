melissayunzhi.li

index.html       SELECTED WORKS: the corridor of rooms. Each <article class="room"> is one room, front to back.
archive.html     every work, as a plain index by year.
works/*.html     one standalone page per work. Replace "Write about this work here." and add photos.
about.html       about page.
writings.html    the journal ("Don't look in here" room). Paste each entry's text into its <div class="entry-text">.
workshops.html   workshops you run. Copy the commented <article> block for each one.        site.css   shared look for archive, about and work pages.
images/          photos. Name each after its work:
                   images/flickring-home.jpg     main photo: fills the top of the screen when you hover the title, archive hover, top of the work page
                   images/flickring-home-2.jpg   more photos on the work page
                   images/flickring-home-3.jpg   (-4, -5 ... copy a <figure> in the page for each)
                   images/about.jpg              portrait on the about page
build.py         optional: edit the WORKS list and run `python3 build.py .` to regenerate archive + work pages.
                 (This overwrites works/*.html, so only use it before you start writing in those pages.)

Moving a work in or out of the selected corridor:
  1. add or remove its <article class="room"> in index.html
  2. in build.py set the last value of its line to True/False (this sets the marker in the archive), or edit archive.html by hand.

To publish: drag this folder into Netlify, or push it to a GitHub Pages repo,
then point melissayunzhi.li at it from your domain settings.

Video: open build.py, find EXTRA, and paste a Vimeo link into a work's video="" (e.g. video="https://vimeo.com/123456789"),
       then run `python3 build.py .`  Or paste Vimeo's embed <iframe> straight into the work's page where it says VIDEO.
Cursor: the pixel arrow and hand are at the bottom of site.css (and in index.html). Swap the data: URLs for your own
       cursor image (PNG or SVG, up to 128 x 128 px) if you want your exact Cargo cursor.
Phones: resting in a room for about a second shows its photo; scrolling hides it. Desktop uses hover.

Tags: every category on a work becomes a tag page (installation.html, web-art.html, ...), built automatically
      by build.py from the categories in WORKS. Netlify and GitHub Pages serve them as /installation, /web-art.
      Add a category to a work, run `python3 build.py .`, and its tag page appears.

Logos: images/icons/instagram.png, are-na.png, linkedin.png are your official logos. Replace a file to change it;
       the site recolours them to match. (They show once the site is on a web host, not from files opened on your computer.)
_redirects: for Netlify. Sends old Cargo addresses (/flickring-home, /spg, /bacteria ...) to the new pages.

CV:   works/cv.html is built from your CV (build.py, CV = ...). Put cv.pdf in this folder and a "Download as PDF" link appears.
