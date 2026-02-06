from app.core.database import SessionLocal, engine, Base
from app.models import (
    Disciplina, Turma, Professor, Sede, Ambiente, GradeCurricular, Horario
)

def limpar_dados(db):
    """Limpa todos os dados existentes"""
    db.query(GradeCurricular).delete()
    db.query(Horario).delete()
    db.query(Ambiente).delete()
    db.query(Sede).delete()
    db.query(Turma).delete()
    db.query(Professor).delete()
    db.query(Disciplina).delete()
    db.commit()

def criar_sede_ambientes(db):
    """Cria sede e ambientes"""
    sede = Sede(
        nome="Colégio Estadual Princesa Isabel",
        endereco="Rua Principal, 123",
        cidade="Curitiba",
        estado="PR",
        cep="80000-000"
    )
    db.add(sede)
    db.commit()
    db.refresh(sede)
    
    # Criar ambientes (salas)
    for i in range(1, 21):
        ambiente = Ambiente(
            nome=f"Sala {i}",
            codigo=f"S{str(i).zfill(2)}",
            tipo="SALA_AULA",
            capacidade=40,
            sede_id=sede.id
        )
        db.add(ambiente)
    db.commit()
    return sede

def criar_professores(db):
    """Cria todos os professores com suas disciplinas"""
    
    # Lista de professores com nome e máximo de aulas (será calculado)
    professores_data = [
        "Alvaro", "Aline", "Aline V", "Andreia", "Andreza", "Carolina",
        "Cristiano", "Diomar", "Edelvan", "Fernanda", "Gessinger", "Gian",
        "Giovani", "Helmut", "Lucas", "Lucia", "Márcia Regina", "Marly",
        "Matheus", "Mayhara", "Mirele", "Nadia", "Paola", "Rafaela",
        "Renata", "Rodrigo", "Rosane", "Rosani", "Sandro", "SENAI"
    ]
    
    professores = {}
    for idx, nome in enumerate(professores_data, 1):
        professor = Professor(
            nome=nome,
            email=f"{nome.lower().replace(' ', '')}@escola.com",
            telefone=f"41999{str(idx).zfill(6)}",
            cpf=f"000.000.000-{str(idx).zfill(2)}",
            carga_horaria_maxima=40,  # Será atualizado depois
            horas_atividade=8,
            max_aulas_seguidas=4,
            max_aulas_dia=8,
            tempo_deslocamento=0,
            ativo=True
        )
        db.add(professor)
        professores[nome] = professor
    
    db.commit()
    for nome in professores:
        db.refresh(professores[nome])
    
    return professores

def criar_disciplinas(db):
    """Cria todas as disciplinas únicas"""
    
    disciplinas_nomes = [
        # 9 anos
        "Arte", "Ciências", "Educação Física", "Geografia", "História",
        "Língua Inglesa", "Língua Portuguesa", "Matemática", 
        "Cidadania e Civismo", "Educação Financeira", "Programação e Robótica",
        "Rec. língua portuguesa", "Rec matemática",
        
        # 1º ano
        "Biologia", "Química", "Programação e IA", "Estratégias de MkT",
        "Finanças Empresariais", "Princípios de Administração", "Recursos Humanos",
        "Técnicas Integradas", "Informática Empresarial", "Princípios Econômicos",
        "SENAI", "Arte Paranaense", "História do Paraná", "Geografia do Paraná",
        
        # 2º ano
        "Filosofia", "Sociologia", "Literatura e Prod de texto",
        "Sociologia GOV CID Sociedade", "Filosofia Análise de Textos Filos",
        "Programação", "Robótica", "Física e Tecnologia",
        
        # 3º ano
        "Física", "Projeto de vida", "Arte II", "Geografia I", "História I",
        "Língua Inglesa I", "Sociologia I", "Biologia II", "Física II",
        "Física III", "Matemática II"
    ]
    
    # Cores diferentes para as disciplinas
    cores = [
        "#EF4444", "#F97316", "#F59E0B", "#EAB308", "#84CC16", "#22C55E",
        "#10B981", "#14B8A6", "#06B6D4", "#0EA5E9", "#3B82F6", "#6366F1",
        "#8B5CF6", "#A855F7", "#D946EF", "#EC4899", "#F43F5E", "#FB923C",
        "#FBBF24", "#A3E635", "#4ADE80", "#2DD4BF", "#22D3EE", "#38BDF8",
        "#60A5FA", "#818CF8", "#A78BFA", "#C084FC", "#E879F9", "#F472B6",
        "#FB7185", "#FCA5A5", "#FDBA74", "#FCD34D", "#BEF264", "#86EFAC",
        "#5EEAD4", "#67E8F9", "#7DD3FC", "#93C5FD", "#A5B4FC", "#C4B5FD",
        "#D8B4FE", "#F0ABFC", "#F9A8D4", "#FCA5A5"
    ]
    
    disciplinas = {}
    for idx, nome in enumerate(disciplinas_nomes):
        disciplina = Disciplina(
            nome=nome,
            carga_horaria_semanal=2,  # Padrão, será ajustado nas grades
            duracao_aula=50,
            cor=cores[idx % len(cores)],
            ativa=True
        )
        db.add(disciplina)
        disciplinas[nome] = disciplina
    
    db.commit()
    for nome in disciplinas:
        db.refresh(disciplinas[nome])
    
    return disciplinas

