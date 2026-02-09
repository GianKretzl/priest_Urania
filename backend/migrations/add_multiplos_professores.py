"""
Script de migração para adicionar suporte a múltiplos professores
Adiciona:
- Campo multiplos_professores na tabela disciplinas
- Campo professor_id_2 na tabela horarios_aulas
"""

from sqlalchemy import create_engine, text
import os


def run_migration():
    """Executa a migração para adicionar suporte a múltiplos professores"""
    
    # Obter DATABASE_URL do ambiente
    database_url = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/horarios")
    
    engine = create_engine(database_url)
    
    with engine.connect() as conn:
        print("Iniciando migração para múltiplos professores...")
        
        try:
            # 1. Adicionar coluna multiplos_professores na tabela disciplinas
            print("1. Adicionando coluna 'multiplos_professores' na tabela disciplinas...")
            conn.execute(text("""
                ALTER TABLE disciplinas 
                ADD COLUMN IF NOT EXISTS multiplos_professores BOOLEAN DEFAULT FALSE
            """))
            conn.commit()
            print("   ✓ Coluna 'multiplos_professores' adicionada com sucesso")
            
            # 2. Adicionar coluna professor_id_2 na tabela grades_curriculares
            print("2. Adicionando coluna 'professor_id_2' na tabela grades_curriculares...")
            conn.execute(text("""
                ALTER TABLE grades_curriculares 
                ADD COLUMN IF NOT EXISTS professor_id_2 INTEGER REFERENCES professores(id)
            """))
            conn.commit()
            print("   ✓ Coluna 'professor_id_2' adicionada em grades_curriculares")
            
            # 3. Adicionar coluna professor_id_2 na tabela horarios_aulas
            print("3. Adicionando coluna 'professor_id_2' na tabela horarios_aulas...")
            conn.execute(text("""
                ALTER TABLE horarios_aulas 
                ADD COLUMN IF NOT EXISTS professor_id_2 INTEGER REFERENCES professores(id)
            """))
            conn.commit()
            print("   ✓ Coluna 'professor_id_2' adicionada em horarios_aulas")
            
            # 4. Marcar disciplinas de recomposição como permitindo múltiplos professores
            print("4. Configurando disciplinas de recomposição...")
            result = conn.execute(text("""
                UPDATE disciplinas 
                SET multiplos_professores = TRUE 
                WHERE LOWER(nome) LIKE '%recomp%matemática%' 
                   OR LOWER(nome) LIKE '%recomp%matematica%'
                   OR LOWER(nome) LIKE '%recomp%língua%portuguesa%'
                   OR LOWER(nome) LIKE '%recomp%lingua%portuguesa%'
                   OR LOWER(nome) LIKE '%recomposição%matemática%'
                   OR LOWER(nome) LIKE '%recomposição%matemática%'
                   OR LOWER(nome) LIKE '%recomposição%língua%'
                   OR LOWER(nome) LIKE '%recomposicao%matematica%'
                   OR LOWER(nome) LIKE '%recomposicao%lingua%'
            """))
            conn.commit()
            updated_rows = result.rowcount
            print(f"   ✓ {updated_rows} disciplina(s) de recomposição configurada(s)")
            
            print("\n✅ Migração concluída com sucesso!")
            print("\nResumo das alterações:")
            print("  • disciplinas.multiplos_professores (BOOLEAN)")
            print("  • grades_curriculares.professor_id_2 (INTEGER, nullable)")
            print("  • horarios_aulas.professor_id_2 (INTEGER, nullable)")
            
        except Exception as e:
            print(f"\n❌ Erro durante a migração: {e}")
            conn.rollback()
            raise


if __name__ == "__main__":
    run_migration()
