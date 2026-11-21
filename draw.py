#!/usr/bin/env python3
"""THE MERIDIAN WIRE - Variant A: the world in one day, Saturday 21 Nov 2026.

Compose program for the make.fun news-image-20261121 entry. Draws a
1024x1024 front page (entry.png, next to this file) with Pillow only:
flat layered shapes, real-polygon world map, every story carrying its
source on the page. Deterministic: no randomness, no clocks, no network.
All facts come from the day's merged news pool (POOL21.md).
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from mapdata import WORLD  # noqa: E402

FONT_DIR = os.path.join(HERE, "fonts")
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
MX = 16                      # page margin
CW = W - 2 * MX              # content width = 992

PAPER = (247, 241, 227)      # cream #F7F1E3
CARD_BG = (253, 250, 242)
INK = (20, 33, 61)           # navy #14213D
RED = (176, 58, 46)          # accent #B03A2E
NAVY = (22, 40, 63)          # caption band / map sea #16283F
LAND = (96, 116, 92)
GREY = (90, 86, 76)
FAINT = (203, 192, 164)
WHITE = (255, 255, 255)

REGION_RGB = {
    "EUROPE": (176, 58, 46),
    "ASIA": (29, 111, 184),
    "MIDEAST": (125, 60, 152),
    "AFRICA": (30, 132, 73),
    "AMERICAS": (202, 111, 30),
    "OCEANIA": (20, 143, 119),
    "GLOBAL": (93, 109, 126),
}

SERIF = "PlayfairDisplay-900.ttf"
SANSB = "Archivo-Bold.ttf"
SANSM = "Archivo-Medium.ttf"

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

_cache = {}


def F(name, size):
    key = (name, int(size))
    if key not in _cache:
        _cache[key] = ImageFont.truetype(os.path.join(FONT_DIR, name), int(size))
    return _cache[key]


def tw(s, font):
    return d.textlength(s, font=font)


def wrap(text, font, max_w, max_lines=None):
    """Greedy word wrap; returns lines that each fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = word if not cur else cur + " " + word
        if tw(trial, font) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    if max_lines and len(lines) > max_lines:
        lines = lines[:max_lines]
    return lines


def text(x, y, s, font, fill=INK, anchor="la"):
    d.text((x, y), s, font=font, fill=fill, anchor=anchor)


def fit_size(s, name, start, max_w, floor=10):
    """Largest font size <= start at which s fits max_w."""
    size = start
    while size > floor and tw(s, F(name, size)) > max_w:
        size -= 1
    return size

# ---------------------------------------------------------------- POOL data
NUMBERS = [
    ("3", "weapons cross into Poland: two missiles and a jet drone"),
    ("42", "injured in the Kryvyi Rih strike, four of them children"),
    ("900,000", "AI chips the US cleared for China in one move"),
    ("6", "Houthi missile workshops destroyed in Sana'a"),
    ("€1BN", "adopted by the EU for Ukraine aid"),
    ("159/1", "India at stumps in Wellington, day three"),
]

TIMELINE = [
    ("Overnight", "Kryvyi Rih strike: two killed, 42 injured"),
    ("Morning", "Rutte flies to Warsaw over the missiles"),
    ("Midday", "Antalya: third COP31 draft due after overnight talks"),
    ("Afternoon", "Denmark expels the Russian attache"),
    ("Evening", "BepiColombo reaches Mercury; India 159/1 at stumps"),
]

REGION_COUNTS = [
    ("EUROPE", 12), ("ASIA", 8), ("AMERICAS", 8), ("MIDEAST", 5),
    ("AFRICA", 1), ("OCEANIA", 1), ("GLOBAL", 3),
]

