from sqlalchemy import Column, Integer, ForeignKey, Table
from app.core.database import Base

# Tabela de associação muitos-para-muitos entre Professor e Disciplina
professor_disciplina = Table(
    'professor_disciplina',
    Base.metadata,
    Column('professor_id', Integer, ForeignKey('professores.id', ondelete='CASCADE'), primary_key=True),
    Column('disciplina_id', Integer, ForeignKey('disciplinas.id', ondelete='CASCADE'), primary_key=True)
)
