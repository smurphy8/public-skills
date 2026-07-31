---
name: explainer
description: Create a throwaway HTML explainer in a plain, flat editorial style with serif body text and simple-English prose. Use when the user explicitly asks for an explainer, an HTML explainer, or invokes the explainer command with a topic, question, source file, or set of findings.
---

# Create an explainer

Create one self-contained HTML document that explains the requested subject clearly and accurately.

## Workflow

1. Resolve the subject from the user's command or request. If the subject is absent, ask for it. Infer audience and depth from context. Do not ask when a reasonable default works.
2. Inspect supplied files. When a fact is current or uncertain, verify it. Cite sources with ordinary HTML links when the explainer depends on external sources.
3. Choose a narrative structure suited to the subject. Prefer a clear thesis, mechanism, concrete example or evidence, important caveats, and a concise conclusion. Do not force generic sections that do not help.
4. Create the temporary document by running:
   ```bash
   python3 <skill-directory>/scripts/new_explainer.py \
     --title "<document title>" --subtitle "<one-sentence deck>" \
     [--from-file <abs-path>]... [--output <dir>]
   ```
   Treat the absolute path printed by the script as the only output target.
5. Replace `<!-- EXPLAINER_CONTENT -->` in that file with semantic HTML. Preserve the existing document structure and CSS.
6. Use `section`, `h2`, `h3`, `p`, `ul`, `ol`, `blockquote`, `figure`, `figcaption`, `table`, `aside`, `code`, `pre`, `strong`, `em`, `a`, plus `<pre class="mermaid">`, `<pre class="vega-lite">`, and `<math>` (see below) as first-class primitives. Do not add other JavaScript, external stylesheets, web fonts, tracking, or unrelated UI.
7. Prefer paragraphs over a wall of cards. Use tables only for exact comparisons, and callouts only for genuinely important points. The `## Language` section below governs the prose itself.
8. Run the self-check on the drafted prose. This step is NOT optional.
   1. Count the words in the three longest sentences, under the Rule 8.6 count in constraint 2. Split any sentence that exceeds the cap for its classification.
   2. Search the draft for `'ll`, `'re`, `'ve`, `n't`, `it's`, `has been`, `have been`, `had been`, `should`, `would`, `may`, `might`, `could`, `is being`, `, making`, `, allowing`, `, enabling`, `, ensuring`, `;`, `e.g.`, `i.e.`, and `etc.`. Every hit outside the Untouchables is a violation. Fix each one.
   3. Search for every `if` and `when`. Move each one that trails its command to the start of its sentence and add a comma.
   4. Search for the members of the check / verify / confirm / validate set that you did NOT choose, and for `config` / `settings` when you did not fix that pair. Replace every hit with the chosen term.
9. Run validation: `python3 <skill-directory>/scripts/new_explainer.py --validate "<absolute-output-path>"`
10. Return the absolute output path as a clickable file link when the host supports it.

## Language

The prose obeys the mechanical rules of ASD-STE100 Simplified Technical English, adapted for expository writing. These are authoring obligations on you. `--validate` does NOT check them, so the self-check in step 8 is the only enforcement before a human reads the result.

See also `references/simple-english.md` — it is the authority for the full 53-rule catalog, the modal ladder, the part-of-speech rulings, and the substitution tables. Read it to adjudicate a specific case. Cite rule numbers only from that file.

1. **Classification.** Classify each passage as procedural (tells the reader what to do) or descriptive (explains what a thing is or does). Every other rule depends on this. Do not mix the two in one passage.
2. **Sentence caps.** Procedural: maximum 20 words per sentence. Descriptive: maximum 25 words. Notes and captions take the descriptive limit. Per Rule 8.6, each of the following counts as ONE word: a backticked command or identifier, a number, a number with units, an abbreviation, quoted text, a title, a label, a proper noun, a hyphenated word, a product name with a version number (`Claude Opus 4.8` is one word, not three), and the whole of any parenthesised aside. On prose dense with figures, Rule 8.6 buys so much headroom that the cap stops binding — watch the six-sentence paragraph limit in constraint 3 instead.
3. **Paragraphs.** One topic per paragraph, maximum six sentences.
4. **Verbs.** Use only the infinitive, the imperative, the simple present, the simple past, the simple future, and the past participle as an adjective. No present perfect ("has been updated" → "we updated"). No `-ing` form as a verb. `-ing` is permitted only inside a technical noun ("logging", "the mounting bracket").
5. **Voice.** Active. Passive is permitted only in descriptive text, and only when the agent of the action is genuinely unknown.
6. **Modals.** Permitted: `can`, `will`, `must`. Banned: `should`, `would`, `may`, `might`, `could`. A requirement becomes `must`. A possibility becomes `can`. A recommendation is stated as a fact or deleted. A hypothetical is restructured as "If X occurs, Y occurs."
7. **Condition before command.** Every `if` or `when` stands at the START of its sentence, separated by a comma. "Increase the timeout if the network is slow" → "If the network is slow, increase the timeout."
8. **One word, one meaning.** Fix the vocabulary BEFORE drafting. Pick one verb for the check / verify / confirm / validate concept and one noun for the config / settings concept. Then use no other word for that concept anywhere in the document.
9. **Completeness.** Keep articles. Keep the conjunction "that". No contractions. STE is short sentences with complete grammar, never telegraph style.
10. **Punctuation.** No semicolons — write two sentences. Replace `e.g.` with "for example" and `i.e.` with "that is". Delete `etc.` by naming the items or by writing "and more".
11. **Filler.** Delete words that carry no fact: `simply`, `just`, `easily`, `seamlessly`, `effortlessly`, `robust`, `powerful`, `comprehensive`, `performant`, `it is worth noting that`, `it is important to`. Replace `leverage` / `utilize` with `use`, `in order to` with `to`, `prior to` with `before`, `in the event that` with `if`, and `due to the fact that` with `because`.
12. **Safety pattern.** In a warning, the command or the condition comes FIRST and the risk comes second. Use a word that shows the risk level: `WARNING` for injury, `CAUTION` for damage or data loss.
13. **Untouchables.** Never rewrite code blocks, inline code, identifiers, CLI commands, flags, file paths, quoted error messages, log lines, product names, API endpoint names, or config keys.