# no, place, region, topic, headline, deck (sources in parens), strip source
# tag, strip data label, caption band text, pin lon/lat, scene key
CARDS = [
    (1, "WARSAW, POLAND", "EUROPE", "MISSILES",
     "Rutte flies to Warsaw after missiles land",
     "Two missiles and a suspected jet drone came down in the "
     "south-east, a Kh-101 near Nowy Lipowiec. NATO's Rutte calls it "
     "a \"grave violation\"; Tusk calls it a deliberate provocation. (AP)",
     "AP - SOFX", "3 WEAPONS CROSS", "NOWY LIPOWIEC - MISSILES DOWN",
     21.0, 52.2, "poland"),
    (2, "ANTALYA", "GLOBAL", "CLIMATE SUMMIT",
     "COP31 runs into overtime with no deal yet",
     "Talks ran past Friday's scheduled close into Saturday, with "
     "92,000 accredited. The draft drops every fossil-fuel reference "
     "and the $120bn finance target; a third draft is due this "
     "morning. (AP)",
     "Ongoing - AP", "NO DEAL YET", "ANTALYA - INTO OVERTIME",
     30.7, 36.9, "cop31"),
    (3, "WASHINGTON", "AMERICAS", "TECH",
     "US clears 900,000 AI chips for China",
     "Washington cleared about 900,000 advanced AI chips for export "
     "to China in a single licensing move. Beijing welcomed the "
     "decision; security hawks in Congress called it a strategic "
     "giveaway. (Reuters)",
     "Cleared - US", "900,000 CHIPS", "WASHINGTON - THE CHIP CLEARANCE",
     -77.0, 38.9, "chips"),
    (4, "KRYVYI RIH", "EUROPE", "STRIKE",
     "Russian strike kills two, injures 42",
     "Strike kills two and injures 42, four of them children, city "
     "chief says. One of Russia's largest war attacks. (AppiStos)",
     "City chief says", "2 DEAD - 42 HURT", "KRYVYI RIH - OVERNIGHT STRIKE",
     33.4, 47.9, "kyiv"),
    (5, "COPENHAGEN", "EUROPE", "PLOT",
     "Denmark exposes 'assassination plot'",
     "Russia 'planned and initiated' a plot on a Ukrainian-American "
     "rapper, Denmark says. Attache expelled. (BBC)",
     "Denmark says - BBC", "ATTACHE EXPELLED", "COPENHAGEN - THE PLOT",
     12.6, 55.7, "copenhagen"),
    (6, "KYIV", "EUROPE", "BARRAGE",
     "Russia's barrage: 400 drones, 110 missiles",
     "Eight dead in the overnight barrage. Power rationed in Kyiv; "
     "some 50 Rivne settlements blacked out. (BBC)",
     "Officials' count", "400 DRONES - 110 MISSILES",
     "KYIV - OVERNIGHT BARRAGE", 30.5, 50.4, "barrage"),
    (7, "RIYADH - SANA'A", "MIDEAST", "ESCALATION",
     "Coalition hits Houthi workshops; 3 missiles downed",
     "Jets destroy six Houthi workshops in Sana'a. Saudi defences "
     "down three missiles over Riyadh. (Reuters)",
     "Coalition says", "3 MISSILES DOWNED", "SANA'A - WORKSHOPS HIT",
     46.7, 24.6, "riyadh"),
    (8, "BRUSSELS", "EUROPE", "MILITARY AID",
     "EU adopts €1bn aid for Ukraine",
     "Joint buying via the Peace Facility; Britain pledges 1,000+ "
     "drones alongside. (Reuters)",
     "Adopted - EU", "EUR 1BN ADOPTED", "BRUSSELS - AID ADOPTED",
     4.3, 50.8, "ukeu"),
    (9, "NEW YORK", "AMERICAS", "CYBERATTACK",
     "JPMorgan, Visa, Mastercard hit by cyberattack",
     "The banks report incidents at third-party vendors. Their core "
     "payment networks are unaffected, they say. (Reuters)",
     "Banks say", "3 NETWORKS HIT", "NEW YORK - THE VENDOR BREACH",
     -73.9, 40.8, "cyber"),
    (10, "MERCURY", "GLOBAL", "DEEP SPACE",
     "BepiColombo reaches Mercury tonight",
     "Eight years out, ESA and JAXA's twin orbiters burn at 19:24 "
     "CET tonight to be captured by Mercury. (ESA)",
     "ESA - tonight", "8 YEARS - TONIGHT", "MERCURY - ARRIVAL TONIGHT",
     None, None, "mercury"),
    (11, "THE HAGUE", "GLOBAL", "WORLD COURT",
     "Myanmar ruling rattles Israel's Gaza defence",
     "Myanmar verdict raises questions in Jerusalem over its own "
     "case, experts say. Ruling came Thursday. (BBC)",
     "Experts say", "GENOCIDE VERDICT", "THE HAGUE - THE VERDICT",
     4.3, 52.1, "seoul"),
    (12, "KHARG ISLAND", "MIDEAST", "OIL",
     "Iran runs a tanker convoy to test the blockade",
     "Crews sail 14+ tankers from Kharg Island to test the US "
     "blockade. Brent jumps 4.6% to $94.65. (Reuters)",
     "Traders say", "BRENT $94.65", "KHARG ISLAND - THE CONVOY",
     50.3, 29.2, "tanker"),
    (13, "WELLINGTON", "OCEANIA", "CRICKET",
     "India fight back: 159/1 at stumps, day three",
     "India trail New Zealand by 209 in the first Test after the "
     "hosts made 368. Nicholls made 175 not out for the hosts. (ICC)",
     "Scorecard - ICC", "159/1 - DAY THREE", "WELLINGTON - DAY THREE",
     174.8, -41.3, "cricket"),
]

# no, one-line text (source in parens), region, pin lon/lat (None = off-map)
BRIEFS = [
    (14, "Sumy A HIMARS strike wipes out 20 Russian commanders, Ukraine says (Ukrinform)", "EUROPE", 34.8, 50.9),
    (15, "London Britain hit Moscow with retaliatory cyberattacks, officials say (Reuters)", "EUROPE", -0.1, 51.5),
    (16, "California California subpoenas Nvidia in an AI-chip export probe (Reuters)", "AMERICAS", -121.5, 38.6),
    (17, "New Delhi India launches its first H5N1 vaccine (Reuters)", "ASIA", 77.2, 28.6),
    (18, "New Delhi Modi opens an SCO dialogue forum in the capital (Reuters)", "ASIA", 77.2, 28.6),
    (19, "Imphal Manipur violence leaves 11 dead and 181 in hospital (PTI)", "ASIA", 93.9, 24.8),
    (20, "Atlanta Measles costs the US its elimination status, the CDC confirms (AP)", "AMERICAS", -84.4, 33.7),
    (21, "Pasadena Voyager 1 is now one light-day from Earth (NASA)", "AMERICAS", -118.1, 34.1),
    (22, "Tokyo Japan will buy up to 8m barrels of Saudi crude (Reuters)", "ASIA", 139.7, 35.7),
    (23, "Leverkusen Bayer agrees a $7.25bn Roundup settlement (Reuters)", "EUROPE", 7.0, 51.0),
    (24, "Jakarta Indonesia asks Google why 19,000 accounts vanished (Reuters)", "ASIA", 106.8, -6.2),
    (25, "Las Vegas Grand Prix qualifying runs under the lights tonight (AP)", "AMERICAS", -115.1, 36.2),
    (26, "Hodeidah The UN warns port strikes threaten Yemen's aid lifeline (UN)", "MIDEAST", 43.0, 14.8),
    (27, "Washington Trump says Iran wants a deal on its nuclear programme (AP)", "AMERICAS", -77.0, 38.9),
    (28, "Odisha Relief under way after Akvan: 372,000 sheltered, no deaths (Ridhu Times)", "ASIA", 84.9, 19.3),
    (29, "Johannesburg The ANC polls 31%, its worst since 1994; coalition race begins (BBC)", "AFRICA", 28.0, -26.2),
    (30, "Kathmandu Nepal's new leader Balendra Shah faces an India test (BBC)", "ASIA", 85.3, 27.7),
    (31, "Cardiff Lauren Price beats Kotaskova to become undisputed champion (BBC)", "EUROPE", -3.2, 51.5),
    (32, "Gaza On World Children's Day, Palestinian children appeal for help (UN)", "MIDEAST", 34.3, 31.5),
    (33, "Buenos Aires Argentina's Senate backs a disability framework, 71-0 (AP)", "AMERICAS", -58.4, -34.6),
    (34, "Frankfurt ECB names Boone and Brunnermeier for its Executive Board (Reuters)", "EUROPE", 8.7, 50.1),
    (35, "Kharkiv Ukraine says it has finished a \"Bear Trap\" in the Kharkiv area (Ukrinform)", "EUROPE", 36.2, 49.9),
    (36, "Kuala Lumpur Malaysia to send 10,000 Rohingya to Turkey for training (Reuters)", "ASIA", 101.7, 3.1),
    (37, "Rome Italian workers and students march against Meloni's government (AFP)", "EUROPE", 12.5, 41.9),
    (38, "Jeddah Saudi Arabia warns of thunderstorms through Tuesday (SPA)", "MIDEAST", 39.2, 21.5),
]

