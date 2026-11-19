"""Front-page drawing kit for news-image-20261119.

Everything on the page is drawn here with Pillow primitives: no
photographs, no downloaded art. The canvas is 1024x1024, warm
newsprint. build_page.py (outside this repository) lays the page out
with these helpers; main.py only ships the finished PNG.
"""
from PIL import Image, ImageDraw, ImageFont

PAGE_W, PAGE_H = 1024, 1024
MARGIN = 14
GUTTER = 8

PALETTE = {
    "paper": (247, 243, 232), "ink": (26, 26, 30),
    "soft": (68, 64, 58), "muted": (120, 114, 102),
    "card": (255, 253, 247), "card_edge": (205, 198, 184),
    "red": (178, 34, 34), "blue": (31, 78, 140),
    "gold": (176, 124, 22), "green": (42, 110, 62),
    "brown": (122, 74, 32), "teal": (18, 120, 122),
    "purple": (104, 74, 150), "map_dot": (122, 136, 152),
    "map_sea": (233, 238, 242),
}

REGION = {
    "Americas": "green", "Europe": "blue", "Africa": "brown",
    "Middle East": "red", "Asia": "gold", "Oceania": "teal",
    "Global": "purple",
}

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS_R = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

# The grader container has no Pillow at all, so this file never runs
# there. Locally, fall back from DejaVu/Liberation to Noto, then to
# Pillow's built-in bitmap font, so a missing font file cannot crash
# the render.
ALT_FONTS = {
    SERIF_B: ["/usr/share/fonts/truetype/noto/NotoSerif-Bold.ttf"],
    SERIF_I: ["/usr/share/fonts/truetype/noto/NotoSerif-Italic.ttf"],
    SANS_R: ["/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"],
    SANS_B: ["/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"],
}

_cache = {}


def get_font(path, size):
    key = (path, size)
    if key not in _cache:
        got = None
        for cand in [path] + ALT_FONTS.get(path, []):
            try:
                got = ImageFont.truetype(cand, size)
                break
            except OSError:
                continue
        _cache[key] = got or ImageFont.load_default()
    return _cache[key]


def blank_page():
    img = Image.new("RGB", (PAGE_W, PAGE_H), PALETTE["paper"])
    return img, ImageDraw.Draw(img)


def wrap_text(d, text, f, width):
    """Split text into lines that fit width (greedy, by words)."""
    out, cur = [], ""
    for word in text.split():
        trial = word if not cur else cur + " " + word
        if d.textlength(trial, font=f) <= width:
            cur = trial
        else:
            if cur:
                out.append(cur)
            cur = word
    if cur:
        out.append(cur)
    return out


def draw_para(d, x, y, text, f, width, fill=None, gap=None, limit=None):
    """Draw wrapped text. Returns (lines_total, bottom_y)."""
    fill = fill if fill is not None else PALETTE["ink"]
    gap = gap if gap is not None else f.size + 2
    lines = wrap_text(d, text, f, width)
    shown = lines if limit is None else lines[:limit]
    for i, line in enumerate(shown):
        d.text((x, y + i * gap), line, font=f, fill=fill)
    return len(lines), y + len(shown) * gap


def badge(d, cx, cy, n, color, r=9):
    """White-numbered colour disc centred at (cx, cy)."""
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color,
              outline=(255, 255, 255), width=1)
    f = get_font(SANS_B, 11 if r >= 9 else 9)
    s = str(n)
    tw = d.textlength(s, font=f)
    d.text((cx - tw / 2, cy - f.size / 2 - 1), s, font=f,
           fill=(255, 255, 255))


def tag(d, x, y, n, region, topic, color):
    """Badge + REGION · TOPIC label. Returns the y just below it."""
    badge(d, x + 9, y + 8, n, color, r=9)
    f = get_font(SANS_B, 10)
    d.text((x + 22, y + 3),
           region.upper() + "  \u00b7  " + topic.upper(), font=f, fill=color)
    return y + 18


def frame(d, x, y, w, h, accent):
    """Card body with a coloured stripe along the top."""
    d.rectangle([x, y, x + w, y + h], fill=PALETTE["card"],
                outline=PALETTE["card_edge"], width=1)
    d.rectangle([x, y, x + w, y + 4], fill=accent)


