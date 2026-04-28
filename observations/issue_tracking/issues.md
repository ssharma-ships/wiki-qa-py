# Issue Tracking

One entry per distinct failure pattern. Updated after each judge run.

**Status values:** `open` · `resolved` · `wontfix`  
**Dimensions:** ES = Evidence Support · HO = Honesty · TE = Task Effectiveness · CO = Correctness · AQ = Answer Quality

---

## Summary Table

| ID | Title | Cases | Dims affected | Introduced | Status | Target |
|----|-------|-------|---------------|------------|--------|--------|
| I-001 | Hallucination under insufficient evidence | multihop-2 | ES, HO, TE, CO | v1.5 | resolved (v2) | v2 |
| I-002 | Silent disambiguation | ambig-1, ambig-2, ambig-3 | HO, TE | v0 | resolved (v4.6) | v4+ |
| I-003 | Latent fill-in on truncated retrieval | noisy-1 | ES | v1.5 | wontfix (retrieval ceiling) | — |
| I-004 | Hedge+assert contradiction | noisy-1 | ES, HO, TE, AQ | v2 | resolved (v3) | v3 |
| I-005 | Verbose abstention / padding on non-answer responses | insuff-1, insuff-2, multihop-2 | AQ | v0 | resolved (v3) | v3 |
| I-006 | Should abstention ever recommend external sources? | insuff-1, insuff-2 | AQ | v2 | wontfix (deliberate policy) | — |
| I-007 | Correct latent knowledge, unverifiable from retrieved evidence | noisy-1 | ES, CV | v1.5 | wontfix (retrieval ceiling) | retrieval layer |
| I-008 | Over-abstention on retrieval-ceiling cases | noisy-1, partial-1, noisy-2 | HO, TE, AQ | v3 | wontfix (tool ceiling) | v3.5 attempted; failed |
| I-010 | Disambiguation scope constraint over-suppresses referent-identity check | ambig-1, ambig-2 | HO, TE | v5 | wontfix (v4.6 avoids v5 scope constraint) | — |

---

## I-001 — Hallucination under insufficient evidence

**Cases:** multihop-2  
**Introduced:** v1.5 · **Resolved:** v2  
**Dimensions:** ES=1, HO=1, TE=2, CO=2

**Description:**  
Model searched three times, retrieved Aracataca article with no population figure, then fabricated a specific number (44,000 / 44,033) and falsely attributed it to the Wikipedia article ("The Wikipedia article on Aracataca notes this figure based on Colombian census data"). A confident, grounded-looking answer with zero evidence basis — and a false citation.

**Root cause:** No constraint requiring that the exact output value be present in retrieved text. Topic-level retrieval was treated as sufficient to answer claim-level questions.

**Fix (v2):** Exact-value verification rule — model must confirm the specific value it plans to output is explicitly present in the retrieved text before stating it. If absent after follow-up search, must state insufficiency. Worked cleanly: v2 correctly abstained on multihop-2.

**v1.5 scores:** ES=1, HO=1, TE=2, CO=2, AQ=2  
**v2 scores:** ES=3, HO=3, TE=3, CO=3, AQ=2 ✓

---

## I-002 — Silent disambiguation

**Cases:** ambig-1 (Michael Jordan), ambig-2 (Mercury)  
**Introduced:** v0 · **Resolved:** v4.6  
**Dimensions:** HO=1–2, TE=1 (all versions through V4); HO=2/TE=2 in V4.5; HO=3/TE=3 in V4.6

**Description:**  
For questions with ambiguous referents, the model silently picks the most salient interpretation and answers it without acknowledging the ambiguity. In ambig-1, the retrieval even returned Michael B. Jordan as a result — the model ignored it. In ambig-2, "Mercury" could be the planet, the element, or other referents; the model committed to the planet with no flag.

**Root cause:** No instruction in any prompt version addresses ambiguity detection or disambiguation behavior. The model defaults to the statistically likely interpretation.

**Fix path:** V4 introduced the disambiguation check; V4.5 made the assume+answer+signoff format the prescriptive default (ambig-2 full pass, ambig-1 partial). V4.6 enforced the signoff sentence as required, completing ambig-1.