DATE_CHECK = (
    "Left out as Friday 20 November's news: Wall Street's AI sell-off "
    "and the Nasdaq's 5.28% fall, Mongolia's president resigning, "
    "Kyiv's three bridges hit, Cyclone Akvan's landfall at Gopalpur, "
    "the Shenzhen three-leader summit, the UK-EU reset deal and "
    "Asia's AI sell-off (Taipei -6.2%). The world court's Myanmar "
    "ruling and Anthropic's $81.3bn IPO filing both came on Thursday "
    "19 November. Not yet happened: any final COP31 text."
)

FOOTER_L = ("Every story here happened, or was first reported, on Saturday "
            "21 November 2026. Contested claims are attributed.")
FOOTER_R = "Sources named beside each story - original drawings"

# ------------------------------------------------------------------- header
def draw_header():
    # kicker bar: section left, the date centred, story count right
    text(MX, 11, "THE WORLD IN ONE DAY", F(SANSB, 11), INK)
    dt = "SATURDAY 21 NOVEMBER 2026"
    text(W / 2, 9, dt, F(SANSB, 12), INK, anchor="ma")
    right = "38 STORIES - 7 REGIONS - EVERY ONE DATED TODAY"
    text(W - MX, 11, right, F(SANSB, 11), INK, anchor="ra")
    d.rectangle([MX, 31, W - MX, 34], fill=RED)
    d.line([MX, 37, W - MX, 37], fill=INK, width=1)

    # masthead: the paper's name is the anchor, not the date
    title = "THE MERIDIAN WIRE"
    size = fit_size(title, SERIF, 64, CW)
    text(MX, 38, title, F(SERIF, size), INK)
    # hook band: the three biggest stories, white on the paper's red
    hk = ("MISSILES LAND IN POLAND - US CLEARS 900,000 AI CHIPS FOR "
          "CHINA - COP31 DEADLOCKED IN OVERTIME")
    d.rectangle([MX, 96, W - MX, 118], fill=RED)
    text(W / 2, 103, hk, F(SANSB, 12), WHITE, anchor="ma")

    # UTC timeline strip
    ty0, ty1 = 120, 156
    d.rectangle([MX, ty0, W - MX, ty1], outline=INK, width=1)
    cell = CW / 5.0
    for i, (lab, ev) in enumerate(TIMELINE):
        cx = MX + i * cell
        if i:
            d.line([cx, ty0, cx, ty1], fill=FAINT, width=1)
        text(cx + 7, ty0 + 3, lab.upper(), F(SANSB, 10), RED)
        for j, ln in enumerate(wrap(ev, F(SANSM, 9), cell - 13, 2)):
            text(cx + 7, ty0 + 17 + j * 11, ln, F(SANSM, 9), INK)

    # THE DAY IN NUMBERS
    ny = 164
    text(MX, ny, "THE DAY IN NUMBERS", F(SANSB, 10), GREY)
    col = CW / 6.0
    for i, (num, cap) in enumerate(NUMBERS):
        cx = MX + i * col
        text(cx, ny + 10, num, F(SERIF, 24), RED)
        for j, ln in enumerate(wrap(cap, F(SANSM, 9), col - 10, 2)):
            text(cx, ny + 41 + j * 10, ln, F(SANSM, 9), INK)

    # region count chips
    cy = 226
    gap = 6
    widths = []
    for name, n in REGION_COUNTS:
        s = "%s %d" % (name, n)
        widths.append(tw(s, F(SANSB, 10)) + 14)
    total = sum(widths) + gap * (len(widths) - 1)
    cx = MX + (CW - total) / 2.0
    for (name, n), wdt in zip(REGION_COUNTS, widths):
        d.rectangle([cx, cy, cx + wdt, cy + 18], fill=REGION_RGB[name])
        text(cx + wdt / 2, cy + 3, "%s %d" % (name, n), F(SANSB, 10),
             WHITE, anchor="ma")
        cx += wdt + gap
    return cy + 18  # next free y = 242

# ------------------------------------------------------------------- scenes
# Each painter fills the scene box (strip minus caption band) with flat
# layered shapes. Data labels / source tags / caption band are added by
# the card renderer, never by the painters.
def sc_kyiv(x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(38, 52, 84))
    ry = y1 - (y1 - y0) * 0.28
    d.rectangle([x0, ry, x1, y1], fill=(52, 96, 128))          # river
    by = ry - 6
    d.rectangle([x0, by, x1, by + 5], fill=(16, 22, 38))       # bridge deck
    for fx in (0.30, 0.68):
        tx = x0 + (x1 - x0) * fx
        d.rectangle([tx - 3, y0 + 8, tx + 3, by], fill=(16, 22, 38))
        for k in range(1, 5):
            d.line([tx, y0 + 10, x0 + (x1 - x0) * (fx - 0.05 * k), by],
                   fill=(140, 160, 190), width=1)
            d.line([tx, y0 + 10, x0 + (x1 - x0) * (fx + 0.05 * k), by],
                   fill=(140, 160, 190), width=1)
    for i, fx in enumerate((0.12, 0.5, 0.86)):                 # missile arcs
        sx = x0 + (x1 - x0) * fx
        d.arc([sx - 26, y0 + 2 + i * 3, sx + 30, y0 + 52 + i * 3],
              start=200, end=320, fill=RED, width=2)
        d.ellipse([sx + 24, y0 + 20 + i * 3, sx + 30, y0 + 26 + i * 3],
                  fill=RED)


def sc_akvan(x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(70, 130, 160))
    cx, cy = x0 + (x1 - x0) * 0.36, y0 + (y1 - y0) * 0.48
    for r in (30, 23, 16, 9):
        d.arc([cx - r, cy - r * 0.8, cx + r, cy + r * 0.8],
              start=20, end=300, fill=WHITE, width=3)
    d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=(30, 70, 95))
    d.polygon([(x0, y1), (x1, y1), (x1, y1 - 12),
               (x0 + (x1 - x0) * 0.55, y1 - 20), (x0, y1 - 8)],
              fill=(214, 196, 140))                            # coast
    for i in range(9):                                         # rain
        rx = x0 + 12 + i * ((x1 - x0 - 20) / 8.0)
        d.line([rx, y0 + 8, rx - 5, y0 + 20], fill=(210, 235, 245), width=2)