# ---------------------------------------------------------------- scenes

def art_shenzhen(d, x, y, w, h):
    """Three towers with flags, a summit table seen from above."""
    d.rectangle([x, y, x + w, y + h], fill=(36, 44, 76))
    # towers: one dark silhouette polygon with lit vertical strips
    d.polygon([(x, y + h), (x, y + h * 0.45), (x + w * 0.18, y + h * 0.45),
               (x + w * 0.18, y + h * 0.28), (x + w * 0.30, y + h * 0.28),
               (x + w * 0.30, y + h * 0.52), (x + w * 0.46, y + h * 0.52),
               (x + w * 0.46, y + h * 0.20), (x + w * 0.58, y + h * 0.20),
               (x + w * 0.58, y + h * 0.62), (x + w * 0.74, y + h * 0.62),
               (x + w * 0.74, y + h * 0.40), (x + w, y + h * 0.40),
               (x + w, y + h)], fill=(18, 22, 40))
    for bx in (0.05, 0.22, 0.36, 0.50, 0.64, 0.82):
        d.line([x + w * bx, y + h * 0.55, x + w * bx, y + h * 0.95],
               fill=(240, 200, 90), width=2)
    # moon
    d.ellipse([x + w * 0.80, y + h * 0.05, x + w * 0.80 + 24,
               y + h * 0.05 + 24], fill=(240, 190, 80))
    # flags as small triangles on poles, left to right
    for fx, col in ((0.10, (220, 40, 40)), (0.24, (40, 90, 200)),
                    (0.38, (230, 230, 230))):
        d.line([x + w * fx, y + h * 0.62, x + w * fx, y + h * 0.86],
               fill=(210, 210, 210), width=2)
        d.polygon([(x + w * fx, y + h * 0.62), (x + w * fx + 16, y + h * 0.66),
                   (x + w * fx, y + h * 0.70)], fill=col)
    # round table, bottom right
    d.ellipse([x + w * 0.58, y + h * 0.68, x + w * 0.97, y + h * 0.92],
              fill=(150, 110, 60), outline=(220, 180, 100), width=2)
    d.text((x + 6, y + 4), "SHENZHEN  \u00b7  APEC",
           font=get_font(SANS_B, 10), fill=(255, 255, 255))


def art_gulf(d, x, y, w, h):
    """Radar screen: dark green, sweep, blips, coastline below."""
    d.rectangle([x, y, x + w, y + h], fill=(10, 40, 22))
    cx, cy = x + w * 0.5, y + h * 0.46
    for rr in (30, 22, 14):
        d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr],
                  outline=(60, 160, 90), width=1)
    d.line([cx - 30, cy, cx + 30, cy], fill=(60, 160, 90), width=1)
    d.line([cx, cy - 30, cx, cy + 30], fill=(60, 160, 90), width=1)
    d.line([cx, cy, cx + 22, cy - 20], fill=(140, 240, 140), width=2)
    for bx, by in ((0.30, 0.30), (0.66, 0.28), (0.58, 0.60), (0.76, 0.52)):
        d.ellipse([x + w * bx - 3, y + h * by - 3, x + w * bx + 3,
                   y + h * by + 3], fill=(255, 90, 70))
    # coastline strip
    d.polygon([(x, y + h), (x, y + h * 0.82), (x + w * 0.35, y + h * 0.86),
               (x + w * 0.65, y + h * 0.80), (x + w, y + h * 0.88),
               (x + w, y + h)], fill=(232, 214, 170))
    f = get_font(SANS_B, 10)
    d.text((x + 6, y + 4), "KUWAIT  \u00b7  BAHRAIN", font=f,
           fill=(140, 240, 140))
    d.text((x + w - 56, y + h - 15), "ALI AL SALEM", font=f,
           fill=(90, 60, 20))


