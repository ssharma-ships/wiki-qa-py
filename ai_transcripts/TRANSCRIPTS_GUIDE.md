# AI Transcripts Guide

## Purpose

This folder contains selected AI collaboration transcripts from the take-home assignment, included as process evidence. They show how the project was planned, scoped, iterated on, and documented with AI assistance — not as a deliverable in themselves, but as a record of the collaboration process.

---

## Contents

```
ai_transcripts/
  raw/
    planning/
      chatgpt_planning.md      ← ChatGPT planning conversation (initial scoping)
      claude_planning.md       ← Claude planning conversation (phased plan, hypotheses)
    claudecode/
      raw_jsonl/               ← Original Claude Code session transcripts (JSONL format)
      raw_md/                  ← Markdown conversions of those sessions (for readability)
  summaries/
    claudecode_session_index.md     ← Index of all 29 Claude Code sessions with dates and descriptions
    decision_log.md                 ← Summary of major decision topics discussed across sessions
    iteration_history.md            ← Summary of what each iteration session covered
    reviewer_facing_process_summary.md  ← Narrative overview of how AI collaboration was structured
```

---

## Conversion Process

Claude Code sessions are natively stored as JSONL files, one per session. A conversion script was used to convert each JSONL file into a readable Markdown transcript, preserving the turn-by-turn structure of user messages, assistant responses, and tool calls. Original JSONL files were kept alongside the Markdown versions. The Markdown files are the intended format for human review.

---

## Reviewer Guidance

Start with the files in `summaries/` — they provide a structured overview of what happened across the AI sessions without requiring end-to-end reading of raw transcripts. The `claudecode_session_index.md` is the best entry point for navigating specific Claude Code sessions. Raw transcripts are included as supporting evidence for anyone who wants to trace a specific decision or exchange back to its source.

---

## Redaction and Safety Note

Transcripts were reviewed for obvious sensitive values. Raw files should not contain API keys, tokens, or `.env` contents. During the Markdown conversion, long tool result outputs (such as file listings or truncated command output) were shortened for readability — this is indicated inline where it occurs. If any sensitive value is identified later, it should be redacted from the raw file directly.

The substantive project artifacts — judgment calls, trade-off analysis, prompt design rationale, evaluation results, and issue documentation — are captured in `RATIONALE.md`, `prompts.py`, the iteration log, the issue tracker, and the `observations/` directory. The transcripts here are process evidence, not the primary record of decisions.