def criar_turmas(db):
    """Cria todas as turmas"""
    turmas_data = [
        ("9A", "9º Ano", "MATUTINO"),
        ("9B", "9º Ano", "MATUTINO"),
        ("9C", "9º Ano", "MATUTINO"),
        ("9D", "9º Ano", "MATUTINO"),
        ("1A", "1º Ano", "MATUTINO"),
        ("1B", "1º Ano - Eletromecânica", "MATUTINO"),
        ("1C", "1º Ano", "MATUTINO"),
        ("2A", "2º Ano", "MATUTINO"),
        ("2B", "2º Ano", "MATUTINO"),
        ("3A", "3º Ano", "MATUTINO"),
        ("3B", "3º Ano", "MATUTINO"),
    ]
    
    turmas = {}
    for codigo, nome, turno in turmas_data:
        turma = Turma(
            nome=codigo,
            ano_serie=nome,
            turno=turno,
            numero_alunos=30,
            ativa=True
        )
        db.add(turma)
        turmas[codigo] = turma
    
    db.commit()
    for codigo in turmas:
        db.refresh(turmas[codigo])
    
    return turmas

def criar_grades_curriculares(db, professores, disciplinas, turmas):
    """Cria as grades curriculares e atribui professores às disciplinas"""
    
    # Estrutura: turma -> [(disciplina, aulas, professor), ...]
    grades_data = {
        # 9 anos (A, B, C, D) - mesma grade
        "9A": [
            ("Arte", 2, "Andreza"),
            ("Ciências", 2, "Andreia"),
            ("Educação Física", 2, "Giovani"),
            ("Geografia", 3, "Aline"),
            ("História", 2, "Rosani"),
            ("Língua Inglesa", 2, "Rafaela"),
            ("Língua Portuguesa", 3, "Renata"),
            ("Matemática", 5, "Nadia"),
            ("Cidadania e Civismo", 1, "Fernanda"),
            ("Educação Financeira", 2, "Diomar"),
            ("Programação e Robótica", 2, "Gian"),
            ("Rec. língua portuguesa", 2, "Márcia Regina"),
            ("Rec matemática", 2, "Mayhara"),
            ("Rec matemática", 2, "Alvaro"),  # 2 professores mesmo horário
        ],
        "1A": [
            ("Arte", 2, "Andreza"),
            ("Biologia", 2, "Carolina"),
            ("Educação Física", 2, "Rodrigo"),
            ("Geografia", 2, "Edelvan"),
            ("Língua Inglesa", 1, "Rafaela"),
            ("Língua Portuguesa", 1, "Márcia Regina"),
            ("Matemática", 3, "Sandro"),
            ("Cidadania e Civismo", 1, "Cristiano"),
            ("Programação e IA", 1, "Lucas"),
            ("Química", 2, "Aline V"),
            ("Estratégias de MkT", 2, "Lucas"),
            ("Finanças Empresariais", 2, "Lucas"),
            ("Princípios de Administração", 2, "Lucia"),
            ("Recursos Humanos", 2, "Lucia"),
            ("Técnicas Integradas", 1, "Matheus"),
            ("Informática Empresarial", 2, "Lucia"),
            ("Princípios Econômicos", 1, "Matheus"),
        ],
        "1B": [
            ("Arte", 2, "Andreza"),
            ("Biologia", 2, "Carolina"),
            ("Educação Física", 2, "Rodrigo"),
            ("Geografia", 2, "Edelvan"),
            ("Língua Inglesa", 1, "Rafaela"),
            ("Língua Portuguesa", 2, "Márcia Regina"),
            ("Matemática", 3, "Sandro"),
            ("Cidadania e Civismo", 1, "Cristiano"),
            ("Programação e IA", 1, "Matheus"),
            ("Química", 2, "Aline V"),
            ("SENAI", 12, "SENAI"),
        ],
        "1C": [
            ("Arte", 2, "Andreza"),
            ("Biologia", 2, "Carolina"),
            ("Educação Física", 2, "Rodrigo"),
            ("Geografia", 2, "Edelvan"),
            ("Língua Inglesa", 2, "Rafaela"),
            ("Língua Portuguesa", 4, "Márcia Regina"),
            ("Matemática", 4, "Sandro"),
            ("Cidadania e Civismo", 1, "Cristiano"),
            ("Programação e IA", 2, "Matheus"),
            ("Química", 2, "Aline V"),
            ("Educação Financeira", 2, "Diomar"),
            ("Arte Paranaense", 1, "Marly"),
            ("História do Paraná", 2, "Rosane"),
            ("Geografia do Paraná", 2, "Edelvan"),
        ],
        "2A": [
            ("Arte", 2, "Andreza"),
            ("Educação Física", 2, "Rodrigo"),
            ("Língua Inglesa", 2, "Rafaela"),
            ("Língua Portuguesa", 4, "Renata"),
            ("Matemática", 4, "Sandro"),
            ("Filosofia", 2, "Cristiano"),
            ("Educação Financeira", 2, "Mayhara"),
            ("Cidadania e Civismo", 1, "Fernanda"),
            ("Sociologia", 2, "Cristiano"),
            ("Literatura e Prod de texto", 2, "Fernanda"),
            ("Sociologia GOV CID Sociedade", 1, "Edelvan"),
            ("Filosofia Análise de Textos Filos", 2, "Cristiano"),
        ],
        "2B": [
            ("Arte", 2, "Andreza"),
            ("Educação Física", 2, "Rodrigo"),
            ("Língua Inglesa", 2, "Rafaela"),
            ("Língua Portuguesa", 4, "Renata"),
            ("Matemática", 4, "Sandro"),
            ("Filosofia", 2, "Cristiano"),
            ("Educação Financeira", 2, "Mayhara"),
            ("Cidadania e Civismo", 1, "Fernanda"),
            ("Sociologia", 2, "Cristiano"),
            ("Programação", 2, "Gian"),
            ("Robótica", 2, "Gian"),
            ("Física e Tecnologia", 1, "Alvaro"),
        ],
        "3A": [
            ("Educação Física", 2, "Giovani"),
            ("Física", 2, "Alvaro"),
            ("Língua Portuguesa", 4, "Mirele"),
            ("Matemática", 4, "Paola"),
            ("Cidadania e Civismo", 1, "Edelvan"),
            ("Educação Financeira", 2, "Mayhara"),
            ("Projeto de vida", 1, "Edelvan"),
            ("Rec. língua portuguesa", 2, "Mirele"),
            ("Rec matemática", 2, "Mayhara"),
            ("Arte II", 2, "Marly"),
            ("Geografia I", 2, "Edelvan"),
            ("História I", 2, "Rosane"),
            ("Língua Inglesa I", 2, "Gessinger"),
            ("Sociologia I", 2, "Cristiano"),
        ],
        "3B": [
            ("Educação Física", 2, "Giovani"),
            ("Física", 2, "Alvaro"),
            ("Língua Portuguesa", 4, "Mirele"),
            ("Matemática", 4, "Paola"),
            ("Cidadania e Civismo", 1, "Edelvan"),
            ("Educação Financeira", 2, "Paola"),
            ("Projeto de vida", 1, "Edelvan"),
            ("Rec. língua portuguesa", 2, "Mirele"),
            ("Rec matemática", 2, "Mayhara"),
            ("Biologia II", 2, "Carolina"),
            ("Física II", 2, "Alvaro"),
            ("Física III", 2, "Alvaro"),
            ("Matemática II", 2, "Helmut"),
            ("Química", 2, "Aline V"),
        ],
    }
    
    # Replicar 9A para 9B, 9C, 9D
    for turma_codigo in ["9B", "9C", "9D"]:
        grades_data[turma_codigo] = grades_data["9A"]
    
    # Calcular carga horária de cada professor
    carga_professores = {}
    for turma_codigo, materias in grades_data.items():
        for disciplina_nome, aulas, professor_nome in materias:
            if professor_nome not in carga_professores:
                carga_professores[professor_nome] = 0
            carga_professores[professor_nome] += aulas
    
    # Atualizar carga horária dos professores
    for professor_nome, total_aulas in carga_professores.items():
        professores[professor_nome].carga_horaria_maxima = total_aulas
    db.commit()
    
    # Atribuir disciplinas aos professores (relação muitos-para-muitos)
    for turma_codigo, materias in grades_data.items():
        for disciplina_nome, aulas, professor_nome in materias:
            prof = professores[professor_nome]
            disc = disciplinas[disciplina_nome]
            
            # Adicionar disciplina ao professor se ainda não está
            if disc not in prof.disciplinas:
                prof.disciplinas.append(disc)
    db.commit()
    
    # Criar grades curriculares
    for turma_codigo, materias in grades_data.items():
        turma = turmas[turma_codigo]
        for disciplina_nome, aulas, professor_nome in materias:
            grade = GradeCurricular(
                turma_id=turma.id,
                disciplina_id=disciplinas[disciplina_nome].id,
                professor_id=professores[professor_nome].id,
                aulas_por_semana=aulas
            )
            db.add(grade)
    
    db.commit()

