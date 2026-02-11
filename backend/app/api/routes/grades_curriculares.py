from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import List
from pydantic import BaseModel
from app.core.database import get_db
from app.models.grade_curricular import GradeCurricular as GradeCurricularModel
from app.models.turma import Turma
from app.models.professor import Professor
from app.schemas import GradeCurricular, GradeCurricularCreate, GradeCurricularUpdate


class CopiarGradesRequest(BaseModel):
    turma_origem_id: int
    turma_destino_id: int
    sobrescrever: bool = True

router = APIRouter(prefix="/grades-curriculares", tags=["grades-curriculares"])


@router.get("/", response_model=List[GradeCurricular])
def listar_grades(skip: int = 0, limit: int = 500, db: Session = Depends(get_db)):
    grades = db.query(GradeCurricularModel).options(
        joinedload(GradeCurricularModel.turma),
        joinedload(GradeCurricularModel.disciplina),
        joinedload(GradeCurricularModel.professor)
    ).offset(skip).limit(limit).all()
    
    # Carregar professor_2 manualmente para cada grade
    for grade in grades:
        if grade.professor_id_2:
            grade.professor_2 = db.query(Professor).filter(Professor.id == grade.professor_id_2).first()
    
    return grades


@router.get("/turma/{turma_id}", response_model=List[GradeCurricular])
def listar_grades_por_turma(turma_id: int, db: Session = Depends(get_db)):
    grades = db.query(GradeCurricularModel).options(
        joinedload(GradeCurricularModel.turma),
        joinedload(GradeCurricularModel.disciplina),
        joinedload(GradeCurricularModel.professor)
    ).filter(GradeCurricularModel.turma_id == turma_id).all()
    
    # Carregar professor_2 manualmente para cada grade
    for grade in grades:
        if grade.professor_id_2:
            grade.professor_2 = db.query(Professor).filter(Professor.id == grade.professor_id_2).first()
    
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
    
    # Carregar professor_2 se existir
    if grade.professor_id_2:
        grade.professor_2 = db.query(Professor).filter(Professor.id == grade.professor_id_2).first()
    
    return grade


@router.post("/", response_model=GradeCurricular)
def criar_grade(grade: GradeCurricularCreate, db: Session = Depends(get_db)):
    db_grade = GradeCurricularModel(**grade.model_dump())
    db.add(db_grade)
    db.commit()
    db.refresh(db_grade)
    
    # Carregar professor_2 se existir
    if db_grade.professor_id_2:
        db_grade.professor_2 = db.query(Professor).filter(Professor.id == db_grade.professor_id_2).first()
    
    return db_grade


@router.put("/{grade_id}", response_model=GradeCurricular)
def atualizar_grade(grade_id: int, grade: GradeCurricularUpdate, db: Session = Depends(get_db)):
    db_grade = db.query(GradeCurricularModel).options(
        joinedload(GradeCurricularModel.turma),
        joinedload(GradeCurricularModel.disciplina),
        joinedload(GradeCurricularModel.professor)
    ).filter(GradeCurricularModel.id == grade_id).first()
    
    if not db_grade:
        raise HTTPException(status_code=404, detail="Grade curricular não encontrada")
    
    # Use exclude_unset=True mas trate None explicitamente para professor_id_2
    update_data = grade.model_dump(exclude_unset=True)
    
    # Se professor_id_2 está presente no update (mesmo que seja None), atualizar
    if 'professor_id_2' in update_data:
        db_grade.professor_id_2 = update_data['professor_id_2']
    
    # Atualizar os outros campos
    for key, value in update_data.items():
        if key != 'professor_id_2':  # Já tratamos isso acima
            setattr(db_grade, key, value)
    
    db.commit()
    db.refresh(db_grade)
    
    # Carregar professor_2 se existir
    if db_grade.professor_id_2:
        db_grade.professor_2 = db.query(Professor).filter(Professor.id == db_grade.professor_id_2).first()
    else:
        db_grade.professor_2 = None
    
    return db_grade


@router.delete("/{grade_id}")
def deletar_grade(grade_id: int, db: Session = Depends(get_db)):
    db_grade = db.query(GradeCurricularModel).filter(GradeCurricularModel.id == grade_id).first()
    if not db_grade:
        raise HTTPException(status_code=404, detail="Grade curricular não encontrada")
    
    db.delete(db_grade)
    db.commit()
    return {"message": "Grade curricular deletada com sucesso"}


@router.post("/copiar")
def copiar_grades(request: CopiarGradesRequest, db: Session = Depends(get_db)):
    """
    Copia todas as grades curriculares de uma turma para outra
    """
    # Verificar se as turmas existem
    turma_origem = db.query(Turma).filter(Turma.id == request.turma_origem_id).first()
    turma_destino = db.query(Turma).filter(Turma.id == request.turma_destino_id).first()
    
    if not turma_origem:
        raise HTTPException(status_code=404, detail="Turma de origem não encontrada")
    if not turma_destino:
        raise HTTPException(status_code=404, detail="Turma de destino não encontrada")
    
    if request.turma_origem_id == request.turma_destino_id:
        raise HTTPException(status_code=400, detail="Turma de origem e destino devem ser diferentes")
    
    # Buscar grades da turma de origem
    grades_origem = db.query(GradeCurricularModel).filter(
        GradeCurricularModel.turma_id == request.turma_origem_id
    ).all()
    
    if not grades_origem:
        raise HTTPException(status_code=404, detail="Nenhuma grade encontrada na turma de origem")
    
    # Se sobrescrever, deletar grades existentes da turma de destino
    if request.sobrescrever:
        db.query(GradeCurricularModel).filter(
            GradeCurricularModel.turma_id == request.turma_destino_id
        ).delete()
    
    # Copiar cada grade
    grades_copiadas = 0
    for grade_original in grades_origem:
        nova_grade = GradeCurricularModel(
            turma_id=request.turma_destino_id,
            disciplina_id=grade_original.disciplina_id,
            professor_id=grade_original.professor_id,
            professor_id_2=grade_original.professor_id_2,
            aulas_por_semana=grade_original.aulas_por_semana,
            ativa=grade_original.ativa
        )
        db.add(nova_grade)
        grades_copiadas += 1
    
    db.commit()
    
    return {
        "success": True,
        "message": f"{grades_copiadas} grade(s) copiada(s) de {turma_origem.nome} para {turma_destino.nome}",
        "turma_origem": turma_origem.nome,
        "turma_destino": turma_destino.nome,
        "grades_copiadas": grades_copiadas
    }
