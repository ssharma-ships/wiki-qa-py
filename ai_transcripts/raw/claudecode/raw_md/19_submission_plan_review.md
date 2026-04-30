# Session: 707bc3c6-84f8-473e-922c-56a023cc46d3


---

## User  `2026-04-28 22:11:16`

/model
            
            opus

---

## User  `2026-04-28 22:11:16`

Set model to [1mOpus 4.7[22m

---

## User  `2026-04-28 22:12:18`

Can you read the take-home assignment document in the docs folder and then come up with a detailed plan on what are the steps that need to be taken? Once you come up with that plan, compare your plan with the plan that is in the docs folder, which says submission packaging plan. What I want you to do is come up with your own plan, review the material, come up with your own plan, compare it with the plan that already exists, critique the plan that exists, and find the delta between your plan and the existing plan.

---

## Assistant  `2026-04-28 22:12:21`

I'll start by exploring the docs folder to find the assignment document and the existing submission packaging plan.

---

## Assistant  `2026-04-28 22:12:22`

**Tool call — `Bash`**
```json
{
  "command": "ls C:/Users/shivi/wiki-qa-py/docs/",
  "description": "List files in docs folder"
}
```

---

## User  `2026-04-28 22:12:22`

**Tool result:**
```
anthropic_prompt_engineering_take_home.md.txt
basic_call_setup_plan.md
claude_wikipedia_qa_experiment_plan.md.txt
eval_rubric-dont-use.md
submission_packaging_plan.md
```

---

## Assistant  `2026-04-28 22:12:25`

**Tool call — `Read`**
```json
{
  "file_path": "C:/Users/shivi/wiki-qa-py/docs/anthropic_prompt_engineering_take_home.md.txt"
}
```

---

## User  `2026-04-28 22:12:25`

**Tool result:**
```
1	# Anthropic Prompt Engineering Take-Home Assignment
2	
3	---
4	
5	## Context
6	
7	As AI capabilities advance rapidly, engineers at Anthropic face a unique challenge:
8	building tools and experiences that are genuinely useful, trustworthy, and delightful.
9	
10	The best products:
11	- Demonstrate taste
12	- Handle complexity gracefully
13	- Solve real problems in non-obvious ways
14	
15	This assignment evaluates your prompt engineering and evaluation skills through a focused, practical task.
16	
17	---
18	
19	## Time Expectation
20	
21	- **Target:** 1–2 hours  
22	- **Hard limit:** 8 hours  
23	
24	Guidelines:
25	- Insight and depth > breadth  
26	- Many strong submissions are completed in under 2 hours  
27	- If you exceed 8 hours, stop and submit  
28	
29	**Requirement:**  
30	Include time spent in your written rationale.
31	
32	---
33	
34	## The Task
35	
36	Build a system that uses **Claude + Wikipedia** to answer questions and evaluate its performance.
37	
38	### Requirements
39	
40	1. **System Prompt + Tool Design**
41	   - Design a system prompt for an LLM with access to:
42	     ```
43	     search_wikipedia(query: str)
44	     ```
45	   - The prompt should guide effective use of Wikipedia for high-quality answers
46	
47	2. **Wikipedia Retrieval Integration**
48	   - Implement a working end-to-end system
49	   - Allowed approaches:
50	     - MediaWiki API
51	     - Wikipedia dump
52	     - Local search index
53	     - Any custom method
54	
55	3. **Evaluation Suite**
56	   - Build a system to evaluate performance across test cases
57	
58	---
59	
60	## Deliverables
61	
62	### 1. Runnable Prototype
63	- Must be executable by reviewers
64	- Accepts a question → returns an answer
65	- Should indicate whether search was used
66	
67	**Acceptable formats:**
68	- CLI
69	- Script
70	- Notebook
71	
72	**Must include:**
73	- Setup instructions (dependencies, API keys)
74	- Sample queries or demo mode
75	
76	---
77	
78	### 2. Code
79	- Submit via GitHub repository
80	- Co

[... 1705 chars truncated]
```

---

## Assistant  `2026-04-28 22:12:27`

**Tool call — `Read`**
```json
{
  "file_path": "C:/Users/shivi/.claude/projects/C--Users-shivi-wiki-qa-py/memory/project_state.md"
}
```

---

## User  `2026-04-28 22:12:27`

**Tool result:**
```
1	---
2	name: Project phase and build state
3	description: Current phase, completed runs, score tables, and what's next for the wiki-qa-py experiment
4	type: project
5	originSessionId: a1880a7e-0f4d-464b-8897-38c3a8055f32
6	---
7	**Current state: V4.6 run, judged, and locked as final. Submission is ready.**
8	
9	**No further prompt iteration planned.** V4.6 is the final prompt. All three open issues (I-002 resolved; I-008/I-003/I-007 wontfix; I-006/I-010 deliberate closes) are documented in the issue tracker and iteration log.
10	
11	---
12	
13	## Prompt version plan
14	
15	| Version | Target behavior | Status |
16	|---------|----------------|--------|
17	| V0 | Baseline — intentionally minimal, exposes H1/H2/H3 failures | **done** |
18	| V1 | Answer focus — direct and concise, no unrequested context | **done** |
19	| V1.5 | Search-first mandate — restores retrieval while keeping V1 conciseness | **done** |
20	| V2 | Exact-value evidence verification — grounding at the claim level | **done** |
21	| V3 | Full abstention discipline — closes hedge+assert loophole; concise non-answers | **done** |
22	| V3.5 | Retrieval-recovery policy — attempted I-008 fix; failed, regressions — **not carried forward** | **done (failed)** |
23	| V4 | Disambiguation protocol — explicit pre-answer ambiguity check; builds from V3 | **done** |
24	| V4.5 | Hardened disambiguation (assume+answer+signoff) + hedge+assert negation closure | **done** |
25	| V5 | Scope constraint + signoff enforcement — net regression; documents I-010 trade-off | **done (regression)** |
26	| V4.6 | Signoff enforcement only (priority 2 isolated) — builds from V4.5, not V5 | **done — FINAL** |
27	
28	---
29	
30	## V4.6 scores (v4.6_eval_run1 — 18 cases) — FINAL, best overall results
31	
32	Judge file: `observations/v4.6/v4.6_eval_run1_judge.md`
33	
34	| case_id | ES | HO | TE | CO | AQ | CV | epi_correct | tags |
35	|---|---|---|---|---|---|---|---|---|
36	| simple-1 | 3 | 3 | 3 | 3 | 3 | 3 | true | — |
37	| simple-

[... 10354 chars truncated]
```

---

## Assistant  `2026-04-28 22:12:30`

Now let me look at the existing files structure to understand what's already in place.

---

## Assistant  `2026-04-28 22:12:31`

**Tool call — `Bash`**
```json
{
  "command": "ls C:/Users/shivi/wiki-qa-py/",
  "description": "List top-level repo files"
}
```

---

## User  `2026-04-28 22:12:31`

**Tool result:**
```
__pycache__
agent.py
CLAUDE.md
docs
eval
eval_cases.yaml
eval_cases_old.yaml
judge.py
logs
observations
prompts.py
run.py
run_eval.py
run_v0_obs.py
tools.py
wikipedia_client.py
```

---

## Assistant  `2026-04-28 22:12:32`

**Tool call — `Read`**
```json
{
  "file_path": "C:/Users/shivi/wiki-qa-py/docs/submission_packaging_plan.md"
}
```

---

## User  `2026-04-28 22:12:32`

**Tool result:**
```
1	# Submission Packaging Plan
2	
3	The code and experiment are complete. V4.6 is locked as the final prompt (15/18 epi_correct).
4	This plan covers everything needed to turn the completed work into a submittable package.
5	
6	---
7	
8	## The 4 Deliverables
9	
10	1. Runnable prototype with setup instructions and demo mode
11	2. Clean GitHub repository
12	3. Design rationale — written document + ~5 min video
13	4. AI transcripts (evidence of human judgment, not just logs)
14	
15	---
16	
17	## Step 1 — GitHub repo audit and cleanup
18	
19	**Check:**
20	- Does `README.md` exist with setup instructions (Python version, pip install, API key)?
21	- Does `requirements.txt` exist?
22	- Can a reviewer run the system with one command (e.g. `python agent.py "some question"`)?
23	- Does output indicate whether search was used? (Assignment explicitly requires this.)
24	- Is there a demo mode or sample query list?
25	
26	**Concrete gaps to close:**
27	- Add setup instructions: Python version, `pip install -r requirements.txt`, `ANTHROPIC_API_KEY` env var
28	- Add sample invocation block (3–4 hard-coded test questions)
29	- Confirm tool call trace appears in output (search used: yes/no)
30	- Organize repo so a reviewer can orient in 60 seconds
31	
32	---
33	
34	## Step 2 — AI transcript packaging
35	
36	This is a first-class deliverable, not an afterthought.
37	
38	**What to do:**
39	- Export or collect transcripts from the Claude Code session
40	- Transcripts must show judgment: where you pushed back, why you chose V4.6 over V5,
41	  why I-008 is wontfix, why retrieval was held fixed
42	- Write a 1-page judgment summary narrating the key decisions if transcripts are long
43	
44	**Key source:** `observations/iteration_log.md` — the hypothesis → change → outcome
45	narrative maps directly to "how you evaluated outputs and made tradeoffs."
46	
47	---
48	
49	## Step 3 — Written design rationale document
50	
51	**Source files (in priority order):**
52	1. `memory/project_state.md` — sco

[... 2892 chars truncated]
```

---

## Assistant  `2026-04-28 22:12:37`

Let me quickly check the current state of a few key files to ground my own plan.

---

## Assistant  `2026-04-28 22:12:39`

**Tool call — `Bash`**
```json
{
  "command": "ls C:/Users/shivi/wiki-qa-py/ | grep -iE \"readme|requirements|setup|\\.env|license|gitignore\"",
  "description": "Check for setup/readme files"
}
```

---

## User  `2026-04-28 22:12:39`

**Tool result:**
```
(Bash completed with no output)
```

---

## Assistant  `2026-04-28 22:12:39`

**Tool call — `Bash`**
```json
{
  "command": "ls C:/Users/shivi/wiki-qa-py/eval/ C:/Users/shivi/wiki-qa-py/observations/ 2>&1 | head -60",
  "description": "List eval and observations folders"
}
```

---

## User  `2026-04-28 22:12:40`

**Tool result:**
```
C:/Users/shivi/wiki-qa-py/eval/:
eval_and_scoring.md
eval_and_scoring_old.md
judge_prompt.txt
judge_prompt_old.txt

C:/Users/shivi/wiki-qa-py/observations/:
issue_tracking
iteration_log.md
test_setup_run1.md
test_setup_run2.md
v0
v1
v1.5
v2
v3
v3.5
v4
v4.5
v4.6
v5
```

---

## Assistant  `2026-04-28 22:12:40`

**Tool call — `Read`**
```json
{
  "file_path": "C:/Users/shivi/wiki-qa-py/run.py"
}
```

---

## User  `2026-04-28 22:12:40`

**Tool result:**
```
1	# Single-question interactive CLI. Wraps run_agent() for manual one-off use:
2	#   python run.py -q "Who wrote Hamlet?" --prompt v4
3	# Prints the answer and search count to stdout. Good for spot-checking a prompt
4	# on one case without running the full eval suite.
5	
6	import argparse
7	
8	from agent import DEFAULT_MODEL, MAX_SEARCHES, run_agent
9	from prompts import PROMPTS
10	
11	
12	def main():
13	    parser = argparse.ArgumentParser(description="Wikipedia QA agent")
14	    parser.add_argument("-q", "--question", type=str, default=None)
15	    parser.add_argument("--prompt", type=str, default="v0", choices=list(PROMPTS.keys()))
16	    parser.add_argument("--model", type=str, default=DEFAULT_MODEL)
17	    parser.add_argument("--log", type=str, default=None)
18	    args = parser.parse_args()
19	
20	    question = args.question or input("Question: ").strip()
21	    system_prompt = PROMPTS[args.prompt]
22	
23	    trace = run_agent(
24	        question=question,
25	        system_prompt=system_prompt,
26	        model=args.model,
27	        log_path=args.log,
28	        prompt_version=args.prompt,
29	    )
30	
31	    print("\n=== Answer ===")
32	    print(trace["final_answer"] or "(no answer generated)")
33	    print(f"\n=== Searches used: {trace['search_count']} / max {MAX_SEARCHES} ===")
34	    print(f"=== Stop reason: {trace['stop_reason']} ===")
35	    if args.log:
36	        print(f"=== Trace logged to: {args.log} ===")
37	
38	
39	if __name__ == "__main__":
40	    main()
41	
```

---

## Assistant  `2026-04-28 22:14:51`

I've read the assignment and the existing `submission_packaging_plan.md`. Below is my own plan built from the assignment requirements, then a critique of the existing plan, then the delta.

---

## My Plan (built from assignment requirements, ignoring existing plan)

### Phase A — Reviewer-can-run-it gate (highest blast radius if it fails)
- **A1. `README.md`** with: Python version, `pip install -r requirements.txt`, `ANTHROPIC_API_KEY` setup, one-liner invocation (`python run.py -q "…" --prompt v4.6`), 3–5 copy-paste sample queries, repo map (1 line per top-level file), eval-suite invocation, **explicit model name used**.
- **A2. `requirements.txt`** — pin only `anthropic`, `requests`, `pyyaml` (or whatever's actually imported).
- **A3. `.env.example`** with `ANTHROPIC_API_KEY=`.
- **A4. Decide demo-mode form** — assignment requires "sample queries OR demo mode." Either `--demo` flag in `run.py` or a `samples.txt`. Don't leave ambiguous.
- **A5. Verify "search used" output** — assignment explicitly requires output indicating whether search was used. `run.py` currently prints `Searches used: N`. Confirm that satisfies the requirement or add an explicit `Search used: yes/no` line.
- **A6. Smoke test** — clone fresh into a tmp dir, walk the README literally as a stranger would. This is the single highest-ROI 30 min in the whole exercise.

### Phase B — Repo hygiene
- **B1.** Decide fate of `eval_cases_old.yaml`, `eval/*_old.*`, `run_v0_obs.py`, `__pycache__/`. Either delete from submission branch or relocate to `archive/`.
- **B2.** `.gitignore` for `__pycache__/`, `.env`, `*.pyc`.
- **B3.** Decide fate of `CLAUDE.md` — it's instructions to me, not the reviewer. Either keep + reference in README as AI-collaboration evidence, or gitignore. **Don't leave it ambiguous.**
- **B4.** Confirm `prompts.py` carries inline rationale comments per version.

### Phase C — Written design rationale (single doc, e.g. `RATIONALE.md`)
Map 1:1 to assignment's 6 required topics, but **lead with framing**:
- **Frame** (top of doc): "Behavior-control experiment, not QA optimization. Retrieval fixed. Prompt is the policy layer." Plus one-change-per-version discipline.
- **§1 Prompt approach** — surface H1/H2/H3 explicitly as named hypotheses with resolution status. This is the differentiator.
- **§2 Eval design** — 6 dimensions (ES/HO/TE/CO/AQ/CV), one-sentence "why this dimension" each, judge prompt rationale, validation strategy.
- **§3 Performance** — single consolidated V0→V4.6 summary table (not 10 full tables). Each remaining failure attributed to root cause.
- **§4 Iterations** — 5 decision points (V1 conciseness, V2 grounding, V3 abstention, V4/V4.6 disambiguation, V5 regression diagnosis). The V5 regression is the standout judgment moment.
- **§5 Extensions** — body-text retrieval (fixes I-008), multi-query disambiguation, holdout eval, cross-version regression tests.
- **§6 Time spent** — actual hours, tracked during execution, not post-hoc guessed.

Source files in priority order: `project_state.md` (scores), `iteration_log.md` (narrative), `issues.md` (wontfix decisions), `prompts.py` (rationale), `eval_and_scoring.md` (rubric).

### Phase D — AI transcripts
- **D1. Curated `TRANSCRIPTS.md` is the primary artifact.** A 1–2 page judgment summary up front: where I pushed back, where I overruled Claude, key tradeoffs I owned (V4.6 vs V5, I-008 wontfix, retrieval-held-fixed). Raw transcripts are appendix.
- **D2. Scrub for secrets** — API keys, personal info, internal paths.
- **D3.** Specific evidence-of-judgment moments to cite: V5 regression diagnosis, I-008 wontfix call, V4.6 isolation from V5.

### Phase E — Video (~5 min)
Write only after rationale doc is done; use it as script.
- 0:00–0:30 Frame
- 0:30–1:15 V0 baseline failure live (ambig-1)
- 1:15–2:00 Eval design + one judge output
- 2:00–3:30 V0→V4.6 arc, 3 core fixes, V5 regression
- 3:30–4:15 V4.6 ambig-1 pass + noisy-1 honest failure (I-008)
- 4:15–5:00 Extensions + time
- **Pre-record check:** terminal contains no API keys, no `.env` visible, no internal URLs.

### Phase F — Submission packaging
- **F1.** Greenhouse field-by-field checklist: repo URL, run instructions, transcripts, video link, written doc.
- **F2.** Final fresh-clone walkthrough.
- **F3.** Confirm video link is shareable (not "anyone with link… inside Anthropic").

### Sequencing
A → B (parallel with A) → C → D (parallel with C) → E → F. A first because it blocks reviewers; F last because it's verification.

---

## Critique of the existing `submission_packaging_plan.md`

**Strengths:**
- All 4 deliverables identified, sourced correctly to existing artifacts.
- Source-file priority list in Step 3 is sharper than what I had.
- Sequencing rationale ("Step 2 second because uniquely yours, can't be delegated") is a real insight.
- Video segment timing is tight and well-allocated.
- Calls out V5 regression and I-008 honest failure as worth highlighting — correct judgment.

**Weaknesses (the plan operates one level too abstract for a packaging exercise — it reads like strategy when it should read like a checklist):**

1. **No fresh-clone smoke test.** Single highest-value 30 min step is missing.
2. **`requirements.txt` and `.env.example` not concretely listed.** Step 1 asks "does it exist?" without specifying contents.
3. **Demo mode hand-waved.** "Add sample invocation block (3–4 questions)" — flag? file? README block? Decide.
4. **Model name not flagged.** Assignment explicitly requires specifying model used. Plan doesn't mention this.
5. **No `_old` file cleanup decision** (`eval_cases_old.yaml`, `eval/*_old.*`, `run_v0_obs.py`). These are noise to a reviewer.
6. **CLAUDE.md handling not addressed.** It's in the repo and reviewers will see it.
7. **Transcript curation framed as optional** ("if transcripts are long"). Should be primary — raw transcripts without curation invite the "purely AI-generated" failure mode the assignment warns about.
8. **No transcript/video secret-scrubbing step.**
9. **Hypotheses (H1/H2/H3) not surfaced as a written-doc element.** They're a project-level differentiator; the doc's §1 should name them.
10. **Score table strategy ambiguous.** "Score table V0→V4.6" — full reproduction is huge; condensed summary is the right call but plan doesn't specify.
11. **No final Greenhouse-field verification.** Plan ends at video; no submit-checklist.
12. **No time-tracking mechanic.** "Include a real estimate" — but no instruction to log hours per phase as you go, so estimate ends up post-hoc and weak.
13. **No risk register.** Windows paths, secret leaks, video re-takes, transcript bloat — none surfaced.

---

## Delta (mine vs. existing)

**Additions in mine that the existing plan lacks:**
- Fresh-clone smoke test (A6)
- Concrete `requirements.txt` / `.env.example` artifacts (A2/A3)
- Explicit demo-mode decision (A4)
- "Search used" output verification (A5)
- Repo map in README (A1)
- Model name call-out (A1)
- `_old`-file and `__pycache__` cleanup decision (B1/B2)
- CLAUDE.md handling decision (B3)
- Hypotheses H1/H2/H3 elevated as a §1 element (C)
- Curated transcript summary as **primary** artifact, raw as appendix (D1)
- Secret scrubbing for transcripts and video (D2, E)
- Phase F: explicit Greenhouse-field verification + final fresh-clone walkthrough (F1–F3)
- Time tracking during execution, not after (C §6)
- Pre-record video privacy check (E)

**Things the existing plan has that mine should adopt:**
- Source-file priority list in Step 3 (cleaner than my version)
- "Step 2 uniquely yours, can't be delegated" sequencing rationale
- Tighter video segment timing breakdown

**Net assessment:** Existing plan is structurally sound but is missing ~12 concrete checklist-level items, most of which are 5–15 minute tasks that prevent a high-cost failure (reviewer can't run it, secret leak, missing assignment requirement). I'd merge: keep the existing plan's structure and source-file priorities, layer in my Phases A6, B1–B3, D1 (re-framed), F, and the hypotheses framing in §1.

Want me to rewrite `docs/submission_packaging_plan.md` as a merged checklist-style version?

---

## User  `2026-04-28 22:16:51`

Yes, go ahead.

---

## Assistant  `2026-04-28 22:17:56`

**Tool call — `Write`**
```json
{
  "file_path": "C:/Users/shivi/wiki-qa-py/docs/submission_packaging_plan.md",
  "content": "# Submission Packaging Plan\n\nThe code and experiment are complete. V4.6 is locked as the final prompt (15/18 epi_correct).\nThis is a checklist for turning the completed work into a submittable package.\n\nEach item is a discrete check-off. If a step doesn't apply, mark it N/A — don't skip silently.\n\n---\n\n## The 4 Deliverables (Greenhouse fields)\n\n1. GitHub repository link\n2. Instructions to run the system (in repo README)\n3. AI transcripts (curated, with judgment summary)\n4. Design rationale — written document + ~5 min video\n\n---\n\n## Phase A — Reviewer-can-run-it gate\n\nA failure here invalidates everything else. Do this first.\n\n- [ ] **A1. `README.md` at repo root** containing:\n  - [ ] Python version (e.g. 3.11+)\n  - [ ] Install: `pip install -r requirements.txt`\n  - [ ] API key setup: `ANTHROPIC_API_KEY` env var (point to `.env.example`)\n  - [ ] **Model used** — explicit name (e.g. `claude-sonnet-4-...`). Assignment requires this.\n  - [ ] One-liner invocation: `python run.py -q \"Who wrote Hamlet?\" --prompt v4.6`\n  - [ ] 3–5 copy-paste sample queries covering different case types (simple, ambiguous, insufficient)\n  - [ ] How to interpret output (search count, stop_reason)\n  - [ ] How to run the eval suite + judge end-to-end\n  - [ ] Repo map: 1 line per top-level file/dir\n- [ ] **A2. `requirements.txt`** — pin only what's actually imported (`anthropic`, `requests`, `pyyaml`, etc.). Confirm by grepping imports.\n- [ ] **A3. `.env.example`** with `ANTHROPIC_API_KEY=`.\n- [ ] **A4. Demo-mode decision** — assignment requires \"sample queries OR demo mode.\" Pick one:\n  - Option A: `--demo` flag in `run.py` that runs 3 hardcoded questions\n  - Option B: `samples.txt` with copy-paste cases referenced from README\n  - Don't leave this ambiguous.\n- [ ] **A5. \"Search used\" output check** — assignment explicitly requires output to indicate whether search was used. `run.py` prints `Searches used: N`. Confirm that satisfies the requirement, or add explicit `Search used: yes/no`.\n- [ ] **A6. Fresh-clone smoke test** — clone into a tmp dir, follow README literally as a stranger. Fix anything that breaks. **Highest-ROI 30 min in this whole exercise.**\n\n---\n\n## Phase B — Repo hygiene\n\nRun in parallel with Phase A.\n\n- [ ] **B1. Cleanup decisions** — for each, choose: keep as-is / move to `archive/` / delete:\n  - `eval_cases_old.yaml`\n  - `eval/judge_prompt_old.txt`, `eval/eval_and_scoring_old.md`\n  - `run_v0_obs.py`\n  - `__pycache__/`\n- [ ] **B2. `.gitignore`** — covers `__pycache__/`, `.env`, `*.pyc`, IDE files.\n- [ ] **B3. `CLAUDE.md` handling** — these are instructions to the AI, not the reviewer. Decide:\n  - Option A: keep + reference in README as evidence of how AI was directed (counts toward AI-collaboration deliverable)\n  - Option B: gitignore for the submission branch\n- [ ] **B4. `prompts.py`** — confirm each version has an inline rationale comment (1–2 lines explaining what changed and why).\n- [ ] **B5. No secrets in repo** — grep for `sk-`, `ANTHROPIC_API_KEY=` followed by a value, etc.\n\n---\n\n## Phase C — Written design rationale\n\nSingle doc at `RATIONALE.md` (or `docs/rationale.md`). Most content already exists — this is assembly + framing.\n\n**Source files in priority order:**\n1. `memory/project_state.md` — score tables, issue tracker, key findings\n2. `prompts.py` — prompt text + inline rationale\n3. `observations/iteration_log.md` — full intervention narrative\n4. `observations/issue_tracking/issues.md` — wontfix decisions\n5. `eval/eval_and_scoring.md` — dimension definitions\n\n**Doc structure (frame first, then assignment's 6 required topics):**\n\n- [ ] **Framing paragraph at top** — \"Behavior-control experiment, not QA optimization. Retrieval is fixed; prompt is the policy layer. One change per version.\" This is the differentiator — set it in the first 60 seconds of reading.\n\n- [ ] **§1 Prompt engineering approach + rationale**\n  - [ ] Surface H1/H2/H3 explicitly as named hypotheses + resolution status\n  - [ ] V0 as intentional baseline (expose hypotheses, not optimize)\n  - [ ] One-change-per-version discipline + why\n\n- [ ] **§2 Eval design — dimensions + why**\n  - [ ] ES, HO, TE, CO, AQ, CV — one-sentence \"why this dimension\" for each\n  - [ ] Why LLM-as-judge (scale, consistency, explainability)\n  - [ ] How judge prompt was designed and validated (regression test before V4.5)\n\n- [ ] **§3 System performance — works/fails**\n  - [ ] Single consolidated V0→V4.6 summary table (not 10 full per-version tables)\n  - [ ] Each remaining failure attributed to root cause\n  - [ ] I-008 framed as tool ceiling, not prompt failure\n\n- [ ] **§4 Iterations — changes based on evals**\n  - [ ] 5 decision points only (not all 10 versions): V1 conciseness, V2 grounding, V3 abstention, V4/V4.6 disambiguation, V5 regression diagnosis\n  - [ ] V5 regression is a standout judgment moment — include it\n\n- [ ] **§5 Extensions — what you'd do with more time**\n  - Body-text retrieval (fixes I-008 at tool level)\n  - Multi-query disambiguation (search both interpretations, compare)\n  - Holdout eval set (test generalization beyond 18 cases)\n  - Automated cross-version regression tests\n\n- [ ] **§6 Time spent** — actual hours, tracked during execution per phase. Not a post-hoc guess.\n\n---\n\n## Phase D — AI transcripts\n\nRun in parallel with Phase C.\n\n- [ ] **D1. `TRANSCRIPTS.md` (or `ai_transcripts/`) — curated judgment summary is the primary artifact**, raw transcripts are appendix. The assignment warns: \"Purely AI-generated work without human judgment will not pass.\" Curation IS the judgment evidence.\n- [ ] **D2. Judgment summary (1–2 pages)** with concrete moments:\n  - V4.6 vs V5 isolation decision\n  - I-008 wontfix call (tool ceiling, not prompt failure)\n  - Retrieval-held-fixed framing decision\n  - V3.5 failure → revert to V3 → V4\n  - Where I pushed back on Claude's suggestions\n- [ ] **D3. Scrub for secrets** — API keys, personal email, internal paths, anything sensitive.\n- [ ] **D4.** Cross-link from rationale doc and README.\n\n---\n\n## Phase E — Video (~5 min)\n\nWrite only after rationale doc is done; use it as the script.\n\n| Segment | Duration | Content |\n|---|---|---|\n| Frame the experiment | 0:45 | \"I treated the prompt as a controllable policy. Retrieval is fixed. Here's why.\" |\n| Show a baseline failure | 0:45 | Run ambig-1 on V0 live — silent disambiguation, explain what's wrong |\n| Eval design | 0:45 | Show the 6 dimensions and judge output for one case |\n| Iteration arc | 1:15 | Score table V0→V4.6, name 3 core fixes, show V5 regression as structural finding |\n| Final result + failure | 0:45 | Run ambig-1 on V4.6 (full pass), then noisy-1 (tool ceiling — honest failure) |\n| Extensions + time | 0:45 | What you'd do next + how long this took |\n\n- [ ] **E1. Pre-record privacy check** — terminal has no API keys, no `.env` open, no internal URLs visible.\n- [ ] **E2. Recording tool decided** (Loom / OBS / QuickTime). Test audio first.\n- [ ] **E3. One practice run, then record.** Don't perfectionism past 2 takes.\n- [ ] **E4. Confirm video link is shareable to external reviewers** (not \"anyone inside org X\").\n\n---\n\n## Phase F — Final submission verification\n\n- [ ] **F1. Second fresh-clone walkthrough** after all changes are in.\n- [ ] **F2. Greenhouse field check** — every field has an artifact:\n  - [ ] GitHub repo URL (public)\n  - [ ] Run instructions (point to README in repo)\n  - [ ] AI transcripts link or attached\n  - [ ] Written rationale link or attached\n  - [ ] Video link\n- [ ] **F3. Time spent confirmed** in rationale doc.\n- [ ] **F4. Click submit.**\n\n---\n\n## Sequencing\n\n1. **Phase A first** — blocks reviewers from running anything; A6 (smoke test) gates everything downstream.\n2. **Phase B parallel with A** — independent cleanup work.\n3. **Phase C after A** — so the doc references what's actually in the repo.\n4. **Phase D parallel with C** — uniquely yours, can't be delegated to extracted artifacts; uses different source material than C.\n5. **Phase E after C** — uses C as the script.\n6. **Phase F last** — verification only.\n\n---\n\n## Risk register\n\n- **Windows path conventions** in README — call out OS-specifics or test on a Unix-y shell.\n- **Secret leaks in video / transcripts** — D3 and E1 are the controls; don't skip.\n- **Transcript bloat** — raw dumps without curation read as \"purely AI-generated.\" D1 framing protects against this.\n- **Video re-take loop** — budget for 2 takes max; the doc-as-script approach prevents this.\n- **`_old` file confusion** — reviewer sees `eval_cases_old.yaml` next to `eval_cases.yaml` and wonders. B1 forces a decision.\n- **CLAUDE.md ambiguity** — reviewer sees AI instructions and wonders if it's documentation. B3 forces a decision.\n"
}
```

---

## User  `2026-04-28 22:18:00`

**Tool result:**
```
The file C:/Users/shivi/wiki-qa-py/docs/submission_packaging_plan.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

---

## Assistant  `2026-04-28 22:18:08`

Rewrote `docs/submission_packaging_plan.md` as a checklist-style merged plan. Key changes from the original:

- **Phase A** now has 6 concrete check-offs including the fresh-clone smoke test (A6), explicit model-name requirement (A1), demo-mode decision (A4), and "search used" output verification (A5).
- **Phase B** added: cleanup decision for `_old` files and `__pycache__` (B1), CLAUDE.md handling decision (B3), secret-grep (B5).
- **Phase C** kept your source-file priority list; added framing-paragraph-at-top and explicit H1/H2/H3 surfacing in §1.
- **Phase D** reframed: curated judgment summary is now the **primary** artifact, raw transcripts the appendix. Added secret-scrubbing.
- **Phase E** kept your video segment table verbatim; added pre-record privacy check and shareability check.
- **Phase F** new: Greenhouse field-by-field verification + second fresh-clone walkthrough.
- **Risk register** at the bottom.

Sequencing rationale preserved (Step 2/D is "uniquely yours, can't be delegated").
