#!/usr/bin/env python3
"""The Meridian Wire — NI21 round 5. Local renderer (Pillow only).

Structure copied from the pixel-measured dissection of NI21 #1 (giggs18):
date-only masthead, three equal leads, 10 mini cards, uniform 64px scenes,
black location bars, red circle badges, CONFIRMED/REPORTED chips, dot-matrix
map, hard one-line briefs, DATE CHECK with an Unverified clause.
All stories/numbers come ONLY from POOL21 (21 Nov 2026).
"""
import os, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, str(Path(__file__).resolve().parent))
from mapdata import WORLD

HERE = Path(__file__).resolve().parent
W = H = 1024
PAPER = (245, 241, 224); INK = (18, 18, 18); RED = (192, 40, 25)
DARKRED = (150, 28, 18); GREY = (90, 86, 76); LGREY = (214, 208, 188)
WHITE = (255, 255, 255); BLACK = (10, 10, 10)

def F(name, size):
    return ImageFont.truetype(str(HERE / "fonts" / name), size)
SERIF = lambda s: F("PlayfairDisplay-900.ttf", s)
BOLD = lambda s: F("Archivo-Bold.ttf", s)
MED = lambda s: F("Archivo-Medium.ttf", s)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

def tw(text, font):
    return d.textlength(text, font=font)

def fit(text, font, maxw):
    if tw(text, font) <= maxw: return text
    while text and tw(text + "…", font) > maxw: text = text[:-1]
    return text.rstrip() + "…"

def wrap(text, font, maxw, maxlines):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if tw(t, font) <= maxw: cur = t
        else:
            if cur: lines.append(cur)
            cur = w_
            if len(lines) == maxlines: break
    if cur and len(lines) < maxlines: lines.append(cur)
    return lines

