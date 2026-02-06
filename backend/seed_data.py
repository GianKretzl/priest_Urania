"""
Script para popular o banco de dados com dados reais da escola
Execute: python seed_data.py
"""

from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine, Base
from app.models.disciplina import Disciplina
from app.models.turma import Turma, TurnoEnum
from app.models.professor import Professor
from app.models.grade_curricular import GradeCurricular
from app.models.sede import Sede
from app.models.ambiente import Ambiente, TipoAmbienteEnum
from app.models.horario import Horario

# Criar todas as tabelas
Base.metadata.create_all(bind=engine)

def limpar_dados(db: Session):
    """Limpa todos os dados existentes"""
    print("🗑️  Limpando dados existentes...")
    db.query(GradeCurricular).delete()
    db.query(Horario).delete()
    db.query(Ambiente).delete()
    db.query(Sede).delete()
    db.query(Turma).delete()
    db.query(Disciplina).delete()
    db.query(Professor).delete()
    db.commit()
    print("✅ Dados limpos!")

def criar_sede_e_ambientes(db: Session):
    """Cria a sede e ambientes (salas de aula)"""
    print("\n🏫 Criando sede e ambientes...")
    
    sede = Sede(
        nome="Sede Principal",
        endereco="Rua Principal, 123",
        cidade="Curitiba",
        estado="PR",
        cep="80000-000",
        ativa=True
    )
    db.add(sede)
    db.commit()
    db.refresh(sede)
    
    # Criar 15 salas de aula
    for i in range(1, 16):
        ambiente = Ambiente(
            nome=f"Sala {i}",
            codigo=f"S{i:02d}",
            tipo=TipoAmbienteEnum.SALA_AULA,
            capacidade=35,
            sede_id=sede.id,
            ativo=True
        )
        db.add(ambiente)
    
    # Criar ambientes especiais
    ambientes_especiais = [
        ("Laboratório de Informática", "LAB-INF", TipoAmbienteEnum.SALA_INFORMATICA),
        ("Laboratório de Química", "LAB-QUI", TipoAmbienteEnum.LABORATORIO),
        ("Laboratório de Física", "LAB-FIS", TipoAmbienteEnum.LABORATORIO),
        ("Quadra Poliesportiva", "QUADRA", TipoAmbienteEnum.QUADRA),
        ("Auditório", "AUD", TipoAmbienteEnum.AUDITORIO),
    ]
    
    for nome, codigo, tipo in ambientes_especiais:
        ambiente = Ambiente(
            nome=nome,
            codigo=codigo,
            tipo=tipo,
            capacidade=40,
            sede_id=sede.id,
            ativo=True
        )
        db.add(ambiente)
    
    db.commit()
    print(f"✅ Criada 1 sede com {15 + len(ambientes_especiais)} ambientes!")
    return sede

