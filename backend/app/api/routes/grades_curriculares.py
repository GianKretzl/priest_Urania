from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import List
from app.core.database import get_db
from app.models.grade_curricular import GradeCurricular as GradeCurricularModel
from app.schemas import GradeCurricular, GradeCurricularCreate, GradeCurricularUpdate

router = APIRouter(prefix="/grades-curriculares", tags=["grades-curriculares"])


@router.get("/", response_model=List[GradeCurricular])
def listar_grades(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    grades = db.query(GradeCurricularModel).options(
        joinedload(GradeCurricularModel.turma),
        joinedload(GradeCurricularModel.disciplina),
        joinedload(GradeCurricularModel.professor)
    ).offset(skip).limit(limit).all()
    return grades


@router.get("/turma/{turma_id}", response_model=List[GradeCurricular])
def listar_grades_por_turma(turma_id: int, db: Session = Depends(get_db)):
    grades = db.query(GradeCurricularModel).options(
        joinedload(GradeCurricularModel.turma),
        joinedload(GradeCurricularModel.disciplina),
        joinedload(GradeCurricularModel.professor)
    ).filter(GradeCurricularModel.turma_id == turma_id).all()
    return grades


@router.get("/professor/{professor_id}", response_model=List[GradeCurricular])
def listar_grades_por_professor(professor_id: int, db: Session = Depends(get_db)):
    grades = db.query(GradeCurricularModel).filter(GradeCurricularModel.professor_id == professor_id).all()
    return grades


@router.get("/{grade_id}", response_model=GradeCurricular)
def obter_grade(grade_id: int, db: Session = Depends(get_db)):
    grade = db.query(GradeCurricularModel).filter(GradeCurricularModel.id == grade_id).first()
    if not grade:
        raise HTTPException(status_code=404, detail="Grade curricular não encontrada")
    return grade


@router.post("/", response_model=GradeCurricular)
def criar_grade(grade: GradeCurricularCreate, db: Session = Depends(get_db)):
    db_grade = GradeCurricularModel(**grade.model_dump())
    db.add(db_grade)
    db.commit()
    db.refresh(db_grade)
    return db_grade


@router.put("/{grade_id}", response_model=GradeCurricular)
def atualizar_grade(grade_id: int, grade: GradeCurricularUpdate, db: Session = Depends(get_db)):
    db_grade = db.query(GradeCurricularModel).filter(GradeCurricularModel.id == grade_id).first()
    if not db_grade:
        raise HTTPException(status_code=404, detail="Grade curricular não encontrada")
    
    for key, value in grade.model_dump(exclude_unset=True).items():
        setattr(db_grade, key, value)
    
    db.commit()
    db.refresh(db_grade)
    return db_grade


@router.delete("/{grade_id}")
def deletar_grade(grade_id: int, db: Session = Depends(get_db)):
    db_grade = db.query(GradeCurricularModel).filter(GradeCurricularModel.id == grade_id).first()
    if not db_grade:
        raise HTTPException(status_code=404, detail="Grade curricular não encontrada")
    
    db.delete(db_grade)
    db.commit()
    return {"message": "Grade curricular deletada com sucesso"}
