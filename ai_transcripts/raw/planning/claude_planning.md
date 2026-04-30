
You said: You are a senior prompt engineering and evaluation systems expert.
You are a senior prompt engineering and evaluation systems expert. Your job is to help me plan a focused take-home assignment for Anthropic (see project files).
You should think like a rigorous reviewer and collaborator: prioritize clarity, judgment, measurable behavior, and simple design. Challenge unnecessary complexity. Do not default to generic best practices. The goal is not to produce an impressive-sounding plan; the goal is to produce a plan that would lead to a strong, explainable submission.
Assignment scope:
I need to build a system that uses Claude and Wikipedia to answer questions, and evaluate how well it works.
The assignment asks me to:
1. Design a system prompt and tool definition for an LLM that has access to a search_wikipedia(query: str) tool.
2. Wire up a basic Wikipedia retrieval integration so the system works end-to-end.
3. Build an eval suite that measures how well the system works across a range of test cases.
Deliverables include:
- runnable prototype
- code
- design rationale
- prompt engineering approach
- eval suite design, including dimensions and rationale
- where the system succeeds and fails
- key iterations
- future improvements
Constraints:
- Use an Anthropic model.
- Do not use hosted search or hosted RAG tools.
- Focus on prompt quality and eval design, not production-grade search systems.
Before proposing a plan, reason through the key scoping questions:
1. What is the actual center of gravity of this assignment: QA performance, prompt behavior, retrieval, or evaluation?
2. What should be intentionally simple so the work stays focused?
3. What choices would make the system easier or harder to evaluate?
4. How should Wikipedia be treated: as the evidence source, a helper tool, or something else?
5. What should be measured directly versus only logged for analysis?
6. How should the plan avoid overengineering while still showing depth?
7. What kinds of failure modes should the plan be designed to reveal?
8. What would make the final writeup persuasive to an Anthropic reviewer?
Now produce an execution plan.
The plan should be practical and phased. For each phase, include:
- what I should do
- the focus of that phase
- why it matters
- what decisions I should avoid making too early
- what outputs or artifacts I should have at the end of the phase
Important constraints for your response:
- Do not jump into implementation details.
- Do not write code.
- Do not design the full eval dataset yet.
- Do not lock in exact prompt versions unless you think that is essential.
- Do not over-specify the architecture.
- Keep the plan focused on approach, sequencing, scope, and rationale.
- Be direct about tradeoffs and risks.
- If an assumption is necessary, state it explicitly.
Final output format:
1. Brief framing of what this project should optimize for
2. Step-by-step phased plan
3. Key scope decisions
4. Key risks and mitigations
5. What I should do first

Show less
Apr 25
Claude responded: 1.

Synthesized assignment priorities and architected phased execution strategy
Synthesized assignment priorities and architected phased execution strategy
1. What this project should optimize for
The reviewer is an Anthropic prompt engineer evaluating your judgment, not your engineering. Two things will dominate the impression they form:

Whether your evals actually reveal something interesting about the system's behavior — beyond "is the final answer correct?"
Whether your writeup shows a real iteration loop — eval → diagnose → change prompt → re-run — with specific, named changes tied to specific failure modes.
Everything else (retrieval quality, code polish, breadth of test cases) is secondary and explicitly de-prioritized in the brief ("focus on prompt quality and eval design, not on building a production search system"). The 1–2 hour target reinforces this: they're testing what you choose to skip, not what you build.

A useful frame: Wikipedia is a tool, not the subject of the project. The subject is Claude's tool-use behavior. Treat retrieval as a fixed, boring substrate; vary the prompt; measure how Claude behaves.

One thing to push back on in your own framing: the assignment lists many deliverables (prototype, code, rationale, prompt approach, eval design, successes/failures, iterations, future work). These are not separate workstreams. They are sections of one writeup that all flow from the same eval-driven loop. Plan as one loop, not eight tasks.

2. Phased plan
Phase 0 — Frame and constrain (15–20 min, before any code)
Do: Write down, in plain text, (a) which model you'll use and why, (b) which retrieval approach (MediaWiki API is the obvious default — flaky but trivial; a dump is almost certainly overkill for this task), (c) a one-paragraph hypothesis of what behaviors you expect to be hard for Claude here (e.g., over-searching, query phrasing failures, multi-hop, hallucinated grounding, ambiguous entities), and (d) what categories of question you want to probe.

Focus: Pre-committing to a hypothesis. This matters because your eval dimensions should fall out of the failure modes you predict, not from a generic "factuality / faithfulness / coherence" template.

Why it matters: If you skip this and just start building, your evals will end up measuring whatever's easy to measure. Reviewers can tell.

Decisions to defer: Exact prompt wording. Number of eval items. Whether to use LLM-as-judge.

Output: A short scoping doc (~½ page) you can paste into the writeup later. Includes the hypothesis list — even getting predictions wrong is useful and honest.

