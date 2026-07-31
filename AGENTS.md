# Agent Ground Rules

## Purpose
This repository is used to create and maintain agent skills. These rules define the baseline engineering policy for all work here, with a strict preference for open standards and portable skill design.

## Scope
These rules apply to all work in this repository.

## Ground Rules

### 1. Open Standards First (Strict by Default)
**Policy:** Prefer open, documented, portable standards for formats, protocols, and skill structure. Proprietary choices require a documented exception.

**Rationale:** Open standards preserve interoperability and keep skills reusable across tools and runtimes. See: https://agentskills.io/home

**Checks:**
- Use standard `SKILL.md`-compatible conventions where applicable.
- Avoid vendor-specific-only formats when an open equivalent exists.
- If an exception is required, record reason, impact, and fallback or exit path.
- Skills are installed into agent roots via the Nix-managed copy-tree sync (see [`SKILLS.md`](SKILLS.md#install)). Do not symlink this repo or any subtree into `~/.claude/skills`, `~/.agents/skills`, or any project's `.claude/skills` / `.agents/skills` — tool discovery rejects symlinks.

### 2. Portability and Interoperability by Design
**Policy:** Author skills so they can operate in multiple compatible agent environments with minimal changes.

**Rationale:** Skills should be transferable assets, not tightly coupled to one runtime or environment.

**Checks:**
- Parameterize or isolate environment-specific paths and config.
- Make external dependencies explicit and replaceable.
- Document required environment assumptions in the skill.

### 3. Deterministic, Verifiable Workflows
**Policy:** Prefer repeatable, script-backed or explicitly stepwise workflows over ambiguous instructions.

**Rationale:** Deterministic workflows improve reliability and make outcomes easier to audit and reproduce.

**Checks:**
- Define concrete inputs and outputs for critical flows.
- Move repeated logic into `scripts/` when appropriate.
- Include validation steps that confirm expected outcomes.

## Exception Process
Exceptions are allowed only when no viable open-standard option exists, or an external constraint requires a proprietary dependency.

When an exception is used, record:
- Decision
- Why it is needed
- Time horizon
- Migration or fallback plan
