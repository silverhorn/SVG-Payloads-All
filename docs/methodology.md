# Methodology

## 1. Find the features

Places SVG shows up: avatars, logos, covers, product images, attachments, rich-text editors, import/export, "upload by URL", report or invoice generators, email templates, preview/thumbnail services, chat file sharing.

Also check APIs that accept the same data (mobile endpoints, GraphQL mutations, presigned uploads). Their validation often differs from the web UI.

## 2. Learn how the file is handled

| Question | How to check |
|---|---|
| Is `.svg` accepted at all? | Upload a harmless SVG (`rect`) |
| Is it validated by extension, `Content-Type`, content or all three? | Change each independently (see `bypasses.md`) |
| Is it stored as-is, re-encoded or sanitized? | Download it back and diff the bytes |
| Where is it served from? | Same origin, a CDN, an object-store bucket, a separate user-content domain |
| What headers does it get? | `Content-Type`, `Content-Disposition`, `X-Content-Type-Options`, `Content-Security-Policy` |
| How is it embedded? | `<img>` (no script), `<object>`/`<embed>`/`<iframe>` (script), direct link (script) |
| Is anything generated from it? | Thumbnails, PDFs, emails, OCR, AV scanning: each is a separate parser |

## 3. Choose payloads by behaviour

- Served raw to browsers: `xss/`.
- Parsed or converted on the server: `xxe/`, `ssrf/`, `renderers/`.
- Content or metadata reflected in server-generated text: `ssti/`.

Run `tools/build.py` first so every payload reports to your callback host, then upload one file at a time and note which one triggers.

## 4. Confirm and scope impact

- XSS: which origin runs it, who can reach it, does it need interaction.
- XXE and SSRF: what proof did you get (hostname, instance-id, callback), what can the server reach.
- SSTI: engine and the minimal proof from `ssti/README.md`.

## 5. Report

- Exact file and request that triggered it, with the response or callback log.
- Screenshots for rendered output. Browser and version for XSS.
- State what you did not do (no data collection, no credential use).
- Keep PoCs benign. `alert(document.domain)`, a callback ping or a hostname is enough.

## Rules of engagement

- Only test targets and features the program explicitly includes.
- Do not run denial-of-service tests. This repo contains none on purpose.
- Do not access other users' data or retrieve secrets (cloud credentials, tokens).
- Delete uploads you created where the program allows it.