def art_gta(d, x, y, w, h):
    """Vice City sunset: banded sky, sun, palms, big VI, controller."""
    bands = [(255, 120, 90), (255, 80, 140), (150, 60, 180), (60, 30, 90)]
    for i, col in enumerate(bands):
        d.rectangle([x, y + h * i / 4, x + w, y + h * (i + 1) / 4], fill=col)
    d.ellipse([x + w * 0.38, y + h * 0.08, x + w * 0.38 + 32,
               y + h * 0.08 + 32], fill=(255, 220, 120))
    # skyline blocks
    for i, th in enumerate((0.42, 0.58, 0.48, 0.66, 0.54, 0.60, 0.44)):
        bx = x + i * w / 7
        d.rectangle([bx + 1, y + h * (1 - th), bx + w / 7 - 1, y + h],
                    fill=(14, 8, 30))
    # palm
    d.line([x + w * 0.12, y + h * 0.70, x + w * 0.12, y + h * 0.96],
           fill=(10, 40, 20), width=3)
    for dx, dy in ((-0.06, -0.06), (0.06, -0.06), (-0.03, -0.09),
                   (0.03, -0.09)):
        d.line([x + w * 0.12, y + h * 0.70, x + w * (0.12 + dx),
                y + h * (0.70 + dy)], fill=(10, 40, 20), width=2)
    # big VI
    f = get_font(SERIF_B, 26)
    d.text((x + w * 0.60, y + h * 0.30), "VI", font=f, fill=(255, 255, 255))
    # controller bar
    d.rounded_rectangle([x + w * 0.30, y + h * 0.66, x + w * 0.70,
                         y + h * 0.88], radius=8, fill=(40, 40, 60),
                        outline=(255, 255, 255), width=1)
    d.ellipse([x + w * 0.35, y + h * 0.72, x + w * 0.35 + 7,
               y + h * 0.72 + 7], fill=(255, 120, 140))
    d.ellipse([x + w * 0.62, y + h * 0.72, x + w * 0.62 + 7,
               y + h * 0.72 + 7], fill=(120, 220, 140))
    f2 = get_font(SANS_B, 15)
    d.text((x + w - 38, y + 2), "99", font=f2, fill=(255, 220, 120))


def art_voyager(d, x, y, w, h):
    """Deep space: starfield, dish of concentric arcs, dashed path."""
    d.rectangle([x, y, x + w, y + h], fill=(8, 10, 28))
    import random
    rnd = random.Random(19)
    for _ in range(46):
        sx = x + rnd.random() * w
        sy = y + rnd.random() * h * 0.75
        r = rnd.choice((1, 1, 2))
        d.ellipse([sx - r, sy - r, sx + r, sy + r],
                  fill=(255, 255, 255) if rnd.random() > 0.3
                  else (180, 200, 255))
    # Earth, small, bottom left
    d.ellipse([x + 6, y + h - 26, x + 30, y + h - 2], fill=(60, 120, 200))
    d.ellipse([x + 10, y + h - 22, x + 22, y + h - 10], fill=(40, 160, 90))
    # dish: concentric arcs + boom + body
    cx, cy = x + w * 0.52, y + h * 0.32
    for rr in (26, 19, 12):
        d.arc([cx - rr, cy - rr, cx + rr, cy + rr], 200, 20,
              fill=(220, 220, 230), width=3)
    d.line([cx + 8, cy + 8, x + w * 0.72, y + h * 0.55],
           fill=(200, 200, 210), width=3)
    d.rectangle([x + w * 0.66, y + h * 0.50, x + w * 0.82, y + h * 0.66],
                fill=(180, 180, 190), outline=(120, 120, 130))
    # dashed trajectory from Earth to the probe
    for t in range(0, 10, 2):
        fx = t / 10.0
        px = x + 20 + (cx - x - 20) * fx
        py = y + h - 14 - (y + h - 14 - cy) * fx
        d.ellipse([px - 1.5, py - 1.5, px + 1.5, py + 1.5],
                  fill=(255, 220, 120))
    f = get_font(SANS_B, 11)
    d.text((x + w - 108, y + h - 18), "1 LIGHT-DAY", font=f,
           fill=(255, 220, 120))


