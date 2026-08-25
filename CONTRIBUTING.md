# Contributing

## How this repository is produced

This is a published subset of a larger private catalog. It is **generated**, not
edited directly.

The private repository holds skills that cannot be published: internal
hostnames, customer identifiers, and API surfaces that are not public. Rather
than trusting a careful hand to keep those apart, the public copy is built by a
script from an explicit allowlist onto a branch with no shared history.

```
private main ──●──●──●──●        (never pushed here)

public       ●                   orphan root, no parent
             │
             └─ scripts/export-public.sh
                  reads nix/public-allowlist.nix
                  copies allowlisted, git-tracked paths
                  runs scripts/scan-public.sh
                  commits
```

The orphan branch is the point. A branch descended from `main` would carry every
private commit as reachable ancestry, so a clone could recover them regardless
of what the tip looks like. An orphan root has no parent, so there is nothing to
recover.

## Guardrails, and what each is worth

| Layer | Catches | Defeated by |
|---|---|---|
| Orphan branch topology | All private history | Nothing — it is not reachable |
| Path allowlist in `pre-push` | Private files in a push | `--no-verify`, or a clone with no hook |
| `scripts/scan-public.sh` | Private strings in allowed files | `--no-verify`, or an unknown marker |
| `docs/public-readiness.md` | What no regex decides | Human inattention |

**Be clear about the hook's limits.** It is local to one clone, a fresh clone has
none configured, and `git push --no-verify` skips it entirely. It is a seatbelt.
The durable protection is the topology above it.

Enable the hook once per clone:

```bash
git config core.hooksPath .githooks
```

The scanner is a denylist. It matches markers a real audit of this codebase
found, so it guards against regressions of known problems. It cannot catch a new
internal hostname or a customer name in prose. That is what the readiness review
is for.

## Adding a skill

1. Create `<provider>/skills/<skill-name>/SKILL.md` plus any scripts, assets, or
   references. Folder names are globally unique across providers, lowercase with
   hyphens.
2. Add the provider to `nix/sources.nix` if it is new:

   ```nix
   <provider> = { path = ../<provider>; subdir = "skills"; filter.maxDepth = 1; };
   ```

3. Run `nix flake check` to confirm the catalog still evaluates.

Follow the ground rules in [`AGENTS.md`](AGENTS.md): open standards first,
portability by design, deterministic workflows.

Write skills that work from a fresh clone. Resolve paths relative to the script
(`Path(__file__).resolve().parent`), never absolutely. Declare Python
dependencies inline with PEP 723:

```python
# /// script
# requires-python = ">=3.11"
# dependencies = ["requests"]
# ///
```

## Versioning a skill

A skill that carries a `CHANGELOG.md` follows [semver](https://semver.org/).

**While the major version is `0`, a breaking change takes the minor slot.**
Pre-1.0 semver has nowhere else to put one. For a skill whose product is a
standard rather than an API, "breaking" means a document or config that complied
with the previous version does not comply with this one. A defect fix that
changes no rule and no interface takes the patch slot.

**The changelog entry lands in the same commit as the change it records.** A
changelog written later is a changelog reconstructed from `git log`, and the
reconstruction is guesswork about intent that was obvious at the time. The
explainer's history had to be recovered this way once; that is the reason this
section exists.

**`CHANGELOG.md` is authoritative and `plugin.json` mirrors it.** The order
matters because only one of them installs. The bundler and `scripts/install.sh`
copy `<provider>/skills/<id>/` and nothing above it, so a manifest at
`<provider>/.claude-plugin/plugin.json` is invisible to an installed skill —
deliberately, and the canonical spec asserts it. A version stated only in a
manifest cannot be read by the person holding the skill. Put the changelog in the
skill directory and bump the manifests to match.

Do not add a `version:` key to `SKILL.md` frontmatter. Frontmatter is `name`,
`description`, and optionally `allowed-tools`. A third copy of the version would
sit in the file most certain to be read while being the easiest to forget.

**A documentation-only change does not bump the version.** A bump asserts that
the skill changed. If no rule, script, template, asset, or output moved, leave
the number alone.

## Publishing a skill

A skill becomes public only by being added to `publicSources` in
`nix/public-allowlist.nix`, and that requires a completed review.

1. Work through [`docs/public-readiness.md`](docs/public-readiness.md) for every
   skill in the source.
2. Run the mechanical pass:

   ```bash
   ./scripts/scan-public.sh <source-dir>     # must print "clean"
   ```

3. Commit the completed review alongside the allowlist change. A review that is
   not committed did not happen.
4. Export and verify:

   ```bash
   ./scripts/export-public.sh
   ```

The scanner passing is necessary and not sufficient. Several checklist items are
marked **judgment** because no pattern decides them — whether a value is a real
customer identifier, whether an API surface is confidential, whether publishing
a protocol analysis invites a complaint.

## Refreshing the public repository

`scripts/export-public.sh` is the refresh mechanism, not a one-shot. It rebuilds
the public tree from the allowlist on every run, so additions, edits, and
**removals** all propagate. Removing a source from `publicSources` and
re-running deletes its files from the public branch.

The script refuses to run against a dirty worktree, copies only git-tracked
content via `git archive`, and aborts before committing if the scanner finds
anything.
