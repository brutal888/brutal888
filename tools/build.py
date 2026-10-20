"""Generates the animated SVGs for the GitHub profile README, in dark and light themes.

Run:  python tools/build.py
Edit the CONTENT section below, then re-run and commit assets/.
GitHub shows SVGs as images: CSS animations work, scripts and web fonts do not,
so everything uses system fonts and pure CSS keyframes.
"""
from pathlib import Path
from html import escape

OUT = Path(__file__).resolve().parent.parent / "assets"
OUT.mkdir(exist_ok=True)

SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, 'Cascadia Code', Menlo, Consolas, 'Liberation Mono', monospace"

THEMES = {
    "dark": dict(bg="#0b0d12", panel="#11141b", panel2="#161a23", line="#232836", text="#eceef3", muted="#8b93a7",
                 faint="#4b5263", cpu="#8c9dff", mem="#52e3b1", disk="#ffb95e", net="#e18cff", ok="#3ddc97",
                 red="#ff6b70", glow=".55"),
    "light": dict(bg="#ffffff", panel="#f7f8fa", panel2="#f0f2f5", line="#e2e5eb", text="#14161c", muted="#5b6475",
                  faint="#a3aab8", cpu="#4a5ee0", mem="#0d9c6b", disk="#cf8317", net="#a243cd", ok="#10a870",
                  red="#e0464c", glow=".35"),
}

# ============================ CONTENT ============================
NAME = "Gagandeep Khokhar"
HANDLE = "brutal888"
PHRASES = [
    "builds LLM systems end to end",
    "ships full-stack apps to production",
    "self-hosts everything, on purpose",
    "reverse-engineers USB hardware",
]
FETCH = [
    ("role", "AI / LLM dev · full-stack"),
    ("work", "Sr. IT Exec @ Desire Energy"),
    ("base", "Jaipur, IN · remote-ready"),
    ("infra", "Proxmox · Ollama · nginx"),
    ("editor", "Claude Code + CLAUDE.md"),
    ("status", "open to AI / LLM roles"),
]

PROJECTS = [
    dict(key="studio33s", title="Studio 33s", tag="LIVE · studio33s.com", accent="mem", anim="orbit",
         lines=["Live studio site with its own headless CMS:",
                "Fastify API, SQLite, admin SPA, 360° tours."],
         chips=["Fastify 5", "SQLite", "React 18", "GSAP"]),
    dict(key="vps-monitor", title="VPS Monitor", tag="PRIVATE · self-hosted", accent="cpu", anim="spark",
         lines=["Real-time server dashboard, zero npm deps.",
                "Live processes, alerts, security, logs."],
         chips=["Node.js", "SSE", "node:sqlite", "SVG charts"]),
    dict(key="lex-eq", title="Lex EQ", tag="ANDROID · reverse-engineered", accent="disk", anim="eq",
         lines=["Decoded a USB-C DAC's HID protocol and",
                "replaced its vendor app with a Kotlin one."],
         chips=["Kotlin", "USB Host API", "HID", "Actions"]),
    dict(key="llm", title="Self-hosted LLMs", tag="INFRA · in production", accent="net", anim="tokens",
         lines=["Open-source models on Proxmox via Ollama,",
                "chosen on quality, latency and memory."],
         chips=["Ollama", "Proxmox VE", "Linux", "nginx"]),
    dict(key="agency-3d", title="Agency 3D", tag="FULL-STACK · Next.js 16", accent="cpu", anim="cube",
         lines=["Next.js platform with admin and a 3D front:",
                "Prisma on Turso, NextAuth, React Three Fiber."],
         chips=["Next.js 16", "Prisma", "R3F", "Tailwind 4"]),
    dict(key="bots", title="Bot Suite", tag="AUTOMATION · Python", accent="mem", anim="chat",
         lines=["Discord & Telegram bots: slash commands,",
                "music streaming, alerts, game-stats polling."],
         chips=["Python", "discord.py", "Telegram", "Docker"]),
]

STACK = [
    ("AI & LLM", "net", ["Ollama", "Claude Code", "Agentic workflows", "Tool use", "Prompt iteration"]),
    ("Frontend", "cpu", ["React 19", "Next.js 16", "TypeScript", "Tailwind 4", "Three.js / R3F", "GSAP", "Framer Motion"]),
    ("Backend", "mem", ["Node.js", "Fastify 5", "Python", "Prisma", "SQLite / libSQL", "NextAuth", "REST APIs"]),
    ("Infra", "disk", ["Linux (RHEL · Ubuntu)", "Proxmox VE", "AWS EC2 · S3", "Docker", "nginx", "PM2", "GitHub Actions"]),
    ("Also", "faint", ["Kotlin / Android", "Bash", "Windows Server · AD", "RHCSA"]),
]
# ================================================================


