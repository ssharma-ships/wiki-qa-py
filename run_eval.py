#!/usr/bin/env python3
# Batch harness. Loops over all cases in eval_cases.yaml, calls run_agent()
# for each, and writes the combined log to logs/{version}/{version}_eval_run{N}.json.
# That log file is what judge.py reads for scoring.
"""
Run the agent on all eval_cases.yaml cases and save the combined log.

Usage:
    python run_eval.py --prompt v0 [--model MODEL]

Output: logs/{prompt_version}_eval_run{N}.json
"""
import argparse
import json
import sys
from pathlib import Path

import yaml
from dotenv import load_dotenv

from agent import run_agent, DEFAULT_MODEL
from prompts import PROMPTS

load_dotenv()

EVAL_CASES_PATH = Path("eval_cases.yaml")
LOG_BASE = Path("logs")


def load_questions() -> list[tuple[str, str]]:
    """Return (case_id, question) pairs in file order."""
    data = yaml.safe_load(EVAL_CASES_PATH.read_text(encoding="utf-8"))
    return [(c["case_id"], c["question"]) for c in data["cases"]]


def detect_run_number(prompt_version: str) -> int:
    version_dir = LOG_BASE / prompt_version
    if not version_dir.exists():
        return 1
    existing = [f for f in version_dir.glob(f"{prompt_version}_eval_run*.json")
                if "_forhuman" not in f.name]
    return len(existing) + 1


def main():
    parser = argparse.ArgumentParser(description="Run agent on all eval cases.")
    parser.add_argument("--prompt", required=True, help="Prompt version key (e.g. v0)")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="Model to use")
    args = parser.parse_args()

    prompt_version = args.prompt.lower()
    if prompt_version not in PROMPTS:
        sys.exit(f"Unknown prompt version '{prompt_version}'. Available: {list(PROMPTS)}")

    system_prompt = PROMPTS[prompt_version]
    questions = load_questions()
    run_num = detect_run_number(prompt_version)

    log_dir = LOG_BASE / prompt_version
    log_dir.mkdir(parents=True, exist_ok=True)
    log_path = log_dir / f"{prompt_version}_eval_run{run_num}.json"

    print(f"Prompt: {prompt_version} | Model: {args.model} | Run: {run_num}")
    print(f"Cases: {len(questions)}")
    print()

    traces = []
    for case_id, question in questions:
        print(f"[{case_id}] {question}")
        trace = run_agent(
            question=question,
            system_prompt=system_prompt,
            model=args.model,
            prompt_version=prompt_version,
        )
        traces.append(trace)
        print(f"  searches={trace['search_count']}  stop={trace['stop_reason']}")

    log_path.write_text(json.dumps(traces, indent=2, default=str), encoding="utf-8")
    print(f"\nLog written to: {log_path}")

    human_path = log_dir / f"{prompt_version}_eval_run{run_num}_forhuman.json"
    case_id_by_question = {q: cid for cid, q in questions}
    human_records = [
        {
            "case_id": case_id_by_question.get(t["question"], "unknown"),
            "prompt_version": t.get("prompt_version", prompt_version),
            "question": t["question"],
            "answer": t.get("final_answer"),
        }
        for t in traces
    ]
    human_path.write_text(json.dumps(human_records, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Human review file: {human_path}")
    print(f"Run judge with: python judge.py --log {log_path}")


if __name__ == "__main__":
    main()
