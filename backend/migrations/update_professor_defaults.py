"""
Script de migração para ajustar valores padrão e remover tempo_deslocamento
"""

import sys
import os

# Adicionar o diretório pai ao path para importar os módulos
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine, text
from app.core.config import settings

def migrate():
    """Atualiza valores padrão e remove coluna tempo_deslocamento"""
    
    engine = create_engine(settings.DATABASE_URL)
    
    with engine.connect() as connection:
        print("🔍 Verificando estrutura atual da tabela professores...")
        
        # Verificar se a coluna tempo_deslocamento existe
        result = connection.execute(text("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='professores' 
            AND column_name='tempo_deslocamento'
        """))
        
        column_exists = len(list(result)) > 0
        
        # 1. Atualizar max_aulas_seguidas para 3 (padrão, mas não é regra rígida)
        print("\n📝 Atualizando max_aulas_seguidas para 3 (padrão)...")
        connection.execute(text("""
            UPDATE professores 
            SET max_aulas_seguidas = 3 
            WHERE max_aulas_seguidas != 3
        """))
        connection.commit()
        print("✓ max_aulas_seguidas atualizado!")
        
        # 2. Atualizar max_aulas_dia para 12 (máximo 6 por período)
        print("\n📝 Atualizando max_aulas_dia para 12 (6 por período)...")
        connection.execute(text("""
            UPDATE professores 
            SET max_aulas_dia = 12 
            WHERE max_aulas_dia != 12
        """))
        connection.commit()
        print("✓ max_aulas_dia atualizado!")
        
        # 3. Remover coluna tempo_deslocamento se existir
        if column_exists:
            print("\n🗑️  Removendo coluna 'tempo_deslocamento'...")
            connection.execute(text("""
                ALTER TABLE professores 
                DROP COLUMN tempo_deslocamento
            """))
            connection.commit()
            print("✓ Coluna 'tempo_deslocamento' removida!")
        else:
            print("\n✓ Coluna 'tempo_deslocamento' já foi removida anteriormente")
        
        print("\n✅ Migração concluída com sucesso!")
        print("\n📊 Novos valores padrão:")
        print("   - max_aulas_seguidas: 3 (padrão, mas flexível)")
        print("   - max_aulas_dia: 12 (6 aulas por período)")
        print("   - tempo_deslocamento: REMOVIDO")

if __name__ == "__main__":
    migrate()