def sc_markets(x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(18, 24, 40))
    for i in range(1, 4):
        gy = y0 + (y1 - y0) * i / 4.0
        d.line([x0, gy, x1, gy], fill=(52, 64, 92), width=1)
    pts = [(x0 + (x1 - x0) * f, y0 + (y1 - y0) * g)
           for f, g in ((0.02, 0.25), (0.25, 0.32), (0.45, 0.28),
                        (0.62, 0.55), (0.80, 0.62), (0.97, 0.85))]
    d.line(pts, fill=RED, width=3)
    for px, py in pts:
        d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=RED)


def _flag_uk(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(30, 50, 130))
    d.line([x, y, x + w, y + h], fill=WHITE, width=3)
    d.line([x + w, y, x, y + h], fill=WHITE, width=3)
    d.rectangle([x + w / 2 - 3, y, x + w / 2 + 3, y + h], fill=WHITE)
    d.rectangle([x, y + h / 2 - 3, x + w, y + h / 2 + 3], fill=WHITE)
    d.rectangle([x + w / 2 - 2, y, x + w / 2 + 2, y + h], fill=RED)
    d.rectangle([x, y + h / 2 - 2, x + w, y + h / 2 + 2], fill=RED)


def _flag_eu(x, y, w, h):
    import math
    d.rectangle([x, y, x + w, y + h], fill=(30, 50, 160))
    cx, cy, r = x + w / 2, y + h / 2, h * 0.30
    for i in range(12):
        a = math.radians(i * 30 - 90)
        sx, sy = cx + r * math.cos(a), cy + r * math.sin(a)
        d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(245, 197, 24))


def sc_ukeu(x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(210, 220, 235))
    w = (x1 - x0) * 0.34
    h = (y1 - y0) * 0.52
    y = y0 + (y1 - y0) * 0.20
    _flag_uk(x0 + (x1 - x0) * 0.10, y, w, h)
    _flag_eu(x1 - (x1 - x0) * 0.10 - w, y, w, h)
    d.line([x0 + (x1 - x0) * 0.47, y + h * 0.5, x0 + (x1 - x0) * 0.53,
            y + h * 0.5], fill=INK, width=3)


def sc_cop31(x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(170, 205, 225))
    cx, cy = x0 + (x1 - x0) * 0.36, y0 + (y1 - y0) * 0.52
    r = (y1 - y0) * 0.36
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(52, 130, 90))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(30, 90, 130), width=2)
    d.polygon([(cx - r * 0.6, cy - r * 0.3), (cx - r * 0.1, cy - r * 0.55),
               (cx + r * 0.05, cy - r * 0.1), (cx - r * 0.4, cy + r * 0.1)],
              fill=(214, 196, 140))
    tx = x1 - (x1 - x0) * 0.22                                # thermometer
    d.rectangle([tx, y0 + 8, tx + 7, y1 - 16], fill=WHITE, outline=INK)
    d.rectangle([tx + 1, y0 + (y1 - y0) * 0.45, tx + 6, y1 - 16], fill=RED)
    d.ellipse([tx - 4, y1 - 22, tx + 11, y1 - 7], fill=RED)
    kx, ky = x0 + (x1 - x0) * 0.70, y0 + (y1 - y0) * 0.30     # overtime clock
    kr = max(9, (y1 - y0) * 0.20)
    d.ellipse([kx - kr, ky - kr, kx + kr, ky + kr], fill=WHITE, outline=INK,
              width=2)
    d.line([kx, ky, kx, ky - kr * 0.72], fill=INK, width=2)
    d.line([kx, ky, kx + kr * 0.55, ky + kr * 0.30], fill=RED, width=2)


def sc_poland(x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(120, 170, 90))
    for i in range(5):
        fy = y0 + (y1 - y0) * (0.25 + i * 0.16)
        d.line([x0, fy, x1, fy - 6], fill=(96, 140, 70), width=3)
    mx0, my0 = x0 + (x1 - x0) * 0.30, y0 + (y1 - y0) * 0.52   # missile
    mx1, my1 = x0 + (x1 - x0) * 0.72, y0 + (y1 - y0) * 0.66
    d.line([mx0, my0, mx1, my1], fill=(90, 94, 100), width=7)
    d.polygon([(mx1, my1), (mx1 + 10, my1 - 5), (mx1 + 10, my1 + 5)], fill=RED)
    for i in range(3):
        sx, sy = mx0 - 6 - i * 7, my0 - 8 - i * 5
        d.ellipse([sx - 4, sy - 3, sx + 4, sy + 3], fill=(200, 200, 195))


def sc_iraq(x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(226, 199, 145))
    d.ellipse([x1 - 44, y0 + 6, x1 - 18, y0 + 32], fill=(240, 190, 60))
    gy = y1 - (y1 - y0) * 0.30
    d.rectangle([x0, gy, x1, y1], fill=(206, 172, 112))
    for fx in (0.22, 0.58):
        vx, vy = x0 + (x1 - x0) * fx, gy - 12
        d.rectangle([vx, vy, vx + 44, vy + 13], fill=(96, 100, 74))
        d.rectangle([vx + 30, vy - 7, vx + 42, vy], fill=(96, 100, 74))
        d.line([vx + 36, vy - 7, vx + 52, vy - 10], fill=(60, 62, 48), width=3)
        for wx in (vx + 8, vx + 34):
            d.ellipse([wx - 5, vy + 9, wx + 5, vy + 19], fill=(40, 40, 36))

def sc_italy(x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(196, 210, 226))
    bw = (x1 - x0) * 0.52
    bx, by = x0 + (x1 - x0) * 0.24, y0 + (y1 - y0) * 0.10
    d.rectangle([bx, by, bx + bw, by + (y1 - y0) * 0.26], fill=RED)
    gy = y1 - (y1 - y0) * 0.34
    d.rectangle([x0, gy + 6, x1, y1], fill=(150, 150, 148))
    for i in range(7):                                         # crowd
        hx = x0 + 12 + i * ((x1 - x0 - 24) / 6.0)
        d.ellipse([hx - 4, gy - 3, hx + 4, gy + 5], fill=(40, 44, 60))
        d.rectangle([hx - 5, gy + 4, hx + 5, gy + 9], fill=(40, 44, 60))


