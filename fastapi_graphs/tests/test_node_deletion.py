from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.main import app
from app import models

test_graph_data = {
    'nodes': [
        {'name': 'a'},
        {'name': 'b'},
        {'name': 'c'},
        {'name': 'd'}
    ],
    'edges': [
        {'source': 'a', 'target': 'b'},
        {'source': 'b', 'target': 'c'},
        {'source': 'c', 'target': 'd'},
        {'source': 'd', 'target': 'a'}
    ]
}

def test_delete_node(client: TestClient, db: Session):
    response = client.post('/api/graph/', json=test_graph_data)
    graph_id = response.json()['id']
    
    delete_response = client.delete(f'/api/graph/{graph_id}/node/b/')
    assert delete_response.status_code == 204
    
    vertices = db.query(models.Vertex).filter(models.Vertex.graph_id == graph_id).all()
    vertex_names = {v.name for v in vertices}
    assert 'b' not in vertex_names
    assert len(vertex_names) == 3
    
    edges = db.query(models.Edge).filter(models.Edge.graph_id == graph_id).all()
    edge_connections = set()
    for edge in edges:
        source = db.query(models.Vertex).filter(models.Vertex.id == edge.source_id).first()
        target = db.query(models.Vertex).filter(models.Vertex.id == edge.target_id).first()
        edge_connections.add((source.name, target.name))
    
    assert edge_connections == {('c', 'd'), ('d', 'a')}


def test_delete_node_graph_doesnt_exist(client: TestClient):
    graph_id = 777
    delete_response = client.delete(f'/api/graph/{graph_id}/node/a/')
    assert delete_response.status_code == 404
    assert f'Graph {graph_id} not found' in delete_response.json()['detail'] 