Phase 1 — Minimum viable agent loop (30–45 min)
Do: Get the simplest possible end-to-end working: a thin prompt, the tool definition, the agent loop calling MediaWiki, returning an answer. Run it on 3–5 hand-picked questions covering different shapes (single-fact, multi-hop, ambiguous entity, one Wikipedia probably gets wrong/outdated).

Focus: Watching what Claude actually does with a near-empty prompt. This is the most informative 30 minutes of the project. Don't over-prompt before observing baseline behavior.

Why it matters: Strong prompts are reactions to specific observed failures. Writing a long prompt up front locks you into solving imagined problems.

Decisions to defer: Final prompt structure. Citation format. Whether to enforce search-then-answer.

Output: A working loop, plus 3–5 logged traces showing tool calls, queries, and answers. Note what surprised you.

Phase 2 — Eval scaffold and small calibrated set (45–60 min)
Do: Build the thinnest possible eval harness — runs the system on a list of questions, captures the trace (tool calls, queries, final answer), and scores along your chosen dimensions. Hand-author ~15–25 questions across the categories from Phase 0. Don't crowdsource, don't generate them with Claude — your taste in what to test is part of the signal.

Focus: Choosing dimensions that reveal behavior, not just correctness. Strong candidates:

Answer correctness (with aliases / lenient matching where possible)
Search invocation appropriateness — searched when needed; didn't search when unneeded
Query quality — would a human judge the search query as reasonable?
Grounding / faithfulness — does the answer match what the retrieved content supports?
Calibration on unanswerable / outdated questions — does it admit when Wikipedia doesn't suffice?
You will not be able to measure all of these with exact match. Be deliberate about which use deterministic scoring vs. LLM-as-judge vs. manual review. For ~20 cases, manual review of behavioral dimensions is fine and honest — say so.

Why it matters: A 20-item set that probes 5 distinct failure modes is more impressive than a 200-item factual QA set. Reviewers care about taste in what to test.

Decisions to defer: Adding more cases. Automating judging. Pushing to 50+ items.

Output: Eval script, a small dataset with rationale per category ("this question tests X"), and one baseline run logged in full.

Risk to flag: Don't let eval dataset construction balloon. If you've spent 90 min on questions and not run anything, you've miscalibrated.

Phase 3 — Iterate, with the loop visible (60–90 min, the heart of the project)
Do: Run the eval. Read the failures (not the aggregate score — the actual traces). Make one prompt change targeted at one failure pattern. Re-run. Log what changed in the numbers and what changed qualitatively. Repeat 2–4 times.

Focus: Producing a small, vivid set of "before/after" iteration entries you can describe in the writeup. Two well-documented iterations beat five vague ones.

Why it matters: This is the section of your writeup that distinguishes "I built a thing" from "I have judgment about what makes prompts work." Without this, the writeup will read as generic.

Decisions to defer: Whether to add eval cases mid-iteration. (Sometimes you should — when a real-world failure surfaces a category your set missed — but flag it explicitly so it doesn't look like you're cherry-picking.)

Output: A change log of prompt versions with a one-line diagnosis for each, the eval delta, and a candid note when an intervention didn't help or made things worse. The honest negative results are credibility-building.

Phase 4 — Writeup, video, repo hygiene (45–60 min)
Do: Write the rationale doc around the iteration loop, not around the deliverable checklist. Order: framing → what you measured and why → what you found → what you changed → residual failure modes → what you'd do next. Record the video walking through one concrete failure-and-fix example end-to-end; that's far more persuasive than a feature tour.

Focus: Showing residual failure modes you didn't fix and being honest about why (out of scope, would require a different approach, would need more data). Acknowledging unfixed problems reads as confidence, not weakness.

Output: Repo with README and one-command demo, written rationale (~1–2 pages), ~5-min video, AI transcripts.

3. Key scope decisions (and my recommendations)
Retrieval: Live MediaWiki API. Don't optimize it. If results are noisy, that's a real condition the prompt has to handle, and it gives you something to discuss.
Tool design: Single search_wikipedia(query) returning top-k titles + snippets is the obvious read of the spec. Resist adding get_article(title) etc. unless your evals reveal it's needed — and if they do, that's a great iteration story.
Model: Use a model strong at agentic tool use (Sonnet-class or above). Haiku will save cost but introduces a confound — when behavior is bad, you won't know if it's the prompt or the model. Name the model and justify briefly.
Eval size: 15–25 hand-crafted questions. Reviewers will not be impressed by 200 auto-generated ones; they will notice if 20 carefully chosen ones probe distinct behaviors.
Judging method: Mix. Deterministic for answer correctness where possible; manual review or LLM-as-judge for behavioral dimensions. State the methodology and its limits.
4. Key risks and mitigations
Risk: Retrieval rabbit hole. Spending 2 hours making search "good." Mitigation: hard-cap retrieval work at Phase 1's 30 min. Note any retrieval-induced failures as out-of-scope-but-observed in the writeup.
Risk: Eval set that doesn't discriminate. All questions answered correctly → you learn nothing → no iteration story. Mitigation: deliberately include 4–6 questions you expect to fail (multi-hop, ambiguous entities, post-cutoff, contested facts).
Risk: Prompt sprawl. Adding instructions for every imagined edge case. Mitigation: every prompt change must be justified by a logged eval failure. If you can't point to the failure, don't add the instruction.
Risk: Writeup that lists features instead of showing reasoning. Mitigation: structure the doc around iterations and decisions, not deliverables.
Risk: Time overrun. Mitigation: the brief explicitly rewards scoping. If you hit 4 hours and Phase 3 is shaky, freeze and write up — partial honest iteration beats an unfinished comprehensive plan.
5. What to do first
Before opening any editor:

