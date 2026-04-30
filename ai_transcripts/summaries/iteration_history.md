# Iteration History — AI Collaboration Summary

**Source:** Claude Code sessions 03–17 (prompt iteration and eval phases)  
**Purpose:** Summary of what each AI session covered during the build and iteration work.

---

## Baseline and Setup (Sessions 01–08)

**Session 01 — Project Exploration and Scoping (Apr 25)**
First Claude Code session. Covered reading the existing planning documents, understanding what had been decided in the planning chats, and orienting to the repo structure. The session established what existed (planning docs only, no code) and what needed to be built.

**Session 02 — Tool Schema Definition (Apr 26)**
Covered creating `tools.py` with the frozen `SEARCH_WIKIPEDIA_TOOL` constant. Also included early work on `wikipedia_client.py`. The session was focused on getting the tool contract in place before writing any prompts.

**Session 03 — V0 Baseline Run and Observations (Apr 26)**
Covered running the V0 baseline prompt against the initial test cases and observing what the system produced. The session involved reading traces, noting patterns in how the model was behaving, and beginning to form a view of what the first prompt change should address.

**Session 05 — Test Case Development (Apr 26)**
Covered designing and writing the initial set of eval cases. The session worked through case categories and what each case was meant to test. Output was `eval_cases.yaml` with 10 initial cases.

**Session 06 — Project Status Check (Apr 26)**
Brief re-orientation session after a gap. Covered reading project memory and reviewing build state. No substantive new work.

**Session 07 — Eval Harness and Judge Setup (Apr 26)**
Covered building `run_eval.py` and `judge.py` and wiring them together. The session also covered designing the judge prompt and scoring rubric. This was the core infrastructure session that made automated evaluation possible.

**Session 08 — Eval Human-Readable Output (Apr 26)**
Covered adding human-readable Q&A output to `run_eval.py` so that manual review alongside judge scores was possible. A relatively short session focused on output formatting.

---

## Evaluation and Iteration (Sessions 09–17)

**Session 09 — V0 Judge Evaluation Run (Apr 26)**
Covered running the judge against V0 outputs for the first time. The session involved reading judge scores across all five dimensions and reviewing the per-case breakdowns. This was the first quantified view of baseline behavior.

**Session 10 — V1 Regression Analysis (Apr 26)**
Covered comparing V1 and V0 judge outputs side by side. The session identified that V1 was scoring lower on certain dimensions compared to V0 and worked through why. The diagnosis was that the conciseness constraint in V1 had suppressed search behavior, causing evidence support to drop. The session concluded with a recommendation for what V1.5 should change.

**Session 11 — V1.5 Eval Run (Apr 26)**
Covered running the full eval and judge pipeline for V1.5, which restored the search-first requirement while keeping V1's conciseness instruction. The session reviewed scores across dimensions and compared against V0 and V1.

**Session 12 — V2 Eval Run (Apr 27)**
Covered running eval and judge for V2, which added explicit evidence-grounding requirements. The session reviewed dimension score changes, particularly on evidence support, compared to prior versions.

**Session 13 — Eval Case Expansion (Apr 27)**
Covered expanding the eval case set. The session identified which behaviors would be targeted by later prompt versions and which case categories needed more coverage. Output was an expanded `eval_cases.yaml`.

**Session 14 — V3 and V4 Iteration and Eval (Apr 27)**
Covered designing V3 (explicit uncertainty and abstention) and V4 (ambiguity decomposition), running V3 through the eval pipeline, and reviewing results. The session also discussed V3.5 as a potential fix for over-abstention cases before running it. This was the longest iteration session and covered multiple prompt versions in sequence.

**Session 15 — V4 Eval Run (Apr 28)**
Covered running the full eval and judge pipeline for V4. The session reviewed the V4 score table and compared it against V3 and V3.5.

**Session 16 — V4.5 Analysis and V5 Proposal (Apr 28)**
Covered reading V4.5 judge output, identifying remaining failure modes, and discussing whether V5 was warranted and what it should address. The session concluded with a V5 direction.

**Session 17 — V4.6 Judge Run (Apr 28)**
Covered running the judge for V4.6. The session checked scores against V4.5 to confirm whether there was regression or improvement. This was the last scored prompt version before switching to packaging work.
