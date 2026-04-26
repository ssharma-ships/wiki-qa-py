#!/usr/bin/env python3
"""
Score a saved QA log against eval_cases.yaml using an LLM judge.

Usage:
    python judge.py --log logs/v0_run1.json [--model MODEL]

Matches each eval case to a trace by question string (exact match).
Writes: observations/{log_stem}_judge.md
        observations/{log_stem}_judge.jsonl
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
OBS_BASE = Path("observations")

DEFAULT_MODEL = "claude-opus-4-7"
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


def get_prompt_version(traces_by_question: dict[str, dict]) -> str:
    for trace in traces_by_question.values():
        return trace.get("prompt_version", "unknown")
    return "unknown"


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


def validate_verdict(verdict: dict) -> list[str]:
    """Return a list of structural error strings. Empty list means valid."""
    errors = []
    for key in ("case_id", "scores", "abstention_expected", "epistemic_behavior_correct", "failure_tags", "rationales"):
        if key not in verdict:
            errors.append(f"missing key: {key!r}")
    if "scores" in verdict:
        if not isinstance(verdict["scores"], dict):
            errors.append("'scores' is not a dict")
        else:
            for k in DIM_KEYS:
                if k not in verdict["scores"]:
                    errors.append(f"scores missing key: {k!r}")
                elif verdict["scores"][k] not in (1, 2, 3):
                    errors.append(f"scores[{k!r}]={verdict['scores'][k]!r} not in {{1,2,3}}")
    if "abstention_expected" in verdict and not isinstance(verdict["abstention_expected"], bool):
        errors.append("'abstention_expected' is not a bool")
    if "epistemic_behavior_correct" in verdict and not isinstance(verdict["epistemic_behavior_correct"], bool):
        errors.append("'epistemic_behavior_correct' is not a bool")
    if "failure_tags" in verdict and not isinstance(verdict["failure_tags"], list):
        errors.append("'failure_tags' is not a list")
    if "rationales" in verdict:
        if not isinstance(verdict["rationales"], dict):
            errors.append("'rationales' is not a dict")
        else:
            for k in DIM_KEYS:
                if k not in verdict["rationales"]:
                    errors.append(f"rationales missing key: {k!r}")
    return errors


def fetch_raw_judge_response(judge_prompt: str, user_message: str, model: str) -> str:
    """
    Call the judge model and return the raw text response.
    Retries once on APIError (transient failures only).
    Does not retry on JSON parse or validation errors — at temperature=0 the
    output is deterministic, so a retry would return the same bad response.
    """
    def _call() -> str:
        resp = _client.messages.create(
            model=model,
            max_tokens=JUDGE_MAX_TOKENS,
            system=judge_prompt,
            messages=[{"role": "user", "content": user_message}],
        )
        raw = resp.content[0].text.strip()
        # Strip code fences if present
        raw = re.sub(r"^```(?:json)?\s*", "", raw)
        raw = re.sub(r"\s*```$", "", raw)
        # If the model added prose before/after the JSON, extract the object
        match = re.search(r"\{[\s\S]*\}", raw)
        if match:
            raw = match.group(0)
        return raw

    try:
        return _call()
    except anthropic.APIError:
        return _call()  # one retry for transient API errors; if this also fails, propagate


# ---------------------------------------------------------------------------
# Markdown output
# ---------------------------------------------------------------------------

def build_judge_md(log_path: Path, results: list[dict], model: str) -> str:
    n_scored = sum(1 for r in results if "verdict" in r)
    n_failed = sum(1 for r in results if "error" in r)

    lines = [
        f"# Judge Results — {log_path.stem}",
        "",
        f"**Log:** `{log_path}`  ",
        f"**Judge model:** {model}  ",
        f"**Cases scored:** {n_scored}  ",
        f"**Cases failed:** {n_failed}",
        "",
        "---",
        "",
        "## Summary",
        "",
        "| case_id | ES | HO | TE | CO | AQ | abst_expected | epi_correct | tags |",
        "|---------|----|----|----|----|----|---------------|-------------|------|",
    ]

    for r in results:
        if "error" in r:
            case_id = r["case"]["case_id"]
            lines.append(f"| {case_id} | — | — | — | — | — | — | — | FAILED |")
        else:
            v = r["verdict"]
            s = v["scores"]
            scores_cols = " | ".join(str(s[k]) for k in DIM_KEYS)
            abst_exp = "true" if v["abstention_expected"] else "false"
            epi_ok = "true" if v["epistemic_behavior_correct"] else "false"
            tags = ", ".join(v["failure_tags"]) if v["failure_tags"] else "—"
            lines.append(f"| {v['case_id']} | {scores_cols} | {abst_exp} | {epi_ok} | {tags} |")

    lines += ["", "---", ""]

    for r in results:
        case = r["case"]

        if "error" in r:
            lines += [
                f"## {case['case_id']} — FAILED",
                "",
                f"**Question:** {case['question']}  ",
                f"**Error:** `{r['error']}`",
                "",
            ]
            raw = r.get("raw_response")
            if raw:
                preview = raw[:500] + ("..." if len(raw) > 500 else "")
                lines += ["**Raw response (truncated):**", "```", preview, "```", ""]
            lines += ["---", ""]
            continue

        v = r["verdict"]
        lines += [
            f"## {v['case_id']}",
            "",
            f"**Question:** {case['question']}  ",
            f"**Evidence condition:** {case['evidence_condition']}  ",
            f"**Abstention expected:** {v['abstention_expected']}  ",
            f"**Epistemic behavior correct:** {v['epistemic_behavior_correct']}",
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
# JSONL output
# ---------------------------------------------------------------------------

def build_jsonl(log_stem: str, prompt_version: str, results: list[dict]) -> str:
    lines = []
    for r in results:
        case_id = r["case"]["case_id"]
        if "error" in r:
            entry = {
                "log_stem": log_stem,
                "prompt_version": prompt_version,
                "case_id": case_id,
                "error": r["error"],
                "raw_response": r.get("raw_response"),
            }
        else:
            v = r["verdict"]
            entry = {
                "log_stem": log_stem,
                "prompt_version": prompt_version,
                "case_id": case_id,
                "scores": v["scores"],
                "abstention_expected": v["abstention_expected"],
                "epistemic_behavior_correct": v["epistemic_behavior_correct"],
                "failure_tags": v["failure_tags"],
                "rationales": v["rationales"],
            }
        lines.append(json.dumps(entry, ensure_ascii=False))
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Judge a saved QA log.")
    parser.add_argument("--log", required=True, type=Path, help="Path to log JSON file")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="Judge model")
    parser.add_argument("--out-suffix", default="", help="Suffix appended to output stem (e.g. '.1' → run2.1_judge.md)")
    args = parser.parse_args()

    log_path: Path = args.log
    if not log_path.exists():
        sys.exit(f"Log file not found: {log_path}")

    judge_prompt = JUDGE_PROMPT_PATH.read_text(encoding="utf-8")
    scoring_guide = SCORING_GUIDE_PATH.read_text(encoding="utf-8")
    eval_cases = load_eval_cases()
    traces_by_question = load_traces(log_path)
    prompt_version = get_prompt_version(traces_by_question)

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
        raw_response = None
        try:
            raw_response = fetch_raw_judge_response(judge_prompt, user_message, args.model)
            verdict = json.loads(raw_response)
            errors = validate_verdict(verdict)
            if errors:
                raise ValueError("; ".join(errors))
        except json.JSONDecodeError as e:
            print(f"PARSE_ERROR ({e})")
            print(f"  raw: {raw_response[:200]!r}")
            results.append({"case": case, "error": f"JSONDecodeError: {e}", "raw_response": raw_response})
            continue
        except ValueError as e:
            print(f"VALIDATION_ERROR ({e})")
            print(f"  raw: {raw_response[:200]!r}")
            results.append({"case": case, "error": f"ValidationError: {e}", "raw_response": raw_response})
            continue
        except anthropic.APIError as e:
            print(f"API_ERROR ({e})")
            results.append({"case": case, "error": f"APIError: {e}", "raw_response": None})
            continue

        results.append({"case": case, "verdict": verdict})
        scores = verdict["scores"]
        score_str = "/".join(str(scores[k]) for k in DIM_KEYS)
        print(f"[{score_str}] tags={verdict['failure_tags']}")

    obs_dir = OBS_BASE / prompt_version
    obs_dir.mkdir(parents=True, exist_ok=True)
    out_stem = log_path.stem + args.out_suffix
    md_path = obs_dir / f"{out_stem}_judge.md"
    md_path.write_text(build_judge_md(log_path, results, args.model), encoding="utf-8")
    print(f"\nJudge report written to: {md_path}")

    jsonl_path = obs_dir / f"{out_stem}_judge.jsonl"
    jsonl_path.write_text(build_jsonl(out_stem, prompt_version, results), encoding="utf-8")
    print(f"JSONL written to:         {jsonl_path}")


if __name__ == "__main__":
    main()
