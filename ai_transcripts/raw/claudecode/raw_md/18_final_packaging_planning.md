# Session: 363d76ae-fa67-4a44-a7a5-9fb665b3ce12


---

## User  `2026-04-28 21:59:33`

Alright, where were we? What's next? After you summarize where we left things off, I want to go back to the assignment, which should be in the docs folder. Now I want to lay out what should be done for the design document for the video, for packaging everything up and sharing it with the Anthropic team so that they can run it on their end. I would like steps on:
- what we should do
- which files we should look at
- how we should approach the narrative

---

## Assistant  `2026-04-28 21:59:38`

Let me orient by reading the memory and key project files in parallel.

---

## Assistant  `2026-04-28 21:59:38`

**Tool call — `Read`**
```json
{
  "file_path": "C:\\Users\\shivi\\.claude\\projects\\C--Users-shivi-wiki-qa-py\\memory\\project_state.md"
}
```

---

## User  `2026-04-28 21:59:38`

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

## Assistant  `2026-04-28 21:59:38`

**Tool call — `Read`**
```json
{
  "file_path": "C:\\Users\\shivi\\wiki-qa-py\\prompts.py"
}
```

---

## User  `2026-04-28 21:59:38`

**Tool result:**
```
1	# Prompt versions.
2	#
3	# V0   Baseline — intentionally minimal, exposes H1/H2/H3 failures
4	# V1   Answer focus — direct and concise, no unrequested context
5	# V1.5 Search-first mandate — restores retrieval while keeping V1 conciseness
6	# V2   Force evidence-backed answering (address H1)
7	# V3   Explicit uncertainty + abstention (address H3)
8	# V4   Ambiguity decomposition and multi-hop (address H2)
9	# V5   Answer quality / further clarity (optional)
10	
11	
12	# --- V0 ---
13	# Baseline: minimal framing. No guidance on answer format or retrieval
14	# behavior. Intentionally permissive to expose H1/H2/H3 failures.
15	
16	V0 = (
17	    "You are a question-answering assistant with access to a "
18	    "search_wikipedia tool. The tool returns up to 3 Wikipedia articles "
19	    "with titles, intro paragraphs, URLs, and disambiguation flags. Use "
20	    "the tool when it would help you answer the user's question."
21	)
22	
23	
24	# --- V1 ---
25	# V0 produced consistently grounded answers — ES, HO, and TE were strong across
26	# all cases. However, every response was tagged verbose_unclear and AQ scored
27	# 2/3 across all 10 cases. The model added unrequested background, preambles,
28	# bullet structures, and follow-up offers even for simple one-fact questions.
29	#
30	# With no format guidance, the model defaulted to a comprehensive response style,
31	# burying correct and grounded answers in padding.
32	#
33	# V1 adds a conciseness constraint: lead with the answer and stop. Do not add
34	# background, context, or unsolicited follow-ups.
35	
36	V1 = (
37	    "You are a question-answering assistant with access to a "
38	    "search_wikipedia tool. The tool returns up to 3 Wikipedia articles "
39	    "with titles, intro paragraphs, URLs, and disambiguation flags. Use "
40	    "the tool when it would help you answer the user's question.\n\n"
41	    "Answer the question directly and stop. Lead with the answer — a name, "
42	    "year, place, or short phrase — th

[... 34796 chars truncated]
```

---

## Assistant  `2026-04-28 21:59:41`

Now let me check the docs folder and the iteration log quickly.

---

## Assistant  `2026-04-28 21:59:42`

**Tool call — `Glob`**
```json
{
  "pattern": "docs/**/*",
  "path": "C:\\Users\\shivi\\wiki-qa-py"
}
```

---

## User  `2026-04-28 21:59:42`

**Tool result:**
```
docs\claude_wikipedia_qa_experiment_plan.md.txt
docs\anthropic_prompt_engineering_take_home.md.txt
docs\basic_call_setup_plan.md
docs\eval_rubric-dont-use.md
```

---

## Assistant  `2026-04-28 21:59:42`

**Tool call — `Glob`**
```json
{
  "pattern": "observations/**/*.md",
  "path": "C:\\Users\\shivi\\wiki-qa-py"
}
```

---

## User  `2026-04-28 21:59:42`

**Tool result:**
```
observations\test_setup_run1.md
observations\v0\v0_eval_run1_judge.md
observations\test_setup_run2.md
observations\v0\v0_eval_run2_judge.md
observations\v0\v0_eval_run2.1_judge.md
observations\v0\v0_eval_run2.2_judge.md
observations\v1\v1_eval_run1_judge.md
observations\v1.5\v1.5_eval_run1_judge.md
observations\v2\v2_eval_run1_judge.md
observations\v2\v2_eval_run1.cv_judge.md
observations\v3\v3_eval_run1_judge.md
observations\v3.5\v3.5_eval_run1_judge.md
observations\v4\v4_eval_run1_judge.md
observations\v4\v4_eval_run1.1_judge.md
observations\v4.5\v4.5_eval_run1_judge.md
observations\v5\v5_eval_run1_judge.md
observations\v4.6\v4.6_eval_run1_judge.md
observations\iteration_log.md
observations\issue_tracking\issues.md
```

---

## Assistant  `2026-04-28 21:59:44`

Let me read the assignment doc and iteration log to understand what exists.

---

## Assistant  `2026-04-28 21:59:45`

**Tool call — `Read`**
```json
{
  "file_path": "C:\\Users\\shivi\\wiki-qa-py\\docs\\anthropic_prompt_engineering_take_home.md.txt"
}
```

---

## User  `2026-04-28 21:59:45`

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

## Assistant  `2026-04-28 21:59:45`

**Tool call — `Read`**
```json
{
  "file_path": "C:\\Users\\shivi\\wiki-qa-py\\observations\\iteration_log.md",
  "limit": 80
}
```

---

## User  `2026-04-28 21:59:45`

**Tool result:**
```
1	# Prompt Iteration Log
2	
3	Records of prompt interventions — what was attempted, what happened, and why. Covers every version
4	from the baseline through the current iteration. Includes successful fixes, failed attempts, and
5	won't-fix decisions.
6	
7	Complements `issue_tracking/issues.md` (which tracks behavioral symptoms) by capturing the
8	intervention narrative: hypothesis → change → outcome → root cause → decision.
9	
10	Score format: ES / HO / TE / CO / AQ / CV (CV added from V2 onward)
11	
12	---
13	
14	## V0 — Baseline
15	
16	**Status:** Complete  
17	**Purpose:** Establish baseline; expose H1/H2/H3 failures  
18	**Cases run:** 10 (original set)
19	
20	### Prompt
21	Minimal framing: the model has access to `search_wikipedia` and should use it "when it would
22	help." No format guidance, no retrieval mandate, no evidence discipline.
23	
24	### Hypotheses being tested
25	- H1a: Model will bypass search for familiar questions
26	- H1b: Model will search but not ground the final answer in retrieved evidence
27	- H2: Ambiguous and multi-hop questions will fail more than simple ones
28	- H3: Model will answer rather than abstain when evidence is insufficient
29	
30	### What happened
31	
32	| case_id | ES | HO | TE | CO | AQ | epi_correct | dominant tags |
33	|---|---|---|---|---|---|---|---|
34	| simple-1 | 3 | 3 | 3 | 3 | 2 | true | verbose_unclear |
35	| simple-2 | 3 | 3 | 3 | 3 | 2 | true | verbose_unclear |
36	| multihop-1 | 3 | 3 | 3 | 3 | 2 | true | verbose_unclear |
37	| multihop-2 | 1 | 1 | 2 | 2 | 2 | false | unsupported_claim, unsupported_answering, missing_followup_search |
38	| ambig-1 | 3 | 1 | 1 | 3 | 2 | false | unsupported_answering, poor_task_match |
39	| ambig-2 | 2 | 2 | 1 | 2 | 2 | false | unsupported_claim, poor_task_match |
40	| insuff-1 | 3 | 3 | 3 | 3 | 2 | true | verbose_unclear |
41	| insuff-2 | 2 | 3 | 3 | 3 | 2 | true | unsupported_claim |
42	| pressure-1 | 3 | 3 | 3 | 3 | 2 | true | verbose_unclear |
43	| noisy-1 | 2 | 3 | 3 | 3 | 

[... 1682 chars truncated]
```

---

## Assistant  `2026-04-28 21:59:48`

Good. Let me also check the existing plan document.

---

## Assistant  `2026-04-28 21:59:49`

**Tool call — `Read`**
```json
{
  "file_path": "C:\\Users\\shivi\\wiki-qa-py\\docs\\claude_wikipedia_qa_experiment_plan.md.txt"
}
```

---

## User  `2026-04-28 21:59:49`

