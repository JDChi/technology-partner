#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from datetime import date, datetime
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
KNOWLEDGE_DIRNAME = "knowledge"
INDEX_FILENAME = "index.json"
CREATABLE_ENTRY_TYPES = ("pattern", "scenario", "workflow", "decision")
INDEXED_ENTRY_TYPES = ("architecture", "pattern", "scenario", "workflow", "decision")
TYPE_DIRECTORIES = {
    "architecture": "architecture",
    "pattern": "patterns",
    "scenario": "scenarios",
    "workflow": "workflows",
    "decision": "decisions",
}
TYPE_TEMPLATES = {
    "pattern": "knowledge-entry-template.md",
    "scenario": "knowledge-entry-template.md",
    "workflow": "knowledge-entry-template.md",
    "decision": "decision-record-template.md",
}
DATE_PREFIX_RE = re.compile(r"^(?P<date>\d{4}-\d{2}-\d{2})-(?P<slug>.+)$")


def slugify(title: str) -> str:
    normalized = unicodedata.normalize("NFKD", title)
    ascii_only = normalized.encode("ascii", "ignore").decode("ascii")
    tokens = re.findall(r"[a-zA-Z0-9]+", ascii_only.lower())
    if tokens:
        return "-".join(tokens)

    cleaned = re.sub(r"[^\w\s-]", " ", title, flags=re.UNICODE).strip().lower()
    cleaned = re.sub(r"[-\s]+", "-", cleaned)
    if cleaned:
        return cleaned

    raise ValueError(f"Cannot derive a slug from title: {title!r}")


def repo_root(root: Path | None = None) -> Path:
    return Path(root) if root is not None else REPO_ROOT


def knowledge_root(root: Path | None = None) -> Path:
    return repo_root(root) / KNOWLEDGE_DIRNAME


def template_path(root: Path, entry_type: str) -> Path:
    template_name = TYPE_TEMPLATES[entry_type]
    path = root / "templates" / template_name
    if not path.exists():
        raise FileNotFoundError(f"Template not found: {path}")
    return path


def destination_path(root: Path, entry_type: str, title: str) -> Path:
    slug = slugify(title)
    base_directory = knowledge_root(root) / TYPE_DIRECTORIES[entry_type]
    base_directory.mkdir(parents=True, exist_ok=True)

    if entry_type == "decision":
        filename = f"{date.today().isoformat()}-{slug}.md"
    else:
        filename = f"{slug}.md"
    return base_directory / filename


def render_template(root: Path, entry_type: str, title: str) -> str:
    template = template_path(root, entry_type).read_text(encoding="utf-8")
    if entry_type == "decision":
        rendered = template.replace("# Decision Title", f"# {title}", 1)
        return rendered.replace("- YYYY-MM-DD", f"- {date.today().isoformat()}", 1)

    return template.replace("# Title", f"# {title}", 1)


def extract_title(path: Path) -> str:
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return path.stem


def entry_created_at(path: Path) -> str:
    return date.fromtimestamp(path.stat().st_mtime).isoformat()


def build_entry(entry_type: str, path: Path, base_root: Path) -> dict[str, str]:
    relative_path = path.relative_to(knowledge_root(base_root)).as_posix()
    slug = path.stem.lower()
    entry = {
        "type": entry_type,
        "path": relative_path,
        "title": extract_title(path),
        "slug": slug,
        "created_at": entry_created_at(path),
    }

    if entry_type == "decision":
        match = DATE_PREFIX_RE.match(path.stem)
        if match:
            entry["date"] = match.group("date")
            entry["slug"] = match.group("slug")

    return entry


def collect_entries(root: Path) -> dict[str, list[dict[str, str]]]:
    entries = {entry_type: [] for entry_type in INDEXED_ENTRY_TYPES}
    base = knowledge_root(root)

    for entry_type, directory_name in TYPE_DIRECTORIES.items():
        directory = base / directory_name
        if not directory.exists():
            continue

        for path in sorted(directory.glob("*.md")):
            entries[entry_type].append(build_entry(entry_type, path, root))

    return entries


def write_index(root: Path, entries: dict[str, list[dict[str, str]]]) -> Path:
    index_path = knowledge_root(root) / INDEX_FILENAME
    payload = {
        "generated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "entries": entries,
    }
    index_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return index_path


def sync_index(root: Path | None = None) -> Path:
    current_root = repo_root(root)
    entries = collect_entries(current_root)
    return write_index(current_root, entries)


def create_entry(root: Path | None, entry_type: str, title: str) -> Path:
    if entry_type not in CREATABLE_ENTRY_TYPES:
        raise ValueError(f"Unsupported entry type: {entry_type}")

    current_root = repo_root(root)
    target_path = destination_path(current_root, entry_type, title)
    if target_path.exists():
        raise FileExistsError(f"Target file already exists: {target_path}")

    target_path.write_text(render_template(current_root, entry_type, title), encoding="utf-8")
    sync_index(current_root)
    return target_path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Create knowledge entries and keep knowledge/index.json in sync."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    create_parser = subparsers.add_parser("create", help="Create a knowledge entry and sync index.json")
    create_parser.add_argument("type", choices=CREATABLE_ENTRY_TYPES)
    create_parser.add_argument("title")

    subparsers.add_parser("sync", help="Rebuild knowledge/index.json from the filesystem")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        if args.command == "create":
            created_path = create_entry(None, args.type, args.title)
            index_path = knowledge_root() / INDEX_FILENAME
            print(f"Created {created_path.relative_to(REPO_ROOT).as_posix()}")
            print(f"Synced {index_path.relative_to(REPO_ROOT).as_posix()}")
            return 0

        index_path = sync_index()
        total_entries = sum(len(entries) for entries in collect_entries(repo_root()).values())
        print(f"Synced {index_path.relative_to(REPO_ROOT).as_posix()} with {total_entries} entries")
        return 0
    except Exception as exc:  # pragma: no cover - exercised through CLI usage.
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
