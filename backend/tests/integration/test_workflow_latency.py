import time


def test_workflow_transition_latency_budget(client):
    start = time.perf_counter()
    response = client.post(
        "/api/v1/runs",
        json={"query": "normal workload", "provider_scope": "aws"},
    )
    assert response.status_code == 202
    elapsed = time.perf_counter() - start
    assert elapsed < 2.0