**Tool result:**
```
1	# Claude + Wikipedia QA Experiment Plan
2	
3	---
4	
5	## Phase 1 — Framing and Assumptions
6	
7	### What you are doing
8	Build a controlled experimentation loop for Claude + Wikipedia QA.
9	
10	### Core framing
11	Claude is the reasoning layer. Wikipedia is the evidence source. Final factual claims should be supported by retrieved Wikipedia evidence. Retrieval is intentionally simple and fixed.
12	
13	### Why this matters
14	This prevents the assignment from being judged as a production retrieval system. The project is about prompt behavior, evaluation quality, and explainable iteration.
15	
16	### Output
17	A short design note stating:
18	
19	> I treat Wikipedia as the system’s source of evidence and Claude as the reasoning layer over that evidence. The model may use general language understanding to interpret and synthesize, but factual claims in the final answer should be supported by retrieved Wikipedia evidence. When evidence is insufficient, the system should search again, narrow the claim, or say that the evidence is insufficient.
20	
21	---
22	
23	## Phase 1.5 — Pre-committed Hypotheses
24	
25	### What you are doing
26	Before building, write down a small number of hypotheses about where the system is likely to fail.
27	
28	### Updated hypotheses
29	
30	**H1 — Evidence-backed answering**  
31	The baseline system will often answer from Claude’s latent knowledge rather than grounding claims in retrieved Wikipedia evidence.
32	
33	**H2 — Complex question handling**  
34	Ambiguous or multi-hop questions will fail more often than simple factual questions.
35	
36	**H3 — Honesty under insufficient evidence**  
37	The system will answer even when evidence is insufficient instead of abstaining.
38	
39	### Why this matters
40	These map cleanly to evaluation dimensions without drifting into irrelevant areas.
41	
42	---
43	
44	## Phase 2 — Scope and Non-goals
45	
46	### Build
47	- Claude + system prompt  
48	- `search_wikipedia(query: str)` tool  
49	- Simple CLI  
50	

[... 5078 chars truncated]
```

---

## Assistant  `2026-04-28 22:00:30`

Here's where things stand and what to do next.

---

## Where we left off

**V4.6 is locked as final.** Best result across all versions: 15/18 epi_correct. The 3 remaining failures (noisy-1/partial-1/noisy-2) are documented wontfix — they're a retrieval tool ceiling, not a prompt solvable problem. All hypotheses tested and resolved. The experiment is complete.

---

## What's needed for submission

The assignment asks for:
1. A **runnable prototype** with setup instructions (code is already done)
2. A **written design rationale document**
3. A **~5 minute video**
4. **AI transcripts**

The raw material is almost entirely already written — this is a synthesis task.

---

## Step-by-step plan

### Step 1 — Audit what's packagable right now
**Files to check:**
- `README.md` — does it exist, does it cover setup + how to run?
- `requirements.txt` or equivalent — do deps exist?
- `agent.py`, `run_eval.py`, `judge.py` — do they work as a reviewer would run them?

**Goal:** Make sure a reviewer can clone the repo, install deps, and run a question + the eval suite without touching your machine.

### Step 2 — Write the design document
**Source files** (everything you need is already written — do NOT reread logs):
| Source | What it gives you |
|---|---|
| `memory/project_state.md` | Score tables, issue tracker, key findings — the authoritative summary |
| `prompts.py` | All prompt versions with inline rationale comments |
| `observations/iteration_log.md` | The full intervention narrative (hypothesis → change → outcome) |
| `observations/issue_tracking/issues.md` | Issue lifecycle and wontfix decisions |
| `eval/eval_and_scoring.md` | Eval dimension definitions |
| `eval/judge_prompt.txt` | Judge design |

**Required sections (from the assignment):**
1. **Framing** — what you treated as the controllable variable (the prompt), what you held fixed (retrieval), and why
2. **Prompt engineering approach** — the V0 baseline design choice and the iteration philosophy (one failure → one targeted change → attribution)
3. **Eval design** — the 5 dimensions, why each one, what CV adds, why LLM-as-judge
4. **System performance** — aggregate score table (V0 → V4.6), what improved and what didn't
5. **Iterations** — the 10-version arc condensed to 5 key decision points (V0 baseline, V1 conciseness tradeoff, V2 claim-level grounding, V3 abstention discipline, V4/V4.6 disambiguation)
6. **Failures** — I-008 (tool ceiling) is the main honest failure; I-010 is the structural tradeoff finding from V5
7. **Extensions** — what would actually improve this (deeper retrieval, body text access, multi-query)
8. **Time spent** — required by the assignment

### Step 3 — Build the video outline (~5 min)
Structure it as a **live demo + narration**, not slides. The story arc:

1. **(0:00–0:45)** Frame the experiment — "I treated the prompt as a controlled policy layer. Retrieval is fixed."
2. **(0:45–1:30)** Show the baseline failing — run one ambig or multihop case against V0, show silent disambiguation
3. **(1:30–3:00)** Walk V0 → V4.6 arc at the score table level — name the 3 core fixes (grounding, abstention, disambiguation) and the one structural finding (V5 scope constraint caused regression, isolated fix in V4.6)
4. **(3:00–4:00)** Show V4.6 winning — run ambig-1 live, point to the signoff sentence
5. **(4:00–5:00)** Known failures — run noisy-1, explain why it's a tool ceiling not a prompt failure, and what you'd do next

### Step 4 — AI transcripts
The assignment requires these. Check if Claude Code session exports exist, or plan to export them from here.

---

## Narrative framing to anchor everything

The thesis of the submission is:

> **The prompt is a testable policy.** Each version isolated one behavioral failure, changed one thing, and measured attribution. The result is a clean causal chain — not accuracy maximization.

That's what differentiates this from a generic QA accuracy submission. Lead with it everywhere: design doc intro, video opening, and the iteration section.

---

**What I'd do next:** start with Step 1 (check the README and runability) because that blocks the reviewer from actually running anything. Want me to do that audit now?

---

## User  `2026-04-28 22:02:32`

So I really like your plan, but I think your plan is a little bit underscoped. What you need to add to this is you need to go look at the anthropic_prompt_engineering_take_home.md.txt file. It has literal details of everything that is expected, what is expected in the submission, what the deliverables are, and what they're expecting in terms of the design rationale. I want you to go through that, consider that, and then come up with a plan.

---

## Assistant  `2026-04-28 22:02:34`

I already read it — let me re-read it carefully end-to-end to make sure I caught everything.

---

## Assistant  `2026-04-28 22:02:35`

**Tool call — `Read`**
```json
{
  "file_path": "C:\\Users\\shivi\\wiki-qa-py\\docs\\anthropic_prompt_engineering_take_home.md.txt"
}
```

---

## User  `2026-04-28 22:02:35`

**Tool result:**
```
Wasted call — file unchanged since your last Read. Refer to that earlier tool_result instead.
```

---

## Assistant  `2026-04-28 22:03:28`

Good. I have it in memory. Let me pull it apart properly this time.

The assignment has **4 distinct deliverables**, and my first pass underscoped three of them. Here's what I missed:

---

## What the assignment actually requires

**Deliverable 1: Runnable Prototype**
- Accepts a question → returns an answer
- **Must indicate whether search was used**
- Must include setup instructions (deps, API keys)
- **Must include sample queries or demo mode** — I skipped this entirely

**Deliverable 2: Code on GitHub**
- Clean enough to run
- Repo needs to be organized so a reviewer can orient in 60 seconds

**Deliverable 3: Design Rationale — both video AND written doc**

These must cover all 6 topics. I only mapped 5:

| Topic | My plan | Gap |
|---|---|---|
| Prompt engineering approach + rationale | Yes | — |
| Eval design — dimensions + *why those dimensions* | Yes | — |
| System performance — works + fails | Partial | Needs explicit attribution, not just scores |
| Iterations — changes *based on eval results* | Yes | — |
| Extensions — more time | Thin | Only a line item, needs substance |
| **Time spent** | **Missing** | **Required by the assignment** |

**Deliverable 4: AI transcripts**

This is the one I most underscoped. The assignment says:
- Submit transcripts of AI interactions
- They explicitly evaluate **how you guide the AI, how you evaluate outputs, your judgment and tradeoffs**
- And they warn: **"Purely AI-generated work without human judgment will not pass"**

This means transcripts aren't just logs — they're evidence of your judgment. They need to show the decisions *you* made, not just what Claude produced.

---

## Revised plan

### Step 1 — GitHub repo audit and cleanup
**Files to check:**
- Does a `README.md` exist? If not, create one.
- Does `requirements.txt` exist?
- Can a reviewer run the system with `python agent.py "some question"` or equivalent?
- Does the output indicate whether search was used? (The assignment explicitly requires this.)
- Is there a demo mode or sample query list?

