# Public readiness review

A skill does not become public because it looks harmless. It becomes public
because someone reviewed it against this checklist and committed the result.

Adding a source to `publicSources` in `nix/public-allowlist.nix` requires a
completed review for every skill in that source, committed in the same change.

`scripts/scan-public.sh` catches known-bad strings and nothing more. It is a
regression guard, not a reviewer. Every item below marked **judgment** is
something no regex decides.

## Why this exists

An audit of this repository found no committed secrets — credential blobs are
GPG-encrypted, gitignored, and absent from history. What it did find was
customer and internal-infrastructure data spread through ordinary example text:
an internal hostname repeated 58 times, private device IPs, real customer well
names used as sample values, and `file:line` citations into a private monorepo.
None of that looks like a leak while you are writing it. All of it is a leak
once the repository is public.

## Checklist

Copy this block into the change that adds the skill, fill it in, and commit it.

### Credentials and paths

- [ ] No credentials, tokens, API keys, or client secrets, including in example
      commands and expected-output blocks.
- [ ] No path to a credential file, encrypted or not. A path discloses your
      layout and invites someone to look for the file.
- [ ] No `.gpg` references.
- [ ] No developer-absolute paths (`/Users/…`, `/home/…`). Scripts resolve their
      own location; documentation uses a placeholder or a `$VAR`.

### Hosts and networks

- [ ] No internal hostnames or non-public fully-qualified domain names.
- [ ] No private IP addresses, and no device addresses of any kind.
- [ ] No internal subdomains of a third-party SaaS product, which name your
      employer even when the product is public.
- [ ] No database connection strings, queue URLs, or VPN hosts.

### Customer and business data

- [ ] No customer, company, well, site, or facility names — including as
      example values. **judgment**
- [ ] No real parameter IDs, PIDs, serial numbers, UUIDs, or account IDs.
      Replace with obviously-synthetic values that cannot be looked up.
- [ ] No email addresses or phone numbers, including your own work address.
- [ ] No person names other than the repository owner.
- [ ] Fixtures are synthetic, not captured from production. A capture carries
      whatever happened to be in the response. **judgment**

### Provenance

- [ ] No `file:line` citations into a private repository. These disclose that
      the repository exists, its layout, and that you read it.
- [ ] No undocumented internal API routes whose existence is itself
      confidential. **judgment**
- [ ] No content derived from material under an NDA, and no reverse-engineered
      third-party protocol, without a deliberate decision recorded in the
      change. The risk here is legal rather than privacy, so the scanner and the
      rest of this checklist will both pass it. **judgment**

### Works on its own

- [ ] Every cross-skill reference resolves inside the public set. A pointer to a
      skill that is not published is a dead end for the reader.
- [ ] Script dependencies are declared inline (PEP 723 `# /// script`).
- [ ] The skill runs from a fresh clone with no repository-specific setup.
- [ ] Asset resolution is relative to the script, never absolute.

### Licensing

- [ ] Vendored third-party assets are listed in `THIRD-PARTY-NOTICES.md` with
      version, license, and the upstream copyright notice reproduced.
      Publishing is redistribution, and MIT and BSD-3-Clause both require the
      notice to travel with the copy. Minification strips license preambles, so
      a minified bundle needs its notice restored by hand.
- [ ] No vendored asset under a copyleft or non-commercial license that
      conflicts with this repository's MIT license. **judgment**

## Mechanical pass

Run these before signing off. They do not replace the checklist.

```bash
./scripts/scan-public.sh <source-dir>          # must print "clean"
grep -rnE '/Users/|/home/' <source-dir>        # expect no hits
grep -rniE '@[a-z0-9.-]+\.(com|net|io|org)' <source-dir>   # inspect each hit
```

## Sign-off

```
Skill(s):     <ids>
Source:       <key in nix/sources.nix>
Reviewed by:  <name>
Date:         <YYYY-MM-DD>
Scanner:      clean / <n> hits resolved
Judgment items: <what you decided and why, for each **judgment** box>
Result:       APPROVED / BLOCKED (<reason>)
```

## Completed reviews

### explainer (source: `agents`)

```
Skill(s):     explainer
Source:       agents
Reviewed by:  Scott Murphy
Date:         2026-07-31
Scanner:      clean (0 hits across 14 tracked files)
Result:       APPROVED
```

Two defects were found and fixed before approval:

1. `agents/skills/explainer/SKILL.md` pointed at
   `~/.claude/skills/dataviz/SKILL.md` as the palette authority. That skill is
   not in this repository, so a public reader followed a dangling path. The
   guidance is now stated directly, with the external skill named as optional.
2. The four vendored bundles under `agents/skills/explainer/assets/` had no
   attribution. Mermaid is MIT; Vega, Vega-Lite, and Vega-Embed are
   BSD-3-Clause and require the copyright notice in a redistribution.
   `THIRD-PARTY-NOTICES.md` now reproduces all four, with hashes verified
   against `assets/README.md`.