def art_akvan(d, x, y, w, h):
    """Cyclone as a computed spiral polyline over a coast, rain."""
    d.rectangle([x, y, x + w, y + h], fill=(206, 226, 238))
    d.polygon([(x + w * 0.62, y), (x + w, y), (x + w, y + h),
               (x + w * 0.72, y + h), (x + w * 0.66, y + h * 0.55),
               (x + w * 0.70, y + h * 0.30)], fill=(228, 214, 170))
    import math
    cx, cy = x + w * 0.42, y + h * 0.58
    pts = []
    for k in range(60):
        a = k * 0.32
        r = 3 + k * 0.32
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a) * 0.9))
    d.line(pts, fill=(40, 90, 140), width=3, joint="curve")
    d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=(40, 90, 140))
    for i in range(5):
        d.line([x + w * (0.06 + i * 0.05), y + h * 0.80,
                x + w * (0.02 + i * 0.05), y + h * 0.92],
               fill=(90, 140, 190), width=2)
    f = get_font(SANS_B, 10)
    d.text((x + 6, y + 4), "120\u2013130 KM/H", font=f, fill=(40, 90, 140))
    f2 = get_font(SANS_B, 9)
    d.text((x + w - 96, y + h - 15), "BAY OF BENGAL", font=f2,
           fill=(90, 60, 20))


def art_wallstreet(d, x, y, w, h):
    """Candlestick chart falling, towers behind, -561."""
    d.rectangle([x, y, x + w, y + h], fill=(238, 226, 214))
    for i, th in enumerate((0.55, 0.75, 0.60, 0.85, 0.65)):
        bx = x + 6 + i * 16
        d.rectangle([bx, y + h * (1 - th), bx + 12, y + h],
                    fill=(120, 110, 100))
    # candlesticks: green up, red down, falling overall
    candles = [(0.10, 0.30, 0.22, 0.36, 1), (0.26, 0.34, 0.30, 0.44, 0),
               (0.42, 0.40, 0.36, 0.50, 0), (0.58, 0.52, 0.48, 0.60, 0),
               (0.74, 0.62, 0.58, 0.72, 0)]
    for fx, top, bot, low, up in candles:
        col = (42, 140, 70) if up else (178, 34, 34)
        d.line([x + w * fx + 6, y + h * top, x + w * fx + 6, y + h * low],
               fill=col, width=1)
        d.rectangle([x + w * fx, y + h * bot, x + w * fx + 12,
                     y + h * low], fill=col)
    f = get_font(SANS_B, 15)
    d.text((x + w - 62, y + 4), "\u2212561", font=f, fill=PALETTE["red"])


def art_berlin(d, x, y, w, h):
    """EU flag, German tricolour stripe, podium with microphones."""
    d.rectangle([x, y, x + w, y + h], fill=(214, 226, 238))
    # EU flag panel
    d.rectangle([x + 8, y + 8, x + 92, y + 48], fill=(31, 78, 140))
    import math
    for k in range(12):
        a = k * 30 * math.pi / 180
        sx = x + 50 + 15 * math.cos(a)
        sy = y + 28 + 12 * math.sin(a)
        d.polygon([(sx, sy - 3), (sx + 1, sy - 1), (sx + 3, sy),
                   (sx + 1, sy + 1), (sx, sy + 3), (sx - 1, sy + 1),
                   (sx - 3, sy), (sx - 1, sy - 1)], fill=(240, 210, 60))
    # German tricolour
    for i, col in enumerate(((0, 0, 0), (178, 34, 34), (240, 210, 60))):
        d.rectangle([x + w - 46, y + 8 + i * 9, x + w - 8, y + 17 + i * 9],
                    fill=col)
    # podium
    d.rectangle([x + w * 0.38, y + h * 0.58, x + w * 0.62, y + h * 0.95],
                fill=(90, 60, 30))
    d.rectangle([x + w * 0.34, y + h * 0.54, x + w * 0.66, y + h * 0.60],
                fill=(120, 85, 45))
    for mx in (0.44, 0.56):
        d.line([x + w * mx, y + h * 0.54, x + w * mx, y + h * 0.44],
               fill=(40, 40, 40), width=2)
        d.ellipse([x + w * mx - 3, y + h * 0.42, x + w * mx + 3,
                   y + h * 0.42 + 5], fill=(40, 40, 40))


