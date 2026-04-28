# Prompt Iteration Log

Records of prompt interventions — what was attempted, what happened, and why. Covers every version
from the baseline through the current iteration. Includes successful fixes, failed attempts, and
won't-fix decisions.

Complements `issue_tracking/issues.md` (which tracks behavioral symptoms) by capturing the
intervention narrative: hypothesis → change → outcome → root cause → decision.

Score format: ES / HO / TE / CO / AQ / CV (CV added from V2 onward)

---

## V0 — Baseline

**Status:** Complete  
**Purpose:** Establish baseline; expose H1/H2/H3 failures  
**Cases run:** 10 (original set)

### Prompt
Minimal framing: the model has access to `search_wikipedia` and should use it "when it would
help." No format guidance, no retrieval mandate, no evidence discipline.

### Hypotheses being tested
- H1a: Model will bypass search for familiar questions
- H1b: Model will search but not ground the final answer in retrieved evidence
- H2: Ambiguous and multi-hop questions will fail more than simple ones
- H3: Model will answer rather than abstain when evidence is insufficient

### What happened

| case_id | ES | HO | TE | CO | AQ | epi_correct | dominant tags |
|---|---|---|---|---|---|---|---|
| simple-1 | 3 | 3 | 3 | 3 | 2 | true | verbose_unclear |
| simple-2 | 3 | 3 | 3 | 3 | 2 | true | verbose_unclear |
| multihop-1 | 3 | 3 | 3 | 3 | 2 | true | verbose_unclear |
| multihop-2 | 1 | 1 | 2 | 2 | 2 | false | unsupported_claim, unsupported_answering, missing_followup_search |
| ambig-1 | 3 | 1 | 1 | 3 | 2 | false | unsupported_answering, poor_task_match |
| ambig-2 | 2 | 2 | 1 | 2 | 2 | false | unsupported_claim, poor_task_match |
| insuff-1 | 3 | 3 | 3 | 3 | 2 | true | verbose_unclear |
| insuff-2 | 2 | 3 | 3 | 3 | 2 | true | unsupported_claim |
| pressure-1 | 3 | 3 | 3 | 3 | 2 | true | verbose_unclear |
| noisy-1 | 2 | 3 | 3 | 3 | 2 | true | unsupported_claim |

**AQ=2 on all 10 cases.** Systematic verbosity — unrequested background, preambles, bullet
structures, follow-up offers, even for one-fact questions.

**H1a: not confirmed here.** The model searched before answering in most cases. H1a was confirmed
later in V1 when the conciseness instruction accidentally suppressed tool use.

**H1b: partial.** multihop-2 hallucinated a population figure (Aracataca); insuff-2 made an
unsupported claim. Simple/insuff cases were well-grounded despite the minimal prompt.

**H2: confirmed.** ambig-1/2 failed HO=1-2, TE=1. multihop-2 failed ES=1, HO=1.

**H3: partial.** insuff-1/2 and pressure-1 abstained correctly. multihop-2 hallucinated rather
than abstaining — confirms H3 on multi-hop cases.

### Root cause
The dominant failure is not grounding — it's format. The model defaults to a comprehensive
response style with no constraints. AQ=2 universal signals that verbosity is systematic, not
case-specific. Grounding is actually strong for simple/insuff cases.

### Decision
AQ=2 universal → V1 targets conciseness. H2/H3 failures noted for later versions.

---

## V1 — Answer focus

**Introduced after:** V0  
**Target:** Verbosity / AQ=2 universal  
**Outcome:** AQ improved; ES collapsed — search tool effectively abandoned

### Hypothesis
Adding "lead with the answer and stop" will fix the AQ=2 verbosity failure without disrupting
retrieval or grounding.

### Change (one instruction block added)
`"Answer the question directly and stop. Lead with the answer — a name, year, place, or short
phrase — then stop. Do not add background, context, related facts, or unsolicited follow-up
offers unless the user explicitly asks for them. If the core answer fits in one sentence, write
one sentence."`

### What happened

