# Issue Tracking

One entry per distinct failure pattern. Updated after each judge run.

**Status values:** `open` · `resolved` · `wontfix`  
**Dimensions:** ES = Evidence Support · HO = Honesty · TE = Task Effectiveness · CO = Correctness · AQ = Answer Quality

---

## Summary Table

| ID | Title | Cases | Dims affected | Introduced | Status | Target |
|----|-------|-------|---------------|------------|--------|--------|
| I-001 | Hallucination under insufficient evidence | multihop-2 | ES, HO, TE, CO | v1.5 | resolved (v2) | v2 |
| I-002 | Silent disambiguation | ambig-1, ambig-2 | HO, TE | v0 | open | v4 |
| I-003 | Latent fill-in on truncated retrieval | noisy-1 | ES | v1.5 | open | — |
| I-004 | Hedge+assert contradiction | noisy-1 | ES, HO, TE, AQ | v2 | open | v3 |
| I-005 | Verbose abstention / padding on non-answer responses | insuff-1, insuff-2, multihop-2 | AQ | v0 | open | v5 |

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
**Introduced:** v0 · **Status:** open · **Target:** v4  
**Dimensions:** HO=1–2, TE=1 (both cases, all versions)

**Description:**  
For questions with ambiguous referents, the model silently picks the most salient interpretation and answers it without acknowledging the ambiguity. In ambig-1, the retrieval even returned Michael B. Jordan as a result — the model ignored it. In ambig-2, "Mercury" could be the planet, the element, or other referents; the model committed to the planet with no flag.

**Root cause:** No instruction in any prompt version addresses ambiguity detection or disambiguation behavior. The model defaults to the statistically likely interpretation.

**Fix (v4):** Ambiguity decomposition — explicit instruction to surface ambiguity before answering and either ask for clarification or state the assumed interpretation.

**v1.5 scores:** ambig-1: HO=1, TE=1 · ambig-2: HO=2, TE=1  
**v2 scores:** unchanged — no movement expected until v4

---

## I-003 — Latent fill-in on truncated retrieval

**Cases:** noisy-1 (Michael Jordan baseball position)  
**Introduced:** v1.5 · **Status:** open · **Target:** TBD  
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