# ---------------------------------------------------------------- data (POOL21)
# num, place, region, category, slug, chip, headline, deck, lon, lat, scene
CARDS = [
 (1,"WARSAW, POLAND","EUROPE","DIPLOMACY","3 WEAPONS CROSS","CONFIRMED – AP",
  "Rutte flies to Warsaw after missiles land",
  "Two missiles and a suspected jet drone came down in the south-east, a Kh-101 near Nowy Lipowiec. Rutte calls it a “grave violation”; Tusk a deliberate provocation.",
  21.0,52.2,"missile"),
 (2,"ANTALYA, TÜRKIYE","GLOBAL","CLIMATE","NO DEAL YET","REPORTED – AP",
  "COP31 runs into overtime, no deal yet",
  "Talks ran past Friday's scheduled close into Saturday. The draft drops every fossil-fuel reference and the $120bn finance target; a third draft is due this morning.",
  30.7,36.9,"sun"),
 (3,"NEW YORK, USA","AMERICAS","MARKETS","NASDAQ −5.28%","REPORTED – SIMPLELIFE",
  "Wall Street enters correction in AI rout",
  "The S&P 500 fell about 3.7% on Friday, pushing it into correction territory. The Nasdaq dropped 5.28% as chip and AI shares plunged.",
  -74.0,40.7,"chart"),
 (4,"KRYVYI RIH, UKRAINE","EUROPE","CONFLICT","42 INJURED","REPORTED – APPISTOS",
  "Russian strike kills two, injures 42",
  "An overnight strike kills two and injures 42, four of them children, the city's military chief says.",
  33.4,47.9,"blast"),
 (5,"COPENHAGEN, DENMARK","EUROPE","SECURITY","ATTACHÉ OUT","CONFIRMED – BBC",
  "Denmark exposes 'assassination plot'",
  "Denmark says Russia planned to kill a Ukrainian-American rapper near Copenhagen. The attaché is expelled.",
  12.6,55.7,"eye"),
 (6,"KYIV, UKRAINE","EUROPE","CONFLICT","400 DRONES","CONFIRMED – BBC",
  "Russia's barrage: 400 drones, 110 missiles",
  "At least eight are dead across Ukraine in the overnight barrage. The Austrian embassy is hit in Kyiv.",
  30.5,50.4,"drones"),
 (7,"ODISHA, INDIA","ASIA","STORM","372,000","REPORTED – RIDHU TIMES",
  "After Akvan: 372,000 moved, no deaths",
  "A day after landfall, no deaths are reported and relief is under way. Schools stay shut through Saturday.",
  84.9,19.3,"cyclone"),
 (8,"BRUSSELS, BELGIUM","EUROPE","DEFENCE","€1BN AID","CONFIRMED – REUTERS",
  "EU adopts €1bn military aid for Ukraine",
  "Joint buying runs via the Peace Facility. Britain pledges 1,000+ drones in a £260m package alongside.",
  4.3,50.8,"coin"),
 (9,"NEW YORK, USA","AMERICAS","FINANCE","3 NETWORKS","REPORTED – REUTERS",
  "JPMorgan, Visa, Mastercard hit by attack",
  "The banks report cyber incidents at third-party vendors. Their core payment networks are unaffected.",
  -73.9,40.8,"shield"),
 (10,"ULAANBAATAR, MONGOLIA","ASIA","POLITICS","SNAP ELECTION","REPORTED – REUTERS",
  "Mongolia's president resigns",
  "The resignation sets the stage for a snap election. It caps a week of political turmoil in the capital.",
  106.9,47.9,"flag"),
 (11,"THE HAGUE, NETHERLANDS","GLOBAL","COURTS","VERDICT","REPORTED – BBC",
  "Myanmar ruling rattles Israel's defence",
  "The world court's genocide verdict against Myanmar raises questions in Jerusalem over its own case, experts say.",
  4.3,52.1,"scales"),
 (12,"JOHANNESBURG, SOUTH AFRICA","AFRICA","POLITICS","ANC 31%","CONFIRMED – BBC",
  "ANC scrambles after worst result since 1994",
  "The ANC wins 31% of the vote, its worst since 1994. It now races for coalition deals to stay in government.",
  28.0,-26.2,"ballot"),
 (13,"WELLINGTON, NEW ZEALAND","OCEANIA","CRICKET","159/1 · DAY TWO","CONFIRMED – ICC",
  "India fight back: 159/1 at stumps, day two",
  "India trail New Zealand by 209 in the first Test after the hosts made 368. Nicholls made 175 not out.",
  174.8,-41.3,"cricket"),
]
BRIEFS = [
 ("Kathmandu:","Nepal's new leader Balendra Shah faces an India test"),
 ("Washington:","US releases more UFO footage filmed in the Middle East"),
 ("Los Angeles:","Hyundai unveils the 2027 Elantra at the auto show"),
 ("Cardiff:","Lauren Price beats Kotaskova, undisputed champion"),
 ("Paris:","Three police sentenced over beating of Michel Zecler"),
 ("Oxford:","Life, 22 years minimum, for Thames drowning murder"),
 ("New York:","Nikhil Gupta gets 19+ years over Sikh murder plot"),
 ("Cincinnati:","Fiona the hippo dies after eating a hat"),
 ("Washington:","US sanctions four Iranians over oil revenues"),
 ("Hormuz:","A tanker is struck and on fire in the strait"),
 ("Los Angeles:","Jury convicts man who started Palisades Fire"),
 ("Frankfurt:","ECB names Boone and Brunnermeier for its board"),
 ("Buenos Aires:","Senate backs disability framework, 71–0"),
 ("Riyadh:","Saudi coalition intercepts Houthi missiles"),
 ("Barcelona:","Pill hailed as pancreatic-cancer breakthrough"),
 ("Gaza:","Palestinian children appeal for help on Children's Day"),
 ("Madrid:","Amnesty: Spanish police used excess force in strike"),
 ("Rome:","Workers and students march against Meloni government"),
 ("Jeddah:","Saudi Arabia warns of thunderstorms through Tuesday"),
 ("Kuala Lumpur:","Malaysia to send 10,000 Rohingya to Turkey"),
 ("Kharkiv:","Ukraine says it has finished a “Bear Trap” there"),
 ("Islamabad:","Pakistan minerals worth $8–10 trillion, minister says"),
 ("Singapore:","US presses Singapore, Malaysia on Iran sanctions"),
 ("Paris:","France seeks UN council meeting on Kyiv strikes"),
 ("Kyiv:","War tally: 771 Ukrainians killed, 2,300+ missing"),
 ("Ankara:","Turkey welcomes World Court's Myanmar ruling"),
 ("Turin:","ATP semis set: Alcaraz–Shelton, Zverev–Medvedev"),
]
DAYPARTS = [
 ("OVERNIGHT","Kryvyi Rih strike: two killed, 42 injured"),
 ("MORNING","Rutte flies to Warsaw over the missiles"),
 ("MIDDAY","Antalya: third COP31 draft due after talks"),
 ("AFTERNOON","Denmark expels the Russian attaché"),
 ("EVENING","Stumps in Wellington: India 159/1"),
]