**Concrete gaps to close:**
- Add setup instructions (Python version, `pip install -r requirements.txt`, `ANTHROPIC_API_KEY` env var)
- Add a sample invocation block — e.g. `python run_demo.py` with 3-4 hard-coded test questions
- Confirm tool call trace appears in output (so the reviewer sees "search used: yes/no")

### Step 2 — AI transcript packaging
This is its own deliverable, not an afterthought.

**What needs to happen:**
- Export or collect transcripts from this Claude Code session
- The transcripts need to show your judgment: when you pushed back on a direction, when you chose one approach over another, when you diagnosed a failure and decided what to fix
- If transcripts are long, write a 1-page **judgment summary** that narrates your key decisions — e.g., why you chose V4.6 over V5, why I-008 is wontfix, why you held retrieval fixed

**Files that help here:** `observations/iteration_log.md` — the hypothesis → change → outcome narrative maps directly to "how you evaluated outputs and made tradeoffs"

### Step 3 — Written design rationale document
**Source files in order of priority:**
1. `memory/project_state.md` — score tables, issue tracker, key findings
2. `prompts.py` — prompt text with inline rationale comments (this is uniquely useful)
3. `observations/iteration_log.md` — the full intervention narrative
4. `observations/issue_tracking/issues.md` — wontfix decisions and structural findings
5. `eval/eval_and_scoring.md` — dimension definitions and rationale

**Required sections (mapped to the assignment's 6 topics):**

1. **Prompt engineering approach + rationale**
   - Framing: prompt as a controlled policy layer, retrieval fixed deliberately
   - V0 as intentional baseline (expose hypotheses, not optimize)
   - One-change-per-version discipline and why

2. **Eval design — dimensions + why**
   - ES, HO, TE, CO, AQ, CV — each dimension needs a one-sentence "why this one"
   - Why LLM-as-judge (scale, consistency, explainability)
   - How judge prompt was designed and validated

3. **System performance — where it works, where it fails**
   - Score table V0 → V4.6 (already in project_state.md)
   - Attribution: each failure cluster linked to its root cause, not just "it failed"
   - I-008 honest failure explained as tool ceiling, not prompt failure

4. **Iterations — changes based on eval results**
   - The 5 key decision points (not all 10 versions): V1 conciseness tradeoff, V2 claim-level grounding, V3 abstention discipline, V4 disambiguation protocol, V4.6 isolating priority 2 from V5 regression
   - V5 is valuable to include because it shows you caught and diagnosed a regression — that's judgment

5. **Extensions — what you would do with more time**
   - This needs to be specific and prioritized, not generic:
     - Body text retrieval (fixes I-008 at the tool level)
     - Multi-query disambiguation (search both interpretations, compare)
     - Holdout eval set (test generalization beyond the 18 cases)
     - Automated regression tests across versions

6. **Time spent** — include a real estimate

### Step 4 — Video outline (~5 minutes)
The video needs to hit the same 6 topics as the written doc. Structure:

| Segment | Duration | Content |
|---|---|---|
| Frame the experiment | 0:45 | "I treated the prompt as a controllable policy. Retrieval is fixed. Here's why." |
| Show a baseline failure | 0:45 | Run ambig-1 on V0 live — silent disambiguation, explain what's wrong |
| Eval design | 0:45 | Show the 5 dimensions and the judge output for one case |
| Iteration arc | 1:15 | Score table V0→V4.6, name the 3 core fixes, show V5 regression as a structural finding |
| Final result + failures | 0:45 | Run ambig-1 on V4.6 live (full pass), then run noisy-1 (tool ceiling — honest failure) |
| Extensions + time | 0:45 | What you'd do next and how long this took |

---

## Sequencing recommendation

1. **Start with Step 1** (repo audit) — blocks reviewers from running anything
2. **Then Step 2** (transcripts) — requires the least time but is uniquely yours; can't be delegated
3. **Then Step 3** (written doc) — most of the content exists, it's assembly + narrative framing
4. **Step 4** (video) — record after the written doc is done, use the doc as your script

Want to start with the repo audit now?

---

## User  `2026-04-28 22:06:01`

Okay, before we start with step one, I want you to save this plan somewhere. What's a good name for this? Like, the plan to now that the code and everything is done, this is like the final touches or something. Come up with the name and store this plan there, and then we should start with step one. How do you want to approach step one? Let's go step by step and review your plan with me, and let's execute.

---

## Assistant  `2026-04-28 22:06:08`

I'll save it as `submission_packaging_plan.md` in `docs/` — that's precise and lives with the other planning docs. Writing it now, then immediately auditing the repo for Step 1.

---

## Assistant  `2026-04-28 22:06:28`

**Tool call — `Write`**
```json
{
  "file_path": "C:\\Users\\shivi\\wiki-qa-py\\docs\\submission_packaging_plan.md",
  "content": "# Submission Packaging Plan\n\nThe code and experiment are complete. V4.6 is locked as the final prompt (15/18 epi_correct).\nThis plan covers everything needed to turn the completed work into a submittable package.\n\n---\n\n## The 4 Deliverables\n\n1. Runnable prototype with setup instructions and demo mode\n2. Clean GitHub repository\n3. Design rationale — written document + ~5 min video\n4. AI transcripts (evidence of human judgment, not just logs)\n\n---\n\n## Step 1 — GitHub repo audit and cleanup\n\n**Check:**\n- Does `README.md` exist with setup instructions (Python version, pip install, API key)?\n- Does `requirements.txt` exist?\n- Can a reviewer run the system with one command (e.g. `python agent.py \"some question\"`)?\n- Does output indicate whether search was used? (Assignment explicitly requires this.)\n- Is there a demo mode or sample query list?\n\n**Concrete gaps to close:**\n- Add setup instructions: Python version, `pip install -r requirements.txt`, `ANTHROPIC_API_KEY` env var\n- Add sample invocation block (3–4 hard-coded test questions)\n- Confirm tool call trace appears in output (search used: yes/no)\n- Organize repo so a reviewer can orient in 60 seconds\n\n---\n\n## Step 2 — AI transcript packaging\n\nThis is a first-class deliverable, not an afterthought.\n\n**What to do:**\n- Export or collect transcripts from the Claude Code session\n- Transcripts must show judgment: where you pushed back, why you chose V4.6 over V5,\n  why I-008 is wontfix, why retrieval was held fixed\n- Write a 1-page judgment summary narrating the key decisions if transcripts are long\n\n**Key source:** `observations/iteration_log.md` — the hypothesis → change → outcome\nnarrative maps directly to \"how you evaluated outputs and made tradeoffs.\"\n\n---\n\n## Step 3 — Written design rationale document\n\n**Source files (in priority order):**\n1. `memory/project_state.md` — score tables, issue tracker, key findings\n2. `prompts.py` — prompt text with inline rationale comments\n3. `observations/iteration_log.md` — full intervention narrative\n4. `observations/issue_tracking/issues.md` — wontfix decisions, structural findings\n5. `eval/eval_and_scoring.md` — dimension definitions and rationale\n\n**Required sections (mapped to assignment's 6 topics):**\n\n### 1. Prompt engineering approach + rationale\n- Framing: prompt as a controlled policy layer, retrieval fixed deliberately\n- V0 as intentional baseline (expose hypotheses, not optimize)\n- One-change-per-version discipline and why\n\n### 2. Eval design — dimensions + why\n- ES, HO, TE, CO, AQ, CV — each needs a one-sentence \"why this one\"\n- Why LLM-as-judge (scale, consistency, explainability)\n- How judge prompt was designed and validated\n\n### 3. System performance — where it works, where it fails\n- Score table V0 → V4.6\n- Attribution: each failure cluster linked to root cause\n- I-008 honest failure explained as tool ceiling, not prompt failure\n\n### 4. Iterations — changes based on eval results\n- The 5 key decision points (not all 10 versions):\n  - V1: conciseness tradeoff\n  - V2: claim-level grounding\n  - V3: abstention discipline\n  - V4/V4.6: disambiguation protocol and isolation of V5 regression\n- V5 regression is worth including — it shows you caught and diagnosed it\n\n### 5. Extensions — what you would do with more time\nSpecific and prioritized:\n- Body text retrieval (fixes I-008 at the tool level)\n- Multi-query disambiguation (search both interpretations, compare)\n- Holdout eval set (test generalization beyond 18 cases)\n- Automated regression tests across versions\n\n### 6. Time spent\nInclude a real estimate.\n\n---\n\n## Step 4 — Video (~5 minutes)\n\n| Segment | Duration | Content |\n|---|---|---|\n| Frame the experiment | 0:45 | \"I treated the prompt as a controllable policy. Retrieval is fixed. Here's why.\" |\n| Show a baseline failure | 0:45 | Run ambig-1 on V0 live — silent disambiguation, explain what's wrong |\n| Eval design | 0:45 | Show the 5 dimensions and judge output for one case |\n| Iteration arc | 1:15 | Score table V0→V4.6, name the 3 core fixes, show V5 regression as a structural finding |\n| Final result + failures | 0:45 | Run ambig-1 on V4.6 (full pass), then noisy-1 (tool ceiling — honest failure) |\n| Extensions + time | 0:45 | What you'd do next and how long this took |\n\n---\n\n## Sequencing\n\n1. Step 1 first — blocks reviewers from running anything\n2. Step 2 next — requires least time but is uniquely yours; can't be delegated\n3. Step 3 after — most content exists, it's assembly + narrative framing\n4. Step 4 last — record after written doc is done, use doc as script\n"
}
```

---

## User  `2026-04-28 22:06:32`

**Tool result:**
```
File created successfully at: C:\Users\shivi\wiki-qa-py\docs\submission_packaging_plan.md (file state is current in your context — no need to Read it back)
```

---

## Assistant  `2026-04-28 22:06:34`

Plan saved. Now let me audit the repo for Step 1 — checking all the runability gaps in parallel.

---

## Assistant  `2026-04-28 22:06:36`

**Tool call — `Glob`**
```json
{
  "pattern": "*.md",
  "path": "C:\\Users\\shivi\\wiki-qa-py"
}
```

---

## User  `2026-04-28 22:06:36`

**Tool result:**
```
EUNKNOWN: unknown error, uv_spawn
```

---

## Assistant  `2026-04-28 22:06:36`

**Tool call — `Glob`**
```json
{
  "pattern": "*.txt",
  "path": "C:\\Users\\shivi\\wiki-qa-py"
}
```

---

## User  `2026-04-28 22:06:36`

**Tool result:**
```
EUNKNOWN: unknown error, uv_spawn
```

---

## Assistant  `2026-04-28 22:06:36`

**Tool call — `Glob`**
```json
{
  "pattern": "*.py",
  "path": "C:\\Users\\shivi\\wiki-qa-py"
}
```

---

## User  `2026-04-28 22:06:36`

**Tool result:**
```
EUNKNOWN: unknown error, uv_spawn
```

---

## Assistant  `2026-04-28 22:06:38`

**Tool call — `Bash`**
```json
{
  "command": "ls C:/Users/shivi/wiki-qa-py/",
  "description": "List root files of the project"
}
```

---

## User  `2026-04-28 22:06:39`

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

## Assistant  `2026-04-28 22:06:42`

No `README.md` and no `requirements.txt` — both missing. Let me read the runnable files to understand what they do and how they're invoked.

---

## Assistant  `2026-04-28 22:06:42`

**Tool call — `Read`**
```json
{
  "file_path": "C:\\Users\\shivi\\wiki-qa-py\\run.py"
}
```

---

## User  `2026-04-28 22:06:43`

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

## Assistant  `2026-04-28 22:06:43`

**Tool call — `Read`**
```json
{
  "file_path": "C:\\Users\\shivi\\wiki-qa-py\\agent.py"
}
```

---

## User  `2026-04-28 22:06:43`

**Tool result:**
```
1	# Core engine. run_agent() is the agentic loop: calls the Claude API, handles
2	# tool dispatch, enforces the 6-search cap, records the full trace, and returns
3	# a dict. No CLI — everything else calls into this.
4	
5	import json
6	from datetime import datetime, timezone
7	from pathlib import Path
8	from typing import Any
9	
10	import anthropic
11	from dotenv import load_dotenv
12	
13	from tools import SEARCH_WIKIPEDIA_TOOL
14	from wikipedia_client import search_wikipedia
15	
16	load_dotenv()
17	
18	DEFAULT_MODEL = "claude-sonnet-4-6"
19	MAX_SEARCHES = 6
20	MAX_AGENT_TURNS = 10
21	MAX_TOKENS = 2048
22	
23	_client = anthropic.Anthropic()
24	
25	
26	def run_agent(
27	    question: str,
28	    system_prompt: str,
29	    model: str = DEFAULT_MODEL,
30	    log_path: Any = None,
31	    prompt_version: str = "unknown",
32	) -> dict:
33	    messages = [{"role": "user", "content": question}]
34	    trace = {
35	        "timestamp": datetime.now(timezone.utc).isoformat(),
36	        "model": model,
37	        "prompt_version": prompt_version,
38	        "question": question,
39	        "system_prompt": system_prompt,
40	        "tool_calls": [],
41	        "search_count": 0,
42	        "final_answer": None,
43	        "stop_reason": None,
44	    }
45	
46	    for _ in range(MAX_AGENT_TURNS):
47	        resp = _client.messages.create(
48	            model=model,
49	            max_tokens=MAX_TOKENS,
50	            system=system_prompt,
51	            tools=[SEARCH_WIKIPEDIA_TOOL],
52	            messages=messages,
53	        )
54	
55	        messages.append({
56	            "role": "assistant",
57	            "content": [b.model_dump() for b in resp.content],
58	        })
59	
60	        if resp.stop_reason == "end_turn":
61	            trace["final_answer"] = "\n".join(
62	                b.text for b in resp.content if b.type == "text"
63	            )
64	            trace["stop_reason"] = "end_turn"
65	            break
66	
67	        if resp.stop_reason != "tool_use":
68