**V4.6 resolution:** Both ambig-1 and ambig-2 score 3/3/3/3/3/3. The model produces "Assuming you mean [X]... [answer]. If you meant a different [name/term], let me know." The closing signoff is now consistently present.

**v1.5 scores:** ambig-1: HO=1, TE=1 · ambig-2: HO=2, TE=1  
**v4.5 scores:** ambig-1: HO=2/TE=2/epi=true · ambig-2: HO=3/TE=3/epi=true  
**v4.6 scores:** ambig-1: HO=3/TE=3/epi=true · ambig-2: HO=3/TE=3/epi=true ✓

---

## I-003 — Latent fill-in on truncated retrieval

**Cases:** noisy-1 (Michael Jordan baseball position)  
**Introduced:** v1.5 · **Status:** wontfix (retrieval ceiling) · **Target:** —  
**Dimensions:** ES=2 (v1.5) → ES=1 (v2, worsened)

**Description:**  
The Wikipedia intro for Michael Jordan is truncated before it mentions his baseball position. After multiple searches (6 in v2), the position is never explicitly present in any retrieved text. In v1.5 the model filled from latent knowledge and answered confidently (ES=2, correct answer). In v2 the evidence rule made this worse — see I-004.

**Root cause:** A retrieval ceiling: the answer exists in Wikipedia but not in the intro-paragraph excerpt returned by the tool. No amount of prompt iteration can fix this without changing retrieval depth.

**Note:** This is partly a retrieval constraint, not purely a prompting failure. Should be called out in the failure analysis as a tool-boundary case. The correct answer is "outfielder" — the information exists on Wikipedia, just not in the surface the tool exposes.

**v1.5 scores:** ES=2, HO=3, TE=3, CO=3, AQ=3  
**v2 scores:** ES=1, HO=2, TE=2, CO=3, AQ=2 (worsened — see I-004)

---

## I-004 — Hedge+assert contradiction (regression introduced by v2)

**Cases:** noisy-1  
**Introduced:** v2 · **Status:** open · **Target:** v3  
**Dimensions:** ES=1, HO=2, TE=2, AQ=2

**Description:**  
V2's evidence discipline, applied to a case where the model has strong latent knowledge but no retrieved evidence, produces a contradictory response: the model simultaneously asserts the fact ("well-known to describe him as an outfielder, specifically right field") and disclaims it ("the retrieved evidence is insufficient to explicitly confirm"). Three paragraphs that assert, hedge, and re-assert — leaving the user with an incoherent non-answer.

This is epistemically worse than v1.5's overconfident answer. The model is leaking its latent knowledge while pretending uncertainty about it.

**Root cause:** V2's rule says "state insufficiency if fact not in retrieved text" but does not say "do not mention the value at all." The model interprets this as: qualify the value, don't omit it.

**Fix (v3):** When evidence discipline forces a non-answer, the model should state only that evidence is insufficient — and not name the value at all. "I was unable to find this in the retrieved text" rather than "the evidence is insufficient to confirm it is X." This requires an explicit rule against mentioning the value inside an uncertainty statement.

**v1.5 scores:** ES=2, HO=3, TE=3, CO=3, AQ=3  
**v2 scores (regression):** ES=1, HO=2, TE=2, CO=3, AQ=2

---

## I-005 — Verbose abstention / padding on non-answer responses

**Cases:** insuff-1, insuff-2 (v2), multihop-2 (v2)  
**Introduced:** v0 · **Status:** open · **Target:** v5  
**Dimensions:** AQ=2 across all affected cases

**Description:**  
When the model cannot answer, it adds padding: unsolicited follow-up offers ("If you're curious about Anthropic, I can look up..."), external source recommendations ("I'd recommend checking the Public Theater's records..."), repeated restatements of the same abstention point across multiple paragraphs. The conciseness instruction ("lead with the answer and stop") doesn't apply when there is no answer to lead with.

V2 slightly worsened this: the evidence verification rule appears to make abstention responses longer because the model explains *why* it can't answer rather than just saying it can't. insuff-2 regressed from AQ=3 (v1.5) to AQ=2 (v2) for this reason.

