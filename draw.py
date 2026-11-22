#!/usr/bin/env python3
"""THE MERIDIAN WIRE - Round 4 challenger A4. Saturday 21 November 2026.
Fresh compose program (Pillow only, deterministic). Facts ONLY from POOL21.
Builds three layout variants (A/B/C) for the duel, then writes the winner
as entry.png. Usage: python3 draw.py [A|B|C|all]
"""
import os, sys
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from mapdata import WORLD
FD = os.path.join(HERE, "fonts")
W = H = 1024
PAPER=(247,241,227); CARD=(253,250,242); INK=(20,33,61); RED=(176,58,46)
NAVY=(22,40,63); LAND=(110,130,100); GREY=(90,86,76); FAINT=(203,192,164); WHITE=(255,255,255)
RC={"EUROPE":(176,58,46),"ASIA":(29,111,184),"MIDEAST":(125,60,152),"AFRICA":(30,132,73),
    "AMERICAS":(202,111,30),"OCEANIA":(20,143,119),"GLOBAL":(93,109,126)}
SERIF="PlayfairDisplay-900.ttf"; SB="Archivo-Bold.ttf"; SM="Archivo-Medium.ttf"
_c={}
def F(n,s):
    k=(n,int(s))
    if k not in _c: _c[k]=ImageFont.truetype(os.path.join(FD,n),int(s))
    return _c[k]

# ---------------- POOL21 data (verbatim facts) ----------------
NUMBERS=[("3","weapons cross into Poland: two missiles + a jet drone"),
 ("42","injured in Kryvyi Rih, four of them children"),
 ("-5.28%","Nasdaq fall at Friday's close"),
 ("372,000","moved to shelters as Akvan hit"),
 ("\u20ac1BN","EU military aid adopted for Ukraine"),
 ("159/1","India at stumps in Wellington")]
TIMELINE=[("Overnight","Kryvyi Rih strike: two killed, 42 injured"),
 ("Morning","Rutte flies to Warsaw over the missiles"),
 ("Midday","Antalya: third COP31 draft due after overnight talks"),
 ("Afternoon","Denmark expels the Russian attache"),
 ("Evening","Stumps in Wellington: India 159/1")]