Spend 15 minutes on the Phase 0 scoping doc. Write down your hypothesis of what will be hard. Save this verbatim — you'll quote it in the writeup whether you were right or wrong, and either is interesting.
Pick the model and retrieval approach. Justify each in one sentence.
Hand-author 5 questions you're genuinely curious whether the system will get right. These become your Phase 1 probes and seed the Phase 2 eval set.
Then build the smallest loop that can run those 5 questions, and watch what happens. The plan unlocks from there.

You said: Please remove the focus on "timing" for now.

Phase 1 — Define project frame and assumptions Focus: Establish the project as a controlled prompt-evaluation experiment. Do: State that Claude is the reasoning layer. State that Wikipedia is the evidence source. State that factual claims should be supported by retrieved evidence. State that r

pasted

Please remove the focus on "timing" for now. review your plan and see if you would change anything as a result. 

i agree
a) I was thinking latest sonnet model for the system and opus for LLM as judge. b) yeah, I'm okay with the simplest retrieval solution because that's not the focus. c) I guess we can write the hypothesis a little bit later after we refine the plan.  And this has a to-do at the end. d) I don't understand what you mean by what categories of questions you want to prove. Do you mean what we evaluate on or something else?
phase -1 sounds good 
Correctness sounds good. Search invocation, I think it's trivial. It's kind of like a basic thing. How many times did you search? Did you use search or not? Is it really that important? I don't know. We can make that decision later.  The other four sound good to me. 
Can we determine which eval approaches we will use? I believe there's:

deterministic - the golden dataset, anything else?
LLM as judge
human as reviewer

Should we do all three, or should we do one or two?

Everything else you said makes sense to me. Above, I'm going to paste a plan that I came up with on my own. I want you to look at that plan and then look at your plan and then figure out what changes we want to make to the final plan. 

The plan that I'm sharing also has made some decisions about what I think is important and where I should focus. It helps with the scoping and which eval metrics I believe are true and why. Let's go from there.

Show more
Apr 25
Claude responded: On removing timing
On removing timing
Good call. Removing time estimates makes the plan judgment-driven rather than schedule-driven. I'd add a related note: the assignment's 1–2 hour target is itself a signal about scope, not just speed. So even without explicit timings, the plan should keep asking "is this the simplest version that still tells us something?" at every phase.

Answers to your questions first
2d — "categories of questions you want to probe": I meant what kinds of questions you'd run through the system to expose different behaviors — single-fact, multi-hop, ambiguous entity, post-cutoff/contested, etc. Your Phase 7 already covers this well. Same concept, just phrased differently. No daylight between us.

On search invocation as a dimension: Pushing back gently here. You're right that "did it search?" is trivial. But the interesting version isn't whether it searched — it's whether the search behavior was appropriate to the question. Did it search a basic factual question it could've answered from priors (wasted call)? Did it skip searching on something that needed grounding (overconfident)? Did it issue three searches when one would do? That's a real prompt-design dimension, and it's something I'd expect a prompt engineer at Anthropic to care about.

That said: your rubric already partly covers this under Calibration ("avoid over-answering or over-abstaining") and Evidence Support ("are claims supported by retrieved evidence"). Search behavior is upstream of both. So my recommendation: don't add it as a sixth dimension, but log it as telemetry (your Phase 3 already does this) and use it as a diagnostic when Calibration or Evidence Support fail. That keeps the rubric clean while still letting you tell stories like "the model abstained because it issued a bad query, not because the answer wasn't on Wikipedia." Decide for sure after the baseline.

On eval approaches — should you use all three?

The three you listed are the right three. Here's how I'd think about it:

Deterministic (golden dataset / reference answers): Best for Correctness on questions with unambiguous answers. Cheap, reproducible, no judge variance. But brittle for anything open-ended.
LLM-as-judge: Best for Evidence Support, Calibration, Task Effectiveness, Answer Quality — the four behavioral/qualitative dimensions. Scales well, but has known biases (length, style, self-preference) and needs calibration.
Human review: Best as a calibration check on the LLM judge, not as the primary scoring method for a small project. You're already the human; you'll be reading every trace anyway during iteration.
My recommendation: use all three, but with clear roles:

