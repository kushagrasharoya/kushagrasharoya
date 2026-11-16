#!/usr/bin/env python3
"""Generate assets/hero.svg.
Sun = the username. Each PUBLIC repo = a planet orbiting the sun.
Each planet has moons = the languages (GitHub language stats) + tech stack (repo topics) used in that repo.
Usage: python scripts/generate_solar_system.py <username> [out.svg] [mock.json]
Uses GITHUB_TOKEN if present. Standard library only."""
import json, math, os, random, sys, urllib.request, zlib
from xml.sax.saxutils import escape

user = sys.argv[1]
out = sys.argv[2] if len(sys.argv) > 2 else "assets/hero.svg"
mock = sys.argv[3] if len(sys.argv) > 3 else None
TOKEN = os.environ.get("GITHUB_TOKEN")

def api(url):
    req = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json", "User-Agent": "solar-system-profile"})
    if TOKEN:
        req.add_header("Authorization", f"Bearer {TOKEN}")
    return json.load(urllib.request.urlopen(req, timeout=30))

def fetch_repos():
    if mock:
        return json.load(open(mock))
    repos, page = [], 1
    while True:
        data = api(f"https://api.github.com/users/{user}/repos?type=owner&per_page=100&page={page}&sort=pushed")
        repos += data
        if len(data) < 100:
            return repos
        page += 1

def fetch_langs(r):
    if mock:
        return r.get("languages", {})
    try:
        return api(r["languages_url"])
    except Exception:
        return {r["language"]: 1} if r.get("language") else {}

repos = [r for r in fetch_repos()
         if not r.get("private") and not r.get("fork") and not r.get("archived")
         and r["name"].lower() != user.lower()]
repos.sort(key=lambda r: r.get("pushed_at") or "", reverse=True)

LANG = {"Python": "#3776AB", "JavaScript": "#F7DF1E", "TypeScript": "#3178C6", "HTML": "#E34F26",
        "CSS": "#A78BFA", "Java": "#F97316", "C": "#94A3B8", "C++": "#F472B6", "Jupyter Notebook": "#F37626",
        "Shell": "#34D399", "Go": "#00ADD8", "Rust": "#DEA584", "PHP": "#8892BF", "Kotlin": "#A97BFF",
        "Dart": "#38BDF8", "C#": "#22C55E", "Ruby": "#EF4444", "SCSS": "#EC4899", "Batchfile": "#C1F12E"}
TECH = {"react": "#61DAFB", "nodejs": "#68A063", "node": "#68A063", "express": "#E5E7EB", "flask": "#E5E7EB",
        "fastapi": "#05998B", "django": "#44B78B", "tensorflow": "#FF6F00", "pytorch": "#EE4C2C",
        "mysql": "#4479A1", "mongodb": "#47A248", "docker": "#2496ED", "langchain": "#34D399",
        "chartjs": "#FF6384", "chart-js": "#FF6384", "llm": "#C084FC", "rag": "#C084FC", "iot": "#22D3EE"}
PLANET = ["#60A5FA", "#F472B6", "#34D399", "#FBBF24", "#A78BFA", "#FB7185", "#22D3EE", "#FB923C", "#C084FC", "#4ADE80", "#38BDF8", "#F87171"]

def moons_for(r):
    langs = sorted(fetch_langs(r).items(), key=lambda kv: -kv[1])
    items = [(l, LANG.get(l, "#CBD5E1")) for l, _ in langs[:3]]
    have = {n.lower() for n, _ in items}
    for t in r.get("topics", []) or []:
        if t.lower() not in have and len(items) < 5:
            items.append((t, TECH.get(t.lower(), "#E2E8F0")))
            have.add(t.lower())
    return items

W, H, CX, CY = 1000, 480, 500, 262
RINGS = [(205, 4), (290, 6), (375, 8), (450, 10)]
RINGS = [(rx, cap, rx * 0.37) for rx, cap in RINGS]
MAXN = sum(c for _, c, _ in RINGS)
shown, extra = repos[:MAXN], max(0, len(repos) - MAXN)
FONT = "font-family:'JetBrains Mono','SFMono-Regular',Consolas,monospace"

def path(rx, ry, cw):
    sw = 1 if cw else 0
    return f"M{CX+rx},{CY} a{rx},{ry} 0 1,{sw} {-2*rx},0 a{rx},{ry} 0 1,{sw} {2*rx},0"

rng = random.Random(7)
stars = "".join(
    f'<circle cx="{rng.uniform(0,W):.0f}" cy="{rng.uniform(0,H):.0f}" r="{rng.choice([.6,.8,1,1.3])}" fill="#fff">'
    f'<animate attributeName="opacity" values="0.15;1;0.15" dur="{rng.uniform(2,6):.1f}s" begin="-{rng.uniform(0,6):.1f}s" repeatCount="indefinite"/></circle>'
    for _ in range(130))