# no, place, region, headline, deck, srctag, datalabel, caption, lon, lat, scene
CARDS=[
 (1,"WARSAW","EUROPE","Rutte flies to Warsaw after missiles land",
  "Two missiles and a suspected jet drone came down in the south-east, a Kh-101 near Nowy Lipowiec. Rutte: \u201cgrave violation\u201d; Tusk: deliberate provocation. (AP)",
  "AP","3 WEAPONS CROSS","NOWY LIPOWIEC \u00b7 MISSILES DOWN",21.0,52.2,"missile"),
 (2,"ANTALYA","GLOBAL","COP31 runs into overtime with no deal yet",
  "Talks ran past Friday's scheduled close into Saturday. Draft drops every fossil-fuel reference and the $120bn finance target; third draft due this morning. (AP)",
  "AP","NO DEAL YET","ANTALYA \u00b7 INTO OVERTIME",30.7,36.9,"globe"),
 (3,"NEW YORK","AMERICAS","Wall Street enters correction as AI rout deepens",
  "S&P 500 fell about 3.7% on Friday, into correction territory. Nasdaq dropped 5.28% as chip and AI shares plunged. (SimpleLife)",
  "SIMPLELIFE","NASDAQ -5.28%","NEW YORK \u00b7 FRIDAY'S CLOSE",-74.0,40.7,"chart"),
 (4,"KRYVYI RIH","EUROPE","Russian strike kills two, injures 42",
  "Overnight strike kills two and injures 42, four of them children, the city's military chief says. One of Russia's largest attacks of the war. (AppiStos)",
  "APPISTOS","2 DEAD \u00b7 42 HURT","KRYVYI RIH \u00b7 OVERNIGHT",33.4,47.9,"strike"),
 (5,"COPENHAGEN","EUROPE","Denmark exposes 'assassination plot'",
  "Russia \u2018planned and initiated\u2019 a bid to kill a Ukrainian-American rapper near Copenhagen, Denmark says. The Russian attache is expelled. (BBC)",
  "BBC","ATTACHE EXPELLED","COPENHAGEN \u00b7 PLOT EXPOSED",12.6,55.7,"target"),
 (6,"KYIV","EUROPE","Russia's barrage: 400 drones, 110 missiles",
  "At least eight dead across Ukraine in the overnight barrage. Austrian embassy hit in Kyiv; France calls for a UN Security Council meeting. (BBC)",
  "BBC","400 DRONES \u00b7 110 MISSILES","KYIV \u00b7 OVERNIGHT BARRAGE",30.5,50.4,"sky"),
 (7,"ODISHA","ASIA","After Akvan: 372,000 moved, no deaths",
  "A day after landfall, no deaths reported and relief under way. Storm weakens to a depression; schools stay shut through Saturday. (Ridhu Times)",
  "RIDHU TIMES","372,000 MOVED","ODISHA \u00b7 AFTER AKVAN",84.9,19.3,"storm"),
 (8,"BRUSSELS","EUROPE","EU adopts 1bn euro military aid for Ukraine",
  "Joint buying runs via the Peace Facility. Britain pledges 1,000+ drones in a \u00a3260m package alongside the EU deal. (Reuters)",
  "REUTERS","\u20ac1BN ADOPTED","BRUSSELS \u00b7 AID ADOPTED",4.3,50.8,"flags"),
 (9,"NEW YORK","AMERICAS","JPMorgan, Visa, Mastercard hit by cyberattack",
  "Banks report incidents at third-party vendors. Core payment networks are unaffected, they say. (Reuters)",
  "REUTERS","3 NETWORKS HIT","NEW YORK \u00b7 VENDOR BREACH",-73.9,40.8,"cards"),
 (10,"ULAANBAATAR","ASIA","Mongolia's president resigns",
  "Resignation sets the stage for a snap election. It caps a week of political turmoil in the capital. (Reuters)",
  "REUTERS","SNAP ELECTION NEXT","ULAANBAATAR \u00b7 RESIGNATION",106.9,47.9,"steppe"),
 (11,"THE HAGUE","GLOBAL","Myanmar ruling rattles Israel's Gaza defence",
  "World court's genocide verdict against Myanmar raises questions in Jerusalem over its own case, experts say. Ruling itself came Thursday. (BBC)",
  "BBC","GENOCIDE VERDICT","THE HAGUE \u00b7 WORLD COURT",4.3,52.1,"court"),
 (12,"JOHANNESBURG","AFRICA","ANC scrambles after worst result since 1994",
  "ANC wins 31% of the vote, its worst since 1994. It now races for coalition deals to stay in government. (BBC)",
  "BBC","ANC 31%","JOHANNESBURG \u00b7 THE COUNT",28.0,-26.2,"vote"),
 (13,"WELLINGTON","OCEANIA","India fight back: 159/1 at stumps, day two",
  "India trail New Zealand by 209 in the first Test after hosts made 368. Nicholls made 175 not out for the hosts. (ICC)",
  "ICC","159/1 \u00b7 DAY TWO","WELLINGTON \u00b7 STUMPS",174.8,-41.3,"cricket"),
]
BRIEFS=[
 (14,"Kathmandu Nepal's new leader Balendra Shah faces an India test (BBC)","ASIA",85.3,27.7),
 (15,"Washington US releases more UFO footage filmed in the Middle East (BBC)","AMERICAS",-77.0,38.9),
 (16,"Los Angeles Hyundai unveils the 2027 Elantra at the auto show (Fast Company)","AMERICAS",-118.2,34.1),
 (17,"Cardiff Lauren Price beats Kotaskova to become undisputed champion (BBC)","EUROPE",-3.2,51.5),
 (18,"Paris Three police sentenced over the beating of Michel Zecler (BBC)","EUROPE",2.4,48.9),
 (19,"Oxford Life, 22 years minimum, for the Thames drowning murder (BBC)","EUROPE",-1.3,51.8),
 (20,"New York Nikhil Gupta gets 19+ years over the Sikh murder plot (BBC)","AMERICAS",-74.0,40.7),
 (21,"Cincinnati Fiona the hippo dies after eating a hat (AP)","AMERICAS",-84.5,39.1),
 (22,"Washington US sanctions four Iranians over oil revenues (OFAC)","AMERICAS",-77.1,38.8),
 (23,"Hormuz A tanker is struck and on fire in the Strait of Hormuz (UKMTO)","MIDEAST",56.3,26.6),
 (24,"Los Angeles Jury convicts the man who started the Palisades Fire (AP)","AMERICAS",-118.3,34.0),
 (25,"Frankfurt ECB names Boone and Brunnermeier for its Executive Board (Reuters)","EUROPE",8.7,50.1),
 (26,"Buenos Aires Argentina's Senate backs a disability framework, 71-0 (AP)","AMERICAS",-58.4,-34.6),
 (27,"Riyadh A Saudi coalition intercepts Houthi missiles over Riyadh (Reuters)","MIDEAST",46.7,24.6),
 (28,"Barcelona A pill is hailed as a breakthrough for pancreatic cancer (Reuters)","EUROPE",2.2,41.4),
 (29,"Gaza On World Children's Day, Palestinian children appeal for help (UN)","MIDEAST",34.3,31.5),
 (30,"Madrid Amnesty says Spanish police used excess force in the strike (AP)","EUROPE",-3.7,40.4),
 (31,"Rome Italian workers and students march against Meloni's government (AFP)","EUROPE",12.5,41.9),
 (32,"Jeddah Saudi Arabia warns of thunderstorms through Tuesday (SPA)","MIDEAST",39.2,21.5),
 (33,"Kuala Lumpur Malaysia to send 10,000 Rohingya to Turkey for training (Reuters)","ASIA",101.7,3.1),
 (34,"Kharkiv Ukraine says it has finished a \u201cBear Trap\u201d in the Kharkiv area (Ukrinform)","EUROPE",36.2,49.9),
 (35,"Islamabad Pakistan's minerals are worth $8-10 trillion, its minister says (Reuters)","ASIA",73.1,33.7),
 (36,"Singapore US presses Singapore and Malaysia on Iran sanctions (Reuters)","ASIA",103.8,1.35),
 (37,"Paris France seeks a UN council meeting on the Kyiv strikes (AFP)","EUROPE",2.3,48.8),
 (38,"Kyiv The war tally: 771 Ukrainians killed, 2,300+ missing (homevo)","EUROPE",30.6,50.5),
 (39,"Ankara Turkey welcomes the World Court's Myanmar ruling (Anadolu)","MIDEAST",32.9,39.9),
 (40,"Turin ATP semis are set: Alcaraz v Shelton, Zverev v Medvedev (ATP)","EUROPE",7.7,45.1),
]
DATECHECK=("Left out as Friday 20 November's news: Kyiv's three bridges hit, Cyclone Akvan's landfall at Gopalpur, "
 "COP31's final day ending with no deal, Asia's AI sell-off (Taipei -6.2%), the UK-EU reset deal and Phillips's 118 "
 "in the first innings. Not yet happened, so not shown: any final COP31 text, the ATP semi-final results and "
 "BepiColombo's entry into orbit around Mercury (due today).")
