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

Add an `<article class="entry" id="…">` to `updates.html`, newest first, and add a matching
`<a class="post">` teaser to the Updates section of `index.html`.
