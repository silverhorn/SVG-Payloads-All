# SSRF via SVG

These payloads make a **server-side** renderer or converter (thumbnailer, PDF or PNG generator, import feature) fetch a URL. Browsers do not fetch most of these when the SVG is merely viewed.

`COLLAB_HOST` is replaced by `tools/build.py`. Every callback path is unique, so the path that arrives tells you which element the renderer followed.

## Files

- `01` to `04`: SVG elements that load resources (`image`, `use`, `feImage`).
- `05` to `07`: CSS and `xml-stylesheet` fetches.
- `08`, `09`: HTML inside `foreignObject`. Headless-Chrome or wkhtmltopdf-style renderers follow these.
- `10`, `11`: cloud metadata proof (AWS IMDS `instance-id`). `10` is blind, `11` renders the response into the output (PDF or screenshot).
- `12`, `13`: the renderer executes script. `12` reports back; `13` is the legacy wkhtmltopdf/PhantomJS-style local file XHR.
- `ip-bypass.txt`: encodings and parser tricks for filtered destinations.

## Reading the callback

- The `User-Agent` usually names the library: `ImageMagick`, `Java/x`, `HeadlessChrome`, `wkhtmltoimage`, `python-requests`, `libcurl`. Use it to pick the matching notes in `renderers/README.md`.
- DNS-only hit: egress is filtered or only resolution is allowed.
- Hits for `ssrf-iframe` or `ssrf-html-*`: a full browser engine renders the SVG. Try `12` and `13`.

## Etiquette

Cloud metadata services should be hit only for proof (`instance-id`, a role name). Do not fetch or use credentials. Stay inside the program's scope.
