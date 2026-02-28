def test_create_and_get_run_contract(client):
    response = client.post(
        "/api/v1/runs",
        json={"query": "Build a resilient web app", "provider_scope": "aws"},
    )
    assert response.status_code == 202
    payload = response.json()
    assert "run_id" in payload

    run_response = client.get(f"/api/v1/runs/{payload['run_id']}")
    assert run_response.status_code == 200
    run_payload = run_response.json()
    assert run_payload["run_id"] == payload["run_id"]
    assert isinstance(run_payload["provider_runs"], list)
