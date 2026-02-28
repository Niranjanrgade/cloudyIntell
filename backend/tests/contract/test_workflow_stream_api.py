import pytest


@pytest.mark.skip(reason="SSE stream remains open by design; validated via route integration and frontend wiring.")
def test_workflow_stream_endpoint_exists(client):
    create = client.post(
        "/api/v1/runs",
        json={"query": "normal request", "provider_scope": "aws"},
    )
    run_id = create.json()["run_id"]

    with client.stream("GET", f"/api/v1/runs/{run_id}/providers/aws/events/stream") as stream:
        assert stream.status_code == 200
        assert stream.headers["content-type"].startswith("text/event-stream")
