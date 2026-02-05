from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.sede import Sede as SedeModel
from app.schemas import Sede, SedeCreate, SedeUpdate

router = APIRouter(prefix="/sedes", tags=["sedes"])


@router.get("/", response_model=List[Sede])
def listar_sedes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    sedes = db.query(SedeModel).offset(skip).limit(limit).all()
    return sedes


@router.get("/{sede_id}", response_model=Sede)
def obter_sede(sede_id: int, db: Session = Depends(get_db)):
    sede = db.query(SedeModel).filter(SedeModel.id == sede_id).first()
    if not sede:
        raise HTTPException(status_code=404, detail="Sede não encontrada")
    return sede


@router.post("/", response_model=Sede)
def criar_sede(sede: SedeCreate, db: Session = Depends(get_db)):
    db_sede = SedeModel(**sede.model_dump())
    db.add(db_sede)
    db.commit()
    db.refresh(db_sede)
    return db_sede


@router.put("/{sede_id}", response_model=Sede)
def atualizar_sede(sede_id: int, sede: SedeUpdate, db: Session = Depends(get_db)):
    db_sede = db.query(SedeModel).filter(SedeModel.id == sede_id).first()
    if not db_sede:
        raise HTTPException(status_code=404, detail="Sede não encontrada")
    
    for key, value in sede.model_dump(exclude_unset=True).items():
        setattr(db_sede, key, value)
    
    db.commit()
    db.refresh(db_sede)
    return db_sede


@router.delete("/{sede_id}")
def deletar_sede(sede_id: int, db: Session = Depends(get_db)):
    db_sede = db.query(SedeModel).filter(SedeModel.id == sede_id).first()
    if not db_sede:
        raise HTTPException(status_code=404, detail="Sede não encontrada")
    
    db.delete(db_sede)
    db.commit()
    return {"message": "Sede deletada com sucesso"}