def criar_professores(db: Session):
    """Cria os professores"""
    print("\n👨‍🏫 Criando professores...")
    
    professores_data = [
        ("Alvaro", "alvaro@escola.com", "41999000001"),
        ("Aline", "aline@escola.com", "41999000002"),
        ("Aline V", "alinev@escola.com", "41999000003"),
        ("Andreia", "andreia@escola.com", "41999000004"),
        ("Andreza", "andreza@escola.com", "41999000005"),
        ("Carolina", "carolina@escola.com", "41999000006"),
        ("Cristiano", "cristiano@escola.com", "41999000007"),
        ("Diomar", "diomar@escola.com", "41999000008"),
        ("Edelvan", "edelvan@escola.com", "41999000009"),
        ("Fernanda", "fernanda@escola.com", "41999000010"),
        ("Gessinger", "gessinger@escola.com", "41999000011"),
        ("Gian", "gian@escola.com", "41999000012"),
        ("Giovani", "giovani@escola.com", "41999000013"),
        ("Helmut", "helmut@escola.com", "41999000014"),
        ("Lucas", "lucas@escola.com", "41999000015"),
        ("Lucia", "lucia@escola.com", "41999000016"),
        ("Márcia Regina", "marciaregina@escola.com", "41999000017"),
        ("Marly", "marly@escola.com", "41999000018"),
        ("Matheus", "matheus@escola.com", "41999000019"),
        ("Mayhara", "mayhara@escola.com", "41999000020"),
        ("Mirele", "mirele@escola.com", "41999000021"),
        ("Nadia", "nadia@escola.com", "41999000022"),
        ("Paola", "paola@escola.com", "41999000023"),
        ("Rafaela", "rafaela@escola.com", "41999000024"),
        ("Renata", "renata@escola.com", "41999000025"),
        ("Rodrigo", "rodrigo@escola.com", "41999000026"),
        ("Rosane", "rosane@escola.com", "41999000027"),
        ("Rosani", "rosani@escola.com", "41999000028"),
        ("Sandro", "sandro@escola.com", "41999000029"),
        ("SENAI", "senai@escola.com", "41999000030"),
    ]
    
    professores = {}
    for nome, email, telefone in professores_data:
        cpf = f"000.000.000-{len(professores)+1:02d}"
        professor = Professor(
            nome=nome,
            email=email,
            telefone=telefone,
            cpf=cpf,
            carga_horaria_maxima=40,
            horas_atividade=8,
            max_aulas_seguidas=4,
            max_aulas_dia=8,
            tempo_deslocamento=0,
            ativo=True
        )
        db.add(professor)
        professores[nome] = professor
    
    db.commit()
    
    # Refresh para obter IDs
    for prof in professores.values():
        db.refresh(prof)
    
    print(f"✅ Criados {len(professores)} professores!")
    return professores

def criar_disciplinas(db: Session):
    """Cria as disciplinas"""
    print("\n📚 Criando disciplinas...")
    
    disciplinas_nomes = set([
        "Arte", "Arte II", "Arte Paranaense",
        "Biologia", "Biologia II",
        "Ciências",
        "Cidadania e Civismo",
        "Educação Financeira",
        "Educação Física",
        "Estratégias de MkT",
        "Finanças Empresariais",
        "Filosofia", "Filosofia Análise de Textos Filos",
        "Física", "Física II", "Física III", "Física e Tecnologia",
        "Geografia", "Geografia I", "Geografia do Paraná",
        "História", "História I", "História do Paraná",
        "Informática Empresarial",
        "Língua Inglesa", "Língua Inglesa I",
        "Língua Portuguesa",
        "Literatura e Prod de texto",
        "Matemática", "Matemática II",
        "Princípios de Administração",
        "Princípios Econômicos",
        "Programação", "Programação e Robótica", "Programação e IA",
        "Projeto de vida",
        "Química",
        "Rec língua portuguesa",
        "Rec matemática",
        "Recursos Humanos",
        "Robótica",
        "SENAI",
        "Sociologia", "Sociologia I", "Sociologia GOV CID Sociedade",
        "Técnicas Integradas",
    ])
    
    disciplinas = {}
    contador_codigo = 1
    for nome in sorted(disciplinas_nomes):
        # Gerar código único usando hash ou contador
        codigo_base = nome[:15].upper().replace(" ", "_").replace("ÃO", "AO").replace("Á", "A").replace("Ô", "O")
        codigo = f"{codigo_base}_{contador_codigo}"
        
        disciplina = Disciplina(
            nome=nome,
            codigo=codigo,
            carga_horaria_semanal=2,  # Valor padrão, será sobrescrito pelas grades
            cor="#" + format(hash(nome) % 0xFFFFFF, '06x'),
            ativa=True
        )
        db.add(disciplina)
        disciplinas[nome] = disciplina
        contador_codigo += 1
    
    db.commit()
    
    # Refresh para obter IDs
    for disc in disciplinas.values():
        db.refresh(disc)
    
    print(f"✅ Criadas {len(disciplinas)} disciplinas!")
    return disciplinas