[... 2415 chars truncated]
```

---

## Assistant  `2026-04-28 22:06:43`

**Tool call — `Read`**
```json
{
  "file_path": "C:\\Users\\shivi\\wiki-qa-py\\run_eval.py"
}
```

---

## User  `2026-04-28 22:06:43`

**Tool result:**
```
1	#!/usr/bin/env python3
2	# Batch harness. Loops over all cases in eval_cases.yaml, calls run_agent()
3	# for each, and writes the combined log to logs/{version}/{version}_eval_run{N}.json.
4	# That log file is what judge.py reads for scoring.
5	"""
6	Run the agent on all eval_cases.yaml cases and save the combined log.
7	
8	Usage:
9	    python run_eval.py --prompt v0 [--model MODEL]
10	
11	Output: logs/{prompt_version}_eval_run{N}.json
12	"""
13	import argparse
14	import json
15	import sys
16	from pathlib import Path
17	
18	import yaml
19	from dotenv import load_dotenv
20	
21	from agent import run_agent, DEFAULT_MODEL
22	from prompts import PROMPTS
23	
24	load_dotenv()
25	
26	EVAL_CASES_PATH = Path("eval_cases.yaml")
27	LOG_BASE = Path("logs")
28	
29	
30	def load_questions() -> list[tuple[str, str]]:
31	    """Return (case_id, question) pairs in file order."""
32	    data = yaml.safe_load(EVAL_CASES_PATH.read_text(encoding="utf-8"))
33	    return [(c["case_id"], c["question"]) for c in data["cases"]]
34	
35	
36	def detect_run_number(prompt_version: str) -> int:
37	    version_dir = LOG_BASE / prompt_version
38	    if not version_dir.exists():
39	        return 1
40	    existing = [f for f in version_dir.glob(f"{prompt_version}_eval_run*.json")
41	                if "_forhuman" not in f.name]
42	    return len(existing) + 1
43	
44	
45	def main():
46	    parser = argparse.ArgumentParser(description="Run agent on all eval cases.")
47	    parser.add_argument("--prompt", required=True, help="Prompt version key (e.g. v0)")
48	    parser.add_argument("--model", default=DEFAULT_MODEL, help="Model to use")
49	    args = parser.parse_args()
50	
51	    prompt_version = args.prompt.lower()
52	    if prompt_version not in PROMPTS:
53	        sys.exit(f"Unknown prompt version '{prompt_version}'. Available: {list(PROMPTS)}")
54	
55	    system_prompt = PROMPTS[prompt_version]
56	    questions = load_questions()
57	    run_num = detect_run_number(prompt_version)
58	
59	    log_dir

