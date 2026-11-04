#!/usr/bin/env python3
# how distinct are the token colors in each variant? CIEDE2000 between every pair of roles.
import math, sys
sys.path.insert(0, "/home/ayush/projects/hipster-green-zed-theme/scripts")
import importlib, gen
importlib.reload(gen)

ROLES = ["fg", "property", "keyword", "function", "type", "string", "number",
         "operator", "tag", "attribute", "builtin", "escape", "comment"]
# pairs that are allowed to match (same idea in code)
OK = {("fg", "property"), ("tag", "keyword"), ("builtin", "function"), ("attribute", "type"),
      ("escape", "number"), ("operator", "fg"), ("tag", "function"), ("builtin", "type"),
      ("attribute", "function"), ("escape", "type"), ("attribute", "keyword"), ("escape", "keyword"),
      ("builtin", "keyword"), ("tag", "type"), ("escape", "string"), ("builtin", "property"),
      ("tag", "property"), ("attribute", "property"), ("tag", "number"), ("builtin", "number"),
      ("attribute", "number"), ("escape", "function"), ("escape", "property"), ("operator", "property")}
CORE = ["fg", "keyword", "function", "type", "string", "number", "operator", "comment"]


def lab(h):
    c = [x / 255 for x in gen.rgb(h)]
    c = [x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
    X = (0.4124 * c[0] + 0.3576 * c[1] + 0.1805 * c[2]) / 0.95047
    Y = 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]
    Z = (0.0193 * c[0] + 0.1192 * c[1] + 0.9505 * c[2]) / 1.08883
    f = lambda t: t ** (1 / 3) if t > 0.008856 else 7.787 * t + 16 / 116
    return 116 * f(Y) - 16, 500 * (f(X) - f(Y)), 200 * (f(Y) - f(Z))


def de2000(a, b):
    L1, a1, b1 = lab(a); L2, a2, b2 = lab(b)
    C1, C2 = math.hypot(a1, b1), math.hypot(a2, b2)
    Cb = (C1 + C2) / 2
    G = 0.5 * (1 - math.sqrt(Cb ** 7 / (Cb ** 7 + 25 ** 7)))
    a1p, a2p = (1 + G) * a1, (1 + G) * a2
    C1p, C2p = math.hypot(a1p, b1), math.hypot(a2p, b2)
    h1p = math.degrees(math.atan2(b1, a1p)) % 360
    h2p = math.degrees(math.atan2(b2, a2p)) % 360
    dLp, dCp = L2 - L1, C2p - C1p
    dh = h2p - h1p
    if C1p * C2p == 0: dh = 0
    elif dh > 180: dh -= 360
    elif dh < -180: dh += 360
    dHp = 2 * math.sqrt(C1p * C2p) * math.sin(math.radians(dh / 2))
    Lbp, Cbp = (L1 + L2) / 2, (C1p + C2p) / 2
    hs = h1p + h2p
    if C1p * C2p == 0: hbp = hs
    elif abs(h1p - h2p) <= 180: hbp = hs / 2
    else: hbp = (hs + 360) / 2 if hs < 360 else (hs - 360) / 2
    T = 1 - 0.17 * math.cos(math.radians(hbp - 30)) + 0.24 * math.cos(math.radians(2 * hbp)) \
        + 0.32 * math.cos(math.radians(3 * hbp + 6)) - 0.20 * math.cos(math.radians(4 * hbp - 63))
    dth = 30 * math.exp(-(((hbp - 275) / 25) ** 2))
    Rc = 2 * math.sqrt(Cbp ** 7 / (Cbp ** 7 + 25 ** 7))
    Sl = 1 + 0.015 * (Lbp - 50) ** 2 / math.sqrt(20 + (Lbp - 50) ** 2)
    Sc, Sh = 1 + 0.045 * Cbp, 1 + 0.015 * Cbp * T
    Rt = -math.sin(math.radians(2 * dth)) * Rc
    return math.sqrt((dLp / Sl) ** 2 + (dCp / Sc) ** 2 + (dHp / Sh) ** 2 + Rt * (dCp / Sc) * (dHp / Sh))


def report(MIN):
    bad_total = 0
    for v in gen.VARIANTS:
        close = []
        for i, a in enumerate(CORE):
            for b in CORE[i + 1:]:
                if (a, b) in OK or (b, a) in OK:
                    continue
                d = de2000(v[a], v[b])
                if d < MIN:
                    close.append(f"{a}/{b} {d:.0f}")
        worst = min(de2000(v[a], v[b]) for i, a in enumerate(CORE) for b in CORE[i + 1:]
                    if (a, b) not in OK and (b, a) not in OK)
        print(f"{v['name']:20} min {worst:5.1f}  {', '.join(close) if close else 'ok'}")
        if close and v["name"] != "Hipster Green Dark":
            bad_total += 1
    return bad_total


if __name__ == "__main__":
    sys.exit(1 if report(float(sys.argv[1]) if len(sys.argv) > 1 else 20) else 0)
