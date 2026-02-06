from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import List
from app.core.database import get_db
from app.models.professor import Professor as ProfessorModel
from app.models.disciplina import Disciplina as DisciplinaModel
from app.schemas import Professor, ProfessorCreate, ProfessorUpdate

router = APIRouter(prefix="/professores", tags=["professores"])


@router.get("/", response_model=List[Professor])
def listar_professores(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    professores = db.query(ProfessorModel).options(joinedload(ProfessorModel.disciplinas)).offset(skip).limit(limit).all()
    return professores


@router.get("/{professor_id}", response_model=Professor)
def obter_professor(professor_id: int, db: Session = Depends(get_db)):
    professor = db.query(ProfessorModel).options(joinedload(ProfessorModel.disciplinas)).filter(ProfessorModel.id == professor_id).first()
    if not professor:
        raise HTTPException(status_code=404, detail="Professor não encontrado")
    return professor


@router.post("/", response_model=Professor)
def criar_professor(professor: ProfessorCreate, db: Session = Depends(get_db)):
    professor_data = professor.model_dump(exclude={'disciplinas_ids'})
    db_professor = ProfessorModel(**professor_data)
    
    # Associar disciplinas
    if professor.disciplinas_ids:
        disciplinas = db.query(DisciplinaModel).filter(
            DisciplinaModel.id.in_(professor.disciplinas_ids)
        ).all()
        db_professor.disciplinas = disciplinas
    
    db.add(db_professor)
    db.commit()
    db.refresh(db_professor)
    return db_professor


@router.put("/{professor_id}", response_model=Professor)
def atualizar_professor(professor_id: int, professor: ProfessorUpdate, db: Session = Depends(get_db)):
    db_professor = db.query(ProfessorModel).filter(ProfessorModel.id == professor_id).first()
    if not db_professor:
        raise HTTPException(status_code=404, detail="Professor não encontrado")
    
    professor_data = professor.model_dump(exclude_unset=True, exclude={'disciplinas_ids'})
    for key, value in professor_data.items():
        setattr(db_professor, key, value)
    
    # Atualizar disciplinas se fornecido
    if professor.disciplinas_ids is not None:
        disciplinas = db.query(DisciplinaModel).filter(
            DisciplinaModel.id.in_(professor.disciplinas_ids)
        ).all()
        db_professor.disciplinas = disciplinas
    
    db.commit()
    db.refresh(db_professor)
    return db_professor


@router.delete("/{professor_id}")
def deletar_professor(professor_id: int, db: Session = Depends(get_db)):
    db_professor = db.query(ProfessorModel).filter(ProfessorModel.id == professor_id).first()
    if not db_professor:
        raise HTTPException(status_code=404, detail="Professor não encontrado")
    
    db.delete(db_professor)
    db.commit()
    return {"message": "Professor deletado com sucesso"}
