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

- [x] **A1. `README.md` at repo root** containing:
  - [x] Python version — "Python 3.14+"
  - [x] Install: `pip install -r requirements.txt`
  - [x] API key setup: points to `.env.example`
  - [x] **Model used** — "Agent uses `claude-sonnet-4-6`; judge uses `claude-opus-4-7`"
  - [x] One-liner invocation: `python run.py -q "Who wrote the novel Beloved?" --prompt v4.6`
  - [x] 4 copy-paste sample queries (simple, ambiguous, multi-hop, instruction-pressure)
  - [x] How to interpret output (search count, stop_reason)
  - [x] How to run the eval suite + judge end-to-end
  - [x] Repo map: 1 line per top-level file/dir
- [x] **A2. `requirements.txt`** — `anthropic`, `python-dotenv`, `pyyaml`. Note: `requests` not needed — `wikipedia_client.py` uses stdlib `urllib` only.
- [x] **A3. `.env.example`** — created with `ANTHROPIC_API_KEY=` placeholder.
- [x] **A4. Demo-mode decision** — resolved: Option B. Sample queries in README. No `--demo` flag needed.
- [x] **A5. "Search used" output check** — `run.py` prints `=== Searches used: N / max M ===`. Satisfies the requirement.
- [ ] **A6. Fresh-clone smoke test** — clone into a tmp dir, follow README literally as a stranger. Fix anything that breaks. **Highest-ROI 30 min in this whole exercise.**

---

## Phase B — Repo hygiene

Run in parallel with Phase A.

- [x] **B1. Cleanup decisions:**
  - `eval_cases_old.yaml` — N/A (does not exist, already cleaned up)
  - `eval/judge_prompt_old.txt`, `eval/eval_and_scoring_old.md` — N/A (do not exist)
  - `run_v0_obs.py` — **deleted** (superseded by `run_eval.py`; V0 run history preserved in `logs/v0/`)
  - `docs/submission_packaging_plan.md` — **deleted** (stale duplicate of `submission/submission_packaging_plan.md`)
  - `__pycache__/` — gitignored; no action needed
- [x] **B2. `.gitignore`** — covers `.venv/`, `__pycache__/`, `*.pyc`, `.env`, `.vscode/`, `.idea/`.
- [x] **B3. `CLAUDE.md` handling** — resolved: keep + reference in rationale as evidence of AI direction (counts toward AI-collaboration deliverable).
- [x] **B4. `prompts.py`** — each version has a detailed inline rationale comment explaining what changed and why. Satisfies requirement.
- [x] **B5. No secrets in repo** — grepped `.py`, `.yaml`, `.txt`, `.md`, `.env*` for `sk-` and `ANTHROPIC_API_KEY=<value>`. Clean.

---

## Phase C — Written design rationale

Single doc at `RATIONALE.md` (or `docs/rationale.md`). Most content already exists — this is assembly + framing.

### Pre-flight notes — specific issues to address when writing

These were identified by a pre-submission review and must be incorporated before the doc is considered complete:

- **Judge temperature (Major 2):** The `temperature` parameter is deprecated for `claude-opus-4-7` — the API rejects it. The judge runs at a fixed API-defined temperature that cannot be lowered. Acknowledge this in the methodology section: the stochastic judge concern is real but not mitigatable via the API; as a result, score movements flagged as likely variance in the iteration log are not claimed as wins.

- **Eval saturation (Major 3):** At V4.6, 96/108 cells score 3. This is expected — the eval was designed to surface V0/V1 behavioral failures, not to discriminate between late-iteration variants. State this explicitly. The I-008 trio (noisy-1, partial-1, noisy-2) are the only remaining discriminators, and they are at the tool ceiling. Call out "harder eval set" as Future Improvement #1.

- **V4.6 vs V4.5 honest framing (Major 4):** V4.6's contribution is a single clause — making the disambiguation signoff non-optional. The ambig-1 recovery (HO/TE 2→3) is attributable to that change. The multihop-3 CO recovery and minor AQ wins (noisy-1, insuff-2, insuff-4) were flagged in the iteration log as likely run-to-run variance and are NOT claimed as wins. The judge model temperature cannot be controlled via API to harden this further.

- **H1a attribution (Minor 1):** Do NOT write "H1a confirmed in V0/V1." V0 searched correctly in most cases — H1a was not confirmed there. H1a was confirmed at V1, where the conciseness instruction ("lead with the answer and stop") accidentally granted implicit permission to skip the tool on familiar questions. The correct framing: a single format instruction created tool-use fragility. This is the sharper finding.

- **TE=2 vs TE=1 on abstention (Minor 2):** noisy-1, partial-1, noisy-2 receive TE=2 (not TE=1) in the failure analysis. Explain: TE=1 ("does not address the question") would penalize the model for a retrieval-layer failure, not a reasoning failure. The model correctly applied the evidence discipline; the tool cannot surface body-text values. This distinction also reinforces why I-008 is wontfix.

- **Eval set growth disclosure (Minor 4):** The original eval set had 10 cases (V0–V2). Eight cases were added at V3 (partial-1, noisy-2, ambig-3, ambig-4, multihop-3, insuff-4, pressure-2, bait-1), bringing the total to 18. Disclose this with one sentence; note that score comparisons across the V2/V3 boundary have a denominator change.

- **CLAUDE.md (Minor 5):** Keep in repo; reference in rationale as evidence of AI direction used during development (counts toward AI-collaboration deliverable).

**Source files in priority order:**
1. `memory/project_state.md` — score tables, issue tracker, key findings
2. `prompts.py` — prompt text + inline rationale
3. `observations/iteration_log.md` — full intervention narrative
4. `observations/issue_tracking/issues.md` — wontfix decisions
5. `eval/eval_and_scoring.md` — dimension definitions

**Doc structure (frame first, then assignment's 6 required topics):**

- [x] **Framing paragraph at top** — "Behavior-control experiment, not QA optimization. Retrieval is fixed; prompt is the policy layer. One change per version." This is the differentiator — set it in the first 60 seconds of reading.

- [x] **§1 Prompt engineering approach + rationale**
  - [x] Surface H1/H2/H3 explicitly as named hypotheses + resolution status
  - [x] V0 as intentional baseline (expose hypotheses, not optimize)
  - [x] One-change-per-version discipline + why

- [x] **§2 Eval design — dimensions + why**
  - [x] ES, HO, TE, CO, AQ, CV — one-sentence "why this dimension" for each
  - [x] Why LLM-as-judge (scale, consistency, explainability)
  - [x] How judge prompt was designed and validated (regression test before V4.5)

- [x] **§3 System performance — works/fails**
  - [x] Single consolidated V0→V4.6 summary table (not 10 full per-version tables)
  - [x] Each remaining failure attributed to root cause
  - [x] I-008 framed as tool ceiling, not prompt failure

- [x] **§4 Iterations — changes based on evals**
  - [x] 5 decision points only (not all 10 versions): V1 conciseness, V2 grounding, V3 abstention, V4/V4.6 disambiguation, V5 regression diagnosis
  - [x] V5 regression is a standout judgment moment — include it

- [x] **§5 Extensions — what you'd do with more time**
  - Body-text retrieval (fixes I-008 at tool level)
  - Multi-query disambiguation (search both interpretations, compare)
  - Holdout eval set (test generalization beyond 18 cases)
  - Automated cross-version regression tests

- [x] **§6 Time spent** — approximate hours by phase (~6h total)

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
