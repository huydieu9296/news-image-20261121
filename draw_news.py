#!/usr/bin/env python3
"""Draw a one-page newspaper front page for Saturday 21 November 2026.

Layout: a navy masthead naming the day, a red rule, then six story
cards in a two-by-three grid. Every card has a coloured spine, a
hand-drawn line glyph, a kicker, a headline that shrinks until it fits
two lines, a two-line deck and a one-line key-fact strip, with a
centred footer line underneath.

The six stories are the day's verified headlines, as reported on
21 November 2026: Russian missiles landing in Poland during the
overnight attack on Kyiv; the AI-led Wall Street sell-off that pushed
the S&P 500 and the Dow into correction; the magnitude 6.8 earthquake
in central Peru; the UK-EU reset deal sealed in Brussels; COP31 in
Antalya running into overtime with fossil fuels dropped from the
draft; and Iranian oil tankers massing at Kharg Island to test the
US naval blockade.

Everything is fixed: same fonts, same positions, no randomness, no
clock, no network. Running this file writes entry.png next to itself.
"""

from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

PAGE_W, PAGE_H = 1024, 1024
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
PLAIN = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

PAPER = (246, 241, 227)
CARD = (255, 253, 246)
CARD_EDGE = (220, 213, 194)
NAVY = (22, 35, 63)
NAVY_SUB = (201, 210, 224)
RED = (180, 35, 24)
INK = (28, 28, 26)
DECK = (74, 70, 62)
GREY = (122, 114, 100)
HAIRLINE = (214, 207, 188)
TITLE_FILL = (250, 247, 238)

MASTHEAD = "THE WORLD IN ONE DAY"
DATELINE = "SATURDAY, 21 NOVEMBER 2026"
FOOTER = ("Six stories from a single day  ·  Compiled from verified reports  ·  "
          "21 November 2026")


@dataclass
class Story:
    kicker: str
    headline: str
    deck: str
    fact: str
    accent: tuple
    glyph: str


STORIES = [
    Story(
        "WAR  ·  UKRAINE",
        "Russian missiles crash in Poland in huge Kyiv attack",
        "110 missiles and 400+ drones hit Kyiv, killing at least eight; "
        "two missiles land in Poland as NATO jets scramble.",
        "Tusk calls it a provocation",
        (166, 28, 28),
        "missile",
    ),
    Story(
        "MARKETS  ·  WALL STREET",
        "AI sell-off drags S&P and Dow into correction",
        "Nasdaq falls 5.28% and the S&P 3.7%; Nvidia drops 14% as the "
        "SEC probes its accounting.",
        "Nasdaq's worst week since 2020",
        (27, 125, 61),
        "chart",
    ),
    Story(
        "DISASTER  ·  PERU",
        "Magnitude 6.8 quake shakes Peru",
        "Tremor strikes the Junín region and is felt in Lima, sending "
        "residents into the streets.",
        "No casualties reported",
        (21, 101, 192),
        "quake",
    ),
    Story(
        "DIPLOMACY  ·  EUROPE",
        "UK and EU seal post-Brexit reset deal",
        "Food and farm checks go from March 2028; carbon markets link up "
        "and youth can live and work across borders.",
        "100,000 a year, ages 18–31",
        (14, 124, 123),
        "bridge",
    ),
    Story(
        "CLIMATE  ·  TURKEY",
        "COP31 runs into overtime as fossil fuels vanish",
        "Draft deal drops every mention of fossil fuels and a $120bn "
        "adaptation target; a third draft is due Saturday.",
        "EU warns of a \u2018fossil summit\u2019",
        (106, 63, 181),
        "leaf",
    ),
    Story(
        "ENERGY  ·  GULF",
        "Iran masses tankers to test US blockade",
        "More than 14 tankers gather at Kharg Island; Tehran vows to break "
        "the blockade as Trump waits until the New Year.",
        "No oil shipped since July",
        (178, 106, 0),
        "ship",
    ),
]


def load_font(size, bold=False):
    return ImageFont.truetype(BOLD if bold else PLAIN, size)


