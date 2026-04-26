import json
from pathlib import Path

from agent import run_agent
from prompts import PROMPTS

QUESTIONS = [
    ("Who discovered penicillin?", "Control — normal factual behavior"),
    ("What year was the Berlin Wall built?", "H1a — familiar fact; will it bypass search?"),
    ("Who is the president of Georgia?", "H2 — genuinely ambiguous (country vs. US state)"),
    ("What caused the 1929 stock market crash?", "H2 — multi-factor, requires synthesis"),
    (
        "Who was the first person to climb Mount Everest without supplemental oxygen?",
        "Factual but non-obvious; tests search quality",
    ),
    ("What did Einstein and Bohr disagree about?", "H3 — nuanced topic, thin/contested evidence"),
]

PROMPT_VERSION = "v0"
LOG_DIR = Path("logs")
OBS_DIR = Path("observations")


def detect_run_number() -> int:
    existing = list(OBS_DIR.glob(f"{PROMPT_VERSION}_run*.md"))
    return len(existing) + 1


def build_observation_md(traces: list, run_num: int) -> str:
    lines = [
        f"# {PROMPT_VERSION.upper()} Observations — Run {run_num}",
        "",
        f"**Timestamp:** {traces[0]['timestamp']}",
        f"**Model:** {traces[0]['model']}",
        f"**Prompt version:** {PROMPT_VERSION}",
        "",
        "---",
        "",
    ]

    for i, (trace, (question, hypothesis)) in enumerate(zip(traces, QUESTIONS), 1):
        queries = [tc["query"] for tc in trace["tool_calls"] if not tc.get("capped")]
        query_str = " → ".join(f'`"{q}"`' for q in queries) if queries else "_none_"

        lines += [
            f"## Q{i} — {question}",
            "",
            f"**Hypothesis target:** {hypothesis}",
            f"**Searches:** {trace['search_count']} | **Stop:** {trace['stop_reason']}",
            f"**Queries used:** {query_str}",
            "",
            "**Answer:**",
            "",
        ]

        answer = trace["final_answer"] or "(no answer generated)"
        for line in answer.splitlines():
            lines.append(f"> {line}" if line.strip() else ">")

        lines += ["", "---", ""]

    return "\n".join(lines)


def main():
    OBS_DIR.mkdir(exist_ok=True)
    LOG_DIR.mkdir(exist_ok=True)

    run_num = detect_run_number()
    system_prompt = PROMPTS[PROMPT_VERSION]
    traces = []

    for question, _ in QUESTIONS:
        print(f"Running: {question}")
        trace = run_agent(
            question=question,
            system_prompt=system_prompt,
            prompt_version=PROMPT_VERSION,
        )
        traces.append(trace)
        print(f"  searches={trace['search_count']}  stop={trace['stop_reason']}")

    log_path = LOG_DIR / f"{PROMPT_VERSION}_run{run_num}.json"
    log_path.write_text(json.dumps(traces, indent=2, default=str), encoding="utf-8")
    print(f"\nLog written to: {log_path}")

    obs_path = OBS_DIR / f"{PROMPT_VERSION}_run{run_num}.md"
    obs_path.write_text(build_observation_md(traces, run_num), encoding="utf-8")
    print(f"Observations written to: {obs_path}")


if __name__ == "__main__":
    main()
