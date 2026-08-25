# Changelog

All notable changes to the `explainer` skill.

This skill follows [Semantic Versioning](https://semver.org/). **The major
version is `0`, and that is a claim about the prose standard, not modesty.** The
language standard has changed four times in ways that make a document written
against an earlier version non-compliant. Until `1.0.0`, expect that to keep
happening, and read the minor-version entries below as breaking changes.

Both install paths — `scripts/install.sh` and the Nix `copy-tree` sync — replace
the skill directory rather than merging into it. Updating swaps the prose
standard wholesale, so a document you wrote last week may not satisfy the
standard you just installed. The old document is still fine; it just is not
compliant with the new rules.

## 0.4.0 — 2026-08-19

### Added

- **Language constraint 14, `Pointers`.** Gloss every pointer on first use: name
  in plain words what it points at, in the same sentence. A pointer is a
  reference whose referent a reader cannot recover from the reference itself — a
  section or step number, a table or figure number, a rule number, a ticket
  identifier, an internal code. A self-describing name such as `Postgres 16` or
  `--validate` is not a pointer and needs no gloss.
- **The deletion test**, which decides whether a gloss is owed. Delete every
  pointer from the sentence. If the sentence still states its claim, the pointers
  annotate a stated fact and no gloss is owed. If the sentence collapses, the
  pointers *are* the claim and each one must name its referent.
- **A re-gloss rule.** A gloss is owed again on the first use after an
  intervening `h2`, because a reader arriving from a table of contents or a
  search never read the first one.
- **A pointer sweep as the first step of self-check Part A**, shipping literal
  search patterns. It runs first because a gloss adds words, so a length count
  taken before glossing measures text that no longer exists.
- **A `Pointers and indexes` section in `references/simple-english.md`**, marked
  as this project's ruling rather than an ASD-STE100 one. The standard legislates
  referents only for pronouns, so the extension is stated as an extension.

### Why

A sentence could pass all thirteen constraints, both self-check parts, and
`--validate` while telling the reader nothing, because no rule asked whether a
reader could resolve a reference. Applying the existing filler rule to such a
sentence leaves it shorter, cleaner, and still unreadable — which is the
argument that the new constraint is not redundant with the old one.

The three interactions that would otherwise justify dropping a gloss are settled
inside the constraint: the filler sweep does not delete a gloss because a gloss
states a fact, the pointer's own text stays exact under the Untouchables rule,
and a gloss that breaches the sentence cap splits the sentence instead.

## 0.3.0 — 2026-08-03

### Added

- **Eight narrative obligations**, stated at equal force with the language
  constraints: assert the thesis, vary sentence length across the full range
  below the cap, keep the analogy and the worked example, write in your own voice
  where you are the agent, let each paragraph carry a developed thought,
  reproduce quoted material exactly, write captions to the descriptive limit, and
  leave marketing register out.
- **Part B of the self-check — texture.** Every step of the existing self-check
  searched for material to delete, so nothing could fail a document for being
  lifeless. Part B can. It measures the sentence-length distribution against a
  two-sided target and confirms that the thesis, the analogy, and the author's
  voice are present.

### Changed

- **The carve-outs became obligations.** They previously appeared in the
  permissive mood ("sentence variety is permitted"), which is the whole defect: an
  obligation must be discharged, while a permission can be declined at no cost.
  Two mandatory inputs pushed toward deletion and one optional input pushed back.
- **The em dash and the colon were explicitly restored.** The standard bans the
  semicolon and nothing else, but the `;` sweep had been generalized to every
  mark that joins clauses. The self-check now says so in as many words.
- **Sentence caps are labelled ceilings, never targets**, at the point where the
  cap is given.

### Why

The prose standard from 0.2.0 did what it was built to do and also flattened the
storytelling. Measured, not supposed: across 93 documents and 108,814 words by
one author on one subject in one week, banned modals fell 96% and over-cap
sentences fell from 15.1% to 1.1% — and em dashes fell 88%, colons 57%, first
person 37%, and the 18-to-25-word sentence band from 24.1% to 19.2%. The wins
are kept. The losses are what this version repairs.

## 0.2.1 — 2026-08-03

### Fixed

- **Vega-Lite charts rendered blank.** Two defects, both in the chart init path.
  The source `<pre>` was never hidden, so the reader saw the raw JSON spec styled
  as a dark code block with the real chart below it. And `"width": "container"`
  collapsed to zero, because Vega-Lite resolves container sizing against the
  parent's computed width, which measures 0 for a freshly created div.
- The source block is now hidden only after `vegaEmbed` resolves, so a spec that
  fails to compile stays visible as a diagnostic instead of leaving a blank gap.
- **An unhandled promise rejection on a Vega compile failure.** The surrounding
  `try`/`catch` only caught synchronous `JSON.parse` throws.

Mermaid rendering and fixed-pixel charts are unaffected.

## 0.2.0 — 2026-07-31

### Added

- **A prose standard based on ASD-STE100 Simplified Technical English**, adapted
  for expository writing. Thirteen always-in-context constraints in `SKILL.md`:
  procedural and descriptive classification, sentence caps, one topic per
  paragraph, simple tenses only, active voice, a three-modal set
  (`can` / `will` / `must`), condition before command, one word per meaning, no
  contractions, no semicolons, a filler denylist, a safety pattern, and a list of
  untouchable strings.
- **`references/simple-english.md`**, carrying the full 53-rule catalog across 9
  sections, the modal ladder, the part-of-speech rulings, and the substitution
  tables. Adapted from a third-party MIT-licensed summary. ASD's copyrighted
  approved-word and banned-word lists are deliberately not reproduced — rule
  mechanics only.
- **Six explainer carve-outs from the standard**, and a mandatory self-check as
  workflow step 8.

### Changed

- **Styling went flat.** One off-white surface, card border and shadow removed
  outright, a smaller and heavier `h1`, a neutralized rule color, and a bare
  `hr`. The terracotta accent and the serif body text stay — the chrome was the
  decoration and the palette is the identity.
- **Measure settled at a 102-character line**, midway between the original 72 and
  a too-wide 131, by pairing a narrower container with restored padding. The page
  still fills its width while the prose column stays tight.

### Why

Applied literally, the standard flattens expository prose into a telegram,
deletes the analogies that make a mechanism legible, and hedges a thesis into
neutral description. The carve-outs are load-bearing rather than hedging, which
is why they sit beside the constraints at equal weight. Version 0.3.0 records
what happened when that intent was shipped in too weak a grammatical mood.

## 0.1.0 — 2026-07-29

### Added

- **Initial release.** One Python standard-library CLI that mints a
  self-contained, typography-first HTML document in a fixed editorial style, then
  hands it back to the invoking agent to fill with prose. The division of labour
  is the design: the script mints structure and the agent writes content.
- **Create mode** — `--title`, `--subtitle`, `--from-file` (repeatable, records
  source lineage as HTML comments without reading the files), and `--output`.
- **Validate mode** — `--validate` enforces residency, document structure, the
  required serif stack, and a four-slot inline-script allowlist.
- **Diagrams** via bundled offline Mermaid 10.9.6, authored as
  `<pre class="mermaid">`.
- **Charts** via bundled offline Vega, Vega-Lite, and Vega-Embed, authored as
  `<pre class="vega-lite">` with inline `data.values`, rendered as inline SVG so
  print stays sharp.
- **Math** via native MathML — no library and no web font. `--validate` warns,
  and does not fail, on a `<math>` element missing `xmlns`.
- **An output boundary.** Explainers are throwaway artifacts written beneath the
  operating system's temporary directory unless the caller opts out with
  `--output`. Each invocation creates a uniquely named file and never overwrites
  an earlier one.
- Claude and Codex host manifests, plus an OpenCode adapter, for host
  portability.

Every asset is inlined offline, so a document renders from `file://` with the
network down: no CDN, no web fonts, no tracking, no external stylesheet.
