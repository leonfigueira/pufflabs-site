#!/usr/bin/env python3
"""Generates one landing page per app from _src/apps-*.json.
Run after editing the JSON: python3 _src/build.py"""
import json, glob, os, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
apps = {}
for f in sorted(glob.glob(os.path.join(ROOT, "_src", "apps-*.json"))):
    apps.update(json.load(open(f)))

HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{name} · Puff Labs</title>
<meta name="description" content="{tagline} {intro_short}">
<meta name="keywords" content="{keywords}">
<link rel="icon" type="image/png" href="assets/favicon.png">
<link rel="canonical" href="https://pufflabs.work/{slug}.html">
<meta property="og:title" content="{name}">
<meta property="og:description" content="{tagline}">
<meta property="og:type" content="product">
<meta property="og:image" content="https://pufflabs.work/assets/apps/{slug}.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300..600;1,9..144,300..600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/style.css">
<script type="application/ld+json">{schema}</script>
</head>
<body>
<header>
  <nav class="nav">
    <a class="brand" href="/"><span class="dot"></span> Puff Labs</a>
    <div class="nav-links">
      <a href="/#apps">Apps</a>
      <a href="updates.html">Updates</a>
      <a href="/#about">About</a>
    </div>
  </nav>
</header>
<main class="wrap">
  <section class="app-hero">
    <img class="appicon" src="assets/apps/{slug}.png" alt="{name} app icon" width="96" height="96">
    <div>
      <h1>{short}</h1>
      <p class="lede">{tagline}</p>
      {cta}
      <div class="devices-strip">{devices_html}</div>
    </div>
  </section>
"""

FOOT = """  <section class="closer">
    <h2>{closer_h}</h2>
    <p>{closer_p}</p>
    {cta}
  </section>
  <a class="backlink" href="/#apps">← All Puff Labs apps</a>
</main>
<footer>
  <div class="wrap foot-row">
    <span>© 2026 Puff Labs</span>
    <a href="mailto:leonfigueira@gmail.com">leonfigueira@gmail.com</a>
    <span class="spacer"></span>
    <a href="https://leonfigueira.github.io/runlow-site/privacy.html">Privacy</a>
    <a href="https://leonfigueira.github.io/runlow-site/support.html">Support</a>
  </div>
</footer>
</body>
</html>
"""

for slug, a in apps.items():
    live = bool(a["store"])
    cta = (f'<a class="buy" href="https://apps.apple.com/gb/app/id{a["store"]}">Get it on the App Store · {a["price"]}</a>'
           if live else '<span class="pending">Built, and with Apple for review</span>')
    schema = json.dumps({
        "@context":"https://schema.org","@type":"SoftwareApplication","name":a["name"],
        "operatingSystem":"iOS, macOS","applicationCategory":"MobileApplication",
        "description":a["tagline"],
        "author":{"@type":"Organization","name":"Puff Labs"},
        **({"offers":{"@type":"Offer","price":a["price"].replace("£",""),"priceCurrency":"GBP"}} if live else {})
    })
    devices_html = "".join(f"<span>{d.strip()}</span>" for d in a["devices"].split("·"))
    html_out = HEAD.format(slug=slug, cta=cta, schema=schema, devices_html=devices_html,
                           intro_short=a["intro"][:110], **a)

    shots = sorted(glob.glob(os.path.join(ROOT, f"assets/shots/{slug}/*.png")))
    if shots:
        html_out += '  <section style="padding-top:24px">\n    <div class="gallery">\n'
        for sh in shots:
            rel = os.path.relpath(sh, ROOT)
            html_out += f'      <img src="{rel}" alt="{a["short"]} screenshot" loading="lazy">\n'
        html_out += '    </div>\n  </section>\n'

    html_out += f'  <section class="feature" style="border-top:none">\n    <p class="lede">{a["intro"]}</p>\n  </section>\n'
    for s in a["sections"]:
        html_out += f'  <section class="feature">\n    <h2>{s["h"]}</h2>\n'
        if s.get("p"): html_out += f'    <p>{s["p"]}</p>\n'
        if s.get("ul"):
            html_out += "    <ul>\n" + "".join(f"      <li>{li}</li>\n" for li in s["ul"]) + "    </ul>\n"
        html_out += "  </section>\n"

    closer_h = f"Get {a['short']}" if live else f"{a['short']} is coming"
    closer_p = (f"One purchase covers {a['devices']}. No subscription, no account, no tracking."
                if live else "It is built and with Apple for review. It will appear here the day it lands.")
    html_out += FOOT.format(cta=cta, closer_h=closer_h, closer_p=closer_p)
    open(os.path.join(ROOT, f"{slug}.html"), "w").write(html_out)
    print(f"  {slug}.html  {len(shots)} shots, {len(a['sections'])} sections")