def criar_turmas(db: Session):
    """Cria as turmas"""
    print("\n🎓 Criando turmas...")
    
    turmas_data = [
        ("9º Ano A", "9A", "9º Ano", "MATUTINO"),
        ("9º Ano B", "9B", "9º Ano", "MATUTINO"),
        ("9º Ano C", "9C", "9º Ano", "MATUTINO"),
        ("9º Ano D", "9D", "9º Ano", "MATUTINO"),
        ("1º Ano A - Administração", "1A", "1º Ano", "MATUTINO"),
        ("1º Ano B - Eletromecânica", "1B", "1º Ano", "MATUTINO"),
        ("1º Ano C - Normal", "1C", "1º Ano", "MATUTINO"),
        ("2º Ano A", "2A", "2º Ano", "MATUTINO"),
        ("2º Ano B", "2B", "2º Ano", "MATUTINO"),
        ("3º Ano A", "3A", "3º Ano", "MATUTINO"),
        ("3º Ano B", "3B", "3º Ano", "MATUTINO"),
    ]
    
    turmas = {}
    for nome, codigo, ano_serie, turno in turmas_data:
        turma = Turma(
            nome=nome,
            ano_serie=ano_serie,
            turno=TurnoEnum[turno],
            numero_alunos=35,
            ativa=True
        )
        db.add(turma)
        turmas[codigo] = turma
    
    db.commit()
    
    # Refresh para obter IDs
    for turma in turmas.values():
        db.refresh(turma)
    
    print(f"✅ Criadas {len(turmas)} turmas!")
    return turmas