# ---------------------------------------------------------------- scenes
SKY = (250,222,175); NAVY=(14,31,52); BLUE=(135,180,220); SAND=(242,210,150)
GREEN=(130,185,120); TEAL=(120,190,190); ORANGE=(240,140,50); YELL=(250,205,70)
def scene(kind, x, y, w, h=64):
    cx, cy = x+w//2, y+h//2
    if kind=="missile":
        d.rectangle([x,y,x+w,y+h], fill=SKY)
        d.rectangle([x,y+h-12,x+w,y+h], fill=GREEN)
        d.polygon([(x+w*0.18,y+h*0.78),(x+w*0.62,y+h*0.16),(x+w*0.72,y+h*0.26),(x+w*0.28,y+h*0.88)], fill=(200,200,205))
        d.polygon([(x+w*0.62,y+h*0.16),(x+w*0.80,y+h*0.10),(x+w*0.72,y+h*0.26)], fill=RED)
        d.polygon([(x+w*0.18,y+h*0.78),(x+w*0.06,y+h*0.92),(x+w*0.28,y+h*0.88)], fill=ORANGE)
    elif kind=="sun":
        d.rectangle([x,y,x+w,y+h], fill=(252,232,185))
        d.ellipse([cx-26,y+6,cx+26,y+58], fill=ORANGE)
        d.rectangle([x,y+h-14,x+w,y+h], fill=TEAL)
        d.polygon([(x+8,y+h-14),(x+34,y+h-34),(x+60,y+h-14)], fill=(60,120,70))
        d.polygon([(x+w-60,y+h-14),(x+w-34,y+h-30),(x+w-8,y+h-14)], fill=(60,120,70))
    elif kind=="chart":
        d.rectangle([x,y,x+w,y+h], fill=NAVY)
        pts=[(x+10,y+12),(x+w*0.32,y+20),(x+w*0.52,y+16),(x+w*0.72,y+34),(x+w-12,y+52)]
        d.line(pts, fill=(255,90,70), width=6)
        for px,py in pts: d.ellipse([px-4,py-4,px+4,py+4], fill=YELL)
        d.polygon([(x+w-12,y+52),(x+w-26,y+50),(x+w-14,y+38)], fill=(255,90,70))
    elif kind=="blast":
        d.rectangle([x,y,x+w,y+h], fill=(70,80,105))
        d.rectangle([x,y+h-16,x+w,y+h], fill=(45,45,55))
        for bx,bw_ in [(0.08,0.20),(0.36,0.16),(0.60,0.22),(0.86,0.12)]:
            d.rectangle([x+w*bx,y+h-16-26,x+w*(bx+bw_),y+h-16], fill=(30,30,40))
        d.ellipse([cx-24,y+2,cx+24,y+50], fill=ORANGE)
        d.ellipse([cx-14,y+10,cx+14,y+44], fill=YELL)
    elif kind=="eye":
        d.rectangle([x,y,x+w,y+h], fill=(170,215,240))
        d.ellipse([cx-52,y+8,cx+52,y+56], fill=WHITE)
        d.ellipse([cx-20,y+14,cx+20,y+50], fill=NAVY)
        d.ellipse([cx-7,y+24,cx+7,y+38], fill=WHITE)
        d.polygon([(x+6,y+h-4),(cx,y+16),(x+w-6,y+h-4)], outline=(60,90,120))
    elif kind=="drones":
        d.rectangle([x,y,x+w,y+h], fill=NAVY)
        for dx,dy,s in [(0.22,0.42,1.0),(0.52,0.30,1.25),(0.80,0.48,0.9)]:
            px,py=x+w*dx,y+h*dy
            d.rectangle([px-16*s,py-4*s,px+16*s,py+4*s], fill=(200,205,215))
            d.ellipse([px-20*s,py-9*s,px-8*s,py-3*s], outline=YELL, width=2)
            d.ellipse([px+8*s,py-9*s,px+20*s,py-3*s], outline=YELL, width=2)
        d.rectangle([x,y+h-10,x+w,y+h], fill=(30,50,35))
    elif kind=="cyclone":
        d.rectangle([x,y,x+w,y+h], fill=BLUE)
        for r,col in [(26,WHITE),(19,BLUE),(12,WHITE),(6,NAVY)]:
            d.ellipse([cx-r,y+32-r,cx+r,y+32+r], outline=col, width=5)
        d.rectangle([x,y+h-12,x+w,y+h], fill=SAND)
    elif kind=="coin":
        d.rectangle([x,y,x+w,y+h], fill=(170,215,170))
        d.ellipse([cx-27,y+5,cx+27,y+59], fill=YELL, outline=(190,150,20), width=3)
        d.text((cx,cy), "€", font=SERIF(38), fill=(120,90,0), anchor="mm")
        d.polygon([(x+8,y+h-6),(x+26,y+h-30),(x+44,y+h-6)], fill=(90,140,90))
        d.polygon([(x+w-44,y+h-6),(x+w-26,y+h-30),(x+w-8,y+h-6)], fill=(90,140,90))
    elif kind=="shield":
        d.rectangle([x,y,x+w,y+h], fill=(200,220,245))
        d.polygon([(cx, y+4),(cx+30,y+12),(cx+30,y+32),(cx,y+60),(cx-30,y+32),(cx-30,y+12)], fill=BLUE, outline=NAVY)
        d.rectangle([cx-13,cy-8,cx+13,cy+12], fill=WHITE)
        d.rectangle([cx-13,cy-8,cx+13,cy-2], fill=RED)
    elif kind=="flag":
        d.rectangle([x,y,x+w,y+h], fill=(250,230,180))
        d.rectangle([cx-3,y+6,cx+3,y+60], fill=(90,70,50))
        d.polygon([(cx+3,y+8),(cx+52,y+16),(cx+3,y+28)], fill=RED)
        d.rectangle([x,y+h-10,x+w,y+h], fill=GREEN)
    elif kind=="scales":
        d.rectangle([x,y,x+w,y+h], fill=(225,215,190))
        d.rectangle([cx-3,y+6,cx+3,y+56], fill=(120,90,30))
        d.line([cx-38,y+14,cx+38,y+14], fill=(120,90,30), width=5)
        d.polygon([(cx-38,y+14),(cx-50,y+38),(cx-26,y+38)], outline=(120,90,30), width=3)
        d.polygon([(cx+38,y+14),(cx+26,y+38),(cx+50,y+38)], outline=(120,90,30), width=3)
        d.rectangle([cx-16,y+56,cx+16,y+60], fill=(120,90,30))
    elif kind=="ballot":
        d.rectangle([x,y,x+w,y+h], fill=(252,230,175))
        d.rectangle([cx-36,y+22,cx+36,y+58], fill=WHITE, outline=INK, width=3)
        d.rectangle([cx-20,y+18,cx+20,y+26], fill=BLACK)
        d.rectangle([cx-30,y+8,cx+2,y+24], fill=WHITE, outline=INK, width=2)
        d.line([cx-24,y+16,cx-16,y+21], fill=RED, width=3); d.line([cx-16,y+21,cx-6,y+11], fill=RED, width=3)
    elif kind=="cricket":
        d.rectangle([x,y,x+w,y+h], fill=GREEN)
        d.rectangle([cx-10,y+4,cx+10,y+60], fill=(232,205,150))
        d.line([cx-34,y+54,cx+6,y+18], fill=(140,95,45), width=7)
        d.ellipse([cx+22,y+8,cx+44,y+30], fill=RED)
        for sx in (-26,0,26): d.rectangle([cx+sx-2,y+8,cx+sx+2,y+26], fill=WHITE)
    d.rectangle([x,y,x+w-1,y+h-1], outline=(120,115,95))

