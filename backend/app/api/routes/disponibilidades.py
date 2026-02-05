from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.disponibilidade import Disponibilidade as DisponibilidadeModel
from app.schemas import Disponibilidade, DisponibilidadeCreate, DisponibilidadeUpdate

router = APIRouter(prefix="/disponibilidades", tags=["disponibilidades"])


@router.get("/", response_model=List[Disponibilidade])
def listar_disponibilidades(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    disponibilidades = db.query(DisponibilidadeModel).offset(skip).limit(limit).all()
    return disponibilidades


@router.get("/professor/{professor_id}", response_model=List[Disponibilidade])
def listar_disponibilidades_por_professor(professor_id: int, db: Session = Depends(get_db)):
    disponibilidades = db.query(DisponibilidadeModel).filter(
        DisponibilidadeModel.professor_id == professor_id
    ).all()
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