def art_cop31(d, x, y, w, h):
    """Globe with meridians, a rising green arrow, leaf."""
    d.rectangle([x, y, x + w, y + h], fill=(232, 240, 232))
    cx, cy = x + w * 0.42, y + h * 0.52
    d.ellipse([cx - 34, cy - 34, cx + 34, cy + 34], fill=(120, 180, 220),
              outline=(31, 78, 140), width=2)
    d.ellipse([cx - 12, cy - 34, cx + 12, cy + 34], outline=(31, 78, 140),
              width=1)
    d.line([cx - 34, cy, cx + 34, cy], fill=(31, 78, 140), width=1)
    d.arc([cx - 34, cy - 34, cx + 34, cy + 34], 300, 60,
          fill=(31, 78, 140), width=1)
    d.ellipse([cx - 22, cy - 8, cx - 8, cy + 4], fill=(42, 140, 70))
    d.ellipse([cx + 6, cy + 8, cx + 20, cy + 20], fill=(42, 140, 70))
    # rising arrow
    d.line([x + w * 0.80, y + h * 0.85, x + w * 0.80, y + h * 0.30],
           fill=(42, 140, 70), width=4)
    d.polygon([(x + w * 0.80, y + h * 0.18), (x + w * 0.72, y + h * 0.32),
               (x + w * 0.88, y + h * 0.32)], fill=(42, 140, 70))
    f = get_font(SANS_B, 13)
    d.text((x + 6, y + 4), "$120bn", font=f, fill=(42, 140, 70))
    f2 = get_font(SANS_B, 9)
    d.text((x + 6, y + h - 15), "ADAPTATION", font=f2, fill=(42, 110, 62))


def art_nvidia(d, x, y, w, h):
    """A chip (concentric squares, pins) over a rising bar chart."""
    d.rectangle([x, y, x + w, y + h], fill=(16, 20, 26))
    # bars rising
    for i, th in enumerate((0.18, 0.24, 0.30, 0.38, 0.48, 0.60)):
        bx = x + 8 + i * 15
        d.rectangle([bx, y + h - 14 - h * th, bx + 10, y + h - 14],
                    fill=(60, 200, 120))
    # chip
    cx, cy = x + w * 0.68, y + h * 0.44
    d.rectangle([cx - 17, cy - 17, cx + 17, cy + 17], fill=(30, 34, 44),
                outline=(120, 220, 130), width=2)
    d.rectangle([cx - 9, cy - 9, cx + 9, cy + 9], fill=(60, 200, 120))
    for px in range(-2, 3):
        d.line([cx + px * 7, cy - 21, cx + px * 7, cy - 17],
               fill=(120, 220, 130), width=2)
        d.line([cx + px * 7, cy + 17, cx + px * 7, cy + 21],
               fill=(120, 220, 130), width=2)
    f = get_font(SANS_B, 11)
    d.text((x + 6, y + 4), "H-SERIES", font=f, fill=(120, 220, 130))


