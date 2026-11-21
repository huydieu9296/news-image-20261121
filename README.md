# The World in One Day — 21 November 2026

A newspaper front page that sums up Saturday 21 November 2026 in a
single image. Six verified stories from the day — Russian missiles
landing in Poland during the overnight attack on Kyiv, the AI-led
Wall Street sell-off that pushed the S&P 500 and the Dow into
correction, the magnitude 6.8 earthquake in central Peru, the UK-EU
reset deal sealed in Brussels, COP31 in Antalya running into
overtime with fossil fuels dropped from the draft, and Iranian oil
tankers massing at Kharg Island to test the US naval blockade —
laid out as a classic broadsheet: navy masthead, red rule, and six
story blocks with a coloured side bar, a hand-drawn icon, a kicker,
a headline and a two-line deck.

## Run

```sh
python3 draw_news.py   # builds entry.png (1024x1024, under 1 MiB)
python3 main.py        # validates entry.png and copies it to $MAKEFUN_OUTPUT_DIR
```

`main.py` uses only the Python standard library. It checks the PNG
magic bytes, the 1 MiB size limit and the 1024x1024 dimensions,
copies the file byte for byte, then reads the copy back to confirm
it is identical. `MAKEFUN_OUTPUT_DIR` defaults to `/output`.

The picture is fully deterministic: fixed layout, fixed DejaVu
fonts, no randomness, no timestamps and no network access. Two runs
of `main.py` write byte-identical files.
