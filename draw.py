# news-image-20261125 — poster for Wednesday 25 November 2026.
# Draws one 1024x1024 PNG with PIL only: no network, no clock, no
# randomness, so two runs write byte-identical files. Six stories that
# were first reported in the 25 November 2026 news cycle, each checked
# against its source on 25 Nov 2026 (Reuters, CNN, BBC, Al Jazeera,
# Amnesty International).
#
# The six stories, and where each was verified on 25 Nov 2026:
#   1. PACIFIC — Australia and Solomon Islands signed a security
#      pact (Reuters, first published 25 Nov 00:01:57Z).
#   2. USA — the CIA and the Office of the Director of National
#      Intelligence were hit by a cyberattack (CNN, 25 Nov).
#   3. RUSSIA — official figures put Russian war deaths at about
#      500,000 (BBC, 25 Nov 00:56).
#   4. USA · SPAIN — Kilmar Ábrego García self-deported to Spain
#      (BBC / Al Jazeera, 25 Nov).
#   5. GAZA — Amnesty International reported on 25 Nov that Israel
#      imposed measures preventing births in Gaza and urged the ICC
#      to act (Amnesty International).
#   6. GAZA — an Israeli strike on an apartment in Shati camp killed
#      four people (Al Jazeera, 25 Nov ~02:00 UTC).
#
# Layout: a navy masthead (title, gold date rule, one-line standfirst),
# then six cards in two columns and three rows, then a footer line with
# the sources and the competition slug. The palette is one deep navy
# background, a lighter card navy, near-white headlines, grey-blue body
# text, and one accent colour per story tag so a reader can scan the
# six cards at a glance.
#
# Determinism: no network, no clock, no randomness, no environment
# input. The only inputs are the DejaVu fonts in /usr/share/fonts and
# the constants below, so every run writes the same bytes.
#
# Run:  python3 draw.py        (writes entry.png next to this file)

import hashlib
import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
OUT = HERE / "entry.png"

W, H = 1024, 1024
BG = (13, 22, 38)          # deep navy
PANEL = (24, 36, 58)       # card navy
PANEL_EDGE = (58, 82, 122)
INK = (240, 244, 250)      # near-white text
MUTED = (168, 184, 205)    # grey-blue secondary text
GOLD = (232, 184, 84)      # masthead rule + date
RED = (224, 82, 82)
TEAL = (64, 190, 178)
BLUE = (96, 150, 235)
GREEN = (110, 196, 110)
ORANGE = (235, 150, 64)
VIOLET = (168, 130, 220)

FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")


# DejaVu is the system font set on the build machine; sizes are fixed
# so text metrics — and therefore the PNG bytes — never move.
def font(name, size):
    return ImageFont.truetype(str(FONT_DIR / name), size)


F_TITLE = font("DejaVuSans-Bold.ttf", 58)
F_DATE = font("DejaVuSans-Bold.ttf", 27)
F_TAG = font("DejaVuSans-Bold.ttf", 21)
F_HEAD = font("DejaVuSans-Bold.ttf", 27)
F_BODY = font("DejaVuSans.ttf", 21)
F_FOOT = font("DejaVuSans.ttf", 19)

# (tag, tag colour, headline, body, source line)
# Headlines stay short enough to fit two lines at 27 pt in a 444 px
# card; bodies are one or two lines at 21 pt. Every source line names
# the outlet the story was checked against, not a search result.
STORIES = [
    # Honiara: the pact Canberra and Honiara signed the same day.
    (
        "PACIFIC",
        TEAL,
        "Australia signs security pact with Solomons",
        "Canberra and Honiara seal a security deal as Pacific "
        "rivalry sharpens.",
        "Reuters",
    ),
    # Washington: the attack on the two US intelligence agencies.
    (
        "USA",
        RED,
        "CIA and ODNI hit by cyberattack",
        "US spy agencies suffer a cyberattack; the scale and "
        "source are still unclear.",
        "CNN",
    ),
    # Moscow: the official toll the figures now imply.
    (
        "RUSSIA",
        ORANGE,
        "Russian war dead put at ~500,000",
        "Official figures put the war death toll at about half "
        "a million.",
        "BBC",
    ),
    # Washington to Madrid: the self-deportation that ended the case.
    (
        "USA · SPAIN",
        BLUE,
        "Ábrego García self-deports to Spain",
        "Ábrego García leaves the US for Spain, ending "
        "his deportation case.",
        "BBC / Al Jazeera",
    ),
    # Gaza: Amnesty's report and its call to the ICC.
    (
        "GAZA",
        VIOLET,
        "Amnesty: Israel curbed births in Gaza",
        "Amnesty says Israel imposed measures preventing births "
        "and urges the ICC to act.",
        "Amnesty International",
    ),
    # Gaza City: the strike on the Shati camp apartment.
    (
        "GAZA · STRIKE",
        GREEN,
        "Strike on Shati camp flat kills four",
        "An Israeli strike on an apartment in Shati camp kills "
        "four people.",
        "Al Jazeera",
    ),
]

