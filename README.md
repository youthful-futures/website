# Youthful Futures — website

Single-page landing site. Static HTML/CSS, no dependencies.

- Edit copy in `src/index.html`, then run `python3 build.py` to regenerate `index.html` (it inlines the Open paths artwork into the hero).
- Styles: `assets/style.css` (brand colours and Manrope from the identity kit).
- Preview: `python3 -m http.server` and open http://localhost:8000.

Pages: `index.html` (built), `privacy.html`, `terms.html`, `404.html`. Hosted on GitHub Pages at youthfulfutures.org (`CNAME`).

Privacy by design: no cookies, analytics, forms or third-party requests; all fonts are self-hosted. If you add any of these, update `privacy.html` first.

To do later:
- **People**: the section was removed for now. Its styles are still in `assets/style.css` (`.team`, `.person`) for when it returns.
- **Legal details**: add the organisation's legal name and address to `privacy.html` and a governing-law clause to `terms.html` once established (see the HTML comments).