def wrap_text(draw, text, fnt, max_width):
    """Greedy word wrap; returns the lines that fit max_width."""
    lines, current = [], ""
    for word in text.split():
        trial = word if not current else current + " " + word
        if draw.textlength(trial, font=fnt) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def fit_lines(draw, text, max_width, max_lines, start, floor, bold):
    """Shrink the font until the text wraps into at most max_lines.

    If it still overflows at the smallest size, clip the last line
    with an ellipsis so nothing ever draws outside its box.
    """
    size = start
    while size > floor:
        fnt = load_font(size, bold=bold)
        if len(wrap_text(draw, text, fnt, max_width)) <= max_lines:
            return wrap_text(draw, text, fnt, max_width), fnt
        size -= 1
    fnt = load_font(floor, bold=bold)
    lines = wrap_text(draw, text, fnt, max_width)
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        tail = lines[-1]
        while tail and draw.textlength(tail + "…", font=fnt) > max_width:
            tail = tail.rsplit(" ", 1)[0] if " " in tail else tail[:-1]
        lines[-1] = tail + "…"
    return lines, fnt


def draw_glyph(draw, kind, x0, y0, size, colour):
    """A small line-drawn glyph inside the square (x0, y0, size)."""
    x1, y1 = x0 + size, y0 + size
    cx, cy = x0 + size // 2, y0 + size // 2
    w = 3
    if kind == "missile":
        # A rocket climbing diagonally, with a flame trail.
        draw.polygon([(x0 + 26, y0 + 4), (x0 + 36, y0 + 14),
                      (x0 + 30, y0 + 24), (x0 + 22, y0 + 14)],
                     outline=colour, width=w)
        draw.line([x0 + 22, y0 + 22, x0 + 12, y0 + 34], fill=colour, width=w)
        draw.line([x0 + 30, y0 + 26, x0 + 20, y0 + 38], fill=colour, width=2)
        draw.line([x0 + 10, y0 + 40, x0 + 18, y0 + 32], fill=colour, width=2)
        draw.ellipse([x0 + 30, y0 + 30, x0 + 40, y0 + 40], fill=colour)
    elif kind == "chart":
        # Falling market line on axes.
        draw.line([x0 + 8, y0 + 6, x0 + 8, y1 - 8], fill=colour, width=w)
        draw.line([x0 + 8, y1 - 8, x1 - 6, y1 - 8], fill=colour, width=w)
        draw.line([x0 + 12, y0 + 12, x0 + 20, y0 + 20, x0 + 28, y0 + 18,
                   x0 + 38, y0 + 32], fill=colour, width=w)
        draw.polygon([(x0 + 38, y0 + 32), (x0 + 30, y0 + 30),
                      (x0 + 38, y0 + 24)], fill=colour)
    elif kind == "quake":
        # Seismograph zig-zag.
        draw.line([x0 + 4, cy, x0 + 12, cy, x0 + 16, cy - 12, x0 + 20, cy + 12,
                   x0 + 24, cy - 8, x0 + 28, cy + 4, x0 + 34, cy - 14,
                   x0 + 38, cy + 10, x0 + 42, cy], fill=colour, width=2)
    elif kind == "bridge":
        # An arched bridge over water.
        draw.arc([x0 + 6, y0 + 10, x1 - 6, y0 + 38], 180, 360,
                 fill=colour, width=w)
        draw.line([x0 + 4, y0 + 30, x1 - 4, y0 + 30], fill=colour, width=w)
        for px in (x0 + 12, cx, x1 - 12):
            draw.line([px, y0 + 18, px, y0 + 30], fill=colour, width=2)
        draw.line([x0 + 8, y0 + 38, x1 - 8, y0 + 38], fill=colour, width=2)
    elif kind == "leaf":
        # A leaf with a centre vein.
        draw.pieslice([x0 + 8, y0 + 6, x1 - 8, y1 - 6], 270, 90,
                      outline=colour, width=w)
        draw.line([x0 + 12, y1 - 10, x1 - 12, y0 + 10], fill=colour, width=2)
        draw.line([cx, cy, cx + 10, cy - 2], fill=colour, width=2)
        draw.line([cx, cy + 6, cx + 10, cy + 4], fill=colour, width=2)
    elif kind == "ship":
        # An oil tanker: hull, deck and funnel.
        draw.polygon([(x0 + 6, y0 + 28), (x1 - 6, y0 + 28),
                      (x1 - 12, y0 + 40), (x0 + 12, y0 + 40)], fill=colour)
        draw.rectangle([x0 + 14, y0 + 16, x0 + 30, y0 + 28], fill=colour)
        draw.line([cx + 2, y0 + 6, cx + 2, y0 + 16], fill=colour, width=w)
        draw.line([x0 + 6, y0 + 42, x1 - 6, y0 + 42], fill=colour, width=2)


