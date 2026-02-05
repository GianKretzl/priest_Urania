from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.turma import Turma as TurmaModel
from app.schemas import Turma, TurmaCreate, TurmaUpdate

router = APIRouter(prefix="/turmas", tags=["turmas"])


@router.get("/", response_model=List[Turma])
def listar_turmas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    turmas = db.query(TurmaModel).offset(skip).limit(limit).all()
    return turmas


@router.get("/{turma_id}", response_model=Turma)
def obter_turma(turma_id: int, db: Session = Depends(get_db)):
    turma = db.query(TurmaModel).filter(TurmaModel.id == turma_id).first()
    if not turma:
        raise HTTPException(status_code=404, detail="Turma não encontrada")
    return turma


@router.post("/", response_model=Turma)
def criar_turma(turma: TurmaCreate, db: Session = Depends(get_db)):
    db_turma = TurmaModel(**turma.model_dump())
    db.add(db_turma)
    db.commit()
    db.refresh(db_turma)
    return db_turma


@router.put("/{turma_id}", response_model=Turma)
def atualizar_turma(turma_id: int, turma: TurmaUpdate, db: Session = Depends(get_db)):
    db_turma = db.query(TurmaModel).filter(TurmaModel.id == turma_id).first()
    if not db_turma:
        raise HTTPException(status_code=404, detail="Turma não encontrada")
    
    for key, value in turma.model_dump(exclude_unset=True).items():
        setattr(db_turma, key, value)
    
    db.commit()
    db.refresh(db_turma)
    return db_turma


@router.delete("/{turma_id}")
def deletar_turma(turma_id: int, db: Session = Depends(get_db)):
    db_turma = db.query(TurmaModel).filter(TurmaModel.id == turma_id).first()
    if not db_turma:
        raise HTTPException(status_code=404, detail="Turma não encontrada")
    
    db.delete(db_turma)
    db.commit()
    return {"message": "Turma deletada com sucesso"}