rings_svg, bodies, i = [], [], 0
for k, (rx, cap, ry) in enumerate(RINGS):
    chunk = shown[i:i + cap]
    i += cap
    if not chunk:
        continue
    rings_svg.append(f'<ellipse cx="{CX}" cy="{CY}" rx="{rx}" ry="{ry:.0f}" fill="none" stroke="#94A3B8" stroke-opacity=".22" stroke-dasharray="3 6"/>')
    dur = 26 + k * 16
    for j, r in enumerate(chunk):
        pc = PLANET[zlib.crc32(r["name"].encode()) % len(PLANET)]
        size = 9 + min(5, math.log2(1 + r.get("stargazers_count", 0) * 3 + r.get("size", 0) / 800))
        begin = dur * j / len(chunk) + k * 3
        name = r["name"] if len(r["name"]) <= 20 else r["name"][:19] + "…"
        ms = moons_for(r)
        mr = size + 12
        moons = [f'<circle r="{mr:.1f}" fill="none" stroke="#fff" stroke-opacity=".12" stroke-dasharray="2 3"/>']
        for m, (mn, mc) in enumerate(ms):
            mdur = 5 + m * 1.5
            moons.append(f'<g><animateMotion dur="{mdur}s" begin="-{mdur*m/len(ms):.1f}s" repeatCount="indefinite" path="M{mr:.1f},0 a{mr:.1f},{mr:.1f} 0 1,1 {-2*mr:.1f},0 a{mr:.1f},{mr:.1f} 0 1,1 {2*mr:.1f},0"/>'
                         f'<circle r="3.4" fill="{mc}"/><title>{escape(mn)}</title></g>')
        stack = " · ".join(n for n, _ in ms)
        if len(stack) > 28: stack = stack[:27] + "…"
        bodies.append(f'''<g><animateMotion dur="{dur}s" begin="-{begin:.1f}s" repeatCount="indefinite" path="{path(rx, ry, k % 2 == 0)}"/>
<title>{escape(r["name"])} — {escape(", ".join(n for n, _ in ms) or "no languages yet")}</title>
<circle r="{size*2:.1f}" fill="{pc}" opacity=".14"/><circle r="{size:.1f}" fill="{pc}"/><circle r="{size:.1f}" fill="url(#shade)"/>
{"".join(moons)}
<text y="{mr+14:.1f}" text-anchor="middle" fill="#E5E7EB" font-size="10" font-weight="700" stroke="#02030A" stroke-width="3" paint-order="stroke" style="{FONT}">{escape(name)}</text>
<text y="{mr+25:.1f}" text-anchor="middle" fill="#9CA3AF" font-size="8" stroke="#02030A" stroke-width="2.5" paint-order="stroke" style="{FONT}">{escape(stack)}</text></g>''')

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
<defs>
<radialGradient id="bg" cx="50%" cy="50%" r="75%"><stop offset="0" stop-color="#0B1030"/><stop offset="1" stop-color="#02030A"/></radialGradient>
<radialGradient id="sun" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="#FFF3B0"/><stop offset=".45" stop-color="#FBBF24"/><stop offset="1" stop-color="#F97316"/></radialGradient>
<radialGradient id="glow" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="#FBBF24" stop-opacity=".55"/><stop offset="1" stop-color="#FBBF24" stop-opacity="0"/></radialGradient>
<radialGradient id="shade" cx="35%" cy="30%" r="75%"><stop offset="0" stop-color="#fff" stop-opacity=".35"/><stop offset=".6" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".55"/></radialGradient>
<linearGradient id="comet" x1="0" x2="1"><stop offset="0" stop-color="#A5F3FC" stop-opacity="0"/><stop offset="1" stop-color="#fff"/></linearGradient>
<linearGradient id="title" x1="0" x2="1"><stop offset="0" stop-color="#FDE68A"/><stop offset="1" stop-color="#A78BFA"/></linearGradient>
<clipPath id="c"><rect width="{W}" height="{H}" rx="18"/></clipPath>
</defs>
<rect width="{W}" height="{H}" rx="18" fill="url(#bg)"/>
<g clip-path="url(#c)">
{stars}
<ellipse cx="150" cy="420" rx="260" ry="90" fill="#6D28D9" opacity=".10"/>
<ellipse cx="880" cy="90" rx="240" ry="80" fill="#10B981" opacity=".08"/>
{"".join(rings_svg)}
<circle cx="{CX}" cy="{CY}" r="110" fill="url(#glow)"><animate attributeName="r" values="95;120;95" dur="6s" repeatCount="indefinite"/></circle>
<circle cx="{CX}" cy="{CY}" r="34" fill="url(#sun)"/>
<circle cx="{CX}" cy="{CY}" r="34" fill="none" stroke="#FDE68A" stroke-width="3"/>
<text x="{CX}" y="{CY+58}" text-anchor="middle" fill="#FDE68A" font-size="13" font-weight="700" letter-spacing="1" stroke="#02030A" stroke-width="3" paint-order="stroke" style="{FONT}">{escape(user)}</text>
{"".join(bodies)}
<g><animateTransform attributeName="transform" type="translate" values="-200,40;1200,330" dur="9s" begin="1s" repeatCount="indefinite"/>
<rect x="-90" y="-1" width="90" height="2" rx="1" fill="url(#comet)"/><circle r="3" fill="#fff"/></g>
<text x="40" y="62" fill="url(#title)" font-size="34" font-weight="800" style="{FONT}">KUSHAGRA SHAROYA</text>
</g></svg>'''
os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
open(out, "w", encoding="utf-8").write(svg)
print(f"wrote {out}: {len(shown)} repos shown, {extra} extra")
