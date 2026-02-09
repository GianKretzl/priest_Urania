"""
Migration to add tipo_aula field to horarios_aulas table
and make some fields nullable for hora_atividade entries
"""
from sqlalchemy import create_engine, text
import os

def run_migration():
    # Get database URL from environment
    database_url = os.getenv("DATABASE_URL", "postgresql://urania_user:urania_pass@db:5432/urania_db")
    engine = create_engine(database_url)
    
    with engine.connect() as conn:
        # Create enum type for tipo_aula if it doesn't exist
        conn.execute(text("""
            DO $$ BEGIN
                CREATE TYPE tipoaulaenum AS ENUM ('AULA_NORMAL', 'HORA_ATIVIDADE');
            EXCEPTION
                WHEN duplicate_object THEN null;
            END $$;
        """))
        conn.commit()
        
        # Add tipo_aula column with default value
        conn.execute(text("""
            ALTER TABLE horarios_aulas 
            ADD COLUMN IF NOT EXISTS tipo_aula tipoaulaenum DEFAULT 'AULA_NORMAL' NOT NULL;
        """))
        conn.commit()
        
        # Make turma_id, disciplina_id, and ambiente_id nullable
        conn.execute(text("""
            ALTER TABLE horarios_aulas 
            ALTER COLUMN turma_id DROP NOT NULL,
            ALTER COLUMN disciplina_id DROP NOT NULL,
            ALTER COLUMN ambiente_id DROP NOT NULL;
        """))
        conn.commit()
        
        print("Migration completed successfully!")

if __name__ == "__main__":
    run_migration()