FOOT_L="Every story here happened, or was first reported, on Saturday 21 November 2026. Contested claims are attributed."
FOOT_R="Sources named beside each story \u00b7 original drawings"

# ---------------- helpers ----------------
class Page:
    def __init__(self):
        self.img=Image.new("RGB",(W,H),PAPER); self.d=ImageDraw.Draw(self.img)
    def tw(self,s,f): return self.d.textlength(s,font=f)
    def wrap(self,t,f,mw,ml=None):
        out=[]; cur=""
        for wd in t.split():
            tr=wd if not cur else cur+" "+wd
            if self.tw(tr,f)<=mw or not cur: cur=tr
            else: out.append(cur); cur=wd
        if cur: out.append(cur)
        return out[:ml] if ml else out
    def T(self,x,y,s,f,fill=INK,anchor="la"): self.d.text((x,y),s,font=f,fill=fill,anchor=anchor)
    def fit(self,s,n,start,mw,floor=9):
        z=start
        while z>floor and self.tw(s,F(n,z))>mw: z-=1
        return z

# ---------------- scenes (fresh, flat, data-carrying) ----------------
def scene(p,kind,x0,y0,x1,y1):
    d=p.d; w=x1-x0; h=y1-y0
    if kind=="missile":
        d.rectangle([x0,y0,x1,y1],fill=(122,172,92))
        for i in range(4): d.line([x0,y0+h*(0.3+i*0.18),x1,y0+h*(0.24+i*0.18)],fill=(96,140,70),width=3)
        d.line([x0+w*0.28,y0+h*0.5,x0+w*0.7,y0+h*0.64],fill=(90,94,100),width=7)
        d.polygon([(x0+w*0.7,y0+h*0.64),(x0+w*0.7+10,y0+h*0.64-5),(x0+w*0.7+10,y0+h*0.64+5)],fill=RED)
    elif kind=="globe":
        d.rectangle([x0,y0,x1,y1],fill=(170,205,225))
        cx,cy,r=x0+w*0.38,y0+h*0.52,h*0.36
        d.ellipse([cx-r,cy-r,cx+r,cy+r],fill=(52,130,90),outline=(30,90,130),width=2)
        tx=x1-w*0.2; d.rectangle([tx,y0+6,tx+7,y1-14],fill=WHITE,outline=INK)
        d.rectangle([tx+1,y0+h*0.45,tx+6,y1-14],fill=RED); d.ellipse([tx-4,y1-20,tx+11,y1-5],fill=RED)
    elif kind=="chart":
        d.rectangle([x0,y0,x1,y1],fill=(18,24,40))
        pts=[(x0+w*f,y0+h*g) for f,g in ((0.03,0.25),(0.28,0.32),(0.48,0.28),(0.65,0.55),(0.82,0.62),(0.97,0.85))]
        d.line(pts,fill=RED,width=3)
        for px,py in pts: d.ellipse([px-2,py-2,px+2,py+2],fill=RED)
    elif kind in ("strike","sky"):
        d.rectangle([x0,y0,x1,y1],fill=(34,46,80))
        for fx in (0.15,0.5,0.82):
            sx=x0+w*fx; d.arc([sx-24,y0+2,sx+28,y0+h*0.75],start=200,end=325,fill=RED,width=2)
            d.ellipse([sx+22,y0+h*0.36,sx+28,y0+h*0.36+6],fill=RED)
        d.rectangle([x0,y1-h*0.16,x1,y1],fill=(14,20,36))
    elif kind=="target":
        d.rectangle([x0,y0,x1,y1],fill=(168,196,218))
        cx,cy,r=x0+w*0.58,y0+h*0.5,h*0.32
        d.ellipse([cx-r,cy-r,cx+r,cy+r],outline=RED,width=3)
        d.line([cx-r-6,cy,cx-r*0.35,cy],fill=RED,width=3); d.line([cx+r*0.35,cy,cx+r+6,cy],fill=RED,width=3)
        d.line([cx,cy-r-6,cx,cy-r*0.35],fill=RED,width=3); d.line([cx,cy+r*0.35,cx,cy+r+6],fill=RED,width=3)
        d.ellipse([cx-2,cy-2,cx+2,cy+2],fill=RED)
    elif kind=="storm":
        d.rectangle([x0,y0,x1,y1],fill=(70,130,160))
        cx,cy=x0+w*0.36,y0+h*0.48
        for r in (28,21,14,8): d.arc([cx-r,cy-r*0.8,cx+r,cy+r*0.8],start=20,end=300,fill=WHITE,width=3)
        d.polygon([(x0,y1),(x1,y1),(x1,y1-10),(x0+w*0.55,y1-18),(x0,y1-6)],fill=(214,196,140))
    elif kind=="flags":
        d.rectangle([x0,y0,x1,y1],fill=(210,220,235))
        import math
        fw,fh=w*0.32,h*0.52; fy=y0+h*0.22
        d.rectangle([x0+w*0.1,fy,x0+w*0.1+fw,fy+fh],fill=(30,50,130))
        d.rectangle([x0+w*0.1+fw/2-2,fy,x0+w*0.1+fw/2+2,fy+fh],fill=RED)
        d.rectangle([x0+w*0.1,fy+fh/2-2,x0+w*0.1+fw,fy+fh/2+2],fill=RED)
        ex=x1-w*0.1-fw; d.rectangle([ex,fy,ex+fw,fy+fh],fill=(30,50,160))
        for i in range(8):
            a=math.radians(i*45); sx,sy=ex+fw/2+fh*0.28*math.cos(a),fy+fh/2+fh*0.28*math.sin(a)
            d.ellipse([sx-2,sy-2,sx+2,sy+2],fill=(245,197,24))
    elif kind=="cards":
        d.rectangle([x0,y0,x1,y1],fill=(24,30,44))
        for i,col in enumerate(((70,110,170),(90,130,90),(150,120,60))):
            bx,by=x0+w*(0.06+i*0.26),y0+h*(0.2+i*0.06)
            d.rounded_rectangle([bx,by,bx+w*0.32,by+h*0.52],radius=5,fill=col,outline=(220,225,235))
    elif kind=="steppe":
        d.rectangle([x0,y0,x1,y1],fill=(170,205,228))
        gy=y0+h*0.6; d.rectangle([x0,gy,x1,y1],fill=(148,168,96))
        gx,gw,gh=x0+w*0.14,w*0.3,h*0.34
        d.polygon([(gx,gy),(gx+gw*0.5,gy-gh),(gx+gw,gy)],fill=(240,238,230))
        px=x0+w*0.66; d.line([px,gy,px,gy-h*0.6],fill=(70,60,50),width=3)
        d.rectangle([px,gy-h*0.6,px+w*0.2,gy-h*0.6+h*0.26],fill=(40,90,160))
    elif kind=="court":
        d.rectangle([x0,y0,x1,y1],fill=(206,214,224))
        bw=x1-x0; bx,by=x0+bw*0.22,y0+h*0.14
        d.polygon([(bx-6,by+8),(bx+bw*0.28,by-6),(bx+bw*0.56+6,by+8)],fill=INK)
        d.rectangle([bx,by+10,bx+bw*0.56,y1-8],fill=(238,236,228))
        for i in range(4):
            cx=bx+8+i*(bw*0.56-16)/3; d.rectangle([cx-3,by+12,cx+3,y1-8],fill=(150,150,145))
    elif kind=="vote":
        d.rectangle([x0,y0,x1,y1],fill=(232,214,170))
        for i in range(10):
            bx=x0+8+i*((w-16)/10); bh=h*0.55 if i<3 else h*0.3
            d.rectangle([bx,y1-8-bh,bx+(w-16)/14,y1-8],fill=RED if i<3 else (150,150,145))
    elif kind=="cricket":
        d.rectangle([x0,y0,x1,y1],fill=(110,168,92))
        d.rectangle([x0+w*0.3,y0,x0+w*0.7,y1],fill=(226,206,150))
        sx=x1-w*0.3
        for i in range(3): d.rectangle([sx+i*7,y0+h*0.3,sx+i*7+3,y0+h*0.72],fill=(240,220,120))
        d.ellipse([x0+w*0.52,y0+h*0.18,x0+w*0.52+9,y0+h*0.18+9],fill=RED)
    else:
        d.rectangle([x0,y0,x1,y1],fill=(200,205,215))

