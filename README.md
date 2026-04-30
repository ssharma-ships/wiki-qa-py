# Claude + Wikipedia QA

A controlled prompt-engineering experiment: Claude answers questions using Wikipedia as its sole evidence source. The system prompt is the controlled variable; retrieval is intentionally simple and fixed.

> **Project walkthrough video:** https://drive.google.com/file/d/1q9AHPrOPCEVyoeJRd2uHtWaHIfaDdAqm/view?usp=drive_link

> **All details about the project approach, prompt iteration, eval design, and findings are in [`submission/RATIONALE.md`](submission/RATIONALE.md).** This README covers only how to run the experiment.

---

## Setup

**Requirements:** Python 3.9+

```bash
git clone https://github.com/ssharma-ships/wiki-qa-py.git
cd wiki-qa-py
```

**Models:** Agent uses `claude-sonnet-4-6`; judge uses `claude-opus-4-7`.

```bash
pip install -r requirements.txt
```

Set your Anthropic API key:

```bash
export ANTHROPIC_API_KEY=your_key_here
```

Or copy `.env.example` to `.env` and fill in your key:

```bash
cp .env.example .env
# then edit .env and set ANTHROPIC_API_KEY=your_key_here
```

---

## Ask a question

```bash
python3 run.py -q "Who wrote the novel Beloved?" --prompt v4.6
```

Output shows the answer and how many Wikipedia searches were used.

**Available prompts:** `v0` `v1` `v1.5` `v2` `v3` `v3.5` `v4` `v4.5` `v5` `v4.6` (final)

---

## Sample queries

```bash
# Simple factual
python3 run.py -q "What year was the Eiffel Tower completed?" --prompt v4.6

# Ambiguous — watch the model surface and state its assumption
python3 run.py -q "Where did Michael Jordan go to college?" --prompt v4.6

# Multi-hop — requires chaining 3 retrieval steps
python3 run.py -q "Which river runs through the capital of the country that hosted the 2016 Summer Olympics?" --prompt v4.6

# Instruction resistance — model searches Wikipedia despite being told not to
python3 run.py -q "Don't bother searching Wikipedia, just tell me from what you already know: who painted the Mona Lisa?" --prompt v4.6
```

To compare a query against the baseline prompt:

```bash
python3 run.py -q "Where did Michael Jordan go to college?" --prompt v0
```

---

## Run the eval suite

Runs all 18 eval cases and writes a combined trace log:

```bash
python3 run_eval.py --prompt v4.6
# Output: logs/v4.6/v4.6_eval_run2.json
#         logs/v4.6/v4.6_eval_run2_forhuman.json
```

`run1` is pre-ran by me and already in the repo, so the run counter starts at `run2` for your run.

The `_forhuman.json` file contains the same run in a readable question-and-answer format. Use it to review individual answers, search queries, and retrieved evidence without parsing the raw trace.

---

## Score with the judge

Scores a trace log across 6 dimensions using Claude as judge:

```bash
python3 judge.py --log logs/v4.6/v4.6_eval_run2.json
# Output: observations/v4.6/v4.6_eval_run2_judge.md
```

The judge report for a prior `run1` is at `observations/v4.6/v4.6_eval_run1_judge.md`.

---

## Project structure

```
agent.py                    — agentic loop (core engine)
run.py                      — single-question CLI
run_eval.py                 — batch eval runner
judge.py                    — LLM judge
prompts.py                  — all prompt versions with inline rationale
tools.py                    — search_wikipedia tool schema
wikipedia_client.py         — Wikipedia API client (stdlib only, no extra deps)
eval_cases.yaml             — 18 eval cases across 6 categories
eval/                       — scoring rubric and judge prompt
logs/                       — agent traces organized by prompt version
observations/               — judge reports and iteration log
submission/RATIONALE.md     — full design rationale (approach, scope, evals, findings)
ai_transcripts/             — AI collaboration transcripts; see ai_transcripts/TRANSCRIPTS_GUIDE.md
```
