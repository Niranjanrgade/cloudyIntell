def test_partial_results_and_failure_reason_surface(client):
    response = client.post(
        "/api/v1/runs",
        json={"query": "timeout in network domain", "provider_scope": "aws"},
    )
    run_id = response.json()["run_id"]

    detail = client.get(f"/api/v1/runs/{run_id}")
    provider_run = detail.json()["provider_runs"][0]
    assert provider_run["status"] == "failed"
    assert provider_run["failure_reason"]
    assert provider_run["latest_output"]
