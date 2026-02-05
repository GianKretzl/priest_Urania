from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.ambiente import Ambiente as AmbienteModel
from app.schemas import Ambiente, AmbienteCreate, AmbienteUpdate

router = APIRouter(prefix="/ambientes", tags=["ambientes"])


@router.get("/", response_model=List[Ambiente])
def listar_ambientes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    ambientes = db.query(AmbienteModel).offset(skip).limit(limit).all()
    return ambientes


@router.get("/sede/{sede_id}", response_model=List[Ambiente])
def listar_ambientes_por_sede(sede_id: int, db: Session = Depends(get_db)):
    ambientes = db.query(AmbienteModel).filter(AmbienteModel.sede_id == sede_id).all()
    return ambientes


@router.get("/{ambiente_id}", response_model=Ambiente)
def obter_ambiente(ambiente_id: int, db: Session = Depends(get_db)):
    ambiente = db.query(AmbienteModel).filter(AmbienteModel.id == ambiente_id).first()
    if not ambiente:
        raise HTTPException(status_code=404, detail="Ambiente não encontrado")
    return ambiente


@router.post("/", response_model=Ambiente)
def criar_ambiente(ambiente: AmbienteCreate, db: Session = Depends(get_db)):
    db_ambiente = AmbienteModel(**ambiente.model_dump())
    db.add(db_ambiente)
    db.commit()
    db.refresh(db_ambiente)
    return db_ambiente


@router.put("/{ambiente_id}", response_model=Ambiente)
def atualizar_ambiente(ambiente_id: int, ambiente: AmbienteUpdate, db: Session = Depends(get_db)):
    db_ambiente = db.query(AmbienteModel).filter(AmbienteModel.id == ambiente_id).first()
    if not db_ambiente:
        raise HTTPException(status_code=404, detail="Ambiente não encontrado")
    
    for key, value in ambiente.model_dump(exclude_unset=True).items():
        setattr(db_ambiente, key, value)
    
    db.commit()
    db.refresh(db_ambiente)
    return db_ambiente


@router.delete("/{ambiente_id}")
def deletar_ambiente(ambiente_id: int, db: Session = Depends(get_db)):
    db_ambiente = db.query(AmbienteModel).filter(AmbienteModel.id == ambiente_id).first()
    if not db_ambiente:
        raise HTTPException(status_code=404, detail="Ambiente não encontrado")
    
    db.delete(db_ambiente)
    db.commit()
    return {"message": "Ambiente deletado com sucesso"}
