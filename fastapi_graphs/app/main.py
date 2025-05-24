import collections
import logging
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app.database import get_db, engine, recreate_tables
from app import models
from app.schemas import (
    GraphCreate, GraphCreateResponse, GraphReadResponse,
    AdjacencyListResponse, ErrorResponse
)

app = FastAPI(title='FastAPI Project')

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

@app.get('/')
def root():
    return {'message': 'Welcome to FastAPI Project'}

@app.get('/api/graph/{graph_id}', response_model=GraphReadResponse, responses={404: {'model': ErrorResponse}})
def get_graph(graph_id: int, db: Session = Depends(get_db)):
    graph = db.query(models.Graph).filter(models.Graph.id == graph_id).one_or_none()
    if not graph:
        raise HTTPException(status_code=404, detail='Graph entity not found')
    
    return {
        'id': graph.id,
        'nodes': [{'name': vertex.name} for vertex in graph.vertices],
        'edges': [{'source': edge.source_vertex.name, 'target': edge.target_vertex.name} for edge in graph.edges]
    }

@app.get('/api/graph/{graph_id}/adjacency_list', response_model=AdjacencyListResponse, responses={404: {'model': ErrorResponse}})
def get_adjacency_list(graph_id: int, db: Session = Depends(get_db)):
    graph = db.query(models.Graph).filter(models.Graph.id == graph_id).one_or_none()
    if not graph:
        raise HTTPException(status_code=404, detail='Graph not found')
    adjacency_list = {vertex.name: [] for vertex in graph.vertices}
    for vertex in graph.vertices:
        for edge in vertex.out_edges:
            adjacency_list[vertex.name].append(edge.target_vertex.name)
    
    return {'adjacency_list': adjacency_list}

@app.get('/api/graph/{graph_id}/reverse_adjacency_list', response_model=AdjacencyListResponse, responses={404: {'model': ErrorResponse}})
def get_reverse_adjacency_list(graph_id: int, db: Session = Depends(get_db)):
    graph = db.query(models.Graph).filter(models.Graph.id == graph_id).one_or_none()
    if not graph:
        raise HTTPException(status_code=404, detail='Graph not found')
    reverse_adjacency_list = {vertex.name: [] for vertex in graph.vertices}
    for vertex in graph.vertices:
        for edge in vertex.in_edges:
            reverse_adjacency_list[vertex.name].append(edge.source_vertex.name)
    
    return {'adjacency_list': reverse_adjacency_list}

@app.post('/api/graph/', response_model=GraphCreateResponse, status_code=status.HTTP_201_CREATED, responses={400: {'model': ErrorResponse}})
def create_graph(graph_data: GraphCreate, db: Session = Depends(get_db)):
    try:
        graph = models.Graph()
        db.add(graph)
        db.flush()
        
        vertex_map = {}
        for node in graph_data.nodes:
            vertex = models.Vertex(
                graph_id=graph.id,
                name=node.name
            )
            db.add(vertex)
            db.flush()
            vertex_map[node.name] = vertex.id
        
        for edge in graph_data.edges:
            source_id = vertex_map.get(edge.source)
            target_id = vertex_map.get(edge.target)
            
            if not source_id or not target_id:
                raise HTTPException(
                    status_code=400, 
                    detail=f'Invalid edge: vertex not found for source={edge.source} or target={edge.target}'
                )
            
            new_edge = models.Edge(
                graph_id=graph.id,
                source_id=source_id,
                target_id=target_id
            )
            db.add(new_edge)
        
        db.commit()
        return {'id': graph.id}
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@app.delete('/api/graph/{graph_id}/node/{node_name}', status_code=status.HTTP_204_NO_CONTENT, responses={404: {'model': ErrorResponse}})
def delete_node(graph_id: int, node_name: str, db: Session = Depends(get_db)):
    graph = db.query(models.Graph).filter(models.Graph.id == graph_id).one_or_none()
    if not graph:
        raise HTTPException(status_code=404, detail=f'Graph {graph_id} not found')
    
    node = db.query(models.Vertex).filter(
        models.Vertex.graph_id == graph_id,
        models.Vertex.name == node_name
    ).first()
    
    if not node:
        raise HTTPException(status_code=404, detail=f'Node {node_name} not found')
    
    db.delete(node)
    db.commit()
    return None

def create_tables():
    models.Base.metadata.create_all(bind=engine)

app.add_event_handler('startup', create_tables)