def strip(p,card,x,y,w,h,band,tag_s,lab_s):
    no,place,region,head,deck,src,label,cap,lon,lat,kind=card
    scene(p,kind,x,y,x+w,y+h-band)
    p.d.rectangle([x,y,x+w,y+4],fill=RC[region])
    tw_=p.tw(src,F(SB,tag_s))+8
    p.d.rectangle([x+w-tw_-3,y+6,x+w-3,y+6+tag_s+6],fill=NAVY)
    p.T(x+w-3,y+8,src,F(SB,tag_s),WHITE,anchor="ra")
    ls=p.fit(label,SB,lab_s,w-24,floor=7); lw=p.tw(label,F(SB,ls))+10
    p.d.rectangle([x+4,y+h-band-ls-10,x+4+lw,y+h-band-3],fill=WHITE)
    p.T(x+9,y+h-band-ls-8,label,F(SB,ls),INK)
    p.d.rectangle([x,y+h-band,x+w,y+h],fill=NAVY)
    cs=band-5
    while cs>7 and p.tw(cap,F(SB,cs))>w-10: cs-=1
    p.T(x+w/2,y+h-band+2,cap,F(SB,cs),WHITE,anchor="ma")

def card_box(p,card,x,y,w,h,strip_h,head_f,deck_f,head_name=SB):
    no,place,region,head,deck,src,label,cap,lon,lat,kind=card
    p.d.rectangle([x,y,x+w,y+h],fill=CARD,outline=FAINT)
    strip(p,card,x,y,w,strip_h,13,8,10)
    ry=y+strip_h+4
    p.T(x+6,ry,"%d %s \u00b7 %s"%(no,place,region),F(SB,9),RC[region])
    hy=ry+13
    for ln in p.wrap(head,F(head_name,head_f),w-12,2):
        p.T(x+6,hy,ln,F(head_name,head_f),INK); hy+=head_f+3
    dy=hy+1
    for ln in p.wrap(deck,F(SM,deck_f),w-12,4):
        if dy+deck_f>y+h-2: break
        p.T(x+6,dy,ln,F(SM,deck_f),INK); dy+=deck_f+2

