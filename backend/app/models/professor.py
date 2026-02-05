from sqlalchemy import Column, Integer, String, Boolean, Float
from sqlalchemy.orm import relationship
from app.core.database import Base


class Professor(Base):
    __tablename__ = "professores"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False, index=True)
    email = Column(String, unique=True, nullable=False)
    telefone = Column(String)
    cpf = Column(String, unique=True)
    
    # Carga horária
    carga_horaria_maxima = Column(Integer, default=40)  # Horas semanais
    horas_atividade = Column(Integer, default=0)  # Horas para atividades extras
    
    # Limites de aulas
    max_aulas_seguidas = Column(Integer, default=4)
    max_aulas_dia = Column(Integer, default=8)
    
    # Deslocamento
    tempo_deslocamento = Column(Integer, default=0)  # Tempo em minutos
    
    ativo = Column(Boolean, default=True)
    
    # Relacionamentos
    grades_curriculares = relationship("GradeCurricular", back_populates="professor")
    disponibilidades = relationship("Disponibilidade", back_populates="professor")
    horarios_aula = relationship("HorarioAula", back_populates="professor")