def sc_japan(x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(240, 238, 230))
    base = y1 - 8
    d.line([x0 + 8, base, x1 - 8, base], fill=INK, width=2)
    for i, frac in enumerate((0.34, 0.44, 0.58, 0.78)):
        bx = x0 + (x1 - x0) * (0.16 + i * 0.21)
        bh = (y1 - y0 - 18) * frac
        d.rectangle([bx, base - bh, bx + (x1 - x0) * 0.13, base],
                    fill=(29, 111, 184) if i < 3 else RED)


def sc_seoul(x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(206, 214, 224))
    w = (x1 - x0) * 0.56
    bx, by = x0 + (x1 - x0) * 0.22, y0 + max(8, (y1 - y0) * 0.14)
    d.polygon([(bx - 6, by + 8), (bx + w / 2, by - 6), (bx + w + 6, by + 8)],
              fill=INK)
    d.rectangle([bx, by + 10, bx + w, y1 - 10], fill=(238, 236, 228))
    for i in range(4):
        cx = bx + 8 + i * (w - 16) / 3.0
        d.rectangle([cx - 3, by + 12, cx + 3, y1 - 8], fill=(150, 150, 145))
    d.rectangle([bx - 4, y1 - 12, bx + w + 4, y1 - 6], fill=INK)


def sc_kenya(x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(232, 214, 170))
    gy = y1 - (y1 - y0) * 0.22
    d.rectangle([x0, gy, x1, y1], fill=(198, 158, 100))
    cx = x0 + (x1 - x0) * 0.38
    top = y0 + 6
    d.polygon([(cx - 20, gy), (cx, top), (cx + 20, gy)], outline=INK, width=3)
    d.line([cx - 13, gy - (gy - top) * 0.35, cx + 13, gy - (gy - top) * 0.35],
           fill=INK, width=2)
    d.line([cx - 7, gy - (gy - top) * 0.65, cx + 7, gy - (gy - top) * 0.65],
           fill=INK, width=2)
    px = x1 - (x1 - x0) * 0.30                                 # pumpjack
    d.polygon([(px, gy), (px + 26, gy - 22), (px + 34, gy - 16), (px + 8, gy)],
              fill=(70, 74, 80))
    d.rectangle([px + 2, gy - 4, px + 10, gy], fill=(70, 74, 80))


def sc_bukele(x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(214, 224, 238))
    bw, bh = (x1 - x0) * 0.40, (y1 - y0) * 0.44
    bx, by = x0 + (x1 - x0) * 0.30, y1 - bh - 6
    d.rectangle([bx, by, bx + bw, by + bh], fill=(120, 130, 150))
    d.rectangle([bx + bw * 0.2, by + 6, bx + bw * 0.8, by + 11], fill=INK)
    pw = bw * 0.44
    d.rectangle([bx + bw * 0.28, by - (y1 - y0) * 0.30,
                 bx + bw * 0.28 + pw, by - 4], fill=WHITE, outline=INK)
    d.ellipse([bx + bw * 0.40, by - (y1 - y0) * 0.24,
               bx + bw * 0.52, by - (y1 - y0) * 0.14], fill=RED)


def sc_cricket(x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(110, 168, 92))
    d.rectangle([x0 + (x1 - x0) * 0.30, y0, x0 + (x1 - x0) * 0.70, y1],
                fill=(226, 206, 150))                          # pitch
    sx = x1 - (x1 - x0) * 0.30
    for i in range(3):                                         # stumps
        d.rectangle([sx + i * 7, y0 + (y1 - y0) * 0.30,
                     sx + i * 7 + 3, y0 + (y1 - y0) * 0.72],
                    fill=(240, 220, 120))
    bx, by = x0 + (x1 - x0) * 0.34, y0 + (y1 - y0) * 0.30      # bat
    d.polygon([(bx, by), (bx + 9, by + 4), (bx + 20, by + 34),
               (bx + 11, by + 38)], fill=(196, 150, 90))
    d.ellipse([x0 + (x1 - x0) * 0.52, y0 + (y1 - y0) * 0.18,
               x0 + (x1 - x0) * 0.52 + 10, y0 + (y1 - y0) * 0.18 + 10],
              fill=RED)                                        # ball


def sc_barrage(x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(30, 40, 70))
    w, h = x1 - x0, y1 - y0
    for i, fx in enumerate((0.08, 0.22, 0.38, 0.55, 0.72, 0.88)):
        for j, fy in enumerate((0.22, 0.45, 0.62)):
            px, py = x0 + w * fx + (j % 2) * 5, y0 + h * fy
            d.line([px - 4, py, px + 4, py], fill=(200, 210, 225), width=2)
            d.line([px, py - 3, px, py + 3], fill=(200, 210, 225), width=2)
    for i, fx in enumerate((0.15, 0.48, 0.80)):                 # missile arcs
        sx = x0 + w * fx
        d.arc([sx - 24, y0 + 2 + i * 3, sx + 28, y0 + h * 0.72 + i * 3],
              start=200, end=325, fill=RED, width=2)
        d.ellipse([sx + 22, y0 + h * 0.36 + i * 3, sx + 28,
                   y0 + h * 0.36 + i * 3 + 6], fill=RED)
    gy = y1 - h * 0.16                                         # skyline
    d.rectangle([x0, gy, x1, y1], fill=(14, 20, 36))
    for i, bw in enumerate((0.10, 0.16, 0.12, 0.18, 0.11)):
        bx = x0 + w * (0.04 + i * 0.19)
        d.rectangle([bx, gy - h * (0.10 + (i % 3) * 0.05), bx + w * bw, gy],
                    fill=(14, 20, 36))
    for fx in (0.30, 0.66):                                    # flashes
        ex, ey = x0 + w * fx, gy - 3
        d.ellipse([ex - 5, ey - 4, ex + 5, ey + 4], fill=(245, 180, 60))