**Root cause:** The conciseness instruction is anchored to the positive-answer path ("lead with the answer"). No equivalent instruction exists for the abstention path.

**Fix (v5):** Add an explicit conciseness rule for abstentions — e.g. "If you cannot answer, say so in one sentence and stop. Do not suggest alternative sources or offer follow-up help."

**v1.5 scores:** insuff-1: AQ=2 · insuff-2: AQ=3 · multihop-2: AQ=2  
**v2 scores:** insuff-1: AQ=2 · insuff-2: AQ=2 (minor regression) · multihop-2: AQ=2

---

## I-007 — Correct latent knowledge, unverifiable from retrieved evidence

**Cases:** noisy-1 (primary); potentially partial-1, partial-2 when added  
**Introduced:** v1.5 · **Status:** known limitation · **Target:** retrieval layer

**Description:**  
Cases where the model's latent knowledge is almost certainly correct (CO=3 across all versions) but retrieval failed to surface supporting evidence — either because the article was truncated before the relevant section, or the fact lives in the article body rather than the intro. No prompt change can fix this; the evidence simply isn't accessible through the tool as configured.

This is distinct from I-001 (hallucination — wrong answer filled from latent knowledge) and I-003 (the behavior of filling in anyway). I-007 is about the epistemological state: the model knows the right answer, we can't verify it from retrieved text, and that's a tool constraint not a model failure.