def header(p,hook_fill=RED,mast_cx=None):
    MX=16; CW=W-2*MX
    p.T(MX,10,"SATURDAY 21 NOVEMBER 2026",F(SB,11),INK)
    p.T(W-MX,10,"40 STORIES \u00b7 7 REGIONS \u00b7 EVERY ONE DATED TODAY",F(SB,11),INK,anchor="ra")
    p.d.rectangle([MX,29,W-MX,32],fill=RED); p.d.line([MX,35,W-MX,35],fill=INK)
    title="THE MERIDIAN WIRE"; sz=p.fit(title,SERIF,62,CW)
    if mast_cx: p.T(mast_cx,36,title,F(SERIF,sz),INK,anchor="ma")
    else: p.T(MX,36,title,F(SERIF,sz),INK)
    p.d.rectangle([MX,94,W-MX,116],fill=hook_fill)
    p.T(W/2,100,"MISSILES LAND IN POLAND \u00b7 COP31 SLIPS INTO OVERTIME \u00b7 WALL STREET FALLS INTO CORRECTION",F(SB,11),WHITE,anchor="ma")
    return 118

def timeline_row(p,y):
    MX=16; CW=W-2*MX
    p.d.rectangle([MX,y,W-MX,y+34],outline=INK)
    cell=CW/5.0
    for i,(lab,ev) in enumerate(TIMELINE):
        cx=MX+i*cell
        if i: p.d.line([cx,y,cx,y+34],fill=FAINT)
        p.T(cx+6,y+2,lab.upper(),F(SB,9),RED)
        for j,ln in enumerate(p.wrap(ev,F(SM,8),cell-12,2)): p.T(cx+6,y+15+j*10,ln,F(SM,8),INK)
    return y+38

