from fastapi.testclient import TestClient
from control.main import app

def test_blocks_prod_and_accepts_a_readout():
    client = TestClient(app)
    blocked = client.post("/review", json={"environment": "prod", "monthly_cost": 400, "cost_cap": 100, "citation": "", "image": "billing:latest"}).json()
    assert blocked["status"] == "blocked"
    assert blocked["live"] is False
    assert blocked["missing"] == ["policy", "cost_ok", "citation", "pinned_image"]
    ready = client.post("/review", json={"environment": "staging", "monthly_cost": 40, "cost_cap": 100, "citation": "corpus/refusals.md", "image": "billing:1.4.2"}).json()
    assert ready["status"] == "ready_for_readout"
    assert ready["live"] is False
