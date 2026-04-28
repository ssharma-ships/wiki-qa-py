# Core engine. run_agent() is the agentic loop: calls the Claude API, handles
# tool dispatch, enforces the 6-search cap, records the full trace, and returns
# a dict. No CLI — everything else calls into this.

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import anthropic
from dotenv import load_dotenv

from tools import SEARCH_WIKIPEDIA_TOOL
from wikipedia_client import search_wikipedia

load_dotenv()

DEFAULT_MODEL = "claude-sonnet-4-6"
MAX_SEARCHES = 6
MAX_AGENT_TURNS = 10
MAX_TOKENS = 2048

_client = anthropic.Anthropic()


def run_agent(
    question: str,
    system_prompt: str,
    model: str = DEFAULT_MODEL,
    log_path: Any = None,
    prompt_version: str = "unknown",
) -> dict:
    messages = [{"role": "user", "content": question}]
    trace = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "model": model,
        "prompt_version": prompt_version,
        "question": question,
        "system_prompt": system_prompt,
        "tool_calls": [],
        "search_count": 0,
        "final_answer": None,
        "stop_reason": None,
    }

    for _ in range(MAX_AGENT_TURNS):
        resp = _client.messages.create(
            model=model,
            max_tokens=MAX_TOKENS,
            system=system_prompt,
            tools=[SEARCH_WIKIPEDIA_TOOL],
            messages=messages,
        )

        messages.append({
            "role": "assistant",
            "content": [b.model_dump() for b in resp.content],
        })

        if resp.stop_reason == "end_turn":
            trace["final_answer"] = "\n".join(
                b.text for b in resp.content if b.type == "text"
            )
            trace["stop_reason"] = "end_turn"
            break

        if resp.stop_reason != "tool_use":
            trace["stop_reason"] = f"unexpected:{resp.stop_reason}"
            break

        tool_results = []
        for block in resp.content:
            if block.type != "tool_use":
                continue

            if block.name != "search_wikipedia":
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": json.dumps({"error": f"Unknown tool: {block.name}"}),
                    "is_error": True,
                })
                continue

            if trace["search_count"] >= MAX_SEARCHES:
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": json.dumps({
                        "error": (
                            "Search limit reached (6 searches max). "
                            "Provide a final answer based on evidence already "
                            "gathered, or state that the available evidence is insufficient."
                        )
                    }),
                })
                trace["tool_calls"].append({
                    "tool_use_id": block.id,
                    "query": block.input.get("query"),
                    "capped": True,
                })
                continue

            query = block.input.get("query", "")
            result = search_wikipedia(query)
            trace["search_count"] += 1
            trace["tool_calls"].append({
                "tool_use_id": block.id,
                "query": query,
                "result": result,
                "capped": False,
            })
            tool_results.append({
                "type": "tool_result",
                "tool_use_id": block.id,
                "content": json.dumps(result),
            })

        messages.append({"role": "user", "content": tool_results})
    else:
        trace["stop_reason"] = "max_agent_turns_reached"

    if log_path:
        path = Path(log_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(trace, indent=2, default=str), encoding="utf-8")

    return trace