def sc_copenhagen(x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(168, 196, 218))
    w, h = x1 - x0, y1 - y0
    gy = y1 - h * 0.34
    for i, (fx, fw, fh) in enumerate(((0.02, 0.22, 0.30), (0.27, 0.18, 0.22),
                                      (0.48, 0.24, 0.36), (0.75, 0.20, 0.26))):
        bx, bw = x0 + w * fx, w * fw
        top = gy - h * fh
        d.rectangle([bx, top, bx + bw, gy], fill=(52, 62, 78))
        d.polygon([(bx - 2, top), (bx + bw / 2, top - h * 0.14),
                   (bx + bw + 2, top)], fill=(122, 62, 48))
    d.rectangle([x0, gy, x1, y1], fill=(96, 104, 112))
    cx, cy = x0 + w * 0.60, y0 + h * 0.36                       # reticle
    r = h * 0.30
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=RED, width=3)
    d.line([cx - r - 6, cy, cx - r * 0.35, cy], fill=RED, width=3)
    d.line([cx + r * 0.35, cy, cx + r + 6, cy], fill=RED, width=3)
    d.line([cx, cy - r - 6, cx, cy - r * 0.35], fill=RED, width=3)
    d.line([cx, cy + r * 0.35, cx, cy + r + 6], fill=RED, width=3)
    d.ellipse([cx - 2, cy - 2, cx + 2, cy + 2], fill=RED)


def sc_cyber(x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(24, 30, 44))
    w, h = x1 - x0, y1 - y0
    cw_, ch_ = w * 0.34, h * 0.52
    for i, (fx, col) in enumerate(((0.05, (70, 110, 170)),
                                   (0.30, (90, 130, 90)),
                                   (0.55, (150, 120, 60)))):
        bx, by = x0 + w * fx, y0 + h * (0.20 + i * 0.07)
        d.rounded_rectangle([bx, by, bx + cw_, by + ch_], radius=5,
                            fill=col, outline=(220, 225, 235), width=1)
        d.rectangle([bx, by + ch_ * 0.24, bx + cw_, by + ch_ * 0.40],
                    fill=(20, 24, 34))
        d.rectangle([bx + cw_ * 0.10, by + ch_ * 0.55,
                     bx + cw_ * 0.26, by + ch_ * 0.78],
                    fill=(225, 200, 110), outline=(120, 100, 40))
    tx, ty = x1 - w * 0.16, y0 + h * 0.16                       # warning sign
    tr = h * 0.30
    d.polygon([(tx, ty), (tx + tr, ty + tr * 0.85), (tx - tr, ty + tr * 0.85)],
              fill=(245, 197, 24), outline=INK, width=2)
    text(tx, ty + tr * 0.28, "!", F(SANSB, max(10, int(tr * 0.62))), INK,
         anchor="ma")


def sc_mongolia(x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(170, 205, 228))
    w, h = x1 - x0, y1 - y0
    d.ellipse([x0 + w * 0.06, y0 + h * 0.08, x0 + w * 0.06 + 22,
               y0 + h * 0.08 + 22], fill=(245, 200, 70))
    gy = y0 + h * 0.58
    d.rectangle([x0, gy, x1, y1], fill=(148, 168, 96))          # steppe
    d.rectangle([x0, gy, x1, gy + 3], fill=(120, 140, 74))
    gx, gw = x0 + w * 0.14, w * 0.30                            # ger tent
    gh = h * 0.34
    d.polygon([(gx, gy), (gx + gw * 0.5, gy - gh), (gx + gw, gy)],
              fill=(240, 238, 230))
    d.rectangle([gx + gw * 0.42, gy - gh * 0.34, gx + gw * 0.58, gy],
                fill=(150, 84, 52))
    d.line([gx + gw * 0.5, gy - gh, gx + gw * 0.5, gy - gh - 5],
           fill=(90, 70, 50), width=2)
    px = x0 + w * 0.66                                          # flag
    d.line([px, gy, px, gy - h * 0.62], fill=(70, 60, 50), width=3)
    fw, fh = w * 0.20, h * 0.26
    d.rectangle([px, gy - h * 0.62, px + fw, gy - h * 0.62 + fh],
                fill=(40, 90, 160))
    d.rectangle([px, gy - h * 0.62, px + fw * 0.36, gy - h * 0.62 + fh],
                fill=RED)


def sc_chips(x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(16, 26, 48))
    w, h = x1 - x0, y1 - y0
    for fx in (0.10, 0.90):                                     # traces
        for fy in (0.25, 0.50, 0.75):
            px, py = x0 + w * fx, y0 + h * fy
            d.line([x0 + w * 0.30 if fx < 0.5 else x0 + w * 0.70, py,
                    px, py], fill=(60, 120, 170), width=2)
            d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=(120, 200, 240))
    cw_, ch_ = w * 0.40, h * 0.62                               # the chip
    bx, by = x0 + w * 0.30, y0 + h * 0.19
    for i in range(4):                                          # pins
        py = by + ch_ * (0.15 + i * 0.23)
        d.rectangle([bx - 7, py, bx, py + 3], fill=(200, 205, 215))
        d.rectangle([bx + cw_, py, bx + cw_ + 7, py + 3],
                    fill=(200, 205, 215))
    d.rectangle([bx, by, bx + cw_, by + ch_], fill=(36, 48, 74),
                outline=(140, 190, 230), width=2)
    iw, ih = cw_ * 0.52, ch_ * 0.52
    d.rectangle([bx + (cw_ - iw) / 2, by + (ch_ - ih) / 2,
                 bx + (cw_ + iw) / 2, by + (ch_ + ih) / 2],
                fill=(52, 130, 190))
    text(bx + cw_ / 2, by + ch_ * 0.40, "AI", F(SANSB, 13), WHITE,
         anchor="ma")


def sc_riyadh(x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(24, 30, 58))
    w, h = x1 - x0, y1 - y0
    for i, fx in enumerate((0.16, 0.50, 0.84)):                 # trails
        sx, sy = x0 + w * fx, y0 + h * 0.62
        d.arc([sx - 26, y0 + 2, sx + 26, y0 + h * 0.80],
              start=200, end=330, fill=(200, 120, 90), width=2)
        ex, ey = sx + 20, y0 + h * (0.30 + i * 0.05)            # burst
        for a in range(0, 360, 45):
            import math
            dx, dy = math.cos(math.radians(a)), math.sin(math.radians(a))
            d.line([ex, ey, ex + dx * 8, ey + dy * 8],
                   fill=(250, 200, 90), width=2)
        d.ellipse([ex - 2, ey - 2, ex + 2, ey + 2], fill=(255, 230, 150))
    gy = y1 - h * 0.18                                          # skyline
    d.rectangle([x0, gy, x1, y1], fill=(10, 14, 26))
    for i, bw in enumerate((0.12, 0.18, 0.10, 0.16, 0.12)):
        bx = x0 + w * (0.03 + i * 0.19)
        d.rectangle([bx, gy - h * (0.08 + (i % 3) * 0.05),
                     bx + w * bw, gy], fill=(10, 14, 26))


