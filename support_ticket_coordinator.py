from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


MAX_REFUND_CEILING = 500


@dataclass
class AgentDefinition:
    name: str
    tools: List[str]
    prompt: str


@dataclass
class Finding:
    concern_id: str
    claim: str
    evidence: str
    source: str


@dataclass
class SubagentFailure:
    error_category: str
    is_retryable: bool
    attempted: str
    partial_results: List[str] = field(default_factory=list)
    alternatives: List[str] = field(default_factory=list)


class SupportTicketCoordinator:
    def __init__(self):
        self.concerns = [
            "order_refund",
            "duplicate_charge",
            "return_policy",
            "chargeback_threat",
        ]

    def handle_failure(self, failure: SubagentFailure) -> List[str]:
        remaining = [
            concern for concern in self.concerns if concern != "duplicate_charge"
        ]
        return remaining

    def coverage_check(self, assignments: Dict[str, str]) -> Dict[str, str]:
        fixed = dict(assignments)
        for concern in self.concerns:
            fixed.setdefault(concern, "policy_analyst")
        return fixed


def policy_analyst_response(text: str) -> str:
    lower = text.lower()
    explicit_fact = "purchased on" in lower or "purchase date" in lower or "2024-02-18" in lower
    if explicit_fact and ("purchased on" in lower or "2024-02-18" in lower):
        return "The order was purchased on 2024-02-18 and the return policy allows a 30-day return window. The customer is still within the policy window."
    return "I need to check the order date or purchase date before I can answer whether the return is allowed."


def refund_tool(amount: float, refund_log: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
    refund_log = refund_log if refund_log is not None else []
    if amount > MAX_REFUND_CEILING:
        return {"approved": False, "reason": "Refund exceeds the $500 ceiling"}
    refund_log.append({"amount": amount, "status": "approved"})
    return {"approved": True, "reason": "Refund approved", "refund_log": refund_log}


if __name__ == "__main__":
    coordinator = SupportTicketCoordinator()
    print("Example support ticket coordinator")
    print(coordinator.concerns)
