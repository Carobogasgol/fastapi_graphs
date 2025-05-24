from pydantic import BaseModel
from typing import List, Dict, Any

class Node(BaseModel):
    name: str

class Edge(BaseModel):
    source: str
    target: str

class GraphCreate(BaseModel):
    nodes: List[Node]
    edges: List[Edge]

class GraphCreateResponse(BaseModel):
    id: int

class GraphReadResponse(BaseModel):
    id: int
    nodes: List[Node]
    edges: List[Edge]

class AdjacencyListResponse(BaseModel):
    adjacency_list: Dict[str, List[str]]

class ErrorResponse(BaseModel):
    message: str

class ValidationError(BaseModel):
    loc: List[Any]
    msg: str
    type: str

class HTTPValidationError(BaseModel):
    detail: List[ValidationError] 