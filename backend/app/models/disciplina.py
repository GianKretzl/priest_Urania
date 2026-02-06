from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.professor_disciplina import professor_disciplina


class Disciplina(Base):
    __tablename__ = "disciplinas"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False, index=True)
    carga_horaria_semanal = Column(Integer, nullable=False)  # Número de aulas por semana
    duracao_aula = Column(Integer, default=50)  # Duração em minutos
    cor = Column(String, default="#3B82F6")  # Cor para visualização
    ativa = Column(Boolean, default=True)
    
    # Relacionamentos
    professores = relationship("Professor", secondary=professor_disciplina, back_populates="disciplinas")
    grades_curriculares = relationship("GradeCurricular", back_populates="disciplina")
    horarios_aula = relationship("HorarioAula", back_populates="disciplina")
