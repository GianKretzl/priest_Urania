from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.horario import Horario as HorarioModel, HorarioAula
from app.schemas import (
    Horario,
    HorarioCreate,
    HorarioUpdate,
    HorarioAula as HorarioAulaSchema,
    GerarHorarioRequest,
    GerarHorarioResponse
)
from app.scheduler.generator import HorarioGenerator

router = APIRouter(prefix="/horarios", tags=["horarios"])


@router.get("/", response_model=List[Horario])
def listar_horarios(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    horarios = db.query(HorarioModel).offset(skip).limit(limit).all()
    return horarios


@router.get("/{horario_id}", response_model=Horario)
def obter_horario(horario_id: int, db: Session = Depends(get_db)):
    horario = db.query(HorarioModel).filter(HorarioModel.id == horario_id).first()
    if not horario:
        raise HTTPException(status_code=404, detail="Horário não encontrado")
    return horario


@router.get("/{horario_id}/aulas", response_model=List[HorarioAulaSchema])
def listar_aulas_horario(horario_id: int, db: Session = Depends(get_db)):
    # Verificar se horário existe
    horario = db.query(HorarioModel).filter(HorarioModel.id == horario_id).first()
    if not horario:
        raise HTTPException(status_code=404, detail="Horário não encontrado")
    
    aulas = db.query(HorarioAula).filter(HorarioAula.horario_id == horario_id).all()
    return aulas


@router.get("/{horario_id}/turma/{turma_id}", response_model=List[HorarioAulaSchema])
def listar_aulas_por_turma(horario_id: int, turma_id: int, db: Session = Depends(get_db)):
    aulas = db.query(HorarioAula).filter(
        HorarioAula.horario_id == horario_id,
        HorarioAula.turma_id == turma_id
    ).order_by(HorarioAula.dia_semana, HorarioAula.ordem).all()
    return aulas


@router.get("/{horario_id}/professor/{professor_id}", response_model=List[HorarioAulaSchema])
def listar_aulas_por_professor(horario_id: int, professor_id: int, db: Session = Depends(get_db)):
    aulas = db.query(HorarioAula).filter(
        HorarioAula.horario_id == horario_id,
        HorarioAula.professor_id == professor_id
    ).order_by(HorarioAula.dia_semana, HorarioAula.ordem).all()
    return aulas


@router.post("/", response_model=Horario)
def criar_horario(horario: HorarioCreate, db: Session = Depends(get_db)):
    db_horario = HorarioModel(**horario.model_dump())
    db.add(db_horario)
    db.commit()
    db.refresh(db_horario)
    return db_horario


@router.put("/{horario_id}", response_model=Horario)
def atualizar_horario(horario_id: int, horario: HorarioUpdate, db: Session = Depends(get_db)):
    db_horario = db.query(HorarioModel).filter(HorarioModel.id == horario_id).first()
    if not db_horario:
        raise HTTPException(status_code=404, detail="Horário não encontrado")
    
    for key, value in horario.model_dump(exclude_unset=True).items():
        setattr(db_horario, key, value)
    
    db.commit()
    db.refresh(db_horario)
    return db_horario


@router.post("/{horario_id}/gerar", response_model=GerarHorarioResponse)
def gerar_horario(horario_id: int, request: GerarHorarioRequest, db: Session = Depends(get_db)):
    """
    Endpoint principal para gerar o horário usando o motor de otimização.
    Similar ao sistema Urânia.
    """
    # Verificar se horário existe
    horario = db.query(HorarioModel).filter(HorarioModel.id == horario_id).first()
    if not horario:
        raise HTTPException(status_code=404, detail="Horário não encontrado")
    
    # Atualizar status
    horario.status = "EM_PROGRESSO"
    db.commit()
    
    try:
        # Criar gerador
        generator = HorarioGenerator(db, horario_id)
        
        # Gerar horário
        resultado = generator.gerar(tempo_maximo=request.tempo_maximo_geracao)
        
        return GerarHorarioResponse(
            success=resultado["success"],
            message=resultado["message"],
            horario_id=horario_id,
            total_aulas=resultado.get("total_aulas", 0),
            aulas_alocadas=resultado.get("aulas_alocadas", 0),
            pendencias=resultado.get("pendencias", []),
            qualidade_score=resultado.get("qualidade_score", 0),
            tempo_geracao=resultado.get("tempo_geracao", 0)
        )
    
    except Exception as e:
        # Reverter status em caso de erro
        horario.status = "RASCUNHO"
        db.commit()
        raise HTTPException(status_code=500, detail=f"Erro ao gerar horário: {str(e)}")


@router.delete("/{horario_id}")
def deletar_horario(horario_id: int, db: Session = Depends(get_db)):
    db_horario = db.query(HorarioModel).filter(HorarioModel.id == horario_id).first()
    if not db_horario:
        raise HTTPException(status_code=404, detail="Horário não encontrado")
    
    # Deletar aulas associadas
    db.query(HorarioAula).filter(HorarioAula.horario_id == horario_id).delete()
    
    db.delete(db_horario)
    db.commit()
    return {"message": "Horário deletado com sucesso"}
