from __future__ import annotations


def evaluate_acceptance(findings: list[dict], iteration_count: int, max_iterations: int = 3) -> dict:
    evidence_unavailable = any(
        evidence.get("availability_status") == "unavailable"
        for finding in findings
        for evidence in finding.get("evidence", [])
    )
    failed_findings = [finding for finding in findings if finding.get("outcome") == "fail"]
    unresolved = len(failed_findings)

    if evidence_unavailable:
        return {
            "accepted": False,
            "status": "stopped",
            "terminal_reason": "evidence_unavailable",
            "unresolved_findings": unresolved,
        }

    if unresolved == 0:
        return {
            "accepted": True,
            "status": "accepted",
            "terminal_reason": "accepted",
            "unresolved_findings": 0,
        }

    if iteration_count >= max_iterations:
        return {
            "accepted": False,
            "status": "stopped",
            "terminal_reason": "iteration_limit",
            "unresolved_findings": unresolved,
        }

    return {
        "accepted": False,
        "status": "optimizing",
        "terminal_reason": None,
        "unresolved_findings": unresolved,
    }
