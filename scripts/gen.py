#!/usr/bin/env python3
"""Builds themes/hipster.json from the palettes below.

Run: python3 scripts/gen.py          (writes the theme)
     python3 scripts/gen.py --check  (contrast report only)
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "themes", "hipster.json")


def rgb(h):
    h = h.lstrip("#")[:6]
    return [int(h[i:i + 2], 16) for i in (0, 2, 4)]


def hexs(c):
    return "#" + "".join(f"{max(0, min(255, round(x))):02x}" for x in c)


def mix(a, b, t):
    """t=0 gives a, t=1 gives b."""
    a, b = rgb(a), rgb(b)
    return hexs([a[i] + (b[i] - a[i]) * t for i in range(3)])


def alpha(c, a):
    return c[:7] + f"{round(a * 255):02x}"


def lum(h):
    c = [x / 255 for x in rgb(h)]
    c = [x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


def contrast(a, b):
    la, lb = sorted([lum(a), lum(b)], reverse=True)
    return (la + 0.05) / (lb + 0.05)


# One dict per variant. ansi is 8 normal + 8 bright.
VARIANTS = [
    dict(
        name="Hipster Green Dark", appearance="dark",
        blurb="the original iTerm2/Tabby scheme, kept exact",
        bg="#100b05", panel="#0d0905", raised="#1a1510", line="#18120a",
        border="#083905", fg="#84c138", bright="#23ff18", muted="#6f8463",
        gutter="#5f7055", comment="#6f8463", cursor="#23ff18", selection="#083905",
        keyword="#b200b2", function="#00a6b2", type="#e5e500", string="#00a600",
        number="#b200b2", constant="#b200b2", operator="#86a93e", punct="#86a93e",
        property="#84c138", variable="#84c138", tag="#246eb2", attribute="#00a6b2",
        builtin="#246eb2", escape="#e5e500", doc="#00a600", special="#00e5e5",
        error="#e50000", warning="#e5e500", info="#00a6b2", success="#00a600",
        ansi=["#000000", "#b6214a", "#00a600", "#bfbf00", "#246eb2", "#b200b2", "#00a6b2", "#bfbfbf",
              "#666666", "#e50000", "#86a93e", "#e5e500", "#0000ff", "#e500e5", "#00e5e5", "#e5e5e5"],
    ),
    dict(
        name="Hipster Green Soft", appearance="dark",
        blurb="same hues, with the dim purple and blue lifted so everything reads",
        bg="#100b05", panel="#0c0804", raised="#1b160f", line="#19130b",
        border="#123d0c", fg="#95c95a", bright="#5cf04f", muted="#7a8c6b",
        gutter="#66785a", comment="#76896a", cursor="#3dff2e", selection="#1a4a12",
        keyword="#e07ee0", function="#4fd0dc", type="#ece05a", string="#4fe0a8",
        number="#ffa060", constant="#ffa060", operator="#b4c49a", punct="#9aab82",
        property="#a9d47a", variable="#95c95a", tag="#7fb0f0", attribute="#3cc4cf",
        builtin="#7fb0f0", escape="#ffa060", doc="#5aa85a", special="#5fe8e8",
        error="#f05a5a", warning="#e3df5a", info="#3cc4cf", success="#4cc24c",
        ansi=["#1b160f", "#e0566b", "#4cc24c", "#d6d046", "#6fa4e0", "#d77bd7", "#3cc4cf", "#c8c8c0",
              "#6c6c64", "#f05a5a", "#a3d86a", "#eee86a", "#8db8f0", "#eb9aeb", "#6ee8e8", "#ecece4"],
    ),
    dict(
        name="Hipster Matrix", appearance="dark",
        blurb="pure black, green only, like a phosphor CRT",
        bg="#000000", panel="#000000", raised="#071407", line="#041004",
        border="#0d2d0d", fg="#33e05a", bright="#7dff9a", muted="#3f8f50",
        gutter="#2f7a3f", comment="#3f8f50", cursor="#7dff9a", selection="#0f3d18",
        keyword="#c8ff3c", function="#4ae8ff", type="#eaffea", string="#9effe0",
        number="#ffe14a", constant="#ffe14a", operator="#88b090", punct="#4fa860",
        property="#33e05a", variable="#33e05a", tag="#c8ff3c", attribute="#4ae8ff",
        builtin="#4ae8ff", escape="#ffe14a", doc="#4fa860", special="#4ae8ff",
        error="#ff5c5c", warning="#d8ff8c", info="#5cf2c0", success="#33e05a",
        ansi=["#000000", "#d94a4a", "#1fb84a", "#a6f04a", "#2fa88a", "#5cc46e", "#5cf2c0", "#9fd9a8",
              "#2f5a36", "#ff5c5c", "#33e05a", "#d8ff8c", "#5cd6b0", "#8cffa6", "#9effe0", "#d9ffe0"],
    ),
    dict(
        name="Hipster Moss", appearance="dark",
        blurb="muted earthy greens, easy on the eyes for long sessions",
        bg="#11160e", panel="#0d110a", raised="#1f261b", line="#181f14",
        border="#2a3324", fg="#a8c870", bright="#d6e8a8", muted="#7f8f6e",
        gutter="#6a7a5c", comment="#7a8a69", cursor="#c8ff4a", selection="#2c4a14",
        keyword="#e89a5a", function="#6fd0b8", type="#f0dc7a", string="#8fc9e8",
        number="#f08aa0", constant="#f08aa0", operator="#c4c8b0", punct="#9aa488",
        property="#c2d4a2", variable="#a8c870", tag="#6fd0b8", attribute="#e89a5a",
        builtin="#8fc9e8", escape="#f0dc7a", doc="#8ea876", special="#8fc9e8",
        error="#e07a6a", warning="#e3cc7a", info="#86c7ad", success="#a3c46a",
        ansi=["#1f261b", "#d0705e", "#a3c46a", "#d9b85b", "#7fa6bf", "#c08aa8", "#86c7ad", "#c9cfb8",
              "#4f5a45", "#e0837a", "#bcd98a", "#e8d38a", "#9bbfd4", "#d4a0bf", "#a3dcc6", "#e8ecdc"],
    ),
    dict(
        name="Hipster Forest", appearance="dark",
        blurb="deep pine night with warm fruit accents",
        bg="#0f1813", panel="#0b130f", raised="#17241c", line="#142019",
        border="#1f3328", fg="#9ad978", bright="#b8f28a", muted="#7c9686",
        gutter="#628070", comment="#6f8c7c", cursor="#a6ff5c", selection="#1a4a22",
        keyword="#ffa25a", function="#5cd8c0", type="#f5d76e", string="#9cc8ff",
        number="#ff7a9a", constant="#ff7a9a", operator="#b8c8bc", punct="#94a89c",
        property="#a8e0c8", variable="#9ad978", tag="#5cd8c0", attribute="#f5d76e",
        builtin="#c4a8f5", escape="#ffa25a", doc="#86b08e", special="#c4a8f5",
        error="#f27a7a", warning="#f2d27a", info="#7ed6bc", success="#a8d97a",
        ansi=["#17241c", "#e6737a", "#a8d97a", "#f2d27a", "#7fb2d9", "#c79ae6", "#7ed6bc", "#c3d6b8",
              "#46604f", "#f28c8c", "#bfeb8f", "#f7df99", "#9fcbe0", "#d6b3f0", "#9ee8d2", "#e8f2e2"],
    ),
    dict(
        name="Hipster Midnight", appearance="dark",
        blurb="blue-black night sky with neon green text",
        bg="#0b0f17", panel="#080b12", raised="#141a26", line="#111622",
        border="#1c2433", fg="#a6d97a", bright="#3dff6a", muted="#7381a0",
        gutter="#5a6680", comment="#7a8296", cursor="#3dff6a", selection="#0f4022",
        keyword="#c792ea", function="#82aaff", type="#ffcb6b", string="#7fe0c8",
        number="#f78c6c", constant="#f78c6c", operator="#c0c8dc", punct="#8a96b4",
        property="#bfe0a0", variable="#a6d97a", tag="#ff7a93", attribute="#ffcb6b",
        builtin="#82aaff", escape="#89ddff", doc="#7fa880", special="#89ddff",
        error="#ff6b7a", warning="#ffcb6b", info="#82aaff", success="#3dff6a",
        ansi=["#141a26", "#ff6b7a", "#3dd96a", "#ffcb6b", "#82aaff", "#c792ea", "#89ddff", "#c0c8d8",
              "#4a5570", "#ff8a96", "#3dff6a", "#ffdb8f", "#a0bfff", "#dbb0f5", "#a6e8ff", "#eef2fa"],
    ),
    dict(
        name="Hipster Mint", appearance="dark",
        blurb="cool teal dark with mint text and pink pops",
        bg="#0d1716", panel="#0a1211", raised="#152321", line="#121e1d",
        border="#1d302e", fg="#6eeab8", bright="#6dffc4", muted="#76968c",
        gutter="#5e807a", comment="#6a8c84", cursor="#3dffc0", selection="#0c4a3a",
        keyword="#ff8fb1", function="#82b4ff", type="#ffd479", string="#c8f08c",
        number="#f5a97f", constant="#f5a97f", operator="#a8c8c0", punct="#88aaa2",
        property="#a0e8d0", variable="#6eeab8", tag="#ff8fb1", attribute="#ffd479",
        builtin="#82b4ff", escape="#f5a97f", doc="#7fb59a", special="#c4a7f5",
        error="#ff7a8a", warning="#ffd479", info="#5ce1c6", success="#a6e3a1",
        ansi=["#152321", "#ff7a8a", "#a6e3a1", "#ffd479", "#7ab8f0", "#ff8fb1", "#5ce1c6", "#b8e6d0",
              "#3f5c57", "#ff99a6", "#c0f0bb", "#ffe099", "#9ad8f0", "#ffadc8", "#8ff0dc", "#e6faf2"],
    ),
    dict(
        name="Hipster Pink", appearance="dark",
        blurb="neon pink, palette from the hipster-pink fork",
        bg="#0b070a", panel="#080507", raised="#1a0e16", line="#150b12",
        border="#2a1620", fg="#ff4fa8", bright="#ff8ad4", muted="#a3748c",
        gutter="#8a5470", comment="#9c6c85", cursor="#fe019a", selection="#330a22",
        keyword="#c77dff", function="#ffd166", type="#6ec1ff", string="#5de0e6",
        number="#ff9e5e", constant="#ff9e5e", operator="#e8a8cc", punct="#c08aa8",
        property="#ffb3de", variable="#ff8cc6", tag="#c77dff", attribute="#ffd166",
        builtin="#6ec1ff", escape="#ff9e5e", doc="#50c878", special="#8fe88a",
        error="#ff3b6b", warning="#ffd166", info="#6ec1ff", success="#50c878",
        ansi=["#1a0e16", "#ff3b6b", "#50c878", "#ffd166", "#6ec1ff", "#fe019a", "#5de0e6", "#bfbfbf",
              "#666666", "#ff6a8f", "#7ee0a0", "#ffe199", "#9bd4ff", "#ff4db8", "#8eecf0", "#e5e5e5"],
    ),
    dict(
        name="Hipster Purple", appearance="dark",
        blurb="violet night with candy accents",
        bg="#0d0914", panel="#0a0710", raised="#1a1426", line="#151021",
        border="#2a2040", fg="#b58cff", bright="#d4b8ff", muted="#8a7aa8",
        gutter="#6a5c88", comment="#8a8ab0", cursor="#c77dff", selection="#2e1460",
        keyword="#ff79c6", function="#8be9fd", type="#f1fa8c", string="#50fa7b",
        number="#ffb86c", constant="#ffb86c", operator="#d0c4ec", punct="#a898c8",
        property="#d4b8ff", variable="#c9b0ff", tag="#ff79c6", attribute="#f1fa8c",
        builtin="#8be9fd", escape="#ffb86c", doc="#9ab890", special="#8be9fd",
        error="#ff5c7a", warning="#f1fa8c", info="#8be9fd", success="#a6e3a1",
        ansi=["#1a1426", "#ff5c7a", "#a6e3a1", "#f1fa8c", "#8b9cff", "#c77dff", "#8be9fd", "#cfc6e6",
              "#4a4066", "#ff7a93", "#c0f0bb", "#f6fcaa", "#a8b6ff", "#dba8ff", "#a8f0ff", "#f2eefc"],
    ),
    dict(
        name="Hipster Blue", appearance="dark",
        blurb="deep navy with electric blue text",
        bg="#070b14", panel="#050810", raised="#111a2a", line="#0d1522",
        border="#1a2840", fg="#5cb8ff", bright="#9ed6ff", muted="#6f8aac",
        gutter="#4f6a8c", comment="#7a8aa0", cursor="#3da8ff", selection="#0f3360",
        keyword="#c792ea", function="#5ce1e6", type="#ffd479", string="#7ee0a0",
        number="#ff9e7a", constant="#ff9e7a", operator="#b0c8e0", punct="#88a0bc",
        property="#9ed6ff", variable="#5cb8ff", tag="#ff8fb1", attribute="#ffd479",
        builtin="#5ce1e6", escape="#ff9e7a", doc="#6fa890", special="#5ce1e6",
        error="#ff6b7a", warning="#ffd479", info="#5ce1e6", success="#7ee0a0",
        ansi=["#111a2a", "#ff6b7a", "#7ee0a0", "#ffd479", "#3da8ff", "#c792ea", "#5ce1e6", "#c0cfe0",
              "#3f5270", "#ff8a96", "#a0f0bb", "#ffe099", "#7cc4ff", "#dbb0f5", "#9ef0f2", "#eef4fc"],
    ),
    dict(
        name="Hipster Red", appearance="dark",
        blurb="dark red room, warm coral text",
        bg="#120707", panel="#0e0505", raised="#221010", line="#1c0c0c",
        border="#3a1616", fg="#ff6b61", bright="#ff9a8a", muted="#a87470",
        gutter="#8a5652", comment="#a46f6a", cursor="#ff3b30", selection="#4a0c0c",
        keyword="#ffd479", function="#7fd6ff", type="#c8a0ff", string="#b8e07a",
        number="#5ce1c6", constant="#5ce1c6", operator="#f0c0bc", punct="#c09894",
        property="#ffb8ae", variable="#ff8a80", tag="#ffd479", attribute="#c8a0ff",
        builtin="#7fd6ff", escape="#5ce1c6", doc="#b88a7a", special="#7fd6ff",
        error="#ff4060", warning="#ffd479", info="#ff9a8a", success="#c8d070",
        ansi=["#221010", "#ff3b30", "#c8d070", "#ffd479", "#d88a80", "#ff8cc0", "#ffb0a6", "#e8cfcc",
              "#5c3330", "#ff6a60", "#dce088", "#ffe099", "#f0a8a0", "#ff9cc8", "#ffd0c8", "#fff0ee"],
    ),
    dict(
        name="Hipster Amber", appearance="dark",
        blurb="the amber monitor sibling, warm orange phosphor",
        bg="#120c05", panel="#0e0904", raised="#1f160a", line="#1a1208",
        border="#3a2608", fg="#f2b04a", bright="#ffd27a", muted="#a07a45",
        gutter="#8a6a3e", comment="#9c7845", cursor="#ffc040", selection="#4a3008",
        keyword="#ff5f3a", function="#ffe066", type="#fff0c8", string="#b8d46a",
        number="#d6a0ff", constant="#d6a0ff", operator="#b8a08a", punct="#b89a70",
        property="#f8c878", variable="#f2b04a", tag="#ff5f3a", attribute="#ffe066",
        builtin="#fff0c8", escape="#d6a0ff", doc="#b88f55", special="#ffe066",
        error="#ff6a4a", warning="#ffd27a", info="#ffe0a8", success="#d9c050",
        ansi=["#1f160a", "#e8603c", "#d9c050", "#f2b04a", "#c89060", "#d98a5a", "#e0b880", "#e8d4b0",
              "#5c4528", "#ff7a52", "#ecd870", "#ffd27a", "#e0b07a", "#f0a878", "#ffe0a8", "#fff3dc"],
    ),
    dict(
        name="Hipster Sage", appearance="light",
        blurb="soft sage paper, green ink",
        bg="#eef2e6", panel="#e4eadb", raised="#dfe6d3", line="#e5ebdb",
        border="#cdd6bf", fg="#1f5a14", bright="#2a8a12", muted="#5f6e52",
        gutter="#7a876c", comment="#5c6950", cursor="#1a920c", selection="#c4e8a8",
        keyword="#8a3a9e", function="#0b6f78", type="#7d5f00", string="#a8501a",
        number="#c0306a", constant="#c0306a", operator="#3d4636", punct="#4a5440",
        property="#3d5c1c", variable="#1f5a14", tag="#0b6f78", attribute="#7d5f00",
        builtin="#2f5aa0", escape="#c0306a", doc="#46703a", special="#2f5aa0",
        error="#c0302a", warning="#9a6a00", info="#0b6f78", success="#2f7a1a",
        ansi=["#2f4022", "#c0302a", "#2f7a1a", "#9a6a00", "#2f5aa0", "#8a3a9e", "#0b6f78", "#cdd6bf",
              "#5f6e52", "#d9483a", "#3d9a24", "#b07e10", "#4070c0", "#a050b8", "#1a8a94", "#e4eadb"],
    ),
    dict(
        name="Hipster Paper", appearance="light",
        blurb="warm cream paper, like printed code",
        bg="#f8f4e8", panel="#efe9d9", raised="#ebe4d2", line="#f0ebdc",
        border="#ddd4bd", fg="#1e4f0c", bright="#3b8a12", muted="#6e6855",
        gutter="#8f8872", comment="#6e6852", cursor="#2a8a0e", selection="#d6ebb8",
        keyword="#8a3aa8", function="#0a6a87", type="#8a5a00", string="#2e58a8",
        number="#c0302a", constant="#c0302a", operator="#3c3a2c", punct="#4e4c3c",
        property="#4a6a1f", variable="#1e4f0c", tag="#8a3aa8", attribute="#8a5a00",
        builtin="#0a6a87", escape="#c0302a", doc="#4e6e36", special="#7a3f9a",
        error="#c0301e", warning="#9a6400", info="#0a6a87", success="#3a7a18",
        ansi=["#2b2a1f", "#c0301e", "#3a7a18", "#9a6400", "#2e58a8", "#a12c7b", "#0a6a87", "#ddd4bd",
              "#6e6855", "#d9452e", "#4a9a22", "#b07a10", "#4672c4", "#bc4a96", "#1a86a6", "#efe9d9"],
    ),
]


def build(v):
    dark = v["appearance"] == "dark"
    bg, fg = v["bg"], v["fg"]
    hover = mix(v["raised"], fg, 0.06)
    a = v["ansi"]
    dim = [mix(c, bg, 0.35) for c in a[:8]]
    names = ["black", "red", "green", "yellow", "blue", "magenta", "cyan", "white"]

    colors = {
        "border": v["border"],
        "border.variant": mix(v["border"], bg, 0.5),
        "border.focused": v["cursor"],
        "border.selected": v["cursor"],
        "border.transparent": "#00000000",
        "border.disabled": mix(v["border"], bg, 0.5),
        "elevated_surface.background": v["raised"] if dark else v["panel"],
        "surface.background": v["panel"],
        "background": v["panel"],
        "element.background": v["raised"],
        "element.hover": hover,
        "element.active": alpha(v["cursor"], 0.25),
        "element.selected": v["selection"],
        "element.selection_background": alpha(v["selection"], 0.8),
        "element.disabled": v["raised"],
        "drop_target.background": alpha(v["selection"], 0.6),
        "ghost_element.background": "#00000000",
        "ghost_element.hover": hover,
        "ghost_element.active": alpha(v["cursor"], 0.2),
        "ghost_element.selected": v["selection"],
        "ghost_element.disabled": "#00000000",
        "text": fg,
        "text.muted": v["muted"],
        "text.placeholder": v["gutter"],
        "text.disabled": v["gutter"],
        "text.accent": v["bright"],
        "icon": fg,
        "icon.muted": v["muted"],
        "icon.disabled": v["gutter"],
        "icon.placeholder": v["gutter"],
        "icon.accent": v["bright"],
        "debugger.accent": v["error"],
        "status_bar.background": v["panel"],
        "title_bar.background": v["panel"],
        "title_bar.inactive_background": v["panel"],
        "toolbar.background": bg,
        "tab_bar.background": v["panel"],
        "tab.inactive_background": v["panel"],
        "tab.active_background": bg,
        "search.match_background": alpha(v["warning"], 0.25),
        "search.active_match_background": alpha(v["warning"], 0.45),
        "panel.background": v["panel"],
        "panel.focused_border": v["cursor"],
        "panel.indent_guide": mix(v["border"], bg, 0.3),
        "panel.indent_guide_active": v["gutter"],
        "panel.indent_guide_hover": v["muted"],
        "panel.overlay_background": v["raised"],
        "panel.overlay_hover": hover,
        "pane.focused_border": alpha(v["cursor"], 0.6),
        "pane_group.border": v["border"],
        "scrollbar.thumb.background": alpha(fg, 0.15),
        "scrollbar.thumb.hover_background": alpha(fg, 0.28),
        "scrollbar.thumb.active_background": alpha(v["cursor"], 0.4),
        "scrollbar.thumb.border": "#00000000",
        "scrollbar.track.background": "#00000000",
        "scrollbar.track.border": "#00000000",
        "minimap.thumb.background": alpha(fg, 0.12),
        "minimap.thumb.hover_background": alpha(fg, 0.2),
        "minimap.thumb.active_background": alpha(fg, 0.3),
        "minimap.thumb.border": "#00000000",
        "editor.foreground": fg,
        "editor.background": bg,
        "editor.gutter.background": bg,
        "editor.subheader.background": v["raised"],
        "editor.active_line.background": v["line"],
        "editor.highlighted_line.background": v["line"],
        "editor.debugger_active_line.background": alpha(v["warning"], 0.15),
        "editor.line_number": v["gutter"],
        "editor.active_line_number": v["bright"] if dark else fg,
        "editor.hover_line_number": fg,
        "editor.invisible": mix(v["gutter"], bg, 0.4),
        "editor.wrap_guide": alpha(v["border"], 0.6),
        "editor.active_wrap_guide": v["border"],
        "editor.indent_guide": mix(v["border"], bg, 0.3),
        "editor.indent_guide_active": v["gutter"],
        "editor.document_highlight.read_background": alpha(v["selection"], 0.45),
        "editor.document_highlight.write_background": alpha(v["selection"], 0.7),
        "editor.document_highlight.bracket_background": alpha(v["cursor"], 0.18),
        "terminal.background": bg,
        "terminal.foreground": fg,
        "terminal.bright_foreground": v["bright"],
        "terminal.dim_foreground": v["muted"],
        "terminal.ansi.background": bg,
        "link_text.hover": v["function"],
        "version_control.added": v["success"],
        "version_control.modified": v["warning"],
        "version_control.deleted": v["error"],
        "version_control.renamed": v["info"],
        "version_control.conflict": v["error"],
        "version_control.ignored": v["gutter"],
        "vim.normal.background": v["cursor"],
        "vim.insert.background": v["function"],
        "vim.visual.background": v["keyword"],
        "vim.replace.background": v["error"],
    }
    for i, n in enumerate(names):
        colors[f"terminal.ansi.{n}"] = a[i]
        colors[f"terminal.ansi.bright_{n}"] = a[i + 8]
        colors[f"terminal.ansi.dim_{n}"] = dim[i]

    status = {}
    for key, c in [("conflict", v["error"]), ("created", v["success"]), ("deleted", v["error"]),
                   ("error", v["error"]), ("hint", v["muted"]), ("info", v["info"]),
                   ("modified", v["warning"]), ("renamed", v["info"]), ("success", v["success"]),
                   ("warning", v["warning"])]:
        status[key] = c
        status[key + ".background"] = alpha(c, 0.12)
        status[key + ".border"] = alpha(c, 0.5)
    for key in ("hidden", "ignored", "unreachable", "predictive"):
        status[key] = v["gutter"] if key != "predictive" else v["muted"]
        status[key + ".background"] = v["raised"]
        status[key + ".border"] = v["border"]

    cursors = [v["cursor"], v["function"], v["keyword"], v["type"], v["number"], v["property"],
               v["string"], v["special"]]
    players = [{"cursor": c, "background": c, "selection": alpha(c, 0.22)} for c in cursors]
    players[0]["selection"] = v["selection"]

    def s(c, **kw):
        d = {"color": c}
        d.update(kw)
        return d

    bold = {"font_weight": 700}
    ital = {"font_style": "italic"}
    syntax = {
        "attribute": s(v["attribute"]),
        "boolean": s(v["constant"]),
        "comment": s(v["comment"], **ital),
        "comment.doc": s(v["doc"], **ital),
        "constant": s(v["constant"]),
        "constructor": s(v["type"], **bold),
        "embedded": s(v["special"]),
        "emphasis": s(fg, **ital),
        "emphasis.strong": s(v["bright"], **bold),
        "enum": s(v["type"]),
        "function": s(v["function"], **bold),
        "function.builtin": s(v["builtin"]),
        "function.method": s(v["function"], **bold),
        "hint": s(v["muted"], **ital),
        "keyword": s(v["keyword"], **bold),
        "label": s(v["attribute"]),
        "link_text": s(v["function"]),
        "link_uri": s(v["builtin"]),
        "namespace": s(v["type"]),
        "number": s(v["number"]),
        "operator": s(v["operator"]),
        "predictive": s(v["muted"], **ital),
        "preproc": s(v["keyword"]),
        "primary": s(fg),
        "property": s(v["property"]),
        "punctuation": s(v["punct"]),
        "punctuation.bracket": s(v["punct"]),
        "punctuation.delimiter": s(v["punct"]),
        "punctuation.list_marker": s(v["bright"]),
        "punctuation.special": s(v["keyword"]),
        "string": s(v["string"]),
        "string.escape": s(v["escape"]),
        "string.regex": s(v["escape"]),
        "string.special": s(v["special"]),
        "string.special.symbol": s(v["constant"]),
        "tag": s(v["tag"]),
        "tag.doctype": s(v["keyword"]),
        "text.literal": s(v["string"]),
        "title": s(v["bright"], **bold),
        "type": s(v["type"], **bold),
        "type.builtin": s(v["type"], **ital),
        "variable": s(v["variable"]),
        "variable.special": s(v["keyword"], **ital),
        "variant": s(v["constant"]),
        "property.json_key": s(v["function"]),
        "markup.heading": s(v["bright"], **bold),
        "markup.list.marker": s(v["bright"]),
        "markup.link": s(v["function"]),
        "markup.raw": s(v["special"]),
        "markup.quote": s(v["comment"], **ital),
        "markup.bold": s(v["bright"], **bold),
        "markup.italic": s(fg, **ital),
    }

    accents = [v["cursor"], v["function"], v["type"], v["keyword"], v["number"], v["property"]]
    style = dict(colors)
    style.update(status)
    style["players"] = players
    style["syntax"] = syntax
    return {"name": v["name"], "appearance": v["appearance"], "accents": accents, "style": style}


CHECKED = ["fg", "keyword", "function", "type", "string", "number", "operator", "punct",
           "property", "tag", "builtin", "escape", "doc", "special", "comment", "gutter", "muted"]


def check():
    bad = 0
    for v in VARIANTS:
        lows = []
        for k in CHECKED:
            need = 3.0 if k == "gutter" else 4.5
            r = contrast(v[k], v["bg"])
            if r < need:
                lows.append(f"{k} {v[k]} {r:.2f}")
        sel = contrast(v["fg"], v["selection"])
        if sel < 4.5:
            lows.append(f"fg on selection {sel:.2f}")
        # classic is an exact port, so its low spots are expected
        tag = "  (exact port, not enforced)" if v["name"] == "Hipster Green Dark" else ""
        print(f"{v['name']:24} {'ok' if not lows else ', '.join(lows)}{tag}")
        if lows and not tag:
            bad += 1
    return bad


if __name__ == "__main__":
    bad = check()
    if "--check" in sys.argv:
        sys.exit(1 if bad else 0)
    family = {
        "$schema": "https://zed.dev/schema/themes/v0.2.0.json",
        "name": "Hipster",
        "author": "Ayush Bhat <tfeayush@gmail.com>",
        "themes": [build(v) for v in VARIANTS],
    }
    with open(OUT, "w") as f:
        json.dump(family, f, indent=2)
        f.write("\n")
    print(f"wrote {len(VARIANTS)} themes to {OUT}")
