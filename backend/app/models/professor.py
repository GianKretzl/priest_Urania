from sqlalchemy import Column, Integer, String, Boolean, Float
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property
from app.core.database import Base
from app.models.professor_disciplina import professor_disciplina


class Professor(Base):
    __tablename__ = "professores"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False, index=True)
    email = Column(String, unique=True, nullable=False)
    telefone = Column(String)
    cpf = Column(String, unique=True)
    
    # Carga horária
    carga_horaria_maxima = Column(Integer, default=30)  # Horas de REGÊNCIA semanais (aulas em sala)
    # Nota: Este campo agora representa as horas de regência, não mais a carga total
    # A carga total (jornada) é calculada como: regência + atividade
    
    # Limites de aulas
    max_aulas_seguidas = Column(Integer, default=3)  # Padrão 3, mas não é regra rígida
    max_aulas_dia = Column(Integer, default=12)  # Máximo 12 (6 por período)
    
    ativo = Column(Boolean, default=True)
    
    @property
    def horas_regencia(self) -> int:
        """
        Retorna as horas de regência (aulas em sala).
        Este é o valor base informado pelo usuário.
        """
        return self.carga_horaria_maxima
    
    @property
    def horas_atividade(self) -> int:
        """
        Calcula automaticamente as horas-atividade seguindo a regra 15/5.
        Para cada 3 horas de regência → 1 hora de atividade.
        Exemplo: 30h regência → 10h atividade | 15h regência → 5h atividade
        """
        return int(self.horas_regencia / 3)
    
    @property
    def carga_horaria_total(self) -> int:
        """
        Calcula a carga horária total (jornada de trabalho).
        Total = Horas de Regência + Horas-Atividade
        """
        return self.horas_regencia + self.horas_atividade
    
    # Relacionamentos
    disciplinas = relationship("Disciplina", secondary=professor_disciplina, back_populates="professores")
    grades_curriculares = relationship("GradeCurricular", back_populates="professor", foreign_keys="GradeCurricular.professor_id")
    disponibilidades = relationship("Disponibilidade", back_populates="professor")
    horarios_aula = relationship("HorarioAula", back_populates="professor", foreign_keys="HorarioAula.professor_id")
