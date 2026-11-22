[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/gta6scam/meridian-wire-21-nov/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/gta6scam/meridian-wire-21-nov/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

# The Meridian Wire — Saturday 21 November 2026 in one picture (Round 4 challenger A4)

A single 1024×1024 front page summing up Saturday 21 November 2026: 40 stories
from 7 regions — missiles landing in Poland, COP31 slipping into overtime,
Wall Street falling into correction, Denmark exposing a plot, the EU adopting
€1bn in military aid for Ukraine, and India 159/1 at stumps in Wellington.

Facts come ONLY from the verified POOL21 pool. Every number on the page was
swept against it: the EU **adopted €1bn** (joint buying via the Peace Facility;
Britain pledges 1,000+ drones in a £260m package) — never "€8bn paid".
Numbers strip: 3 · 42 · −5.28% · 372,000 · €1BN · 159/1, all bound to cards.

Anatomy (§7/§8): giant Playfair masthead = the paper's NAME as anchor (date
demoted to the top bar), red hook band with the top-3 stories, 13 pictured
cards each with source tag + data label + caption band and ≥2 facts per deck,
UTC timeline (5 slots), real-polygon world map with numbered pins Ø18px (r9)
for the 13 cards and dots for the 27 briefs, DATE CHECK naming 6 Friday
20 November discards + 3 not-yet items, footer with sources.

## Duel record (mandatory, this build)

Three layout variants were built and rendered by draw.py (`python3 draw.py all`):

- **Variant A — Rail** (vertical UTC/numbers rail, 2-column card flow):
  FAILED completeness — briefs overflowed into the DATE CHECK box and the
  footer was pushed off-page.
- **Variant B — Stack** (horizontal timeline + numbers, 3 serif lead cards,
  5+5 mini grid, map + 2-column briefs): **WINNER.** Only variant where all
  40 stories, DATE CHECK and footer fit with no overlap; at 300px the
  masthead, hook band, numbers and lead headlines stay legible.
- **Variant C — Ledger** (centred masthead, navy hook, 3-column briefs):
  FAILED completeness — the 3-column brief block overflowed into DATE CHECK.

Only the winner (B) is kept as `entry.png`; A and C remain reproducible from
draw.py as backups.

**3D vs 2D:** the page uses flat 2D data strips (winner). A 3D/isometric
treatment was rejected as the backup direction: it inflates file size and
hurts 300px readability of decks and pin numbers, with no added facts.

## Files

- `draw.py` — fresh deterministic Pillow compose program (stdlib + PIL only).
- `main.py` — copy-pattern hand-in: copies the committed `entry.png` into
  `os.environ["MAKEFUN_OUTPUT_DIR"]` (never hardcodes /output).
- `entry.png` — 104,198 bytes, sha256
  f1027fb401b9825763667baeeae63e5666c58c926c8f2604d19511c8278798ad
  (palette-quantized; render-twice byte-identical; nobody isolation test PASS).
- `mapdata.py`, `fonts/` — real country polygons + Playfair/Archivo (OFL).

All illustrations are original drawings composed by draw.py.
