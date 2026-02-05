from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum, Boolean, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base
from datetime import datetime
import enum


class StatusHorarioEnum(str, enum.Enum):
    RASCUNHO = "RASCUNHO"
    EM_PROGRESSO = "EM_PROGRESSO"
    FINALIZADO = "FINALIZADO"
    APROVADO = "APROVADO"


class DiaSemanaEnum(str, enum.Enum):
    SEGUNDA = "SEGUNDA"
    TERCA = "TERCA"
    QUARTA = "QUARTA"
    QUINTA = "QUINTA"
    SEXTA = "SEXTA"
    SABADO = "SABADO"


class Horario(Base):
    __tablename__ = "horarios"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    ano_letivo = Column(Integer, nullable=False)
    semestre = Column(Integer, default=1)
    
    status = Column(Enum(StatusHorarioEnum), default=StatusHorarioEnum.RASCUNHO)
    
    data_criacao = Column(DateTime, default=datetime.utcnow)
    data_atualizacao = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Estatísticas da geração
    total_aulas = Column(Integer, default=0)
    aulas_alocadas = Column(Integer, default=0)
    pendencias = Column(JSON, default=[])  # Lista de pendências encontradas
    qualidade_score = Column(Integer, default=0)  # Score de 0-100
    
    # Relacionamentos
    aulas = relationship("HorarioAula", back_populates="horario")


class HorarioAula(Base):
    __tablename__ = "horarios_aulas"
    
    id = Column(Integer, primary_key=True, index=True)
    
    horario_id = Column(Integer, ForeignKey("horarios.id"), nullable=False)
    turma_id = Column(Integer, ForeignKey("turmas.id"), nullable=False)
    disciplina_id = Column(Integer, ForeignKey("disciplinas.id"), nullable=False)
    professor_id = Column(Integer, ForeignKey("professores.id"), nullable=False)
    ambiente_id = Column(Integer, ForeignKey("ambientes.id"), nullable=False)
    
    dia_semana = Column(Enum(DiaSemanaEnum), nullable=False)
    horario_inicio = Column(String, nullable=False)  # Formato: "08:00"
    horario_fim = Column(String, nullable=False)  # Formato: "08:50"
    ordem = Column(Integer, nullable=False)  # 1ª aula, 2ª aula, etc.
    
    # Relacionamentos
    horario = relationship("Horario", back_populates="aulas")
    turma = relationship("Turma", back_populates="horarios_aula")
    disciplina = relationship("Disciplina", back_populates="horarios_aula")
    professor = relationship("Professor", back_populates="horarios_aula")
    ambiente = relationship("Ambiente", back_populates="horarios_aula")