def card(c, x, y, w, lead=False):
    num, place, region, cat, slug, chip, head, deck, lon, lat, kind = c
    scene(kind, x, y, w)
    # slug box top-left inside scene (smaller on minis so slug+chip never collide)
    sf = BOLD(12 if lead else 10)
    sw = tw(slug, sf) + 10
    d.rectangle([x+4, y+4, x+4+sw, y+(21 if lead else 19)], fill=BLACK)
    d.text((x+9, y+6), slug, font=sf, fill=WHITE)
    # chip top-right
    cf = BOLD(10 if lead else 8)
    cw = tw(chip, cf) + 8
    d.rectangle([x+w-4-cw, y+4, x+w-4, y+(20 if lead else 18)], fill=WHITE, outline=BLACK, width=1)
    d.text((x+w-4-cw+4, y+6), chip, font=cf, fill=INK)
    # black location bar
    by = y + 64
    d.rectangle([x, by, x+w, by+20], fill=BLACK)
    lf = BOLD(12)
    d.text((x+6, by+4), fit(place, lf, w-12), font=lf, fill=WHITE)
    # badge row
    ry = by + 24
    d.ellipse([x, ry, x+20, ry+20], fill=RED)
    d.text((x+10, ry+10), str(num), font=BOLD(12), fill=WHITE, anchor="mm")
    rf = BOLD(12 if lead else 11)
    d.text((x+26, ry+3), fit(f"{region} · {cat}", rf, w-26), font=rf, fill=RED)
    # headline
    hy = ry + 24
    if lead:
        size = 20
        while size > 15 and tw(head, SERIF(size)) > w: size -= 1
        hf = SERIF(size)
        d.text((x, hy), fit(head, hf, w), font=hf, fill=INK)
        hy += 24
        df = MED(12)
        for ln in wrap(deck, df, w, 3):
            d.text((x, hy), ln, font=df, fill=(45,43,38)); hy += 14
    else:
        hf = SERIF(15)
        for ln in wrap(head, hf, w, 2):
            d.text((x, hy), ln, font=hf, fill=INK); hy += 16
        df = MED(11)
        for ln in wrap(deck, df, w, 3):
            d.text((x, hy), ln, font=df, fill=(45,43,38)); hy += 11