def sc_mercury(x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(8, 10, 20))
    w, h = x1 - x0, y1 - y0
    for i, (fx, fy) in enumerate(((0.08, 0.2), (0.2, 0.65), (0.35, 0.12),
                                  (0.55, 0.75), (0.68, 0.15), (0.88, 0.6),
                                  (0.45, 0.4), (0.12, 0.85))):  # stars
        px, py = x0 + w * fx, y0 + h * fy
        d.ellipse([px - 1, py - 1, px + 1, py + 1], fill=(220, 228, 245))
    pr = h * 0.44                                               # Mercury
    cx, cy = x1 - w * 0.26, y0 + h * 0.52
    d.ellipse([cx - pr, cy - pr, cx + pr, cy + pr], fill=(216, 150, 92))
    d.ellipse([cx - pr * 0.55, cy - pr * 0.3, cx - pr * 0.2,
               cy + pr * 0.05], fill=(190, 124, 74))
    d.ellipse([cx + pr * 0.15, cy + pr * 0.3, cx + pr * 0.5,
               cy + pr * 0.6], fill=(198, 134, 80))
    sx, sy = x0 + w * 0.16, y0 + h * 0.30                       # spacecraft
    d.rectangle([sx, sy, sx + 16, sy + 9], fill=(210, 214, 222))
    d.rectangle([sx - 13, sy + 1, sx - 2, sy + 8], fill=(52, 110, 180))
    d.rectangle([sx + 18, sy + 1, sx + 29, sy + 8], fill=(52, 110, 180))
    d.arc([sx - 6, sy - 8, cx - pr * 0.6, cy + pr * 0.9],
          start=300, end=60, fill=(150, 170, 200), width=1)


def sc_tanker(x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(168, 200, 222))
    w, h = x1 - x0, y1 - y0
    d.ellipse([x0 + w * 0.06, y0 + h * 0.08, x0 + w * 0.06 + 20,
               y0 + h * 0.08 + 20], fill=(245, 200, 70))
    sy = y0 + h * 0.42                                          # sea
    d.rectangle([x0, sy, x1, y1], fill=(44, 96, 140))
    for i in range(4):
        wy = sy + 6 + i * (h * 0.13)
        d.line([x0 + w * (0.05 + i * 0.07), wy, x0 + w * (0.30 + i * 0.07),
                wy], fill=(120, 175, 205), width=2)
    hx, hy = x0 + w * 0.10, sy - h * 0.10                       # tanker
    hw = w * 0.80
    d.polygon([(hx, hy), (hx + hw, hy), (hx + hw - 14, hy + h * 0.16),
               (hx + 8, hy + h * 0.16)], fill=(150, 52, 40))
    d.rectangle([hx + 6, hy - 5, hx + hw - 6, hy], fill=(60, 64, 70))
    for i, col in enumerate(((52, 110, 170), (202, 111, 30),
                             (40, 130, 90), (52, 110, 170))):
        cx = hx + hw * 0.10 + i * hw * 0.17
        d.rectangle([cx, hy - 15, cx + hw * 0.14, hy - 5], fill=col)
    d.rectangle([hx + hw * 0.82, hy - 24, hx + hw * 0.90, hy - 5],
                fill=(235, 235, 230))
    d.rectangle([hx + hw * 0.845, hy - 30, hx + hw * 0.875, hy - 24],
                fill=(90, 94, 100))


SCENES = {"kyiv": sc_kyiv, "akvan": sc_akvan, "markets": sc_markets,
          "ukeu": sc_ukeu, "cop31": sc_cop31, "poland": sc_poland,
          "iraq": sc_iraq, "italy": sc_italy, "japan": sc_japan,
          "seoul": sc_seoul, "kenya": sc_kenya, "bukele": sc_bukele,
          "cricket": sc_cricket, "barrage": sc_barrage,
          "copenhagen": sc_copenhagen, "cyber": sc_cyber,
          "mongolia": sc_mongolia, "chips": sc_chips,
          "riyadh": sc_riyadh, "mercury": sc_mercury,
          "tanker": sc_tanker}


def draw_strip(card, x, y, w, h, band_h, tag_size, label_size):
    """Illustrated strip: scene + region top rule + source tag top-right,
    data label bottom-left, navy caption band along the bottom edge."""
    (no, place, region, topic, head, deck, srctag, label, caption,
     lon, lat, scene) = card
    d.rectangle([x, y, x + w, y + h], fill=CARD_BG)
    SCENES[scene](x, y, x + w, y + h - band_h)
    d.rectangle([x, y, x + w, y + 4], fill=REGION_RGB[region])
    tagw = tw(srctag, F(SANSB, tag_size)) + 8
    d.rectangle([x + w - tagw - 3, y + 6, x + w - 3,
                 y + 6 + tag_size + 6], fill=NAVY)
    text(x + w - 3, y + 8, srctag, F(SANSB, tag_size), WHITE, anchor="ra")
    label_size = fit_size(label, SANSB, label_size, w - 24, floor=7)
    labw = tw(label, F(SANSB, label_size)) + 10
    d.rectangle([x + 4, y + h - band_h - label_size - 10,
                 x + 4 + labw, y + h - band_h - 3], fill=WHITE)
    text(x + 9, y + h - band_h - label_size - 8, label,
         F(SANSB, label_size), INK)
    d.rectangle([x, y + h - band_h, x + w, y + h], fill=NAVY)
    cap = caption
    cs = band_h - 5
    while cs > 7 and tw(cap, F(SANSB, cs)) > w - 10:
        cs -= 1
    text(x + w / 2, y + h - band_h + 2, cap, F(SANSB, cs), WHITE,
         anchor="ma")


def draw_lead(card, x, y, w):
    (no, place, region, topic, head, deck, srctag, label, caption,
     lon, lat, scene) = card
    d.rectangle([x, y, x + w, y + 224], fill=CARD_BG, outline=FAINT)
    draw_strip(card, x, y, w, 96, 15, 9, 12)
    ry = y + 102
    text(x + 8, ry, "%d %s - %s - %s" % (no, place, region, topic),
         F(SANSB, 11), REGION_RGB[region])
    hy = ry + 16
    for ln in wrap(head, F(SERIF, 22), w - 16, 2):
        text(x + 8, hy, ln, F(SERIF, 22), INK)
        hy += 25
    dy = hy + 2
    for ln in wrap(deck, F(SANSM, 12), w - 16, 4):
        text(x + 8, dy, ln, F(SANSM, 12), INK)
        dy += 13


