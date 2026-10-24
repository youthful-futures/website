"""Build the Writing section from content/youthful-futures-series.md.

Writes writing/index.html (series page) and writing/<slug>/index.html for each
essay, and returns the essay list so build.py can add cards to the home page.
No dependencies: the series uses a small, predictable subset of Markdown.
"""
import html
import re
from pathlib import Path

ROOT = Path(__file__).parent
SOURCE = ROOT / "content/youthful-futures-series.md"
SITE = "https://youthfulfutures.org"
SERIES = "Youthful Futures"
OLD_PREFIX = "/youthful-futures/"   # slugs in the hand-off
NEW_PREFIX = "/writing/"            # where they live on this site

CSP = ("default-src 'none'; script-src 'none'; style-src 'self'; img-src 'self'; "
       "font-src 'self'; base-uri 'none'; form-action 'none'; upgrade-insecure-requests")


# ---------- Markdown subset ----------

def inline(text, notes=None):
    """Escape, then apply links, footnote refs, bold, italic and bare URLs."""
    s = html.escape(text, quote=False)
    s = s.replace("`", "")

    def link(m):
        label, url = m.group(1), m.group(2).replace(OLD_PREFIX, NEW_PREFIX)
        ext = url.startswith("http")
        attrs = ' rel="noopener noreferrer"' if ext else ""
        return f'<a href="{html.escape(url)}"{attrs}>{label}</a>'
    s = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", link, s)

    if notes is not None:
        def ref(m):
            n = notes[m.group(1)]
            return f'<sup class="fn"><a href="#note-{n}" id="ref-{n}-{m.start()}" aria-label="Source {n}">{n}</a></sup>'
        s = re.sub(r"\[\^([\w-]+)\]", ref, s)

    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<![*\w])\*(?!\s)(.+?)(?<!\s)\*(?![*\w])", r"<em>\1</em>", s)
    s = re.sub(r'(?<!["=>])(https?://[^\s<;]+)',
               lambda m: f'<a href="{m.group(1)}" rel="noopener noreferrer">{m.group(1)}</a>', s)
    return s


def paragraphs(lines):
    out, buf = [], []
    for line in lines + [""]:
        if line.strip():
            buf.append(line.strip())
        elif buf:
            out.append(" ".join(buf))
            buf = []
    return out


# ---------- Parse the series ----------

def parse():
    text = SOURCE.read_text()
    text = text.split("\n---\n", 1)[1] if text.startswith("---") else text  # drop front matter
    head, *chunks = re.split(r"^# (?=\d+\. )", text, flags=re.M)

    standfirst = re.search(r"### Series standfirst\s+\*\*(.+?)\*\*", head, re.S).group(1)
    intro_block = head.split("### Series introduction", 1)[1].split("### Series SEO", 1)[0]
    intro = paragraphs(intro_block.strip().splitlines())
    seo_title = re.search(r"\*\*SEO title:\*\* (.+)", head).group(1).strip()
    seo_desc = re.search(r"\*\*Meta description:\*\* (.+)", head).group(1).strip()

    essays = []
    for chunk in chunks:
        chunk = chunk.split("\n# Handoff notes", 1)[0].rstrip().rstrip("-").rstrip()
        title_line, rest = chunk.split("\n", 1)
        num, title = re.match(r"(\d+)\. (.+)", title_line).groups()
        meta = dict(re.findall(r"^\*\*([\w ]+):\*\* (.+)$", rest, flags=re.M))
        slug = meta["Slug"].strip("` ").replace(OLD_PREFIX, "").strip("/")
        body_part, _, notes_part = rest.partition("### Sources and notes")
        body_lines = [l for l in body_part.splitlines() if not re.match(r"^\*\*[\w ]+:\*\* ", l)]
        defs = re.findall(r"^\[\^([\w-]+)\]: (.+)$", notes_part, flags=re.M)
        related = re.findall(r"\[([^\]]+)\]\(([^)]+)\)", meta.get("Suggested related articles", ""))
        essays.append({
            "num": int(num), "title": title.strip(), "slug": slug,
            "dek": meta["Dek"].strip(), "seo_title": meta["SEO title"].strip(),
            "description": meta["Meta description"].strip(),
            "tags": [t.strip() for t in meta.get("Tags", "").split(",") if t.strip()],
            "body": paragraphs(body_lines), "defs": defs,
            "related": [(t, u.replace(OLD_PREFIX, NEW_PREFIX)) for t, u in related],
        })
    return {"standfirst": standfirst, "intro": intro, "seo_title": seo_title,
            "seo_desc": seo_desc, "essays": essays}


# ---------- Page shell ----------

def page(title, description, canonical, body, og_type="website"):
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="Content-Security-Policy" content="{CSP}">
<meta name="referrer" content="no-referrer">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(description)}">
<meta name="theme-color" content="#29245C">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(description)}">
<meta property="og:type" content="{og_type}">
<meta property="og:url" content="{SITE}{canonical}">
<meta property="og:image" content="{SITE}/assets/img/04-First-post-1200x627.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="canonical" href="{SITE}{canonical}">
<link rel="icon" href="/assets/img/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/assets/img/favicon-32.png" sizes="32x32">
<link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">
<link rel="stylesheet" href="/assets/style.css">
</head>
<body>

<a class="skip" href="#main">Skip to content</a>