def svg(w, h, body, css, title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{escape(title)}">'
            f'<title>{escape(title)}</title><style>{css}'
            '@media (prefers-reduced-motion: reduce){*{animation:none!important}}</style>'
            f'{body}</svg>')


def mono_w(text, size):  # monospace advance ≈ 0.6em
    return len(text) * size * 0.6


def sparkline(w, h, seed, n=40):
    """A deterministic, organic-looking line that tiles seamlessly (first == last point)."""
    import math
    pts = []
    for i in range(n + 1):
        x = i * w / n
        t = i / n * 2 * math.pi
        y = 0.5 + 0.22 * math.sin(t * 2 + seed) + 0.12 * math.sin(t * 5 + seed * 2) + 0.07 * math.sin(t * 11 + seed * 3)
        pts.append((x, h * (1 - y)))
    d = f"M{pts[0][0]:.1f},{pts[0][1]:.1f}"
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        cx = (x0 + x1) / 2
        d += f" C{cx:.1f},{y0:.1f} {cx:.1f},{y1:.1f} {x1:.1f},{y1:.1f}"
    return d


# ----------------------------- header -----------------------------
def header(t):
    W, H = 1200, 400
    c = t
    css = f"""
    .sans{{font-family:{SANS}}} .mono{{font-family:{MONO}}}
    .mark rect{{animation:breathe 3.6s cubic-bezier(.2,.8,.2,1) infinite;transform-box:fill-box;transform-origin:center}}
    .mark rect:nth-child(2){{animation-delay:.45s}} .mark rect:nth-child(3){{animation-delay:1.35s}} .mark rect:nth-child(4){{animation-delay:.9s}}
    @keyframes breathe{{0%,100%{{transform:scale(1);opacity:1}}50%{{transform:scale(.7);opacity:.5}}}}
    .blob{{animation:drift 18s ease-in-out infinite alternate}} .blob2{{animation-delay:-9s}}
    @keyframes drift{{to{{transform:translate(60px,30px) scale(1.12)}}}}
    .rise{{animation:rise 1s cubic-bezier(.2,.8,.2,1) both}} .d1{{animation-delay:.15s}} .d2{{animation-delay:.3s}} .d3{{animation-delay:.45s}}
    @keyframes rise{{from{{opacity:0;transform:translateY(14px)}}}}
    .ping{{animation:ping 2s cubic-bezier(.2,.8,.2,1) infinite;transform-box:fill-box;transform-origin:center}}
    @keyframes ping{{from{{transform:scale(.6);opacity:.9}}to{{transform:scale(2.6);opacity:0}}}}
    .scroll{{animation:scroll 14s linear infinite}} @keyframes scroll{{to{{transform:translateX(-{W}px)}}}}
    .caret{{animation:blink 1s steps(1) infinite}} @keyframes blink{{50%{{opacity:0}}}}
    .fetch g{{animation:rise .8s cubic-bezier(.2,.8,.2,1) both}}
    """
    # rotating typed phrases: each gets a 3.5 s slot in a cycle
    n, slot = len(PHRASES), 3.5
    cyc = n * slot
    size, x0, y0 = 25, 66, 270
    phrases = ""
    for i, p in enumerate(PHRASES):
        pw = mono_w(p, size)
        a, b = i * slot / cyc * 100, (i + 1) * slot / cyc * 100
        typed, hold, erase = a + 1.1 / cyc * 100, a + 2.9 / cyc * 100, b - 0.05
        css += (f"@keyframes w{i}{{0%,{a:.2f}%{{width:0}}{typed:.2f}%,{hold:.2f}%{{width:{pw:.0f}px}}{erase:.2f}%,100%{{width:0}}}}"
                f"@keyframes c{i}{{0%,{a:.2f}%{{transform:translateX(0);opacity:0}}{a+.01:.2f}%{{opacity:1}}"
                f"{typed:.2f}%,{hold:.2f}%{{transform:translateX({pw:.0f}px);opacity:1}}{erase:.2f}%{{transform:translateX(0);opacity:1}}{erase+.01:.2f}%,100%{{opacity:0}}}}"
                f".pw{i}{{animation:w{i} {cyc}s steps({len(p)},end) infinite}} .pc{i}{{animation:c{i} {cyc}s steps({len(p)},end) infinite}}")
        phrases += (f'<clipPath id="cp{i}"><rect class="pw{i}" x="{x0 + 26}" y="{y0 - 24}" height="34" width="0"/></clipPath>'
                    f'<text x="{x0 + 26}" y="{y0}" class="mono" font-size="{size}" fill="{c["text"]}" clip-path="url(#cp{i})">{escape(p)}</text>'
                    f'<rect class="pc{i}" x="{x0 + 28}" y="{y0 - 19}" width="11" height="24" rx="2" fill="{c["mem"]}" opacity="0"/>')

    # neofetch-style panel
    px, py, pw_, ph = 700, 46, 440, 312
    keys = ["cpu", "mem", "disk", "net", "cpu", "mem"]
    fetch = ""
    for i, (k, v) in enumerate(FETCH):
        fetch += (f'<g style="animation-delay:{.5 + i * .09:.2f}s"><text x="{px + 28}" y="{py + 100 + i * 31}" class="mono" font-size="16">'
                  f'<tspan fill="{c[keys[i]]}" font-weight="600">{escape(k)}</tspan>'
                  f'<tspan x="{px + 116}" fill="{c["text"]}">{escape(v)}</tspan></text></g>')
    swatches = "".join(f'<rect x="{px + 28 + i * 32}" y="{py + ph - 34}" width="24" height="13" rx="3" fill="{c[k]}"/>'
                       for i, k in enumerate(["cpu", "mem", "disk", "net", "ok", "red", "muted", "faint"]))

    spark = sparkline(W, 60, 1.3)
    spark2 = sparkline(W, 60, 4.1)
    body = f"""
    <defs>
      <filter id="blur" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="60"/></filter>
      <pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse"><path d="M32 0H0V32" fill="none" stroke="{c['line']}" stroke-width="1" opacity=".55"/></pattern>
      <linearGradient id="fade" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{c['bg']}" stop-opacity="0"/><stop offset="1" stop-color="{c['bg']}"/></linearGradient>
      <linearGradient id="sg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{c['cpu']}" stop-opacity=".22"/><stop offset="1" stop-color="{c['cpu']}" stop-opacity="0"/></linearGradient>
      <clipPath id="frame"><rect width="{W}" height="{H}" rx="24"/></clipPath>
    </defs>
    <g clip-path="url(#frame)">
      <rect width="{W}" height="{H}" fill="{c['bg']}"/>
      <rect width="{W}" height="{H}" fill="url(#grid)"/>
      <g opacity="{c['glow']}" filter="url(#blur)">
        <circle class="blob" cx="180" cy="40" r="170" fill="{c['cpu']}" opacity=".45"/>
        <circle class="blob blob2" cx="1040" cy="60" r="150" fill="{c['mem']}" opacity=".35"/>
      </g>
      <rect width="{W}" height="{H}" fill="url(#fade)"/>
      <g transform="translate(0,{H - 70})" opacity=".9">
        <g class="scroll"><path d="{spark} L{W},60 L0,60Z" fill="url(#sg)"/><path d="{spark}" fill="none" stroke="{c['cpu']}" stroke-width="1.6" opacity=".7"/>
          <g transform="translate({W},0)"><path d="{spark} L{W},60 L0,60Z" fill="url(#sg)"/><path d="{spark}" fill="none" stroke="{c['cpu']}" stroke-width="1.6" opacity=".7"/></g></g>
        <g class="scroll" style="animation-duration:22s"><path d="{spark2}" fill="none" stroke="{c['net']}" stroke-width="1.2" stroke-dasharray="3 4" opacity=".55"/>
          <g transform="translate({W},0)"><path d="{spark2}" fill="none" stroke="{c['net']}" stroke-width="1.2" stroke-dasharray="3 4" opacity=".55"/></g></g>
      </g>
    </g>
    <rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="24" fill="none" stroke="{c['line']}"/>

    <g class="rise">
      <g class="mark" transform="translate(66,70)">
        <rect width="20" height="20" rx="5" fill="{c['cpu']}"/><rect x="25" width="20" height="20" rx="5" fill="{c['mem']}"/>
        <rect y="25" width="20" height="20" rx="5" fill="{c['disk']}"/><rect x="25" y="25" width="20" height="20" rx="5" fill="{c['net']}"/>
      </g>
      <text x="128" y="88" class="mono" font-size="17" fill="{c['muted']}">~/{HANDLE}</text>
      <circle cx="134" cy="106" r="4" fill="{c['ok']}"/><circle class="ping" cx="134" cy="106" r="4" fill="none" stroke="{c['ok']}" stroke-width="1.5"/>
      <text x="146" y="112" class="mono" font-size="15" fill="{c['ok']}">online · shipping</text>
    </g>
    <text x="64" y="208" class="sans rise d1" font-size="62" font-weight="700" letter-spacing="-1.5" fill="{c['text']}">{escape(NAME)}</text>
    <g class="rise d2">
      <text x="{x0}" y="{y0}" class="mono" font-size="{size}" fill="{c['mem']}">❯</text>
      {phrases}
    </g>
    <text x="66" y="324" class="sans rise d3" font-size="20" fill="{c['muted']}">From the Linux layer up to the pixels.</text>

    <g class="rise d2">
      <rect x="{px}" y="{py}" width="{pw_}" height="{ph}" rx="16" fill="{c['panel']}" stroke="{c['line']}"/>
      <text x="{px + 28}" y="{py + 46}" class="mono" font-size="16" fill="{c['muted']}"><tspan fill="{c['mem']}">{HANDLE}</tspan>@<tspan fill="{c['cpu']}">jaipur</tspan>  $ fetch</text>
      <line x1="{px + 28}" x2="{px + pw_ - 28}" y1="{py + 64}" y2="{py + 64}" stroke="{c['line']}"/>
      <g class="fetch">{fetch}</g>
      {swatches}
      <rect class="caret" x="{px + pw_ - 44}" y="{py + 32}" width="9" height="18" rx="2" fill="{c['mem']}"/>
    </g>
    """
    return svg(W, H, body, css, f"{NAME}: AI / LLM developer, full-stack")


