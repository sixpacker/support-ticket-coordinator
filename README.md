# Multi-Agent Support Ticket Coordinator

This project demonstrates the core ideas from the Week 2 assignment: scoped subagents, explicit context passing, structured findings, pre-tool validation, failure propagation, and coverage checking.

## What is included

- A coordinator model that tracks the four support-ticket concerns.
- Agent definitions with explicit tool scoping.
- A policy-analyst example showing the hedged-answer problem and the corrected explicit-context answer.
- A refund hook simulation that blocks over-ceiling refunds.
- Structured subagent failures with partial results and alternatives.
- A simple coverage check that ensures all concerns are assigned.

## Running the checks

```bash
pytest -q
```

## Key lessons

1. Tool scoping prevents a specialist agent from using unrelated tools.
2. Subagents do not inherit context; facts must be explicitly passed in prompts.
3. Findings must preserve attribution via claim, evidence, and source.
4. A single validation hook is safer than repeating business rules in every agent prompt.
5. Structured errors should allow the coordinator to continue on unaffected work while clearly naming gaps.

## Reflection

The assignment is a clear reminder that multi-agent reliability is not just about making more agents; it is about defining precise boundaries, carrying explicit facts, and ensuring the coordinator can validate coverage and failure states.
