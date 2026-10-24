"""Build the site.
Run: python3 build.py
- index.html from src/index.html (inlines the Open paths artwork into the hero,
  and adds the latest essays to the Writing section)
- writing/ from content/youthful-futures-series.md (see build_writing.py)"""
import re
from pathlib import Path

import build_writing

root = Path(__file__).parent
svg = (root / "assets/img/open-paths-colour.svg").read_text()
svg = re.sub(r"<title>.*?</title>", "", svg)
svg = re.sub(r'\s(width|height|role)="[^"]*"', "", svg, count=3)
svg = svg.replace("<svg ", '<svg focusable="false" preserveAspectRatio="xMidYMin slice" ', 1)

series = build_writing.build()
cards = "\n        ".join(build_writing.card(e) for e in series["essays"][:3])

html = (root / "src/index.html").read_text().replace("{{ART}}", svg).replace("{{ESSAYS}}", cards)
(root / "index.html").write_text(html)
print("index.html written")
