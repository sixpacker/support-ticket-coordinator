from support_ticket_coordinator import (
    AgentDefinition,
    Finding,
    SupportTicketCoordinator,
    SubagentFailure,
    policy_analyst_response,
    refund_tool,
)


def test_scoped_agent_definitions_only_allow_necessary_tools():
    order_agent = AgentDefinition(
        name="order_investigator",
        tools=["lookup_order", "check_billing_history"],
        prompt="Investigate order and billing issues.",
    )
    policy_agent = AgentDefinition(
        name="policy_analyst",
        tools=["read_policy"],
        prompt="Answer return-window questions using policy docs.",
    )

    assert order_agent.tools == ["lookup_order", "check_billing_history"]
    assert policy_agent.tools == ["read_policy"]
    assert "refund_order" not in policy_agent.tools


def test_policy_analyst_requires_explicit_context():
    hedged = policy_analyst_response("I need to check the order date before I can answer.")
    decisive = policy_analyst_response(
        "The order was purchased on 2024-02-18 and the policy says 30 days. The customer is within the 30-day window."
    )

    assert "need to check" in hedged.lower()
    assert "30-day" in decisive.lower() or "30 day" in decisive.lower()


def test_findings_keep_claim_evidence_and_source():
    finding = Finding(
        concern_id="duplicate_charge",
        claim="The duplicate charge is likely a billing duplication.",
        evidence="The customer saw two charges for the same invoice on the same day.",
        source="billing ledger",
    )

    assert finding.concern_id == "duplicate_charge"
    assert finding.claim
    assert finding.evidence
    assert finding.source


def test_refund_hook_rejects_over_ceiling_and_keeps_log_empty():
    refund_log = []
    result = refund_tool(amount=750, refund_log=refund_log)

    assert result["approved"] is False
    assert result["reason"] == "Refund exceeds the $500 ceiling"
    assert refund_log == []


def test_failure_is_structured_and_coordinator_continues_other_concerns():
    coordinator = SupportTicketCoordinator()
    failure = SubagentFailure(
        error_category="billing_api_timeout",
        is_retryable=True,
        attempted="duplicate charge investigation",
        partial_results=["billing log retrieved"],
        alternatives=["escalate to finance", "ask customer for bank statement"],
    )

    remaining = coordinator.handle_failure(failure)

    assert failure.error_category == "billing_api_timeout"
    assert failure.is_retryable is True
    assert remaining == ["order_refund", "return_policy", "chargeback_threat"]


def test_coverage_check_detects_and_redelegates_gap():
    coordinator = SupportTicketCoordinator()
    initial_assignments = {"order_refund": "order_investigator", "duplicate_charge": "order_investigator"}
    fixed_assignments = coordinator.coverage_check(initial_assignments)

    assert "return_policy" in fixed_assignments
    assert "chargeback_threat" in fixed_assignments


def test_dispatch_rejects_over_ceiling_refund_before_tool_runs():
    coordinator = SupportTicketCoordinator()
    result = coordinator.dispatch_concern("order_refund", {"amount": 750, "order_id": "A-42"})

    assert result["approved"] is False
    assert result["reason"] == "Refund exceeds the $500 ceiling"


def test_policy_violation_rejects_refund_after_30_days_for_600_item():
    coordinator = SupportTicketCoordinator()
    policy_response = policy_analyst_response(
        "The order was purchased on 2024-01-01 and the customer is requesting a refund for a $600 item on 2024-02-15. The policy allows 30 days only."
    )
    refund_result = coordinator.dispatch_concern(
        "order_refund",
        {"amount": 600, "order_id": "A-99", "refund_log": []},
    )

    assert "30 days" in policy_response.lower() or "30-day" in policy_response.lower()
    assert refund_result["approved"] is False
    assert refund_result["reason"] == "Refund exceeds the $500 ceiling"


def test_extract_concerns_from_customer_ticket_text():
    coordinator = SupportTicketCoordinator()
    ticket = (
        "I need a refund for a $600 item after 30 days. "
        "I am also threatening a chargeback because I want my money back."
    )

    concerns = coordinator.extract_concerns(ticket)

    assert "order_refund" in concerns
    assert "return_policy" in concerns
    assert "chargeback_threat" in concerns


def test_process_ticket_tracks_concerns_and_coverage():
    coordinator = SupportTicketCoordinator()
    ticket = "I need a refund for a $600 item and I am threatening a chargeback."

    result = coordinator.process_ticket(ticket)

    assert result["concerns"]
    assert "order_refund" in result["concerns"]
    assert "chargeback_threat" in result["concerns"]
    assert result["coverage_ok"] is True