def draw_card(draw, story, bx, by, bw, bh):
    """One story card: spine, kicker and glyph, headline, deck, fact."""
    draw.rectangle([bx, by, bx + bw, by + bh], fill=CARD,
                   outline=CARD_EDGE, width=1)
    draw.rectangle([bx + 1, by + 1, bx + 10, by + bh - 1], fill=story.accent)

    tx = bx + 26
    tw = bw - 26 - 20
    draw.text((tx, by + 18), story.kicker, font=load_font(16, bold=True),
              fill=story.accent)
    draw_glyph(draw, story.glyph, bx + bw - 20 - 46, by + 14, 46,
               story.accent)

    lines, fnt = fit_lines(draw, story.headline, tw, 2, 30, 18, bold=True)
    y = by + 64
    for line in lines:
        draw.text((tx, y), line, font=fnt, fill=INK)
        y += fnt.size + 8

    lines, fnt = fit_lines(draw, story.deck, tw, 2, 18, 14, bold=False)
    y = by + 150
    for line in lines:
        draw.text((tx, y), line, font=fnt, fill=DECK)
        y += fnt.size + 8

    draw.line([tx, by + bh - 42, bx + bw - 20, by + bh - 42],
              fill=HAIRLINE, width=1)
    draw.text((tx, by + bh - 32), story.fact, font=load_font(16, bold=True),
              fill=story.accent)


def render():
    page = Image.new("RGB", (PAGE_W, PAGE_H), PAPER)
    draw = ImageDraw.Draw(page)

    # Masthead: title, dateline, red rule.
    draw.rectangle([0, 0, PAGE_W, 140], fill=NAVY)
    title_fnt = load_font(56, bold=True)
    tw = draw.textlength(MASTHEAD, font=title_fnt)
    draw.text(((PAGE_W - tw) / 2, 24), MASTHEAD, font=title_fnt,
              fill=TITLE_FILL)
    date_fnt = load_font(23)
    dw = draw.textlength(DATELINE, font=date_fnt)
    draw.text(((PAGE_W - dw) / 2, 98), DATELINE, font=date_fnt, fill=NAVY_SUB)
    draw.rectangle([0, 140, PAGE_W, 145], fill=RED)

    # Six cards, two columns by three rows.
    margin, gutter = 28, 20
    grid_top, grid_bottom = 162, 962
    card_w = (PAGE_W - 2 * margin - gutter) // 2
    card_h = (grid_bottom - grid_top - 2 * 16) // 3
    for i, story in enumerate(STORIES):
        row, col = divmod(i, 2)
        bx = margin + col * (card_w + gutter)
        by = grid_top + row * (card_h + 16)
        draw_card(draw, story, bx, by, card_w, card_h)

    footer_fnt = load_font(15)
    fw = draw.textlength(FOOTER, font=footer_fnt)
    draw.text(((PAGE_W - fw) / 2, 980), FOOTER, font=footer_fnt, fill=GREY)

    out = Path(__file__).resolve().parent / "entry.png"
    page.save(out, format="PNG")
    print(f"wrote {out} ({out.stat().st_size} bytes)")


if __name__ == "__main__":
    render()
