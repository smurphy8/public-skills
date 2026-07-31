# Agents Skills

Generative-content skills — authoring skills that turn a topic, question, or set of findings into a browsable artifact for a human to read. Peers of the provider-integration trees (OnPing, Aha, Azure DevOps, Google, HF, Pak Energy); these are provider-agnostic and produce standalone documents.

## Skills

### explainer

Create a throwaway HTML explainer in a plain, flat editorial style with serif body text and simple-English prose. Mints a single self-contained file (no CDN, no tracking, print-friendly) with optional Mermaid diagrams, Vega-Lite charts, and native MathML math; validates existing files against the style and output-boundary invariants. Prose obeys an ASD-STE100-derived language standard documented in `explainer/references/simple-english.md`.

- **Script:** `explainer/scripts/new_explainer.py`
- **Modes:** `--title <t> --subtitle <s> [--from-file <path>] [--output <dir>]` (create) or `--validate <path>` (lint)
- **Output:** Absolute path to a single self-contained `.html` file under `$TMPDIR/explainers/` (default) or the caller-supplied `--output` directory
