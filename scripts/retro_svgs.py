"""Generate retro (early-2000s console) animated SVGs for the GitHub profile README.
Text is drawn with a hand-made 5x7 bitmap font so nothing depends on web fonts."""
import random
import sys
from pathlib import Path

OUT = Path(sys.argv[1] if len(sys.argv) > 1 else "assets")
OUT.mkdir(parents=True, exist_ok=True)

# ───────────────────────────── 5x7 bitmap font ─────────────────────────────
E = "....."
F = {
    "A": [".###.", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"],
    "B": ["####.", "#...#", "#...#", "####.", "#...#", "#...#", "####."],
    "C": [".###.", "#...#", "#....", "#....", "#....", "#...#", ".###."],
    "D": ["####.", "#...#", "#...#", "#...#", "#...#", "#...#", "####."],
    "E": ["#####", "#....", "#....", "####.", "#....", "#....", "#####"],
    "F": ["#####", "#....", "#....", "####.", "#....", "#....", "#...."],
    "G": [".###.", "#...#", "#....", "#.###", "#...#", "#...#", ".####"],
    "H": ["#...#", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"],
    "I": [".###.", "..#..", "..#..", "..#..", "..#..", "..#..", ".###."],
    "J": ["..###", "...#.", "...#.", "...#.", "...#.", "#..#.", ".##.."],
    "K": ["#...#", "#..#.", "#.#..", "##...", "#.#..", "#..#.", "#...#"],
    "L": ["#....", "#....", "#....", "#....", "#....", "#....", "#####"],
    "M": ["#...#", "##.##", "#.#.#", "#.#.#", "#...#", "#...#", "#...#"],
    "N": ["#...#", "#...#", "##..#", "#.#.#", "#..##", "#...#", "#...#"],
    "O": [".###.", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."],
    "P": ["####.", "#...#", "#...#", "####.", "#....", "#....", "#...."],
    "Q": [".###.", "#...#", "#...#", "#...#", "#.#.#", "#..#.", ".##.#"],
    "R": ["####.", "#...#", "#...#", "####.", "#.#..", "#..#.", "#...#"],
    "S": [".####", "#....", "#....", ".###.", "....#", "....#", "####."],
    "T": ["#####", "..#..", "..#..", "..#..", "..#..", "..#..", "..#.."],
    "U": ["#...#", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."],
    "V": ["#...#", "#...#", "#...#", "#...#", "#...#", ".#.#.", "..#.."],
    "W": ["#...#", "#...#", "#...#", "#.#.#", "#.#.#", "#.#.#", ".#.#."],
    "X": ["#...#", "#...#", ".#.#.", "..#..", ".#.#.", "#...#", "#...#"],
    "Y": ["#...#", "#...#", ".#.#.", "..#..", "..#..", "..#..", "..#.."],
    "Z": ["#####", "....#", "...#.", "..#..", ".#...", "#....", "#####"],
    "0": [".###.", "#...#", "#..##", "#.#.#", "##..#", "#...#", ".###."],
    "1": ["..#..", ".##..", "..#..", "..#..", "..#..", "..#..", ".###."],
    "2": [".###.", "#...#", "....#", "...#.", "..#..", ".#...", "#####"],
    "3": ["####.", "....#", "....#", ".###.", "....#", "....#", "####."],
    "4": ["...#.", "..##.", ".#.#.", "#..#.", "#####", "...#.", "...#."],
    "5": ["#####", "#....", "####.", "....#", "....#", "#...#", ".###."],
    "6": [".###.", "#....", "#....", "####.", "#...#", "#...#", ".###."],
    "7": ["#####", "....#", "...#.", "..#..", ".#...", ".#...", ".#..."],
    "8": [".###.", "#...#", "#...#", ".###.", "#...#", "#...#", ".###."],
    "9": [".###.", "#...#", "#...#", ".####", "....#", "....#", ".###."],
    " ": [E] * 7,
    ".": [E, E, E, E, E, E, "..#.."],
    ",": [E, E, E, E, E, "..#..", ".#..."],
    ":": [E, "..#..", E, E, E, "..#..", E],
    "-": [E, E, E, ".###.", E, E, E],
    "+": [E, "..#..", "..#..", "#####", "..#..", "..#..", E],
    "/": ["....#", "....#", "...#.", "..#..", ".#...", "#....", "#...."],
    "!": ["..#..", "..#..", "..#..", "..#..", "..#..", E, "..#.."],
    "?": [".###.", "#...#", "....#", "...#.", "..#..", E, "..#.."],
    "'": ["..#..", "..#..", E, E, E, E, E],
    ">": ["#....", ".#...", "..#..", "...#.", "..#..", ".#...", "#...."],
    "<": ["....#", "...#.", "..#..", ".#...", "..#..", "...#.", "....#"],
    "*": [E, E, E, "..#..", E, E, E],  # middle dot
    "(": ["...#.", "..#..", ".#...", ".#...", ".#...", "..#..", "...#."],
    ")": [".#...", "..#..", "...#.", "...#.", "...#.", "..#..", ".#..."],
    "[": [".###.", ".#...", ".#...", ".#...", ".#...", ".#...", ".###."],
    "]": [".###.", "...#.", "...#.", "...#.", "...#.", "...#.", ".###."],
    "&": [".##..", "#..#.", "#.#..", ".#...", "#.#.#", "#..#.", ".##.#"],
    "=": [E, E, "#####", E, "#####", E, E],
    "_": [E, E, E, E, E, E, "#####"],
}


def text_w(s, sc):
    return len(s) * 6 * sc - sc


def text_path(s, x, y, sc):
    """Path data for string s, top-left at (x, y), pixel size sc. Rows are run-merged."""
    d = []
    for i, ch in enumerate(s.upper()):
        g = F.get(ch, F["?"])
        ox = x + i * 6 * sc
        for r, row in enumerate(g):
            c = 0
            while c < 5:
                if row[c] == "#":
                    start = c
                    while c < 5 and row[c] == "#":
                        c += 1
                    n = c - start
                    d.append(f"M{ox + start * sc:g} {y + r * sc:g}h{n * sc:g}v{sc:g}h{-n * sc:g}z")
                else:
                    c += 1
    return "".join(d)


def txt(s, x, y, sc, fill, extra="", anchor="start"):
    if anchor == "middle":
        x = x - text_w(s, sc) / 2
    elif anchor == "end":
        x = x - text_w(s, sc)
    return f'<path d="{text_path(s, x, y, sc)}" fill="{fill}" {extra}/>'


def glow_txt(s, x, y, sc, fill, glow, anchor="start", blur="glow"):
    """Text with a blurred halo underneath."""
    return (txt(s, x, y, sc, glow, f'filter="url(#{blur})" opacity=".9"', anchor)
            + txt(s, x, y, sc, fill, "", anchor))


COMMON_DEFS = """
    <filter id="glow" x="-20%" y="-50%" width="140%" height="200%"><feGaussianBlur stdDeviation="3"/></filter>
    <filter id="glowBig" x="-20%" y="-60%" width="140%" height="220%"><feGaussianBlur stdDeviation="7"/></filter>
    <pattern id="scan" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="1.4" fill="#000" opacity=".28"/></pattern>
    <radialGradient id="vig" cx="50%" cy="50%" r="75%"><stop offset=".6" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".75"/></radialGradient>
"""


def svg(w, h, label, defs, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
            f'role="img" aria-label="{label}">\n  <defs>{COMMON_DEFS}{defs}\n  </defs>\n{body}\n'
            f'  <rect width="{w}" height="{h}" fill="url(#scan)"/>\n'
            f'  <rect width="{w}" height="{h}" fill="url(#vig)"/>\n</svg>\n')


def particles(rng, n, w, h, colors, y_min=0, rise=140):
    out = []
    for _ in range(n):
        x, y = rng.uniform(0, w), rng.uniform(y_min, h)
        s = rng.choice([2, 2, 3, 4])
        dur = rng.uniform(5, 11)
        beg = -rng.uniform(0, dur)
        dx = rng.uniform(-25, 25)
        out.append(
            f'<rect x="{x:.0f}" y="{y:.0f}" width="{s}" height="{s}" fill="{rng.choice(colors)}" opacity="0">'
            f'<animateTransform attributeName="transform" type="translate" from="0 0" to="{dx:.0f} {-rise}" '
            f'dur="{dur:.1f}s" begin="{beg:.1f}s" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values="0;.9;0" dur="{dur:.1f}s" begin="{beg:.1f}s" repeatCount="indefinite"/></rect>')
    return "\n  ".join(out)


# ────────────────────────────── 1. BOOT HEADER ──────────────────────────────
def boot():
    W, H = 900, 340
    rng = random.Random(7)
    vx, vy = 450, 196  # vanishing point
    defs = """
    <radialGradient id="fog" cx="50%" cy="60%" r="55%"><stop offset="0" stop-color="#2a6cff" stop-opacity=".55"/><stop offset=".5" stop-color="#0b2a8a" stop-opacity=".25"/><stop offset="1" stop-color="#000" stop-opacity="0"/></radialGradient>
    <linearGradient id="pil" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#cfe6ff" stop-opacity=".95"/><stop offset=".25" stop-color="#5fa2ff" stop-opacity=".7"/><stop offset="1" stop-color="#0a2a8a" stop-opacity="0"/></linearGradient>
    <linearGradient id="sweep" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#bfe0ff" stop-opacity=".55"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
    <linearGradient id="floor" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2a6cff" stop-opacity=".0"/><stop offset="1" stop-color="#2a6cff" stop-opacity=".35"/></linearGradient>"""
    b = [f'<rect width="{W}" height="{H}" fill="#000"/>']

    # fog that fades in, then breathes forever
    b.append('<g><animate attributeName="opacity" values="1;.65;1" dur="5s" begin="3s" repeatCount="indefinite"/>'
             '<ellipse cx="450" cy="215" rx="560" ry="210" fill="url(#fog)" opacity="0">'
             '<animate attributeName="opacity" from="0" to="1" begin=".2s" dur="2.4s" fill="freeze"/></ellipse></g>')

    # perspective floor grid
    g = ['<g opacity="0" stroke="#3b7bff" stroke-width="1"><animate attributeName="opacity" from="0" to=".55" begin=".6s" dur="2s" fill="freeze"/>']
    g.append(f'<rect x="0" y="{vy}" width="{W}" height="{H - vy}" fill="url(#floor)" stroke="none"/>')
    for i in range(-14, 15):
        g.append(f'<line x1="{vx}" y1="{vy}" x2="{vx + i * 75}" y2="{H}" stroke-opacity=".35"/>')
    yy, step = vy + 4, 4
    while yy < H:
        g.append(f'<line x1="0" y1="{yy:.0f}" x2="{W}" y2="{yy:.0f}" stroke-opacity="{min(.5, .08 + (yy - vy) / 300):.2f}"/>')
        step *= 1.35
        yy += step
    g.append("</g>")
    b.append("".join(g))

    # glowing towers rising out of the floor, back to front
    towers = []
    for i in range(22):
        d = rng.uniform(0.05, 1)
        side = rng.choice([-1, 1])
        spread = rng.uniform(70, 470) * (0.35 + d * 0.9)
        x = vx + side * spread
        base = vy + d * 115
        w = 5 + d * 20
        h = rng.uniform(35, 150) * (0.45 + d * 0.8)
        towers.append((d, x, base, w, h))
    towers.sort()
    for k, (d, x, base, w, h) in enumerate(towers):
        beg = 0.5 + k * 0.09
        op = 0.35 + d * 0.6
        pulse = rng.uniform(3, 6)
        b.append(
            f'<g opacity="{op:.2f}"><animate attributeName="opacity" values="{op:.2f};{op * .55:.2f};{op:.2f}" dur="{pulse:.1f}s" begin="{beg + 1.5:.1f}s" repeatCount="indefinite"/>'
            f'<rect x="{x - w / 2:.1f}" y="{base:.1f}" width="{w:.1f}" height="0" fill="url(#pil)">'
            f'<animate attributeName="height" from="0" to="{h:.1f}" begin="{beg:.2f}s" dur="1.3s" fill="freeze" calcMode="spline" keySplines=".2 .8 .2 1"/>'
            f'<animate attributeName="y" from="{base:.1f}" to="{base - h:.1f}" begin="{beg:.2f}s" dur="1.3s" fill="freeze" calcMode="spline" keySplines=".2 .8 .2 1"/></rect>'
            f'<rect x="{x - w / 2:.1f}" y="{base - h:.1f}" width="{w:.1f}" height="2" fill="#fff" opacity="0">'
            f'<animate attributeName="opacity" from="0" to=".9" begin="{beg + 1.2:.2f}s" dur=".3s" fill="freeze"/></rect></g>')

    b.append(particles(rng, 46, W, H, ["#7fd4ff", "#cfe6ff", "#3b7bff"], y_min=80))

    # light sweep
    b.append('<rect x="-320" y="0" width="260" height="340" fill="url(#sweep)" transform="skewX(-18)" opacity="0">'
             '<animate attributeName="x" from="-320" to="1250" begin="2.7s" dur="1.5s" fill="freeze"/>'
             '<animate attributeName="opacity" values="0;1;1;0" begin="2.7s" dur="1.5s" fill="freeze"/></rect>')

    # flash at the moment the logo lands
    b.append(f'<rect width="{W}" height="{H}" fill="#cfe6ff" opacity="0">'
             '<animate attributeName="opacity" values="0;.35;0" begin="2.9s" dur=".6s" fill="freeze"/></rect>')

    # small top label
    b.append('<g opacity="0"><animate attributeName="opacity" from="0" to=".85" begin="1s" dur="1s" fill="freeze"/>'
             + txt("COAXUS SYSTEMS", 450, 28, 2, "#7fd4ff", anchor="middle") + "</g>")

    # title
    b.append('<g opacity="0"><animate attributeName="opacity" from="0" to="1" begin="2.9s" dur="1.1s" fill="freeze"/>'
             + txt("JULIAN TRUJILLO", 450, 84, 5, "#2a6cff", 'filter="url(#glowBig)"', "middle")
             + glow_txt("JULIAN TRUJILLO", 450, 84, 5, "#eef6ff", "#5fa2ff", "middle")
             + "</g>")
    b.append('<g opacity="0"><animate attributeName="opacity" from="0" to="1" begin="3.6s" dur="1s" fill="freeze"/>'
             + glow_txt("SOFTWARE ENGINEER * SYSTEMS ARCHITECT * BUILDER", 450, 140, 2, "#9fd0ff", "#2a6cff", "middle")
             + "</g>")

    # PRESS START blink
    b.append('<g opacity="0"><animate attributeName="opacity" values="1;0" calcMode="discrete" dur="1.1s" begin="4.6s" repeatCount="indefinite"/>'
             + glow_txt("- PRESS START -", 450, 300, 2, "#ffffff", "#2a6cff", "middle") + "</g>")

    (OUT / "boot.svg").write_text(svg(W, H, "Julian Trujillo - retro console boot screen", defs, "  " + "\n  ".join(b)))


# ────────────────────────── shared: floating crystals ──────────────────────────
def cube(cx, cy, s, rng, op):
    """Isometric translucent cube that bobs and drifts."""
    h = s * 0.58
    top = f"{cx},{cy - s} {cx + s},{cy - s + h} {cx},{cy - s + 2 * h} {cx - s},{cy - s + h}"
    left = f"{cx - s},{cy - s + h} {cx},{cy - s + 2 * h} {cx},{cy + 2 * h} {cx - s},{cy + h}"
    right = f"{cx + s},{cy - s + h} {cx},{cy - s + 2 * h} {cx},{cy + 2 * h} {cx + s},{cy + h}"
    dur = rng.uniform(5, 9)
    dy = rng.uniform(8, 18)
    return (f'<g opacity="{op:.2f}"><animateTransform attributeName="transform" type="translate" '
            f'values="0 0;{rng.uniform(-6, 6):.0f} {-dy:.0f};0 0" dur="{dur:.1f}s" begin="{-rng.uniform(0, dur):.1f}s" repeatCount="indefinite"/>'
            f'<polygon points="{top}" fill="#9fd0ff"/><polygon points="{left}" fill="#2a6cff"/>'
            f'<polygon points="{right}" fill="#1446b8"/>'
            f'<polygon points="{top} " fill="none" stroke="#e6f3ff" stroke-opacity=".6"/></g>')


BG_DEFS = """
    <linearGradient id="bgBlue" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#001a52"/><stop offset=".55" stop-color="#000a2a"/><stop offset="1" stop-color="#00030f"/></linearGradient>
    <linearGradient id="hl" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#5fa2ff" stop-opacity=".75"/><stop offset="1" stop-color="#5fa2ff" stop-opacity="0"/></linearGradient>"""


def cycle_values(positions, hold=0.9):
    """values/keyTimes that hold on each position and glide to the next, looping."""
    n = len(positions)
    vals, kts = [], []
    for i, p in enumerate(positions):
        t0 = i / n
        vals += [p, p]
        kts += [t0, t0 + hold / n]
    vals.append(positions[0])
    kts.append(1)
    return ";".join(map(str, vals)), ";".join(f"{k:.3f}" for k in kts)


def window_onoff(i, n):
    vals = ["1" if j == i else "0" for j in range(n)]
    kts = [f"{j / n:.3f}" for j in range(n)]
    return ";".join(vals), ";".join(kts)


# ─────────────────────────────── 2. SYSTEM MENU ───────────────────────────────
def menu():
    W, H = 900, 380
    rng = random.Random(11)
    T = 14  # seconds for a full cycle
    b = [f'<rect width="{W}" height="{H}" fill="url(#bgBlue)"/>']
    for _ in range(9):
        b.append(cube(rng.uniform(40, 860), rng.uniform(60, 360), rng.uniform(10, 34), rng, rng.uniform(.07, .2)))
    b.append(particles(rng, 28, W, H, ["#7fd4ff", "#cfe6ff"], rise=90))

    # header
    b.append(f'<rect x="0" y="0" width="{W}" height="52" fill="#000" opacity=".35"/>')
    b.append(f'<rect x="0" y="52" width="{W}" height="2" fill="#3b7bff"><animate attributeName="opacity" values="1;.35;1" dur="3s" repeatCount="indefinite"/></rect>')
    b.append(glow_txt("SYSTEM MENU", 32, 18, 3, "#eef6ff", "#2a6cff"))
    b.append(txt("PLAYER 1", 868, 22, 2, "#7fd4ff", anchor="end"))

    items = ["PROFILE", "FOCUS", "LANGUAGES", "STATUS"]
    ys = [100, 160, 220, 280]
    vals, kts = cycle_values([y - 14 for y in ys])
    b.append(f'<rect x="28" y="{ys[0] - 14}" width="270" height="44" fill="url(#hl)">'
             f'<animate attributeName="y" values="{vals}" keyTimes="{kts}" dur="{T}s" repeatCount="indefinite"/>'
             f'<animate attributeName="opacity" values="1;.6;1" dur="1.2s" repeatCount="indefinite"/></rect>')
    vals2, _ = cycle_values([0, 60, 120, 180])
    b.append(f'<g><animateTransform attributeName="transform" type="translate" values="{";".join("0 " + v for v in vals2.split(";"))}" keyTimes="{kts}" dur="{T}s" repeatCount="indefinite"/>'
             f'<g><animateTransform attributeName="transform" type="translate" values="0 0;5 0;0 0" dur=".8s" repeatCount="indefinite"/>'
             + txt(">", 40, ys[0], 3, "#ffffff") + "</g></g>")
    for it, y in zip(items, ys):
        b.append(txt(it, 70, y, 3, "#d6e9ff"))

    # info panel
    px, py, pw, ph = 330, 78, 540, 250
    b.append(f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="6" fill="#000a2a" opacity=".75" stroke="#3b7bff" stroke-width="2"/>')
    b.append(f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="6" fill="none" stroke="#5fa2ff" stroke-width="5" filter="url(#glow)" opacity=".5">'
             '<animate attributeName="opacity" values=".5;.15;.5" dur="2.5s" repeatCount="indefinite"/></rect>')

    def panel(i, content):
        v, k = window_onoff(i, len(items))
        return (f'<g opacity="{"1" if i == 0 else "0"}"><animate attributeName="opacity" values="{v}" keyTimes="{k}" '
                f'calcMode="discrete" dur="{T}s" repeatCount="indefinite"/>{content}</g>')

    lx = px + 28

    def row(label, value, y, vcol="#ffffff"):
        return txt(label, lx, y, 2, "#7fd4ff") + txt(value, lx + 150, y, 2, vcol)

    p0 = (glow_txt("PROFILE", lx, py + 22, 3, "#eef6ff", "#2a6cff")
          + row("NAME", "JULIAN TRUJILLO", py + 80) + row("CLASS", "SOFTWARE ENGINEER", py + 115)
          + row("SUBCLASS", "SYSTEMS ARCHITECT", py + 150) + row("ALIGNMENT", "CLEAN CODE", py + 185)
          + txt("LV 99", px + pw - 28, py + 22, 3, "#ffd166", anchor="end"))
    p1 = glow_txt("FOCUS", lx, py + 22, 3, "#eef6ff", "#2a6cff")
    for j, f in enumerate(["SCALABLE BACKEND SYSTEMS", "CLEAN ARCHITECTURE + DDD", "MODERN FRONTEND UX", "DEVOPS + CLOUD-NATIVE"]):
        p1 += txt(">", lx, py + 80 + j * 35, 2, "#ffd166") + txt(f, lx + 24, py + 80 + j * 35, 2, "#ffffff")

    def bar(y, filled, total=10):
        s = ""
        for c in range(total):
            col = "#5fa2ff" if c < filled else "#0b2a6b"
            s += f'<rect x="{lx + 150 + c * 22}" y="{y}" width="18" height="14" fill="{col}" stroke="#7fd4ff" stroke-opacity=".4"/>'
        return s

    p2 = (glow_txt("LANGUAGES", lx, py + 22, 3, "#eef6ff", "#2a6cff")
          + txt("SPANISH", lx, py + 80, 2, "#7fd4ff") + bar(py + 78, 10) + txt("NATIVE", lx + 380, py + 80, 2, "#ffffff")
          + txt("ENGLISH", lx, py + 125, 2, "#7fd4ff") + bar(py + 123, 7) + txt("B2", lx + 380, py + 125, 2, "#ffffff")
          + txt("PYTHON / JAVA / TS / PHP", lx, py + 180, 2, "#d6e9ff"))
    p3 = (glow_txt("STATUS", lx, py + 22, 3, "#eef6ff", "#2a6cff")
          + f'<rect x="{lx}" y="{py + 78}" width="14" height="14" fill="#39d353"><animate attributeName="opacity" values="1;.2;1" dur="1s" repeatCount="indefinite"/></rect>'
          + txt("ONLINE", lx + 26, py + 80, 2, "#39d353")
          + row("QUEST", "BUILD THINGS THAT LAST", py + 120, "#ffd166")
          + row("WEBSITE", "COAXUS.DEV", py + 155)
          + row("MOTTO", "IT JUST WORKS.", py + 190))
    for i, c in enumerate([p0, p1, p2, p3]):
        b.append(panel(i, c))

    # footer hints
    b.append(f'<rect x="0" y="{H - 34}" width="{W}" height="34" fill="#000" opacity=".4"/>')
    b.append(txt("[A] SELECT    [B] BACK    [START] MENU", 32, H - 22, 2, "#7fd4ff"))
    (OUT / "menu.svg").write_text(svg(W, H, "Retro system menu: profile, focus, languages, status", BG_DEFS, "  " + "\n  ".join(b)))


# ────────────────────────────── 3. MEMORY CARD ──────────────────────────────
ICONS = {  # 8x8 pixel icons, char -> color
    "chart": ["........", "......YY", "......YY", "...CC.YY", "...CC.YY", "BB.CC.YY", "BB.CC.YY", "WWWWWWWW"],
    "cap": ["...WW...", ".WWWWWW.", "WWWWWWWW", ".BWWWWB.", "..BBBBY.", "..BBBBY.", "......Y.", ".....YY."],
    "bolt": ["....YY..", "...YY...", "..YY....", ".YYYYYY.", "....YY..", "...YY...", "..YY....", ".Y......"],
    "doc": [".WWWWW..", ".W...WW.", ".W.CC.W.", ".W....W.", ".W.BBBW.", ".W....W.", ".W.BBBW.", ".WWWWWW."],
}
ICOL = {"Y": "#ffd166", "C": "#7fd4ff", "B": "#5fa2ff", "W": "#eef6ff"}


def icon(name, x, y, s):
    out = []
    for r, row in enumerate(ICONS[name]):
        for c, ch in enumerate(row):
            if ch != ".":
                out.append(f'<rect x="{x + c * s}" y="{y + r * s}" width="{s}" height="{s}" fill="{ICOL[ch]}"/>')
    return "".join(out)


def memcard():
    W, H = 900, 400
    rng = random.Random(23)
    T = 12
    b = [f'<rect width="{W}" height="{H}" fill="url(#bgBlue)"/>']
    for _ in range(6):
        b.append(cube(rng.uniform(40, 860), rng.uniform(80, 380), rng.uniform(10, 26), rng, rng.uniform(.06, .14)))
    b.append(particles(rng, 22, W, H, ["#7fd4ff", "#cfe6ff"], rise=80))

    b.append(f'<rect x="0" y="0" width="{W}" height="52" fill="#000" opacity=".35"/>')
    b.append(f'<rect x="0" y="52" width="{W}" height="2" fill="#3b7bff"/>')
    b.append(glow_txt("MEMORY CARD  SLOT 1", 32, 18, 3, "#eef6ff", "#2a6cff"))
    b.append(txt("4 SAVES * 8 MB", 868, 22, 2, "#7fd4ff", anchor="end"))

    saves = [
        ("chart", "ANALYTICS PLATFORMS", "FINANCE + REAL ESTATE", "12"),
        ("cap", "EDUCATION SYSTEMS", "LMS + SSO + HIGH TRAFFIC", "09"),
        ("bolt", "EVENT-DRIVEN CORE", "BACKENDS + MICROSERVICES", "15"),
        ("doc", "REPORTING ENGINES", "PDF + DATA DASHBOARDS", "07"),
    ]
    pos = [(32, 80), (466, 80), (32, 228), (466, 228)]
    cw, ch = 402, 128
    for (ic, title, sub, blocks), (x, y) in zip(saves, pos):
        b.append(f'<rect x="{x}" y="{y}" width="{cw}" height="{ch}" rx="6" fill="#000a2a" opacity=".7" stroke="#1f4fbf" stroke-width="2"/>')
        b.append(f'<rect x="{x + 16}" y="{y + 20}" width="88" height="88" rx="4" fill="#001a52" stroke="#3b7bff"/>')
        dur = rng.uniform(1.6, 2.4)
        b.append(f'<g><animateTransform attributeName="transform" type="translate" values="0 0;0 -4;0 0" dur="{dur:.1f}s" repeatCount="indefinite"/>'
                 + icon(ic, x + 28, y + 32, 8) + "</g>")
        b.append(txt(title, x + 122, y + 30, 2, "#ffffff"))
        b.append(txt(sub, x + 122, y + 62, 1.5, "#7fd4ff"))
        b.append(txt(f"BLOCKS {blocks}", x + 122, y + 96, 1.5, "#ffd166"))
        b.append(txt("SAVED", x + cw - 16, y + 96, 1.5, "#39d353", anchor="end"))

    # cursor frame cycling through saves
    xs = [p[0] - 6 for p in pos]
    ys = [p[1] - 6 for p in pos]
    vx_, kts = cycle_values(xs)
    vy_, _ = cycle_values(ys)
    b.append(f'<rect x="{xs[0]}" y="{ys[0]}" width="{cw + 12}" height="{ch + 12}" rx="8" fill="none" stroke="#9fd0ff" stroke-width="3">'
             f'<animate attributeName="x" values="{vx_}" keyTimes="{kts}" dur="{T}s" repeatCount="indefinite"/>'
             f'<animate attributeName="y" values="{vy_}" keyTimes="{kts}" dur="{T}s" repeatCount="indefinite"/>'
             '<animate attributeName="stroke-opacity" values="1;.35;1" dur="1s" repeatCount="indefinite"/></rect>')
    b.append(f'<rect x="{xs[0]}" y="{ys[0]}" width="{cw + 12}" height="{ch + 12}" rx="8" fill="none" stroke="#5fa2ff" stroke-width="8" filter="url(#glow)" opacity=".6">'
             f'<animate attributeName="x" values="{vx_}" keyTimes="{kts}" dur="{T}s" repeatCount="indefinite"/>'
             f'<animate attributeName="y" values="{vy_}" keyTimes="{kts}" dur="{T}s" repeatCount="indefinite"/></rect>')

    b.append(f'<rect x="0" y="{H - 30}" width="{W}" height="30" fill="#000" opacity=".4"/>')
    b.append(txt("LOAD GAME?   ALL SAVES ARE PRODUCTION-READY", 32, H - 20, 1.5, "#7fd4ff"))
    (OUT / "memory-card.svg").write_text(svg(W, H, "Memory card with four save files: what I build", BG_DEFS, "  " + "\n  ".join(b)))


# ──────────────────────────────── 4. FOOTER ────────────────────────────────
def footer():
    W, H = 900, 230
    rng = random.Random(5)
    b = [f'<rect width="{W}" height="{H}" fill="#000"/>',
         '<ellipse cx="450" cy="250" rx="520" ry="150" fill="#0b2a8a" opacity=".45"><animate attributeName="opacity" values=".45;.25;.45" dur="4s" repeatCount="indefinite"/></ellipse>']
    b.append(particles(rng, 40, W, H, ["#7fd4ff", "#cfe6ff", "#3b7bff"], rise=110))
    b.append(txt("THANKS FOR PLAYING", 450, 40, 4, "#2a6cff", 'filter="url(#glowBig)"', "middle"))
    b.append(glow_txt("THANKS FOR PLAYING", 450, 40, 4, "#eef6ff", "#5fa2ff", "middle"))
    b.append(txt("CONTINUE?", 450, 104, 3, "#ffd166", anchor="middle"))

    # countdown 9..0
    digits = [str(9 - i) for i in range(10)]
    for i, dgt in enumerate(digits):
        v = ";".join("1" if j == i else "0" for j in range(10))
        k = ";".join(f"{j / 10:.1f}" for j in range(10))
        b.append(f'<g opacity="{"1" if i == 0 else "0"}"><animate attributeName="opacity" values="{v}" keyTimes="{k}" calcMode="discrete" dur="10s" repeatCount="indefinite"/>'
                 + glow_txt(dgt, 450, 132, 4, "#ffffff", "#2a6cff", "middle") + "</g>")

    b.append('<g><animate attributeName="opacity" values="1;0" calcMode="discrete" dur=".8s" repeatCount="indefinite"/>'
             + txt(">", 362, 180, 2, "#ffffff") + "</g>")
    b.append(txt("YES", 384, 180, 2, "#ffffff") + txt("NO", 498, 180, 2, "#5f7aa8"))
    b.append(txt("2026 COAXUS.DEV", 450, 212, 1.5, "#3b7bff", anchor="middle"))
    (OUT / "footer.svg").write_text(svg(W, H, "Thanks for playing - continue?", "", "  " + "\n  ".join(b)))


boot()
menu()
memcard()
footer()
for p in sorted(OUT.glob("*.svg")):
    print(p.name, f"{p.stat().st_size / 1024:.1f} KB")
