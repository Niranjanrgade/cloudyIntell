def test_evidence_unavailable_stops_acceptance(client):
    response = client.post(
        "/api/v1/runs",
        json={"query": "no-evidence scenario", "provider_scope": "azure"},
    )
    assert response.status_code == 202
    run_id = response.json()["run_id"]

    detail = client.get(f"/api/v1/runs/{run_id}")
    provider_run = detail.json()["provider_runs"][0]
    assert provider_run["provider"] == "azure"
    assert provider_run["accepted"] is False
    assert provider_run["terminal_reason"] == "evidence_unavailable"