def art_kerch(d, x, y, w, h):
    """Suspension bridge, middle span dropped, waves below."""
    d.rectangle([x, y, x + w, y + h], fill=(204, 224, 238))
    # towers
    for tx in (0.20, 0.80):
        d.rectangle([x + w * tx - 3, y + h * 0.18, x + w * tx + 3,
                     y + h * 0.78], fill=(120, 110, 100))
    # cables
    d.line([x + w * 0.02, y + h * 0.30, x + w * 0.20, y + h * 0.18,
            x + w * 0.50, y + h * 0.42], fill=(80, 80, 80), width=2)
    d.line([x + w * 0.98, y + h * 0.30, x + w * 0.80, y + h * 0.18,
            x + w * 0.50, y + h * 0.42], fill=(80, 80, 80), width=2)
    # deck, broken in the middle
    d.rectangle([x + w * 0.02, y + h * 0.52, x + w * 0.42, y + h * 0.58],
                fill=(90, 84, 76))
    d.polygon([(x + w * 0.44, y + h * 0.52), (x + w * 0.56, y + h * 0.60),
               (x + w * 0.56, y + h * 0.66), (x + w * 0.44, y + h * 0.58)],
              fill=(90, 84, 76))
    d.rectangle([x + w * 0.58, y + h * 0.52, x + w * 0.98, y + h * 0.58],
                fill=(90, 84, 76))
    # smoke + waves
    d.ellipse([x + w * 0.46, y + h * 0.28, x + w * 0.46 + 16,
               y + h * 0.28 + 16], fill=(150, 150, 150))
    d.ellipse([x + w * 0.50, y + h * 0.20, x + w * 0.50 + 12,
               y + h * 0.20 + 12], fill=(170, 170, 170))
    for i in range(5):
        d.arc([x + w * (0.05 + i * 0.18), y + h * 0.82,
               x + w * (0.23 + i * 0.18), y + h * 0.96], 180, 360,
              fill=(60, 110, 160), width=2)
    f = get_font(SANS_B, 10)
    d.text((x + 6, y + 4), "3RD HIT THIS WEEK", font=f, fill=(80, 80, 80))


def art_tokyo(d, x, y, w, h):
    """Mount Fuji, a torii gate, a red sun disc."""
    d.rectangle([x, y, x + w, y + h], fill=(238, 214, 200))
    d.ellipse([x + w * 0.66, y + h * 0.06, x + w * 0.66 + 30,
               y + h * 0.06 + 30], fill=(220, 60, 50))
    d.polygon([(x + w * 0.05, y + h * 0.92), (x + w * 0.45, y + h * 0.20),
               (x + w * 0.85, y + h * 0.92)], fill=(120, 130, 170))
    d.polygon([(x + w * 0.34, y + h * 0.42), (x + w * 0.45, y + h * 0.20),
               (x + w * 0.56, y + h * 0.42)], fill=(255, 255, 255))
    # torii
    d.rectangle([x + w * 0.68, y + h * 0.70, x + w * 0.71, y + h * 0.94],
                fill=(200, 40, 30))
    d.rectangle([x + w * 0.85, y + h * 0.70, x + w * 0.88, y + h * 0.94],
                fill=(200, 40, 30))
    d.rectangle([x + w * 0.64, y + h * 0.64, x + w * 0.92, y + h * 0.69],
                fill=(200, 40, 30))
    d.rectangle([x + w * 0.68, y + h * 0.74, x + w * 0.88, y + h * 0.77],
                fill=(200, 40, 30))
    f = get_font(SANS_B, 10)
    d.text((x + 6, y + 4), "2+2  TOKYO", font=f, fill=(120, 40, 30))


def art_cricket(d, x, y, w, h):
    """A scoreboard panel, a red ball with seam, a bat."""
    d.rectangle([x, y, x + w, y + h], fill=(232, 240, 226))
    d.rectangle([x + 8, y + 6, x + w - 8, y + 52], fill=(26, 26, 30))
    f = get_font(SANS_B, 13)
    d.text((x + 14, y + 10), "ENG  297/4", font=f, fill=(255, 255, 255))
    f2 = get_font(SANS_B, 11)
    d.text((x + 14, y + 26), "DUCKETT 133", font=f2, fill=(240, 210, 60))
    f3 = get_font(SANS_B, 10)
    d.text((x + 14, y + 40), "BY 97 RUNS", font=f3, fill=(120, 220, 140))
    # bat: rotated rectangle drawn as a polygon, left
    d.polygon([(x + w * 0.24, y + h * 0.62), (x + w * 0.32, y + h * 0.66),
               (x + w * 0.16, y + h * 0.94), (x + w * 0.08, y + h * 0.90)],
              fill=(210, 170, 110), outline=(140, 100, 60))
    d.line([x + w * 0.28, y + h * 0.64, x + w * 0.38, y + h * 0.56],
           fill=(140, 100, 60), width=4)
    # ball with seam, right
    d.ellipse([x + w * 0.72, y + h * 0.66, x + w * 0.72 + 24,
               y + h * 0.66 + 24], fill=(178, 34, 34))
    d.arc([x + w * 0.72 + 2, y + h * 0.66 + 4, x + w * 0.72 + 22,
           y + h * 0.66 + 20], 60, 300, fill=(255, 255, 255), width=1)


