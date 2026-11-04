# Hipster for Zed

Bold, terminal-style themes for Zed. It started as a port of Hipster Green from iTerm2/Tabby and now has 14 variants.

![all variants](screenshots/preview.png)

## Install

In Zed, open the command palette, run `zed: extensions`, search for **Hipster** and install it. Then pick a variant with `theme selector: toggle`.

## Variants

Click a name to see its full-size screenshot (shown with JetBrains Mono).

Dark:

- **[Hipster Green Dark](screenshots/hipster-green-dark.png)**: the original iTerm2/Tabby scheme, kept exact
- **[Hipster Green Soft](screenshots/hipster-green-soft.png)**: same colors, but the dim purple and blue are brighter so they're easier to read
- **[Hipster Matrix](screenshots/hipster-matrix.png)**: pure black and only greens, like an old CRT
- **[Hipster Moss](screenshots/hipster-moss.png)**: muted earthy greens for long sessions
- **[Hipster Forest](screenshots/hipster-forest.png)**: deep pine background with warm fruit colors
- **[Hipster Midnight](screenshots/hipster-midnight.png)**: blue-black background with neon green text
- **[Hipster Mint](screenshots/hipster-mint.png)**: teal dark with mint text and pink highlights
- **[Hipster Pink](screenshots/hipster-pink.png)**: neon pink, palette from the [hipster-pink](https://github.com/physetersarealwayshigh/hipster-pink-zed-theme) fork
- **[Hipster Purple](screenshots/hipster-purple.png)**: violet night with candy accents
- **[Hipster Blue](screenshots/hipster-blue.png)**: deep navy with electric blue text
- **[Hipster Red](screenshots/hipster-red.png)**: dark red room with warm coral text
- **[Hipster Amber](screenshots/hipster-amber.png)**: orange, like an old amber monitor

Light:

- **[Hipster Sage](screenshots/hipster-sage.png)**: soft sage paper with green ink
- **[Hipster Paper](screenshots/hipster-paper.png)**: warm cream paper, like printed code

Every variant except the original keeps text at 4.5:1 contrast or better, and gives keywords, functions, types, strings and numbers their own colors. The original stays exact to the source scheme, so its purple and blue are a bit dimmer.

## Editing the themes

All variants are generated from `scripts/gen.py`. Change a palette there and run:

```sh
python3 scripts/gen.py          # rewrites themes/hipster.json
python3 scripts/gen.py --check  # contrast report only
python3 scripts/distinct.py     # checks keywords, functions, types etc. look different
python3 scripts/preview.py      # rebuilds screenshots/preview.png
```

Don't edit the JSON by hand, it gets overwritten.

## License

MIT
