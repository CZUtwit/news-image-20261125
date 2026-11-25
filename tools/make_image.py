#!/usr/bin/env python3
"""Build entry.png for news-image-20261125: The World in One Day — 25 Nov 2026.

Champion-format broadsheet: masthead, deck, region chips, 13 main stories,
ALSO list, HOW SURE legend, dotted world map, DATE CHECK, numbers + UTC
timeline. Pure Pillow, no network, deterministic output.
Run: python3 tools/make_image.py  (writes entry.png next to this repo root)
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "entry.png")

W, H = 1024, 1024
M = 28                      # outer margin
CW = W - 2 * M              # content width 968

PAPER = (247, 243, 234)     # warm off-white
INK = (24, 24, 22)
RED = (178, 34, 34)
GREY = (110, 108, 100)
LGREY = (200, 196, 186)
CARD_BG = (255, 255, 255)
CHIP_BG = (232, 227, 214)
MAP_DOT = (178, 172, 158)

def font(name, size):
    return ImageFont.truetype(f"/usr/share/fonts/truetype/dejavu/{name}.ttf", size)

F_TITLE = font("DejaVuSans-Bold", 23)
F_DATE = font("DejaVuSans-Bold", 15)
F_DECK = font("DejaVuSans-Bold", 18)
F_CHIP = font("DejaVuSans-Bold", 11)
F_H = font("DejaVuSans-Bold", 15)
F_PLACE = font("DejaVuSans-Bold", 11)
F_STITLE = font("DejaVuSans-Bold", 13)
F_BODY = font("DejaVuSans", 11)
F_SRC = font("DejaVuSans", 10)
F_BADGE = font("DejaVuSans-Bold", 9)
F_ALSO = font("DejaVuSans", 10)
F_ALSO_B = font("DejaVuSans-Bold", 10)
F_DC = font("DejaVuSans", 10)
F_DC_B = font("DejaVuSans-Bold", 10)
F_FOOT = font("DejaVuSans", 10)
F_FOOT_B = font("DejaVuSans-Bold", 10)

MAIN = [
    ("01", "ADEN", "CONFLICT", "Houthis close in on Aden",
     "Houthi fighters are amassing about 50 miles north of Yemen's temporary capital as residents and aid groups prepare to flee.",
     "Daily Summary", "REPORTED"),
    ("02", "CANBERRA", "DIPLOMACY", "Solomon Islands signs security pact with Australia",
     "The treaty names Canberra the primary security partner, with no foreign military bases \u2014 a turn from Honiara's China pact.",
     "Reuters", "REPORTED"),
    ("03", "JIUQUAN", "SPACE", "Shenzhou-24 docks with Pakistan's first astronaut",
     "The crewship lifted off at 08:18 and docked with Tiangong hours later. Muhammad Zeeshan Ali is the first foreigner to visit.",
     "Reuters \u00b7 Xinhua", "REPORTED"),
    ("04", "CARTAGENA", "CRIME", "All hostages freed as troops storm supermarket",
     "Special forces ended a day-long siege at an \u00c9xito store at about 1am, freeing some 20 hostages. One gunman was killed, four detained.",
     "Reuters \u00b7 AFP", "REPORTED"),
    ("05", "PYONGYANG", "DIPLOMACY", "North Korea orders Swiss office shut, expels envoy",
     "Pyongyang gave envoy Astier Sylvain 48 hours to leave after Bern sanctioned the Songdowon camp over Ukrainian children.",
     "Daily Summary", "REPORTED"),
    ("06", "KYIV", "WAR & AID", "Ukraine says it needs \u20ac115bn for 2027",
     "Zelensky said Kyiv has \u20ac90bn in EU commitments secured and is hunting for the remaining \u20ac25bn to fund the economy and war effort.",
     "Daily Summary", "REPORTED"),
    ("07", "TOKYO", "MARKETS", "Asian tech stocks tumble on AI-boom doubts",
     "The Nikkei fell 2.8%, South Korea 5.3% and Taiwan 5.1% as fresh US tariff threats hit sentiment and the chip rally fizzled.",
     "Reuters", "REPORTED"),
    ("08", "HODEIDAH", "CONFLICT", "Saudi-led coalition says it hit Hodeidah port",
     "Spokesman Turki al-Maliki said the coalition struck port facilities and targets in Saada and Amran after Houthi threats to Saudi ports.",
     "Daily Summary", "REPORTED"),
    ("09", "RIYADH", "CONFLICT", "Houthis say they hit Saudi refinery, Riyadh district",
     "The group claimed strikes on the Ras Tanura refinery and the capital's financial district; the coalition said it downed four drones.",
     "Reuters", "CLAIM"),
    ("10", "DHAKA", "LABOUR", "Bangladesh raises garment wage 36% to 17,000 taka",
     "The wage board decided the rise after a 12-hour meeting; it takes effect 1 December. Workers had demanded a doubling.",
     "Reuters \u00b7 AP", "REPORTED"),
    ("11", "CANBERRA", "ECONOMY", "Australia's inflation jumps to 4.9%",
     "October CPI rose from 4.3%, with the trimmed mean at 3.8%, as fuel and clothing prices climbed. The cash rate stands at 4.85%.",
     "ABS", "REPORTED"),
    ("12", "SYDNEY", "COURTS", "Ex-officer guilty of double murder",
     "Beau Lamarre-Condon, 31, was convicted of murdering Jesse Baird, 26, and Luke Davies, 29, in February 2024. Sentencing is March 2027.",
     "Reuters", "REPORTED"),
    ("13", "WASHINGTON", "TECH & POLITICS", "Lawmakers question Trump's role in Huang's return",
     "Nvidia's chief is due to testify before a Senate panel as Congress probes his reinstatement after an 11-day absence.",
     "Reuters", "REPORTED"),
]

ALSO = [
    ("HONG KONG", "Tai Po fire: 1 year on, 168 mourned"),
    ("VIENNA", "Brent $90.97 as OPEC+ meets 29 Nov"),
    ("WASHINGTON", "US tariffs on 16 economies (reported)"),
    ("SHANGHAI", "Leaders pledge loyalty after Chen probe"),
    ("GAZA CITY", "Second Hamas security chief killed (claim)"),
    ("WEST JAVA", "Hunt for dozens in flooded gold mine"),
    ("SEOUL", "SK chief's ex-wife rejects divorce deal"),
    ("KYIV", "Zelensky: Russia readying new strikes"),
    ("AMMAN", "Jordan sentences man to death over attack"),
    ("ATHENS", "Greeks strike over wages, services"),
    ("WASHINGTON", "US shelves Russia deal plan (reported)"),
    ("BAMAKO", "Sahel rebels turn to cheap drones"),
    ("RIYADH", "Saudi 2027 budget: $370bn spending"),
    ("NEW YORK", "Bitcoin slips 1% to $59,258"),
]

CHIPS = [("MIDDLE EAST", 6), ("EAST ASIA", 6), ("OCEANIA & S. ASIA", 5),
         ("EUROPE", 3), ("AMERICAS", 5), ("AFRICA", 1), ("ENERGY", 1)]

# dotted-map land ranges: (row, x0, x1) on a 64 x 26 grid
LAND = [
    (1, 3, 10), (1, 23, 27),
    (2, 2, 14), (2, 22, 28), (2, 32, 36), (2, 40, 62),
    (3, 2, 18), (3, 23, 27), (3, 30, 38), (3, 39, 63),
    (4, 2, 20), (4, 30, 39), (4, 39, 63),
    (5, 3, 19), (5, 31, 38), (5, 40, 62),
    (6, 4, 18), (6, 31, 37), (6, 41, 61),
    (7, 5, 17), (7, 31, 36), (7, 42, 60),
    (8, 6, 16), (8, 31, 38), (8, 43, 58),
    (9, 7, 14), (9, 29, 41), (9, 44, 57),
    (10, 8, 13), (10, 29, 41), (10, 45, 56),
    (11, 11, 14), (11, 30, 40), (11, 46, 55),
    (12, 18, 26), (12, 30, 40), (12, 50, 57),
    (13, 18, 26), (13, 31, 39), (13, 52, 57),
    (14, 18, 25), (14, 31, 38), (14, 52, 56),
    (15, 19, 24), (15, 32, 37),
    (16, 19, 24), (16, 32, 37), (16, 52, 58),
    (17, 20, 24), (17, 33, 37), (17, 52, 59),
    (18, 20, 23), (18, 33, 36), (18, 52, 58),
    (19, 20, 23), (19, 34, 36), (19, 53, 57),
    (20, 21, 23), (20, 34, 36), (20, 53, 56),
    (21, 21, 22), (21, 34, 35),
    (22, 21, 22), (23, 21, 22), (24, 21, 22),
]
PINS = [  # (lon, lat) of the 13 main stories
    (45.0, 12.8), (149.1, -35.3), (98.5, 39.8), (-75.5, 10.4),
    (125.8, 39.0), (30.5, 50.4), (139.7, 35.7), (42.8, 14.8),
    (46.7, 24.7), (90.4, 23.8), (151.2, -33.9), (114.2, 22.3),
    (-77.0, 38.9),
]

DATE_CHECK = ("NOT TODAY \u2014 first reported earlier: Huawei guilty verdict \u00b7 Chen Jining probe \u00b7 "
              "Abrego Garcia leaves US \u00b7 Tidal AI-music ban \u00b7 Broadcom's 23 VMware flaws \u00b7 UNAIDS HIV report \u00b7 "
              "Democrats' 259 House seats \u00b7 Giuliani Medal of Freedom \u00b7 Xiamen's 50 Boeing jets \u00b7 "
              "Cameroon separatist trial \u00b7 SpaceX USSF-266 \u00b7 Canada Para hockey 10\u20130 \u2014 all Tuesday 24 Nov.")
NUMBERS_LINE = ("THE DAY IN NUMBERS:  27 stories  \u00b7  7 regions  \u00b7  \u20ac115bn Ukraine need  "
                "\u00b7  17,000 taka wage  \u00b7  \u22125.3% KOSPI")
TIMELINE_LINE = ("UTC: 00:00 Aden \u00b7 00:18 Shenzhou-24 \u00b7 01:19 Kyiv \u00b7 02:21 Hodeidah "
                 "\u00b7 03:56 Docking \u00b7 04:50 Pyongyang \u00b7 06:00 Cartagena")


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead bar ----
    d.rectangle([0, 0, W, 44], fill=INK)
    d.text((M, 11), "THE WORLD IN ONE DAY", font=F_TITLE, fill=(250, 247, 240))
    dt = "WEDNESDAY \u00b7 25 NOVEMBER 2026"
    d.text((W - M - d.textlength(dt, font=F_DATE), 14), dt, font=F_DATE, fill=(250, 247, 240))

    # ---- deck ----
    d.text((M, 50), "Houthis close on Aden \u00b7 Shenzhou-24 docks \u00b7 Canberra signs Solomons pact",
           font=F_DECK, fill=RED)

    # ---- region chips ----
    y = 76
    x = M
    for name, n in CHIPS:
        label = f"{name}  {n}"
        w = d.textlength(label, font=F_CHIP) + 18
        d.rounded_rectangle([x, y, x + w, y + 24], radius=12, fill=CHIP_BG)
        d.text((x + 9, y + 6), label, font=F_CHIP, fill=INK)
        x += w + 8

    # ---- main stories header ----
    y = 108
    d.text((M, y), "THE 13 MAIN STORIES", font=F_H, fill=INK)
    d.line([(M + 218, y + 10), (W - M, y + 10)], fill=INK, width=2)

    # ---- main cards: 2 columns, 7 left / 6 right, pitch 84 ----
    col_w = (CW - 16) // 2
    card_h = 84
    top = 130
    for i, (num, place, cat, title, body, src, status) in enumerate(MAIN):
        col = 0 if i < 7 else 1
        row = i if i < 7 else i - 7
        x0 = M + col * (col_w + 16)
        y0 = top + row * card_h
        d.rectangle([x0, y0, x0 + col_w, y0 + card_h - 6], fill=CARD_BG)
        d.rectangle([x0, y0, x0 + 4, y0 + card_h - 6], fill=RED if i % 2 == 0 else INK)
        tx = x0 + 12
        d.text((tx, y0 + 5), f"{num} \u00b7 {place} \u2014 {cat}", font=F_PLACE, fill=RED)
        bw = d.textlength(status, font=F_BADGE) + 10
        bx = x0 + col_w - bw - 8
        d.rounded_rectangle([bx, y0 + 4, bx + bw, y0 + 18], radius=7,
                            fill=(232, 227, 214) if status == "REPORTED" else (250, 225, 200))
        d.text((bx + 5, y0 + 6), status, font=F_BADGE, fill=INK)
        d.text((tx, y0 + 20), title, font=F_STITLE, fill=INK)
        blines = wrap(d, body, F_BODY, col_w - 24)
        by = y0 + 38
        for ln in blines[:2]:
            d.text((tx, by), ln, font=F_BODY, fill=(60, 58, 52))
            by += 14
        d.text((tx, y0 + 66), f"Source: {src}", font=F_SRC, fill=GREY)

    # ---- ALSO section: 3 columns, 5 rows ----
    y = 726
    d.text((M, y), "ALSO TODAY \u2014 14 MORE", font=F_H, fill=INK)
    d.line([(M + 200, y + 10), (W - M, y + 10)], fill=INK, width=2)
    acol_w = (CW - 2 * 14) // 3
    ay = 750
    for i, (place, head) in enumerate(ALSO):
        col = i % 3
        row = i // 3
        x0 = M + col * (acol_w + 14)
        yy = ay + row * 18
        d.text((x0, yy), place, font=F_ALSO_B, fill=RED)
        px = x0 + d.textlength(place, font=F_ALSO_B) + 5
        d.text((px, yy), f"\u2014 {head}", font=F_ALSO, fill=INK)

    # ---- HOW SURE legend, full width ----
    fy = 848
    d.text((M, fy), "HOW SURE:  ", font=F_FOOT_B, fill=INK)
    fx = M + d.textlength("HOW SURE:  ", font=F_FOOT_B)
    foot = ("REPORTED \u2014 same-day wire or official report   \u00b7   CLAIM \u2014 one side's account, flagged   "
            "\u00b7   ONGOING \u2014 still developing   \u00b7   All stories first reported 25 November 2026 (UTC).")
    d.text((fx, fy), foot, font=F_FOOT, fill=GREY)

    # ---- bottom band: map + DATE CHECK ----
    y = 862
    d.line([(M, y), (W - M, y)], fill=LGREY, width=1)
    d.text((M, 870), "WHERE IT HAPPENED \u2014 13 MAIN STORIES", font=F_DC_B, fill=INK)
    dx = M + 316
    d.text((dx, 870), "DATE CHECK", font=F_DC_B, fill=RED)
    # dotted world map, left
    map_x0, map_y0 = M, 888
    mw, mh = 300, 112
    cell_w, cell_h = mw / 64.0, mh / 26.0
    land_cells = set()
    for (r, a, b) in LAND:
        for cx in range(a, b + 1):
            land_cells.add((cx, r))
    for (cx, r) in land_cells:
        px = map_x0 + (cx + 0.5) * cell_w
        py = map_y0 + (r + 0.5) * cell_h
        d.ellipse([px - 1.6, py - 1.6, px + 1.6, py + 1.6], fill=MAP_DOT)
    for (lon, lat) in PINS:
        gx = (lon + 180.0) / 360.0 * 64.0
        gy = (90.0 - lat) / 150.0 * 26.0
        px = map_x0 + gx * cell_w
        py = map_y0 + gy * cell_h
        d.ellipse([px - 3.4, py - 3.4, px + 3.4, py + 3.4], fill=RED)
        d.ellipse([px - 1.4, py - 1.4, px + 1.4, py + 1.4], fill=(255, 255, 255))
    # DATE CHECK + numbers + timeline, right
    dw = W - M - dx
    dlines = wrap(d, DATE_CHECK, F_DC, dw)
    dy = 888
    for ln in dlines:
        d.text((dx, dy), ln, font=F_DC, fill=(60, 58, 52))
        dy += 13
    dy += 6
    d.text((dx, dy), NUMBERS_LINE, font=F_DC_B, fill=INK)
    dy += 16
    d.text((dx, dy), TIMELINE_LINE, font=F_DC, fill=(60, 58, 52))

    img.save(OUT, optimize=True)
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