<header class="nav">
  <div class="wrap nav__inner">
    <a href="/" class="nav__logo" aria-label="Youthful Futures home">
      <img src="/assets/img/wordmark-horizontal-indigo.svg" alt="Youthful Futures" width="216" height="32">
    </a>
    <nav aria-label="Primary">
      <ul class="nav__links">
        <li><a href="/#about">About</a></li>
        <li><a href="/#work">Our work</a></li>
        <li><a href="/writing/">Writing</a></li>
        <li><a href="/#connect">Connect</a></li>
      </ul>
    </nav>
  </div>
</header>

<main id="main">
{body}
</main>

<footer class="footer">
  <div class="wrap footer__grid">
    <img src="/assets/img/wordmark-stacked-reverse.svg" alt="Youthful Futures" width="150" height="69">
    <p class="footer__tag">Many futures. Every young person.</p>
    <nav class="footer__links" aria-label="Legal">
      <a href="/privacy.html">Privacy</a>
      <a href="/terms.html">Terms</a>
      <a href="mailto:contact@youthfulfutures.org">Contact</a>
    </nav>
    <p class="footer__small">© 2026 Youthful Futures</p>
  </div>
</footer>
</body>
</html>
"""


def minutes(essay):
    words = sum(len(p.split()) for p in essay["body"])
    return max(1, round(words / 230))


def card(e, heading="h3"):
    return f"""<li class="essay">
          <a href="/writing/{e['slug']}/">
            <span class="essay__num">{e['num']:02d}</span>
            <{heading} class="essay__title">{inline(e['title'])}</{heading}>
            <p class="essay__dek">{inline(e['dek'])}</p>
            <span class="essay__meta">{minutes(e)} min read</span>
          </a>
        </li>"""


# ---------- Pages ----------

def series_page(data):
    intro = "\n".join(f"        <p>{inline(p)}</p>" for p in data["intro"])
    cards = "\n        ".join(card(e, "h2") for e in data["essays"])
    body = f"""  <section class="series-hero">
    <div class="wrap">
      <p class="label label--celadon">Writing · A 12-part series</p>
      <h1>{SERIES}</h1>
      <p class="series-hero__standfirst">{inline(data['standfirst'])}</p>
    </div>
  </section>

  <section class="series-intro">
    <div class="wrap">
      <div class="prose prose--article">
{intro}
      </div>
    </div>
  </section>

  <section class="series-list" aria-label="Essays in the series">
    <div class="wrap">
      <ol class="essays">
        {cards}
      </ol>
    </div>
  </section>"""
    return page(data["seo_title"], data["seo_desc"], "/writing/", body)


def essay_page(e, prev, nxt):
    notes = {nid: i + 1 for i, (nid, _) in enumerate(e["defs"])}
    paras = "\n".join(f"        <p>{inline(p, notes)}</p>" for p in e["body"])
    sources = "\n".join(
        f'          <li id="note-{i + 1}">{inline(text)}</li>' for i, (_, text) in enumerate(e["defs"]))
    related = "\n".join(
        f'          <li><a href="{u}">{inline(t)}</a></li>' for t, u in e["related"])
    prev_link = (f'<a class="pager__link" href="/writing/{prev["slug"]}/"><span>← Previous</span>{inline(prev["title"])}</a>'
                 if prev else "<span></span>")
    next_link = (f'<a class="pager__link pager__link--next" href="/writing/{nxt["slug"]}/"><span>Next →</span>{inline(nxt["title"])}</a>'
                 if nxt else "<span></span>")
    body = f"""  <article class="essay-page">
    <header class="essay-head">
      <div class="wrap">
        <p class="label label--celadon"><a href="/writing/">{SERIES}</a> · Essay {e['num']} of 12</p>
        <h1>{inline(e['title'])}</h1>
        <p class="essay-head__dek">{inline(e['dek'])}</p>
        <p class="essay-head__meta">{minutes(e)} min read</p>
      </div>
    </header>

    <div class="wrap">
      <div class="prose prose--article">
{paras}
      </div>

      <aside class="essay-foot">
        <details class="sources" open>
          <summary>Sources and notes</summary>
          <ol>
{sources}
          </ol>
        </details>

        <div class="related">
          <h2>Related reading</h2>
          <ul>
{related}
          </ul>
        </div>

        <nav class="pager" aria-label="Series">
          {prev_link}
          {next_link}
        </nav>
        <p class="essay-foot__all"><a href="/writing/">All 12 essays in the series</a></p>
      </aside>
    </div>
  </article>"""
    return page(e["seo_title"], e["description"], f"/writing/{e['slug']}/", body, og_type="article")


def build():
    data = parse()
    out = ROOT / "writing"
    out.mkdir(exist_ok=True)
    (out / "index.html").write_text(series_page(data))
    es = data["essays"]
    for i, e in enumerate(es):
        d = out / e["slug"]
        d.mkdir(exist_ok=True)
        (d / "index.html").write_text(essay_page(e, es[i - 1] if i else None, es[i + 1] if i + 1 < len(es) else None))

    urls = ["/", "/writing/"] + [f"/writing/{e['slug']}/" for e in es] + ["/privacy.html", "/terms.html"]
    (ROOT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "".join(f"  <url><loc>{SITE}{u}</loc></url>\n" for u in urls) + "</urlset>\n")
    print(f"writing/ built: series page + {len(es)} essays")
    return data


if __name__ == "__main__":
    build()
