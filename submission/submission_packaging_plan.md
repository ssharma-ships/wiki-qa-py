# Submission Packaging Plan

The code and experiment are complete. V4.6 is locked as the final prompt (15/18 epi_correct).
This is a checklist for turning the completed work into a submittable package.

Each item is a discrete check-off. If a step doesn't apply, mark it N/A — don't skip silently.

---

## The 4 Deliverables (Greenhouse fields)

1. GitHub repository link
2. Instructions to run the system (in repo README)
3. AI transcripts (curated, with judgment summary)
4. Design rationale — written document + ~5 min video

---

## Phase A — Reviewer-can-run-it gate

A failure here invalidates everything else. Do this first.

- [ ] **A1. `README.md` at repo root** containing:
  - [ ] Python version (e.g. 3.11+)
  - [ ] Install: `pip install -r requirements.txt`
  - [ ] API key setup: `ANTHROPIC_API_KEY` env var (point to `.env.example`)
  - [ ] **Model used** — explicit name (e.g. `claude-sonnet-4-...`). Assignment requires this.
  - [ ] One-liner invocation: `python run.py -q "Who wrote Hamlet?" --prompt v4.6`
  - [ ] 3–5 copy-paste sample queries covering different case types (simple, ambiguous, insufficient)
  - [ ] How to interpret output (search count, stop_reason)
  - [ ] How to run the eval suite + judge end-to-end
  - [ ] Repo map: 1 line per top-level file/dir
- [ ] **A2. `requirements.txt`** — pin only what's actually imported (`anthropic`, `requests`, `pyyaml`, etc.). Confirm by grepping imports.
- [ ] **A3. `.env.example`** with `ANTHROPIC_API_KEY=`.
- [ ] **A4. Demo-mode decision** — assignment requires "sample queries OR demo mode." Pick one:
  - Option A: `--demo` flag in `run.py` that runs 3 hardcoded questions
  - Option B: `samples.txt` with copy-paste cases referenced from README
  - Don't leave this ambiguous.
- [ ] **A5. "Search used" output check** — assignment explicitly requires output to indicate whether search was used. `run.py` prints `Searches used: N`. Confirm that satisfies the requirement, or add explicit `Search used: yes/no`.
- [ ] **A6. Fresh-clone smoke test** — clone into a tmp dir, follow README literally as a stranger. Fix anything that breaks. **Highest-ROI 30 min in this whole exercise.**

---

## Phase B — Repo hygiene

Run in parallel with Phase A.

- [ ] **B1. Cleanup decisions** — for each, choose: keep as-is / move to `archive/` / delete:
  - `eval_cases_old.yaml`
  - `eval/judge_prompt_old.txt`, `eval/eval_and_scoring_old.md`
  - `run_v0_obs.py`
  - `__pycache__/`
- [ ] **B2. `.gitignore`** — covers `__pycache__/`, `.env`, `*.pyc`, IDE files.
- [ ] **B3. `CLAUDE.md` handling** — these are instructions to the AI, not the reviewer. Decide:
  - Option A: keep + reference in README as evidence of how AI was directed (counts toward AI-collaboration deliverable)
  - Option B: gitignore for the submission branch
- [ ] **B4. `prompts.py`** — confirm each version has an inline rationale comment (1–2 lines explaining what changed and why).
- [ ] **B5. No secrets in repo** — grep for `sk-`, `ANTHROPIC_API_KEY=` followed by a value, etc.

---

## Phase C — Written design rationale

Single doc at `RATIONALE.md` (or `docs/rationale.md`). Most content already exists — this is assembly + framing.

**Source files in priority order:**
1. `memory/project_state.md` — score tables, issue tracker, key findings
2. `prompts.py` — prompt text + inline rationale
3. `observations/iteration_log.md` — full intervention narrative
4. `observations/issue_tracking/issues.md` — wontfix decisions
5. `eval/eval_and_scoring.md` — dimension definitions

