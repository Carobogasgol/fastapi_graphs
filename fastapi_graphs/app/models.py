import datetime
import sqlalchemy
import sqlalchemy.orm


class Base(sqlalchemy.orm.DeclarativeBase):
    pass


class Graph(Base):
    __tablename__ = 'graphs'

    id: sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column(primary_key=True, autoincrement=True)
    name: sqlalchemy.orm.Mapped[str] = sqlalchemy.orm.mapped_column(nullable=True)
    created_at: sqlalchemy.orm.Mapped[datetime.datetime] = (
        sqlalchemy.orm.mapped_column(default=datetime.datetime.now)
    )
    updated_at: sqlalchemy.orm.Mapped[datetime.datetime] = sqlalchemy.orm.mapped_column(
        default=datetime.datetime.now,
        onupdate=datetime.datetime.now
    )

    vertices: sqlalchemy.orm.Mapped[list['Vertex']] = sqlalchemy.orm.relationship(
        back_populates='graph', cascade='all, delete-orphan',
    )
    edges: sqlalchemy.orm.Mapped[list["Edge"]] = sqlalchemy.orm.relationship(
        back_populates='graph', cascade='all, delete-orphan',
    )

    def __repr__(self):
        return f"Graph(id={self.id}, name={self.name})"


class Vertex(Base):
    __tablename__ = 'vertices'
    
    id: sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column(primary_key=True, autoincrement=True)
    graph_id: sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column(sqlalchemy.ForeignKey('graphs.id'))
    name: sqlalchemy.orm.Mapped[str] = sqlalchemy.orm.mapped_column(sqlalchemy.String(255), nullable=False)
    
    graph: sqlalchemy.orm.Mapped['Graph'] = sqlalchemy.orm.relationship('Graph', back_populates='vertices')
    out_edges: sqlalchemy.orm.Mapped[list['Edge']] = sqlalchemy.orm.relationship(
        'Edge',
        foreign_keys='Edge.source_id',
        back_populates='source_vertex',
        cascade='all, delete-orphan')
    in_edges: sqlalchemy.orm.Mapped[list['Edge']] = sqlalchemy.orm.relationship(
        'Edge',
        foreign_keys='Edge.target_id',
        back_populates='target_vertex',
        cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'{self.name}'


class Edge(Base):
    __tablename__ = 'edges'
    
    id: sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column(primary_key=True, autoincrement=True)
    graph_id: sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column(sqlalchemy.ForeignKey('graphs.id'))
    source_id: sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column(sqlalchemy.ForeignKey('vertices.id'))
    target_id: sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column(sqlalchemy.ForeignKey('vertices.id'))
    
    graph: sqlalchemy.orm.Mapped['Graph'] = sqlalchemy.orm.relationship('Graph', back_populates='edges')
    source_vertex: sqlalchemy.orm.Mapped['Vertex'] = (
        sqlalchemy.orm.relationship('Vertex', foreign_keys=[source_id], back_populates='out_edges')
    )
    target_vertex: sqlalchemy.orm.Mapped['Vertex'] = (
        sqlalchemy.orm.relationship('Vertex', foreign_keys=[target_id], back_populates='in_edges')
    )
    
    def __repr__(self) -> str:
        return f'{self.source_vertex.name} to {self.target_vertex.name}'
    