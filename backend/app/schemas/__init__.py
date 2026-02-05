from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


class TurnoEnum(str, Enum):
    MATUTINO = "MATUTINO"
    VESPERTINO = "VESPERTINO"
    NOTURNO = "NOTURNO"
    INTEGRAL = "INTEGRAL"


class TipoAmbienteEnum(str, Enum):
    SALA_AULA = "SALA_AULA"
    LABORATORIO = "LABORATORIO"
    QUADRA = "QUADRA"
    AUDITORIO = "AUDITORIO"
    BIBLIOTECA = "BIBLIOTECA"
    SALA_INFORMATICA = "SALA_INFORMATICA"


class DiaSemanaEnum(str, Enum):
    SEGUNDA = "SEGUNDA"
    TERCA = "TERCA"
    QUARTA = "QUARTA"
    QUINTA = "QUINTA"
    SEXTA = "SEXTA"
    SABADO = "SABADO"


class StatusHorarioEnum(str, Enum):
    RASCUNHO = "RASCUNHO"
    EM_PROGRESSO = "EM_PROGRESSO"
    FINALIZADO = "FINALIZADO"
    APROVADO = "APROVADO"


# Disciplina Schemas
class DisciplinaBase(BaseModel):
    nome: str
    codigo: str
    carga_horaria_semanal: int 
    duracao_aula: int = 50
    cor: str = "#3B82F6"
    ativa: bool = True


class DisciplinaCreate(DisciplinaBase):
    pass


class DisciplinaUpdate(BaseModel):
    nome: Optional[str] = None
    codigo: Optional[str] = None
    carga_horaria_semanal: Optional[int] = None
    duracao_aula: Optional[int] = None
    cor: Optional[str] = None
    ativa: Optional[bool] = None


class Disciplina(DisciplinaBase):
    id: int
    
    class Config:
        from_attributes = True


# Turma Schemas
class TurmaBase(BaseModel):
    nome: str
    ano_serie: str
    turno: TurnoEnum
    numero_alunos: int = 0
    ativa: bool = True


class TurmaCreate(TurmaBase):
    pass


class TurmaUpdate(BaseModel):
    nome: Optional[str] = None
    ano_serie: Optional[str] = None
    turno: Optional[TurnoEnum] = None
    numero_alunos: Optional[int] = None
    ativa: Optional[bool] = None


class Turma(TurmaBase):
    id: int
    
    class Config:
        from_attributes = True


# Professor Schemas
class ProfessorBase(BaseModel):
    nome: str
    email: EmailStr
    telefone: Optional[str] = None
    cpf: Optional[str] = None
    carga_horaria_maxima: int = 40
    horas_atividade: int = 0
    max_aulas_seguidas: int = 4
    max_aulas_dia: int = 8
    tempo_deslocamento: int = 0
    ativo: bool = True


class ProfessorCreate(ProfessorBase):
    pass


class ProfessorUpdate(BaseModel):
    nome: Optional[str] = None
    email: Optional[EmailStr] = None
    telefone: Optional[str] = None
    cpf: Optional[str] = None
    carga_horaria_maxima: Optional[int] = None
    horas_atividade: Optional[int] = None
    max_aulas_seguidas: Optional[int] = None
    max_aulas_dia: Optional[int] = None
    tempo_deslocamento: Optional[int] = None
    ativo: Optional[bool] = None


class Professor(ProfessorBase):
    id: int
    
    class Config:
        from_attributes = True


# Sede Schemas
class SedeBase(BaseModel):
    nome: str
    endereco: Optional[str] = None
    cidade: Optional[str] = None
    estado: Optional[str] = None
    cep: Optional[str] = None
    ativa: bool = True


class SedeCreate(SedeBase):
    pass


class SedeUpdate(BaseModel):
    nome: Optional[str] = None
    endereco: Optional[str] = None
    cidade: Optional[str] = None
    estado: Optional[str] = None
    cep: Optional[str] = None
    ativa: Optional[bool] = None


class Sede(SedeBase):
    id: int
    
    class Config:
        from_attributes = True


# Ambiente Schemas
class AmbienteBase(BaseModel):
    nome: str
    codigo: str
    tipo: TipoAmbienteEnum
    capacidade: int = 30
    sede_id: int
    ativo: bool = True


class AmbienteCreate(AmbienteBase):
    pass


class AmbienteUpdate(BaseModel):
    nome: Optional[str] = None
    codigo: Optional[str] = None
    tipo: Optional[TipoAmbienteEnum] = None
    capacidade: Optional[int] = None
    sede_id: Optional[int] = None
    ativo: Optional[bool] = None


class Ambiente(AmbienteBase):
    id: int
    
    class Config:
        from_attributes = True


# Grade Curricular Schemas
class GradeCurricularBase(BaseModel):
    turma_id: int
    disciplina_id: int
    professor_id: int
    aulas_por_semana: int
    ativa: bool = True


class GradeCurricularCreate(GradeCurricularBase):
    pass


class GradeCurricularUpdate(BaseModel):
    turma_id: Optional[int] = None
    disciplina_id: Optional[int] = None
    professor_id: Optional[int] = None
    aulas_por_semana: Optional[int] = None
    ativa: Optional[bool] = None


class GradeCurricular(GradeCurricularBase):
    id: int
    
    class Config:
        from_attributes = True


# Disponibilidade Schemas
class DisponibilidadeBase(BaseModel):
    professor_id: int
    dia_semana: DiaSemanaEnum
    horario_inicio: str
    horario_fim: str
    disponivel: bool = True


class DisponibilidadeCreate(DisponibilidadeBase):
    pass


class DisponibilidadeUpdate(BaseModel):
    professor_id: Optional[int] = None
    dia_semana: Optional[DiaSemanaEnum] = None
    horario_inicio: Optional[str] = None
    horario_fim: Optional[str] = None
    disponivel: Optional[bool] = None


class Disponibilidade(DisponibilidadeBase):
    id: int
    
    class Config:
        from_attributes = True


# Horário Schemas
class HorarioBase(BaseModel):
    nome: str
    ano_letivo: int
    semestre: int = 1
    status: StatusHorarioEnum = StatusHorarioEnum.RASCUNHO


class HorarioCreate(HorarioBase):
    pass


class HorarioUpdate(BaseModel):
    nome: Optional[str] = None
    ano_letivo: Optional[int] = None
    semestre: Optional[int] = None
    status: Optional[StatusHorarioEnum] = None


class Horario(HorarioBase):
    id: int
    data_criacao: datetime
    data_atualizacao: datetime
    total_aulas: int
    aulas_alocadas: int
    pendencias: List[dict] = []
    qualidade_score: int
    
    class Config:
        from_attributes = True


# HorarioAula Schemas
class HorarioAulaBase(BaseModel):
    horario_id: int
    turma_id: int
    disciplina_id: int
    professor_id: int
    ambiente_id: int
    dia_semana: DiaSemanaEnum
    horario_inicio: str
    horario_fim: str
    ordem: int


class HorarioAulaCreate(HorarioAulaBase):
    pass


class HorarioAula(HorarioAulaBase):
    id: int
    
    class Config:
        from_attributes = True


# Geração de Horário
class GerarHorarioRequest(BaseModel):
    horario_id: int
    limitar_janelas: bool = True
    respeitar_deslocamento: bool = True
    distribuir_uniformemente: bool = True
    tempo_maximo_geracao: int = 300  # segundos


class GerarHorarioResponse(BaseModel):
    success: bool
    message: str
    horario_id: int
    total_aulas: int
    aulas_alocadas: int
    pendencias: List[dict]
    qualidade_score: int
    tempo_geracao: float
