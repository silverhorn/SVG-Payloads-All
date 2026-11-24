# Server-side renderers

Find out which library processes the upload first, then pick payloads that fit it. Fingerprint through:

- the `User-Agent` of any callback from `ssrf/` or `xxe/` payloads,
- error messages, response headers (`Server`, `X-Powered-By`), generated PDF metadata (`Producer`, `Creator`),
- the output format (PNG, PDF, JPEG, WebP) and how fonts and filters render.

| Renderer | Try first | Notes |
|---|---|---|
| ImageMagick | `renderers/imagemagick/`, `ssrf/01`, `ssrf/02`, `xxe/` | Behaviour depends heavily on `policy.xml`. Many distributions disable risky coders and `@` paths. Review the ImageTragick advisory (CVE-2016-3714 to CVE-2016-3718) for the history; the original public PoCs are at imagetragick.com |
| librsvg | `xxe/`, `ssrf/01` to `ssrf/04` | Restricts remote loads in recent versions. Check how `image` and `use` resolve relative and absolute paths |
| CairoSVG (Python) | `xxe/`, `ssrf/01`, `ssrf/03` | Check external entity handling and any "unsafe" mode in the integration |
| Apache Batik (Java) | `xxe/`, `ssrf/01` to `ssrf/07`, `ssrf/12` | Check whether script execution is enabled in the transcoder. Look up its security advisories for your version |
| Inkscape (CLI) | `xxe/`, `ssrf/01`, `ssrf/03` | Often invoked from a shell wrapper; test file names (see `docs/methodology.md`) |
| Headless Chrome / Puppeteer / Playwright | `ssrf/08` to `ssrf/12`, `xss/` | A full browser: scripts and HTML in `foreignObject` run. Local file access depends on flags |
| wkhtmltopdf / wkhtmltoimage / PhantomJS | `ssrf/08` to `ssrf/13` | Old WebKit engines. `ssrf/13` tests local file XHR |

## Reading results

- A callback with a renderer-specific `User-Agent` is stronger evidence than a generic one.
- A PDF or PNG that contains fetched content or file text means the response was embedded; screenshot it for the report.
- If the original SVG is also stored and served back, run the `xss/` payloads as well. Conversion and storage are separate attack surfaces.
