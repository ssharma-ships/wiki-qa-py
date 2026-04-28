# Single-question interactive CLI. Wraps run_agent() for manual one-off use:
#   python run.py -q "Who wrote Hamlet?" --prompt v4
# Prints the answer and search count to stdout. Good for spot-checking a prompt
# on one case without running the full eval suite.

import argparse

from agent import DEFAULT_MODEL, MAX_SEARCHES, run_agent
from prompts import PROMPTS


def main():
    parser = argparse.ArgumentParser(description="Wikipedia QA agent")
    parser.add_argument("-q", "--question", type=str, default=None)
    parser.add_argument("--prompt", type=str, default="v0", choices=list(PROMPTS.keys()))
    parser.add_argument("--model", type=str, default=DEFAULT_MODEL)
    parser.add_argument("--log", type=str, default=None)
    args = parser.parse_args()

    question = args.question or input("Question: ").strip()
    system_prompt = PROMPTS[args.prompt]

    trace = run_agent(
        question=question,
        system_prompt=system_prompt,
        model=args.model,
        log_path=args.log,
        prompt_version=args.prompt,
    )

    print("\n=== Answer ===")
    print(trace["final_answer"] or "(no answer generated)")
    print(f"\n=== Searches used: {trace['search_count']} / max {MAX_SEARCHES} ===")
    print(f"=== Stop reason: {trace['stop_reason']} ===")
    if args.log:
        print(f"=== Trace logged to: {args.log} ===")


if __name__ == "__main__":
    main()
