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
7. Prefer paragraphs over a wall of cards. Use tables only for exact comparisons and for a definitions block under constraint 15, and callouts only for genuinely important points. The `## Language` section below governs the prose itself.
8. Run **Part A of the self-check** — violations. This step is NOT optional. Run both parts against the prose **as it stands in the written file**, never against a draft held in your context. A check run before injection measures text you then edit, so its result does not describe what you ship.
   1. **Pointers — run this BEFORE the length count.** Search for `\b[0-9]+[a-z]\b` (catches `5a`, `4c`), for `\b[A-Z][0-9]+\b` (catches `T77`), for `\b[a-z]+[0-9]+[a-z][a-z0-9]*\b` (catches a lowercase internal code such as `o6f3`), and for `Section`, `Rule`, `Step`, `Table`, `Figure`, and `Appendix` followed by a number. Gloss each hit on first use, under constraint 14. These patterns over-match by design: a surfaced pointer that needs no gloss costs you one judgment call, and a missed pointer costs the reader the sentence. A gloss ADDS words, so a length count taken before the gloss measures text that no longer exists.
   2. **Symbols — also BEFORE the length count.** Search for `<code>[^<]{1,6}</code>` (catches `b`, `beta`, `b0`), for `<mi>` (catches a MathML variable), for `\b[A-Za-z][A-Za-z0-9_]{0,3}\([^()]{1,12}\)` (catches a function form such as L(r)), and for Greek letters, written as characters or as names such as `alpha`, `beta`, `tau`, and `lambda`. Read every table header, axis title, chart legend, and diagram label for symbols too. Define each hit on first use, under constraint 15. A hit counts as defined when an adjacent definitions block in the same section defines it. These patterns over-match by design, for the same reason as step 1. A definition adds words too.
   3. Count the words in the three longest sentences, under the Rule 8.6 count in constraint 2. Split any sentence that exceeds the cap for its classification.
   4. Search the draft for `'ll`, `'re`, `'ve`, `n't`, `it's`, `has been`, `have been`, `had been`, `should`, `would`, `may`, `might`, `could`, `is being`, `, making`, `, allowing`, `, enabling`, `, ensuring`, `;`, `e.g.`, `i.e.`, and `etc.`. Every hit outside the Untouchables is a violation. Fix each one. This list is complete as written: the em dash and the colon are NOT on it.
   5. Search for every `if` and `when`. Move each one that trails its command to the start of its sentence and add a comma.
   6. Search for the members of the check / verify / confirm / validate set that you did NOT choose, and for `config` / `settings` when you did not fix that pair. Replace every hit with the chosen term.
   7. **File links.** Search the prose for every file name and path, including a file that a sentence quotes from or cites, such as a docstring or a task list. Make each one a `file://` link, per `## Sources and file links`. `--validate` fails a `--from-file` source without a link and warns on an unlinked absolute path in inline code. It cannot see a file named in plain words, so this step is the only check for that case.
9. Run **Part B of the self-check** — texture. This step is NOT optional either. Every step in Part A searches for material to delete, so Part A cannot fail a document for being lifeless. Part B can. Run it AFTER Part A, because Part A splits and deletes and would undo this work.
   1. **Distribution.** Count the Rule 8.6 length of every sentence and inspect the spread. Two failures, and the repair differs. If the lengths cluster in a band narrower than about 6 words, or fewer than about one sentence in five lands at 18 to 25 words, combine related short claims into one sentence that carries a joint — a subordinate clause, an em-dash aside, or a colon. If MORE than about one sentence in three lands at 18 to 25 words, or fewer than about one in six runs to 8 words or less, split the flabbiest long sentences and let a short one carry the verdict. Both states fail narrative obligation 2. NEVER pad a sentence with filler.
   2. **Devices.** Confirm that the deck and the conclusion assert the thesis, that a chart or a few worked examples from the subject's own data show each mechanism the document explains, and that your own voice is present where you are the agent. Then test every analogy in the file: if a chart or a few examples drawn from the data can do its job, the analogy fails obligation 3, so replace it with them. Never add an analogy to pass this step. Each missing device fails its own obligation: a missing thesis fails narrative obligation 1, a mechanism that the document never shows fails obligation 3, and a missing voice where you are the agent fails obligation 4.
   3. **Re-run after any repair.** A repair under step 1 changes the distribution it was measured against, and a split under Part A creates the clustering step 1 looks for. After your last edit to the file, measure the spread once more. Both checks describe the file only when nothing changed after them.