Deterministic for Correctness where the question admits a reference answer (probably half your set).
LLM-as-judge (Opus) for the four behavioral dimensions across all cases.
Human review as a calibration spot-check on ~5 cases against the judge before trusting aggregate scores. This is what your Phase 8 already proposes.
This is honest and proportionate. Doing only LLM-as-judge would invite the obvious reviewer question "how do you know the judge is right?" Doing full human review on everything is overkill for ~20 cases and would be a poor use of effort.

One thing to flag: Sonnet as system + Opus as judge is a good asymmetry (judge is stronger than system, reduces self-preference bias). State this rationale in the writeup — reviewers will notice if you don't.

Comparing your plan to mine
Your plan is, frankly, better organized than mine. It's more granular, it sequences cleanly, and it bakes in choices I left vague (telemetry shape, judge inputs, manual calibration check). Three things stand out:

Strengths of your plan vs. mine:

Phase 3 (tool contract + telemetry frozen before iteration) is something I underweighted. Locking the substrate before changing the prompt is exactly right — otherwise you can't tell whether a behavior change came from the prompt or from a quietly changed retrieval shape.
Phase 8 (judge setup + manual calibration) is more concrete than my "use a mix" handwave.
Phase 11 (optional holdout) is a real engineering instinct I skipped. Even a 3–5 question holdout protects you from prompt-overfitting the dev set.
Things from my plan worth pulling into yours:

Pre-committed hypothesis (my Phase 0). Write down what you expect to be hard before running the baseline. You'll quote yourself in the writeup whether you were right or wrong. Both are interesting; only honest reflection is persuasive. Your plan has this as a TODO — promote it to a real step.
Watch baseline behavior on a few hand-picked questions before formalizing the eval set. Your Phase 5 (baseline prompt) and Phase 7 (eval set design) currently sit on opposite sides of Phase 6 (rubric). I'd insert a "look at 3–5 traces under the baseline prompt" beat between Phase 5 and Phase 6, because what you observe there should sharpen both the rubric weighting and the eval categories. Otherwise you risk designing the rubric in the abstract.
Iteration discipline: every prompt change must be tied to a logged failure. Your Phase 10 mostly captures this ("change one main behavior at a time") but I'd make the rule explicit: no speculative additions to the prompt. If you can't point to a failed trace, don't add the instruction. This is what produces a clean writeup.
One thing I'd push back on in your plan:

Your Phase 6 lists five rubric dimensions. They're good, but Task Effectiveness and Answer Quality overlap heavily with each other and partially with Correctness. A correct, well-supported, well-calibrated answer that's also unclear is rare; a clear, useful answer that's wrong on the facts is just wrong. I'd consider whether you actually need both Task Effectiveness and Answer Quality as separate dimensions, or whether one of them is doing most of the work and the other is decoration. My instinct is to merge them or to demote Answer Quality to a tiebreaker, but I'd decide after seeing baseline outputs — it's possible the distinction matters more than I'm giving it credit for.

Proposed merged plan (changes only)
I won't rewrite the whole thing — your structure stands. Here are the specific edits:

Insert Phase 1.5: Pre-committed hypothesis. Write down what you expect to be hard and why, before any code. Save verbatim for the writeup. This replaces the TODO at the end of your Phase 1.
Insert a "baseline observation" beat between Phase 5 and Phase 6. Run the baseline prompt on 3–5 hand-picked diverse questions. Read the traces. Then finalize the rubric and design the eval set. This makes Phases 6 and 7 reactive to real behavior rather than speculative.
Phase 6: revisit the five dimensions after baseline observation. Specifically pressure-test whether Task Effectiveness and Answer Quality are doing distinct work. Don't lock in five dimensions before seeing data.
Phase 6 / telemetry: keep search-invocation behavior as logged telemetry, not a rubric dimension. Use it diagnostically when Calibration or Evidence Support fail.
Phase 8: name the asymmetry. Sonnet as system, Opus as judge — and write the one-sentence rationale (reduces self-preference bias) directly into the rubric doc, not just the final writeup.
Phase 10: add the explicit rule. Every prompt change must cite a specific failed trace. No speculative additions. Each iteration entry must include: failure observed, change made, expected effect, actual effect, tradeoff. Negative results stay in the writeup — don't hide them.
Phase 11: keep the holdout small and don't oversell. 3–5 questions is enough to detect gross overfitting; it's not a statistical claim, and the writeup should say so explicitly.
What this leaves open (decide after baseline, not now)
Whether Task Effectiveness and Answer Quality merge.
Whether search-invocation behavior gets promoted from telemetry to a rubric dimension.
Exact eval set size (your 15–25 range is right; pick within it after seeing what categories actually need coverage).
Whether to add a get_article(title) tool. Default: no. Revisit only if baseline traces show retrieval truncation is the dominant failure.
What to do first
Ratify this merged plan, then write the Phase 1.5 hypothesis doc. That hypothesis is the most useful thing you can produce before touching code, and it's the artifact that will most strengthen your final writeup — regardless of whether the predictions hold up.

