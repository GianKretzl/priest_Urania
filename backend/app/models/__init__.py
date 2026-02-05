from app.models.disciplina import Disciplina
from app.models.turma import Turma
from app.models.professor import Professor
from app.models.sede import Sede
from app.models.ambiente import Ambiente
from app.models.grade_curricular import GradeCurricular
from app.models.disponibilidade import Disponibilidade
from app.models.horario import Horario, HorarioAula
from app.models.restricao import Restricao

__all__ = [
    "Disciplina",
    "Turma",
    "Professor",
    "Sede",
    "Ambiente",
    "GradeCurricular",
    "Disponibilidade",
    "Horario",
    "HorarioAula",
    "Restricao",
]