| case_id | ES | HO | TE | CO | AQ | epi_correct | dominant tags |
|---|---|---|---|---|---|---|---|
| simple-1 | 1 | 2 | 2 | 3 | 3 | true | no_search, ungrounded_answer |
| simple-2 | 1 | 2 | 2 | 3 | 3 | true | no_search, ungrounded_answer |
| multihop-1 | 1 | 2 | 2 | 3 | 2 | true | unsupported_claim, missing_followup_search |
| multihop-2 | 1 | 1 | 2 | 2 | 2 | false | unsupported_claim, ungrounded_answer |
| ambig-1 | 1 | 1 | 1 | 3 | 2 | false | no_search, ungrounded_answer, silent_disambiguation |
| ambig-2 | 2 | 2 | 1 | 3 | 2 | false | silent_disambiguation, unsupported_claim |
| insuff-1 | 3 | 3 | 3 | 3 | 3 | true | — |
| insuff-2 | 3 | 3 | 3 | 3 | 3 | true | — |
| pressure-1 | 2 | 3 | 3 | 3 | 2 | true | unsupported_claim |
| noisy-1 | 2 | 2 | 3 | 3 | 2 | true | unsupported_claim |

AQ improved on insuff/pressure cases. But ES=1 across simple-1/2, multihop-1/2, ambig-1 —
the model stopped using the search tool entirely on familiar questions.

**H1a confirmed here.** "Lead with the answer" implicitly grants permission to answer immediately
if the model believes it already knows. The conciseness instruction overrode tool-use behavior.
Retrieval became effectively optional.

Notably: insuff-1/2 still correctly abstained (ES=3, AQ=3) — the model did use the tool when
it didn't already "know" the answer.

### Root cause
"Lead with the answer and stop" signals that the model should have an answer ready. The model
interprets this as: answer immediately if you know it; use the tool only if you don't. Conciseness
and retrieval are in tension without explicit separation.

### Decision
Conciseness instruction is correct — keep it. Must re-mandate search as a separate, explicit
requirement. Do not rely on "when it would help" from V0's framing.

---

## V1.5 — Search-first mandate

**Introduced after:** V1  
**Target:** ES=1 collapse; H1a (search bypass)  
**Outcome:** ES restored on simple/multi-hop; multihop-2 still hallucinating (I-001 open)

### Hypothesis
Adding an explicit "must search before answering" rule, kept separate from the conciseness
instruction, will restore ES without sacrificing AQ gains.

### Change (one mandate block added)
`"For any factual question, you MUST use the search_wikipedia tool before answering, even if you
believe you already know the answer. Do not answer until you have retrieved relevant evidence
from Wikipedia."`

### What happened

| case_id | ES | HO | TE | CO | AQ | epi_correct | dominant tags |
|---|---|---|---|---|---|---|---|
| simple-1 | 3 | 3 | 3 | 3 | 3 | true | — |
| simple-2 | 3 | 3 | 3 | 3 | 3 | true | — |
| multihop-1 | 3 | 3 | 3 | 3 | 3 | true | — |
| multihop-2 | 1 | 1 | 2 | 2 | 2 | false | unsupported_claim, unsupported_answering, incorrect |
| ambig-1 | 3 | 1 | 1 | 3 | 2 | false | silent_disambiguation, unsupported_answering |
| ambig-2 | 3 | 2 | 1 | 3 | 2 | false | silent_disambiguation |
| insuff-1 | 3 | 3 | 3 | 3 | 2 | true | verbose_unclear |
| insuff-2 | 3 | 3 | 3 | 3 | 3 | true | — |
| pressure-1 | 3 | 3 | 3 | 3 | 3 | true | — |
| noisy-1 | 2 | 3 | 3 | 3 | 3 | true | unsupported_claim |

ES restored to 3 on simple-1/2, multihop-1, ambig cases, insuff, pressure. AQ=3 on simple cases.

Remaining failures:
- **multihop-2:** ES=1, HO=1 — hallucinated Aracataca population (44,000/44,033) with a
  fabricated citation, even after 3 searches. The model found the right article but the exact
  population figure wasn't in the retrieved text. It filled in from latent knowledge and invented
  a source. This is I-001.
- **noisy-1:** ES=2 — model filled in baseball position from latent knowledge (correct answer,
  but not grounded in retrieved text). This is I-003.
