#!/usr/bin/env python3
"""Create and validate temporary HTML explainers."""

from __future__ import annotations

import argparse
import html
import re
import secrets
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path


CONTENT_MARKER = "<!-- EXPLAINER_CONTENT -->"
REQUIRED_SERIF_STACK = (
    'Georgia, "Times New Roman", "Iowan Old Style", "Palatino Linotype", serif'
)
RESIDENCY_MARKER = ".explainer-root"

ALLOWED_INLINE_SCRIPTS = ("mermaid", "mermaid-init", "vega-lite", "vega-lite-init")

VEGA_INIT_JS = (
    "document.querySelectorAll('pre.vega-lite').forEach(function(pre){"
    "try{var spec=JSON.parse(pre.dataset.spec||pre.textContent);"
    "var container=document.createElement('div');"
    "container.style.display='block';container.style.width='100%';"
    "pre.after(container);"
    "vegaEmbed(container,spec,{renderer:'svg',actions:false})"
    ".then(function(){pre.classList.add('rendered');})"
    ".catch(function(e){console.error('vega-lite render failed:',e);});}"
    "catch(e){console.error('vega-lite render failed:',e);}});"
)


def temporary_root() -> Path:
    return Path(tempfile.gettempdir()).resolve() / "explainers"


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return (slug[:64].rstrip("-") or "explainer")


def is_beneath(path: Path, directory: Path) -> bool:
    try:
        path.relative_to(directory)
    except ValueError:
        return False
    return True


def find_residency_root(path: Path) -> Path | None:
    """Walk upward from path.parent looking for an `.explainer-root` sentinel.

    Returns the directory containing the sentinel, or None if not found before
    reaching the filesystem root.
    """
    parent = path.parent
    while True:
        if (parent / RESIDENCY_MARKER).is_file():
            return parent
        if parent.parent == parent:
            return None
        parent = parent.parent


def _read_asset(name: str) -> str:
    """Read a vendored asset file from ../assets/<name>."""
    asset_path = Path(__file__).resolve().parent.parent / "assets" / name
    return asset_path.read_text(encoding="utf-8")


def _resolve_source_files(raw_paths: list[str]) -> list[Path]:
    """Resolve each --from-file argument to an absolute Path.

    Fails fast with a stderr message and SystemExit(1) if any path does not
    exist. The script never opens or reads the file's content — this is a
    pointer-only resolution.
    """
    resolved: list[Path] = []
    for raw in raw_paths:
        candidate = Path(raw).expanduser().resolve()
        if not candidate.is_file():
            print(
                f"error: --from-file path does not exist: {candidate}",
                file=sys.stderr,
            )
            raise SystemExit(1)
        resolved.append(candidate)
    return resolved


def create_document(
    title: str,
    subtitle: str,
    *,
    output_dir: Path | None = None,
    from_files: list[Path] | None = None,
) -> Path:
    template_path = Path(__file__).resolve().parent.parent / "assets" / "template.html"
    template = template_path.read_text(encoding="utf-8")

    now = datetime.now(timezone.utc)
    suffix = secrets.token_hex(3)
    if output_dir is None:
        residency_root = temporary_root()
    else:
        residency_root = output_dir
    residency_root.mkdir(parents=True, exist_ok=True)

    if output_dir is not None:
        # Idempotently write the residency sentinel so --validate can locate
        # the accepted root later without needing the flag repeated.
        marker = residency_root / RESIDENCY_MARKER
        if not marker.exists():
            marker.open("w").close()

    output_path = residency_root / (
        f"{slugify(title)}-{now.strftime('%Y%m%d-%H%M%S')}-{suffix}.html"
    )
    created_at = f"{now.strftime('%B')} {now.day}, {now.year} · {now:%H:%M} UTC"

    # Order matters: substitute user-provided text (with HTML escape) first,
    # then splice in the vendored JS payloads via literal .replace() calls.
    # .format() cannot be used — Vega's minified JS contains `{` characters
    # which would break format-string parsing.
    rendered = (
        template.replace("{{TITLE}}", html.escape(title))
        .replace("{{SUBTITLE}}", html.escape(subtitle))
        .replace("{{CREATED_AT}}", created_at)
    )

    mermaid_js = _read_asset("mermaid.min.js")
    vega_js = "\n".join(
        (
            _read_asset("vega.min.js"),
            _read_asset("vega-lite.min.js"),
            _read_asset("vega-embed.min.js"),
        )
    )

    rendered = (
        rendered.replace("/*!MERMAID*/", mermaid_js)
        .replace("/*!VEGA*/", vega_js)
        .replace("/*!VEGA_INIT*/", VEGA_INIT_JS)
    )

    if from_files:
        # Inject one <!-- SOURCE: <abs> --> per file, in order, immediately
        # above the content marker. Do NOT read or embed the file itself.
        source_lines = "".join(
            f"      <!-- SOURCE: {p} -->\n" for p in from_files
        )
        rendered = rendered.replace(
            CONTENT_MARKER, source_lines + f"      {CONTENT_MARKER}", 1
        )

    output_path.write_text(rendered, encoding="utf-8")
    return output_path.resolve()


