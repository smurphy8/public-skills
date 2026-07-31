# Vendored offline JS assets

These files are **checked-in, vendored offline assets** for the `explainer` skill.
They **MUST NOT** be regenerated at build time and **MUST NOT** be fetched at runtime — the explainer script reads them off disk and inlines their contents into every generated document so that each explainer is a self-contained, offline, no-CDN artifact.

## Manifest

| File | Pinned version | Shorthand URL (used to download) | Resolved (version-locked) URL | SHA-256 | Bytes |
|---|---|---|---|---|---|
| `mermaid.min.js` | `10.9.6` | `https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js` | `https://cdn.jsdelivr.net/npm/mermaid@10.9.6/dist/mermaid.min.js` | `eda3a0ad572bbe69a318c1be0163e8233dd824f3f12939e5168feba207767151` | 3 337 508 |
| `vega.min.js` | `5.33.1` | `https://cdn.jsdelivr.net/npm/vega@5/build/vega.min.js` | `https://cdn.jsdelivr.net/npm/vega@5.33.1/build/vega.min.js` | `463f3db6a40b20e9747b4ed38f37ed0add508838f9141b1cf8366784b07b30c8` | 515 242 |
| `vega-lite.min.js` | `5.23.0` | `https://cdn.jsdelivr.net/npm/vega-lite@5/build/vega-lite.min.js` | `https://cdn.jsdelivr.net/npm/vega-lite@5.23.0/build/vega-lite.min.js` | `58c27358e26f2d319cf62f45bc17a4c8362f08645001df2ec8d341eee4097c7f` | 252 198 |
| `vega-embed.min.js` | `6.29.0` | `https://cdn.jsdelivr.net/npm/vega-embed@6/build/vega-embed.min.js` | `https://cdn.jsdelivr.net/npm/vega-embed@6.29.0/build/vega-embed.min.js` | `12d02acfbe3ec59ef9a37dd4822a2e04e2961b5bbb671bbe661d2221715b99da` | 60 630 |

Resolved versions were confirmed via two independent signals:

1. `https://data.jsdelivr.com/v1/packages/npm/<pkg>/resolved?specifier=<major>` returns `{"version": "<resolved>"}`.
2. The `x-jsd-version` response header on the shorthand URL echoes the same value.

## Vega trio: concatenation order for inlining

When the explainer script inlines the Vega bundle into a document, the three files **must** be concatenated in dependency order into a single `<script data-inline="vega-lite">` block:

```
vega.min.js         ← the core Vega runtime; must load first
vega-lite.min.js    ← the Vega-Lite → Vega compiler; depends on Vega
vega-embed.min.js   ← convenience wrapper (vegaEmbed); depends on both
```

Reversing or interleaving the order breaks the browser-side `require`-style guards in the UMD headers of vega-lite.min.js and vega-embed.min.js (both reference `require("vega")` / `require("vega-lite")` on their `object`/`module` branch and fall back to reading `globalThis.vega` / `globalThis.vegaLite` at load time).

Mermaid is independent of the Vega trio and is inlined separately into its own `<script data-inline="mermaid">` block.

## Upgrading

To refresh to a newer patch/minor within the pinned major range (or to move to a new major):

1. Re-run the same curl commands from this repo root — the shorthand URLs above already track the majors:

   ```
   cd agents/skills/explainer/assets
   curl -sSL --fail -o mermaid.min.js    https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js
   curl -sSL --fail -o vega.min.js       https://cdn.jsdelivr.net/npm/vega@5/build/vega.min.js
   curl -sSL --fail -o vega-lite.min.js  https://cdn.jsdelivr.net/npm/vega-lite@5/build/vega-lite.min.js
   curl -sSL --fail -o vega-embed.min.js https://cdn.jsdelivr.net/npm/vega-embed@6/build/vega-embed.min.js
   ```

   For a major bump, edit the `@10` / `@5` / `@6` shorthand in the URLs (and in this README) first.

2. Re-compute hashes and byte sizes:

   ```
   shasum -a 256 mermaid.min.js vega.min.js vega-lite.min.js vega-embed.min.js
   wc -c         mermaid.min.js vega.min.js vega-lite.min.js vega-embed.min.js
   ```

3. Look up the newly resolved pinned versions (either from `curl -sI` on the shorthand URL — the `x-jsd-version` header — or from `https://data.jsdelivr.com/v1/packages/npm/<pkg>/resolved?specifier=<major>`).

4. Update this README's manifest table with the new versions, resolved URLs, hashes, and byte sizes.

5. Re-run the `explainer` skill's smoke test (mint a document that exercises a Mermaid diagram and a Vega-Lite chart, open it, and confirm both render).