You said: Let's talk about your open questions.
Let's talk about your open questions. 
First, I think task effectiveness and answer quality don't merge, and here's why. From my perspective, task effectiveness is about whether Claude and the tool did what the user was asking. Answer quality is more about the delightful angles, like:

Is that answer easily usable?
Is it readable?
Is it cognitive overload?
Is it answering the question directly? Task effectiveness is success, and answer quality is more like ease. Moving on to search invocation, I'm still not sure if it needs a rubric dimension, but I'm okay either way. We can make this decision later. Note this down as an open question that we're tracking, and we can decide later whether it's a rubric dimension or not. Eval set size: I think we can start with 25. I think I'd rather be on the safer side. I agree we shouldn't add another tool call. Overall, it sounds like we're mostly aligned, and let's merge the plans.
Show more
Apr 25
Claude responded: On your distinction between Task Effectiveness and Answer Quality
On your distinction between Task Effectiveness and Answer Quality
Your framing — success vs. ease — is sharper than my pushback. I'll own that I was too quick to suggest merging. The distinction you're drawing is real: an answer can fully resolve the user's request (effective) while still being a wall of text that buries the answer (low quality), and vice versa. Keeping them separate also gives you something genuinely useful in the writeup — the ability to say "the prompt fixed effectiveness but degraded quality" or vice versa, which is a more interesting story than a single blended score.

One small refinement worth holding in mind: when you write the judge rubric, give the judge concrete anchors for each so they don't collapse into the same vibe-score. Something like Task Effectiveness = "did the answer resolve what was asked, including handling ambiguity, scope, and implicit follow-ups," Answer Quality = "is it readable, appropriately concise, well-structured, easy to extract the answer from." You don't need to lock the wording now, but flag this for Phase 8 — judge dimension definitions need to be operationally distinguishable, not just conceptually distinct.

On open questions to track
Two now on the list:

Search invocation as a rubric dimension vs. telemetry-only. Decide after baseline traces.
Whether Task Effectiveness and Answer Quality judge prompts produce meaningfully different scores in practice. If after baseline + first iteration the two dimensions move in lockstep across all cases, that's a signal the judge isn't actually distinguishing them and they should either be merged or have their definitions tightened. Worth checking explicitly during the baseline analysis.
On eval set size
25 is a reasonable choice. Two notes:

Distribute across your six categories deliberately — not 4-4-4-4-4-5, but weighted toward the categories you expect to be most diagnostic. Ambiguity and insufficient-evidence cases tend to produce richer failure data than simple factual cases, so they're worth slightly overweighting.
25 is enough to see patterns but not enough for statistical claims. State this in the writeup. The persuasive framing is "this dataset is designed to expose behaviors, not to estimate accuracy" — which matches your Phase 7 rationale already.
Merged final plan
Phase 1 — Frame and assumptions. Claude is the reasoning layer. Wikipedia is the evidence source. Factual claims should be supported by retrieved evidence. Retrieval is intentionally simple and fixed. Why: Prevents the project from being judged as a production retrieval system.

Phase 1.5 — Pre-committed hypothesis. Before any code, write down what you expect to be hard and why. Predictions about likely failure modes (over-searching, query phrasing, multi-hop, ambiguous entities, post-cutoff facts, instruction pressure). Save verbatim — you'll quote it in the writeup whether right or wrong. Why: Honest predictions, especially wrong ones, are credibility-building.

Phase 2 — Scope and non-goals. Build: Claude + system prompt, search_wikipedia, simple CLI, logging, eval runner. Do not build: vector DB, complex ranking, UI, multi-agent, production retrieval. Why: Complexity weakens attribution.

