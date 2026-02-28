def test_findings_endpoint_payload_shape(client):
    create = client.post(
        "/api/v1/runs",
        json={"query": "strict fail constraints", "provider_scope": "aws"},
    )
    run_id = create.json()["run_id"]

    response = client.get(f"/api/v1/runs/{run_id}/providers/aws/findings")
    assert response.status_code == 200
    payload = response.json()
    assert "items" in payload
    if payload["items"]:
      first = payload["items"][0]
      assert "finding_id" in first
      assert "evidence" in first
