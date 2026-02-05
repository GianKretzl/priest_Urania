from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Enum
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum


class DiaSemanaEnum(str, enum.Enum):
    SEGUNDA = "SEGUNDA"
    TERCA = "TERCA"
    QUARTA = "QUARTA"
    QUINTA = "QUINTA"
    SEXTA = "SEXTA"
    SABADO = "SABADO"


class Disponibilidade(Base):
    __tablename__ = "disponibilidades"
    
    id = Column(Integer, primary_key=True, index=True)
    
    professor_id = Column(Integer, ForeignKey("professores.id"), nullable=False)
    
    dia_semana = Column(Enum(DiaSemanaEnum), nullable=False)
    horario_inicio = Column(String, nullable=False)  # Formato: "08:00"
    horario_fim = Column(String, nullable=False)  # Formato: "12:00"
    disponivel = Column(Boolean, default=True)  # True = disponível, False = indisponível
    
    # Relacionamentos
    professor = relationship("Professor", back_populates="disponibilidades")