# ----------------------------- project cards -----------------------------
def card_anim(kind, c, col, x, y):
    """A tiny unique animation in the card's top-right corner, centred on (x, y)."""
    if kind == "orbit":
        return (f'<g transform="translate({x},{y})"><circle r="26" fill="none" stroke="{c["line"]}" stroke-width="1.5"/>'
                f'<ellipse rx="26" ry="9" fill="none" stroke="{col}" stroke-width="1.5" opacity=".5"/>'
                f'<g class="spin"><circle cx="26" r="4" fill="{col}"/></g><circle r="5" fill="{col}" opacity=".85"/></g>')
    if kind == "spark":
        d = sparkline(140, 40, 2.2, 16)
        return (f'<g transform="translate({x - 70},{y - 20})"><clipPath id="sc"><rect width="70" height="40"/></clipPath>'
                f'<g clip-path="url(#sc)"><g class="slide"><path d="{d}" fill="none" stroke="{col}" stroke-width="2"/></g></g>'
                f'<circle cx="70" cy="20" r="3" fill="{col}" class="pulse"/></g>')
    if kind == "eq":
        bars = "".join(f'<rect x="{i * 12 - 28}" y="-22" width="7" height="44" rx="3" fill="{col}" class="eqb" style="animation-delay:-{i * .23:.2f}s;animation-duration:{.9 + i * .17:.2f}s"/>' for i in range(5))
        return f'<g transform="translate({x},{y})">{bars}</g>'
    if kind == "tokens":
        dots = "".join(f'<rect x="{-36 + i * 13}" y="-4" width="9" height="9" rx="2.5" fill="{col}" class="tok" style="animation-delay:{i * .18:.2f}s"/>' for i in range(6))
        return f'<g transform="translate({x},{y})">{dots}</g>'
    if kind == "cube":
        return (f'<g transform="translate({x},{y})"><g class="spin slow"><rect x="-17" y="-17" width="34" height="34" rx="4" fill="none" stroke="{col}" stroke-width="2"/>'
                f'<rect x="-10" y="-10" width="20" height="20" rx="3" fill="{col}" opacity=".35"/></g>'
                f'<g class="spin rev"><rect x="-24" y="-24" width="48" height="48" rx="8" fill="none" stroke="{c["line"]}" stroke-width="1.5"/></g></g>')
    if kind == "chat":
        return (f'<g transform="translate({x - 30},{y - 18})"><rect width="42" height="20" rx="10" fill="{c["panel2"]}" stroke="{c["line"]}" class="b1"/>'
                f'<rect x="18" y="18" width="42" height="20" rx="10" fill="{col}" opacity=".85" class="b2"/>'
                + "".join(f'<circle cx="{11 + i * 10}" cy="10" r="2.5" fill="{c["muted"]}" class="dot" style="animation-delay:{i * .2:.1f}s"/>' for i in range(3))
                + '</g>')
    return ""


