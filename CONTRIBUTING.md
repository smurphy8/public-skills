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

## Versioning a skill family

A skill family is a provider directory: `onping/`, `ramp/`, `agents/`, and so on.
A versioned family carries **one** `CHANGELOG.md` at its root, for example
`onping/CHANGELOG.md`, and follows [semver](https://semver.org/). A changelog per
skill is too granular to be useful: most changes touch several skills of a family
at once, and a reader wants one place to see what moved and when.

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

**A family changelog does not install with its skills.** The bundler and
`scripts/install.sh` copy `<provider>/skills/<id>/` and nothing above it, so read
the family changelog in the repository. Each entry names the skills it touches.

**`CHANGELOG.md` is authoritative and `plugin.json` mirrors it.** A family with
plugin manifests bumps them to match the changelog. `explainer` predates the
family rule. It is a one-skill family, so its changelog sits in the skill
directory, `agents/skills/explainer/CHANGELOG.md`, and both `agents/` manifests
mirror it.

Do not add a `version:` key to `SKILL.md` frontmatter. Frontmatter is `name`,
`description`, and optionally `allowed-tools`. A third copy of the version would
sit in the file most certain to be read while being the easiest to forget.

**A documentation-only change does not bump the version.** A bump asserts that
a skill in the family changed. If no rule, script, template, asset, or output
moved, leave the number alone.

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

## The OnPing target: `plow-technologies/onping-skills`

The OnPing skills are published separately, to
[`plow-technologies/onping-skills`](https://github.com/plow-technologies/onping-skills),
by `scripts/export-onping-skills.sh`. The guardrails are the same; three things
differ.

- **Selection is per skill.** `nix/onping-skills-allowlist.nix` lists every
  OnPing skill ID as included or excluded. `nix flake check` fails when a skill
  is in neither list, so a new skill cannot reach the target without a decision.
  It also fails when an included skill imports a `_`-prefixed helper that is not
  included.
- **The target's `main` is protected; delivery is by pull request.** An export
  commit is built on top of the target's own `main`, fetched into
  `refs/export/onping-skills/main`, not on an orphan branch. The target's
  history consists only of exports, so this adds no private ancestry, and it
  gives GitHub a shared history to open a pull request against. The exporter
  and the hook both refuse a commit that shares history with this repository's
  `main`.
- **The layout is flat.** Every included skill lands at `onping/skills/<id>/`,
  including the nested `lj-restore-*` group and `onping-line-graph`, so the
  scripts' sibling-helper imports keep working.

```bash
./scripts/export-onping-skills.sh --dry-run    # evaluate and fetch; build nothing
./scripts/export-onping-skills.sh              # commit on local branch export/<sha>; push nothing
./scripts/export-onping-skills.sh --push       # push export/<sha> and open a pull request
./scripts/export-onping-skills.sh --bootstrap  # once, while the target has no main: README only
```

A run where the target's `main` already matches produces no commit and no pull
request. While an export pull request is open, `--push` adds the new export
commit to that pull request's branch instead of opening a second one.

Every OnPing skill that can change live data starts its `SKILL.md`, directly
under the title, with a standard warning: what it changes, whether that can be
undone, and exactly how its script gates the change. Add one to any new
mutating skill, and never claim a gate the script does not implement.

The bootstrap commit holds `README.md` alone, so every skill enters the
protected `main` through a pull request. Each pull request must pass two
checks that the export itself ships in `.github/workflows/checks.yml`:
`scan` runs `scripts/scan-public.sh`, and `flake-check` runs `nix flake check`
and builds the bundle.

The scanner's marker list, `scripts/scan-patterns.tsv`, is never exported: it
names the strings it exists to keep out. CI receives it as a repository
secret, and reports matches without printing a pattern. Refresh the secret
whenever the list changes:

```bash
gh secret set SCAN_PATTERNS --repo plow-technologies/onping-skills < scripts/scan-patterns.tsv
```

After the bootstrap, protect the target's `main` once:

```bash
gh api -X PUT repos/plow-technologies/onping-skills/branches/main/protection \
  --input - <<'JSON'
{"required_status_checks": {"strict": true, "contexts": ["scan", "flake-check"]},
 "enforce_admins": true,
 "required_pull_request_reviews": {"required_approving_review_count": 0},
 "restrictions": null,
 "allow_force_pushes": false,
 "allow_deletions": false}
JSON
```

The approval count is 0 because GitHub does not let an author approve their
own pull request; with a second maintainer, raise it to 1.

The `pre-push` hook guards this target by URL, like the other one: it
accepts only `export/*` branches (and `main` only while creating it), rejects
paths outside the allowlist's `publishedPaths`, and runs the scanner. Its limits
are the ones stated above.

Changes made directly in `onping-skills` are reverted by the next export. Port
an accepted change here first.