def criar_horario_exemplo(db):
    """Cria um horário exemplo"""
    horario = Horario(
        nome="Horário 2026",
        ano_letivo=2026,
        semestre=1,
        status="RASCUNHO"
    )
    db.add(horario)
    db.commit()
    db.refresh(horario)
    return horario

def main():
    print("=" * 60)
    print("🎓 SEED DATA - Sistema de Horários Escolares")
    print("=" * 60)
    
    # Criar tabelas
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        print("🗑️  Limpando dados existentes...")
        limpar_dados(db)
        print("✅ Dados limpos!")
        
        print("\n🏫 Criando sede e ambientes...")
        sede = criar_sede_ambientes(db)
        print(f"✅ Criada 1 sede com 20 ambientes!")
        
        print("\n👨‍🏫 Criando professores...")
        professores = criar_professores(db)
        print(f"✅ Criados {len(professores)} professores!")
        
        print("\n📚 Criando disciplinas...")
        disciplinas = criar_disciplinas(db)
        print(f"✅ Criadas {len(disciplinas)} disciplinas!")
        
        print("\n🎓 Criando turmas...")
        turmas = criar_turmas(db)
        print(f"✅ Criadas {len(turmas)} turmas!")
        
        print("\n📋 Criando grades curriculares e atribuindo professores...")
        criar_grades_curriculares(db, professores, disciplinas, turmas)
        total_grades = db.query(GradeCurricular).count()
        print(f"✅ Criadas {total_grades} grades curriculares!")
        
        print("\n🕐 Criando horário de exemplo...")
        horario = criar_horario_exemplo(db)
        print(f"✅ Criado horário ID {horario.id}!")
        
        print("\n" + "=" * 60)
        print("✅ SEED CONCLUÍDO COM SUCESSO!")
        print("=" * 60)
        print("\n📊 Resumo:")
        print(f"   • 1 Sede")
        print(f"   • 20 Ambientes")
        print(f"   • {len(professores)} Professores")
        print(f"   • {len(disciplinas)} Disciplinas")
        print(f"   • {len(turmas)} Turmas")
        print(f"   • {total_grades} Grades Curriculares")
        print(f"   • 1 Horário (ID: {horario.id})")
        print(f"\n🚀 Sistema pronto para gerar horários!")
        print(f"   Execute: POST /api/v1/horarios/{horario.id}/gerar")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    main()