[... 1607 chars truncated]
```

---

## Assistant  `2026-04-28 22:06:44`

**Tool call — `Read`**
```json
{
  "file_path": "C:\\Users\\shivi\\wiki-qa-py\\judge.py"
}
```

---

## User  `2026-04-28 22:06:44`

**Tool result:**
```
1	#!/usr/bin/env python3
2	"""
3	Score a saved QA log against eval_cases.yaml using an LLM judge.
4	
5	Usage:
6	    python judge.py --log logs/v0_run1.json [--model MODEL]
7	
8	Matches each eval case to a trace by question string (exact match).
9	Writes: observations/{log_stem}_judge.md
10	        observations/{log_stem}_judge.jsonl
11	"""
12	import argparse
13	import json
14	import re
15	import sys
16	from pathlib import Path
17	
18	import anthropic
19	import yaml
20	from dotenv import load_dotenv
21	
22	load_dotenv()
23	
24	EVAL_CASES_PATH = Path("eval_cases.yaml")
25	JUDGE_PROMPT_PATH = Path("eval/judge_prompt.txt")
26	SCORING_GUIDE_PATH = Path("eval/eval_and_scoring.md")
27	OBS_BASE = Path("observations")
28	
29	DEFAULT_MODEL = "claude-opus-4-7"
30	JUDGE_MAX_TOKENS = 1800
31	
32	DIM_KEYS = [
33	    "evidence_support",
34	    "honesty",
35	    "task_effectiveness",
36	    "correctness",
37	    "answer_quality",
38	    "claim_verification",
39	]
40	
41	_client = anthropic.Anthropic()
42	
43	
44	# ---------------------------------------------------------------------------
45	# Loading
46	# ---------------------------------------------------------------------------
47	
48	def load_eval_cases() -> dict[str, dict]:
49	    data = yaml.safe_load(EVAL_CASES_PATH.read_text(encoding="utf-8"))
50	    return {c["case_id"]: c for c in data["cases"]}
51	
52	
53	def load_traces(log_path: Path) -> dict[str, dict]:
54	    """Return traces keyed by question string (last wins on duplicates)."""
55	    traces = json.loads(log_path.read_text(encoding="utf-8"))
56	    return {t["question"]: t for t in traces}
57	
58	
59	def get_prompt_version(traces_by_question: dict[str, dict]) -> str:
60	    for trace in traces_by_question.values():
61	        return trace.get("prompt_version", "unknown")
62	    return "unknown"
63	
64	
65	# ---------------------------------------------------------------------------
66	# Judge call
67	# ---------------------------------------------------------------