_ALLOWED_SCRIPT_RE = re.compile(
    r'<script\s+data-inline="([^"]*)"\s*>(.*?)</script>',
    flags=re.IGNORECASE | re.DOTALL,
)
_ANY_SCRIPT_RE = re.compile(r"<script(?:\s|>)", flags=re.IGNORECASE)
_SCRIPT_SRC_RE = re.compile(r"<script[^>]+\bsrc\s*=", flags=re.IGNORECASE)
_STYLESHEET_RE = re.compile(
    r"<link[^>]+rel=[\"']?stylesheet", flags=re.IGNORECASE
)
_MATH_RE = re.compile(r"<math\b([^>]*)>", flags=re.IGNORECASE)
_PLACEHOLDER_RE = re.compile(r"\{\{[A-Z_]+\}\}")


def _check_script_allowlist(content: str) -> tuple[list[str], str]:
    """Enforce the four-block inline-script allowlist.

    Returns (errors, stripped_content). `stripped_content` is a working copy
    with every allowed <script data-inline="..."> block removed, so the caller
    can re-scan for any remaining <script occurrences.
    """
    errors: list[str] = []
    seen: dict[str, int] = {}
    matches = list(_ALLOWED_SCRIPT_RE.finditer(content))

    for m in matches:
        name = m.group(1)
        if name not in ALLOWED_INLINE_SCRIPTS:
            errors.append(f"unknown data-inline value: `{name}`")
        seen[name] = seen.get(name, 0) + 1

    for name, count in seen.items():
        if name in ALLOWED_INLINE_SCRIPTS and count > 1:
            errors.append(f"duplicate data-inline value: `{name}`")

    for required in ALLOWED_INLINE_SCRIPTS:
        if seen.get(required, 0) == 0:
            errors.append(f"missing required inline script `{required}`")

    if len(matches) != 4:
        errors.append(
            f"expected exactly 4 inline <script data-inline> blocks, found {len(matches)}"
        )

    # Build the stripped copy for the leftover-script sweep.
    stripped = _ALLOWED_SCRIPT_RE.sub("", content)
    return errors, stripped


