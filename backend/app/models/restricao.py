from sqlalchemy import Column, Integer, String, Boolean, Enum
from app.core.database import Base
import enum


class TipoRestricaoEnum(str, enum.Enum):
    MAX_AULAS_SEGUIDAS = "MAX_AULAS_SEGUIDAS"
    MAX_AULAS_DIA = "MAX_AULAS_DIA"
    JANELAS_PROFESSOR = "JANELAS_PROFESSOR"
    DISPONIBILIDADE = "DISPONIBILIDADE"
    DESLOCAMENTO = "DESLOCAMENTO"
    HORAS_ATIVIDADE = "HORAS_ATIVIDADE"


class Restricao(Base):
    __tablename__ = "restricoes"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    tipo = Column(Enum(TipoRestricaoEnum), nullable=False)
    descricao = Column(String)
    peso = Column(Integer, default=1)  # Peso da restrição (1-10)
    ativa = Column(Boolean, default=True)