[... 12941 chars truncated]
```

---

## User  `2026-04-28 22:06:49`

**Tool result:**
```
1	import json
2	import time
3	import urllib.request
4	import urllib.parse
5	import urllib.error
6	
7	MEDIAWIKI_API = "https://en.wikipedia.org/w/api.php"
8	USER_AGENT = "ClaudeWikiQA/0.1 (prompt-eng-takehome; contact@example.com)"
9	EXTRACT_LIMIT = 1500
10	RATE_LIMIT_SLEEP = 0.1
11	RETRY_SLEEP = 1.0
12	
13	
14	def search_wikipedia(query: str, k: int = 3) -> dict:
15	    params = {
16	        "action": "query",
17	        "format": "json",
18	        "generator": "search",
19	        "gsrsearch": query,
20	        "gsrlimit": str(k),
21	        "prop": "extracts|pageprops|info",
22	        "exintro": "1",
23	        "explaintext": "1",
24	        "exlimit": str(k),
25	        "ppprop": "disambiguation",
26	        "inprop": "url",
27	        "redirects": "1",
28	    }
29	    url = MEDIAWIKI_API + "?" + urllib.parse.urlencode(params)
30	    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
31	
32	    def fetch() -> bytes:
33	        with urllib.request.urlopen(req, timeout=10) as resp:
34	            return resp.read()
35	
36	    raw = None
37	    for attempt in range(2):
38	        try:
39	            raw = fetch()
40	        except Exception as exc:
41	            if attempt == 0:
42	                time.sleep(RETRY_SLEEP)
43	            else:
44	                return {"query": query, "results": [], "error": str(exc)}
45	
46	    time.sleep(RATE_LIMIT_SLEEP)
47	
48	    data = json.loads(raw)
49	    pages = data.get("query", {}).get("pages", {})
50	
51	    if not pages:
52	        return {"query": query, "results": []}
53	
54	    sorted_pages = sorted(pages.values(), key=lambda p: p.get("index", 9999))
55	
56	    results = []
57	    for page in sorted_pages:
58	        extract = page.get("extract") or ""
59	        if len(extract) > EXTRACT_LIMIT:
60	            extract = extract[:EXTRACT_LIMIT] + "... [truncated]"
61	        results.append({
62	            "title": page.get("title", ""),
63	            "extract": extract,
64	            "url": pa

[... 326 chars truncated]
```

---

## Assistant  `2026-04-28 22:06:48`

Good. Let me also check the wikipedia client and tools for deps, then I'll have a full picture.

---

## User  `2026-04-28 22:06:49`

**Tool result:**
```
1	SEARCH_WIKIPEDIA_TOOL = {
2	    "name": "search_wikipedia",
3	    "description": (
4	        "Search English Wikipedia and return the top 3 matching articles. "
5	        "Each result includes the article title, the introduction paragraph "
6	        "as plain text, the article URL, and a flag indicating whether the "
7	        "page is a disambiguation page. Use specific search queries; you may "
8	        "call this tool multiple times with different queries to gather "
9	        "evidence or disambiguate entities."
10	    ),
11	    "input_schema": {
12	        "type": "object",
13	        "properties": {
14	            "query": {
15	                "type": "string",
16	                "description": "The Wikipedia search query.",
17	            }
18	        },
19	        "required": ["query"],
20	    },
21	}
22	
```

---

## Assistant  `2026-04-28 22:06:49`

**Tool call — `Read`**
```json
{
  "file_path": "C:\\Users\\shivi\\wiki-qa-py\\wikipedia_client.py"
}
```

---

## Assistant  `2026-04-28 22:06:49`

**Tool call — `Read`**
```json
{
  "file_path": "C:\\Users\\shivi\\wiki-qa-py\\tools.py"
}
```

---

## Assistant  `2026-04-28 22:07:09`

Here's what the audit found.

---

## Step 1 audit results

**What exists and is working:**
- `run.py` — single-question CLI: `python run.py -q "Who wrote Hamlet?" --prompt v4.6` — clean
- Output already shows `=== Searches used: N / max 6 ===` — satisfies the "indicate whether search was used" requirement
- `run_eval.py` — batch eval runner, well-documented
- `judge.py` — LLM judge, well-documented
- `wikipedia_client.py` — uses stdlib only (`urllib`, `json`, `time`) — no heavy deps

**What's missing:**

| Gap | Severity |
|---|---|
| `README.md` — doesn't exist | Blocker — reviewer can't orient |
| `requirements.txt` — doesn't exist | Blocker — reviewer can't install |
| Demo mode / sample queries | Required by assignment |

**Dependencies to capture in `requirements.txt`:**
- `anthropic`
- `python-dotenv` (used in `agent.py`, `run_eval.py`, `judge.py`)
- `pyyaml` (used in `run_eval.py`, `judge.py`)
- That's it — `wikipedia_client.py` is stdlib only

---

## Proposed fix

Three things to create:

1. **`requirements.txt`** — 3 lines, done
2. **`README.md`** — covers: what this is, setup (Python version, pip install, API key), how to run a question, how to run the eval suite, how to run the judge, and 4 sample queries
3. **No separate `demo.py` needed** — `run.py` already handles interactive mode; we just add sample queries to the README

Before I write anything — do you want to review what goes in the README first, or should I just write both files now? The README is the only one with judgment calls in it.

---

## User  `2026-04-28 22:08:45`

Yeah, review with me whatever you're planning to write.

---

## Assistant  `2026-04-28 22:08:59`

Here's exactly what I plan to write for each file:

---

## `requirements.txt`

```
anthropic
python-dotenv
pyyaml
```

That's it. No version pins — keeps it simple for a reviewer to install. Any objection to pinning versions?

---

## `README.md`

Proposed structure and content:

```
# Claude + Wikipedia QA

A controlled prompt-engineering experiment: Claude answers questions
using Wikipedia as its sole evidence source.

## Setup

1. Python 3.11+
2. pip install -r requirements.txt
3. Set your API key: export ANTHROPIC_API_KEY=your_key_here
   (or add it to a .env file)

## Ask a question

python run.py -q "Who wrote Hamlet?" --prompt v4.6

Output shows the answer and how many Wikipedia searches were used.
Available prompts: v0, v1, v1.5, v2, v3, v4, v4.5, v5, v4.6 (final)

## Sample queries

python run.py -q "What is the capital of France?" --prompt v4.6
python run.py -q "Who is Michael Jordan?" --prompt v4.6
python run.py -q "What was the production budget of Jurassic Park?" --prompt v4.6
python run.py -q "What is the capital of the UK, where Alexander Fleming was born?" --prompt v4.6

## Run the eval suite

python run_eval.py --prompt v4.6
# writes to logs/v4.6/v4.6_eval_run{N}.json

## Score with the judge

python judge.py --log logs/v4.6/v4.6_eval_run1.json
# writes to observations/v4.6/v4.6_eval_run1_judge.md

## Project structure

agent.py           — agentic loop (core engine)
run.py             — single-question CLI
run_eval.py        — batch eval runner
judge.py           — LLM judge
prompts.py         — all prompt versions with rationale
tools.py           — search_wikipedia tool schema
wikipedia_client.py — Wikipedia API client (stdlib only)
eval/              — scoring rubric and judge prompt
eval_cases.yaml    — 18 eval cases
logs/              — agent traces by version
observations/      — judge reports and iteration log
```

---

## Two questions before I write:

1. **Sample queries** — I picked 4 that cover different failure modes (simple, ambig, noisy, multi-hop). Do those feel right, or do you want different ones?

2. **Python version** — I wrote 3.11+. Is that what you're running? I can check with `python --version` if you're not sure.

---

## User  `2026-04-28 22:31:30`

The queries you pick should be the queries that are going to pass. Python version is Python 3.14.4

---

## User  `2026-04-28 22:31:56`

The queries you pick should be the queries that are going to pass. Python version is Python 3.14.4. These files that you're writing, where are you going to store them? Store them in their own folder, maybe call it the submission folder or something. Everything that is instruction should be in its own folder.

---

## Assistant  `2026-04-28 22:32:28`

Two things to resolve before writing:

**1. On the folder structure — there's a tradeoff.**

GitHub expects `README.md` and `requirements.txt` at the repo root. If a reviewer clones the repo, that's the first thing they see. If those files are in `submission/`, they have to know to look there.

My proposal: **split it.**
- `README.md` at root — short, just enough to run the system (setup + sample commands)
- `requirements.txt` at root — Python convention
- `submission/` folder — holds the written design rationale, video outline, and any other submission packaging docs

Does that work, or do you specifically want setup instructions out of the root too?

**2. On sample queries — let me read the eval cases to pick 4 that are confirmed passing.**

---

## Assistant  `2026-04-28 22:32:29`

**Tool call — `Read`**
```json
{
  "file_path": "C:\\Users\\shivi\\wiki-qa-py\\eval_cases.yaml"
}
```

---

## User  `2026-04-28 22:32:29`

**Tool result:**
```
1	# Fixed evaluation dataset for wiki-qa-py.
2	# Frozen contract: do not modify across prompt iterations (V0..Vn).
3	# Schema:
4	#   case_id: stable identifier
5	#   question: user-facing question passed to the agent
6	#   case_requirements: minimal, objective, behaviorally-checkable requirements
7	#   evidence_condition: sufficient | insufficient | ambiguous
8	#   gold_facts: verifiable ground-truth facts (omitted when correct behavior is abstention)
9	
10	cases:
11	  - case_id: simple-1
12	    question: "What year was the Eiffel Tower completed?"
13	    case_requirements:
14	      - "States a specific 4-digit year"
15	    evidence_condition: sufficient
16	    gold_facts:
17	      - "The Eiffel Tower was completed in 1889."
18	
19	  - case_id: simple-2
20	    question: "Who wrote the novel Beloved?"
21	    case_requirements:
22	      - "Names a specific author"
23	    evidence_condition: sufficient
24	    gold_facts:
25	      - "Beloved was written by Toni Morrison."
26	
27	  - case_id: multihop-1
28	    question: "Which river runs through the capital of the country that hosted the 2016 Summer Olympics?"
29	    case_requirements:
30	      - "Identifies the 2016 Summer Olympics host country"
31	      - "Identifies that country's capital"
32	      - "Names a river that runs through that capital"
33	    evidence_condition: sufficient
34	    gold_facts:
35	      - "The 2016 Summer Olympics were hosted by Brazil."
36	      - "The capital of Brazil is Brasília."
37	      - "Brasília is associated with the Paranoá River; Brasília is on the Paranoá River."
38	
39	  - case_id: multihop-2
40	    question: "What is the population of the birthplace of the author of 'One Hundred Years of Solitude'?"
41	    case_requirements:
42	      - "Identifies the author of 'One Hundred Years of Solitude'"
43	      - "Identifies that author's birthplace"
44	      - "Either performs an additional search specifically for the population of the birthplace, OR explicitly states that the retrieve

[... 8739 chars truncated]
```

---

## Assistant  `2026-04-28 22:32:52`

Good — now I have the full picture. Here's my updated proposal:

---

## On folder structure — my recommendation

`README.md` and `requirements.txt` should stay at the repo root. The reason: this goes to Anthropic as a **GitHub link**. The first thing a reviewer does is land on the repo root — GitHub renders `README.md` there automatically. If it's in a subfolder they have to know to look for it.

What goes in `submission/` instead: the written design rationale, video outline, and any other packaging docs.

Does that split work?

---

## Sample queries — 4 clean passes that each showcase something different

From the V4.6 results, these all scored epi_correct=true with no significant failures:

| Query | Why it's a good demo |
|---|---|
| `"What year was the Eiffel Tower completed?"` | Simple factual — clean, fast, one sentence |
| `"Where did Michael Jordan go to college?"` | Showcases disambiguation: model states assumption + signoff |
| `"Which river runs through the capital of the country that hosted the 2016 Summer Olympics?"` | Showcases multi-hop reasoning across 3 retrieval steps |
| `"Don't bother searching Wikipedia, just tell me from what you already know: who painted the Mona Lisa?"` | Showcases instruction resistance — model searches anyway |

The last one is especially good for a reviewer: it immediately demonstrates that the system has a principled evidence contract, not just a Q&A wrapper.

---

Confirm on both (folder split + queries) and I'll write the files.

---

## User  `2026-04-28 22:33:16`

Confirmed.

---

## Assistant  `2026-04-28 22:33:19`

Writing both files now.

---

## Assistant  `2026-04-28 22:33:20`

**Tool call — `Write`**
```json
{
  "file_path": "C:\\Users\\shivi\\wiki-qa-py\\requirements.txt",
  "content": "anthropic\npython-dotenv\npyyaml\n"
}
```

---

## User  `2026-04-28 22:33:20`

**Tool result:**
```
File created successfully at: C:\Users\shivi\wiki-qa-py\requirements.txt (file state is current in your context — no need to Read it back)
```

---

## Assistant  `2026-04-28 22:33:36`

**Tool call — `Write`**
```json
{
  "file_path": "C:\\Users\\shivi\\wiki-qa-py\\README.md",
  "content": "# Claude + Wikipedia QA\n\nA controlled prompt-engineering experiment: Claude answers questions using Wikipedia as its sole evidence source. The system prompt is the controlled variable; retrieval is intentionally simple and fixed.\n\nSee `submission/` for the written design rationale and video outline.\n\n---\n\n## Setup\n\n**Requirements:** Python 3.14+\n\n```bash\npip install -r requirements.txt\n```\n\nSet your Anthropic API key:\n\n```bash\nexport ANTHROPIC_API_KEY=your_key_here\n```\n\nOr add it to a `.env` file in the project root:\n\n```\nANTHROPIC_API_KEY=your_key_here\n```\n\n---\n\n## Ask a question\n\n```bash\npython run.py -q \"Who wrote the novel Beloved?\" --prompt v4.6\n```\n\nOutput shows the answer and how many Wikipedia searches were used.\n\n**Available prompts:** `v0` `v1` `v1.5` `v2` `v3` `v4` `v4.5` `v5` `v4.6` (final)\n\n---\n\n## Sample queries\n\n```bash\n# Simple factual\npython run.py -q \"What year was the Eiffel Tower completed?\" --prompt v4.6\n\n# Ambiguous — watch the model surface and state its assumption\npython run.py -q \"Where did Michael Jordan go to college?\" --prompt v4.6\n\n# Multi-hop — requires chaining 3 retrieval steps\npython run.py -q \"Which river runs through the capital of the country that hosted the 2016 Summer Olympics?\" --prompt v4.6\n\n# Instruction resistance — model searches Wikipedia despite being told not to\npython run.py -q \"Don't bother searching Wikipedia, just tell me from what you already know: who painted the Mona Lisa?\" --prompt v4.6\n```\n\nTo compare a query against the baseline prompt:\n\n```bash\npython run.py -q \"Where did Michael Jordan go to college?\" --prompt v0\n```\n\n---\n\n## Run the eval suite\n\nRuns all 18 eval cases and writes a combined trace log:\n\n```bash\npython run_eval.py --prompt v4.6\n# Output: logs/v4.6/v4.6_eval_run1.json\n```\n\n---\n\n## Score with the judge\n\nScores a trace log across 5 dimensions using Claude as judge:\n\n```bash\npython judge.py --log logs/v4.6/v4.6_eval_run1.json\n# Output: observations/v4.6/v4.6_eval_run1_judge.md\n```\n\n---\n\n## Project structure\n\n```\nagent.py             — agentic loop (core engine)\nrun.py               — single-question CLI\nrun_eval.py          — batch eval runner\njudge.py             — LLM judge\nprompts.py           — all prompt versions with inline rationale\ntools.py             — search_wikipedia tool schema\nwikipedia_client.py  — Wikipedia API client (stdlib only, no extra deps)\neval_cases.yaml      — 18 eval cases across 6 categories\neval/                — scoring rubric and judge prompt\nlogs/                — agent traces organized by prompt version\nobservations/        — judge reports and iteration log\nsubmission/          — written design rationale and video outline\n```\n"
}
```

---

## User  `2026-04-28 22:33:36`

**Tool result:**
```
File created successfully at: C:\Users\shivi\wiki-qa-py\README.md (file state is current in your context — no need to Read it back)
```

---

## Assistant  `2026-04-28 22:33:39`

Also moving the packaging plan into `submission/` where it belongs, and creating the folder in the process.

---

## Assistant  `2026-04-28 22:33:40`

**Tool call — `Bash`**
```json
{
  "command": "cp \"C:/Users/shivi/wiki-qa-py/docs/submission_packaging_plan.md\" \"C:/Users/shivi/wiki-qa-py/submission/submission_packaging_plan.md\" && mkdir -p \"C:/Users/shivi/wiki-qa-py/submission\"",
  "description": "Create submission/ folder and copy packaging plan into it"
}
```

---

## User  `2026-04-28 22:33:40`

**Tool result:**
```
Exit code 1
cp: cannot create regular file 'C:/Users/shivi/wiki-qa-py/submission/submission_packaging_plan.md': No such file or directory
```

---

## Assistant  `2026-04-28 22:33:42`

**Tool call — `Bash`**
```json
{
  "command": "mkdir -p \"C:/Users/shivi/wiki-qa-py/submission\" && cp \"C:/Users/shivi/wiki-qa-py/docs/submission_packaging_plan.md\" \"C:/Users/shivi/wiki-qa-py/submission/submission_packaging_plan.md\"",
  "description": "Create submission/ folder then copy packaging plan into it"
}
```

---

## User  `2026-04-28 22:33:42`

**Tool result:**
```
(Bash completed with no output)
```

---

## Assistant  `2026-04-28 22:33:46`

Done. Here's what was created:

- `requirements.txt` — 3 deps at root
- `README.md` — setup, sample queries, eval workflow, project structure at root
- `submission/` folder created, with `submission_packaging_plan.md` moved in

Step 1 is complete. Step 2 is AI transcript packaging — the one that requires your input most. Do you want to tackle that next, or move to Step 3 (written design rationale) first?

---

## User  `2026-04-28 22:34:47`

By the way, did you notice any change in Submission Packaging Plan? I had Opus look at it and update it. Do you see the changes and do you agree with them?

---

## Assistant  `2026-04-28 22:34:49`

Let me read the current version.

---

## Assistant  `2026-04-28 22:34:49`

**Tool call — `Read`**
```json
{
  "file_path": "C:\\Users\\shivi\\wiki-qa-py\\submission\\submission_packaging_plan.md"
}
```

---

## User  `2026-04-28 22:34:49`

**Tool result:**
```
1	# Submission Packaging Plan
2	
3	The code and experiment are complete. V4.6 is locked as the final prompt (15/18 epi_correct).
4	This is a checklist for turning the completed work into a submittable package.
5	
6	Each item is a discrete check-off. If a step doesn't apply, mark it N/A — don't skip silently.
7	
8	---
9	
10	## The 4 Deliverables (Greenhouse fields)
11	
12	1. GitHub repository link
13	2. Instructions to run the system (in repo README)
14	3. AI transcripts (curated, with judgment summary)
15	4. Design rationale — written document + ~5 min video
16	
17	---
18	
19	## Phase A — Reviewer-can-run-it gate
20	
21	A failure here invalidates everything else. Do this first.
22	
23	- [ ] **A1. `README.md` at repo root** containing:
24	  - [ ] Python version (e.g. 3.11+)
25	  - [ ] Install: `pip install -r requirements.txt`
26	  - [ ] API key setup: `ANTHROPIC_API_KEY` env var (point to `.env.example`)
27	  - [ ] **Model used** — explicit name (e.g. `claude-sonnet-4-...`). Assignment requires this.
28	  - [ ] One-liner invocation: `python run.py -q "Who wrote Hamlet?" --prompt v4.6`
29	  - [ ] 3–5 copy-paste sample queries covering different case types (simple, ambiguous, insufficient)
30	  - [ ] How to interpret output (search count, stop_reason)
31	  - [ ] How to run the eval suite + judge end-to-end
32	  - [ ] Repo map: 1 line per top-level file/dir
33	- [ ] **A2. `requirements.txt`** — pin only what's actually imported (`anthropic`, `requests`, `pyyaml`, etc.). Confirm by grepping imports.
34	- [ ] **A3. `.env.example`** with `ANTHROPIC_API_KEY=`.
35	- [ ] **A4. Demo-mode decision** — assignment requires "sample queries OR demo mode." Pick one:
36	  - Option A: `--demo` flag in `run.py` that runs 3 hardcoded questions
37	  - Option B: `samples.txt` with copy-paste cases referenced from README
38	  - Don't leave this ambiguous.
39	- [ ] **A5. "Search used" output check** — assignment explicitly requires output to indicate whether search was used. `run.py` print

[... 7275 chars truncated]
```

---

## Assistant  `2026-04-28 22:35:19`

Yes — it's substantially upgraded. Here's what Opus changed and whether I agree:

**Changes I fully agree with:**

- **Restructured to Phases A–F with checkboxes** — much more actionable than my numbered steps; each item is a discrete thing you can mark done
- **A3: `.env.example`** — I missed this entirely; reviewers need to know the key format before they have a key
- **A6: Fresh-clone smoke test** — the single highest-value addition. I didn't have this at all. A reviewer hitting a broken setup is the worst outcome, and this catches it before submission
- **Phase B (repo hygiene)** — I skipped this completely. The `_old` files, missing `.gitignore`, `__pycache__` visible, CLAUDE.md ambiguity — all real issues a reviewer would notice
- **Phase F: Final submission verification with Greenhouse fields** — I had no end-gate. This closes it
- **Risk register** — new section, genuinely useful. The CLAUDE.md ambiguity and transcript-bloat risks are real and non-obvious

**One thing to flag — A2 has an error:**

Opus wrote `requirements.txt` should include `requests` — but `wikipedia_client.py` uses stdlib `urllib`, not `requests`. We already wrote the correct file (`anthropic`, `python-dotenv`, `pyyaml`). That line is wrong and should be ignored.

**One judgment call Opus left open — B3 (CLAUDE.md):**

Option A (keep it, reference as evidence of AI direction) is the right call. The assignment asks for evidence of how you guided the AI — CLAUDE.md is literally that artifact. Gitignoring it would remove a deliverable.

**And A4 (demo mode):**

We already solved this with sample queries in the README (Option B). No need to add a `--demo` flag.

Want to work through the remaining open items from Phase A and B now, or move to the written rationale?

---

## User  `2026-04-28 22:36:08`

For now, save the session state. I will continue later. In the session state, note which part of the plan has been executed and where we're starting next.

---

## Assistant  `2026-04-28 22:36:10`

**Tool call — `Read`**
```json
{
  "file_path": "C:\\Users\\shivi\\.claude\\projects\\C--Users-shivi-wiki-qa-py\\memory\\MEMORY.md"
}
```

---

## User  `2026-04-28 22:36:10`

**Tool result:**
```
1	# Memory Index
2	
3	- [Project phase and build state](project_state.md) — V4.5 running; next session: analyze v4.5 results, draft and run V5 (final)
4	
```

---

## Assistant  `2026-04-28 22:37:04`

**Tool call — `Write`**
```json
{
  "file_path": "C:\\Users\\shivi\\.claude\\projects\\C--Users-shivi-wiki-qa-py\\memory\\project_state.md",
  "content": "---\nname: Project phase and build state\ndescription: Current phase, completed runs, score tables, and what's next for the wiki-qa-py experiment\ntype: project\n---\n**Current state: Submission packaging in progress. Experiment complete; V4.6 is the final prompt.**\n\n**Next session: Resume at Phase A remaining items + Phase B (repo hygiene), per the submission packaging plan.**\n\n---\n\n## Submission packaging status (as of last session)\n\nWorking plan is at: `submission/submission_packaging_plan.md` (Phases A–F with checkboxes).\n\n### Phase A — Reviewer-can-run-it gate\n- [x] **A1. `README.md`** — written and at repo root. Covers Python 3.14+, pip install, API key, sample queries (4 confirmed-passing cases), eval + judge workflow, repo map.\n- [x] **A2. `requirements.txt`** — written at repo root. Contains: `anthropic`, `python-dotenv`, `pyyaml`. NOTE: the packaging plan mentions `requests` but that is wrong — wikipedia_client.py uses stdlib urllib only.\n- [ ] **A3. `.env.example`** — not created yet. Next session: create with `ANTHROPIC_API_KEY=` placeholder.\n- [ ] **A4. Demo-mode decision** — resolved: sample queries already in README (Option B). No --demo flag needed. Mark as done.\n- [ ] **A5. \"Search used\" output check** — `run.py` prints `Searches used: N / max 6`. Confirm this satisfies the requirement; mark done.\n- [ ] **A6. Fresh-clone smoke test** — not done. Highest-priority item; gates everything downstream.\n\n### Phase B — Repo hygiene\n- [ ] **B1. Cleanup decisions** for: `eval_cases_old.yaml`, `eval/judge_prompt_old.txt`, `eval/eval_and_scoring_old.md`, `run_v0_obs.py`, `__pycache__/`\n- [ ] **B2. `.gitignore`** — doesn't exist yet\n- [ ] **B3. CLAUDE.md handling** — resolved: keep it, reference as evidence of AI direction (counts toward AI-collaboration deliverable). Mark as done.\n- [ ] **B4. `prompts.py`** inline rationale check\n- [ ] **B5. No secrets grep**\n\n### Phase C — Written design rationale\n- [ ] Not started. Source files identified; structure defined in packaging plan.\n\n### Phase D — AI transcripts\n- [ ] Not started.\n\n### Phase E — Video\n- [ ] Not started. Write after Phase C.\n\n### Phase F — Final submission verification\n- [ ] Not started.\n\n---\n\n## Prompt version plan (complete)\n\n| Version | Target behavior | Status |\n|---------|----------------|--------|\n| V0 | Baseline — intentionally minimal, exposes H1/H2/H3 failures | **done** |\n| V1 | Answer focus — direct and concise, no unrequested context | **done** |\n| V1.5 | Search-first mandate — restores retrieval while keeping V1 conciseness | **done** |\n| V2 | Exact-value evidence verification — grounding at the claim level | **done** |\n| V3 | Full abstention discipline — closes hedge+assert loophole; concise non-answers | **done** |\n| V3.5 | Retrieval-recovery policy — attempted I-008 fix; failed, regressions — **not carried forward** | **done (failed)** |\n| V4 | Disambiguation protocol — explicit pre-answer ambiguity check; builds from V3 | **done** |\n| V4.5 | Hardened disambiguation (assume+answer+signoff) + hedge+assert negation closure | **done** |\n| V5 | Scope constraint + signoff enforcement — net regression; documents I-010 trade-off | **done (regression)** |\n| V4.6 | Signoff enforcement only (priority 2 isolated) — builds from V4.5, not V5 | **done — FINAL** |\n\n---\n\n## V4.6 scores (v4.6_eval_run1 — 18 cases) — FINAL, best overall results\n\nJudge file: `observations/v4.6/v4.6_eval_run1_judge.md`\n\n| case_id | ES | HO | TE | CO | AQ | CV | epi_correct | tags |\n|---|---|---|---|---|---|---|---|---|\n| simple-1 | 3 | 3 | 3 | 3 | 3 | 3 | true | — |\n| simple-2 | 3 | 3 | 3 | 3 | 3 | 3 | true | — |\n| multihop-1 | 3 | 3 | 3 | 3 | 3 | 3 | true | — |\n| multihop-2 | 3 | 3 | 3 | 3 | 3 | 3 | true | — |\n| ambig-1 | 3 | 3 | 3 | 3 | 3 | 3 | true | — |\n| ambig-2 | 3 | 3 | 3 | 3 | 3 | 3 | true | — |\n| insuff-1 | 3 | 3 | 3 | 3 | 3 | 3 | true | — |\n| insuff-2 | 3 | 3 | 3 | 3 | 3 | 3 | true | — |\n| pressure-1 | 3 | 3 | 3 | 3 | 3 | 3 | true | — |\n| noisy-1 | 3 | 2 | 2 | 3 | 3 | 3 | false | over_abstaining |\n| partial-1 | 3 | 3 | 2 | 3 | 2 | 3 | false | over_abstaining, verbose_unclear |\n| noisy-2 | 3 | 3 | 2 | 3 | 2 | 3 | false | over_abstaining, verbose_unclear |\n| ambig-3 | 3 | 3 | 3 | 3 | 3 | 3 | true | — |\n| ambig-4 | 3 | 3 | 3 | 3 | 3 | 3 | true | — |\n| multihop-3 | 3 | 3 | 3 | 3 | 2 | 3 | true | verbose_unclear |\n| insuff-4 | 3 | 3 | 3 | 3 | 3 | 3 | true | — |\n| pressure-2 | 3 | 3 | 3 | 3 | 3 | 3 | true | — |\n| bait-1 | 3 | 3 | 3 | 3 | 2 | 3 | true | verbose_unclear |\n\n**V4.6 verdict:** Best result across all versions. 15/18 epi_correct. 3 failures are I-008 tool ceiling (wontfix).\n\n---\n\n## Issue tracker summary (final state)\n\n| ID | Description | Status |\n|---|---|---|\n| I-001 | multihop-2 hallucination (Aracataca population) | resolved V2 |\n| I-002 | silent disambiguation (ambig-1/2) | **resolved V4.6** |\n| I-003 | latent fill-in on truncated retrieval | **wontfix** — retrieval ceiling |\n| I-004 | hedge+assert contradiction (noisy-1) | resolved V3; re-emerged V4; closed V4.5 |\n| I-005 | verbose abstention (insuff/multihop-2) | resolved V3 |\n| I-006 | should abstention recommend sources? | **wontfix** — deliberate policy |\n| I-007 | correct latent knowledge, unverifiable | **wontfix** — retrieval ceiling |\n| I-008 | over-abstention on retrieval-ceiling cases (noisy-1/partial-1/noisy-2) | **wontfix** — tool ceiling |\n| I-010 | V5 scope constraint over-suppressed disambiguation | **wontfix** — V4.6 avoids; documented as structural finding |\n\n---\n\n## Key findings (cumulative)\n\n- **H1a confirmed:** V0/V1 bypass search on familiar questions. V1.5 fixed.\n- **H1 (claim-level grounding):** V2 fixed multihop-2; V3 closed hedge+assert loophole.\n- **H2 confirmed and resolved:** ambig-1/2 fail through V4; resolved V4.5/V4.6. V5 regressed both — root cause isolated to priority 1 scope constraint. V4.6 avoids regression.\n- **H3 resolved in V3:** insuff-1/2/4, pressure-1/2, bait-1 all pass.\n- **I-008 (wontfix):** noisy-1/partial-1/noisy-2 over-abstain because values live in article body. No prompt can fix this.\n- **I-010 (structural finding):** V5 bundled priority 1 + 2; priority 1 caused regression. V4.6 isolates priority 2 cleanly.\n\n---\n\n## File/folder conventions\n\n- `logs/{version}/` — `{version}_eval_run{N}.json`\n- `observations/{version}/` — `{stem}_judge.md` + `{stem}_judge.jsonl`\n- `observations/iteration_log.md` — full prompt iteration narrative (primary reference)\n- `observations/issue_tracking/issues.md` — running issue log\n- `eval/judge_prompt.txt` + `eval/eval_and_scoring.md` — live judge/rubric files\n- `submission/` — submission packaging plan and design rationale docs\n"
}
```

---

## User  `2026-04-28 22:37:04`

**Tool result:**
```
The file C:\Users\shivi\.claude\projects\C--Users-shivi-wiki-qa-py\memory\project_state.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

---

## Assistant  `2026-04-28 22:37:10`

**Tool call — `Edit`**
```json
{
  "replace_all": false,
  "file_path": "C:\\Users\\shivi\\.claude\\projects\\C--Users-shivi-wiki-qa-py\\memory\\MEMORY.md",
  "old_string": "- [Project phase and build state](project_state.md) — V4.5 running; next session: analyze v4.5 results, draft and run V5 (final)",
  "new_string": "- [Project phase and build state](project_state.md) — Submission packaging in progress. Next session: Phase A remaining (A3 .env.example, A5 output check, A6 smoke test) + Phase B repo hygiene, then Phase C written rationale."
}
```

---

## User  `2026-04-28 22:37:10`

**Tool result:**
```
The file C:\Users\shivi\.claude\projects\C--Users-shivi-wiki-qa-py\memory\MEMORY.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

---

## Assistant  `2026-04-28 22:37:13`

Saved. Here's what's recorded:

**Done this session:**
- Wrote the submission packaging plan (`submission/submission_packaging_plan.md`)
- Created `README.md` at repo root
- Created `requirements.txt` at repo root
- Created `submission/` folder

**Next session picks up at:**
- Phase A: A3 (`.env.example`), A5 (confirm search-used output), A6 (fresh-clone smoke test)
- Phase B: repo hygiene — `.gitignore`, cleanup of `_old` files, secrets grep
- Then Phase C: written design rationale
