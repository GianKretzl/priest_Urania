from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum


class TipoAmbienteEnum(str, enum.Enum):
    SALA_AULA = "SALA_AULA"
    LABORATORIO = "LABORATORIO"
    QUADRA = "QUADRA"
    AUDITORIO = "AUDITORIO"
    BIBLIOTECA = "BIBLIOTECA"
    SALA_INFORMATICA = "SALA_INFORMATICA"


class Ambiente(Base):
    __tablename__ = "ambientes"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False, index=True)
    codigo = Column(String, unique=True, nullable=False)
    tipo = Column(Enum(TipoAmbienteEnum), nullable=False)
    capacidade = Column(Integer, default=30)
    
    sede_id = Column(Integer, ForeignKey("sedes.id"), nullable=False)
    ativo = Column(Boolean, default=True)
    
    # Relacionamentos
    sede = relationship("Sede", back_populates="ambientes")
    horarios_aula = relationship("HorarioAula", back_populates="ambiente")
