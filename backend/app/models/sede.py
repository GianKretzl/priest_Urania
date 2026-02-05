from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.core.database import Base


class Sede(Base):
    __tablename__ = "sedes"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False, index=True)
    endereco = Column(String)
    cidade = Column(String)
    estado = Column(String)
    cep = Column(String)
    ativa = Column(Boolean, default=True)
    
    # Relacionamentos
    ambientes = relationship("Ambiente", back_populates="sede")
