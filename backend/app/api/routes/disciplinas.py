from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.disciplina import Disciplina as DisciplinaModel
from app.schemas import Disciplina, DisciplinaCreate, DisciplinaUpdate

router = APIRouter(prefix="/disciplinas", tags=["disciplinas"])


@router.get("/", response_model=List[Disciplina])
def listar_disciplinas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    disciplinas = db.query(DisciplinaModel).offset(skip).limit(limit).all()
    return disciplinas


@router.get("/{disciplina_id}", response_model=Disciplina)
def obter_disciplina(disciplina_id: int, db: Session = Depends(get_db)):
    disciplina = db.query(DisciplinaModel).filter(DisciplinaModel.id == disciplina_id).first()
    if not disciplina:
        raise HTTPException(status_code=404, detail="Disciplina não encontrada")
    return disciplina


@router.post("/", response_model=Disciplina)
def criar_disciplina(disciplina: DisciplinaCreate, db: Session = Depends(get_db)):
    db_disciplina = DisciplinaModel(**disciplina.model_dump())
    db.add(db_disciplina)
    db.commit()
    db.refresh(db_disciplina)
    return db_disciplina


@router.put("/{disciplina_id}", response_model=Disciplina)
def atualizar_disciplina(disciplina_id: int, disciplina: DisciplinaUpdate, db: Session = Depends(get_db)):
    db_disciplina = db.query(DisciplinaModel).filter(DisciplinaModel.id == disciplina_id).first()
    if not db_disciplina:
        raise HTTPException(status_code=404, detail="Disciplina não encontrada")
    
    for key, value in disciplina.model_dump(exclude_unset=True).items():
        setattr(db_disciplina, key, value)
    
    db.commit()
    db.refresh(db_disciplina)
    return db_disciplina


@router.delete("/{disciplina_id}")
def deletar_disciplina(disciplina_id: int, db: Session = Depends(get_db)):
    db_disciplina = db.query(DisciplinaModel).filter(DisciplinaModel.id == disciplina_id).first()
    if not db_disciplina:
        raise HTTPException(status_code=404, detail="Disciplina não encontrada")
    
    db.delete(db_disciplina)
    db.commit()
    return {"message": "Disciplina deletada com sucesso"}
