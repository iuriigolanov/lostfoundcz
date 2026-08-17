# Image Guide — Lost & Found Catering Calculator

All images live in `catering-calculator/img/` and are referenced by **exact filename** from `index.html`. To update or replace a photo: export/crop it to the spec below, save it into `img/` under the **same filename**, overwriting the old one — no code changes needed. If a file is missing, the page falls back to a placeholder box automatically, so a bad filename never breaks the layout, it just leaves a gap.

| Filename | Used for | Status | Required size (W×H) | Aspect ratio | Format | Notes |
|---|---|---|---|---|---|---|
| `logo-partner.png` | Header, left logo badge (the client/partner booking the event) | ⬜ Placeholder — needs a logo | up to 400×200 (min 200×100) | flexible, fits inside a 128×64 box | **PNG**, transparent background | `object-contain` (never cropped) — the whole logo shrinks to fit inside the box with padding, so any aspect ratio works, but a very tall or very wide logo will render smaller. Left empty by design until a specific corporate client is confirmed for an event. |
| `logo-venue.png` | Header, right logo badge (Lost & Found's own logo) | ⬜ Placeholder — needs a logo | up to 400×200 (min 200×100) | flexible, fits inside a 128×64 box | **PNG**, transparent background | Same `object-contain` behavior as logo-partner. A transparent-background export of the neon wordmark logo works best here. |
| `hero-bg.jpg` | Header background (top banner) | ✅ Live | 1600×727 (min 1200×545) | ~2.2:1 (wide banner) | JPG | Displayed behind a 50% black overlay + text, so avoid busy detail in the center where the title sits. `object-cover`, so extra height/width is safely cropped. |
| `gallery-1.jpg` | "Feel the Room" gallery, tile 1 (bar / neon interior) | ✅ Live | 900×600 (min 400×267) | 3:2 | JPG | Grid tile, `object-cover`. Keep the main subject centered — edges get cropped differently on mobile (2-col) vs desktop (4-col). |
| `gallery-2.jpg` | "Feel the Room" gallery, tile 2 (lounge seating) | ✅ Live | 900×600 (min 400×267) | 3:2 | JPG | Same crop rules as gallery-1. Currently a basement lounge/seating shot, not hookah specifically — swap for an actual hookah photo if one becomes available. |
| `gallery-3.jpg` | "Feel the Room" gallery, tile 3 (crowd / party) | ✅ Live | 900×600 (min 400×267) | 3:2 | JPG | Same crop rules as gallery-1. |
| `gallery-4.jpg` | "Feel the Room" gallery, tile 4 (signature cocktails) | ✅ Live | 900×600 (min 400×267) | 3:2 | JPG | Same crop rules as gallery-1. |
| `pkg-economy.jpg` | Package accordion — Basic tier dish photo (filename kept as `pkg-economy.jpg` — tied to the package's internal `id`, not its display name) | ✅ Live (3-photo collage: nachos, cherry beer, shot flight) | 1600×300 (min 900×170) | ~5.3:1 (very wide strip) | JPG | Fixed-height (96px) strip that stretches full-width, so the on-screen ratio actually ranges ~3:1 on mobile to ~8:1 on desktop. Built as 3 side-by-side panels — if replacing with a single photo, use a wide master crop and center the subject. |
| `pkg-standard.jpg` | Package accordion — Casual tier dish photo (filename kept as `pkg-standard.jpg` — tied to the package's internal `id`, not its display name) | ⬜ Placeholder — needs a photo | 1600×300 (min 900×170) | ~5.3:1 (very wide strip) | JPG | Same spec and cropping caveat as pkg-economy. |
| `pkg-premium.jpg` | Package accordion — Premium tier dish photo | ⬜ Placeholder — needs a photo | 1600×300 (min 900×170) | ~5.3:1 (very wide strip) | JPG | Same spec and cropping caveat as pkg-economy. |

## General rules

- **Filenames are case-sensitive and must match exactly** — `Hero-BG.jpg` will not be picked up.
- **Photos are JPG, logos are PNG** — the two logo slots (`logo-partner.png`, `logo-venue.png`) are the only PNGs; every other slot is JPG. The code doesn't reference alternate extensions, so a `.jpeg` or `.webp` file won't be picked up even if renamed.
- **Keep files under ~300 KB each** where possible (all current live photos are 60–270 KB) — this is a single-page site with no lazy-loading/CDN, so total page weight matters for load time.
- Photo slots use CSS `object-fit: cover` (crops to fill), so they don't need to be pixel-perfect — slight over-cropping on the edges is fine, but the *subject* should be reasonably centered. **Logo slots use `object-fit: contain`** (never cropped, just shrunk to fit) — any logo aspect ratio works.
- To add a **new** image slot (e.g. a 5th gallery photo), both the filename in `index.html` and this table need updating together — that's a code change, not just a file swap.

## Current live photos — source & rights note

`hero-bg.jpg` is the venue's own official photo (from lostfoundcz.com). `gallery-1.jpg`, `gallery-2.jpg`, and `gallery-4.jpg` appear to be the venue's own Instagram photos (supplied directly). `gallery-3.jpg` is a guest-submitted photo pulled from the venue's Google Maps listing (public reviews) — worth confirming there's no objection to using it commercially before this goes live, since it wasn't taken by or explicitly licensed to the venue. `pkg-economy.jpg` is a collage built from venue-supplied photos.

**Removed:** `proof.jpg` is no longer referenced — the social-proof block was replaced by the Google Maps reviews carousel (text-only, no photo). The file can stay in `img/` harmlessly or be deleted; it just won't render anywhere.
