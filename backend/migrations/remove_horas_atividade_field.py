"""
Script de migração para remover a coluna horas_atividade da tabela professores
Agora esse campo é calculado automaticamente seguindo a regra 15/5
"""

import sys
import os

# Adicionar o diretório pai ao path para importar os módulos
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine, text
from app.core.config import settings

def migrate():
    """Remove a coluna horas_atividade da tabela professores"""
    
    engine = create_engine(settings.DATABASE_URL)
    
    with engine.connect() as connection:
        print("🔍 Verificando se a coluna 'horas_atividade' existe...")
        
        # Verificar se a coluna existe
        result = connection.execute(text("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='professores' 
            AND column_name='horas_atividade'
        """))
        
        column_exists = len(list(result)) > 0
        
        if column_exists:
            print("📝 A coluna 'horas_atividade' será removida.")
            print("⚠️  Agora as horas-atividade são calculadas automaticamente seguindo a regra 15/5:")
            print("   Para cada 4 horas de jornada: 3h de regência + 1h de atividade")
            print("   Exemplos: 20h → 15h regência + 5h atividade | 40h → 30h regência + 10h atividade")
            print()
            
            # Remover a coluna
            print("🗑️  Removendo coluna 'horas_atividade'...")
            connection.execute(text("""
                ALTER TABLE professores 
                DROP COLUMN horas_atividade
            """))
            connection.commit()
            print("✓ Coluna 'horas_atividade' removida com sucesso!")
        else:
            print("✓ Coluna 'horas_atividade' já foi removida anteriormente")
        
        print("\n✅ Migração concluída com sucesso!")
        print("\n📊 A partir de agora:")
        print("   - horas_atividade = carga_horaria_maxima / 4")
        print("   - horas_regencia = carga_horaria_maxima - horas_atividade")

if __name__ == "__main__":
    migrate()
