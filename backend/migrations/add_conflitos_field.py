"""
Migration: Add tem_conflitos field to horarios table
"""
from sqlalchemy import create_engine, text
import os


def run_migration():
    """Executa a migração para adicionar campo tem_conflitos"""
    
    # Obter DATABASE_URL do ambiente
    database_url = os.getenv("DATABASE_URL", "postgresql://nocrybaby_user:nocrybaby_pass@db:5432/nocrybaby_db")
    
    engine = create_engine(database_url)
    
    with engine.connect() as conn:
        print("Iniciando migração para adicionar campo tem_conflitos...")
        
        try:
            # Adicionar coluna tem_conflitos na tabela horarios
            print("Adicionando coluna 'tem_conflitos' na tabela horarios...")
            conn.execute(text("""
                ALTER TABLE horarios 
                ADD COLUMN IF NOT EXISTS tem_conflitos BOOLEAN DEFAULT FALSE
            """))
            conn.commit()
            print("✓ Coluna 'tem_conflitos' adicionada com sucesso")
            
        except Exception as e:
            print(f"✗ Erro na migração: {e}")
            conn.rollback()
            raise


if __name__ == "__main__":
    run_migration()