def card(p, t):
    W, H = 480, 236
    c = t
    col = c[p["accent"]]
    css = f"""
    .sans{{font-family:{SANS}}} .mono{{font-family:{MONO}}}
    .spin{{animation:spin 6s linear infinite}} .slow{{animation-duration:14s}} .rev{{animation-direction:reverse;animation-duration:20s}}
    @keyframes spin{{to{{transform:rotate(360deg)}}}}
    .slide{{animation:slide 4s linear infinite}} @keyframes slide{{to{{transform:translateX(-70px)}}}}
    .pulse{{animation:pulse 1.4s ease-in-out infinite;transform-box:fill-box;transform-origin:center}} @keyframes pulse{{50%{{transform:scale(1.8);opacity:.4}}}}
    .eqb{{animation:eq 1s ease-in-out infinite alternate;transform-box:fill-box;transform-origin:center}} @keyframes eq{{from{{transform:scaleY(.25)}}to{{transform:scaleY(1)}}}}
    .tok{{animation:tok 1.8s cubic-bezier(.2,.8,.2,1) infinite;opacity:0}} @keyframes tok{{0%{{opacity:0;transform:translateY(6px)}}30%,70%{{opacity:1;transform:none}}100%{{opacity:0}}}}
    .b1{{animation:pop 3s ease-in-out infinite}} .b2{{animation:pop 3s ease-in-out infinite;animation-delay:1.2s}}
    @keyframes pop{{0%,10%{{opacity:0;transform:translateY(4px)}}25%,85%{{opacity:1;transform:none}}100%{{opacity:0}}}}
    .dot{{animation:dot 1s ease-in-out infinite}} @keyframes dot{{50%{{transform:translateY(-3px)}}}}
    .sweep{{animation:sweep 5s cubic-bezier(.45,0,.2,1) infinite}} @keyframes sweep{{0%{{transform:translateX(-200px)}}60%,100%{{transform:translateX({W}px)}}}}
    """
    chips, cx = "", 28
    for ch in p["chips"]:
        w = mono_w(ch, 14) + 22
        if cx + w > W - 24:
            break
        chips += (f'<rect x="{cx}" y="{H - 54}" width="{w:.0f}" height="30" rx="15" fill="{c["panel2"]}" stroke="{c["line"]}"/>'
                  f'<text x="{cx + 11}" y="{H - 34}" class="mono" font-size="14" fill="{c["muted"]}">{escape(ch)}</text>')
        cx += w + 8
    lines = "".join(f'<text x="28" y="{124 + i * 26}" class="sans" font-size="17.5" fill="{c["muted"]}">{escape(l)}</text>' for i, l in enumerate(p["lines"]))
    body = f"""
    <defs><clipPath id="f"><rect width="{W}" height="{H}" rx="18"/></clipPath>
      <linearGradient id="sw" x1="0" x2="1"><stop offset="0" stop-color="{col}" stop-opacity="0"/><stop offset=".5" stop-color="{col}" stop-opacity=".9"/><stop offset="1" stop-color="{col}" stop-opacity="0"/></linearGradient>
      <radialGradient id="gl"><stop offset="0" stop-color="{col}" stop-opacity=".22"/><stop offset="1" stop-color="{col}" stop-opacity="0"/></radialGradient></defs>
    <g clip-path="url(#f)">
      <rect width="{W}" height="{H}" fill="{c['panel']}"/>
      <circle cx="{W - 60}" cy="40" r="170" fill="url(#gl)" opacity="{c['glow']}"/>
      <rect class="sweep" y="0" width="200" height="2" fill="url(#sw)"/>
    </g>
    <rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="18" fill="none" stroke="{c['line']}"/>
    <circle cx="33" cy="36" r="4.5" fill="{col}"/>
    <text x="46" y="41" class="mono" font-size="13.5" letter-spacing=".6" fill="{c['muted']}">{escape(p['tag'])}</text>
    <text x="27" y="88" class="sans" font-size="31" font-weight="700" letter-spacing="-.6" fill="{c['text']}">{escape(p['title'])}</text>
    {lines}
    {chips}
    {card_anim(p['anim'], c, col, W - 58, 56)}
    """
    return svg(W, H, body, css, f"{p['title']}: {' '.join(p['lines'])}")


