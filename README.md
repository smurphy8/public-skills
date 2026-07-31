# Agent skills

Portable agent skills, installed declaratively with Nix.

Each skill is a directory containing a `SKILL.md` and whatever scripts, assets,
and references it needs. Skills follow the [agentskills.io](https://agentskills.io/home)
convention, so they work with any tool that reads `SKILL.md` — Claude Code,
Codex, and other agent runtimes.

This repository is a **published subset** of a larger private catalog. Skills
reach it only after a review against [`docs/public-readiness.md`](docs/public-readiness.md).

## Skills

### explainer

Turns a topic, question, or set of findings into a single self-contained HTML
document in a flat editorial style: serif body text, no CDN, no tracking,
print-friendly. Supports Mermaid diagrams, Vega-Lite charts, and native MathML,
all inlined offline. Prose follows a language standard derived from
ASD-STE100 Simplified Technical English.

- Script: `agents/skills/explainer/scripts/new_explainer.py`
- Create: `--title <t> --subtitle <s> [--from-file <path>] [--output <dir>]`
- Lint an existing file: `--validate <path>`
- Output: one `.html` file under `$TMPDIR/explainers/` by default

## Install

Skills sync into agent skill roots via [`Kyure-A/agent-skills-nix`](https://github.com/Kyure-A/agent-skills-nix).
The flake discovers every `SKILL.md` under each `<provider>/skills/` directory
and copy-tree-syncs the catalog.

**Do not symlink this repository into an agent skill root.** Tool-discovery
walkers reject or silently skip symlinked directories.

### Prerequisites

- Nix with flakes enabled (`experimental-features = nix-command flakes`).
- Home Manager, for the home-level install path.

### Try it without installing

```bash
nix run github:smurphy8/public-skills#skills-list
```

### Home-level install (Home Manager)

Add this repository as a flake input and import its module:

```nix
{
  inputs.skills.url = "github:smurphy8/public-skills";

  outputs = { self, nixpkgs, home-manager, skills, ... }: {
    # inside your home configuration:
    imports = [ skills.homeManagerModules.default ];
  };
}
```

Two targets are enabled by default:

| Target   | Destination                                    | Sync mode   |
|----------|------------------------------------------------|-------------|
| `claude` | `${CLAUDE_CONFIG_DIR:-$HOME/.claude}/skills`   | `copy-tree` |
| `agents` | `$HOME/.agents/skills`                         | `copy-tree` |

Activate with whatever command your setup uses — `home-manager switch`, or
`darwin-rebuild switch --flake <your-config>#<host>` on nix-darwin.

After activation every skill folder is a real directory containing a real
`SKILL.md`, never a symlink.

#### Optional `~/.codex/skills` target

`~/.agents/skills` is the OpenAI agents convention and is always enabled. The
legacy `~/.codex/skills` root is off by default. Enable it only if your Codex
CLI version is verified to scan that path:

```nix
programs.agent-skills.codexLegacyHomeRoot = true;
```

### Project-local install (opt-in)

To install into a single project's `.claude/skills` and `.agents/skills`:

```bash
cd path/to/your/project
nix run github:smurphy8/public-skills#skills-install-local
```

Register a registry alias to shorten that:

```bash
nix registry add skills github:smurphy8/public-skills
nix run skills#skills-install-local
```

To refresh skills on `nix develop` entry, wire the shell hook into your
project's `flake.nix`:

```nix
inputs.skills.url = "github:smurphy8/public-skills";
# inside your devShell:
shellHook = inputs.skills.devShells.${system}.default.shellHook;
```

Project scope and home scope are isolated. A Home Manager activation never
touches a project's `.claude/skills`, and a project sync never touches the home
roots.

### Managed-destination ownership

Every `copy-tree` destination is **Nix-owned**. Files placed there by other
means are unsupported and `rsync --delete` removes them on the next sync. To
add a skill of your own, fork this repository and add it to the catalog.

### Migrating from a symlinked install

If you previously symlinked a skills directory into an agent root, remove those
symlinks before the first `copy-tree` sync. Find them:

```bash
find ~/.claude/skills ~/.agents/skills ~/.codex/skills \
  -maxdepth 1 -type l -print 2>/dev/null
```

Remove only confirmed legacy symlinks. Do not delete real directories holding
your own content.

## Repository layout

```
agents/
  skills/
    explainer/          SKILL.md, scripts/, assets/, references/
nix/
  sources.nix           provider directories the walker scans
  public-allowlist.nix  what may be published
  home.nix              Home Manager module
flake.nix
```

Skill folder names are globally unique across providers, lowercase with hyphens.

## Contributing

See [`CONTRIBUTING.md`](CONTRIBUTING.md). Ground rules for skill design are in
[`AGENTS.md`](AGENTS.md).

## License

MIT — see [`LICENSE`](LICENSE).

This repository redistributes vendored third-party JavaScript (Mermaid,
Vega, Vega-Lite, Vega-Embed) under separate terms. See
[`THIRD-PARTY-NOTICES.md`](THIRD-PARTY-NOTICES.md).
