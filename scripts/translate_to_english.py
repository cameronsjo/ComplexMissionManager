#!/usr/bin/env python3
"""Translate repository content to polished English using OpenAI Codex.

The utility scans the provided files and directories, translating segments that
contain CJK characters while skipping fenced code blocks. Each translated block
is processed by Codex with instructions to produce natural, fluent English so
that awkward literal phrasing is automatically refined. The script requires the
``OPENAI_API_KEY`` environment variable and is designed for automation inside
GitHub Actions or local use.
"""

from __future__ import annotations

import argparse
import logging
import os
import re
import sys
import textwrap
import time
from pathlib import Path
from typing import Iterable, List

try:
    import openai
except ImportError as exc:  # pragma: no cover - dependency missing during import
    raise SystemExit(
        "openai must be installed. Install with 'pip install \"openai>=0.28,<1\"'."
    ) from exc

CJK_RE = re.compile(r"[\u3400-\u9fff]")


def contains_cjk(text: str) -> bool:
    """Return True when the provided text includes any CJK characters."""

    return bool(CJK_RE.search(text))


def discover_files(paths: Iterable[Path], extensions: Iterable[str]) -> List[Path]:
    """Discover files under the provided paths that match the allowed extensions."""

    matched: List[Path] = []
    for path in paths:
        if path.is_dir():
            for candidate in sorted(path.rglob("*")):
                if candidate.is_file() and candidate.suffix in extensions:
                    matched.append(candidate)
        elif path.is_file() and path.suffix in extensions:
            matched.append(path)
    return matched


def translate_with_codex(prompt_text: str, *, temperature: float = 0.1) -> str:
    """Translate and polish ``prompt_text`` using Codex."""

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise SystemExit(
            "OPENAI_API_KEY environment variable is required to use Codex translation."
        )

    openai.api_key = api_key

    prompt = textwrap.dedent(
        f"""
        You are OpenAI Codex helping to maintain English documentation.
        Translate the following Markdown content to natural, polished English.
        Preserve the original structure, indentation, and inline formatting.
        Improve awkward literal phrasing so that the translation reads smoothly
        while keeping the original meaning intact.

        Source text:
        ---
        {prompt_text}
        ---

        Polished English translation:
        """
    ).strip()

    # Codex responses can occasionally include leading newlines; strip them.
    for attempt in range(5):
        try:
            response = openai.Completion.create(
                model="code-davinci-002",
                prompt=prompt,
                temperature=temperature,
                max_tokens=1024,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
            )
        except openai.error.OpenAIError as exc:  # pragma: no cover - network/runtime failures
            wait_time = 2**attempt
            logging.warning("Codex request failed (%s). Retrying in %s seconds.", exc, wait_time)
            time.sleep(wait_time)
            continue
        choice = response.get("choices", [{}])[0]
        text = choice.get("text", "").strip()
        if text:
            return text
    raise RuntimeError("Failed to obtain translation from Codex after multiple attempts.")


def translate_file(path: Path, dry_run: bool = False) -> bool:
    """Translate a single file. Returns True when the file was modified."""

    original_text = path.read_text(encoding="utf-8")
    lines = original_text.splitlines()
    translated_lines: List[str] = []
    in_code_block = False
    pending_block: List[str] = []

    def flush_pending() -> None:
        nonlocal modified
        if not pending_block:
            return
        source_text = "\n".join(pending_block)
        translation = translate_with_codex(source_text)
        translated_segment = translation.splitlines()
        if translated_segment != pending_block:
            modified = True
        translated_lines.extend(translated_segment)
        pending_block.clear()
    modified = False

    for index, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("```"):
            flush_pending()
            in_code_block = not in_code_block
            translated_lines.append(line)
            continue

        if not in_code_block and contains_cjk(line):
            pending_block.append(line)
        else:
            flush_pending()
            translated_lines.append(line)

    flush_pending()

    translated_text = "\n".join(translated_lines)
    if original_text.endswith("\n"):
        translated_text += "\n"

    if not dry_run and modified and translated_text != original_text:
        path.write_text(translated_text, encoding="utf-8")
    return modified and translated_text != original_text


def parse_args(argv: Iterable[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "paths",
        nargs="+",
        type=Path,
        help="Files or directories to translate.",
    )
    parser.add_argument(
        "--extensions",
        nargs="+",
        default=[".md", ".json", ".txt"],
        help="File extensions to include when traversing directories.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Run without writing modifications; exit status reflects pending changes.",
    )
    return parser.parse_args(list(argv))


def main(argv: Iterable[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    targets = discover_files(args.paths, args.extensions)

    any_changes = False
    for target in targets:
        if translate_file(target, dry_run=args.dry_run):
            logging.info("Translated %s", target)
            any_changes = True

    if args.dry_run and any_changes:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
