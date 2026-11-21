#!/usr/bin/env python3
"""Render entry.png for make.fun competition news-image-20261121.

Dense front-page newspaper image: 35 verified stories from Saturday
21 November 2026, 3 leads with spot illustrations, 15 grid briefs,
17 more briefs, a 19-marker world map, and a sources footer. Output is
exactly 1024x1024 PNG.
Run: python3 render.py  (writes entry.png next to this script)
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1024, 1024
MARGIN = 22

PAPER = (248, 244, 233)
INK = (26, 26, 26)
MUTED = (90, 86, 76)
RED = (179, 38, 30)
SEA = (214, 230, 241)
LAND = (203, 210, 178)
LAND_EDGE = (150, 158, 128)
RULE = (60, 58, 50)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


F_TITLE = font("DejaVuSerif-Bold.ttf", 46)
F_DATE = font("DejaVuSans-Bold.ttf", 15)
F_SECTION = font("DejaVuSans-Bold.ttf", 13)
F_LEAD_HEAD = font("DejaVuSerif-Bold.ttf", 20)
F_LEAD_KICK = font("DejaVuSans-Bold.ttf", 10)
F_LEAD_BODY = font("DejaVuSans.ttf", 11)
F_GRID_HEAD = font("DejaVuSans-Bold.ttf", 11)
F_GRID_BODY = font("DejaVuSans.ttf", 11)
F_KEY = font("DejaVuSans.ttf", 10)
F_KEY_B = font("DejaVuSans-Bold.ttf", 10)
F_BRIEF = font("DejaVuSans.ttf", 11)
F_BRIEF_B = font("DejaVuSans-Bold.ttf", 11)
F_FOOT = font("DejaVuSans.ttf", 10)
F_NUM = font("DejaVuSans-Bold.ttf", 9)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, x, y, lines, fnt, fill=INK, leading=None):
    if leading is None:
        leading = fnt.size + 3
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


# ---------------------------------------------------------------- stories
LEADS = [
    {
        "kick": "CLIMATE  ·  ANTALYA",
        "color": (46, 125, 50),
        "head": "COP31 slips into overtime with no deal in sight",
        "body": (
            "EU climate chief Wopke Hoekstra said it was \u201ceither going to be a good "
            "deal or no deal\u201d as talks ran into overtime. The draft stripped out "
            "fossil-fuel references and dropped a $120bn adaptation target."
        ),
    },
    {
        "kick": "UKRAINE  ·  KRYVYI RIH",
        "color": (179, 38, 30),
        "head": "\u201cTriple-tap\u201d strike kills boy, 7, in Zelensky\u2019s home city",
        "body": (
            "Russian missiles hit a restaurant car park in Kryvyi Rih on Friday night, "
            "then drones struck the rescuers \u2014 killing a 7-year-old boy, Tikhon, and "
            "a 20-year-old paramedic, and injuring about 60, on Children\u2019s Day."
        ),
    },
    {
        "kick": "GAZA  ·  GAZA CITY",
        "color": (140, 90, 20),
        "head": "Israeli strike kills three in WCK aid vehicle",
        "body": (
            "A Saturday strike hit a vehicle carrying papers and food for World Central "
            "Kitchen in Gaza City, killing three people aboard, Gaza health officials and "
            "eyewitnesses said. Seven more Palestinians were wounded."
        ),
    },
]

GRID = [
    ("128 NATIONS AGREE \u201cKILLER ROBOT\u201d RULES",
     "States at the UN weapons convention in Geneva agreed on Saturday to negotiate binding rules on autonomous weapons by 2028."),
    ("M6.8 QUAKE SHAKES BANDA SEA",
     "A magnitude 6.8 earthquake struck at 09:42 UTC, 103 km NE of Lospalos, Timor-Leste; felt in Dili and Darwin. No tsunami threat."),
    ("MEXICO CAPTURES \u201cEL CHAPO ISIDRO\u201d",
     "Fausto Isidro Meza Flores, a Los Mazatlecos leader on the FBI\u2019s 10 most wanted list, was captured in Guasave, Sinaloa, overnight with US help."),
    ("TRUMP WEIGHS NEW STRIKES ON IRAN",
     "The US president is considering fresh strikes as Israel presses for action, the NYT reported on Saturday, citing new intelligence on Iranian capabilities."),
    ("PROJECTILE HITS TANKER NEAR OMAN",
     "An outbound tanker was struck in its engine room 17 nautical miles east of Khasab at 05:50 UTC, UKMTO said. No casualties; the projectile was unidentified."),
    ("SAUDI COALITION INTERCEPTS 3 HOUTHI MISSILES",
     "Three missiles aimed at Riyadh were intercepted on Saturday, the coalition said, as it struck back at targets in Yemen."),
    ("DENMARK EXPELS RUSSIAN DEFENCE ATTACH\u00c9",
     "Copenhagen gave the attach\u00e9 seven days to leave over an alleged plot to kill US-Ukrainian rapper Kyivstoner at a September concert; two men were arrested."),
    ("EU DRAFTS 3% DIGITAL TAX ON BIG TECH",
     "Council president Costa proposed a 3% levy in the draft 2028\u201334 budget, cut to \u20ac1.582 trillion, presented on Saturday."),
    ("BEPICOLOMBO DUE AT MERCURY TONIGHT",
     "The ESA\u2013JAXA probe was set to enter Mercury orbit at 18:24 UTC on Saturday after an eight-year journey. Its two orbiters separate on 9\u201310 Dec."),
    ("FLORIDA FLOODS WORSEN",
     "Heavy rain deepened flooding along the central coast on Saturday; parts of Brevard County recorded 28 inches of rain."),
    ("VIETNAM SPEEDS UP LAND SEIZURES",
     "Parliament approved a law on Saturday to fast-track land expropriation for priority projects."),
    ("SOUTH AFRICA MOURNS MLAMBO-NGCUKA, 71",
     "Tributes poured in on Saturday for the country\u2019s first female deputy president (2005\u201308) and former UN Women chief, who died on Friday evening."),
    ("DRONES HIT RUSSIAN SHIP IN GULF OF FINLAND",
     "The US-sanctioned Sparta II caught fire after two drone strikes on Saturday morning and drifted into Finnish waters; the crew was evacuated."),
    ("IRAN \u201cEFFECTIVELY OUT OF NPT\u201d",
     "Lawmaker Abolfazl Zohrevand told TASS that Iran had \u201cactually fallen out of\u201d the nuclear non-proliferation treaty after strikes on its nuclear sites and scientists."),
    ("BASRA POWER-STATION BLAST KILLS 4",
     "A gas-pipeline explosion at the al-Hartha plant at about 06:00 on Saturday killed at least four and injured 30\u201335; the 800 MW station shut down."),
]

BRIEFS = [
    ("MARKETS: AI ROUT DEEPENS \u2014",
     "S&P 500 fell 3.7% on Friday to 6,910, entering correction; Nikkei \u22125.1%, gold \u22124.6%, Bitcoin ~$57,850."),
    ("U17 WORLD CUP \u2014",
     "Colombia 2\u20131 Japan (Mart\u00ednez pen 90+3), Serbia 2\u20130 Honduras, Tanzania 2\u20132 Costa Rica, Venezuela 2\u20131 Cameroon in Qatar."),
    ("MIGRANT CARAVAN \u2014",
     "About 300 migrants crossed from Guatemala into Mexico and walked north towards the US border."),
    ("CONMEBOL",
     "backed Gianni Infantino\u2019s re-election as FIFA president."),
    ("HONDURAS \u2014",
     "Three US citizens were among four people convicted in a sex-trafficking case."),
    ("MAMA AWARDS \u2014",
     "BTS took Album of the Year for \u201cARIRANG\u201d in Osaka, ending the night with five awards; CORTIS won Song of the Year."),
    ("AFLW \u2014",
     "North Melbourne beat Sydney 83\u201351 and Melbourne beat Carlton 75\u201345 to reach Friday\u2019s grand final at IKON Park."),
    ("HARRY KANE",
     "had surgery on Saturday on a torn ankle ligament suffered in Bayern\u2019s draw with Cologne; out for the next few months."),
    ("SPAIN \u2014",
     "S\u00e1nchez announced an extension of the banking levy to 2027 to fund housing; it raises \u20ac1.4bn a year."),
    ("GEN Z PROTESTS, DAY 2 \u2014",
     "Marches continued in France and Spain and an Italian transport strike disrupted trains, a day after walkouts in 25 nations."),
    ("SHORT TRACK \u2014",
     "Choi Min-jeong won her third straight World Tour 1,000m title on home ice in Seoul (1:31.05); Shin Dong-min took the men\u2019s 1,500m."),
    ("ATP FINALS \u2014",
     "Alcaraz beat Shelton 3\u20136, 6\u20133, 7\u20136(1) in Turin to reach a second straight final; Zverev v Medvedev tonight."),
    ("ZELENSKY IN KYIV \u2014",
     "called the Crimean Bridge strikes a \u201cfair response\u201d to 109 Russian attacks on Ukrainian bridges; clearing the span may take a year."),
    ("T20 \u2014",
     "Australia beat England by three wickets with a ball to spare at the MCG \u2014 Chaudhary 66 and 2\u201321, Edwards 25* \u2014 ending England\u2019s seven-game winning run."),
    ("PAKISTAN \u2014",
     "The PCB dropped former captains Rizwan and Masood from central contracts in a 38-player overhaul; Babar and Agha top the new list."),
    ("SANDPAPERGATE \u2014",
     "Fox Sports rested Khawaja and Warner from commentary; Cricket Australia gave captain Cummins its \u201cunanimous support\u201d."),
    ("IRAN CLAIMS TWO US DRONES DOWNED \u2014",
     "the IRGC said it shot down an MQ-9 over Hormuz \u2014 its claimed 58th \u2014 and later an MQ-1 over Qeshm Island."),
]

# (number, place label, key text, lon, lat) — lon/lat nudged slightly where
# markers would otherwise collide at this scale; the Europe / Middle East
# cluster is spread wider than geography so no two markers touch.
MARKERS = [
    (1, "Antalya", "COP31 overtime", 24.0, 36.0),
    (2, "Kryvyi Rih", "triple-tap", 39.0, 50.5),
    (3, "Gaza City", "WCK killed", 33.5, 29.0),
    (4, "Geneva", "robot rules", 6.5, 45.5),
    (5, "Banda Sea", "M6.8 quake", 127.0, -8.5),
    (6, "Guasave", "cartel boss held", -108.5, 25.6),
    (7, "Hormuz", "tanker; drones", 58.5, 24.5),
    (8, "Madrid", "banking levy", -6.5, 39.0),
    (9, "Copenhagen", "attach\u00e9 out", 15.5, 58.0),
    (10, "Brussels", "3% digital tax", -1.5, 51.5),
    (11, "Florida", "floods worsen", -81.0, 28.5),
    (12, "Hanoi", "land-seizure law", 105.8, 21.0),
    (13, "Johannesburg", "tributes", 28.0, -26.2),
    (14, "Gulf of Finland", "Sparta II", 27.0, 61.5),
    (15, "Tehran", "\u201cout of NPT\u201d", 56.5, 41.0),
    (16, "Basra", "station fire", 50.5, 27.5),
    (17, "Seoul", "Choi gold", 127.0, 37.5),
    (18, "Melbourne", "T20; AFLW", 145.0, -37.8),
    (19, "Asunci\u00f3n", "backs Infantino", -57.6, -25.3),
]

# Coarse continent outlines (lon, lat), equirectangular.
CONTINENTS = [
    # North America
    [(-168, 66), (-158, 71), (-140, 70), (-128, 70), (-115, 68), (-105, 68),
     (-95, 69), (-85, 66), (-80, 73), (-70, 62), (-60, 60), (-65, 49),
     (-70, 45), (-75, 40), (-80, 32), (-81, 26), (-84, 30), (-90, 29),
     (-97, 26), (-97, 16), (-94, 17), (-90, 14), (-83, 9), (-79, 9),
     (-82, 15), (-87, 21), (-90, 21), (-97, 26), (-105, 23), (-110, 24),
     (-114, 29), (-117, 33), (-122, 37), (-124, 40), (-124, 48), (-130, 55),
     (-135, 58), (-150, 61), (-160, 58)],
    # South America
    [(-79, 9), (-77, 4), (-80, -3), (-81, -6), (-77, -12), (-70, -18),
     (-70, -23), (-70, -30), (-72, -37), (-73, -44), (-70, -52), (-68, -55),
     (-65, -55), (-62, -49), (-58, -42), (-57, -35), (-52, -32), (-48, -28),
     (-41, -23), (-35, -9), (-35, -5), (-44, -3), (-50, 0), (-52, 5),
     (-60, 8), (-68, 11), (-72, 12), (-77, 8)],
    # Africa
    [(-17, 15), (-16, 21), (-10, 31), (-5, 35), (0, 36), (10, 37), (11, 34),
     (20, 32), (30, 31), (32, 31), (35, 28), (37, 22), (39, 21), (43, 12),
     (48, 11), (51, 10), (46, 5), (41, 2), (40, -3), (39, -6), (40, -10),
     (35, -18), (33, -26), (28, -33), (20, -35), (17, -29), (15, -22),
     (12, -18), (13, -12), (9, -1), (9, 4), (-8, 4), (-13, 8)],
    # Europe
    [(-10, 36), (-9, 43), (-2, 48), (-4, 49), (0, 51), (3, 53), (8, 57),
     (10, 58), (5, 60), (5, 62), (12, 64), (18, 69), (25, 71), (30, 70),
     (32, 66), (28, 61), (24, 58), (21, 55), (19, 54), (14, 54), (12, 54),
     (8, 54), (3, 51), (0, 50), (-2, 47), (-1, 44), (-2, 37), (-6, 36),
     (-9, 37)],
    # UK
    [(-5, 50), (-3, 53), (-5, 56), (-3, 58), (-1, 57), (1, 53), (1, 51)],
    # Asia
    [(30, 70), (40, 68), (50, 69), (60, 69), (70, 72), (80, 73), (90, 75),
     (100, 77), (110, 74), (120, 73), (130, 71), (140, 72), (150, 70),
     (160, 70), (170, 67), (178, 65), (178, 62), (170, 60), (162, 56),
     (158, 52), (155, 59), (150, 59), (142, 54), (141, 48), (135, 44),
     (132, 43), (127, 40), (122, 38), (120, 35), (122, 30), (120, 28),
     (118, 25), (110, 20), (109, 18), (105, 10), (103, 8), (100, 7),
     (98, 10), (94, 17), (92, 21), (89, 22), (86, 20), (80, 15), (77, 8),
     (76, 10), (73, 20), (70, 21), (67, 25), (66, 25), (61, 25), (57, 26),
     (53, 27), (50, 29), (48, 30), (44, 29), (43, 26), (40, 31), (36, 36),
     (35, 36), (30, 36), (27, 37), (26, 38), (30, 40), (33, 42), (38, 42),
     (41, 43), (43, 44), (46, 47), (48, 46), (47, 42), (44, 40), (40, 42),
     (38, 44), (35, 47), (33, 50), (32, 55), (30, 60)],
    # Japan
    [(130, 31), (132, 34), (136, 35), (139, 35), (140, 38), (141, 40),
     (143, 42), (145, 44), (142, 45), (140, 40), (139, 37), (135, 34),
     (131, 32)],
    # Greenland
    [(-58, 64), (-52, 60), (-43, 60), (-40, 64), (-32, 68), (-22, 70),
     (-20, 74), (-30, 76), (-45, 76), (-58, 74), (-62, 70)],
    # Australia
    [(114, -22), (114, -28), (115, -33), (118, -35), (124, -33), (129, -32),
     (132, -32), (135, -35), (138, -35), (140, -38), (145, -38), (147, -38),
     (150, -37), (153, -31), (153, -27), (150, -23), (146, -19), (142, -15),
     (142, -11), (140, -17), (136, -15), (132, -12), (130, -13), (126, -14),
     (122, -17), (118, -20)],
    # New Zealand
    [(167, -45), (172, -41), (174, -37), (178, -38), (175, -40), (170, -43)],
]


# ---------------------------------------------------------------- drawing
WARNINGS = []


def section_header(draw, x, y, w, text):
    draw.text((x, y), text, font=F_SECTION, fill=INK)
    draw.line([(x, y + 19), (x + w, y + 19)], fill=RULE, width=2)
    return y + 26


def draw_brief(draw, x, y, head, body, width):
    """Bold head + regular body across at most 2 lines. Warns on overflow."""
    head = head.rstrip()
    hw = draw.textlength(head + " ", font=F_BRIEF_B)
    words = body.split()
    line1_words, used, idx = [], hw, 0
    for w in words:
        add = draw.textlength((" " if line1_words else "") + w, font=F_BRIEF)
        if used + add <= width:
            line1_words.append(w)
            used += add
            idx += 1
        else:
            break
    draw.text((x, y), head, font=F_BRIEF_B, fill=INK)
    if line1_words:
        draw.text((x + hw, y), " ".join(line1_words), font=F_BRIEF, fill=INK)
    rest = " ".join(words[idx:])
    if rest:
        rl = wrap(draw, rest, F_BRIEF, width)
        if len(rl) > 1:
            WARNINGS.append("brief overflow (3 lines): %s" % head)
        draw.text((x, y + 12), rl[0], font=F_BRIEF, fill=INK)


def draw_lead_art(d, idx, x, y, w, h, color):
    """Flat spot illustration for lead idx inside the (x, y, w, h) band.

    Simple geometric scenes only — globe + clock for the overtime COP31
    talks, skyline + blast star for the Kryvyi Rih strike, aid truck for
    the WCK vehicle — so the leads read pictorially, not as text alone.
    """
    import math
    if idx == 0:
        # COP31: globe, clock past the deadline, rising bars. Pale green.
        d.rectangle([x, y, x + w, y + h], fill=(227, 239, 223))
        cx, cy, r = x + 36, y + h // 2, 15
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(169, 205, 226),
                  outline=(46, 125, 50), width=2)
        d.ellipse([cx - 5, cy - r + 1, cx + 5, cy + r - 1],
                  outline=(46, 125, 50), width=1)
        d.line([(cx - r + 1, cy), (cx + r - 1, cy)], fill=(46, 125, 50), width=1)
        kx, ky, kr = x + 88, y + h // 2, 13
        d.ellipse([kx - kr, ky - kr, kx + kr, ky + kr], fill=(255, 255, 255),
                  outline=(26, 26, 26), width=2)
        d.line([(kx, ky), (kx, ky - kr + 3)], fill=(179, 38, 30), width=2)
        d.line([(kx, ky), (kx + kr - 5, ky + 4)], fill=(26, 26, 26), width=2)
        d.ellipse([kx - 2, ky - 2, kx + 2, ky + 2], fill=(26, 26, 26))
        base = y + h - 6
        for i, bh in enumerate((8, 13, 18, 24)):
            bx = x + 128 + i * 16
            d.rectangle([bx, base - bh, bx + 11, base],
                        fill=(46, 125, 50) if i < 3 else (179, 38, 30))
        d.text((x + w - 96, y + h - 14), "OVERTIME", font=F_LEAD_KICK,
               fill=(179, 38, 30))
    elif idx == 1:
        # Kryvyi Rih: city skyline under a blast star. Pale grey-red.
        d.rectangle([x, y, x + w, y + h], fill=(242, 228, 226))
        base = y + h - 4
        sky = [(8, 16), (26, 24), (44, 12), (62, 20), (82, 28), (102, 14),
               (122, 22), (142, 10), (162, 18), (182, 26), (202, 12)]
        for ox, bh in sky:
            d.rectangle([x + ox, base - bh, x + ox + 14, base],
                        fill=(90, 86, 76))
            d.rectangle([x + ox + 4, base - bh + 3, x + ox + 7, base - bh + 6],
                        fill=(248, 244, 233))
        sx, sy = x + 258, y + 15
        star = []
        for i in range(24):
            ang = math.pi * i / 12
            rr = 15 if i % 2 == 0 else 6
            star.append((sx + rr * math.cos(ang), sy + rr * math.sin(ang)))
        d.polygon(star, fill=(232, 126, 20), outline=(179, 38, 30))
        d.ellipse([sx - 4, sy - 4, sx + 4, sy + 4], fill=(179, 38, 30))
        for dx, dy in ((-38, 8), (-30, -6), (30, 10), (36, -4)):
            d.ellipse([sx + dx - 2, sy + dy - 2, sx + dx + 2, sy + dy + 2],
                      fill=(179, 38, 30))
    else:
        # WCK: aid truck with food parcels. Pale tan.
        d.rectangle([x, y, x + w, y + h], fill=(243, 236, 220))
        base = y + h - 8
        d.rectangle([x + 30, y + 8, x + 150, base - 6], fill=(255, 255, 255),
                    outline=(140, 90, 20), width=2)
        d.rectangle([x + 150, y + 18, x + 190, base - 6], fill=(255, 255, 255),
                    outline=(140, 90, 20), width=2)
        d.polygon([(x + 168, y + 22), (x + 186, y + 22), (x + 186, y + 30),
                   (x + 168, y + 30)], fill=(169, 205, 226))
        for wx in (62, 128, 172):
            d.ellipse([x + wx - 7, base - 13, x + wx + 7, base + 1],
                      fill=(26, 26, 26))
            d.ellipse([x + wx - 3, base - 9, x + wx + 3, base - 3],
                      fill=(248, 244, 233))
        d.text((x + 48, y + 13), "FOOD AID", font=F_LEAD_KICK,
               fill=(140, 90, 20))
        # stacked parcels + steam bowl at the right
        for ox, oy in ((0, 12), (14, 12), (7, 0)):
            d.rectangle([x + 218 + ox, y + 12 + oy, x + 230 + ox, y + 24 + oy],
                        fill=(205, 170, 110), outline=(140, 90, 20), width=1)
        d.arc([x + 258, y + 4, x + 272, y + 16], 200, 340,
              fill=(90, 86, 76), width=2)
        d.arc([x + 266, y + 4, x + 280, y + 16], 200, 340,
              fill=(90, 86, 76), width=2)
        d.polygon([(x + 256, y + 18), (x + 284, y + 18), (x + 278, y + 28),
                   (x + 262, y + 28)], fill=(255, 255, 255),
                  outline=(140, 90, 20))


def render():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead
    title = "THE WORLD TODAY"
    tw = d.textlength(title, font=F_TITLE)
    d.text(((W - tw) / 2, 10), title, font=F_TITLE, fill=INK)
    date_line = "SATURDAY 21 NOVEMBER 2026  ·  35 STORIES  ·  SIX CONTINENTS"
    dw = d.textlength(date_line, font=F_DATE)
    d.text(((W - dw) / 2, 60), date_line, font=F_DATE, fill=RED)
    d.line([(MARGIN, 84), (W - MARGIN, 84)], fill=INK, width=3)
    d.line([(MARGIN, 88), (W - MARGIN, 88)], fill=INK, width=1)

    # ---- leads (y 94 .. ~261): colour bar, spot art, kicker, head, body.
    # Sections below are positioned from the lead block's real end, so the
    # layout self-adjusts instead of relying on hardcoded y values.
    col_w = 320
    gap = 14
    lx = [MARGIN + i * (col_w + gap) for i in range(3)]
    ly = 94
    lead_end = ly
    for i, lead in enumerate(LEADS):
        x = lx[i]
        d.rectangle([x, ly, x + col_w, ly + 4], fill=lead["color"])
        draw_lead_art(d, i, x, ly + 4, col_w, 40, lead["color"])
        y = ly + 4 + 40 + 6
        d.text((x, y), lead["kick"], font=F_LEAD_KICK, fill=lead["color"])
        y += 15
        head_lines = wrap(d, lead["head"], F_LEAD_HEAD, col_w)
        if len(head_lines) > 2:
            WARNINGS.append("lead head overflow: %s" % lead["head"][:40])
        y = draw_lines(d, x, y, head_lines, F_LEAD_HEAD, leading=24)
        y += 2
        body_lines = wrap(d, lead["body"], F_LEAD_BODY, col_w)
        if len(body_lines) > 4:
            WARNINGS.append("lead body overflow: %s" % lead["head"][:40])
        y = draw_lines(d, x, y, body_lines, F_LEAD_BODY, leading=13)
        lead_end = max(lead_end, y)

    # ---- grid section (15 stories, 5 rows x 3 cols)
    gy = section_header(d, MARGIN, lead_end + 6, W - 2 * MARGIN,
                        "THE DAY IN BRIEF \u2014 15 STORIES")
    rows, cols = 5, 3
    cell_h = 52
    for r in range(rows):
        for c in range(cols):
            idx = r * cols + c
            if idx >= len(GRID):
                break
            x = MARGIN + c * (col_w + gap)
            y = gy + r * cell_h
            head, body = GRID[idx]
            hl = wrap(d, head, F_GRID_HEAD, col_w)
            if len(hl) > 1:
                WARNINGS.append("grid head wraps: %s" % head[:40])
            y2 = draw_lines(d, x, y, hl[:1], F_GRID_HEAD, leading=13)
            bl = wrap(d, body, F_GRID_BODY, col_w)
            if len(bl) > 3:
                WARNINGS.append("grid body overflow: %s" % head[:40])
            draw_lines(d, x, y2 + 1, bl[:3], F_GRID_BODY, leading=12)
    grid_end = gy + rows * cell_h

    # ---- map section (19 places, key in two columns of 10 + 9)
    my = section_header(d, MARGIN, grid_end + 8, W - 2 * MARGIN,
                        "WHERE THE NEWS HAPPENED \u2014 19 PLACES")
    map_x, map_y, map_w, map_h = MARGIN, my, 580, 160
    d.rectangle([map_x, map_y, map_x + map_w, map_y + map_h], fill=SEA,
                outline=RULE, width=1)
    lon0, lon1, lat0, lat1 = -170, 190, 75, -60

    def proj(lon, lat):
        px = map_x + (lon - lon0) / (lon1 - lon0) * map_w
        py = map_y + (lat0 - lat) / (lat0 - lat1) * map_h
        return px, py

    for poly in CONTINENTS:
        pts = [proj(lon, lat) for lon, lat in poly]
        d.polygon(pts, fill=LAND, outline=LAND_EDGE)
    _, ey = proj(0, 0)
    d.line([(map_x, ey), (map_x + map_w, ey)], fill=(190, 208, 224), width=1)

    for num, place, key, lon, lat in MARKERS:
        px, py = proj(lon, lat)
        r = 8.5
        d.ellipse([px - r - 2, py - r - 2, px + r + 2, py + r + 2],
                  fill=(255, 255, 255))
        d.ellipse([px - r, py - r, px + r, py + r], fill=RED,
                  outline=(255, 255, 255), width=1)
        label = str(num)
        lw = d.textlength(label, font=F_NUM)
        d.text((px - lw / 2, py - 6), label, font=F_NUM, fill=(255, 255, 255))

    # map key, two columns of ten + nine, 16px rows
    kx = map_x + map_w + 16
    kw = W - MARGIN - kx
    half = (kw - 12) // 2
    for i, (num, place, key, lon, lat) in enumerate(MARKERS):
        col = 0 if i < 10 else 1
        row = i % 10 if col == 0 else i - 10
        x = kx + col * (half + 12)
        y = map_y + 1 + row * 16
        d.ellipse([x, y + 1, x + 13, y + 14], fill=RED)
        label = str(num)
        lw = d.textlength(label, font=F_NUM)
        d.text((x + (13 - lw) / 2, y + 1), label, font=F_NUM,
               fill=(255, 255, 255))
        d.text((x + 17, y), place, font=F_KEY_B, fill=INK)
        pw = d.textlength(place + " ", font=F_KEY_B)
        key_w = pw + d.textlength("\u2014 " + key, font=F_KEY)
        if 17 + key_w > half:
            WARNINGS.append("key line too wide: %s" % place)
        d.text((x + 17 + pw, y), "\u2014 " + key, font=F_KEY, fill=MUTED)
    map_end = map_y + map_h

    # ---- briefs section (17 briefs, 2 columns of 9 + 8)
    by = section_header(d, MARGIN, map_end + 8, W - 2 * MARGIN,
                        "MORE FROM SATURDAY \u2014 17 BRIEFS")
    bcol_w = (W - 2 * MARGIN - 20) // 2
    row_h = 23
    for i, (head, body) in enumerate(BRIEFS):
        col = 0 if i < 9 else 1
        row = i % 9
        x = MARGIN + col * (bcol_w + 20)
        y = by + row * row_h
        draw_brief(d, x, y, head, body, bcol_w)
    briefs_end = by + 9 * row_h

    # ---- footer (one line)
    fy = briefs_end + 6
    d.line([(MARGIN, fy), (W - MARGIN, fy)], fill=RULE, width=1)
    foot = ("Sources: Reuters, AP, BBC, CNN, Al Jazeera, NYT, AFP, Ukrinform, ESA, "
            "UKMTO, FIFA, Yonhap, AAP \u2014 all stories verified from reporting "
            "published Saturday 21 November 2026.")
    fl = wrap(d, foot, F_FOOT, W - 2 * MARGIN)
    if len(fl) > 1:
        WARNINGS.append("footer wraps to %d lines" % len(fl))
    draw_lines(d, MARGIN, fy + 5, fl, F_FOOT, fill=MUTED, leading=12)
    if fy + 5 + len(fl) * 12 > H - 4:
        WARNINGS.append("footer overflows bottom edge")

    out = os.path.join(HERE, "entry.png")
    img.save(out, "PNG", optimize=True)
    print("saved", out, img.size, os.path.getsize(out), "bytes")
    for w in WARNINGS:
        print("WARNING:", w)
    print("stories:", len(LEADS) + len(GRID) + len(BRIEFS),
          "| markers:", len(MARKERS))


if __name__ == "__main__":
    render()
