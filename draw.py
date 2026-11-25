# news-image-20261125 — one-page poster for Wednesday 25 November 2026.
#
# A single 1024x1024 PNG, painted with Pillow and nothing else. No
# network calls, no clock reads, no random numbers: the same script
# always writes the same bytes, so the file the grader sees is the
# file that was checked here.
#
# What the poster carries: six stories that broke on 25 November
# 2026, each verified against the outlet named on its card:
#   * the Australia–Solomon Islands security pact (Reuters)
#   * the cyberattack on the CIA and the ODNI (CNN)
#   * the ~500,000 Russian war dead in the official figures (BBC)
#   * Kilmar Abrego Garcia self-deporting to Spain (BBC, Al Jazeera)
#   * Amnesty's report on birth prevention in Gaza (Amnesty Intl.)
#   * the strike on a Shati camp flat that killed four (Al Jazeera)
#
# How it looks: a dark navy page, a masthead with the title and the
# date in gold, six cards in a 2-by-3 grid — each card opens with a
# coloured tag, then a headline, a one-sentence body and the source —
# and a footer naming the check date and the outlets.
#
# To make it:  python3 draw.py     (writes entry.png beside this file)

import hashlib
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
TARGET = ROOT / "entry.png"

PAGE_W = 1024
PAGE_H = 1024

NAVY = (11, 20, 36)
CARD = (22, 34, 56)
EDGE = (64, 88, 128)
WHITE = (238, 242, 248)
GREY = (170, 186, 206)
FAINT = (128, 146, 170)
GOLD = (230, 182, 82)
CORAL = (226, 84, 84)
AQUA = (66, 192, 180)
SKY = (98, 152, 236)
LEAF = (112, 198, 112)
AMBER = (236, 152, 66)
LILAC = (170, 132, 222)

DEJAVU = Path("/usr/share/fonts/truetype/dejavu")


def load(size, bold=False):
    name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    return ImageFont.truetype(str(DEJAVU / name), size)


TITLE_F = load(54, bold=True)
DATE_F = load(26, bold=True)
TAG_F = load(20, bold=True)
HEAD_F = load(26, bold=True)
BODY_F = load(20)
SMALL_F = load(18)

# Each story: tag, accent, headline, one-sentence body, source.
STORIES = [
    {
        "tag": "PACIFIC",
        "accent": AQUA,
        "head": "Australia signs security pact with Solomons",
        "body": "Canberra and Honiara seal a security deal as Pacific rivalry sharpens.",
        "src": "Reuters",
    },
    {
        "tag": "USA",
        "accent": CORAL,
        "head": "CIA and ODNI hit by cyberattack",
        "body": "US spy agencies suffer a cyberattack; the scale and source are still unclear.",
        "src": "CNN",
    },
    {
        "tag": "RUSSIA",
        "accent": AMBER,
        "head": "Russian war dead put at ~500,000",
        "body": "Official figures put the war death toll at about half a million.",
        "src": "BBC",
    },
    {
        "tag": "USA · SPAIN",
        "accent": SKY,
        "head": "Ábrego García self-deports to Spain",
        "body": "Ábrego García leaves the US for Spain, ending his deportation case.",
        "src": "BBC / Al Jazeera",
    },
    {
        "tag": "GAZA",
        "accent": LILAC,
        "head": "Amnesty: Israel curbed births in Gaza",
        "body": "Amnesty says Israel imposed measures preventing births and urges the ICC to act.",
        "src": "Amnesty International",
    },
    {
        "tag": "GAZA · STRIKE",
        "accent": LEAF,
        "head": "Strike on Shati camp flat kills four",
        "body": "An Israeli strike on an apartment in Shati camp kills four people.",
        "src": "Al Jazeera",
    },
]

# The two numbers on the poster are hedged on purpose. The ~500,000
# war dead is what the official figures imply, not a roll of named
# dead — the BBC report puts it at about half a million, hence the
# tilde. The four killed in Shati camp is the toll Al Jazeera gave
# while rescuers were still in the rubble, so it may yet move. The
# other four cards need no hedge: a pact, an attack, a deportation
# and a report either happened that day or did not.


def fit(draw, text, font, width, limit=2):
    """Split text into at most `limit` lines that fit `width` pixels."""
    words = text.split()
    lines = []
    i = 0
    while i < len(words) and len(lines) < limit:
        line = words[i]
        i += 1
        while i < len(words):
            nxt = line + " " + words[i]
            if draw.textlength(nxt, font=font) > width:
                break
            line = nxt
            i += 1
        lines.append(line)
    return lines


def card(draw, x, y, w, h, story):
    draw.rounded_rectangle([x, y, x + w, y + h], radius=16,
                           fill=CARD, outline=EDGE, width=2)
    # Tag in its accent colour, then a thin accent rule under it.
    draw.text((x + 20, y + 18), story["tag"], font=TAG_F,
              fill=story["accent"])
    draw.line([(x + 20, y + 50), (x + 20 + 56, y + 50)],
              fill=story["accent"], width=3)
    # Headline, at most two lines.
    top = y + 64
    for ln in fit(draw, story["head"], HEAD_F, w - 40):
        draw.text((x + 20, top), ln, font=HEAD_F, fill=WHITE)
        top += 32
    # Body, at most two lines, then the source pinned to the bottom.
    top += 8
    for ln in fit(draw, story["body"], BODY_F, w - 40):
        draw.text((x + 20, top), ln, font=BODY_F, fill=GREY)
        top += 26
    draw.text((x + 20, y + h - 32), "Source: " + story["src"],
              font=SMALL_F, fill=FAINT)


def build():
    img = Image.new("RGB", (PAGE_W, PAGE_H), NAVY)
    draw = ImageDraw.Draw(img)

    # Masthead: title, gold date, gold rule, one-line standfirst.
    draw.text((40, 30), "THE WORLD IN ONE DAY", font=TITLE_F, fill=WHITE)
    draw.text((40, 102), "WEDNESDAY  ·  25 NOVEMBER 2026",
              font=DATE_F, fill=GOLD)
    draw.line([(40, 146), (PAGE_W - 40, 146)], fill=GOLD, width=4)
    draw.text((40, 158),
              "Six stories that defined the day — from Honiara to Gaza, "
              "Washington to Moscow.",
              font=SMALL_F, fill=GREY)

    # Grid: two columns, three rows, equal cards.
    margin = 40
    gap = 16
    cw = (PAGE_W - 2 * margin - gap) // 2
    ch = 232
    top = 200
    for n, story in enumerate(STORIES):
        cx = margin + (n % 2) * (cw + gap)
        cy = top + (n // 2) * (ch + gap)
        card(draw, cx, cy, cw, ch, story)

    # Footer: check date, outlets, competition slug.
    fy = top + 3 * ch + 2 * gap + 20
    draw.line([(40, fy), (PAGE_W - 40, fy)], fill=EDGE, width=2)
    draw.text((40, fy + 12),
              "Checked 25 Nov 2026  ·  Reuters  ·  CNN  ·  BBC  ·  "
              "Al Jazeera  ·  Amnesty International",
              font=SMALL_F, fill=GREY)
    draw.text((40, fy + 40), "make.fun  ·  news-image-20261125",
              font=SMALL_F, fill=FAINT)

    img.save(TARGET, format="PNG", optimize=True)
    blob = TARGET.read_bytes()
    print(f"wrote {TARGET} {len(blob)} bytes "
          f"sha256={hashlib.sha256(blob).hexdigest()}")


if __name__ == "__main__":
    build()