def numbers_row(p,y):
    MX=16; CW=W-2*MX
    p.T(MX,y,"THE DAY IN NUMBERS",F(SB,9),GREY)
    col=CW/6.0
    for i,(n,cap) in enumerate(NUMBERS):
        cx=MX+i*col
        # Playfair's euro glyph reads poorly at strip size; Archivo carries it cleanly
        nf=F(SB,23) if "\u20ac" in n else F(SERIF,23)
        p.T(cx,y+9,n,nf,RED)
        for j,ln in enumerate(p.wrap(cap,F(SM,8),col-10,2)): p.T(cx,y+38+j*10,ln,F(SM,8),INK)
    return y+60

def region_chips(p,y):
    MX=16; CW=W-2*MX
    counts=[("EUROPE",16),("ASIA",6),("AMERICAS",8),("MIDEAST",6),("AFRICA",1),("OCEANIA",1),("GLOBAL",2)]
    widths=[p.tw("%s %d"%(n,c),F(SB,10))+14 for n,c in counts]
    cx=MX+(CW-(sum(widths)+6*(len(counts)-1)))/2
    for (n,c),wd in zip(counts,widths):
        p.d.rectangle([cx,y,cx+wd,y+17],fill=RC[n]); p.T(cx+wd/2,y+3,"%s %d"%(n,c),F(SB,10),WHITE,anchor="ma"); cx+=wd+6
    return y+20

