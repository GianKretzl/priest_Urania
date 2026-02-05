from sqlalchemy import Column, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.core.database import Base


class GradeCurricular(Base):
    __tablename__ = "grades_curriculares"
    
    id = Column(Integer, primary_key=True, index=True)
    
    turma_id = Column(Integer, ForeignKey("turmas.id"), nullable=False)
    disciplina_id = Column(Integer, ForeignKey("disciplinas.id"), nullable=False)
    professor_id = Column(Integer, ForeignKey("professores.id"), nullable=False)
    
    aulas_por_semana = Column(Integer, nullable=False)  # Quantas aulas dessa disciplina por semana
    ativa = Column(Boolean, default=True)
    
    # Relacionamentos
    turma = relationship("Turma", back_populates="grades_curriculares")
    disciplina = relationship("Disciplina", back_populates="grades_curriculares")
    professor = relationship("Professor", back_populates="grades_curriculares")
