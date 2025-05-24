from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.main import app
from app import models

test_graph_data = {
    "nodes": [
        {"name": "a"},
        {"name": "b"},
        {"name": "c"}
    ],
    "edges": [
        {"source": "a", "target": "b"},
        {"source": "b", "target": "c"}
    ]
}

def test_graph_reading(client: TestClient):
    response = client.post("/api/graph/", json=test_graph_data)
    graph_id = response.json()["id"]
    
    read_response = client.get(f'/api/graph/{graph_id}/')
    
    if read_response:
        data = read_response.json()
        for node in data['nodes']:
            assert node in test_graph_data["nodes"]
        for edge in data['edges']:
            assert edge in test_graph_data["edges"]

def test_graph_doesnt_exist(client: TestClient):
    response = client.get(f'/api/graph/{777}/')
    assert response.status_code == 404

def test_adjancency_list(client: TestClient):
    response = client.post("/api/graph/", json=test_graph_data)
    graph_id = response.json()["id"]
    
    read_response = client.get(f'/api/graph/{graph_id}/adjacency_list/')
    if read_response:
        data = read_response.json()
        assert data['adjacency_list'] == {"a":["b"],"b":["c"],"c":[]}

def test_adjacency_list_doesnt_exist(client: TestClient):
    response = client.get(f'/api/graph/{777}/adjacency_list/')
    assert response.status_code == 404
            