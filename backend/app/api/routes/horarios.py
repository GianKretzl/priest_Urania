from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from fastapi.responses import HTMLResponse, PlainTextResponse
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.horario import Horario as HorarioModel, HorarioAula
from app.models.turma import Turma
from app.models.professor import Professor
from app.models.disciplina import Disciplina
from app.models.ambiente import Ambiente
from app.schemas import (
    Horario,
    HorarioCreate,
    HorarioUpdate,
    HorarioAula as HorarioAulaSchema,
    GerarHorarioRequest,
    GerarHorarioResponse
)
from app.scheduler.generator import HorarioGenerator
from app.utils.exporters import HorarioExporter

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
def listar_aulas_horario(horario_id: int, incluir_horas_atividade: bool = False, db: Session = Depends(get_db)):
    # Verificar se horário existe
    horario = db.query(HorarioModel).filter(HorarioModel.id == horario_id).first()
    if not horario:
        raise HTTPException(status_code=404, detail="Horário não encontrado")
    
    # Filtrar aulas (excluir horas atividade por padrão)
    query = db.query(HorarioAula).filter(HorarioAula.horario_id == horario_id)
    if not incluir_horas_atividade:
        query = query.filter(HorarioAula.turma_id.isnot(None))
    
    aulas = query.all()
    return aulas


@router.get("/{horario_id}/turma/{turma_id}", response_model=List[HorarioAulaSchema])
def listar_aulas_por_turma(horario_id: int, turma_id: int, db: Session = Depends(get_db)):
    aulas = db.query(HorarioAula).filter(
        HorarioAula.horario_id == horario_id,
        HorarioAula.turma_id == turma_id
    ).order_by(HorarioAula.dia_semana, HorarioAula.ordem).all()
    return aulas