# ----------------------------- stack -----------------------------
def stack(t):
    W = 900
    c = t
    rows, y = "", 34
    css = f""".sans{{font-family:{SANS}}} .mono{{font-family:{MONO}}}
    .row{{animation:rise .8s cubic-bezier(.2,.8,.2,1) both}} @keyframes rise{{from{{opacity:0;transform:translateX(-10px)}}}}"""
    for i, (label, acc, items) in enumerate(STACK):
        col = c[acc]
        x = 168
        chips = ""
        label_row_start = y  # label sits on the first line of chips
        for it in items:
            w = mono_w(it, 15) + 26
            if x + w > W - 24:
                x = 168
                y += 44
            chips += (f'<g class="chip"><rect x="{x:.0f}" y="{y - 22}" width="{w:.0f}" height="34" rx="9" fill="{c["panel2"]}" stroke="{c["line"]}"/>'
                      f'<rect x="{x:.0f}" y="{y - 22}" width="3" height="34" rx="1.5" fill="{col}"/>'
                      f'<text x="{x + 14:.0f}" y="{y}" class="mono" font-size="15" fill="{c["text"]}">{escape(it)}</text></g>')
            x += w + 9
        label_y = y - 1.5 if label_row_start is None else label_row_start
        rows += (f'<g class="row" style="animation-delay:{i * .12:.2f}s">'
                 f'<rect x="30" y="{label_y - 10.5}" width="7" height="7" rx="2" fill="{col}"/>'
                 f'<text x="46" y="{label_y}" class="sans" font-size="17" font-weight="600" fill="{c["text"]}">{escape(label)}</text>{chips}</g>')
        y += 56
    H = y - 10
    body = (f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="20" fill="{c["panel"]}" stroke="{c["line"]}"/>'
            f'<line x1="150" x2="150" y1="20" y2="{H - 20}" stroke="{c["line"]}"/>{rows}')
    # shift everything down a little so the first row has breathing room
    return svg(W, H + 16, f'<g transform="translate(0,8)">{body}</g>', css, "Tech stack")