**Doc structure (frame first, then assignment's 6 required topics):**

- [ ] **Framing paragraph at top** — "Behavior-control experiment, not QA optimization. Retrieval is fixed; prompt is the policy layer. One change per version." This is the differentiator — set it in the first 60 seconds of reading.

- [ ] **§1 Prompt engineering approach + rationale**
  - [ ] Surface H1/H2/H3 explicitly as named hypotheses + resolution status
  - [ ] V0 as intentional baseline (expose hypotheses, not optimize)
  - [ ] One-change-per-version discipline + why

- [ ] **§2 Eval design — dimensions + why**
  - [ ] ES, HO, TE, CO, AQ, CV — one-sentence "why this dimension" for each
  - [ ] Why LLM-as-judge (scale, consistency, explainability)
  - [ ] How judge prompt was designed and validated (regression test before V4.5)

- [ ] **§3 System performance — works/fails**
  - [ ] Single consolidated V0→V4.6 summary table (not 10 full per-version tables)
  - [ ] Each remaining failure attributed to root cause
  - [ ] I-008 framed as tool ceiling, not prompt failure

- [ ] **§4 Iterations — changes based on evals**
  - [ ] 5 decision points only (not all 10 versions): V1 conciseness, V2 grounding, V3 abstention, V4/V4.6 disambiguation, V5 regression diagnosis
  - [ ] V5 regression is a standout judgment moment — include it

- [ ] **§5 Extensions — what you'd do with more time**
  - Body-text retrieval (fixes I-008 at tool level)
  - Multi-query disambiguation (search both interpretations, compare)
  - Holdout eval set (test generalization beyond 18 cases)
  - Automated cross-version regression tests

- [ ] **§6 Time spent** — actual hours, tracked during execution per phase. Not a post-hoc guess.

---

## Phase D — AI transcripts

Run in parallel with Phase C.

- [ ] **D1. `TRANSCRIPTS.md` (or `ai_transcripts/`) — curated judgment summary is the primary artifact**, raw transcripts are appendix. The assignment warns: "Purely AI-generated work without human judgment will not pass." Curation IS the judgment evidence.
- [ ] **D2. Judgment summary (1–2 pages)** with concrete moments:
  - V4.6 vs V5 isolation decision
  - I-008 wontfix call (tool ceiling, not prompt failure)
  - Retrieval-held-fixed framing decision
  - V3.5 failure → revert to V3 → V4
  - Where I pushed back on Claude's suggestions
- [ ] **D3. Scrub for secrets** — API keys, personal email, internal paths, anything sensitive.
- [ ] **D4.** Cross-link from rationale doc and README.

---

## Phase E — Video (~5 min)

Write only after rationale doc is done; use it as the script.

| Segment | Duration | Content |
|---|---|---|
| Frame the experiment | 0:45 | "I treated the prompt as a controllable policy. Retrieval is fixed. Here's why." |
| Show a baseline failure | 0:45 | Run ambig-1 on V0 live — silent disambiguation, explain what's wrong |
| Eval design | 0:45 | Show the 6 dimensions and judge output for one case |
| Iteration arc | 1:15 | Score table V0→V4.6, name 3 core fixes, show V5 regression as structural finding |
| Final result + failure | 0:45 | Run ambig-1 on V4.6 (full pass), then noisy-1 (tool ceiling — honest failure) |
| Extensions + time | 0:45 | What you'd do next + how long this took |

- [ ] **E1. Pre-record privacy check** — terminal has no API keys, no `.env` open, no internal URLs visible.
- [ ] **E2. Recording tool decided** (Loom / OBS / QuickTime). Test audio first.
- [ ] **E3. One practice run, then record.** Don't perfectionism past 2 takes.
- [ ] **E4. Confirm video link is shareable to external reviewers** (not "anyone inside org X").

---

## Phase F — Final submission verification

- [ ] **F1. Second fresh-clone walkthrough** after all changes are in.
- [ ] **F2. Greenhouse field check** — every field has an artifact:
  - [ ] GitHub repo URL (public)
  - [ ] Run instructions (point to README in repo)
  - [ ] AI transcripts link or attached
  - [ ] Written rationale link or attached
  - [ ] Video link
- [ ] **F3. Time spent confirmed** in rationale doc.
- [ ] **F4. Click submit.**

---

## Sequencing

1. **Phase A first** — blocks reviewers from running anything; A6 (smoke test) gates everything downstream.
2. **Phase B parallel with A** — independent cleanup work.
3. **Phase C after A** — so the doc references what's actually in the repo.
4. **Phase D parallel with C** — uniquely yours, can't be delegated to extracted artifacts; uses different source material than C.
5. **Phase E after C** — uses C as the script.
6. **Phase F last** — verification only.

---

## Risk register

- **Windows path conventions** in README — call out OS-specifics or test on a Unix-y shell.
- **Secret leaks in video / transcripts** — D3 and E1 are the controls; don't skip.
- **Transcript bloat** — raw dumps without curation read as "purely AI-generated." D1 framing protects against this.
- **Video re-take loop** — budget for 2 takes max; the doc-as-script approach prevents this.
- **`_old` file confusion** — reviewer sees `eval_cases_old.yaml` next to `eval_cases.yaml` and wonders. B1 forces a decision.
- **CLAUDE.md ambiguity** — reviewer sees AI instructions and wonders if it's documentation. B3 forces a decision.