### Carve-outs for an explainer

An explainer is expository prose with a thesis, not a maintenance manual. These six departures carry the same weight as the 13 constraints above. Without them you over-apply the standard and produce a telegram.

1. **A thesis is permitted.** The deck and the concluding passage can assert a claim. A claim is a fact you stand behind ("Batching at the edge is the wrong layer to optimise"), not a hedge. Banned modals and hedging language stay banned. Asserting is not hedging.
2. **Sentence variety is permitted under the caps.** The caps are ceilings, not targets. A document whose sentences all run to the same short length violates the spirit of Rule 4.2, which exists to forbid telegraph style. Vary length freely below the limit.
3. **Analogies and concrete examples are kept.** A resemblance is a fact about the subject, not decoration. The Rule 9.x filler deletion does not license removal of the worked example or of the analogy that makes a mechanism legible.
4. **Untouchables extend to quoted source material.** Never rewrite text inside `<blockquote>`, `<code>`, `<pre>`, `<math>`, or any Vega-Lite JSON spec for compliance. Reproduce a quotation from a `--from-file` source exactly, including its own violations.
5. **Figure captions take the descriptive limit** (25 words) and are never imperative.
6. **Marketing register stays out of scope.** The standard deletes persuasion by design and this skill does not restore it. An explainer explains. It does not sell.

## Sources

`--from-file <abs-path>` (repeatable) records source lineage. The script does NOT read the file. It writes one `<!-- SOURCE: <abs-path> -->` HTML comment inside `<article>`, immediately before `<!-- EXPLAINER_CONTENT -->`. You must read each source and weave its content into the prose. This preserves the split: the script mints structure and the agent writes content.
```bash
python3 …/new_explainer.py --title "Incident" --subtitle "…" --from-file /tmp/postmortem.md --from-file /tmp/timeline.txt
```

## Persistence

The default is `$TMPDIR/explainers/`, which is throwaway. `--output <dir>` opts out of the default. The script drops an empty `.explainer-root` sentinel in that dir, so a later `--validate <path>` run auto-detects residency without the flag. Do not gitignore the target dir unless you intend explainers to stay ephemeral even when persisted.
```bash
python3 …/new_explainer.py --title "Q3 Review" --subtitle "Draft" --output ~/docs/reviews
```

## Diagrams

Author with `<pre class="mermaid">` inside `<article>`. The script inlines Mermaid offline. Every block renders to inline SVG at load.
```html
<figure><pre class="mermaid">graph TD; A[Ingest] --> B[Normalize] --> C[Emit]</pre><figcaption>Pipeline stages.</figcaption></figure>
```

## Charts

Charts inherit the document's flat editorial style: muted fills, one hue per series, no gradients, no drop shadows, no chart junk. Set colors explicitly in a `config.range` override rather than relying on the Vega-Lite default palette, which is tuned for dashboards and reads loud against serif body text. Keep a categorical series count at or below six; beyond that, prefer a table. If a separate data-visualization skill is installed and defines a house palette, use its values here.

Author with `<pre class="vega-lite">` inside a `<figure>`. Author the data inline in `data.values`. There is no `--data` flag in v1. Charts render as inline `<svg>` (not `<canvas>`), so print stays sharp.
```html
<figure><pre class="vega-lite">
{"$schema": "https://vega.github.io/schema/vega-lite/v5.json",
 "data": {"values": [{"a": "A", "b": 28}, {"a": "B", "b": 55}, {"a": "C", "b": 43}]},
 "mark": "bar",
 "encoding": {"x": {"field": "a", "type": "nominal"}, "y": {"field": "b", "type": "quantitative"}}}
</pre><figcaption>A short caption.</figcaption></figure>
```

## Math

MathML is native. The document needs no library and no fonts for math. Modern Chrome/Safari/Firefox render `<math>` natively. `--validate` warns (does not fail) on a `<math>` without `xmlns`. Include it to make rendering reliable.
```html
<math xmlns="http://www.w3.org/1998/Math/MathML" display="block"><mi>x</mi><mo>=</mo><mfrac><mrow><mo>-</mo><mi>b</mi><mo>±</mo><msqrt><mrow><msup><mi>b</mi><mn>2</mn></msup><mo>-</mo><mn>4</mn><mi>a</mi><mi>c</mi></mrow></msqrt></mrow><mrow><mn>2</mn><mi>a</mi></mrow></mfrac></math>
```

## Output boundary

- Always create the explainer beneath the operating system's temporary directory, unless the user passes `--output`.
- Never place it in the current repository, beside an input file, in a persistent file library, or in version control.
- Never overwrite an earlier explainer. Each invocation creates a unique file.
- Produce a single self-contained `.html` file unless the user explicitly asks for something else.
- Baseline size is ~4MB (Mermaid + Vega/Vega-Lite/Vega-Embed inlined offline). Fine for a throwaway single-file artifact; not appropriate as a persistent web page or email attachment beyond that limit.