def criar_grades_curriculares(db: Session, turmas: dict, disciplinas: dict, professores: dict):
    """Cria as grades curriculares (turma + disciplina + professor + aulas)"""
    print("\n📋 Criando grades curriculares...")
    
    # Dados estruturados por turma
    grades_data = {
        "9A": [
            ("Arte", "Andreza", 2),
            ("Ciências", "Andreia", 2),
            ("Educação Física", "Giovani", 2),
            ("Geografia", "Aline", 3),
            ("História", "Rosani", 2),
            ("Língua Inglesa", "Rafaela", 2),
            ("Língua Portuguesa", "Renata", 3),
            ("Matemática", "Nadia", 5),
            ("Cidadania e Civismo", "Fernanda", 1),
            ("Educação Financeira", "Diomar", 2),
            ("Programação e Robótica", "Gian", 2),
            ("Rec língua portuguesa", "Márcia Regina", 2),
            ("Rec matemática", "Mayhara", 2),
        ],
        "9B": [
            ("Arte", "Andreza", 2),
            ("Ciências", "Andreia", 2),
            ("Educação Física", "Giovani", 2),
            ("Geografia", "Aline", 3),
            ("História", "Rosani", 2),
            ("Língua Inglesa", "Rafaela", 2),
            ("Língua Portuguesa", "Renata", 3),
            ("Matemática", "Nadia", 5),
            ("Cidadania e Civismo", "Fernanda", 1),
            ("Educação Financeira", "Diomar", 2),
            ("Programação e Robótica", "Gian", 2),
            ("Rec língua portuguesa", "Márcia Regina", 2),
            ("Rec matemática", "Mayhara", 2),
        ],
        "9C": [
            ("Arte", "Andreza", 2),
            ("Ciências", "Andreia", 2),
            ("Educação Física", "Giovani", 2),
            ("Geografia", "Aline", 3),
            ("História", "Rosani", 2),
            ("Língua Inglesa", "Rafaela", 2),
            ("Língua Portuguesa", "Renata", 3),
            ("Matemática", "Nadia", 5),
            ("Cidadania e Civismo", "Fernanda", 1),
            ("Educação Financeira", "Diomar", 2),
            ("Programação e Robótica", "Gian", 2),
            ("Rec língua portuguesa", "Márcia Regina", 2),
            ("Rec matemática", "Mayhara", 2),
        ],
        "9D": [
            ("Arte", "Andreza", 2),
            ("Ciências", "Andreia", 2),
            ("Educação Física", "Giovani", 2),
            ("Geografia", "Aline", 3),
            ("História", "Rosani", 2),
            ("Língua Inglesa", "Rafaela", 2),
            ("Língua Portuguesa", "Renata", 3),
            ("Matemática", "Nadia", 5),
            ("Cidadania e Civismo", "Fernanda", 1),
            ("Educação Financeira", "Diomar", 2),
            ("Programação e Robótica", "Gian", 2),
            ("Rec língua portuguesa", "Márcia Regina", 2),
            ("Rec matemática", "Mayhara", 2),
        ],
        "1A": [
            ("Arte", "Andreza", 2),
            ("Biologia", "Carolina", 2),
            ("Educação Física", "Rodrigo", 2),
            ("Geografia", "Edelvan", 2),
            ("Língua Inglesa", "Rafaela", 1),
            ("Língua Portuguesa", "Márcia Regina", 1),
            ("Matemática", "Sandro", 3),
            ("Cidadania e Civismo", "Cristiano", 1),
            ("Programação e IA", "Lucas", 1),
            ("Química", "Aline V", 2),
            ("Estratégias de MkT", "Lucas", 2),
            ("Finanças Empresariais", "Lucas", 2),
            ("Princípios de Administração", "Lucia", 2),
            ("Recursos Humanos", "Lucia", 2),
            ("Técnicas Integradas", "Matheus", 1),
            ("Informática Empresarial", "Lucia", 2),
            ("Princípios Econômicos", "Matheus", 1),
        ],
        "1B": [
            ("Arte", "Andreza", 2),
            ("Biologia", "Carolina", 2),
            ("Educação Física", "Rodrigo", 2),
            ("Geografia", "Edelvan", 2),
            ("Língua Inglesa", "Rafaela", 1),
            ("Língua Portuguesa", "Márcia Regina", 2),
            ("Matemática", "Sandro", 3),
            ("Cidadania e Civismo", "Cristiano", 1),
            ("Programação e IA", "Matheus", 1),
            ("Química", "Aline V", 2),
            ("SENAI", "SENAI", 12),
        ],
        "1C": [
            ("Arte", "Andreza", 2),
            ("Biologia", "Carolina", 2),
            ("Educação Física", "Rodrigo", 2),
            ("Geografia", "Edelvan", 2),
            ("Língua Inglesa", "Rafaela", 2),
            ("Língua Portuguesa", "Márcia Regina", 4),
            ("Matemática", "Sandro", 4),
            ("Cidadania e Civismo", "Cristiano", 1),
            ("Programação e IA", "Matheus", 2),
            ("Química", "Aline V", 2),
            ("Educação Financeira", "Diomar", 2),
            ("Arte Paranaense", "Marly", 1),
            ("História do Paraná", "Rosane", 2),
            ("Geografia do Paraná", "Edelvan", 2),
        ],
        "2A": [
            ("Arte", "Andreza", 2),
            ("Educação Física", "Rodrigo", 2),
            ("Língua Inglesa", "Rafaela", 2),
            ("Língua Portuguesa", "Renata", 4),
            ("Matemática", "Sandro", 4),
            ("Filosofia", "Cristiano", 2),
            ("Educação Financeira", "Mayhara", 2),
            ("Cidadania e Civismo", "Fernanda", 1),
            ("Sociologia", "Cristiano", 2),
            ("Literatura e Prod de texto", "Fernanda", 2),
            ("Sociologia GOV CID Sociedade", "Edelvan", 1),
            ("Filosofia Análise de Textos Filos", "Cristiano", 2),
        ],
        "2B": [
            ("Arte", "Andreza", 2),
            ("Educação Física", "Rodrigo", 2),
            ("Língua Inglesa", "Rafaela", 2),
            ("Língua Portuguesa", "Renata", 4),
            ("Matemática", "Sandro", 4),
            ("Filosofia", "Cristiano", 2),
            ("Educação Financeira", "Mayhara", 2),
            ("Cidadania e Civismo", "Fernanda", 1),
            ("Sociologia", "Cristiano", 2),
            ("Programação", "Gian", 2),
            ("Robótica", "Gian", 2),
            ("Física e Tecnologia", "Alvaro", 1),
        ],
        "3A": [
            ("Educação Física", "Giovani", 2),
            ("Física", "Alvaro", 2),
            ("Língua Portuguesa", "Mirele", 4),
            ("Matemática", "Paola", 4),
            ("Cidadania e Civismo", "Edelvan", 1),
            ("Educação Financeira", "Mayhara", 2),
            ("Projeto de vida", "Edelvan", 1),
            ("Rec língua portuguesa", "Mirele", 2),
            ("Rec matemática", "Mayhara", 2),
            ("Arte II", "Marly", 2),
            ("Geografia I", "Edelvan", 2),
            ("História I", "Rosane", 2),
            ("Língua Inglesa I", "Gessinger", 2),
            ("Sociologia I", "Cristiano", 2),
        ],
        "3B": [
            ("Educação Física", "Giovani", 2),
            ("Física", "Alvaro", 2),
            ("Língua Portuguesa", "Mirele", 4),
            ("Matemática", "Paola", 4),
            ("Cidadania e Civismo", "Edelvan", 1),
            ("Educação Financeira", "Paola", 2),
            ("Projeto de vida", "Edelvan", 1),
            ("Rec língua portuguesa", "Mirele", 2),
            ("Rec matemática", "Mayhara", 2),
            ("Biologia II", "Carolina", 2),
            ("Física II", "Alvaro", 2),
            ("Física III", "Alvaro", 2),
            ("Matemática II", "Helmut", 2),
            ("Química", "Aline V", 2),
        ],
    }
    
    contador = 0
    for turma_codigo, grades in grades_data.items():
        turma = turmas[turma_codigo]
        
        for disciplina_nome, professor_nome, aulas in grades:
            disciplina = disciplinas.get(disciplina_nome)
            professor = professores.get(professor_nome)
            
            if not disciplina:
                print(f"⚠️  Disciplina '{disciplina_nome}' não encontrada!")
                continue
            
            if not professor:
                print(f"⚠️  Professor '{professor_nome}' não encontrado!")
                continue
            
            grade = GradeCurricular(
                turma_id=turma.id,
                disciplina_id=disciplina.id,
                professor_id=professor.id,
                aulas_por_semana=aulas,
                ativa=True
            )
            db.add(grade)
            contador += 1
    
    db.commit()
    print(f"✅ Criadas {contador} grades curriculares!")

