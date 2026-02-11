from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.models.disponibilidade import Disponibilidade as DisponibilidadeModel, TurnoEnum
from app.schemas import Disponibilidade, DisponibilidadeCreate, DisponibilidadeUpdate

router = APIRouter(prefix="/disponibilidades", tags=["disponibilidades"])


@router.get("/", response_model=List[Disponibilidade])
def listar_disponibilidades(
    skip: int = 0, 
    limit: int = 100, 
    turno: Optional[TurnoEnum] = Query(None, description="Filtrar por turno"),
    db: Session = Depends(get_db)
):
    query = db.query(DisponibilidadeModel)
    
    if turno:
        query = query.filter(DisponibilidadeModel.turno == turno)
    
    disponibilidades = query.offset(skip).limit(limit).all()
    return disponibilidades


@router.get("/professor/{professor_id}", response_model=List[Disponibilidade])
def listar_disponibilidades_por_professor(
    professor_id: int,
    turno: Optional[TurnoEnum] = Query(None, description="Filtrar por turno"),
    db: Session = Depends(get_db)
):
    query = db.query(DisponibilidadeModel).filter(
        DisponibilidadeModel.professor_id == professor_id
    )
    
    if turno:
        query = query.filter(DisponibilidadeModel.turno == turno)
    
    disponibilidades = query.all()
    return disponibilidades


@router.get("/{disponibilidade_id}", response_model=Disponibilidade)
def obter_disponibilidade(disponibilidade_id: int, db: Session = Depends(get_db)):
    disponibilidade = db.query(DisponibilidadeModel).filter(
        DisponibilidadeModel.id == disponibilidade_id
    ).first()
    if not disponibilidade:
        raise HTTPException(status_code=404, detail="Disponibilidade não encontrada")
    return disponibilidade


@router.post("/", response_model=Disponibilidade)
def criar_disponibilidade(disponibilidade: DisponibilidadeCreate, db: Session = Depends(get_db)):
    db_disponibilidade = DisponibilidadeModel(**disponibilidade.model_dump())
    db.add(db_disponibilidade)
    db.commit()
    db.refresh(db_disponibilidade)
    return db_disponibilidade


@router.post("/marcar-dia-nao-trabalha/{professor_id}/{dia_semana}/{turno}")
def marcar_dia_nao_trabalha(
    professor_id: int,
    dia_semana: str,
    turno: str,
    db: Session = Depends(get_db)
):
    """Marca um turno específico como não trabalhado pelo professor"""
    # Remove todas as disponibilidades existentes desse dia e turno
    db.query(DisponibilidadeModel).filter(
        DisponibilidadeModel.professor_id == professor_id,
        DisponibilidadeModel.dia_semana == dia_semana,
        DisponibilidadeModel.turno == turno
    ).delete()
    
    # Cria uma nova marcação de turno não trabalhado
    nova_disp = DisponibilidadeModel(
        professor_id=professor_id,
        dia_semana=dia_semana,
        turno=turno,
        horario_inicio="00:00",
        horario_fim="23:59",
        disponivel=False,
        dia_nao_trabalha=True
    )
    db.add(nova_disp)
    db.commit()
    db.refresh(nova_disp)
    
    return {"message": f"Turno {turno} marcado como não trabalhado", "disponibilidade": nova_disp}


@router.delete("/desmarcar-dia-nao-trabalha/{professor_id}/{dia_semana}/{turno}")
def desmarcar_dia_nao_trabalha(
    professor_id: int,
    dia_semana: str,
    turno: str,
    db: Session = Depends(get_db)
):
    """Remove a marcação de turno não trabalhado"""
    db.query(DisponibilidadeModel).filter(
        DisponibilidadeModel.professor_id == professor_id,
        DisponibilidadeModel.dia_semana == dia_semana,
        DisponibilidadeModel.turno == turno,
        DisponibilidadeModel.dia_nao_trabalha == True
    ).delete()
    db.commit()
    
    return {"message": f"Marcação de turno {turno} não trabalhado removida"}


@router.put("/{disponibilidade_id}", response_model=Disponibilidade)
def atualizar_disponibilidade(
    disponibilidade_id: int,
    disponibilidade: DisponibilidadeUpdate,
    db: Session = Depends(get_db)
):
    db_disponibilidade = db.query(DisponibilidadeModel).filter(
        DisponibilidadeModel.id == disponibilidade_id
    ).first()
    if not db_disponibilidade:
        raise HTTPException(status_code=404, detail="Disponibilidade não encontrada")
    
    for key, value in disponibilidade.model_dump(exclude_unset=True).items():
        setattr(db_disponibilidade, key, value)
    
    db.commit()
    db.refresh(db_disponibilidade)
    return db_disponibilidade


@router.delete("/{disponibilidade_id}")
def deletar_disponibilidade(disponibilidade_id: int, db: Session = Depends(get_db)):
    db_disponibilidade = db.query(DisponibilidadeModel).filter(
        DisponibilidadeModel.id == disponibilidade_id
    ).first()
    if not db_disponibilidade:
        raise HTTPException(status_code=404, detail="Disponibilidade não encontrada")
    
    db.delete(db_disponibilidade)
    db.commit()
    return {"message": "Disponibilidade deletada com sucesso"}