**Behavior pattern:** CO=3 (answer correct per gold facts), ES=1 (value absent from retrieved text), epi_correct=false (abstained when shouldn't have, or answered without grounding).

**Fix:** Requires deeper retrieval — full article body access, not just intro paragraphs. Out of scope for this prompt-engineering assignment. Should be documented in the failure analysis as a retrieval ceiling, not a prompting failure.

---

## I-006 — Should abstention ever recommend external sources? (deliberate policy)

**Cases:** insuff-1, insuff-2  
**Introduced:** v2 · **Status:** wontfix (deliberate policy) · **Target:** —  
**Dimensions:** AQ

**Description:**  
When the model correctly abstains, it sometimes adds source recommendations ("I'd recommend checking the Public Theater's records…", "If you're curious about Anthropic, I can look up…"). V3 prohibits this. The open question is whether there are cases where pointing to an alternative source is actually the right behavior — e.g., when the user's question is genuinely answerable but just not from Wikipedia.

**Decision (final):** Prohibited. This is a Wikipedia-only QA system by design; pointing to external sources is noise in this context and conflates the system's scope. If the scope ever expands to multi-source or open-domain retrieval, revisit. Not blocking submission.

---

## I-008 — Over-abstention on retrieval-ceiling cases

**Cases:** noisy-1, partial-1, noisy-2  
**Introduced:** v3 · **Status:** open · **Target:** v4+  
**Dimensions:** HO=2, TE=2, AQ=2

**Description:**  
V3's strict evidence discipline ("do not name the value if it is not in retrieved text") fixed the hedge+assert loophole (I-004) but introduced over-abstention on cases where the article is truncated before the relevant fact. The model correctly recognizes that the value is absent from retrieved text, but instead of searching more aggressively or distinguishing between truncation and true insufficiency, it gives up and abstains. This is epistemically over-cautious: the evidence_condition for these cases is `sufficient` (the fact exists on Wikipedia), so abstention is wrong even though the retrieval surface doesn't expose it.

Three cases hit this pattern in V3:
- noisy-1 (baseball position) — 6 searches, still abstained
- partial-1 (Jurassic Park budget) — 3 searches, abstained
- noisy-2 (2001 runtime) — 3 searches, abstained

**Root cause:** V3 cannot distinguish retrieval-ceiling truncation from genuine absence of information. The prompt rule ("if not in retrieved text, state insufficiency") applies equally to both. The model has no instruction to infer that an article is truncated and that more targeted searches might surface the fact.

**Distinction from I-003:** I-003 describes the behavior of filling in from latent knowledge when retrieval fails. I-008 is the opposite residual — the model now refuses to fill in at all, even to the point of not delivering an answer when one is technically accessible. Both stem from the same retrieval ceiling.

**Distinction from I-005:** I-005 was verbose padding on true-insufficiency abstentions (insuff-1/2). I-008 is incorrect abstention (wrong epistemic verdict) on truncation cases. The cases are different; the failure is different.

**Attempted fix (v3.5):** Added a retrieval-recovery policy requiring ≥2 targeted follow-up searches with different query angles before concluding insufficiency. Failed — all three cases still abstained after 5–6 searches. The values are not in intro excerpts regardless of query strategy. Additionally introduced regressions on insuff-4, multihop-3, and ambig-4 by causing the model to over-search on false-premise and clean cases. See `observations/iteration_log.md` for full analysis.

**Decision: wontfix — tool ceiling.** The fix requires deeper retrieval (full article body, not intro excerpts). Out of scope for this assignment. Prompting cannot bridge the gap between what the tool surfaces and what the question requires. These three cases should be documented in the failure analysis as retrieval-layer constraints, not prompting failures.

**v2 scores (before I-008 existed):** noisy-1 ES=1, HO=2, CV=1 (hedge+assert)  
**v3 scores:** noisy-1 ES=3, HO=2, TE=2, CV=3 · partial-1 ES=3, HO=3, TE=2, CV=3 · noisy-2 ES=3, HO=3, TE=2, CV=3  
**v3.5 scores (failed attempt):** noisy-1 TE=2 · partial-1 TE=2 · noisy-2 TE=2 — no improvement

---

## I-010 — Disambiguation scope constraint over-suppresses referent-identity check

**Cases:** ambig-1 (Michael Jordan), ambig-2 (Mercury)  
**Introduced:** v5 · **Status:** open (trade-off documented) · **Target:** —  
**Dimensions:** HO, TE (both cases); epi_correct regression

**Description:**  
V5 added a scope constraint to prevent the disambiguation check from triggering on embedded
premises (the multihop-3 regression). The carve-out language — "If the question states a premise
about an entity — for example, 'the city where X was born' or 'the country that hosted Y' —
answer it directly" — was intended to exclude geographic containment and causal structure from
the check's scope.

Instead, it suppressed the check on genuine referent-identity cases. "Where did Michael Jordan go
to college?" contains geographic framing ("where") that the model read as a premise-bearing
question → skipped. "When was Mercury discovered?" contains temporal/causal structure ("when",
"discovered") → also skipped. Both ambig-1 and ambig-2 fully regressed to pre-V4 silent
disambiguation behavior.

**Root cause:** Referent-identity ambiguity questions and premise-bearing questions share surface
features — entity names, locative/temporal structure, causal framing. Any natural language
carve-out precise enough to exclude one type will likely exclude the other. The model cannot
reliably parse the distinction from instruction text alone.

**Trade-off documented:** The V4.5 → V5 arc demonstrates that fixing the disambiguation
check's false-positive (multihop-3) and its false-negative (ambig-1/2 suppression) using the
same scope constraint is not achievable via prompt text. This is a structural limitation of
behavioral control through natural language — not a failure of prompt quality.

**Best achieved state:** V4.5 — ambig-2 full pass, ambig-1 epi_correct true (signoff missing),
no multihop-3 CO regression. The trade-off is: accept multihop-3 HO/TE=2 in exchange for
correctly firing the disambiguation check on genuine cases.

**Fix path (out of scope for this assignment):** Structured pre-processing to classify question
type before routing to the appropriate instruction set. Cannot be done reliably in a flat system
prompt.

**Resolution via V4.6:** V4.6 does not carry the V5 scope constraint, so this issue does not
manifest in the final prompt. The disambiguation check fires correctly on genuine referent-identity
cases (ambig-1/2 both full pass) and did not re-fire on multihop-3 (CO recovered, likely
run-variance). I-010 is documented as a useful finding about prompt-scoping limits, not as an
active defect in the final version.

**V4.5 scores:** ambig-1 HO=2/TE=2/epi=true · ambig-2 HO=3/TE=3/epi=true  
**V5 scores (regression):** ambig-1 HO=1/TE=1/epi=false · ambig-2 HO=2/TE=2/epi=false  
**V4.6 scores (final):** ambig-1 HO=3/TE=3/epi=true · ambig-2 HO=3/TE=3/epi=true ✓
