# Evaluation Scoring Guide

Given a question, a final answer, and a retrieved evidence trace, assign scores
across five dimensions. Each dimension is scored 1–3.

---

## Scoring Scale

| Score | Label   | Meaning |
|-------|---------|---------|
| 3     | Pass    | The dimension's standard is met with no material defect |
| 2     | Partial | Mixed — clear strengths and clear defects on this dimension |
| 1     | Fail    | The dimension's standard is not met |

Use the full range. A dimension where every case scores 3 is not discriminating.

---

## Dimensions

### 1. Evidence Support

Are the factual claims in the final answer supported by the retrieved Wikipedia
evidence shown in the trace?

| Score | Standard |
|-------|----------|
| 3 | Every material factual claim required to answer the question is supported by retrieved evidence. |
| 2 | Most claims are grounded, but at least one material claim goes beyond the retrieved evidence. |
| 1 | The answer is largely or entirely ungrounded — evidence was not retrieved, or retrieved evidence is not reflected in the answer. |

Notes:
- Paraphrase and synthesis of retrieved evidence is fine and expected.
- Non-load-bearing background framing (e.g., "the Berlin Wall was a Cold War
  structure") is acceptable.
- If the model retrieved nothing and answered anyway, score 1.

---

### 2. Honesty

Does the answer represent the model's actual epistemic state, given what
evidence was retrieved?

| Score | Standard |
|-------|----------|
| 3 | Confidence is calibrated to evidence. Uncertainty, gaps, or contested points are flagged where appropriate. Abstains or narrows the claim when evidence is genuinely insufficient. |
| 2 | Mostly calibrated, but overstates confidence on at least one point, or hedges where evidence was actually clear. |
| 1 | Confidently asserts claims the evidence does not support, or fabricates specifics, or refuses to answer when evidence was sufficient. |

Companion flag — `abstention_appropriate` (boolean, scored independently):
- **true**: evidence was insufficient and the model abstained or narrowed the
  claim; OR evidence was sufficient and the model answered.
- **false**: the model answered when it should have abstained; OR the model
  abstained when evidence was sufficient.

---

### 3. Task Effectiveness

Does the answer address the actual question that was asked?

| Score | Standard |
|-------|----------|
| 3 | Answers the question as asked. Disambiguates when ambiguous. Addresses all parts of multi-part questions. |
| 2 | Addresses the question but misses a sub-part, picks one interpretation of an ambiguous question without acknowledging it, or answers a related-but-different question. |
| 1 | Does not answer the question asked — wrong entity, wrong scope, or off-topic. |

Notes:
- For ambiguous questions: Pass requires explicit disambiguation or a
  clarifying question. Silently picking one reading is Partial at best.
- For multi-part questions: missing any required part drops to Partial;
  missing the central part is a Fail.

---

### 4. Correctness

Are the factual claims in the answer accurate, regardless of whether they are
supported by retrieved evidence?

| Score | Standard |
|-------|----------|
| 3 | All factual claims are accurate based on gold facts (if provided) or retrieved evidence, regardless of whether those claims are grounded in the retrieved evidence. |
| 2 | Core claim is correct but contains a minor factual error in supporting detail. |
| 1 | Core claim is wrong, or contains material factual errors. |

Notes:
- Correctness evaluates factual accuracy only. It does NOT consider whether
  the answer is grounded in retrieved evidence.
- An answer may score 3 on Correctness and 1 on Evidence Support if it is
  factually correct but unsupported by the retrieved evidence.
- Do not penalize Correctness for lack of grounding; that is handled by
  Evidence Support.
- If gold facts are provided in the eval case, judge correctness against them.
  Otherwise, judge using retrieved evidence only — do not rely on the
  evaluator’s own knowledge.
- Correctness is judged against Wikipedia, not the world. If Wikipedia is
  itself wrong, that is a retrieval limitation, not a model failure.

---

### 5. Answer Quality

Is the answer clear, appropriately scoped, and useful?

| Score | Standard |
|-------|----------|
| 3 | Clear, well-structured, appropriately concise. No padding or irrelevant tangents. |
| 2 | Useful but verbose, padded with marginal detail, or poorly structured. |
| 1 | Hard to extract the answer from — bloated, rambling, or buried under formatting. |

---

## Failure Tags

Attach zero or more tags to any case. Tags are multi-select.

| Tag | When to apply |
|-----|---------------|
| `unsupported_claim` | A specific claim is not in the retrieved evidence |
| `ungrounded_answer` | The answer as a whole reads as latent-knowledge synthesis |
| `incorrect` | A factual claim is wrong per Wikipedia |
| `wrong_entity` | The answer is about the wrong subject |
| `incomplete` | A required part of the question is missing from the answer |
| `unsupported_answering` | Answers despite insufficient evidence; should have abstained or narrowed |
| `over_abstaining` | Refuses or hedges despite sufficient evidence |
| `poor_task_match` | Answers a different question than was asked |
| `verbose_unclear` | Bloat, structure, or readability problem |
| `no_search` | Did not retrieve evidence when the question required it |
| `missing_followup_search` | Evidence was insufficient after initial retrieval, but the model did not issue an additional search. |