def criar_horario_exemplo(db: Session):
    """Cria um horário de exemplo para teste"""
    print("\n🕐 Criando horário de exemplo...")
    
    horario = Horario(
        nome="Horário 2025 - 1º Semestre",
        ano_letivo=2025,
        semestre=1,
        status="RASCUNHO",
        total_aulas=0,
        aulas_alocadas=0,
        qualidade_score=0
    )
    db.add(horario)
    db.commit()
    db.refresh(horario)
    
    print(f"✅ Criado horário ID {horario.id}!")
    return horario

def main():
    """Função principal"""
    print("=" * 60)
    print("🎓 SEED DATA - Sistema de Horários Escolares")
    print("=" * 60)
    
    db = SessionLocal()
    
    try:
        # 1. Limpar dados existentes
        limpar_dados(db)
        
        # 2. Criar sede e ambientes
        sede = criar_sede_e_ambientes(db)
        
        # 3. Criar professores
        professores = criar_professores(db)
        
        # 4. Criar disciplinas
        disciplinas = criar_disciplinas(db)
        
        # 5. Criar turmas
        turmas = criar_turmas(db)
        
        # 6. Criar grades curriculares
        criar_grades_curriculares(db, turmas, disciplinas, professores)
        
        # 7. Criar horário de exemplo
        horario = criar_horario_exemplo(db)
        
        print("\n" + "=" * 60)
        print("✅ SEED CONCLUÍDO COM SUCESSO!")
        print("=" * 60)
        print(f"\n📊 Resumo:")
        print(f"   • 1 Sede")
        print(f"   • {db.query(Ambiente).count()} Ambientes")
        print(f"   • {len(professores)} Professores")
        print(f"   • {len(disciplinas)} Disciplinas")
        print(f"   • {len(turmas)} Turmas")
        print(f"   • {db.query(GradeCurricular).count()} Grades Curriculares")
        print(f"   • 1 Horário (ID: {horario.id})")
        print("\n🚀 Sistema pronto para gerar horários!")
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
