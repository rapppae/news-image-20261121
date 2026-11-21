"""Render the 21 November 2026 world-news poster as a 1024x1024 PNG.

Local build tool only: the graded entrypoint (main.py) is stdlib-only
and copies the PNG this file produces. All poster content lives in the
DATA tables near the bottom; the code above them only lays a newspaper
page out: masthead, lead story with a market chart, a 2x2 story grid,
an also-today strip and a footer. No clock, no randomness, fonts ship
in assets/, so repeated runs produce identical bytes.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

SIZE = 1024
PAD = 40
GAP = 28
HALF = (SIZE - 2 * PAD - GAP) // 2

C = dict(
    paper=(245, 240, 225),
    navy=(26, 35, 64),
    deep=(18, 25, 48),
    gold=(212, 175, 55),
    pale=(232, 200, 90),
    red=(178, 34, 52),
    teal=(0, 128, 128),
    ink=(30, 30, 34),
    grey=(110, 110, 105),
    white=(255, 255, 255),
    rule=(200, 192, 172),
)

ROOT = Path(__file__).resolve().parent
ASSET_DIR = ROOT / "assets"


def load_fonts():
    def at(name, size):
        return ImageFont.truetype(str(ASSET_DIR / name), size)

    bold, plain = "LiberationSans-Bold.ttf", "DejaVuSans.ttf"
    return {
        "eyebrow": at(bold, 27),
        "date": at(bold, 56),
        "kicker": at(bold, 21),
        "headline": at(bold, 48),
        "body": at(plain, 21),
        "ticker": at(bold, 62),
        "move": at(bold, 23),
        "prices": at(plain, 17),
        "card_kicker": at(bold, 18),
        "card_head": at(bold, 27),
        "card_body": at(plain, 20),
        "strip_title": at(bold, 21),
        "strip_item": at(plain, 19),
        "footer": at(plain, 17),
        "icon_label": at(bold, 22),
    }


def wrap_text(cv, text, font, width):
    """Greedy word wrap: lines that fit `width` pixels."""
    words = text.split()
    lines, i = [], 0
    while i < len(words):
        line = words[i]
        i += 1
        while i < len(words) and cv.textlength(line + " " + words[i], font=font) <= width:
            line += " " + words[i]
            i += 1
        lines.append(line)
    return lines


def letter_spaced(cv, x, y, text, font, fill):
    """Draw text with extra tracking between characters."""
    for ch in text:
        cv.text((x, y), ch, font=font, fill=fill)
        x += cv.textlength(ch, font=font) + 6


def skyline(cv, box, towers):
    """Night skyline along the bottom of `box`, with lit windows."""
    l, t, r, b = box
    pw, ph = r - l, b - t
    for fx, fw, fh in towers:
        x = l + fx * pw
        w, h = fw * pw, fh * ph
        top = b - h
        cv.rectangle((x, top, x + w, b), fill=C["deep"])
        nx, ny = max(1, int(w // 22)), max(1, int(h // 24))
        for i in range(nx):
            for j in range(ny):
                if (i * 2 + j) % 3 == 0:
                    cv.rectangle(
                        (x + 6 + i * 22, top + 8 + j * 24,
                         x + 13 + i * 22, top + 17 + j * 24),
                        fill=C["pale"],
                    )


def chart_panel(cv, ft, box):
    """Navy panel: ticker, day-two move, prices, falling line, skyline."""
    l, t, r, b = box
    w, h = r - l, b - t
    cv.rectangle(box, fill=C["navy"])
    cv.text((l + 22, t + 8), CHART_TICKER, font=ft["ticker"], fill=C["gold"])
    cv.text((l + 22, t + 82), CHART_MOVE, font=ft["move"], fill=C["white"])
    cv.text((l + 22, t + 112), CHART_PRICES, font=ft["prices"], fill=C["white"])
    skyline(cv, (l, b - 90, r, b), CHART_TOWERS)
    # the line sits below the ticker/move/prices text, over the skyline
    pts = [(l + fx * w, t + 140 + fy * (h - 170)) for fx, fy in CHART_LINE]
    cv.line(pts, fill=C["gold"], width=4)
    for px, py in pts:
        cv.ellipse((px - 5, py - 5, px + 5, py + 5), fill=C["gold"])


def glyph(cv, ft, kind, box):
    """Small white/gold glyph on a navy square."""
    l, t, r, b = box
    cv.rectangle(box, fill=C["navy"])
    cx, cy = (l + r) // 2, (t + b) // 2
    if kind == "scales":
        cv.line((cx, t + 12, cx, b - 14), fill=C["gold"], width=3)
        cv.line((l + 12, t + 22, r - 12, t + 22), fill=C["gold"], width=3)
        for sx in (l + 14, r - 34):
            cv.line((sx + 8, t + 22, sx, t + 44), fill=C["gold"], width=2)
            cv.line((sx + 8, t + 22, sx + 16, t + 44), fill=C["gold"], width=2)
            cv.line((sx, t + 44, sx + 16, t + 44), fill=C["gold"], width=2)
        cv.line((l + 16, b - 14, r - 16, b - 14), fill=C["gold"], width=3)
    elif kind == "falling":
        tag = "AI"
        tw = cv.textlength(tag, font=ft["icon_label"])
        cv.text((cx - tw / 2, t + 6), tag, font=ft["icon_label"], fill=C["gold"])
        hs = (40, 30, 20)
        bw = 14
        x = cx - (len(hs) * bw + (len(hs) - 1) * 8) / 2
        for h in hs:
            cv.rectangle((x, b - 10 - h, x + bw, b - 10), fill=C["gold"])
            x += bw + 8
    elif kind == "missile":
        cv.line((l + 22, b - 22, r - 22, t + 22), fill=C["white"], width=7)
        cv.polygon(((r - 22, t + 22), (r - 8, t + 26), (r - 26, t + 8)), fill=C["gold"])
        cv.line((l + 22, b - 22, l + 34, b - 34), fill=C["gold"], width=3)
        cv.line((l + 22, b - 22, l + 10, b - 10), fill=C["gold"], width=3)
        cv.ellipse((l + 8, b - 18, l + 20, b - 6), fill=C["gold"])
    elif kind == "globe":
        cv.ellipse((l + 12, t + 12, r - 12, b - 12), outline=C["white"], width=3)
        cv.ellipse((cx - 13, t + 12, cx + 13, b - 12), outline=C["white"], width=2)
        cv.line((l + 12, cy, r - 12, cy), fill=C["white"], width=2)
        cv.arc((l + 12, t + 28, r - 12, b - 28), start=200, end=340, fill=C["white"], width=2)
        cv.ellipse((r - 26, t + 16, r - 14, t + 28), fill=C["gold"])


def story_card(cv, ft, box, story):
    """One white card: icon, kicker, two-line headline, two-line body."""
    l, t, r, b = box
    kind, kicker, head, body = story
    cv.rectangle(box, fill=C["white"], outline=C["rule"], width=1)
    cv.rectangle((l, t, r, t + 8), fill=C["teal"])
    glyph(cv, ft, kind, (l + 16, t + 16, l + 100, t + 100))
    tx = l + 112
    cv.text((tx, t + 20), kicker, font=ft["card_kicker"], fill=C["red"])
    y = t + 45
    for ln in head:
        cv.text((tx, y), ln, font=ft["card_head"], fill=C["ink"])
        y += 29
    y = t + 105
    for ln in wrap_text(cv, body, ft["card_body"], r - l - 28)[:2]:
        cv.text((l + 14, y), ln, font=ft["card_body"], fill=C["ink"])
        y += 24


def also_strip(cv, ft, box):
    """Navy strip with four short items in two columns."""
    l, t, r, b = box
    cv.rectangle(box, fill=C["navy"])
    cv.text((l + 16, t + 16), "ALSO TODAY", font=ft["strip_title"], fill=C["gold"])
    cw = (r - l - 32) // 2
    for n, item in enumerate(ALSO_TODAY):
        col, row = divmod(n, 2)
        ix = l + 16 + col * cw
        iy = t + 48 + row * 28
        cv.rectangle((ix, iy + 6, ix + 7, iy + 13), fill=C["gold"])
        cv.text((ix + 16, iy), item, font=ft["strip_item"], fill=C["white"])


# --- poster data: every story on the page, as reported 21 November 2026 ---

EYEBROW = "THE WORLD IN ONE DAY"
DATE = "SATURDAY, 21 NOVEMBER 2026"
LEAD_KICKER = "POLAND  \u00b7  NATO"
LEAD_HEAD = ["Russian missile", "lands in Poland"]
LEAD_BODY = (
    "A Kh-101 cruise missile came down 60 km inside Poland during "
    "Russia's biggest attack on Ukraine. PM Tusk calls it an "
    "\u201cintentional provocation\u201d; NATO's Rutte: a \u201cgrave violation\u201d."
)

CHART_TICKER = "ANT"
CHART_MOVE = "\u22128.5% ON DAY TWO"
CHART_PRICES = "$83 IPO  \u2192  $111.50 open  \u2192  $88.91 close"
# normalised (x, y) in panel coordinates, 0..1 across / 0..1 down;
# a falling line: the IPO pop gives it all back on day two
CHART_LINE = (
    (0.03, 0.35), (0.14, 0.42), (0.24, 0.38), (0.36, 0.50),
    (0.50, 0.58), (0.63, 0.68), (0.76, 0.76), (0.88, 0.84), (0.97, 0.92),
)
# (x0, w, h) fractions of panel width/height, windows as (col, row) grid
CHART_TOWERS = (
    (0.02, 0.11, 0.85), (0.15, 0.12, 0.65), (0.29, 0.13, 0.90),
    (0.44, 0.12, 0.70), (0.58, 0.11, 0.88), (0.71, 0.12, 0.62),
    (0.85, 0.12, 0.80),
)

# (icon, kicker, headline lines, body)
STORIES = (
    (
        "missile",
        "WAR  \u00b7  UKRAINE",
        ("400 drones, 110 missiles", "rain on Ukraine"),
        "The overnight barrage kills at least 8; three die in Kyiv as bridges are hit.",
    ),
    (
        "falling",
        "MARKETS  \u00b7  AI",
        ("The AI sell-off goes", "global"),
        "Asia posts its worst week since Covid; Taiwan's worst since the early 1990s.",
    ),
    (
        "globe",
        "DIPLOMACY  \u00b7  PEACE TALKS",
        ("Kushner floats NATO", "path for Kyiv"),
        "The US envoy floats NATO membership if Kyiv cedes land; Trump joins allied talks.",
    ),
    (
        "scales",
        "JUSTICE  \u00b7  THE HAGUE",
        ("Thaci guilty, jailed", "17 months"),
        "Kosovo's ex-president is convicted of obstructing justice in his war-crimes trial.",
    ),
)

ALSO_TODAY = (
    "EU adopts \u20ac1bn in military aid for Ukraine",
    "Tanker struck and on fire in Strait of Hormuz",
    "Kerch Bridge badly damaged in strikes",
    "US Senate rejects Iran war-powers bid 51\u201348",
)

FOOTER = "All stories as reported on 21 November 2026  \u00b7  Sources: Reuters, AP, WSJ, BBC, IBD, NY Post"


def render(path):
    """Lay the page out and save it as a PNG."""
    img = Image.new("RGB", (SIZE, SIZE), C["paper"])
    cv = ImageDraw.Draw(img)
    ft = load_fonts()

    # masthead
    cv.rectangle((0, 0, SIZE, 138), fill=C["navy"])
    letter_spaced(cv, PAD, 30, EYEBROW, ft["eyebrow"], C["gold"])
    cv.text((PAD, 66), DATE, font=ft["date"], fill=C["white"])
    cv.rectangle((0, 138, SIZE, 144), fill=C["gold"])

    # lead story, left column; chart panel, right column
    cv.text((PAD, 185), LEAD_KICKER, font=ft["kicker"], fill=C["red"])
    y = 226
    for ln in LEAD_HEAD:
        cv.text((PAD, y), ln, font=ft["headline"], fill=C["ink"])
        y += 48
    y = 374
    for ln in wrap_text(cv, LEAD_BODY, ft["body"], 505):
        cv.text((PAD, y), ln, font=ft["body"], fill=C["ink"])
        y += 29
    chart_panel(cv, ft, (584, 140, 984, 420))

    # divider
    cv.line((PAD, 486, SIZE - PAD, 486), fill=C["rule"], width=2)

    # story grid: 2 columns x 2 rows
    for n, story in enumerate(STORIES):
        row, col = divmod(n, 2)
        x = PAD + col * (HALF + GAP)
        yy = 500 + row * (166 + 16)
        story_card(cv, ft, (x, yy, x + HALF, yy + 166), story)

    # also-today strip + footer
    also_strip(cv, ft, (PAD, 862, SIZE - PAD, 958))
    cv.text((PAD, 974), FOOTER, font=ft["footer"], fill=C["grey"])

    img.save(path, format="PNG")
    return path
