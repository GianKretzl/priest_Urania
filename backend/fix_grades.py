"""
Script para ajustar grades curriculares que ultrapassam o limite de 30 aulas/semana por turma.
"""
from app.core.database import SessionLocal
from app.models.grade_curricular import GradeCurricular
from app.models.turma import Turma
from collections import defaultdict

def fix_grades():
    db = SessionLocal()
    
    try:
        # Buscar todas as grades ativas
        grades = db.query(GradeCurricular).filter(GradeCurricular.ativa == True).all()
        turmas = db.query(Turma).filter(Turma.ativa == True).all()
        
        # Agrupar aulas por turma
        aulas_por_turma = defaultdict(list)
        for grade in grades:
            aulas_por_turma[grade.turma_id].append(grade)
        
        print("=" * 60)
        print("AJUSTANDO GRADES CURRICULARES")
        print("=" * 60)
        
        modificacoes = 0
        
        for turma_id, grades_turma in aulas_por_turma.items():
            turma = next(t for t in turmas if t.id == turma_id)
            total_aulas = sum(g.aulas_por_semana for g in grades_turma)
            
            if total_aulas > 30:
                print(f"\n{turma.nome}: {total_aulas} aulas (ultrapassou o limite de 30)")
                aulas_excedentes = total_aulas - 30
                print(f"  Precisa reduzir: {aulas_excedentes} aulas")
                
                # Ordenar grades por número de aulas (maiores primeiro)
                grades_ordenadas = sorted(grades_turma, key=lambda g: g.aulas_por_semana, reverse=True)
                
                # Reduzir aulas começando pelas disciplinas com mais aulas
                reduzido = 0
                for grade in grades_ordenadas:
                    if reduzido >= aulas_excedentes:
                        break
                    
                    # Reduzir no máximo 1 aula por disciplina por iteração
                    if grade.aulas_por_semana > 1:
                        reducao = min(1, aulas_excedentes - reduzido, grade.aulas_por_semana - 1)
                        print(f"  - {grade.disciplina.nome}: {grade.aulas_por_semana} → {grade.aulas_por_semana - reducao} aulas")
                        grade.aulas_por_semana -= reducao
                        reduzido += reducao
                        modificacoes += 1
                
                # Se ainda precisa reduzir mais, fazer segunda passagem
                if reduzido < aulas_excedentes:
                    for grade in grades_ordenadas:
                        if reduzido >= aulas_excedentes:
                            break
                        if grade.aulas_por_semana > 1:
                            reducao = min(1, aulas_excedentes - reduzido, grade.aulas_por_semana - 1)
                            if reducao > 0:
                                print(f"  - {grade.disciplina.nome}: {grade.aulas_por_semana} → {grade.aulas_por_semana - reducao} aulas (2ª redução)")
                                grade.aulas_por_semana -= reducao
                                reduzido += reducao
                                modificacoes += 1
                
                novo_total = sum(g.aulas_por_semana for g in grades_turma)
                print(f"  Total após ajuste: {novo_total} aulas")
            
            else:
                print(f"\n{turma.nome}: {total_aulas} aulas ✓ (dentro do limite)")
        
        if modificacoes > 0:
            print(f"\n{'=' * 60}")
            print(f"Total de modificações: {modificacoes}")
            print("Salvando alterações no banco de dados...")
            db.commit()
            print("✓ Alterações salvas com sucesso!")
        else:
            print(f"\n{'=' * 60}")
            print("✓ Nenhuma alteração necessária - todas as turmas estão dentro do limite.")
        
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    fix_grades()