# ---------------------------------------------------------------- claims bar
d.text((14, 7), "THE MERIDIAN WIRE", font=BOLD(13), fill=RED)
claims = "40 STORIES · 13 DRAWN · 6 CONTINENTS · ALL FROM 21 NOVEMBER"
cf = BOLD(12)
d.text((1010 - tw(claims, cf), 7), claims, font=cf, fill=INK)
d.rectangle([0, 29, W, 31], fill=RED)

# ---------------------------------------------------------------- masthead = date
mf = SERIF(74)
title = "Saturday 21 November 2026"
d.text(((W - tw(title, mf)) / 2, 30), title, font=mf, fill=INK)

# ---------------------------------------------------------------- day parts
py = 126
d.rectangle([14, py, 118, py+52], fill=RED)
d.text((24, py+8), "THE DAY", font=BOLD(13), fill=WHITE)
d.text((24, py+26), "IN PARTS", font=BOLD(13), fill=WHITE)
sx = 126; segw = (1010 - sx) / 5
for i, (lab, head) in enumerate(DAYPARTS):
    x0 = sx + i * segw
    if i: d.line([x0, py+4, x0, py+52], fill=LGREY, width=1)
    d.text((x0+8, py+2), lab, font=BOLD(11), fill=RED)
    for j, ln in enumerate(wrap(head, MED(11), segw-14, 3)):
        d.text((x0+8, py+19+j*12), ln, font=MED(11), fill=INK)