Judgment items: no customer data, no private-repo citations, no NDA-derived
content. The skill generates HTML documents and talks to no service. Vendored
licenses (MIT, BSD-3-Clause) are compatible with this repository's MIT license.

### onping, lumberjack-restore, onping-charts (target: `plow-technologies/onping-skills`)

```
Skill(s):     every OnPing skill: the 142 under onping/skills (including the 11
              `_*` helper modules), the 3 lj-restore-* skills under
              onping/skills/lumberjack-restore, and onping-line-graph; 146 IDs,
              listed in nix/onping-skills-allowlist.nix
Source:       onping, lumberjack-restore, onping-charts (per-skill allowlist)
Target:       plow-technologies/onping-skills (not smurphy8/public-skills)
Prepared by:  Claude Code, from owner decisions recorded 2026-09-30
Reviewed by:  Scott Murphy
Date:         2026-09-30
Scanner:      clean (464 hits under the previous patterns, plus the new
              line-numbered-citation, OOXML, and name markers, all resolved)
Judgment items: see below
Result:       APPROVED (after review of plow-technologies/onping-skills PR #1)
```

This source was rated HIGH / "not a candidate" for `smurphy8/public-skills`. It
is cleared for a different target, the company-owned
`plow-technologies/onping-skills`, by fixing the findings. The scrub replays an
earlier unmerged pass (branch `publish-onping-skills`) and extends it to the
files that pass never saw: the MQTT integrator skills, `_mqtt_integrator_routes`,
and a spreadsheet template.

| Marker | Resolution |
|---|---|
| Developer-absolute path | Rewritten to the installed `~/.claude/skills/<skill>/` layout |
| Private device IP | RFC 5737 documentation addresses (`192.0.2.x`) |
| Private-repo citation | Repo roots and every `:line` suffix removed; bare module names kept |
| Real Lumberjack serial | Synthetic `1001` |
| Customer, well, and person names | Synthetic values; the scanner now checks names in every file |
| Real PIDs and IDs in examples | Synthetic values, one consistent mapping (judgment pass, below) |
| Spreadsheet template | 36 real PIDs and a well name replaced; structure unchanged |
| Other providers' credential file names | Removed from comments |

**Judgment: OnPing's API routes are published deliberately.** Documenting them
is what these skills are for, and the target is owned by the company that owns
OnPing. The routes are reachable by any authenticated customer, carry no
credentials, and enforce permissions server-side.

**Judgment: the product host is public.** `https://onping.plowtech.net` is the
OnPing service every skill calls. The scanner permits exactly that host and
still rejects every other occurrence of the employer domain.

**Judgment: authentication is unchanged, by owner decision.** `onping-login`
and the `onping-doc-*` skills keep their resolution order (environment
variable, plaintext file, then `gpg -d` of an encrypted file). No credential is
in the tree; the exported `.gitignore` lists the credential file names.

**Judgment: example values were captured, not invented, and all of them are gone.**
Examples were pasted from production. Beyond what the scanner sees, a manual pass
over every code block and every 3–8 digit number replaced 27 PIDs, the VPIDs, the
audit row IDs, location, site, company, serial, and control-parameter IDs,
truncated hash and UUID prefixes, a private commit reference, and several
customer, well, and site names. It used one shared mapping, so cross-skill
references still line up. The names found are now scanner rows. Kept on
purpose: counts, sizes, ports, timestamps, and the docs site's public document
IDs. Internal bug-tracker numbers were removed by owner decision; the text around
each one still describes the bug, and the scanner now rejects tracker references.

**Judgment: no NDA or reverse-engineered content.** These skills document a
first-party API against a first-party service.

**Owner decision: every skill that changes live data warns.** 53 skills start
their `SKILL.md` with a standard warning that says what they change, whether it
can be undone, and how the script gates it. The warnings come from reading the
scripts. The exported README opens with the same warning, and the LICENSE
disclaims warranty and liability.

**Owner decision: this target is proprietary.** The export writes its own
`LICENSE`, `Copyright (c) 2026 Pak Energy LLC. All Rights Reserved.`, and never
ships this repository's MIT license. This repository and `smurphy8/public-skills`
stay MIT.

## Deferred sources

Reviewed enough to rank, not cleared for publication.

| Source | Rating | Blocking work |
|---|---|---|
| `devtools`, `hugging_face` | CLEAN | One absolute path each to parameterize |
| `aha`, `azdo` | LOW | ~12 absolute paths in examples; `lib/` dirs need `extraPaths` |
| `google` | LOW-MED | Work email and domain hint in 6 lines |
| `aml` | MEDIUM | **Legal, not privacy.** Reverse-engineered vendor protocol with C# source citations; documents credential recovery from a config export. Needs a deliberate decision, not a scrub. |
| `openspec`, `pakenergy` | HIGH | Not a candidate. Real customer identifiers and internal process detail. |
| `onping` | — | Not for this target. Published per skill to `plow-technologies/onping-skills`; see the review above. |
