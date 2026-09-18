# Reflection

This assignment demonstrates that a multi-agent workflow is only reliable when the coordinator enforces boundaries and validation rather than relying on the model to behave perfectly. The most important design choice was to define four concern areas—order refund, duplicate charge, return policy, and chargeback threat—and assign each one to a specialist role with only the tools it actually needs.

The system also needed clear context passing. A policy answer is not reliable if the model is allowed to reason from hidden assumptions; the order date, policy version, and customer facts must be explicit. The same principle applies to the refund rule: a business ceiling like the $500 cap must be enforced centrally so no agent can override it by prompt wording alone.

The coordinator is therefore responsible for coverage, recovery, and evidence. It must detect missing concerns, keep structured findings with claim/evidence/source, and handle failures with partial results and alternatives so the rest of the ticket can continue. This makes the workflow more resilient and easier to audit than a single general-purpose assistant that tries to answer everything at once.