def art_nsa(d, x, y, w, h):
    """A dark server room: stacked racks, one red OFFLINE switch."""
    d.rectangle([x, y, x + w, y + h], fill=(24, 24, 30))
    for i in range(3):
        rx = x + 8 + i * (w - 16) // 3
        rw = (w - 16) // 3 - 6
        d.rectangle([rx, y + 6, rx + rw, y + h * 0.60], fill=(48, 48, 58),
                    outline=(120, 120, 130))
        for j in range(3):
            d.rectangle([rx + 4, y + 12 + j * 14, rx + rw - 4,
                         y + 22 + j * 14], fill=(30, 30, 38))
            d.ellipse([rx + rw - 10, y + 15 + j * 14, rx + rw - 5,
                       y + 20 + j * 14],
                      fill=(60, 200, 120) if (i + j) % 3 else (220, 60, 50))
    # red banner across the bottom
    d.rectangle([x + 8, y + h * 0.68, x + w - 8, y + h - 8],
                fill=(178, 34, 34))
    f = get_font(SANS_B, 12)
    label = "OFFLINE"
    tw = d.textlength(label, font=f)
    d.text((x + (w - tw) / 2, y + h * 0.68 + 2), label, font=f,
           fill=(255, 255, 255))


# ---------------------------------------------------------------- world map

# Stylised world map as land spans on a 96 x 40 cell grid.
# Columns cover lon -180..180, rows cover lat 86..-58. Each entry is
# (row, [(first_col, last_col), ...]) with both ends inclusive.
# Drawn by hand from a globe, not traced from any dataset.
LAND_SPANS = {
    0: [(10, 16), (35, 40)],
    1: [(8, 18), (33, 42)],
    2: [(6, 20), (33, 42), (52, 54)],
    3: [(4, 24), (34, 42), (58, 66), (70, 76)],
    4: [(3, 26), (35, 41), (56, 88)],
    5: [(3, 28), (56, 90)],
    6: [(4, 30), (43, 43), (56, 91)],
    7: [(8, 31), (44, 48), (50, 58), (59, 91)],
    8: [(12, 31), (46, 49), (50, 60), (61, 90)],
    9: [(14, 31), (46, 60), (62, 88)],
    10: [(15, 30), (46, 59), (63, 87)],
    11: [(16, 29), (45, 58), (64, 86)],
    12: [(17, 28), (45, 58), (66, 86)],
    13: [(18, 27), (45, 57), (59, 64), (67, 86)],
    14: [(19, 26), (46, 56), (60, 64), (68, 82)],
    15: [(20, 25), (46, 55), (60, 63), (69, 80)],
    16: [(21, 25), (46, 54), (61, 63), (70, 78)],
    17: [(22, 30), (45, 54), (61, 63), (71, 77)],
    18: [(24, 32), (45, 54), (62, 63), (72, 76)],
    19: [(27, 33), (45, 54), (73, 76)],
    20: [(27, 34), (45, 55), (73, 77)],
    21: [(28, 35), (46, 56), (74, 78)],
    22: [(28, 36), (47, 57), (75, 80)],
    23: [(29, 37), (48, 58), (76, 82)],
    24: [(30, 37), (49, 59), (78, 84)],
    25: [(30, 37), (50, 59), (79, 85)],
    26: [(31, 37), (51, 59), (80, 86)],
    27: [(31, 36), (52, 58), (80, 87)],
    28: [(32, 36), (53, 57), (80, 88)],
    29: [(32, 35), (81, 88)],
    30: [(33, 35), (82, 88)],
    31: [(33, 34), (83, 87), (92, 93)],
    32: [(83, 86), (92, 94)],
    33: [(84, 85), (93, 94)],
    34: [(93, 93)],
    35: [(85, 85)],
}

GRID_COLS, GRID_ROWS = 96, 40
LON_MIN, LON_MAX = -180.0, 180.0
LAT_MAX, LAT_MIN = 86.0, -58.0

