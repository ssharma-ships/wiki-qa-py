# V0 Baseline Test Plan

## Goal
Run 5–6 targeted questions against the V0 baseline prompt to observe failure
patterns across H1, H2, and H3. Observations will directly inform eval
dimensions and rubric design.

---

## Question Set

| # | Question | Hypothesis target |
|---|---|---|
| 1 | Who discovered penicillin? | Control — normal factual behavior |
| 2 | What year was the Berlin Wall built? | H1a — Claude knows this; will it bypass search? |
| 3 | Who is the president of Georgia? | H2 — genuinely ambiguous (country vs. US state) |
| 4 | What caused the 1929 stock market crash? | H2 — multi-factor, requires synthesis |
| 5 | Who was the first person to climb Mount Everest without supplemental oxygen? | Factual but non-obvious; tests search quality |
| 6 | What did Einstein and Bohr disagree about? | H3 — nuanced topic, thin/contested evidence |

---

## Execution

- Script: `run_v0_obs.py` (one-shot, not a permanent artifact)
- Calls `run_agent` directly for each question
- Logs each trace to `logs/v0/<slug>.json`
- Prints a summary table to stdout on completion

---

## Observations File

After runs complete, write `docs/v0_observations.md` with:

1. **Per-question:** answer excerpt, search count, stop reason, key behavior notes
2. **Cross-question patterns:** grounding failures, verbosity, ambiguity handling, abstention behavior
3. **Eval dimension implications:** what each pattern suggests we need to measure

---

## What We Are Watching For

| Failure mode | Hypothesis | Signal |
|---|---|---|
| Skips search on known question | H1a | search_count = 0 for Q2 |
| Searches but ignores retrieved evidence | H1b | Answer goes beyond or contradicts retrieved text |
| No disambiguation on ambiguous entity | H2 | Q3 answered as if unambiguous |
| Fails to decompose multi-factor question | H2 | Q4 answer shallow or missing key causes |
| Answers confidently with thin evidence | H3 | Q6 answer assertive despite ambiguous Wikipedia coverage |
| Verbose / over-answers | General | Any question where answer exceeds what evidence supports |