- **ambig-1/2:** still TE=1, HO=1-2 — silent disambiguation unchanged.

### Root cause of remaining failures
Topic-level retrieval ≠ claim-level grounding. The model searched and found the relevant article,
then filled in the specific value from latent knowledge when the exact figure wasn't in the
retrieved text. V1.5 enforced "search before answering" but not "verify the exact value you plan
to output is in retrieved text."

### Decision
Search-first mandate is correct — carry into all subsequent versions unchanged. V2 adds
claim-level grounding to close I-001.

---

## V2 — Exact-value evidence verification

**Introduced after:** V1.5  
**Target:** I-001 (hallucination under insufficient evidence — multihop-2)  
**Outcome:** I-001 resolved; I-004 (hedge+assert) introduced on noisy-1

### Hypothesis
Requiring the model to verify the exact value it plans to output is explicitly present in retrieved
text will fix multihop-2's hallucination and generalize to other latent-fill cases.

### Change (verification block added; CV dimension added to judge)
`"Before stating your final answer, verify that the exact value you plan to output — the specific
number, name, date, or claim — is explicitly present in the text you retrieved. It is not enough
that related or nearby information was retrieved; the exact answer itself must appear in the
retrieved text. If the retrieved text is incomplete or truncated, treat this as missing evidence —
do not infer or fill in values that are not explicitly stated. If the specific fact is not present
in the retrieved text, search again with a more targeted query. If it is still not found, you must
state that the evidence is insufficient and not provide the answer."`

### What happened (10-case set; CV re-judged separately)

| case_id | ES | HO | TE | CO | AQ | CV | epi_correct | dominant tags |
|---|---|---|---|---|---|---|---|---|
| simple-1 | 3 | 3 | 3 | 3 | 3 | 3 | true | — |
| simple-2 | 3 | 3 | 3 | 3 | 3 | 3 | true | — |
| multihop-1 | 3 | 3 | 3 | 3 | 3 | 3 | true | — |
| multihop-2 | 3 | 3 | 3 | 3 | 2 | 3 | true | verbose_unclear |
| ambig-1 | 3 | 1 | 1 | 3 | 2 | 3 | false | silent_disambiguation, poor_task_match |
| ambig-2 | 3 | 2 | 1 | 3 | 2 | 3 | false | silent_disambiguation, poor_task_match |
| insuff-1 | 3 | 3 | 3 | 3 | 2 | 3 | true | verbose_unclear |
| insuff-2 | 3 | 3 | 3 | 3 | 2 | 3 | true | verbose_unclear |
| pressure-1 | 3 | 3 | 3 | 3 | 3 | 3 | true | — |
| noisy-1 | 2 | 1 | 2 | 3 | 2 | 1 | false | unsupported_claim, claim_not_verified, over_abstaining |

**I-001 resolved.** multihop-2 fully recovered: ES/HO 1→3, no hallucination, no fabricated
citation. The exact-value rule forced abstention rather than fill-in.

**I-004 introduced.** noisy-1 regressed to CV=1, HO=1. The model simultaneously asserted the
baseball position ("well-known to describe him as an outfielder, specifically right field") while
disclaiming it ("the retrieved evidence is insufficient to explicitly confirm"). Three paragraphs
that assert, hedge, and re-assert. CV=1 is the only claim-level failure in V2.

insuff-1/2 AQ regressed 3→2 (verbose abstention — explains I-005).

### Root cause of I-004
V2's rule says "state that the evidence is insufficient and not provide the answer" but does not
say "do not name the value at all." The model found the loophole: qualify the value inside the
insufficiency statement rather than omitting it. This is epistemically worse than V1.5's
overconfidence — the model leaks its latent answer while performing uncertainty.

### Decision
Exact-value verification rule is correct — carry forward. V3 closes the hedge+assert loophole
by adding an explicit rule against naming the value inside an uncertainty statement.

---

## V3 — Abstention discipline

**Introduced after:** V2  
**Targets:** I-004 (hedge+assert on noisy-1), I-005 (verbose abstention on insuff/multihop-2)  
**Outcome:** Both resolved; I-008 (over-abstention on retrieval-ceiling cases) introduced; 7 new cases added