# Notes on the numbers: two figures on the poster are approximate by
# nature, and the poster says so. The "~500,000" Russian war dead is
# the toll the official figures imply, not a count of named dead:
# the BBC's report words it as about half a million, and the poster
# keeps the tilde for that reason. The "four" killed in Shati camp
# is the toll Al Jazeera reported on the day — rescuers were still
# working through the rubble when the story was checked, so the toll
# could still move. The other four stories carry no number that could
# go stale the same way: a pact, an attack, a deportation and a report
# either happened on the day or they did not.


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap measured in pixels; returns list of lines."""
    # Greedy, not optimal: words are added while they fit, so a long
    # word alone on a line is kept rather than split. Callers cap the
    # result to two lines, so a story that runs long is trimmed, never
    # allowed to spill over its card.
    lines = []
    for para in text.split("\n"):
        words = para.split()
        cur = ""
        for word in words:
            trial = f"{cur} {word}".strip()
            if draw.textlength(trial, font=fnt) <= max_w or not cur:
                cur = trial
            else:
                lines.append(cur)
                cur = word
        if cur:
            lines.append(cur)
    return lines


def draw_card(draw, x, y, w, h, story):
    tag, colour, head, body, src = story
    draw.rounded_rectangle([x, y, x + w, y + h], radius=18,
                           fill=PANEL, outline=PANEL_EDGE, width=2)
    # coloured tag chip
    # The chip is the story's accent colour with dark text, so the tag
    # reads as a label even at a glance; its width follows the text.
    chip = tag
    cw = draw.textlength(chip, font=F_TAG) + 24
    draw.rounded_rectangle([x + 22, y + 20, x + 22 + cw, y + 52],
                           radius=9, fill=colour)
    draw.text((x + 34, y + 26), chip, font=F_TAG, fill=(12, 18, 30))
    # headline, up to two lines
    # Headlines are capped at two lines: a third line would collide
    # with the body below it.
    head_lines = wrap(draw, head, F_HEAD, w - 44)[:2]
    hy = y + 68
    for line in head_lines:
        draw.text((x + 22, hy), line, font=F_HEAD, fill=INK)
        hy += 33
    # body, up to two lines
    # The body is the one-sentence version of the story; the source
    # line is pinned to the card bottom so all six cards line up.
    body_lines = wrap(draw, body, F_BODY, w - 44)[:2]
    by = hy + 8
    for line in body_lines:
        draw.text((x + 22, by), line, font=F_BODY, fill=MUTED)
        by += 27
    # source, pinned to the card bottom
    draw.text((x + 22, y + h - 34), "Source: " + src,
              font=F_FOOT, fill=(130, 148, 172))


def main():
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    # --- masthead ---
    # Title, gold date line, gold rule, then the standfirst that tells
    # a reader the poster's span in one sentence.
    draw.text((48, 34), "THE WORLD IN ONE DAY", font=F_TITLE, fill=INK)
    draw.text((48, 108), "WEDNESDAY  \u00b7  25 NOVEMBER 2026",
              font=F_DATE, fill=GOLD)
    draw.line([(48, 152), (W - 48, 152)], fill=GOLD, width=4)
    draw.text((48, 164),
              "Six stories that defined the day \u2014 from Honiara to Gaza, "
              "Washington to Moscow.",
              font=F_FOOT, fill=MUTED)

    # --- six cards: two columns, three rows ---
    # Card width is the leftover after two margins and one gap, split
    # in two; height is fixed so the three rows end at the same line.
    margin = 48
    gap = 20
    cw = (W - 2 * margin - gap) // 2
    ch = 236
    top = 208
    for i, story in enumerate(STORIES):
        col = i % 2
        row = i // 2
        x = margin + col * (cw + gap)
        y = top + row * (ch + gap)
        draw_card(draw, x, y, cw, ch, story)

    # --- footer ---
    # The footer repeats the check date and the outlets, then the
    # competition slug, so the poster stands alone as a record.
    fy = top + 3 * ch + 2 * gap + 22
    draw.line([(48, fy), (W - 48, fy)], fill=PANEL_EDGE, width=2)
    draw.text((48, fy + 14),
              "Checked 25 Nov 2026  \u00b7  Reuters \u00b7 CNN \u00b7 BBC \u00b7 "
              "Al Jazeera \u00b7 Amnesty International",
              font=F_FOOT, fill=MUTED)
    draw.text((48, fy + 42), "make.fun  \u00b7  news-image-20261125",
              font=F_FOOT, fill=(130, 148, 172))

    img.save(OUT, format="PNG", optimize=True)
    data = OUT.read_bytes()
    print(f"wrote {OUT} {len(data)} bytes "
          f"sha256={hashlib.sha256(data).hexdigest()}")


if __name__ == "__main__":
    main()
