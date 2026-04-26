#!/usr/bin/env python3
"""
Score a saved QA log against eval_cases.yaml using an LLM judge.

Usage:
    python judge.py --log logs/v0_run1.json [--model MODEL]

Matches each eval case to a trace by question string (exact match).
Writes: observations/{log_stem}_judge.md
"""
import argparse
import json
import re
import sys
from pathlib import Path

import anthropic
import yaml
from dotenv import load_dotenv

load_dotenv()

EVAL_CASES_PATH = Path("eval_cases.yaml")
JUDGE_PROMPT_PATH = Path("eval/judge_prompt.txt")
SCORING_GUIDE_PATH = Path("eval/eval_and_scoring.md")
OBS_DIR = Path("observations")

DEFAULT_MODEL = "claude-sonnet-4-6"
JUDGE_MAX_TOKENS = 1500

DIM_KEYS = [
    "evidence_support",
    "honesty",
    "task_effectiveness",
    "correctness",
    "answer_quality",
]

_client = anthropic.Anthropic()


# ---------------------------------------------------------------------------
# Loading
# ---------------------------------------------------------------------------

def load_eval_cases() -> dict[str, dict]:
    data = yaml.safe_load(EVAL_CASES_PATH.read_text(encoding="utf-8"))
    return {c["case_id"]: c for c in data["cases"]}


def load_traces(log_path: Path) -> dict[str, dict]:
    """Return traces keyed by question string (last wins on duplicates)."""
    traces = json.loads(log_path.read_text(encoding="utf-8"))
    return {t["question"]: t for t in traces}


# ---------------------------------------------------------------------------
# Judge call
# ---------------------------------------------------------------------------

def build_trace_payload(trace: dict) -> dict:
    return {
        "question": trace["question"],
        "final_answer": trace.get("final_answer"),
        "tool_calls": [
            {
                "query": tc["query"],
                "result": tc.get("result"),
                "capped": tc.get("capped", False),
            }
            for tc in trace.get("tool_calls", [])
        ],
        "search_count": trace["search_count"],
        "stop_reason": trace["stop_reason"],
    }


def compose_user_message(scoring_guide: str, case: dict, trace: dict) -> str:
    case_yaml = yaml.dump(case, allow_unicode=True, default_flow_style=False).strip()
    trace_json = json.dumps(build_trace_payload(trace), indent=2, ensure_ascii=False)
    return (
        f"<scoring_guide>\n{scoring_guide}\n</scoring_guide>\n\n"
        f"<eval_case>\n{case_yaml}\n</eval_case>\n\n"
        f"<trace>\n{trace_json}\n</trace>"
    )


def call_judge(judge_prompt: str, user_message: str, model: str) -> dict:
    resp = _client.messages.create(
        model=model,
        max_tokens=JUDGE_MAX_TOKENS,
        system=judge_prompt,
        messages=[{"role": "user", "content": user_message}],
    )
    raw = resp.content[0].text.strip()
    raw = re.sub(r"^```(?:json)?\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw)
    return json.loads(raw)


# ---------------------------------------------------------------------------
# Markdown output
# ---------------------------------------------------------------------------

def build_judge_md(log_path: Path, results: list[dict], model: str) -> str:
    lines = [
        f"# Judge Results — {log_path.stem}",
        "",
        f"**Log:** `{log_path}`  ",
        f"**Judge model:** {model}  ",
        f"**Cases scored:** {len(results)}",
        "",
        "---",
        "",
        "## Summary",
        "",
        "| case_id | ES | HO | TE | CO | AQ | abstention | tags |",
        "|---------|----|----|----|----|----|------------|------|",
    ]

    for r in results:
        v = r["verdict"]
        s = v["scores"]
        scores_cols = " | ".join(str(s[k]) for k in DIM_KEYS)
        abst = "true" if v["abstention_appropriate"] else "false"
        tags = ", ".join(v["failure_tags"]) if v["failure_tags"] else "—"
        lines.append(f"| {v['case_id']} | {scores_cols} | {abst} | {tags} |")

    lines += ["", "---", ""]

    for r in results:
        case = r["case"]
        v = r["verdict"]

        lines += [
            f"## {v['case_id']}",
            "",
            f"**Question:** {case['question']}  ",
            f"**Evidence condition:** {case['evidence_condition']}  ",
            f"**Abstention appropriate:** {v['abstention_appropriate']}",
            "",
            "**Scores:**",
            "",
            "| Dimension | Score |",
            "|-----------|-------|",
        ]
        for k in DIM_KEYS:
            lines.append(f"| {k.replace('_', ' ').title()} | {v['scores'][k]} |")

        if v["failure_tags"]:
            lines += ["", f"**Failure tags:** {', '.join(v['failure_tags'])}"]

        rationales = v.get("rationales", {})
        non_null = [(k, rationales[k]) for k in DIM_KEYS if rationales.get(k)]
        if non_null:
            lines += ["", "**Rationales:**", ""]
            for k, rat in non_null:
                lines.append(f"*{k.replace('_', ' ').title()}*  ")
                lines.append(f"Issue: {rat.get('issue', '—')}  ")
                if rat.get("answer_span"):
                    lines.append(f'Answer span: "{rat["answer_span"]}"  ')
                if rat.get("evidence_span"):
                    lines.append(f'Evidence span: "{rat["evidence_span"]}"  ')
                lines.append("")

        lines += ["---", ""]

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Judge a saved QA log.")
    parser.add_argument("--log", required=True, type=Path, help="Path to log JSON file")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="Judge model")
    args = parser.parse_args()

    log_path: Path = args.log
    if not log_path.exists():
        sys.exit(f"Log file not found: {log_path}")

    judge_prompt = JUDGE_PROMPT_PATH.read_text(encoding="utf-8")
    scoring_guide = SCORING_GUIDE_PATH.read_text(encoding="utf-8")
    eval_cases = load_eval_cases()
    traces_by_question = load_traces(log_path)

    matched, skipped = [], []
    for case_id, case in eval_cases.items():
        trace = traces_by_question.get(case["question"])
        if trace is None:
            skipped.append(case_id)
        else:
            matched.append((case, trace))

    if skipped:
        print(f"No trace found for {len(skipped)} case(s): {', '.join(skipped)}")
    if not matched:
        sys.exit("No cases matched. Run the agent on the eval cases first.")

    results = []
    for case, trace in matched:
        case_id = case["case_id"]
        print(f"Judging {case_id}...", end=" ", flush=True)
        user_message = compose_user_message(scoring_guide, case, trace)
        try:
            verdict = call_judge(judge_prompt, user_message, args.model)
        except (json.JSONDecodeError, KeyError) as e:
            print(f"FAILED ({e})")
            continue
        results.append({"case": case, "verdict": verdict})
        scores = verdict["scores"]
        score_str = "/".join(str(scores[k]) for k in DIM_KEYS)
        tags = verdict["failure_tags"]
        print(f"[{score_str}] tags={tags}")

    OBS_DIR.mkdir(exist_ok=True)
    out_path = OBS_DIR / f"{log_path.stem}_judge.md"
    out_path.write_text(build_judge_md(log_path, results, args.model), encoding="utf-8")
    print(f"\nJudge report written to: {out_path}")


if __name__ == "__main__":
    main()
