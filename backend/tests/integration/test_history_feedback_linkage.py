def test_history_includes_iteration_feedback_linkage(client):
    client.post(
        "/api/v1/runs",
        json={"query": "strict fail constraints", "provider_scope": "aws"},
    )

    history = client.get("/api/v1/history")
    assert history.status_code == 200
    items = history.json()["items"]
    assert len(items) >= 1
    provider_runs = items[0]["provider_runs"]
    assert "refinement_feedback" in provider_runs[0]