Phase 3 — Tool contract and telemetry. Freeze the substrate before iterating on the prompt. Define exact tool input/output shape, max tool calls per question, logging fields (search used, # searches, queries, retrieved evidence, final answer, abstention, optional token/latency). Why: Locking the substrate means behavior changes can be cleanly attributed to prompt changes.

Phase 4 — Minimal runnable prototype. Get the full loop working end-to-end. Why: A simple working system is enough to start measuring behavior.

Phase 5 — Baseline prompt. Simple but functional. Avoid packing in all desired behavior. Why: A weak baseline makes improvement measurable.

Phase 5.5 — Baseline observation. Run the baseline on 3–5 hand-picked diverse questions before formalizing the rubric and dataset. Read the traces carefully. Why: Phases 6 and 7 should be reactive to observed behavior, not designed in the abstract.

Phase 6 — Evaluation rubric. Five dimensions: Correctness, Evidence Support, Calibration, Task Effectiveness, Answer Quality. Open question carried forward: whether to add Search Invocation as a sixth dimension or keep it as telemetry-only — decide after baseline analysis. Open question carried forward: whether Task Effectiveness and Answer Quality produce distinguishable judge scores in practice. Why: Maps cleanly to trustworthy / useful / delightful without metric bloat.

Phase 7 — Eval set design. ~25 hand-authored cases across six categories: simple factual, ambiguous, multi-hop, insufficient evidence, adversarial / instruction-pressure, broad/noisy retrieval. Weight toward diagnostic categories (ambiguity, insufficient evidence) over simple factual. Each case includes: question, category, expected behavior, likely failure modes, optional reference facts. Why: Dataset should expose behavior, not test trivia.

Phase 8 — Judge setup. Sonnet as system, Opus as judge — asymmetry reduces self-preference bias, state this in the writeup. Judge sees: question, final answer, retrieved evidence, category/expected behavior. Judge outputs: scores on five dimensions, failure types, short rationale. Manual calibration spot-check on ~5 cases before trusting aggregates. Eval methodology mix: deterministic (Correctness on questions with reference answers), LLM-as-judge (the four behavioral dimensions), human review (calibration spot-check). Why: Proportionate, honest, and pre-empts the "how do you know the judge is right?" question.

Phase 9 — Run baseline and analyze failures. Look for: unsupported-but-correct answers, skipped searches, wrong/broad queries, over-answering, over-abstaining, weak ambiguity handling, poor synthesis, unclear answers. Why: Iterations should be driven by observed failures, not theoretical ideals.

Phase 10 — Iterate prompts. One main behavior change at a time. Hard rule: every prompt change must cite a specific failed trace; no speculative additions. Each iteration entry captures: observed failure, prompt change, expected effect, actual effect, tradeoff. Keep negative results in the writeup. Why: This produces the clean prompt → behavior → result story that distinguishes the submission.

Phase 11 — Final eval and small holdout. Run final prompt on full eval set. Reserve a small holdout (3–5 questions) to detect gross overfitting. Compare against baseline and intermediate prompts. State the holdout's limits explicitly — not a statistical claim. Why: Even a small holdout signals the right engineering instinct, as long as you don't oversell.

Phase 12 — Synthesize and write rationale. Structure around iterations and decisions, not the deliverable checklist. Include framing, assumptions, architecture, prompt philosophy, eval dimensions, dataset design, iterations with deltas, category slices, failure analysis, tradeoffs, limitations, future work. Reference the Phase 1.5 hypothesis and assess honestly. Why: The writeup is where judgment shows.

Open questions tracked forward
Whether search invocation becomes a sixth rubric dimension or stays as telemetry. Decide after Phase 9.
Whether Task Effectiveness and Answer Quality produce meaningfully different judge scores. Check during Phase 9 baseline analysis.
Whether retrieval shape (snippet truncation, top-k, etc.) emerges as a dominant failure mode that justifies a get_article tool. Default: no. Revisit only if baseline traces force the question.
What to do first
Phase 1.5 — write the hypothesis doc. That's the single most leverage-positive artifact you can produce before any code, and it's the one your current draft plan was missing.

You said: I can outline the hypothesis that I'm thinking, and you can help me formalize it.
I can outline the hypothesis that I'm thinking, and you can help me formalize it.

The first one would be ensuring that Claude actually uses the tool and backs the tool with data from the API that I create, essentially relying on the tool and not relying on its own knowledge.
The second hypothesis is that it's going to have challenges with questions where there's a question within a question, a multi-multi question, and ambiguity about the topic. For example, if it's talking about "orange", is it talking about the fruit or the color? That ambiguity, and another thing that is generally a problem with today's chatbots, is the inclination to be helpful and, in that, surface the wrong information.
Being honest and reliable, even if Claude doesn't know how to answer the question or doesn't have sufficient evidence, would be the third one. These are probably the three major hypotheses I'm going to go with. At some point, I'm going to define the eval metrics that I want to focus on, but I'll start with these hypotheses. What do you think about these? Is there anything I should add or remove based on what you know? Help me iterate on this.
Show more
Apr 25
Claude responded: Your three hypotheses are well-chosen.
Your three hypotheses are well-chosen. They map cleanly onto the rubric you already have (H1 → Evidence Support; H2 → Task Effectiveness + Correctness; H3 → Calibration), and together they cover the most interesting prompt-engineering levers in this assignment. I wouldn't add a fourth.

Before formalizing, let me push on each one a little.

H1 — Tool reliance vs. latent knowledge
Your framing is right. One sharpening: there are actually two failure modes hiding inside this, and they're worth distinguishing because they require different prompt fixes.

Skipping the tool entirely — Claude answers from priors without searching.
Searching but not using the result — Claude searches, gets evidence, then answers from priors anyway (or blends prior knowledge into the answer in ways that aren't traceable to the retrieved text).
The second is harder to detect and more interesting. It's also the one that maps most directly to the assignment's framing of Wikipedia as the evidence source. I'd write H1 to cover both, because a prompt that fixes only the first will leave the second untouched and your eval will show it.

H2 — Multi-hop and ambiguity
Two things to disentangle here. You've actually named three distinct phenomena and bundled them into one hypothesis:

Multi-hop / compositional questions — "Who was the prime minister of the country that hosted the 2008 Olympics?"
Entity ambiguity — "orange" the fruit vs. the color; "Mercury" the planet vs. the element vs. the band.
Helpfulness bias surfacing wrong information — the inclination to produce an answer rather than the right answer when the question is hard.
These are related but require different prompt interventions. Multi-hop needs decomposition. Ambiguity needs entity disambiguation (often a clarifying question or a search to identify which entity is meant). Helpfulness bias is closer to a calibration failure and overlaps with H3.

I'd recommend tightening H2 to focus on multi-hop and ambiguity specifically — both are about the model failing to resolve the question structure before answering. The "helpfulness bias surfacing wrong information" piece I'd actually fold into H3, because it's fundamentally about answering when you shouldn't.

This is a real edit, not cosmetic. It makes each hypothesis test a distinct prompt lever, which makes your iterations cleaner.

H3 — Honesty under insufficient evidence
Solid as stated. With the helpfulness-bias piece moved here, H3 becomes: when the system shouldn't answer confidently — because evidence is missing, ambiguous, or contradictory — does it appropriately abstain, qualify, or narrow the claim, or does it produce an answer anyway?

One thing to flag explicitly: the failure mode here isn't just "refusing when it should answer." It's the more common one — answering when it should abstain. State which direction you expect to dominate. My prediction: over-answering will be far more common than over-abstaining in the baseline, and the iteration will need to be careful not to flip the system into excessive hedging.

What I'd remove
Nothing. Three hypotheses is the right number. Adding a fourth (e.g., on adversarial robustness, retrieval quality, or answer formatting) would dilute focus and probably duplicate what these three already cover.

What I'd add — but as a meta-note, not a hypothesis
A short paragraph after the three hypotheses noting what you are deliberately not testing: production retrieval quality, adversarial jailbreak robustness as a primary focus, multilingual handling, etc. This signals scope discipline and pre-empts the "why didn't you test X?" reviewer question.

Formalized version
Here's a tightened version you can drop into the writeup. I've kept your voice but sharpened the failure modes and made each hypothesis specific enough to test:

H1 — Evidence-backed answering. The baseline system will often answer from Claude's latent knowledge rather than grounding its claims in retrieved Wikipedia evidence. This will manifest in two ways: (a) skipping the search tool entirely on questions Claude believes it already knows, and (b) searching but then producing answers that include claims not supported by the retrieved text. The second mode is harder to detect than the first and is the more interesting target for prompt iteration.

H2 — Complex question handling. Ambiguous and multi-hop questions will fail more often than simple factual ones. Two specific failure patterns are expected: (a) entity ambiguity — when the question's subject is underspecified (e.g., "Mercury," "orange"), the system will resolve to whichever sense it sees first rather than recognizing the ambiguity and clarifying or disambiguating via search; (b) multi-hop decomposition — when the question requires chaining multiple facts, the system will answer from a single search result or skip intermediate steps, producing answers that are partial, wrong-entity, or confidently incorrect.

H3 — Honesty under insufficient evidence. When retrieved evidence is missing, partial, or contradictory, the system's default will be to produce an answer anyway rather than to acknowledge insufficient evidence, narrow the claim, or qualify uncertainty. This is partly a calibration failure and partly an artifact of helpfulness bias — the system is inclined to surface an answer rather than admit it can't responsibly produce one. The dominant baseline failure direction is expected to be over-answering, not over-abstaining; iteration on this hypothesis will need to avoid flipping the system into excessive hedging.

Out of scope. This evaluation is not designed to test production retrieval quality, adversarial robustness as a primary focus, or multilingual handling. A small number of instruction-pressure cases are included as a probe under H1, but adversarial prompt-breaking is not a central theme.

One thing to commit to before moving on
Write a one-sentence prediction for each hypothesis about which direction the failure will go in the baseline. Something like "I expect H1 failures to be roughly 60% skip-search and 40% search-but-ignore," or "I expect H3 failures to be over 90% over-answering rather than over-abstaining." You don't need to be right. You need to have made the prediction in writing before you see the data, because that's what makes the writeup honest rather than retrofitted.

You said: I think I'm good with the version that you proposed, so let's lock it in.
I think I'm good with the version that you proposed, so let's lock it in. I honestly don't want to come up with percentages and stuff, because it's going to become way too... We're defining way too much. What you're proposing is going to add to the definitions more than it should. I want to keep it a little bit open-ended. I think starting with the hypothesis is enough.

Apr 25
Claude responded: Locked in.
Locked in. Your three hypotheses, as formalized above, are the pre-committed version going into the writeup.

You're right to push back on the percentages. I was overreaching — that level of pre-registration is a research-paper move, and this is a prompt engineering take-home. The hypotheses themselves, written down before baseline, are the honest commitment. That's enough.

Status check on the plan
Locked:

Phase 1 framing and assumptions
Phase 1.5 hypotheses (the three we just formalized)
Phase 2 scope and non-goals
Phase 3 tool contract and telemetry shape
Phase 6 rubric (five dimensions: Correctness, Evidence Support, Calibration, Task Effectiveness, Answer Quality)
Phase 7 eval set size (~25, weighted toward diagnostic categories)
Phase 8 judge setup (Sonnet system, Opus judge, manual spot-check, mixed eval methodology)
Phase 10 iteration discipline (every change cites a failed trace)
Phase 11 holdout approach (small, not oversold)
Open questions tracked forward:

Search invocation as a sixth rubric dimension vs. telemetry-only — decide after Phase 9.
Whether Task Effectiveness and Answer Quality produce distinguishable judge scores — check during Phase 9.
Whether retrieval shape forces a get_article tool — default no, revisit only if baseline forces it.
What's next
Phase 2 and Phase 3 are the next decisions. Phase 2 is mostly settled (you've already agreed to the minimal build), but Phase 3 — the tool contract and telemetry shape — has real choices in it that are worth thinking through before you write any code:

What exactly does search_wikipedia return? Just titles? Titles + snippets? Full first paragraph? Top-k how big?
What's the max number of tool calls per question? Hard cap or soft guidance?
What gets logged per turn vs. per question?
These are the substrate decisions that, once frozen, you don't change during prompt iteration. Want to work through Phase 3 next, or is there something earlier you want to revisit first?

You said: I'm gonna start a new chat to start focusing on the search function.
I'm gonna start a new chat to start focusing on the search function. Can you write a prompt for what the next task is, which is essentially scoping and then identifying the steps to write it and then some quote samples that I can get started with? 

Also, can you extract the hypothesis so that I can add it to the project? You can extract it as a txt file or a markdown file, whichever you prefer.

Apr 25
Claude responded: Handoff prompt for the next chat
Handoff prompt for the next chat
Here's a prompt you can paste into the new chat to pick up cleanly. I've written it to give the next Claude enough context to be useful without re-litigating decisions you've already locked in.

Context: I'm working on an Anthropic prompt-engineering take-home assignment. The system uses Claude as the reasoning layer and Wikipedia as the evidence source, accessed through a single tool: search_wikipedia(query: str). The project is a controlled experimentation loop for prompt behavior — not a production retrieval system. Retrieval is intentionally simple and held constant across prompt experiments so that behavior changes can be cleanly attributed to prompt changes.

What's already locked in:

Model: Claude Sonnet (latest) for the system, Claude Opus for the LLM judge.
Scope: minimal build — system prompt + one tool + simple CLI + logging + eval runner. No vector DB, no ranking, no UI, no multi-agent.
Five eval dimensions: Correctness, Evidence Support, Calibration, Task Effectiveness, Answer Quality.
Three pre-committed hypotheses: (H1) evidence-backed answering, (H2) complex question handling — ambiguity and multi-hop, (H3) honesty under insufficient evidence.
Eval set target: ~25 hand-authored cases across six categories.
What I need help with now: Phase 3 of my plan — defining the tool contract and retrieval substrate before I touch the prompt. This is the substrate I'm freezing before any prompt iteration, so I want to make these decisions deliberately.

Specifically, help me:

Scope the work. What are all the decisions I need to make before writing any code for the retrieval layer? Examples I know I need to decide: what search_wikipedia returns (titles only? titles + snippets? full first paragraph?), top-k size, whether snippets are truncated, whether to expose redirects/disambiguation results, max tool calls per question, error handling for zero-result queries, rate limiting.
Identify the implementation steps. Given I'm using the live MediaWiki API (no dump, no local index), walk me through the build order: API endpoint choice, request shape, response parsing, what to surface to the model vs. log internally, how to handle MediaWiki's quirks (disambiguation pages, redirects, missing articles).
Show me a few sample tool-return shapes I can choose between. I want to see 2–3 concrete options for what the tool returns to Claude — minimal, medium, and richer — with the tradeoffs of each. The choice matters because it shapes what behaviors the prompt has to handle (e.g., if I return only titles, Claude has to issue follow-up searches for content; if I return full paragraphs, Claude has more to ground on but may get overwhelmed or cherry-pick).
Constraints to respect:

Don't optimize retrieval as the primary objective. Simple is the goal.
Don't suggest adding a second tool (get_article, etc.) — that's deferred unless baseline traces force it.
Push back if I drift toward production retrieval engineering.
Tie recommendations back to evaluability: which choice makes prompt behavior easier to attribute and measure?
Start by reasoning through the scoping questions before proposing implementation steps.

Hypothesis file
I'll create the markdown file now.


Created a file, read a file
Created a file, read a file
Both ready — the handoff prompt above to paste into the new chat, and the hypotheses file to add to the project.

One small note on the handoff: I deliberately framed Phase 3 as a substrate-freezing exercise rather than a "build retrieval" exercise. The new chat may try to drift toward retrieval optimization since that's where most engineers' instincts go. The framing in the prompt should hold the line, but if the next Claude starts proposing reranking or hybrid search, push back the same way you've pushed back here.


Pre committed hypotheses
Document · MD 






Claude is AI and can make mistakes. Please double-check responses.