@router.get("/{horario_id}/professor/{professor_id}", response_model=List[HorarioAulaSchema])
def listar_aulas_por_professor(horario_id: int, professor_id: int, incluir_horas_atividade: bool = True, db: Session = Depends(get_db)):
    """Lista aulas de um professor, incluindo horas atividade por padrão"""
    query = db.query(HorarioAula).filter(
        HorarioAula.horario_id == horario_id,
        HorarioAula.professor_id == professor_id
    )
    
    # Por padrão, incluir horas atividade na visualização por professor
    if not incluir_horas_atividade:
        query = query.filter(HorarioAula.turma_id.isnot(None))
    
    aulas = query.order_by(HorarioAula.dia_semana, HorarioAula.ordem).all()
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
def gerar_horario(
    horario_id: int, 
    request: GerarHorarioRequest, 
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Endpoint principal para gerar o horário usando o motor de otimização.
    """
    # Verificar se horário existe
    horario = db.query(HorarioModel).filter(HorarioModel.id == horario_id).first()
    if not horario:
        raise HTTPException(status_code=404, detail="Horário não encontrado")
    
    # Se já está em progresso, retornar status atual
    if horario.status == "EM_PROGRESSO":
        return GerarHorarioResponse(
            success=False,
            message="Geração já em andamento",
            horario_id=horario_id,
            total_aulas=horario.total_aulas,
            aulas_alocadas=horario.aulas_alocadas,
            pendencias=horario.pendencias,
            qualidade_score=horario.qualidade_score,
            tempo_geracao=0,
            tempo_maximo=request.tempo_maximo_geracao
        )
    
    # Atualizar status
    horario.status = "EM_PROGRESSO"
    db.commit()
    
    # Adicionar tarefa em background
    background_tasks.add_task(gerar_horario_background, horario_id, request)
    
    # Retornar resposta imediata
    return GerarHorarioResponse(
        success=True,
        message="Geração iniciada em background",
        horario_id=horario_id,
        total_aulas=0,
        aulas_alocadas=0,
        pendencias=[],
        qualidade_score=0,
        tempo_geracao=0,
        tempo_maximo=request.tempo_maximo_geracao
    )


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


# ==================== ROTAS DE EXPORTAÇÃO ====================

@router.get("/{horario_id}/export/turma/{turma_id}/html", response_class=HTMLResponse)
def exportar_horario_turma_html(horario_id: int, turma_id: int, db: Session = Depends(get_db)):
    """Exporta horário de uma turma em formato HTML"""
    # Verificar se horário existe
    horario = db.query(HorarioModel).filter(HorarioModel.id == horario_id).first()
    if not horario:
        raise HTTPException(status_code=404, detail="Horário não encontrado")
    
    # Verificar se turma existe
    turma = db.query(Turma).filter(Turma.id == turma_id).first()
    if not turma:
        raise HTTPException(status_code=404, detail="Turma não encontrada")
    
    # Buscar aulas
    aulas = db.query(HorarioAula).filter(
        HorarioAula.horario_id == horario_id,
        HorarioAula.turma_id == turma_id
    ).all()
    
    # Enriquecer com dados relacionados
    aulas_data = []
    for aula in aulas:
        disciplina = db.query(Disciplina).filter(Disciplina.id == aula.disciplina_id).first()
        professor = db.query(Professor).filter(Professor.id == aula.professor_id).first()
        ambiente = db.query(Ambiente).filter(Ambiente.id == aula.ambiente_id).first()
        
        aulas_data.append({
            'turma_id': aula.turma_id,
            'professor_id': aula.professor_id,
            'disciplina_id': aula.disciplina_id,
            'dia_semana': aula.dia_semana,
            'horario_inicio': aula.horario_inicio,
            'horario_fim': aula.horario_fim,
            'ordem': aula.ordem,
            'turma_nome': turma.nome,
            'disciplina_nome': disciplina.nome if disciplina else 'N/A',
            'professor_nome': professor.nome if professor else 'N/A',
            'ambiente_nome': ambiente.nome if ambiente else 'N/A'
        })
    
    # Gerar HTML
    horario_data = {
        'nome': horario.nome,
        'ano_letivo': horario.ano_letivo
    }
    exporter = HorarioExporter(horario_data, aulas_data)
    html = exporter.to_html_turma(turma_id, turma.nome)
    
    return HTMLResponse(content=html)


@router.get("/{horario_id}/export/professor/{professor_id}/html", response_class=HTMLResponse)
def exportar_horario_professor_html(horario_id: int, professor_id: int, db: Session = Depends(get_db)):
    """Exporta horário de um professor em formato HTML"""
    # Verificar se horário existe
    horario = db.query(HorarioModel).filter(HorarioModel.id == horario_id).first()
    if not horario:
        raise HTTPException(status_code=404, detail="Horário não encontrado")
    
    # Verificar se professor existe
    professor = db.query(Professor).filter(Professor.id == professor_id).first()
    if not professor:
        raise HTTPException(status_code=404, detail="Professor não encontrado")
    
    # Buscar aulas
    aulas = db.query(HorarioAula).filter(
        HorarioAula.horario_id == horario_id,
        HorarioAula.professor_id == professor_id
    ).all()
    
    # Enriquecer com dados relacionados
    aulas_data = []
    for aula in aulas:
        turma = db.query(Turma).filter(Turma.id == aula.turma_id).first()
        disciplina = db.query(Disciplina).filter(Disciplina.id == aula.disciplina_id).first()
        ambiente = db.query(Ambiente).filter(Ambiente.id == aula.ambiente_id).first()
        
        aulas_data.append({
            'turma_id': aula.turma_id,
            'professor_id': aula.professor_id,
            'disciplina_id': aula.disciplina_id,
            'dia_semana': aula.dia_semana,
            'horario_inicio': aula.horario_inicio,
            'horario_fim': aula.horario_fim,
            'ordem': aula.ordem,
            'turma_nome': turma.nome if turma else 'N/A',
            'disciplina_nome': disciplina.nome if disciplina else 'N/A',
            'professor_nome': professor.nome,
            'ambiente_nome': ambiente.nome if ambiente else 'N/A'
        })
    
    # Gerar HTML
    horario_data = {
        'nome': horario.nome,
        'ano_letivo': horario.ano_letivo
    }
    exporter = HorarioExporter(horario_data, aulas_data)
    html = exporter.to_html_professor(professor_id, professor.nome)
    
    return HTMLResponse(content=html)


@router.get("/{horario_id}/export/turma/{turma_id}/csv", response_class=PlainTextResponse)
def exportar_horario_turma_csv(horario_id: int, turma_id: int, db: Session = Depends(get_db)):
    """Exporta horário de uma turma em formato CSV"""
    # Verificar se horário existe
    horario = db.query(HorarioModel).filter(HorarioModel.id == horario_id).first()
    if not horario:
        raise HTTPException(status_code=404, detail="Horário não encontrado")
    
    # Verificar se turma existe
    turma = db.query(Turma).filter(Turma.id == turma_id).first()
    if not turma:
        raise HTTPException(status_code=404, detail="Turma não encontrada")
    
    # Buscar aulas
    aulas = db.query(HorarioAula).filter(
        HorarioAula.horario_id == horario_id,
        HorarioAula.turma_id == turma_id
    ).all()
    
    # Enriquecer com dados relacionados
    aulas_data = []
    for aula in aulas:
        disciplina = db.query(Disciplina).filter(Disciplina.id == aula.disciplina_id).first()
        professor = db.query(Professor).filter(Professor.id == aula.professor_id).first()
        ambiente = db.query(Ambiente).filter(Ambiente.id == aula.ambiente_id).first()
        
        aulas_data.append({
            'turma_id': aula.turma_id,
            'professor_id': aula.professor_id,
            'disciplina_id': aula.disciplina_id,
            'dia_semana': aula.dia_semana,
            'horario_inicio': aula.horario_inicio,
            'horario_fim': aula.horario_fim,
            'ordem': aula.ordem,
            'turma_nome': turma.nome,
            'disciplina_nome': disciplina.nome if disciplina else 'N/A',
            'professor_nome': professor.nome if professor else 'N/A',
            'ambiente_nome': ambiente.nome if ambiente else 'N/A'
        })
    
    # Gerar CSV
    horario_data = {
        'nome': horario.nome,
        'ano_letivo': horario.ano_letivo
    }
    exporter = HorarioExporter(horario_data, aulas_data)
    csv_content = exporter.to_csv_turma(turma_id)
    
    return PlainTextResponse(content=csv_content, media_type="text/csv")


@router.get("/{horario_id}/export/professor/{professor_id}/csv", response_class=PlainTextResponse)
def exportar_horario_professor_csv(horario_id: int, professor_id: int, db: Session = Depends(get_db)):
    """Exporta horário de um professor em formato CSV"""
    # Verificar se horário existe
    horario = db.query(HorarioModel).filter(HorarioModel.id == horario_id).first()
    if not horario:
        raise HTTPException(status_code=404, detail="Horário não encontrado")
    
    # Verificar se professor existe
    professor = db.query(Professor).filter(Professor.id == professor_id).first()
    if not professor:
        raise HTTPException(status_code=404, detail="Professor não encontrado")
    
    # Buscar aulas
    aulas = db.query(HorarioAula).filter(
        HorarioAula.horario_id == horario_id,
        HorarioAula.professor_id == professor_id
    ).all()
    
    # Enriquecer com dados relacionados
    aulas_data = []
    for aula in aulas:
        turma = db.query(Turma).filter(Turma.id == aula.turma_id).first()
        disciplina = db.query(Disciplina).filter(Disciplina.id == aula.disciplina_id).first()
        ambiente = db.query(Ambiente).filter(Ambiente.id == aula.ambiente_id).first()
        
        aulas_data.append({
            'turma_id': aula.turma_id,
            'professor_id': aula.professor_id,
            'disciplina_id': aula.disciplina_id,
            'dia_semana': aula.dia_semana,
            'horario_inicio': aula.horario_inicio,
            'horario_fim': aula.horario_fim,
            'ordem': aula.ordem,
            'turma_nome': turma.nome if turma else 'N/A',
            'disciplina_nome': disciplina.nome if disciplina else 'N/A',
            'professor_nome': professor.nome,
            'ambiente_nome': ambiente.nome if ambiente else 'N/A'
        })
    
    # Gerar CSV
    horario_data = {
        'nome': horario.nome,
        'ano_letivo': horario.ano_letivo
    }
    exporter = HorarioExporter(horario_data, aulas_data)
    csv_content = exporter.to_csv_professor(professor_id)
    
    return PlainTextResponse(content=csv_content, media_type="text/csv")


def gerar_horario_background(horario_id: int, request: GerarHorarioRequest):
    """
    Função executada em background para gerar o horário
    """
    # Criar nova sessão de banco de dados para a thread em background
    from app.core.database import SessionLocal
    db = SessionLocal()
    
    try:
        # Criar gerador com filtro de turno se especificado
        generator = HorarioGenerator(db, horario_id, turno=request.turno)
        
        # Gerar horário
        resultado = generator.gerar(tempo_maximo=request.tempo_maximo_geracao)
        
        # O resultado já foi salvo no banco pelo generator
        
    except Exception as e:
        # Em caso de erro, atualizar status
        horario = db.query(HorarioModel).filter(HorarioModel.id == horario_id).first()
        if horario:
            horario.status = "RASCUNHO"
            db.commit()
        print(f"Erro na geração em background: {str(e)}")
    finally:
        # Fechar sessão
        db.close()
