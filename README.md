# pufflabs-site

The Puff Labs studio site — https://pufflabs.work

Static HTML, no build step. GitHub Pages serves it; `CNAME` binds the custom domain.

## What this is NOT

This is **not** the app support site. Privacy pages, support pages and the two JSON feeds the
apps poll (`notices/v1.json`, `meters/v1.json`) live in **`runlow-site`** and are served from
`leonfigueira.github.io/runlow-site/`. Those URLs are compiled into shipped apps — never move,
rename or redirect that repo. This repo is the pretty human-facing front, and nothing depends
on it at runtime.

## Adding an update

Each update is its own page under `updates/<slug>.html` (own URL, two-column: article on the
left, an app-chip advert `<aside class="app-chip">` on the right). To add one:

1. Copy an existing page in `updates/` (e.g. `reprompt-6-99.html`) to `updates/<slug>.html`,
   rewrite the article body, and point the app chip at the relevant app (icon, tagline, price,
   App Store id, devices — all in `_src/apps-live.json`). Use absolute `/assets/...` paths.
2. Add a matching `<a class="post">` teaser to the top of the `.posts` list in `updates.html`
   (newest first) — the `.post` border-bottom draws the divider line between entries.
3. Add the same teaser to the Updates section of `index.html` so the homepage shows the latest.