# ----------------------------- footer -----------------------------
def footer(t):
    W, H = 1200, 90
    c = t
    d = sparkline(W, 40, 3.3)
    css = f""".mono{{font-family:{MONO}}} .scroll{{animation:scroll 16s linear infinite}} @keyframes scroll{{to{{transform:translateX(-{W}px)}}}}
    .beat{{animation:beat 2s ease-in-out infinite;transform-box:fill-box;transform-origin:center}} @keyframes beat{{50%{{transform:scale(1.5);opacity:.5}}}}"""
    body = f"""<defs><linearGradient id="fd" x1="0" x2="1"><stop offset="0" stop-color="{c['bg']}"/><stop offset=".15" stop-color="{c['bg']}" stop-opacity="0"/><stop offset=".85" stop-color="{c['bg']}" stop-opacity="0"/><stop offset="1" stop-color="{c['bg']}"/></linearGradient></defs>
    <g transform="translate(0,6)"><g class="scroll"><path d="{d}" fill="none" stroke="{c['mem']}" stroke-width="1.6" opacity=".7"/><g transform="translate({W},0)"><path d="{d}" fill="none" stroke="{c['mem']}" stroke-width="1.6" opacity=".7"/></g></g></g>
    <rect width="{W}" height="50" fill="url(#fd)"/>
    <circle cx="{W/2 - 222}" cy="71" r="5" fill="{c['ok']}" class="beat"/>
    <text x="{W/2 - 204}" y="77" class="mono" font-size="19" fill="{c['muted']}">uptime: always shipping · thanks for visiting</text>"""
    return svg(W, H, body, css, "Thanks for visiting")


def write(name, content):
    (OUT / name).write_text(content, encoding="utf-8")


for theme, t in THEMES.items():
    write(f"header-{theme}.svg", header(t))
    write(f"stack-{theme}.svg", stack(t))
    write(f"footer-{theme}.svg", footer(t))
    for p in PROJECTS:
        write(f"card-{p['key']}-{theme}.svg", card(p, t))
print("built", len(list(OUT.glob("*.svg"))), "svgs in", OUT)
