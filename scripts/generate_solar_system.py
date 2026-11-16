#!/usr/bin/env python3
"""Generate assets/hero.svg: every PUBLIC repo of a user orbits the sun (the username).
Usage: python scripts/generate_solar_system.py <username> [out.svg] [mock.json]
Uses GITHUB_TOKEN if present. Standard library only."""
import json, math, os, random, sys, urllib.request
from datetime import datetime, timezone
from xml.sax.saxutils import escape

user = sys.argv[1]
out = sys.argv[2] if len(sys.argv) > 2 else "assets/hero.svg"
mock = sys.argv[3] if len(sys.argv) > 3 else None

def fetch_repos():
    if mock:
        return json.load(open(mock))
    repos, page = [], 1
    while True:
        req = urllib.request.Request(
            f"https://api.github.com/users/{user}/repos?type=owner&per_page=100&page={page}&sort=pushed",
            headers={"Accept": "application/vnd.github+json", "User-Agent": "solar-system-profile"})
        tok = os.environ.get("GITHUB_TOKEN")
        if tok:
            req.add_header("Authorization", f"Bearer {tok}")
        data = json.load(urllib.request.urlopen(req, timeout=30))
        repos += data
        if len(data) < 100:
            return repos
        page += 1

repos = [r for r in fetch_repos()
         if not r.get("private") and not r.get("fork") and not r.get("archived")
         and r["name"].lower() != user.lower()]          # skip the profile repo itself
repos.sort(key=lambda r: r.get("pushed_at") or "", reverse=True)

COLORS = {"Python": "#3776AB", "JavaScript": "#F7DF1E", "TypeScript": "#3178C6", "HTML": "#E34F26",
          "CSS": "#A78BFA", "Java": "#F97316", "C": "#94A3B8", "C++": "#F472B6", "Jupyter Notebook": "#F37626",
          "Shell": "#34D399", "Go": "#00ADD8", "Rust": "#DEA584", "PHP": "#8892BF", "Kotlin": "#A97BFF",
          "Dart": "#38BDF8", "C#": "#22C55E", "Ruby": "#EF4444", "SCSS": "#EC4899"}
def color(lang): return COLORS.get(lang, "#CBD5E1")

W, H, CX, CY = 1000, 480, 500, 272
RINGS = [(175, 4), (265, 6), (350, 8), (430, 10)]   # (rx, capacity)
RINGS = [(rx, cap, rx * 0.40) for rx, cap in RINGS]
MAXN = sum(c for _, c, _ in RINGS)
shown, extra = repos[:MAXN], max(0, len(repos) - MAXN)
FONT = "font-family:'JetBrains Mono','SFMono-Regular',Consolas,monospace"
now = datetime.now(timezone.utc)

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
    if not chunk and k > 0:
        continue
    rings_svg.append(f'<ellipse cx="{CX}" cy="{CY}" rx="{rx}" ry="{ry:.0f}" fill="none" stroke="#94A3B8" stroke-opacity=".22" stroke-dasharray="3 6"/>')
    dur = 22 + k * 14
    for j, r in enumerate(chunk):
        lang = r.get("language")
        c = color(lang)
        size = 7 + min(6, math.log2(1 + r.get("stargazers_count", 0) * 3 + r.get("size", 0) / 800))
        pushed = r.get("pushed_at")
        recent = pushed and (now - datetime.fromisoformat(pushed.replace("Z", "+00:00"))).days <= 14
        begin = dur * j / len(chunk) + k * 3
        name = r["name"] if len(r["name"]) <= 20 else r["name"][:19] + "…"
        pulse = (f'<circle r="{size+4}" fill="none" stroke="{c}" stroke-opacity=".8"><animate attributeName="r" values="{size+2};{size+12};{size+2}" dur="2.5s" repeatCount="indefinite"/>'
                 f'<animate attributeName="stroke-opacity" values=".8;0;.8" dur="2.5s" repeatCount="indefinite"/></circle>') if recent else ""
        bodies.append(f'''<g><animateMotion dur="{dur}s" begin="-{begin:.1f}s" repeatCount="indefinite" path="{path(rx, ry, k % 2 == 0)}"/>
<title>{escape(r["name"])} · {escape(lang or "n/a")} · ★{r.get("stargazers_count", 0)}</title>
{pulse}<circle r="{size*2.1:.1f}" fill="{c}" opacity=".14"/><circle r="{size:.1f}" fill="{c}"/><circle r="{size:.1f}" fill="url(#shade)"/>
<text y="{size+13:.1f}" text-anchor="middle" fill="#E5E7EB" font-size="10" stroke="#02030A" stroke-width="3" paint-order="stroke" style="{FONT}">{escape(name)}</text></g>''')
    i += cap

langs = []
for r in shown:
    l = r.get("language")
    if l and l not in langs: langs.append(l)
legend = "".join(f'<circle cx="{44+n*0}" cy="0" r="0"/>' for n in range(0))
lx, leg = 40, []
for l in langs[:8]:
    leg.append(f'<circle cx="{lx}" cy="{H-30}" r="4.5" fill="{color(l)}"/><text x="{lx+10}" y="{H-26}" fill="#9CA3AF" font-size="11" style="{FONT}">{escape(l)}</text>')
    lx += 24 + len(l) * 7.2

sub = f"{len(repos)} public repositories in orbit" + (f" (+{extra} beyond the map)" if extra else "")
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
<text x="40" y="90" fill="#9CA3AF" font-size="14" style="{FONT}">Software Engineer · Python Developer · Aspiring AI Engineer</text>
<text x="40" y="112" fill="#6B7280" font-size="11" style="{FONT}">{escape(sub)} · auto-updated</text>
{"".join(leg)}
<text x="{W-40}" y="{H-26}" text-anchor="end" fill="#6B7280" font-size="11" style="{FONT}">pulse = pushed in last 14 days</text>
</g></svg>'''
os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
open(out, "w", encoding="utf-8").write(svg)
print(f"wrote {out}: {len(shown)} repos shown, {extra} extra")
