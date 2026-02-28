def test_findings_include_evidence_and_remediation(client):
    create = client.post(
        "/api/v1/runs",
        json={"query": "strict fail constraints", "provider_scope": "aws"},
    )
    run_id = create.json()["run_id"]

    response = client.get(f"/api/v1/runs/{run_id}/providers/aws/findings")
    assert response.status_code == 200
    items = response.json()["items"]
    assert len(items) > 0
    assert any(item["evidence"] for item in items)
    assert any(item.get("remediation") for item in items if item["outcome"] == "fail")