def draw_map(p,x,y,w,h):
    d=p.d; d.rectangle([x,y,x+w,y+h],fill=NAVY)
    p.T(x+8,y+5,"WHERE IT HAPPENED",F(SB,11),WHITE)
    mx0,my0=x+6,y+24; mw=w-12; sc=mw/360.0
    def proj(lon,lat): return (mx0+(lon+180)*sc, my0+(82-lat)*sc)
    for rings in WORLD.values():
        for ring in rings.split("|"):
            pts=[]
            for pair in ring.split(","):
                lo,la=pair.split(":"); pts.append(proj(float(lo),float(la)))
            if len(pts)>2: d.polygon(pts,fill=LAND)
    for (no,txt,region,lon,lat) in BRIEFS:
        px,py=proj(lon,lat); d.ellipse([px-2.5,py-2.5,px+2.5,py+2.5],fill=RC[region])
    for card in CARDS:
        px,py=proj(card[8],card[9])
        d.ellipse([px-9,py-9,px+9,py+9],fill=RC[card[2]],outline=WHITE)
        p.T(px,py-6,str(card[0]),F(SB,10),WHITE,anchor="ma")
    ly=y+h-22
    for ln in p.wrap("Numbered pins (r9, \u00d818px) = the 13 pictured cards \u00b7 small dots = the 27 briefs",F(SM,9),w-16,2):
        p.T(x+8,ly,ln,F(SM,9),(200,208,220)); ly+=11

def briefs_block(p,x,y,w,cols=2):
    p.T(x,y,"ALSO ON SATURDAY \u00b7 27 MORE STORIES (14\u201340)",F(SB,11),RED)
    colw=(w-12*(cols-1))/cols
    per=(len(BRIEFS)+cols-1)//cols
    for ci in range(cols):
        cx=x+ci*(colw+12); cy=y+17
        for (no,txt,region,lon,lat) in BRIEFS[ci*per:(ci+1)*per]:
            num="%d "%no; off=p.tw(num,F(SB,9))
            p.T(cx,cy,num,F(SB,9),RC[region])
            lines=p.wrap(txt,F(SM,9),colw-off,2)
            for j,ln in enumerate(lines): p.T(cx+off,cy+j*10.5,ln,F(SM,9),INK)
            cy+=max(1,len(lines))*10.5+1.5

def datecheck(p,y,h=44):
    MX=16
    p.d.rectangle([MX,y,W-MX,y+h],outline=RED,width=2)
    p.T(MX+8,y+3,"DATE CHECK",F(SB,10),RED)
    off=p.tw("DATE CHECK ",F(SB,10))+6
    for j,ln in enumerate(p.wrap(DATECHECK,F(SM,9),W-2*MX-16-off,4)):
        p.T(MX+8+(off if j==0 else 0),y+3+j*10.5,ln,F(SM,9),INK)
    return y+h+4

def footer(p,y):
    MX=16
    p.d.line([MX,y,W-MX,y],fill=INK)
    p.T(MX,y+3,FOOT_L,F(SM,8),GREY); p.T(W-MX,y+3,FOOT_R,F(SM,8),GREY,anchor="ra")

