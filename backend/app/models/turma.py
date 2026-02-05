from sqlalchemy import Column, Integer, String, Enum, Boolean
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum


class TurnoEnum(str, enum.Enum):
    MATUTINO = "MATUTINO"
    VESPERTINO = "VESPERTINO"
    NOTURNO = "NOTURNO"
    INTEGRAL = "INTEGRAL"


class Turma(Base):
    __tablename__ = "turmas"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False, index=True)
    ano_serie = Column(String, nullable=False)  # Ex: "1º Ano", "5ª Série"
    turno = Column(Enum(TurnoEnum), nullable=False)
    numero_alunos = Column(Integer, default=0)
    ativa = Column(Boolean, default=True)
    
    # Relacionamentos
    grades_curriculares = relationship("GradeCurricular", back_populates="turma")
    horarios_aula = relationship("HorarioAula", back_populates="turma")
