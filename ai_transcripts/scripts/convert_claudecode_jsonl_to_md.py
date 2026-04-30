#!/usr/bin/env python3
"""Convert Claude Code JSONL transcripts to readable Markdown.

Reads every .jsonl file under INPUT_DIR, writes one .md per file to OUTPUT_DIR.
- Preserves user, assistant, and tool turns
- Renders tool calls and tool results as fenced code blocks
- Skips thinking blocks, metadata lines, and attachment noise
- Truncates tool results longer than TOOL_RESULT_MAX chars
- Strips <local-command-caveat> boilerplate from user messages
- Skips malformed JSON lines silently
"""

import json
import os
import re
import glob
from pathlib import Path

INPUT_DIR = Path("ai_transcripts/raw/claudecode/raw_jsonl")
OUTPUT_DIR = Path("ai_transcripts/raw/claudecode/raw_md")
TOOL_RESULT_MAX = 2000

# Types that carry no readable content
SKIP_TYPES = {
    "permission-mode",
    "file-history-snapshot",
    "last-prompt",
    "attachment",
}


def clean_user_text(text: str) -> str:
    """Strip noise tags from user message text."""
    # Remove caveat block entirely (it's a system warning, not user content)
    text = re.sub(
        r"<local-command-caveat>.*?</local-command-caveat>",
        "",
        text,
        flags=re.DOTALL,
    )
    # Remove <command-message> (redundant with command-name + args)
    text = re.sub(r"<command-message>.*?</command-message>", "", text, flags=re.DOTALL)
    # Unwrap remaining known tags, keeping their inner text
    text = re.sub(r"<([a-zA-Z_-]+)>(.*?)</\1>", r"\2", text, flags=re.DOTALL)
    # Collapse excess blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def truncate(text: str) -> str:
    if len(text) <= TOOL_RESULT_MAX:
        return text
    surplus = len(text) - TOOL_RESULT_MAX
    return text[:TOOL_RESULT_MAX] + f"\n\n[... {surplus} chars truncated]"


def render_assistant_item(item: dict) -> str | None:
    kind = item.get("type")
    if kind == "thinking":
        return None
    if kind == "text":
        t = item.get("text", "").strip()
        return t if t else None
    if kind == "tool_use":
        name = item.get("name", "unknown_tool")
        inp = json.dumps(item.get("input", {}), indent=2, ensure_ascii=False)
        return f"**Tool call — `{name}`**\n```json\n{inp}\n```"
    return None


def render_tool_result(item: dict) -> str:
    raw = item.get("content", "")
    if isinstance(raw, list):
        parts = []
        for c in raw:
            if isinstance(c, dict) and c.get("type") == "text":
                parts.append(c.get("text", ""))
            elif isinstance(c, str):
                parts.append(c)
        raw = "\n".join(parts)
    raw = str(raw)
    raw = truncate(raw)
    return f"**Tool result:**\n```\n{raw}\n```"


def render_user_message(msg: dict) -> str | None:
    content = msg.get("content", "")
    parts = []

    if isinstance(content, str):
        cleaned = clean_user_text(content)
        if cleaned:
            parts.append(cleaned)

    elif isinstance(content, list):
        for item in content:
            if not isinstance(item, dict):
                continue
            kind = item.get("type")
            if kind == "text":
                cleaned = clean_user_text(item.get("text", ""))
                if cleaned:
                    parts.append(cleaned)
            elif kind == "tool_result":
                parts.append(render_tool_result(item))

    if not parts:
        return None
    return "\n\n".join(parts)


def render_assistant_message(msg: dict) -> str | None:
    content = msg.get("content", "")
    parts = []

    if isinstance(content, list):
        for item in content:
            rendered = render_assistant_item(item)
            if rendered:
                parts.append(rendered)
    elif isinstance(content, str):
        t = content.strip()
        if t:
            parts.append(t)

    if not parts:
        return None
    return "\n\n".join(parts)


def convert_session(jsonl_path: Path) -> str:
    turns = []

    with open(jsonl_path, encoding="utf-8", errors="replace") as fh:
        for raw_line in fh:
            raw_line = raw_line.strip()
            if not raw_line:
                continue
            try:
                obj = json.loads(raw_line)
            except json.JSONDecodeError:
                continue

            if obj.get("isSidechain"):
                continue

            msg_type = obj.get("type")
            if msg_type in SKIP_TYPES:
                continue
            if msg_type not in ("user", "assistant"):
                continue

            msg = obj.get("message", {})
            ts = obj.get("timestamp", "")

            if msg_type == "user":
                body = render_user_message(msg)
                if body:
                    turns.append(("User", ts, body))

            elif msg_type == "assistant":
                body = render_assistant_message(msg)
                if body:
                    turns.append(("Assistant", ts, body))

    if not turns:
        return f"# Session: {jsonl_path.stem}\n\n*(no readable content)*\n"

    blocks = [f"# Session: {jsonl_path.stem}\n"]
    for role, ts, body in turns:
        ts_short = ts[:19].replace("T", " ") if ts else ""
        heading = f"## {role}" + (f"  `{ts_short}`" if ts_short else "")
        blocks.append(f"{heading}\n\n{body}")

    return "\n\n---\n\n".join(blocks) + "\n"


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    jsonl_files = sorted(INPUT_DIR.glob("*.jsonl"))
    if not jsonl_files:
        print(f"No .jsonl files found in {INPUT_DIR}")
        return

    print(f"Converting {len(jsonl_files)} sessions -> {OUTPUT_DIR}/")
    for jf in jsonl_files:
        md = convert_session(jf)
        out = OUTPUT_DIR / (jf.stem + ".md")
        out.write_text(md, encoding="utf-8")
        word_count = len(md.split())
        print(f"  {jf.name}  ->  {out.name}  ({word_count} words)")

    print(f"\nDone.")


if __name__ == "__main__":
    main()