d.line([14, py+54, 1010, py+54], fill=LGREY, width=1)

# ---------------------------------------------------------------- cards
for i, c in enumerate(CARDS[:3]):
    card(c, 14 + i * 335, 186, 327, lead=True)
for r in range(2):
    for i in range(5):
        card(CARDS[3 + r*5 + i], 14 + i * 201, 378 + r * 178, 193)

# ---------------------------------------------------------------- bottom header
by = 744
d.text((14, by), "WHERE IT HAPPENED", font=BOLD(14), fill=INK)
rh = "ALSO ON SATURDAY 21 NOVEMBER"
d.text((1010 - tw(rh, BOLD(14)), by), rh, font=BOLD(14), fill=INK)
d.line([14, by+20, 1010, by+20], fill=RED, width=2)

# ---------------------------------------------------------------- dot-matrix map
MX, MY, MW, MH = 14, 766, 396, 138
def inpoly(lon, lat, ring):
    pts = [(float(a), float(b)) for a, b in (p.split(":") for p in ring.split(","))]
    inside = False; n = len(pts)
    for i in range(n):
        x1, y1 = pts[i]; x2, y2 = pts[(i+1) % n]
        if (y1 > lat) != (y2 > lat):
            if lon < (x2-x1) * (lat-y1) / (y2-y1) + x1: inside = not inside
    return inside
def onland(lon, lat):
    for rings in WORLD.values():
        for ring in rings.split("|"):
            if inpoly(lon, lat, ring): return True
    return False
CONT = [("EUROPE",(70,120,190)),("ASIA",(225,140,40)),("AMERICAS",(80,160,90)),
        ("MIDEAST",(170,80,160)),("AFRICA",(215,175,60)),("OCEANIA",(60,170,180))]
def continent(lon, lat):
    if lat < -10 and lon > 110: return 5
    if lon < -30: return 2
    if -17 < lon < 52 and -35 < lat < 37: return 4 if (lon > 34 and lat > 12) else 3
    if lon >= 52 or (lon > 34 and lat >= 37) or (lon > 44): return 1
    if -12 <= lon <= 45 and lat >= 37: return 0
    if lon > 45: return 1
    return 0
for gx in range(66):
    lon = -168 + gx * 5.1
    for gy in range(28):
        lat = 78 - gy * 5.0
        if onland(lon, lat):
            col = CONT[continent(lon, lat)][1]
            px = MX + gx * 6; py_ = MY + gy * 4.9
            d.ellipse([px-1.6, py_-1.6, px+1.6, py_+1.6], fill=col)
def proj(lon, lat):
    return (MX + (lon + 168) / 336 * MW, MY + (78 - lat) / 140 * MH)
for c in CARDS:
    px, py_ = proj(c[8], c[9])
    d.ellipse([px-8, py_-8, px+8, py_+8], fill=RED, outline=WHITE, width=1)
    d.text((px, py_), str(c[0]), font=BOLD(9), fill=WHITE, anchor="mm")