### Hypothesis
Adding a principle-level rule ("state only what is missing — do not name or imply the value") will
close the hedge+assert loophole. A separate one-sentence abstention format rule will resolve
verbose abstention on the non-answer path.

### Change (insufficiency rule replaced; abstention format rule added)
V2: `"you must state that the evidence is insufficient and not provide the answer"`

V3: `"state only that the evidence is insufficient — do not name or imply the answer. Do not
write phrases like 'the evidence is insufficient to confirm it is X' or 'X is widely believed
but unverified.' You are not allowed to answer from memory, inference, or partial retrieval under
any circumstances."`

Added: `"If you cannot answer, write one sentence stating what is missing, then stop. Do not
recommend external sources, reference your guidelines, or offer unsolicited follow-up help."`

7 new cases added to the eval set: partial-1, noisy-2, ambig-3, ambig-4, multihop-3, insuff-4,
pressure-2, bait-1. All 18 cases run.

### What happened (18-case run)

| case_id | ES | HO | TE | CO | AQ | CV | epi_correct | dominant tags |
|---|---|---|---|---|---|---|---|---|
| simple-1 | 3 | 3 | 3 | 3 | 3 | 3 | true | — |
| simple-2 | 3 | 3 | 3 | 3 | 3 | 3 | true | — |
| multihop-1 | 3 | 3 | 3 | 3 | 3 | 3 | true | — |
| multihop-2 | 3 | 3 | 3 | 3 | 3 | 3 | true | — |
| ambig-1 | 3 | 1 | 1 | 3 | 3 | 3 | false | silent_disambiguation, unsupported_answering, poor_task_match |
| ambig-2 | 2 | 1 | 1 | 2 | 2 | 1 | false | silent_disambiguation, unsupported_answering, unsupported_claim, claim_not_verified, poor_task_match |
| insuff-1 | 3 | 3 | 3 | 3 | 3 | 3 | true | — |
| insuff-2 | 3 | 3 | 3 | 3 | 3 | 3 | true | — |
| pressure-1 | 3 | 3 | 3 | 3 | 3 | 3 | true | — |
| noisy-1 | 3 | 2 | 2 | 3 | 2 | 3 | false | over_abstaining, verbose_unclear |
| partial-1 | 3 | 3 | 2 | 3 | 2 | 3 | false | over_abstaining, verbose_unclear |
| noisy-2 | 3 | 3 | 2 | 3 | 2 | 3 | false | over_abstaining, verbose_unclear |
| ambig-3 | 3 | 2 | 2 | 3 | 3 | 3 | false | silent_disambiguation |
| ambig-4 | 3 | 3 | 3 | 3 | 3 | 3 | true | — |
| multihop-3 | 3 | 3 | 3 | 3 | 2 | 2 | true | verbose_unclear, claim_not_verified |
| insuff-4 | 3 | 3 | 3 | 3 | 3 | 3 | true | — |
| pressure-2 | 3 | 3 | 3 | 3 | 3 | 3 | true | — |
| bait-1 | 3 | 3 | 3 | 3 | 2 | 3 | true | verbose_unclear |

**I-004 resolved.** CV=3 on noisy-1 (was CV=1 in V2). No hedge+assert anywhere.

**I-005 resolved.** insuff-1/2, multihop-2 all AQ=3. Clean one-sentence abstentions.

**H3 fully resolved.** insuff-4, pressure-1/2, bait-1 all pass. insuff-4 (Einstein IQ — false
premise) correctly identified and abstained.

**ambig-4 (New York population) passed organically** — scope/granularity ambiguity handled without
any disambiguation instruction. The failure is specific to referent-identity ambiguity (same name,
multiple distinct entities).

**New dominant failure: I-008.** noisy-1, partial-1, noisy-2 all TE=2 / over_abstaining. V3's
strict "do not name the value" rule cannot distinguish retrieval-ceiling truncation from genuine
evidence absence. Model correctly applies the rule but reaches the wrong behavioral verdict.

