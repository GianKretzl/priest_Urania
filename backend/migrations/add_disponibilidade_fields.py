"""
Script de migração para adicionar turno e dia_nao_trabalha às disponibilidades
"""

import sys
import os

# Adicionar o diretório pai ao path para importar os módulos
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine, text
from app.core.config import settings

def migrate():
    """Adiciona os campos turno e dia_nao_trabalha à tabela disponibilidades"""
    
    engine = create_engine(settings.DATABASE_URL)
    
    with engine.connect() as connection:
        # Verificar se as colunas já existem
        result = connection.execute(text("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='disponibilidades' 
            AND column_name IN ('turno', 'dia_nao_trabalha')
        """))
        
        existing_columns = [row[0] for row in result]
        
        # Adicionar coluna turno se não existir
        if 'turno' not in existing_columns:
            print("Adicionando coluna 'turno'...")
            connection.execute(text("""
                ALTER TABLE disponibilidades 
                ADD COLUMN turno VARCHAR
            """))
            connection.commit()
            print("✓ Coluna 'turno' adicionada com sucesso!")
        else:
            print("✓ Coluna 'turno' já existe")
        
        # Adicionar coluna dia_nao_trabalha se não existir
        if 'dia_nao_trabalha' not in existing_columns:
            print("Adicionando coluna 'dia_nao_trabalha'...")
            connection.execute(text("""
                ALTER TABLE disponibilidades 
                ADD COLUMN dia_nao_trabalha BOOLEAN DEFAULT FALSE
            """))
            connection.commit()
            print("✓ Coluna 'dia_nao_trabalha' adicionada com sucesso!")
        else:
            print("✓ Coluna 'dia_nao_trabalha' já existe")
        
        print("\n✅ Migração concluída com sucesso!")

if __name__ == "__main__":
    migrate()
