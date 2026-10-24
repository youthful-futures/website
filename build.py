"""Inline the Open paths artwork into the hero so its lines can animate.
Run: python3 build.py  ->  writes index.html from src/index.html"""
import re
from pathlib import Path

root = Path(__file__).parent
svg = (root / "assets/img/open-paths-colour.svg").read_text()
svg = re.sub(r"<title>.*?</title>", "", svg)
svg = re.sub(r'\s(width|height|role)="[^"]*"', "", svg, count=3)
svg = svg.replace("<svg ", '<svg focusable="false" preserveAspectRatio="xMaxYMax meet" ', 1)
i = 0
def tag(m):
    global i
    i += 1
    return f'<path pathLength="1" style="--d:{0.15 + i * 0.022:.3f}s" '
svg = re.sub(r"<path ", tag, svg)
html = (root / "src/index.html").read_text().replace("{{ART}}", svg)
(root / "index.html").write_text(html)
print(f"index.html written, {i} paths animated")
