# Simple English — full rule reference

Adapted from [AminBlg/SimpleEnglish](https://github.com/AminBlg/SimpleEnglish) (MIT, Copyright (c) 2026 AminBlg). The material here is **adapted, not copied verbatim**: rules are paraphrased, examples are rewritten for explainer prose, and an **Explainer adaptations** section records where this skill departs from the upstream skill.

The standard is **ASD-STE100 Issue 9 (2025-01-15)**, Simplified Technical English. STE is the controlled language that aerospace and defense manufacturers use for maintenance documentation. The rules exist so a tired reader who is not a native English speaker cannot misread a sentence. They remove the usual markers of model-generated prose as a side effect: long sentences, synonym rotation, hedges, filler, and decorative clauses.

`SKILL.md` carries the 14 constraints that fire on every sentence, plus the 8 `## Narrative` obligations that keep the standard from flattening expository prose. This file is the full catalog. Open it when you must adjudicate a specific case: a part-of-speech ruling, the parentheses rule, a possessive apostrophe, the full audit checklist, or [how agents over-apply these rules in practice](#this-repositorys-findings-on-over-application).

## Two warnings before you use this file

**1. Cite rule numbers ONLY from this file.** The official numbering is unintuitive and models fabricate it from memory. This is tested behaviour, not a theoretical risk: an agent without this file cited "Rule 3.1: short sentences". The real Rule 3.1 is about verb forms, and short sentences are Rule 4.1. If a rule number is not in a table below, do not write it.

**2. This skill runs pragmatic mode only.** Domain vocabulary is legal. "Idempotent", "webhook", "Lumberjack", "Vega-Lite", and "MathML" are technical nouns and they stay. Strict mode — full vocabulary discipline against the approved-word dictionary — is out of scope, and this skill never claims ASD-STE100 compliance. See [Limits](#limits).

## Step 1 — classify the passage

Every other rule depends on this classification. Do it first, and do not mix the two modes in one passage.

| | Procedural (instructions) | Descriptive (explanations) |
|---|---|---|
| Purpose | Tell the reader what to do | Explain what a thing is or does |
| Verb form | Imperative: "Install the package." | Simple present, simple past, simple future |
| Sentence limit | **20 words** (Rule 5.1) | **25 words** (Rule 6.3) |
| Unit rule | One instruction per sentence (Rule 5.2) | One topic per paragraph (Rule 6.5), maximum six sentences per paragraph (Rule 6.6) |

In an explainer: a "How to run it" section is procedural. A "How it works" section is descriptive. A `<figcaption>`, an `<aside>` note, and the deck are all descriptive, so each takes the 25-word limit and never the imperative.

## The rule catalog

53 rules in 9 sections, paraphrased from ASD-STE100 Issue 9. The official wording is in the free standard at asd-ste100.org. Word-level rulings — is this specific word approved, and in which part of speech — come from the official dictionary, which this file does not reproduce.

### Section 1 — Words (Rules 1.1–1.14)

| Rule | Instruction |
|---|---|
| 1.1 | Use only approved words, technical nouns, or technical verbs. |
| 1.2 | Use an approved word only as its listed part of speech. |
| 1.3 | Use an approved word only with its approved meaning. |
| 1.4 | Use only the approved forms of verbs and adjectives. |
| 1.5 | You can use domain words as technical nouns ("webhook", "commit", "endpoint"). |
| 1.6 | Use an unapproved word only when it is a technical noun or part of one. |
| 1.7 | Do not use technical nouns as verbs. |
| 1.8 | Use the technical nouns of the project or the industry. |
| 1.9 | When you pick a technical noun, pick a short and clear one. |
| 1.10 | No regional, slang, or jargon words as technical nouns. |
| 1.11 | One item, one name. Do not call it "config" here and "settings" there. |
| 1.12 | You can use domain verbs as technical verbs ("deploy", "compile", "merge"). |
| 1.13 | Do not use technical verbs as nouns. |
| 1.14 | Use American English spelling. |

In pragmatic mode, rules 1.5, 1.8, and 1.12 do the heavy lifting: the domain vocabulary is legal. The rules agents break are 1.7, 1.11, and 1.13.

**Before:** You can webhook the event, then do a deploy. The config is read at boot and the settings are cached.
**After:** Send the event to the webhook. Then deploy the service. The service reads the configuration at boot and caches it.

### Section 2 — Multi-word nouns (Rules 2.1–2.2)

| Rule | Instruction |
|---|---|
| 2.1 | Write multi-word nouns of three words or fewer. |
| 2.2 | When a technical noun needs more than three words, write it in full once, then give a short form or hyphenate the units. |

Break a long noun chain with a preposition: of, on, in, for.

**Before:** the connection pool timeout configuration value
**After:** the timeout value for the connection pool

### Section 3 — Verbs (Rules 3.1–3.7)

| Rule | Instruction |
|---|---|
| 3.1 | Use only the verb forms that the dictionary gives. |
| 3.2 | Use only these forms: infinitive, imperative, simple present, simple past, simple future, past participle as an adjective. |
| 3.3 | Use the past participle only as an adjective ("the cached response"). |
| 3.4 | No auxiliary verbs for complex constructions. No present perfect. No "is to be installed". |
| 3.5 | Use an `-ing` form only as a technical noun or inside one ("logging", "the mounting bracket") — never as a verb. |
| 3.6 | Active voice. In descriptive text, passive is legal only when the agent of the action is unknown. |
| 3.7 | Describe an action with a verb, not a noun ("compress the file", not "perform compression of the file"). |

**Approved modals: `can`, `will`, `must`. Banned: `should`, `would`, `may`, `might`, `could`.** The standard rejects `could` even for possibility: write "an overflow can occur", never "could occur". A requirement becomes `must`. A recommendation is stated as a fact or deleted. This matters double in agent-facing text, because models read `should` as optional. The full mapping is the [modal ladder](#the-modal-ladder).

**Before:** The migration has completed and the table is being rebuilt.
**After:** The migration is complete. The database rebuilds the table.

**Before:** The flag can be set in the config file, making restarts unnecessary.
**After:** You can set the flag in the configuration file. Then a restart is not necessary.

### Section 4 — Sentences (Rules 4.1–4.5)

| Rule | Instruction |
|---|---|
| 4.1 | Write short and clear sentences. |
| 4.2 | Do not omit words and do not use contractions to shorten a sentence. Keep the articles. Keep "that". |
| 4.3 | Use a vertical list for complex text. |
| 4.4 | Use connecting words between sentences on related topics ("Then", "As a result"). |
| 4.5 | Put an article (the, a, an) or a demonstrative adjective (this, these) before a noun where applicable. |

Rule 4.2 is the anti-terseness rule, and it is the one an explainer most needs. STE is short sentences with complete grammar, never telegraph style.

**Before (wrong shortening):** Ensure file exists before running.
**After:** Make sure that the file exists before you run the command.

### Section 5 — Procedural writing (Rules 5.1–5.5)

| Rule | Instruction |
|---|---|
| 5.1 | Maximum 20 words per sentence. Warnings and cautions are included in this limit. |
| 5.2 | One instruction per sentence, unless two actions happen at the same time. |
| 5.3 | Write instructions in the imperative: "Run the migration." |
| 5.4 | Put a required condition before the command, divided by a comma: "If the build fails, read the log." |
| 5.5 | Notes give information, never instructions. A note takes the 25-word limit. |

**Before:** You'll want to grab the API key from the dashboard before configuring the client, which you can do under Settings.
**After:** Get the API key from the dashboard, under Settings. Then configure the client with this key.

### Section 6 — Descriptive writing (Rules 6.1–6.6)

| Rule | Instruction |
|---|---|
| 6.1 | Give information gradually: one new fact per sentence. |
| 6.2 | Use key words and phrases to give the text a logical structure. |
| 6.3 | Maximum 25 words per sentence. |
| 6.4 | Group related information in paragraphs. |
| 6.5 | One topic per paragraph. |
| 6.6 | Maximum six sentences per paragraph. |

No imperative in descriptive text. A description explains. A procedure instructs.

**Before:** The scheduler, which was rewritten in 2024 to address several longstanding issues with fairness and starvation that had accumulated over the years, assigns work to a pool of workers that it manages itself.
**After:** The scheduler assigns work to a pool of workers that it manages. A 2024 rewrite corrected two faults in the old design: unfair ordering, and worker starvation.

### Section 7 — Safety instructions (Rules 7.1–7.3)

| Rule | Instruction |
|---|---|
| 7.1 | Use a word that shows the risk level: `WARNING` for injury, `CAUTION` for damage or data loss. |
| 7.2 | Start with a clear command or condition. |
| 7.3 | Then give the risk or the possible result. |

Never bury the instruction after the explanation. The pattern transfers directly to destructive flags, irreversible migrations, and dangerous API options — which is most of what an explainer warns about.

**Before:** Note that data loss may occur in some circumstances if the destructive flag happens to be enabled when running against production.
**After:** CAUTION: Do not use the `--force` flag against production. The flag deletes rows that do not match the source.

### Section 8 — Punctuation and word count (Rules 8.1–8.7)

| Rule | Instruction |
|---|---|
| 8.1 | All standard punctuation is legal except the semicolon. Write two sentences instead. |
| 8.2 | Use hyphens to connect words that act as one unit. |
| 8.3 | Parentheses are legal for references, item numbers, abbreviations, plural forms, explanations, and alternatives. |
| 8.4 | In a vertical list, the lead-in colon ends a sentence for the word count. |
| 8.5 | Text inside parentheses counts as one word. |
| 8.6 | Count as one word each of these: a number, a number with units, an abbreviation, an alphanumeric identifier, quoted text, a title, a label, a proper noun. |
| 8.7 | A hyphenated word counts as one word. |

**Ruling — Rule 8.1 bans the semicolon and NOTHING else.** Read the rule as written. The em dash is legal, the colon is legal, and Rule 8.4 rules on how a lead-in colon affects the word count, which presupposes that you can write one. Do not generalise the semicolon ban to any other mark. This ruling exists because the generalisation is measured behaviour, not a theoretical risk: across 93 explainers, em dashes fell 88 % and colons 57 % after the standard landed, tracking the semicolon's fall to zero, and no rule asked for either. See [This repository's findings](#this-repositorys-findings-on-over-application).

Rule 8.6 is what makes the caps workable in technical prose. A backticked command is quoted text and counts as one word, so a long identifier does not consume the sentence budget.

Worked count — this sentence is **8 words**, not 13:

> Run `sqlpipe run --config sqlpipe.yaml` against the staging database before 14:00 UTC.

`Run` (1) + the backticked command (1) + `against` (1) + `the` (1) + `staging` (1) + `database` (1) + `before` (1) + `14:00 UTC` (1).

**Ruling — a product name with a version number counts as ONE word.** `Claude Opus 4.8`, `Vega-Lite 5`, `Postgres 16`, and `ASD-STE100 Issue 9` are each one word. Rule 8.6 supports this twice over: the name is a proper noun, and the version is part of the alphanumeric identifier that names the thing. Do not count the version separately, and do not count the words inside the name. This ruling matters because a sentence naming two or three products stays comfortably under the cap under this reading and breaks the cap under the alternative.

Worked count — this sentence is **10 words**, not 15:

> Claude Opus 4.8 produced 1.05 violations per 100 words against 2.55 for Claude Opus 4.5.

`Claude Opus 4.8` (1) + `produced` (1) + `1.05` (1) + `violations` (1) + `per` (1) + `100 words` (1) + `against` (1) + `2.55` (1) + `for` (1) + `Claude Opus 4.5` (1). The sentence carries 4 separate figures and 2 model names and sits well under the descriptive cap.

**Watch Rule 6.6 instead.** Rule 8.6 makes a figure-dense sentence cheap, so on data-heavy prose the cap stops binding and paragraphs grow past the six-sentence ceiling instead. When you write about measurements, count sentences per paragraph rather than words per sentence.

**Before:** The command takes two arguments; the first is the config path (e.g. `sqlpipe.yaml`), the second is the table name, etc.
**After:** The command takes two arguments. The first argument is the path to the configuration, for example `sqlpipe.yaml`. The second argument is the name of the table.

### Section 9 — Writing practices (Rules 9.1–9.4, GR-1 to GR-8)

| Rule | Instruction |
|---|---|
| 9.1 | When a word-for-word replacement does not work, restructure the sentence. |
| 9.2 | Use each approved word correctly: approved meaning, approved part of speech. |
| 9.3 | Do not build phrasal verbs ("go down" → "decrease", "set up" → "install" or "configure"). |
| 9.4 | Keep one consistent style and terminology through the whole document. |

General recommendations:

| Rule | Instruction |
|---|---|
| GR-1 | Keep the conjunction "that". Do not drop it. |
| GR-2 | Be careful with "with" — it hides the real relation between the two nouns. |
| GR-3 | Give every pronoun a clear referent. |
| GR-4 | Prefer "this + noun" over a bare "this". |
| GR-5 | Avoid false friends: words that a non-native reader maps to a different meaning in their own language. |
| GR-6 | Avoid Latin abbreviations. |
| GR-7 | Use inclusive language. |
| GR-8 | Use the possessive apostrophe only when you are sure it is correct. If unsure, do not use it — non-native readers find it hard. |

GR-6 in practice: `e.g.` → "for example", `i.e.` → "that is", and `etc.` is deleted by naming the items or by writing "and more".

**Before:** It's worth noting that the retry logic can be set up prior to deployment in order to gracefully handle transient failures, e.g. rate limits.
**After:** Configure the retry logic before you deploy. The client retries three times, then stops. A rate limit is the usual cause of a retry.

## Vocabulary discipline

The official dictionary — roughly 900 approved words and roughly 1,200 banned words with alternatives — is copyrighted by ASD and is **not reproduced here**. Its mechanics apply without it: **one word, one meaning, one part of speech.** For a word-level ruling, go to the official standard at asd-ste100.org.

### Known part-of-speech rulings

Nine illustrative rulings, useful as patterns for the shape the dictionary's rulings take. This is not the dictionary.

| Word | Ruling |
|---|---|
| test | Noun only. "Do a test", not "test the pump". |
| check | Noun only. "Check that X" becomes "make sure that X". |
| work | Noun only. |
| oil | Noun only, as used in the standard's examples. For the verb, the dictionary gives "lubricate". |
| help | Verb only. For the noun, the dictionary gives "aid": "with the aid of". |
| fall | "To move down by gravity" only, never "decrease". |
| follow | "To come after" only, never "obey". Write "obey the instructions". |
| above | Physical position only. For a limit, write "more than". |
| below | Physical position only. For a limit, write "less than". |

### The modal ladder

| You wrote | STE writes |
|---|---|
| `should` (requirement) | `must` |
| `should` (recommendation) | Delete it, or state it as a fact: "X is better because Y." |
| `may` / `might` / `could` (possibility) | `can` |
| `may` (permission) | `can` |
| `would` (hypothetical) | Restructure: "If X occurs, Y occurs." |

### Slop-to-simple substitutions

**This table is this repo's, not the ASD dictionary.** It maps the words that model-generated prose overuses to plain replacements. Nothing here is an ASD ruling.

**If the word carries no fact, delete it instead of replacing it.** That rule governs the whole table. A replacement that preserves an empty word has not improved the sentence.

| Slop | Write instead |
|---|---|
| leverage, utilize | use |
| in order to | to |
| prior to | before |
| ensure | make sure that |
| it is worth noting that | (delete) |
| it is important to, crucially | (delete — state the fact) |
| simply, just, easily, seamlessly, effortlessly | (delete) |
| robust, powerful, comprehensive, performant | (delete, or give the measurable property) |
| functionality | function, feature |
| enables you to, allows you to | you can |
| is designed to, aims to | (delete — say what it does) |
| facilitate | help, make possible |
| dive into, delve into | read, examine |
| when it comes to | for |
| in the event that | if |
| due to the fact that | because |
| as needed, as necessary | (state the condition) |
| and/or | Pick one, or write "X, or Y, or both" |
| e.g. / i.e. / etc. | for example / that is / (name the items) |
| gracefully handles | (say what it does: "retries three times, then stops") |
| out of the box | by default |
| under the hood | internally |
| blazingly fast, state-of-the-art | fast (give the number) / (delete) |
| streamline | make simpler, make faster |
| plethora, myriad | many |
| addresses the issue, tackles | corrects the fault, removes the error |

### Consistency pass

Fix the vocabulary BEFORE you draft. Collapse each rotation below to one term for the whole document (Rules 1.11, 9.4), then use no other member of the set anywhere.

- check / verify / confirm / validate / ensure → pick one
- config / configuration / settings / options → pick one
- delete / remove / drop / destroy → one per meaning, kept consistent
- error / issue / problem / failure → "error" for errors, "failure" for failed operations
- run / execute / invoke / launch → pick one
- show / display / render / present → pick one

## Untouchables

These are technical names (Rules 1.5, 8.6). Leave them exact, even where they break a vocabulary rule:

- Code blocks and inline code
- Identifiers, CLI commands, flags, file paths
- Quoted error messages and log lines
- Product names, API endpoint names, config keys
- Numbers with units — each counts as one word toward the sentence limit

The explainer skill extends this list. See [Explainer adaptations](#explainer-adaptations).

## This repository's ruling on pointers and indexes

**This section is this repository's, not an ASD ruling.** The standard legislates referents, and it scopes that legislation to pronouns and demonstratives. The extension to numbered pointers is ours.

`SKILL.md` carries it as constraint 14: gloss every pointer on first use, and name in plain words what it points at, in the same sentence. A pointer is a reference whose referent the reader cannot recover from the reference itself — a section or step number, a table or figure number, a rule number, a ticket identifier, an internal code. A self-describing name is not a pointer. `Postgres 16`, `--validate`, and `assets/template.html` each name their own referent, so no gloss is owed.

**Three upstream anchors, and the scope limit that makes this an extension.**

| Anchor | What it says | Why it does not reach a numbered pointer |
|---|---|---|
| GR-3 | Give every pronoun a clear referent. | Scoped to pronouns. |
| GR-4 | Prefer "this + noun" over a bare "this". | Scoped to demonstratives. |
| Rule 8.6 | A label counts as one word. | A counting rule. It says a label is cheap, never that a label is clear. |

GR-4 is the instructive one. A bare "this" stands in for a noun that the writer holds and the reader must guess, and a bare `4c` does exactly that. The logic transfers and the scope does not, so this ruling is stated as ours.

**The deletion test.** Delete every pointer from the sentence. If the sentence still states its claim, the pointers annotate a stated fact and no gloss is owed. If the sentence collapses, the pointers ARE the claim and each one must name its referent.

The test needs to fail the right sentences and pass the rest, so both directions are worked here:

- **Fails.** `In Section 5a we look to implement o6f3 but must keep in mind 4c, 4d in order to fully realize the goal (T77).` Delete the five pointers and the residue is `In Section we look to implement but must keep in mind , in order to fully realize the goal ()`. Nothing survives.
- **Passes.** `Rule 8.6 makes a figure-dense sentence cheap, because a backticked command counts as one word.` Delete the pointer and the sentence still states its claim. No gloss is owed.

**Worked before/after**, on the sentence that prompted the rule:

**Before:** In Section 5a we look to implement o6f3 but must keep in mind 4c, 4d in order to fully realize the goal (T77).
**After:** Section 5a, on the ingest rewrite, implements the `o6f3` batching path. That path depends on two earlier decisions: 4c, which fixes the retry budget, and 4d, which fixes the dead-letter queue. Ticket T77 tracks the work.

Two things about that pair are worth stating plainly. First, the "before" passes every other constraint: no banned modal, no semicolon, no contraction, no present perfect, no trailing condition, and 15 Rule 8.6 words against a 25-word cap. Second, applying the Section 9 filler rules to it produces `Section 5a implements o6f3, which depends on 4c and 4d (T77).` — shorter, cleaner, and still unreadable. **A standard whose full application leaves a sentence unreadable is missing a constraint.** That is the argument for constraint 14, and the deletion test is what keeps it from firing everywhere.

Constraint 14 pushes against three rules, and each conflict is settled in the agent's always-loaded file: a gloss states a fact, so Section 9 filler deletion does not take it; the pointer's own text is an Untouchable, so the gloss goes beside it and never replaces it; and where a gloss breaches Rule 5.1 or Rule 6.3, the sentence splits and the gloss stays.

**What this ruling is NOT built on.** The [over-application findings](#this-repositorys-findings-on-over-application) below rest on a 93-explainer corpus measurement. This one does not. **No pointer-density measurement of that corpus was made**, before or after the standard landed, so no figure is claimed here. The ruling rests on one reported failure and on the rule-gap analysis recorded in `openspec/changes/archive/2026-08-19-add-explainer-pointer-gloss-rule/design.md`. It sits next to measured findings, so the distinction is stated rather than left for a reader to assume.

## Self-check before you deliver

**This step is not optional.** `SKILL.md` carries the authoritative two-part version. This is the same check in full.

Run both parts against the prose **as it stands in the written file**, never against a draft held in your context. A check run before injection measures text you then edit, so its result does not describe what you ship.

### Part A — violations

1. **Pointer sweep — first, before the length count.** Search for `\b[0-9]+[a-z]\b` (catches `5a`, `4c`), for `\b[A-Z][0-9]+\b` (catches `T77`), for `\b[a-z]+[0-9]+[a-z][a-z0-9]*\b` (catches a lowercase internal code such as `o6f3`), and for `Section`, `Rule`, `Step`, `Table`, `Figure`, and `Appendix` followed by a number. Apply the deletion test to each hit, then gloss on first use, per [the pointer ruling](#this-repositorys-ruling-on-pointers-and-indexes). The patterns over-match on purpose: a surfaced pointer that needs no gloss costs one judgment call, and a missed pointer costs the reader the sentence. **This step runs first because a gloss adds words.** A length count taken before the gloss measures text that no longer exists, and the split it prescribes lands on a sentence the gloss then lengthens again.
2. **Longest sentences.** Count the words in the three longest sentences. Split any sentence that is over its classification's cap — 20 words procedural, 25 words descriptive. Apply Rule 8.6 when you count.
3. **Searchable-pattern sweep.** Search for each of these literal strings: `'ll`, `'re`, `'ve`, `n't`, `it's`, `has been`, `have been`, `had been`, `should`, `would`, `may`, `might`, `could`, `is being`, `, making`, `, allowing`, `, enabling`, `, ensuring`, `;`, `e.g.`, `i.e.`, `etc.` Every hit outside the Untouchables is a violation. Fix each one. This list is complete as written: the em dash and the colon are NOT on it, per the Rule 8.1 ruling in Section 8.
4. **Condition placement.** Search for every `if` and every `when`. Move any condition that trails its command to the start of its sentence, and add a comma.
5. **Unchosen synonyms.** Search for the members of the check / verify / confirm / validate set that you did NOT choose, and for `config` / `settings` if that pair was not fixed. Replace every hit with the chosen term.

### Part B — texture

Every step in Part A searches for material to delete, so Part A cannot fail a document for being lifeless. Part B can. Run it AFTER Part A, because Part A splits and deletes and would undo this work.

6. **Distribution.** Count the Rule 8.6 length of every sentence and inspect the spread. The target is two-sided. Too tight or too short — a band narrower than about 6 words, or fewer than about one sentence in five at 18 to 25 words — is repaired by combining related short claims into one sentence that carries a joint: a subordinate clause, an em-dash aside, or a colon. Too long — more than about one sentence in three at 18 to 25 words, or fewer than about one in six at 8 words or less — is repaired by splitting the flabbiest long sentences so a short one can carry the verdict. NEVER pad a sentence with filler.
7. **Devices.** Confirm that the deck and the conclusion assert the thesis, that at least one analogy or worked example appears where the subject has a mechanism to make legible, and that the author's voice is present where the author is the agent.
8. **Re-measure after any repair.** A repair under step 6 changes the distribution it was measured against, and a split under Part A creates the clustering step 6 looks for. After your last edit to the file, measure the spread once more.

### Full audit checklist

Adapted from the upstream `references/checklist.md`. Run this pass when the two-part check above finds a lot, or when the explainer is long. The checks are ordered from mechanical to judgment.

**Mechanical (searchable).** Every hit outside the Untouchables is a violation.

| Search for | Violation | Fix |
|---|---|---|
| `'ll`, `'re`, `'ve`, `n't`, `it's` | Contraction (Rule 4.2) | Expand it. |
| `has been`, `have been`, `had been` | Present or past perfect (Rule 3.4) | Simple past or simple present. |
| `has` / `have` + past participle | Present perfect (Rule 3.4) | Simple past. |
| `should`, `would`, `may`, `might`, `could` | Banned modal (Rule 3.2) | See the modal ladder. |
| `is being`, `are being`, `was being` | Progressive passive (Rules 3.4, 3.5) | Active voice, simple tense. |
| `, making`, `, allowing`, `, enabling`, `, ensuring` | `-ing` clause used as a verb (Rule 3.5) | New sentence with a real subject. |
| `;` | Semicolon (Rule 8.1) | Two sentences. |
| `e.g.`, `i.e.`, `etc.` | Latin abbreviation (GR-6) | "for example", "that is", name the items. |
| `simply`, `just`, `easily`, `seamlessly`, `robust` | Filler, carries no fact | Delete. |
| ` if `, ` when ` (mid-sentence) | Trailing condition (Rule 5.4) | Move the condition to the start, add a comma. |
| `\b[0-9]+[a-z]\b`, `\b[A-Z][0-9]+\b`, `\b[a-z]+[0-9]+[a-z][a-z0-9]*\b`, `Section`/`Rule`/`Step`/`Table`/`Figure`/`Appendix` + number | Bare pointer, referent not recoverable (this repo's constraint 14) | Apply the deletion test, then gloss on first use. |

**Countable.**

1. **Sentence length.** Count the words in each sentence. Procedural: 20. Descriptive: 25. Notes and captions: 25. Apply Rule 8.6.
2. **Paragraph size.** Maximum six sentences per paragraph (Rule 6.6).
3. **Multi-word nouns.** Break any noun chain over three words with a preposition (Rule 2.1).
4. **Instructions per sentence.** One, unless the two actions are simultaneous (Rule 5.2).

**Judgment.**

5. **Classification.** Is each passage cleanly procedural or descriptive? Procedures are imperative. Descriptions are never imperative.
6. **Voice.** For each passive sentence: is the agent truly unknown, and is the passage descriptive? Otherwise make it active (Rule 3.6).
7. **Condition placement.** Every `if` and `when` stands before its command, with a comma (Rule 5.4).
8. **Synonym rotation.** One term per concept across the whole document (Rules 1.11, 9.4).
9. **Warnings.** Command or condition first, risk second (Rules 7.2, 7.3).
10. **Completeness.** The articles are present, "that" is present after "make sure", and no sentence reads as a telegram (Rule 4.2).
11. **Untouchables intact.** Code, identifiers, quoted errors, and proper nouns are unchanged.
12. **Carve-outs respected.** The thesis is still an assertion, the analogies and the worked examples are still present, and the sentence lengths vary below the cap.

## Explainer adaptations

An explainer is expository prose with a thesis, not a maintenance manual. Applied literally, the standard degrades it: uniform sentences, deleted analogies, and a hedged thesis. `SKILL.md` carries these as the eight numbered obligations of its `## Narrative` section, stated in the imperative and carrying the same force as the 14 constraints. They are stated there rather than only here, because an agent that reads only `SKILL.md` still needs them.

They are obligations, not permissions. That wording is deliberate and it was earned: see [This repository's findings](#this-repositorys-findings-on-over-application) below.

1. **Assert the thesis.** State a claim in the deck and in the concluding passage, and stand behind it ("Batching at the edge is the wrong layer to optimise"). Banned modals and hedging language remain banned. Asserting is not hedging, and neutral description does not substitute for a claim.
2. **Vary sentence length across the full range below the cap.** The caps are ceilings, never targets. Both a document of uniformly short sentences and a document of uniformly long ones violate the spirit of Rule 4.2, which exists to forbid telegraph style. The target is two-sided, and `SKILL.md` carries the calibration figures.
3. **Keep the analogy and the worked example.** A resemblance is a fact about the subject, not decoration. Section 9 filler deletion does not license the removal of the worked example or of the analogy that makes a mechanism legible.
4. **Write in the author's own voice where the author is the agent.** First-person reference is legal, and Rule 3.6 often requires it, because active voice needs a named agent. A correction memo states "My earlier figure was wrong".
5. **Let each paragraph carry a developed thought.** Hold to Rule 6.5 and Rule 6.6. A thought split across two paragraphs to stay under the sentence cap is fragmented, not clarified.
6. **Reproduce quoted source material exactly.** Text inside `<blockquote>`, `<code>`, `<pre>`, `<math>`, and any Vega-Lite JSON spec is never rewritten for compliance. A quotation drawn from a `--from-file` source is reproduced exactly, including its own violations.
7. **Write figure captions to the descriptive limit** (25 words), and never in the imperative.
8. **Leave marketing register out.** The standard deletes persuasion by design and this skill does not restore it. An explainer explains. It does not sell.

## This repository's findings on over-application

**This section is this repository's, not an ASD ruling.** It records how agents misread the rules above, measured rather than supposed. Nothing here is in the standard.

The measurement: 93 explainers from one author on one subject across one week, 108,814 words of prose, split by whether they were written before or after this standard landed. Method and full tables in the archived change at `openspec/changes/archive/2026-08-03-restore-explainer-narrative-texture/evidence/corpus-measurement.md`.

The standard worked. Banned modals fell 96 %, semicolons to zero, over-cap sentences 93 %. It also cost four things, and three of them are misreadings of rules that do not say what the agent thought they said.

| Over-application | What the rules actually say | Correction |
|---|---|---|
| **1. The cap read as a target.** The mean sentence barely moved (12.64 to 12.28 words) but the 18-to-25-word band fell from 24.1 % to 19.2 % and the spread narrowed 10 %. The long tail died while the average held. The corpus left 12.5 words of headroom unused under a 25-word cap. | Rule 5.1 and Rule 6.3 give maxima. Rule 4.2 forbids telegraph style, which is the opposite failure and is stated just as plainly. | Obligation 2, with a two-sided target. A document whose sentences cluster fails even when every sentence passes the cap. |
| **2. The `;` sweep generalised.** Em dashes fell 88 % and colons 57 %, tracking the semicolon's fall to zero. | Rule 8.1 bans the semicolon and nothing else. Rule 8.4 rules on the lead-in colon's word count, which presupposes the colon is legal. | The Rule 8.1 ruling in Section 8, plus the Part A step 3 note that the sweep list is closed. |
| **3. First person suppressed.** First-person reference fell 37 %. | No rule restricts it. Rule 3.6 mandates active voice, which requires a named agent — and where the agent is the author, that word is "I". | Obligation 4. "I patched the file" is MORE compliant than "the file was patched". |
| **4. Paragraphs fragmented.** 38 % more paragraphs per document, each 14 % shorter. | Rule 6.6 caps a paragraph at six sentences. Shorter sentences mean six of them cover less ground, so the cap bites harder than intended. | Obligation 5. This one repairs itself once obligation 2 restores the long sentence, so Rule 6.6 needs no change. |

Two second-order findings worth keeping:

- **The em dash and the long sentence are one loss.** The dash is what lets a sentence carry a second thought without splitting in two. Restoring it is what makes obligation 2 achievable rather than merely required.
- **Correcting a floor invites overshooting it.** The first document drafted under obligation 2 landed at 50 % of sentences in the 18-to-25-word band against a 24.1 % baseline, with short sentences down to 13.5 %. It used zero filler, so it complied honestly and optimised anyway. Hence the two-sided target: a floor with no ceiling has only one direction to move in.

## Limits

STE is for technical facts and instructions. Do not apply it to marketing copy, blog voice, or brand writing — it deletes persuasion by design.

This reference is an **unofficial aid**. It is **not affiliated with or endorsed by ASD or STEMG**. **No tool can guarantee ASD-STE100 compliance**, and final approval rests with the writer. **ASD-STE100 is a registered trademark of ASD.** The official standard is a **free download at [asd-ste100.org](https://asd-ste100.org)**.

The ASD approved-word dictionary and banned-word list are copyrighted by ASD and are not reproduced in this file. This file ships rule mechanics only. For any word-level ruling, consult the official standard.
