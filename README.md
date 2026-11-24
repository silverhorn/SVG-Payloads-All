# SVG-Payloads-All

Technique-grouped SVG payloads for testing **file upload** and **SVG processing** features: XSS, XXE, SSRF, SSTI and server-side renderer abuse. The focus is detection and proof of concept. Every payload uses a benign proof (`alert(document.domain)`, an out-of-band ping, `/etc/hostname`, `7*7`) rather than anything destructive.

> **Authorized testing only.** Use these only against targets you are explicitly permitted to test (bug bounty scope, pentest engagement, your own lab) and follow the program rules. No denial-of-service payloads (entity expansion, decompression bombs) are included on purpose.

## Layout

| Folder | Covers |
|---|---|
| `xss/` | Script execution when an SVG is opened or embedded in a browser |
| `xxe/` | External entities: file read, SSRF, blind and error-based, XInclude, external DTDs |
| `ssrf/` | Server-side fetches triggered by converters (`image`, `use`, `feImage`, CSS, `foreignObject`), IP-filter bypass list |
| `ssti/` | Template-injection probes in every place a server may reflect SVG content |
| `renderers/` | Notes per renderer (ImageMagick, librsvg, CairoSVG, Batik, Inkscape, headless Chrome, wkhtmltopdf) |
| `docs/` | Methodology, extension/MIME/sanitizer bypasses, references |
| `tools/build.py` | Fills in your callback host and writes ready-to-upload files to `dist/` |

## Quick start

1. Get a callback host (Burp Collaborator, interactsh, or your own server).
2. Fill it in:

   ```
   python3 tools/build.py --collab abc123.oast.fun
   ```

   Output goes to `dist/`. Use `--only xss xxe` to limit categories and `--list` to list files.
3. Upload payloads one at a time and note which one triggers. Callback paths are unique per payload (`/xxe-oob-general`, `/ssrf-iframe`, `/xss-sweep-rect-onclick`, ...), so a hit identifies the payload and the element that fired.
4. Read the category README to interpret the result, then follow `docs/methodology.md` for impact and reporting.

`xxe/dtd/` holds external DTDs for the blind XXE payloads. Host them on a server you control at the path the SVG expects (`http://COLLAB_HOST/xxe-oob.dtd`, `http://COLLAB_HOST/xxe-error.dtd`).

## Notes

- Payload behaviour varies by browser version, parser and configuration. Re-test in a current browser before reporting.
- Files are plain text. Review a payload before uploading it.
- `COLLAB_HOST` in the raw files is a placeholder; do not upload files from the repo root without running the build step.
