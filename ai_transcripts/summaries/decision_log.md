# Decision Log — AI Collaboration Summary

**Source:** Planning chats (`chatgpt_planning.md`, `claude_planning.md`) and Claude Code sessions 01–29  
**Purpose:** Summary of the major decision topics that were discussed across AI collaboration sessions.

---

## Planning Phase — ChatGPT Chat (`chatgpt_planning.md`)

**Project framing**
The first substantive discussion was about how to frame the project. The conversation covered whether to treat this as a QA accuracy problem or as something narrower. The framing that emerged — a controlled experiment on LLM behavior — was worked out here through multiple exchanges before any code was written.

**Retrieval design**
A significant portion of the early chat addressed how much effort to put into the Wikipedia retrieval layer. The discussion covered vector databases, hybrid ranking, and MediaWiki API options, and the conversation resolved toward keeping retrieval as simple as possible. The reasoning discussed was that retrieval complexity would make it harder to attribute behavioral changes.

**Eval dimension design**
The longest discussion in the ChatGPT chat was about which dimensions to evaluate. The conversation moved through several versions: an initial list, a discussion about whether "helpful," "useful," and "delightful" from the assignment language required separate dimensions, a debate about merging groundedness and citation validity, and a debate about whether search behavior should be a scored dimension or just tracked as telemetry. The conversation settled on five dimensions and agreed to treat search behavior as instrumentation only.

**Prompt version progression**
The chat covered what a natural sequence of prompt versions would look like — starting from a weak baseline and adding behavioral constraints one at a time. Several alternative orderings were discussed before settling on a progression that moved from conciseness to grounding to abstention to ambiguity handling.

**LLM-as-judge scope**
There was an extended exchange about whether the project should go deep on LLM-as-judge reliability, including judge consistency testing, adversarial answer probing, and prompt sensitivity. The conversation pulled back from that direction, agreeing that judge engineering was not the primary signal and that a simple judge rubric was sufficient.

---

## Planning Phase — Claude Chat (`claude_planning.md`)

**Hypothesis formulation**
The three core hypotheses (H1 evidence grounding, H2 complex questions, H3 honesty under insufficient evidence) were worked out in this chat. The conversation covered multiple drafts and refinements, including a discussion about splitting H2 into ambiguity and multi-hop as distinct failure modes and moving helpfulness bias into H3.

**Eval methodology mix**
This chat included a discussion about which scoring method to use for each dimension — deterministic reference matching, LLM-as-judge, or human spot-check. The conversation settled on using all three with clearly defined roles and noted the Sonnet-as-system, Opus-as-judge asymmetry and the rationale for it.

**Eval case count and category weighting**
The conversation covered how many cases to design and how to distribute them across categories. The discussion settled on approximately 25 hand-authored cases weighted toward diagnostic categories rather than simple factual questions.

**Phased plan and iteration discipline**
The bulk of this chat was a phase-by-phase project plan. The conversation covered sequencing, what to defer, what to lock in early, and the rule that every prompt change should be tied to a logged failure rather than being speculative.

---

## Execution Phase — Claude Code Sessions

**Tool schema (Session 02)**
The session covered creating `tools.py` as a frozen contract, with the explicit agreement that the schema would not change across prompt versions. The discussion was brief — the decision was already made in planning.

**Eval harness and judge design (Sessions 07–08)**
These sessions covered how to build the eval runner and judge pipeline, what inputs the judge would see, and how to format output. Session 08 specifically covered adding human-readable output alongside the structured judge scores.

**V1 regression (Session 10)**
The session was a direct comparison of V1 and V0 judge outputs. The discussion identified why V1 performed worse on certain dimensions and what the prompt change should be to address it without losing the conciseness gains.

**Eval case expansion (Session 13)**
The session covered which new cases were needed to test behaviors that would be targeted in later prompt versions. The discussion identified gaps in the original case set and what categories needed more coverage.

**V4.5 analysis and V5 direction (Session 16)**
The session covered reading V4.5 judge output, identifying remaining failure modes, and discussing whether a V5 was warranted and what it should target.

**Final packaging scope (Sessions 18–22)**
These sessions covered what the submission deliverables were, how to structure the documentation, and what the narrative arc of the rationale should be. The discussion involved comparing the actual submission against the original assignment checklist.