def draw_feature(card, x, y, w):
    (no, place, region, topic, head, deck, srctag, label, caption,
     lon, lat, scene) = card
    d.rectangle([x, y, x + w, y + 123], fill=CARD_BG, outline=FAINT)
    draw_strip(card, x, y, w, 46, 12, 7, 9)
    ry = y + 50
    text(x + 5, ry, "%d %s - %s" % (no, place, region),
         F(SANSB, 9), REGION_RGB[region])
    hy = ry + 12
    for ln in wrap(head, F(SANSB, 12), w - 10, 2):
        text(x + 5, hy, ln, F(SANSB, 12), INK)
        hy += 13
    dy = hy + 1
    for ln in wrap(deck, F(SANSM, 10), w - 10, 3):
        text(x + 5, dy, ln, F(SANSM, 10), INK)
        dy += 11

# --------------------------------------------------------------------- map
def draw_map(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=NAVY)
    text(x + 8, y + 6, "WHERE IT HAPPENED", F(SANSB, 11), WHITE)
    mx0, my0 = x + 6, y + 26
    mw = w - 12
    scale = mw / 360.0
    mh = 140 * scale

    def proj(lon, lat):
        return (mx0 + (lon + 180) * scale, my0 + (82 - lat) * scale)

    for rings in WORLD.values():
        for ring in rings.split("|"):
            pts = []
            for pair in ring.split(","):
                lo, la = pair.split(":")
                pts.append(proj(float(lo), float(la)))
            if len(pts) > 2:
                d.polygon(pts, fill=LAND)
    for (no, txt, region, lon, lat) in BRIEFS:
        if lon is None:
            continue
        px, py = proj(lon, lat)
        d.ellipse([px - 2.5, py - 2.5, px + 2.5, py + 2.5],
                  fill=REGION_RGB[region])
    for card in CARDS:
        (no, place, region, topic, head, deck, srctag, label, caption,
         lon, lat, scene) = card
        if lon is None:
            continue  # card 10 is in space: Mercury has no map pin
        px, py = proj(lon, lat)
        d.ellipse([px - 9, py - 9, px + 9, py + 9],
                  fill=REGION_RGB[region], outline=WHITE, width=1)
        text(px, py - 6, str(no), F(SANSB, 10), WHITE, anchor="ma")
    ly = y + h - 24
    for ln in wrap("Numbered pins = the 12 pictured stories on Earth - "
                   "No. 10 is in space: Mercury - small dots = the briefs",
                   F(SANSM, 9), w - 16, 2):
        text(x + 8, ly, ln, F(SANSM, 9), (200, 208, 220))
        ly += 11


def draw_also_on(x, y, w, h):
    text(x, y, "ALSO ON SATURDAY 21 NOVEMBER - 25 MORE STORIES",
         F(SANSB, 12), RED)
    colw = (w - 12) / 2.0
    # split the briefs so both columns carry about the same line count
    def nlines(b):
        num = "%d " % b[0]
        return len(wrap(b[1], F(SANSM, 10),
                        colw - tw(num, F(SANSB, 10)), 2))
    total = sum(nlines(b) for b in BRIEFS)
    cols, acc = [[], []], 0
    for b in BRIEFS:
        if acc + nlines(b) <= total / 2.0 or not cols[0]:
            cols[0].append(b)
            acc += nlines(b)
        else:
            cols[1].append(b)
    for ci, col in enumerate(cols):
        cx = x + ci * (colw + 12)
        cy = y + 18
        for (no, txt, region, lon, lat) in col:
            num = "%d " % no
            text(cx, cy, num, F(SANSB, 10), REGION_RGB[region])
            off = tw(num, F(SANSB, 10))
            lines = wrap(txt, F(SANSM, 10), colw - off, 2)
            for j, ln in enumerate(lines):
                text(cx + off, cy + j * 11.5, ln, F(SANSM, 10), INK)
            cy += max(1, len(lines)) * 11.5


def draw_bottom(y):
    draw_map(MX, y, 290, 232)
    draw_also_on(MX + 304, y, CW - 304, 232)
    return y + 240


def draw_date_check(y):
    d.rectangle([MX, y, W - MX, y + 36], outline=RED, width=2)
    text(MX + 8, y + 3, "DATE CHECK", F(SANSB, 10), RED)
    off = tw("DATE CHECK ", F(SANSB, 10)) + 6
    lines = wrap(DATE_CHECK, F(SANSM, 9), CW - 16 - off, 3)
    for j, ln in enumerate(lines):
        text(MX + 8 + (off if j == 0 else 0), y + 3 + j * 10.5, ln,
             F(SANSM, 9), INK)
    return y + 40


def draw_footer(y):
    d.line([MX, y, W - MX, y], fill=INK, width=1)
    text(MX, y + 3, FOOTER_L, F(SANSM, 9), GREY)
    text(W - MX, y + 3, FOOTER_R, F(SANSM, 9), GREY, anchor="ra")


# -------------------------------------------------------------------- main
def main():
    y = draw_header()                       # ends at 242
    lead_w = (CW - 16) / 3.0
    for i, card in enumerate(CARDS[:3]):
        draw_lead(card, MX + i * (lead_w + 8), y + 2, lead_w)
    gy = y + 232
    feat_w = (CW - 32) / 5.0
    for r in range(2):
        for c in range(5):
            draw_feature(CARDS[3 + r * 5 + c],
                         MX + c * (feat_w + 8), gy + r * 126, feat_w)
    by = gy + 2 * 126 + 4
    by = draw_bottom(by)
    by = draw_date_check(by)
    draw_footer(by)
    # Palette-quantize the flat illustration: same page, far fewer bytes
    # (the dev board breaks score ties on smaller files).
    q = img.quantize(colors=256, method=Image.MEDIANCUT,
                     dither=Image.NONE)
    q.save(OUT, optimize=True)
    img.resize((300, 300), Image.LANCZOS).save(
        os.path.join(HERE, "entry-300.png"), optimize=True)
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
