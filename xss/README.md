# XSS via SVG

Every payload proves execution with `alert(document.domain)` or an out-of-band ping that reports the origin only. None of them read cookies or storage.

`COLLAB_HOST` is replaced by `tools/build.py` (see top-level README).

| File | Trigger | Notes |
|---|---|---|
| `01-onload.svg` | opens directly | Baseline: root `onload` |
| `02-script-tag.svg` | opens directly | Full prolog and DOCTYPE, plain `<script>` |
| `03-script-cdata.svg` | opens directly | CDATA-wrapped script |
| `04-a-href-javascript.svg` | click | `xlink:href="javascript:"` |
| `05-a-href-svg2.svg` | click | SVG2 `href` without `xlink`; catches filters that only strip `xlink:href` |
| `06-animate-onbegin.svg` | auto | SMIL event handler, no click needed |
| `07-animate-href-click.svg` | click | SMIL animates `href` to a `javascript:` URL; often blocked by modern browsers, still useful against blocklists |
| `08-foreignobject-img-onerror.svg` | auto | HTML inside `foreignObject` |
| `09-foreignobject-iframe-srcdoc.svg` | auto | `srcdoc` iframe inherits the origin |
| `10-image-onerror.svg` | auto | Browser dependent |
| `11-xhtml-script.svg` | auto | XHTML-namespace `<script>`; bypasses filters keyed on the SVG `script` element |
| `12-prefixed-root-onload.svg` | auto | Namespace-prefixed root element |
| `13-prefixed-script-element.svg` | auto | Namespace-prefixed `script` |
| `14-charref-onload.svg` | auto | Character references inside the handler |
| `15-charref-javascript-url.svg` | click | Obfuscated `javascript:` schemes (numeric refs, tab, leading newline) |
| `16-internal-entity.svg` | auto | Handler comes from a DOCTYPE entity |
| `17-external-script.svg` | auto | Loads JS from your host; CSP allow-list testing, blind XSS |
| `18-oob-proof.svg` | auto | Pings your host with origin, URL and referrer |
| `19-blind-loader.svg` | auto | Injects a remote script; for blind XSS in admin or moderation panels |
| `20-handler-sweep.svg` | mixed | Many handlers, each pinging a unique path; shows which ones a filter lets through |

## Where an SVG executes script

- Navigated to directly (own tab, link): runs, in the origin that serves the file.
- Embedded with `<object>`, `<embed>`, `<iframe>`: runs.
- Embedded with `<img>`, CSS `background-image`, `<picture>`: does **not** run scripts.
- Served with `Content-Disposition: attachment`, a non-SVG `Content-Type` plus `nosniff`, or a `sandbox` CSP: normally does not run or runs in an opaque origin.

Inline use (SVG text pasted into the DOM via `innerHTML`) is a different problem. Test classic HTML-context vectors there.

## Impact

- Stored on the application's own origin and reachable by other users: usually the interesting case.
- Served from a separate cookieless or sandbox domain: normally low impact. Check whether that origin can reach anything sensitive.
- Only fires for the uploader (self-XSS): usually out of scope.

Behaviour changes between browser versions. Re-test in current Chrome and Firefox before reporting.