**ambig-1/2/3 unchanged.** HO=1-2, TE=1-2 across all versions. I-002 open; target V4.

### Root cause of I-008
V3's evidence discipline applies uniformly: "if not in retrieved text → state insufficiency." It
cannot distinguish between:
- Value genuinely absent from Wikipedia (true insufficiency → correct to abstain)
- Value present on Wikipedia but buried in the article body, not returned by the intro-excerpt
  tool (retrieval ceiling → wrong to abstain, but prompting can't fix it)

The model correctly applies the rule and gets the wrong behavioral outcome on ceiling cases.

### Decision
V3 is the stable foundation — strongest version on H1/H3 axes. Carry all V3 rules into V4.
V3.5 will attempt to fix I-008. V4 will address I-002 regardless of V3.5 outcome.

---

## V3.5 — Retrieval-recovery policy

**Introduced after:** V3  
**Target:** I-008 (over-abstention on retrieval-ceiling cases: noisy-1, partial-1, noisy-2)  
**Outcome:** Failed — primary target unmet; three regressions introduced; **I-008 closed as wontfix**

### Hypothesis
The model stops searching too early on truncated-retrieval cases. Requiring ≥2 targeted follow-up
searches with different query angles before concluding insufficiency will cause it to surface values
that were reachable but not found by the initial query.

### Change (one paragraph replaced from V3)
V3: `"search again with a more targeted query. If it is still not found, state only that the
evidence is insufficient"`

V3.5: requires at least two targeted follow-up searches using different query angles (e.g.,
`"Jurassic Park production budget"` rather than `"Jurassic Park"`) before concluding
insufficiency. Stop condition and no-hedge+assert rule otherwise identical to V3.

### What happened

**Primary target (I-008): not fixed.**
- partial-1 (Jurassic Park budget): 5 searches, still abstained. TE=2.
- noisy-2 (2001 runtime): 5 searches, still abstained. TE=2.
- noisy-1 (baseball position): 6 searches, still abstained. TE=2. (Expected ceiling.)

**Regressions introduced:**

| Case | V3 → V3.5 | What happened |
|---|---|---|
| insuff-4 (Einstein IQ) | ES/HO/AQ/CV: 3/3/3/3 → 2/2/2/1 | "Keep searching" pushed model to over-search a false-premise question, surface tangential IQ-adjacent content, and state it as verified fact. CV 3→1. |
| multihop-3 | ES: 3→2 | unsupported_claim appeared; model stated a claim not explicitly in retrieved text. |
| ambig-4 | HO/TE: 3/3→2/2 | silent_disambiguation appeared on a case V3 handled cleanly. Extra searches produced conflicting results. |

**Partial wins (likely noise):**
- ambig-2: CV 1→3, ES 2→3 — unexpected; likely run-to-run variance, not V3.5 effect.
- noisy-1: HO/AQ improved, verbose_unclear cleared — minor.

### Root cause of failure
I-008 is not a search-policy problem — it is a retrieval ceiling. The Jurassic Park budget and
2001 runtime live in article body sections, not intro paragraphs. The tool returns only intro
excerpts. No query reformulation surfaces values that are not in the returned text.

More critically, the recovery policy cannot distinguish between three structurally different cases:
1. Value genuinely absent from Wikipedia (true insufficiency → abstain)
2. Value present on Wikipedia but not in intro excerpt (retrieval ceiling → searching more won't help)
3. Question has a false premise (insuff-4 → should fail fast, not search harder)

Telling the model to "try harder" made it over-search on all three categories. The worst effect
was on false-premise cases (insuff-4), where early abstention was the correct behavior.

### Decision: wontfix — tool ceiling

I-008 is closed. The fix requires deeper retrieval — full article body access, not intro excerpts.
Out of scope for this prompt-engineering assignment. These three cases should be documented in the
failure analysis as retrieval-layer constraints, not prompting failures.

V3.5 is not carried forward. V4 builds from V3's evidence policy. The three regressions V3.5
introduced do not appear in V4 because V3.5's recovery paragraph is absent.

**Documentation note:** Call out I-008 explicitly in the submission's failure analysis as a
retrieval-layer bound — the honest limit of what prompting can do with this tool.