# ---------------- variants ----------------
def variant_B():
    """Stack: horizontal timeline/numbers, 3 lead + 5+5 grid, map+briefs bottom."""
    p=Page(); MX=16; CW=W-2*MX
    y=header(p); y=timeline_row(p,y); y=numbers_row(p,y); y=region_chips(p,y)+2
    lw=(CW-16)/3
    for i,c in enumerate(CARDS[:3]): card_box(p,c,MX+i*(lw+8),y,lw,196,84,19,11,SERIF)
    y+=202; fw=(CW-32)/5
    for r in range(2):
        for cc in range(5): card_box(p,CARDS[3+r*5+cc],MX+cc*(fw+8),y+r*150,fw,146,44,11,9)
    y+=304
    draw_map(p,MX,y,300,196); briefs_block(p,MX+314,y,CW-314,2)
    y+=202; y=datecheck(p,y,40); footer(p,y)
    return p.img

def variant_A():
    """Rail: masthead left, vertical timeline rail left, cards in 2-col flow right."""
    p=Page(); MX=16; CW=W-2*MX
    y=header(p)
    # vertical rail
    rx,ry,rw=MX,y,150
    p.d.rectangle([rx,ry,rx+rw,ry+300],outline=INK)
    p.T(rx+6,ry+4,"THE DAY, UTC",F(SB,10),RED); cy=ry+20
    for lab,ev in TIMELINE:
        p.T(rx+6,cy,lab.upper(),F(SB,9),RED); cy+=12
        for ln in p.wrap(ev,F(SM,9),rw-12,3): p.T(rx+6,cy,ln,F(SM,9),INK); cy+=11
        cy+=7
    p.T(rx+6,cy+4,"IN NUMBERS",F(SB,10),RED); cy+=18
    for n,cap in NUMBERS:
        p.T(rx+6,cy,n,F(SERIF,17),RED); cy+=20
        for ln in p.wrap(cap,F(SM,8),rw-12,2): p.T(rx+6,cy,ln,F(SM,8),INK); cy+=10
        cy+=4
    gx=MX+rw+10; gw=CW-rw-10; cw2=(gw-8)/2
    idx=0
    for r in range(5):
        for cc in range(2):
            if idx>=10: break
            card_box(p,CARDS[idx],gx+cc*(cw2+8),y+r*122,cw2,116,40,12,9); idx+=1
    y2=y+5*122+4
    lw=(CW-16)/3
    for i,c in enumerate(CARDS[10:13]): card_box(p,c,MX+i*(lw+8),y2,lw,120,42,12,9)
    y2+=126
    draw_map(p,MX,y2,300,120); briefs_block(p,MX+314,y2,CW-314,2)
    y2+=126; y2=datecheck(p,y2,36); footer(p,y2)
    return p.img

def variant_C():
    """Ledger: centred masthead, numbers left column, dense 13-card grid, 3-col briefs."""
    p=Page(); MX=16; CW=W-2*MX
    y=header(p,hook_fill=NAVY,mast_cx=W/2); y=timeline_row(p,y)
    lw=(CW-16)/3
    for i,c in enumerate(CARDS[:3]): card_box(p,c,MX+i*(lw+8),y,lw,180,76,18,11,SERIF)
    y+=186; fw=(CW-32)/5
    for r in range(2):
        for cc in range(5): card_box(p,CARDS[3+r*5+cc],MX+cc*(fw+8),y+r*140,fw,134,42,11,9)
    y+=286; y=numbers_row(p,y); y=region_chips(p,y)+2
    draw_map(p,MX,y,300,150); briefs_block(p,MX+314,y,CW-314,3)
    y+=156; y=datecheck(p,y,40); footer(p,y)
    return p.img

BUILDERS={"A":variant_A,"B":variant_B,"C":variant_C}
def save(img,name):
    q=img.quantize(colors=256,method=Image.MEDIANCUT,dither=Image.NONE)
    out=os.path.join(HERE,name); q.save(out,optimize=True)
    img.resize((300,300),Image.LANCZOS).save(os.path.join(HERE,name.replace(".png","-300.png")),optimize=True)
    print(name,os.path.getsize(out),"bytes")
    return out
def main():
    which=sys.argv[1] if len(sys.argv)>1 else "all"
    if which=="all":
        for k in "ABC": save(BUILDERS[k](),"variant_%s.png"%k)
        save(variant_B(),"entry.png")  # DUEL WINNER: B (see README) - only B ships as entry.png
    else:
        save(BUILDERS[which.upper()](),"entry.png")
if __name__=="__main__": main()
