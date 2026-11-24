# XXE via SVG

SVG is XML, so any parser that loads entities will process these. `xxe/dtd/` holds the external DTDs used by files `07` and `08`.

## Which file when

- `01` to `04`: in-band file read. Works when the server returns or renders parsed text (thumbnails, previews, converted PNG/PDF, metadata fields).
- `05`, `06`: out-of-band detection. A hit on `COLLAB_HOST` proves the parser resolves external entities even when nothing is reflected. `06` helps when general entities are blocked but parameter entities are not.
- `07`: blind exfiltration through an external DTD. Host `dtd/xxe-oob.dtd` on a server you control as `http://COLLAB_HOST/xxe-oob.dtd`. It sends `/etc/hostname` in the query string.
- `08`: error-based. Host `dtd/xxe-error.dtd` the same way. The file content appears in the parser error message, if the app shows errors.
- `09`: XInclude, for when you control only part of the document and cannot add a DOCTYPE.
- `10`, `11`: SSRF through the entity.
- `12`: shows where parsed entity content tends to reappear (`title`, `desc`, `metadata`). External entities cannot be used inside attribute values; XML forbids it.

## Reading the callback

- DNS hit without HTTP: the name resolved but the fetch was blocked or egress is filtered.
- HTTP hit: check `User-Agent`. It often names the parser or runtime (`Java/x`, `python-requests`, `libxml`, `curl`).
- No hit: try the XInclude and parameter-entity variants and the encoding tricks in `docs/bypasses.md` before ruling it out.

## Etiquette

Use `interesting-files.txt` as a guide to proof-grade files. For cloud metadata, stopping at `instance-id` or a role name is enough for a report. Do not retrieve or use credentials.
