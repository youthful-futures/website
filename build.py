"""Inline the Open paths artwork into the hero so it scales with the hero.
Run: python3 build.py  ->  writes index.html from src/index.html"""
import re
from pathlib import Path

root = Path(__file__).parent
svg = (root / "assets/img/open-paths-colour.svg").read_text()
svg = re.sub(r"<title>.*?</title>", "", svg)
svg = re.sub(r'\s(width|height|role)="[^"]*"', "", svg, count=3)
svg = svg.replace("<svg ", '<svg focusable="false" preserveAspectRatio="xMidYMin slice" ', 1)
html = (root / "src/index.html").read_text().replace("{{ART}}", svg)
(root / "index.html").write_text(html)
print("index.html written")