ly = MY + MH + 6
lx = 14
for name, col in CONT:
    d.rectangle([lx, ly+2, lx+8, ly+10], fill=col)
    d.text((lx+11, ly), name, font=BOLD(9), fill=INK)
    lx += 11 + tw(name, BOLD(9)) + 10
tally = "TALLY — EUROPE 16 · ASIA 6 · AMERICAS 8 · MIDEAST 6 · AFRICA 1 · OCEANIA 1 · GLOBAL 2"
d.text((14, ly+15), fit(tally, BOLD(8), 396), font=BOLD(8), fill=DARKRED)

# ---------------------------------------------------------------- briefs
BF = MED(10); BFB = BOLD(10)
bx1, bx2, bw = 425, 718, 292
pitch = 10.5
for i, (lead_in, tail) in enumerate(BRIEFS):
    col = 0 if i < 14 else 1
    x0 = bx1 if col == 0 else bx2
    y0 = 766 + (i if col == 0 else i - 14) * pitch
    num = str(14 + i)
    d.text((x0, y0), num, font=BFB, fill=RED)
    x1 = x0 + tw(num, BFB) + 4
    d.text((x1, y0), lead_in, font=BFB, fill=INK)
    x2 = x1 + tw(lead_in, BFB) + 3
    avail = x0 + bw - x2
    t = tail
    while t and tw(t, BF) > avail:
        t = t.rsplit(" ", 1)[0] if " " in t else t[:-1]
    d.text((x2, y0), t, font=BF, fill=(45,43,38))

# ---------------------------------------------------------------- DATE CHECK
dy = 928
d.rectangle([14, dy, 1010, dy+60], outline=RED, width=2)
d.rectangle([14, dy, 108, dy+60], fill=RED)
d.text((24, dy+11), "DATE", font=BOLD(14), fill=WHITE)
d.text((24, dy+30), "CHECK", font=BOLD(14), fill=WHITE)
dc = ("Left out on purpose — Friday 20 November's news, not Saturday's: Kyiv's three bridges hit (20 Nov) · "
      "Cyclone Akvan's landfall at Gopalpur (20 Nov) · Asia's AI sell-off, Taipei −6.2% (20 Nov) · "
      "the UK–EU reset deal (20 Nov) · Phillips's 118 in the first innings (20 Nov).")
for j, ln in enumerate(wrap(dc, MED(11), 884, 2)):
    d.text((118, dy+4+j*12), ln, font=MED(11), fill=INK)
unv = ("Unverified: Pakistan's minerals “worth $8–10 trillion” is its minister's estimate only — sources conflict, "
       "so no value is shown as fact. Not yet: any final COP31 text, ATP semi-final results, BepiColombo's Mercury orbit entry.")
for j, ln in enumerate(wrap(unv, MED(11), 884, 2)):
    d.text((118, dy+30+j*12), ln, font=MED(11), fill=DARKRED)

# ---------------------------------------------------------------- footer
foot = ("Every story happened, or was first reported, on Saturday 21 November 2026 · Sources: AP · BBC · Reuters · AFP · ICC · "
        "SimpleLife · AppiStos · Ridhu Times · Fast Company · OFAC · UKMTO · UN · SPA · ATP · Ukrinform · Anadolu · Original drawings")
ff = MED(9)
d.text(((W - tw(fit(foot, ff, 996), ff)) / 2, 996), fit(foot, ff, 996), font=ff, fill=GREY)

img.quantize(colors=256, method=Image.FASTOCTREE).save(HERE / "entry.png", optimize=True)
img.resize((300, 300), Image.LANCZOS).quantize(colors=256, method=Image.FASTOCTREE).save(HERE / "entry-300.png", optimize=True)
print("saved", (HERE / "entry.png").stat().st_size)
