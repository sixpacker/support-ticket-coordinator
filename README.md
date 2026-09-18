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

### 1. Coverage gaps and where to look first

I would look first at the coordinator and the decomposition logic, not at the subagents. The subagents are not the source of the bug if they were each given a narrow task and a valid tool set. The real problem is usually that the coordinator failed to enumerate the ticket’s concerns correctly or failed to check whether every concern was assigned. This is why the coverage check matters. It catches the gap before anyone mistakes partial success for complete resolution.

### 2. Tokens and the value of the ticket

This design likely uses more tokens than a single-agent approach because the coordinator adds orchestration overhead, explicit context passing, and structured result handling. In a large single-agent workflow, one prompt may be shorter on paper, but it often includes a far larger shared context window, more competing instructions, more tool choice ambiguity, and more repeated history. For a four concern ticket, the multi-agent approach is worth it because it reduces reasoning drift, isolates tasks, and keeps each agent’s context precise. I would say the extra token cost is justified for tickets with multiple independent concerns, policy edges, or escalation risk. A ticket that is a single simple request, like a straightforward refund with no policy ambiguity and no escalation path, would not be worth the added coordination overhead.

### 3. Facts that had to be passed explicitly

I had to give each subagent the facts it was allowed to use, the exact concern it was responsible for, the tools it could access, and the constraints it had to respect. In other words, I had to add the explicit context that I had initially assumed was already available through the coordinator or inherited state. The policy analyst needed the order date and policy version, the refund processor needed the refund amount and ceiling rule, and the escalation writer needed the customer risk context and the unresolved issue. The key lesson was that subagents do not inherit context. They only get what is explicitly passed in. That is why context isolation and prompt design are such a major part of this assignment.

The assignment is a clear reminder that multi-agent reliability is not just about making more agents; it is about defining precise boundaries, carrying explicit facts, and ensuring the coordinator can validate coverage and failure states.
