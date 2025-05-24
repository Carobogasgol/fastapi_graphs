from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.main import app
from app import models

test_graph_data = {
    'nodes': [
        {'name': 'a'},
        {'name': 'b'},
        {'name': 'c'}
    ],
    'edges': [
        {'source': 'a', 'target': 'b'},
        {'source': 'b', 'target': 'c'}
    ]
}

def test_create_graph(client: TestClient, db: Session):
    response = client.post('/api/graph/', json=test_graph_data)
    assert response.status_code == 201
    graph_id = response.json()['id']
    
    graph = db.query(models.Graph).filter(models.Graph.id == graph_id).first()
    assert graph is not None
    
    vertices = db.query(models.Vertex).filter(models.Vertex.graph_id == graph_id).all()
    assert len(vertices) == 3
    vertex_names = {v.name for v in vertices}
    assert vertex_names == {'a', 'b', 'c'}
    
    edges = db.query(models.Edge).filter(models.Edge.graph_id == graph_id).all()
    assert len(edges) == 2
    edge_connections = set()
    for edge in edges:
        source = db.query(models.Vertex).filter(models.Vertex.id == edge.source_id).first()
        target = db.query(models.Vertex).filter(models.Vertex.id == edge.target_id).first()
        edge_connections.add((source.name, target.name))
    assert edge_connections == {('a', 'b'), ('b', 'c')}

def test_create_graph_invalid_data(client: TestClient):
    invalid_data = {
        'nodes': [
            {'name': 'a'},
            {'name': 'b'}
        ],
        'edges': [
            {'source': 'a', 'target': 'c'}
        ]
    }
    response = client.post('/api/graph/', json=invalid_data)
    assert response.status_code == 400
    assert 'Invalid edge' in response.json()['detail']

def test_create_graph_invalid_edge(client: TestClient):
    invalid_data = {
        'nodes': [
            {'name': 'a'},
            {'name': 'b'}
        ],
        'edges': [
            {'source': 'a', 'target': 'b'},
            {'source': 'b', 'target': 'a'}
        ]
    }
    response = client.post('/api/graph/', json=invalid_data)
    assert response.status_code == 201