def validate_document(raw_path: str) -> tuple[list[str], list[str]]:
    """Validate an existing explainer file.

    Returns (errors, warnings). Warnings do not cause a nonzero exit.
    """
    path = Path(raw_path).expanduser().resolve()
    errors: list[str] = []
    warnings: list[str] = []

    if path.suffix.lower() != ".html":
        errors.append("file does not have an .html extension")
    if not path.is_file():
        errors.append("file does not exist")
        return errors, warnings

    # Residency: prefer a caller-declared root via .explainer-root sentinel,
    # otherwise fall back to the default $TMPDIR/explainers/ rule.
    declared_root = find_residency_root(path)
    if declared_root is None:
        default_root = temporary_root()
        if not is_beneath(path, default_root):
            errors.append(
                "file is outside the temporary explainer directory "
                f"({default_root}) and no `.explainer-root` sentinel was found "
                "on any ancestor directory"
            )

    content = path.read_text(encoding="utf-8")

    if CONTENT_MARKER in content:
        errors.append("explainer content marker has not been replaced")
    if REQUIRED_SERIF_STACK not in content:
        errors.append("required serif font stack is missing")
    if "<main" not in content or "<article" not in content:
        errors.append("required document structure is missing")

    # External script src is always rejected (belt-and-braces: technically the
    # allowlist regex requires the exact `data-inline="..."` shape so an
    # attribute-order swap that puts src first wouldn't be captured as an
    # allowed block anyway, but check the raw content explicitly).
    if _SCRIPT_SRC_RE.search(content):
        errors.append("external scripts are not allowed (src= attribute)")

    # Allowlist enforcement + leftover sweep. All subsequent content-level
    # checks that would false-positive on vendored JS (curly-brace pairs, the
    # <math substring) run against the stripped copy.
    allowlist_errors, stripped = _check_script_allowlist(content)
    errors.extend(allowlist_errors)
    if _ANY_SCRIPT_RE.search(stripped):
        errors.append("disallowed script block outside allowlist")

    if _PLACEHOLDER_RE.search(stripped):
        errors.append("template placeholders remain")

    if _STYLESHEET_RE.search(content):
        errors.append("external stylesheets are not allowed")

    # MathML warning (not an error): every <math> element should carry the
    # MathML xmlns for cross-browser reliability. Scan the stripped copy so
    # incidental substrings inside the vendored JS bundles (e.g. `<Math.abs`)
    # don't trigger false positives.
    for m in _MATH_RE.finditer(stripped):
        attrs = m.group(1) or ""
        if "http://www.w3.org/1998/Math/MathML" not in attrs:
            warnings.append(
                "<math> element missing "
                'xmlns="http://www.w3.org/1998/Math/MathML"'
            )

    return errors, warnings


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create or validate a temporary serif HTML explainer."
    )
    parser.add_argument("--title", help="Document title")
    parser.add_argument("--subtitle", default="", help="One-sentence deck")
    parser.add_argument(
        "--from-file",
        dest="from_file",
        action="append",
        default=None,
        metavar="PATH",
        help=(
            "Absolute or relative path to a source doc; the resolved path is "
            "recorded inside the rendered HTML as a <!-- SOURCE: ... --> "
            "comment for the invoking agent to consume. Repeatable."
        ),
    )
    parser.add_argument(
        "--output",
        metavar="DIR",
        help=(
            "Persist the rendered file under DIR instead of the default temp "
            "directory. Writes a `.explainer-root` sentinel so `--validate` "
            "will accept files under that directory."
        ),
    )
    parser.add_argument(
        "--validate", metavar="PATH", help="Validate an existing file"
    )
    args = parser.parse_args()

    if bool(args.validate) == bool(args.title):
        parser.error("provide exactly one of --title or --validate")

    if args.validate:
        if args.from_file:
            parser.error("--from-file is only valid with --title")
        if args.output:
            parser.error("--output is only valid with --title")
        if args.subtitle:
            parser.error("--subtitle is only valid with --title")

    return args


def main() -> int:
    args = parse_args()
    if args.validate:
        errors, warnings = validate_document(args.validate)
        for warning in warnings:
            print(f"warning: {warning}", file=sys.stderr)
        if errors:
            for error in errors:
                print(f"error: {error}", file=sys.stderr)
            return 1
        print(Path(args.validate).expanduser().resolve())
        return 0

    output_dir = (
        Path(args.output).expanduser().resolve() if args.output else None
    )
    from_files = _resolve_source_files(args.from_file or [])

    print(
        create_document(
            args.title,
            args.subtitle,
            output_dir=output_dir,
            from_files=from_files,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
