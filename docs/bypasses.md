# Bypasses

Ideas for when a straight upload is rejected or sanitized. Apply one change at a time so you know what mattered.

## File name and extension

```
payload.svg    payload.SVG    payload.sVg    payload.svgz (gzip)
payload.svg.png    payload.png.svg    payload.svg%00.png
payload.svg;.png   payload.svg.    payload.svg%20    payload.svg::$DATA
payload.xml    payload.xhtml    payload.html
```

If `.xml`, `.xhtml` or `.html` are accepted, the same XSS applies.

## Content-Type and multipart tricks

- Send `image/svg+xml`, `image/png`, `application/octet-stream`, `text/xml`, `text/plain` and compare. Some servers store by declared type and serve by extension, or the reverse.
- Mismatch the extension and the declared type in both directions.
- Duplicate or alternate parameters: two `filename=` values, `filename*=UTF-8''a.svg`.
- Some stores let you rename or re-type an object after upload. Check any "rename" or "update" API.

## Content validators

- SVG has no magic bytes. Validators typically look for `<svg` or a valid XML parse. Try a BOM (`EF BB BF`), leading whitespace, comments before the root, an XML prolog, a DOCTYPE.
- Padding. If only the first N bytes are scanned, put a large comment first (`<!-- AAAA... -->`, 8 to 64 KB) and the payload after it.
- Encoding. Convert to UTF-16 to evade string filters such as `<script` and `onload`:

  ```
  iconv -f UTF-8 -t UTF-16 payload.svg -o payload-utf16.svg
  ```

  Keep `encoding="UTF-16"` in the XML declaration. UTF-7 and other encodings are parser dependent.
- Gzip the file and upload as `.svgz`.
- Dimension checks: add `width`, `height` and `viewBox`.

## Sanitizers and WAFs

- Discover the allow-list first with `xss/20-handler-sweep.svg`.
- Element allow-lists: try `a`, `animate`, `set`, `use`, `image`, `foreignObject`, `style`, and XHTML-namespace `script` (`xss/11`).
- Namespace tricks: prefixed elements (`xss/12`, `xss/13`).
- Encoding tricks: character references (`xss/14`, `xss/15`), DOCTYPE entities (`xss/16`).
- `javascript:` obfuscation: numeric refs, tab or newline inside the scheme, leading whitespace or control characters.
- Case: XML is case-sensitive (handlers must be lowercase), but HTML-context parsers are not. Test both.
- `href` and `xlink:href` are separate attributes. Filters sometimes handle only one.
- CSP: read the policy on the served file. If inline script is blocked, look at what `script-src` allows (`xss/17` loads from a host you control, useful only if allowed).

## If the SVG is re-encoded

Server-side conversion to PNG or PDF removes browser XSS, but the conversion step is a separate parser. Use `xxe/`, `ssrf/` and `renderers/`. Also check whether the original upload is stored and served as well.

## Delivery context

- Same-origin direct link vs a CDN or bucket: affects impact, not whether it fires.
- Query parameters on storage URLs (such as response-header overrides on presigned URLs) can change `Content-Type` or `Content-Disposition`. Only relevant when the program lets you generate such URLs.