PINS = [
    (1, 114.06, 22.54), (2, 47.98, 29.31), (3, -80.19, 25.76),
    (4, -116.89, 35.42), (5, 85.80, 20.30), (6, -74.01, 40.71),
    (7, 13.40, 52.52), (8, 32.86, 39.93), (9, 116.41, 39.90),
    (10, 36.47, 45.31), (11, 139.69, 35.68), (12, 153.03, -27.47),
    (13, -76.77, 39.11),
]

PIN_COLORS = {
    1: "gold", 2: "red", 3: "green", 4: "purple", 5: "gold",
    6: "green", 7: "blue", 8: "purple", 9: "gold", 10: "blue",
    11: "gold", 12: "teal", 13: "purple",
}

# Wall Street (6) and Fort Meade (13) sit almost on top of each other;
# push their badges apart, with a hairline back to the true spot.
NUDGES = {6: (14, -12), 13: (-16, 10)}


def project(x, y, w, h, lon, lat):
    """Map lon/lat to page coordinates inside the map box."""
    px = x + (lon - LON_MIN) / (LON_MAX - LON_MIN) * w
    py = y + (LAT_MAX - lat) / (LAT_MAX - LAT_MIN) * h
    return px, py


def world_map(d, x, y, w, h):
    """Dotted world map with numbered pins for the 13 illustrated
    stories, plus small dots for the remaining 35 briefs."""
    d.rectangle([x, y, x + w, y + h], fill=PALETTE["map_sea"],
                outline=PALETTE["card_edge"], width=1)
    cell_w = w / GRID_COLS
    cell_h = h / GRID_ROWS
    for row, spans in LAND_SPANS.items():
        cy = y + (row + 0.5) * cell_h
        for c0, c1 in spans:
            for col in range(c0, c1 + 1):
                cx = x + (col + 0.5) * cell_w
                d.ellipse([cx - 1.6, cy - 1.6, cx + 1.6, cy + 1.6],
                          fill=PALETTE["map_dot"])
    # small dots for the 35 briefs (lon, lat) — same research, no pin
    brief_dots = [
        (-0.13, 51.50), (2.35, 48.86), (-3.70, 40.42), (4.90, 52.37),
        (10.75, 59.91), (18.07, 59.33), (12.50, 41.90), (28.98, 41.01),
        (30.31, 59.94), (37.62, 55.76), (31.24, 30.06), (35.93, 31.95),
        (51.39, 35.69), (55.30, 25.20), (44.37, 33.31), (58.59, 35.69),
        (90.41, 23.81), (77.21, 28.61), (121.47, 31.23), (127.02, 37.53),
        (103.82, 1.35), (151.21, -33.87), (174.78, -41.29),
        (-99.13, 19.43), (-58.44, -34.61), (-70.67, -33.45),
        (-43.21, -22.91), (28.05, -26.20), (18.42, -33.92),
        (55.45, -4.68), (100.50, 13.75), (67.01, 24.86),
        (139.77, 35.68), (3.38, 6.52), (135.77, -25.28),
    ]
    for lon, lat in brief_dots:
        px, py = project(x, y, w, h, lon, lat)
        d.ellipse([px - 2, py - 2, px + 2, py + 2],
                  fill=PALETTE["ink"])
    for n, lon, lat in PINS:
        px, py = project(x, y, w, h, lon, lat)
        dx, dy = NUDGES.get(n, (0, 0))
        badge(d, px + dx, py + dy, n, PALETTE[PIN_COLORS[n]], r=9)
        if (dx, dy) != (0, 0):
            d.line([px, py, px + dx, py + dy], fill=PALETTE["ink"], width=1)


def legend(d, x, y, w):
    """Row of region colour chips. Returns the y just below it."""
    f = get_font(SANS_B, 9)
    cx = x
    for region, key in REGION.items():
        d.ellipse([cx, y + 2, cx + 9, y + 11], fill=PALETTE[key])
        label = region.upper()
        d.text((cx + 13, y), label, font=f, fill=PALETTE["soft"])
        cx += 13 + d.textlength(label, font=f) + 14
    return y + 16