10. Run validation: `python3 <skill-directory>/scripts/new_explainer.py --validate "<absolute-output-path>"`
11. Return the absolute output path as a clickable file link when the host supports it.

## Language

The prose obeys the mechanical rules of ASD-STE100 Simplified Technical English, adapted for expository writing. These are authoring obligations on you, and the `## Narrative` obligations below carry equal force. `--validate` does NOT check either set, so the self-check in steps 8 and 9 is the only enforcement before a human reads the result.

See also `references/simple-english.md` — it is the authority for the full 53-rule catalog, the modal ladder, the part-of-speech rulings, and the substitution tables. Read it to adjudicate a specific case. Cite rule numbers only from that file.

1. **Classification.** Classify each passage as procedural (tells the reader what to do) or descriptive (explains what a thing is or does). Every other rule depends on this. Do not mix the two in one passage.
2. **Sentence caps.** Procedural: maximum 20 words per sentence. Descriptive: maximum 25 words. Notes and captions take the descriptive limit. Per Rule 8.6, each of the following counts as ONE word: a backticked command or identifier, a number, a number with units, an abbreviation, quoted text, a title, a label, a proper noun, a hyphenated word, a product name with a version number (`Claude Opus 4.8` is one word, not three), and the whole of any parenthesised aside. On prose dense with figures, Rule 8.6 buys so much headroom that the cap stops binding — watch the six-sentence paragraph limit in constraint 3 instead. **These caps are ceilings, never targets.** Obligation 2 of `## Narrative` governs the spread below them, and it can fail a document in which every sentence passes this cap.
3. **Paragraphs.** One topic per paragraph, maximum six sentences.
4. **Verbs.** Use only the infinitive, the imperative, the simple present, the simple past, the simple future, and the past participle as an adjective. No present perfect ("has been updated" → "we updated"). No `-ing` form as a verb. `-ing` is permitted only inside a technical noun ("logging", "the mounting bracket").
5. **Voice.** Active. Passive is permitted only in descriptive text, and only when the agent of the action is genuinely unknown. Active voice requires a named agent, and where that agent is you, the word is "I".
6. **Modals.** Permitted: `can`, `will`, `must`. Banned: `should`, `would`, `may`, `might`, `could`. A requirement becomes `must`. A possibility becomes `can`. A recommendation is stated as a fact or deleted. A hypothetical is restructured as "If X occurs, Y occurs."
7. **Condition before command.** Every `if` or `when` stands at the START of its sentence, separated by a comma. "Increase the timeout if the network is slow" → "If the network is slow, increase the timeout."
8. **One word, one meaning.** Fix the vocabulary BEFORE drafting. Pick one verb for the check / verify / confirm / validate concept and one noun for the config / settings concept. Then use no other word for that concept anywhere in the document.
9. **Completeness.** Keep articles. Keep the conjunction "that". No contractions. STE is short sentences with complete grammar, never telegraph style.
10. **Punctuation.** The semicolon is the ONLY banned mark — write two sentences instead. Per Rule 8.1 every other standard mark is legal, and two of them do work no other mark does: the em dash carries an aside inside a sentence that would otherwise need two, and the colon introduces an enumeration or a payoff (Rule 8.4 rules on the lead-in colon's word count, which presupposes you can write one). The self-check's literal `;` sweep stops at the semicolon and does NOT extend to the em dash or the colon. Replace `e.g.` with "for example" and `i.e.` with "that is". Delete `etc.` by naming the items or by writing "and more".
11. **Filler.** Delete words that carry no fact: `simply`, `just`, `easily`, `seamlessly`, `effortlessly`, `robust`, `powerful`, `comprehensive`, `performant`, `it is worth noting that`, `it is important to`. Replace `leverage` / `utilize` with `use`, `in order to` with `to`, `prior to` with `before`, `in the event that` with `if`, and `due to the fact that` with `because`.
12. **Safety pattern.** In a warning, the command or the condition comes FIRST and the risk comes second. Use a word that shows the risk level: `WARNING` for injury, `CAUTION` for damage or data loss.
13. **Untouchables.** Never rewrite code blocks, inline code, identifiers, CLI commands, flags, file paths, quoted error messages, log lines, product names, API endpoint names, or config keys.
14. **Pointers.** Gloss every pointer on FIRST use: name in plain words what it points at, in the same sentence. A pointer is a reference whose referent the reader cannot recover from the reference itself — a section or step number, a table or figure number, a rule number, a ticket identifier, an internal code. A self-describing name is NOT a pointer and needs no gloss (`Postgres 16`, `--validate`, `assets/template.html`). **The deletion test decides the case.** Delete every pointer from the sentence. If the sentence still states its claim, the pointers annotate a stated fact and no gloss is owed. If the sentence collapses, the pointers ARE the claim and each one must name its referent. Re-gloss a pointer on its first use after an intervening `h2`, because a reader who arrives at that section from a table of contents or a search never read the first gloss. Three interactions are settled here, because each one is a plausible reason to drop a gloss. **Against constraint 11:** a gloss states a fact, so the filler sweep does not delete it. **Against constraint 13:** the pointer's own text stays exact — the gloss goes beside it and never replaces it. **Against constraint 2:** where a gloss pushes a sentence past its cap, SPLIT the sentence and keep the gloss. Worked case, and note that every other constraint passes the "before" — no banned modal, no semicolon, no contraction, no trailing condition, and 15 Rule 8.6 words against a 25-word cap:
    - **Before:** In Section 5a we look to implement o6f3 but must keep in mind 4c, 4d in order to fully realize the goal (T77).
    - **After:** Section 5a, on the ingest rewrite, implements the `o6f3` batching path. That path depends on two earlier decisions: 4c, which fixes the retry budget, and 4d, which fixes the dead-letter queue. Ticket T77 tracks the work.
    - The "after" invents its glosses, and that is the finding. The "before" withheld facts the writer already held.
15. **Symbols.** Define every variable and symbol on FIRST use — inline no later than the next sentence, or in a definitions block next to the passage: say what quantity it stands for, give its unit if it has one, and say how it is computed if it is derived. A symbol is a name that stands for a quantity — a code variable such as `b` or `beta`, a math variable, a suffixed name such as `b0`, a function form such as L(r), or a Greek letter. Each argument of a function form is a symbol too, so L(r) owes a definition of L and of r. A definitions block is a `<table>` with `Symbol`, `Meaning`, and `Unit` columns, or a `<ul>` whose items each open with the symbol. Place it in the same `h2` section, immediately before or immediately after the paragraph, figure, or table that first uses the symbol, with no other block between them. Each entry carries the same facts as an inline definition and takes the descriptive 25-word limit. Use a block where a passage introduces several symbols at once — inline definition stays the default. A symbol that first appears in a diagram, a chart, a table header, or a `<math>` block owes its definition in the prose before that figure, in a definitions block immediately before it, or in its caption. A block after the figure does not count, because the reader meets the figure first. A standard unit (`psi`) or a universal constant (π) is not a symbol under this rule. No deletion test applies: a reader cannot evaluate an expression whose terms are undefined, so every symbol owes its definition. Re-define a symbol on its first use after an intervening `h2`, for the same reason as a pointer under constraint 14. A definitions block in one section does not cover a later one. The interactions with constraints 2, 11, and 13 are the same as for a pointer gloss: split the sentence and keep the definition, the definition states a fact and is not filler, and the symbol's own text stays exact. Worked case, from an explainer that defined p two sentences after its first use and never defined L:
    - **Before:** The first is the measured start, L(row) − L(p), or NaN on a row that has no shut-in ahead of it.
    - **After:** The first is the measured start, L(row) − L(p), or NaN on a row that has no shut-in ahead of it. Here L is the line pressure in psi, and p is the last closed row before the valve opens.

## Narrative

An explainer is expository prose with a thesis, not a maintenance manual. These eight obligations carry the same force as the 15 constraints above, and they are stated as obligations because a permission does not fire. **A document that fails one of these is not finished, exactly as a document carrying an over-cap sentence is not finished.** Applied without them, the standard produces a telegram.

1. **Assert the thesis.** State a claim in the deck and in the concluding passage, and stand behind it ("Batching at the edge is the wrong layer to optimise"). Banned modals and hedging language stay banned. Asserting is not hedging, and neutral description does not substitute for a claim.
2. **Vary sentence length across the full range below the cap.** The caps are ceilings, never targets. A document whose sentences cluster in a narrow band has failed this obligation even when every sentence passes the cap. Measured against the 43 documents written before this standard: about one sentence in four ran 18 to 25 Rule 8.6 words, one in four ran 8 words or fewer, and the spread was no tighter than 6 words. **The target is two-sided.** Below about one sentence in five at 18 to 25 words, the long sentence that builds an argument is missing. Above about one in three, the short sentence that lands the point is missing, and a document of uniformly long sentences is as monotonous as a document of uniformly short ones. Treat every figure as a diagnostic, never as a quota — padding a sentence to reach a length violates constraint 11 and produces worse prose than the clustering did. Combine related short claims instead, and keep the short ones that carry a verdict.
3. **Show the mechanism with the subject's own evidence first.** Where the subject has a mechanism and the data is in hand, show the mechanism with a chart or with a few worked examples drawn from that data. Use an analogy only where no data shows the mechanism — a design that does not exist yet, or a state that no record captures — and map each part of the analogy back to the subject in the same passage. An analogy that a chart or an example from the data can replace fails this obligation, because the reader must translate the analogy back and the data needs no translation. A subject with no mechanism owes none of these. Never invent an analogy to discharge this obligation. An analogy that does not match the mechanism misleads the reader. The constraint 11 filler deletion does not license removal of the chart, the worked examples, or the analogy that makes a mechanism legible.
4. **Write in your own voice where you are the agent.** First-person reference is legal, and constraint 5 often requires it, because active voice needs a named agent. An explainer that revises your earlier position states "My earlier figure was wrong" and never retreats into "the figure was incorrect".
5. **Let each paragraph carry a developed thought.** Hold to one topic and six sentences, per constraint 3. A thought split across two paragraphs to stay under the sentence cap is fragmented, not clarified. Restoring sentence variety under obligation 2 is what lets six sentences carry a full passage.
6. **Reproduce quoted source material exactly.** Never rewrite text inside `<blockquote>`, `<code>`, `<pre>`, `<math>`, or any Vega-Lite JSON spec for compliance. Reproduce a quotation from a `--from-file` source exactly, including its own violations.
7. **Write figure captions to the descriptive limit** (25 words), and never in the imperative.
8. **Leave marketing register out.** The standard deletes persuasion by design and this skill does not restore it. An explainer explains. It does not sell.

## Sources and file links

`--from-file <abs-path>` (repeatable) records source lineage. The script does NOT read the file. It writes one `<!-- SOURCE: <abs-path> -->` HTML comment inside `<article>`, immediately before `<!-- EXPLAINER_CONTENT -->`, and a visible `Sources` section after the marker that lists each file as a `file://` link. Keep that section. `--validate` fails a document in which a source has no link. You must read each source and weave its content into the prose. This preserves the split: the script mints structure and the agent writes content.

Link every other file that the prose names, too — a file you quote, cite, or point the reader at. Write `<a href="file:///abs/path">`, with the path or the file name as the visible text, and percent-encode a space as `%20`. Resolve a relative path to its absolute path before you link it. The link wraps the path and never rewrites it, per constraint 13. A path inside a code block is quoted material and takes no link. A file that the reader cannot open from this machine, such as a path on a remote device, takes no link, and the prose says where the file lives.
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
