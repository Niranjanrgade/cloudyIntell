def test_provider_separation_and_iteration_limit(client):
    response = client.post(
        "/api/v1/runs",
        json={"query": "strict fail constraints", "provider_scope": "both"},
    )
    assert response.status_code == 202
    run_id = response.json()["run_id"]

    detail = client.get(f"/api/v1/runs/{run_id}")
    assert detail.status_code == 200
    payload = detail.json()
    assert {run["provider"] for run in payload["provider_runs"]} == {"aws", "azure"}
    assert all(run["iteration_count"] <= 3 for run in payload["provider_runs"])
