from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


class TurnoEnum(str, Enum):
    MATUTINO = "MATUTINO"
    VESPERTINO = "VESPERTINO"
    NOTURNO = "NOTURNO"


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


class StatusHorarioEnum(str, Enum):
    RASCUNHO = "RASCUNHO"
    EM_PROGRESSO = "EM_PROGRESSO"
    FINALIZADO = "FINALIZADO"
    APROVADO = "APROVADO"


# Disciplina Schemas
class DisciplinaBase(BaseModel):
    nome: str
    carga_horaria_semanal: int 
    duracao_aula: int = 50
    cor: str = "#3B82F6"
    ativa: bool = True
    multiplos_professores: bool = False


class DisciplinaCreate(DisciplinaBase):
    pass


class DisciplinaUpdate(BaseModel):
    nome: Optional[str] = None
    carga_horaria_semanal: Optional[int] = None
    duracao_aula: Optional[int] = None
    cor: Optional[str] = None
    ativa: Optional[bool] = None
    multiplos_professores: Optional[bool] = None


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
    carga_horaria_maxima: int = 30  # Horas de REGÊNCIA semanais (em sala de aula)
    # horas_atividade é calculado automaticamente (regra 15/5: 1h atividade a cada 3h de regência)
    max_aulas_seguidas: int = 3
    max_aulas_dia: int = 12
    ativo: bool = True


class ProfessorCreate(ProfessorBase):
    disciplinas_ids: List[int] = []


class ProfessorUpdate(BaseModel):
    nome: Optional[str] = None
    email: Optional[EmailStr] = None
    telefone: Optional[str] = None
    cpf: Optional[str] = None
    carga_horaria_maxima: Optional[int] = None
    # horas_atividade removido - é calculado automaticamente
    max_aulas_seguidas: Optional[int] = None
    max_aulas_dia: Optional[int] = None
    ativo: Optional[bool] = None
    disciplinas_ids: Optional[List[int]] = None


class Professor(ProfessorBase):
    id: int
    horas_regencia: int       # Campo calculado (mesmo valor de carga_horaria_maxima)
    horas_atividade: int      # Campo calculado (horas_regencia / 3)
    carga_horaria_total: int  # Campo calculado (horas_regencia + horas_atividade)
    disciplinas: List[Disciplina] = []
    
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
    professor_id_2: Optional[int] = None
    aulas_por_semana: int
    ativa: bool = True


class GradeCurricularCreate(GradeCurricularBase):
    pass


class GradeCurricularUpdate(BaseModel):
    turma_id: Optional[int] = None
    disciplina_id: Optional[int] = None
    professor_id: Optional[int] = None
    professor_id_2: Optional[int] = None
    aulas_por_semana: Optional[int] = None
    ativa: Optional[bool] = None


class GradeCurricular(GradeCurricularBase):
    id: int
    turma: Optional[Turma] = None
    disciplina: Optional[Disciplina] = None
    professor: Optional[Professor] = None
    professor_2: Optional[Professor] = None
    
    class Config:
        from_attributes = True


# Disponibilidade Schemas
class DisponibilidadeBase(BaseModel):
    professor_id: int
    dia_semana: DiaSemanaEnum
    horario_inicio: str
    horario_fim: str
    disponivel: bool = True
    turno: Optional[TurnoEnum] = None
    dia_nao_trabalha: bool = False


class DisponibilidadeCreate(DisponibilidadeBase):
    pass


class DisponibilidadeUpdate(BaseModel):
    professor_id: Optional[int] = None
    dia_semana: Optional[DiaSemanaEnum] = None
    horario_inicio: Optional[str] = None
    horario_fim: Optional[str] = None
    disponivel: Optional[bool] = None
    turno: Optional[TurnoEnum] = None
    dia_nao_trabalha: Optional[bool] = None


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
    tem_conflitos: bool
    
    class Config:
        from_attributes = True


# HorarioAula Schemas
class HorarioAulaBase(BaseModel):
    horario_id: int
    turma_id: int
    disciplina_id: int
    professor_id: int
    professor_id_2: Optional[int] = None
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
    turno: Optional[TurnoEnum] = None  # Turno específico a ser gerado (None = todos)
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
    tempo_maximo: int
