#!/usr/bin/env python3
"""Script para ajustar grades curriculares das turmas 2A, 2B, 3A e 3B"""
import requests
import json

API_URL = "http://localhost:3000/api/proxy"

# Mapeamento de IDs
TURMAS = {
    "2A": 52,
    "2B": 53,
    "3A": 54,
    "3B": 55
}

PROFESSORES = {
    "Andreza": 125,
    "Rodrigo": 146,
    "Rafaela": 144,
    "Renata": 145,
    "Sandro": 149,
    "Cristiano": 127,
    "Mayhara": 140,
    "Fernanda": 130,
    "Edelvan": 129,
    "Gian": 132,
    "Alvaro": 121,
    "Álvaro": 121,
    "Giovani": 133,
    "Mirele": 141,
    "Paola": 143,
    "Marly": 138,
    "Rosane": 147,
    "Gessinger": 131,
    "Carolina": 126,
    "Helmut": 134,
    "Aline V": 123
}

DISCIPLINAS = {
    "Arte": 185,
    "Educação Física": 187,
    "Língua Inglesa": 190,
    "Língua Portuguesa": 191,
    "Matemática": 192,
    "Filosofia": 212,
    "Educação Financeira": 194,
    "Cidadania e Civismo": 193,
    "Sociologia": 213,
    "Literatura e Prod de texto": 214,
    "Sociologia GOV CID Sociedade": 215,
    "Filosofia Análise de Textos Filos": 216,
    "Programação": 217,
    "Robótica": 218,
    "Física e Tecnologia": 219,
    "Física": 220,
    "Projeto de vida": 221,
    "Rec língua portuguesa": 196,
    "Rec matemática": 197,
    "Arte II": 222,
    "Geografia I": 223,
    "História I": 224,
    "Língua Inglesa I": 225,
    "Sociologia I": 226,
    "Biologia II": 227,
    "Física II": 228,
    "Física III": 229,
    "Matemática II": 230,
    "Química": 199
}

# Definição das grades
GRADES = {
    "2A": [
        (2, "Arte", "Andreza"),
        (2, "Educação Física", "Rodrigo"),
        (2, "Língua Inglesa", "Rafaela"),
        (4, "Língua Portuguesa", "Renata"),
        (4, "Matemática", "Sandro"),
        (2, "Filosofia", "Cristiano"),
        (2, "Educação Financeira", "Mayhara"),
        (1, "Cidadania e Civismo", "Fernanda"),
        (2, "Sociologia", "Cristiano"),
        (2, "Literatura e Prod de texto", "Fernanda"),
        (1, "Sociologia GOV CID Sociedade", "Edelvan"),
        (2, "Filosofia Análise de Textos Filos", "Cristiano"),
    ],
    "2B": [
        (2, "Arte", "Andreza"),
        (2, "Educação Física", "Rodrigo"),
        (2, "Língua Inglesa", "Rafaela"),
        (4, "Língua Portuguesa", "Renata"),
        (4, "Matemática", "Sandro"),
        (2, "Filosofia", "Cristiano"),
        (2, "Educação Financeira", "Mayhara"),
        (1, "Cidadania e Civismo", "Fernanda"),
        (2, "Sociologia", "Cristiano"),
        (2, "Programação", "Gian"),
        (2, "Robótica", "Gian"),
        (1, "Física e Tecnologia", "Álvaro"),
    ],
    "3A": [
        (2, "Educação Física", "Giovani"),
        (2, "Física", "Alvaro"),
        (4, "Língua Portuguesa", "Mirele"),
        (4, "Matemática", "Paola"),
        (1, "Cidadania e Civismo", "Edelvan"),
        (2, "Educação Financeira", "Mayhara"),
        (1, "Projeto de vida", "Edelvan"),
        (2, "Rec língua portuguesa", "Mirele"),
        (2, "Rec matemática", "Mayhara"),
        (2, "Arte II", "Marly"),
        (2, "Geografia I", "Edelvan"),
        (2, "História I", "Rosane"),
        (2, "Língua Inglesa I", "Gessinger"),
        (2, "Sociologia I", "Cristiano"),
    ],
    "3B": [
        (2, "Educação Física", "Giovani"),
        (2, "Física", "Alvaro"),
        (4, "Língua Portuguesa", "Mirele"),
        (4, "Matemática", "Paola"),
        (1, "Cidadania e Civismo", "Edelvan"),
        (2, "Educação Financeira", "Paola"),
        (1, "Projeto de vida", "Edelvan"),
        (2, "Rec língua portuguesa", "Mirele"),
        (2, "Rec matemática", "Mayhara"),
        (2, "Biologia II", "Carolina"),
        (2, "Física II", "Álvaro"),
        (2, "Física III", "Álvaro"),
        (2, "Matemática II", "Helmut"),
        (2, "Química", "Aline V"),
    ],
}

def deletar_grades_existentes(turmas_ids):
    """Deletar todas as grades das turmas especificadas"""
    print("\n🗑️  Deletando grades existentes...")
    
    # Buscar todas as grades
    response = requests.get(f"{API_URL}/grades-curriculares")
    grades = response.json()
    
    # Filtrar grades das turmas especificadas
    grades_para_deletar = [g for g in grades if g['turma_id'] in turmas_ids]
    
    print(f"   Encontradas {len(grades_para_deletar)} grades para deletar")
    
    for grade in grades_para_deletar:
        try:
            response = requests.delete(f"{API_URL}/grades-curriculares/{grade['id']}")
            if response.status_code == 200:
                print(f"   ✓ Grade {grade['id']} deletada")
            else:
                print(f"   ✗ Erro ao deletar grade {grade['id']}: {response.text}")
        except Exception as e:
            print(f"   ✗ Exceção ao deletar grade {grade['id']}: {e}")

def criar_grade(turma_id, disciplina_id, professor_id, aulas_por_semana):
    """Criar uma nova grade curricular"""
    data = {
        "turma_id": turma_id,
        "disciplina_id": disciplina_id,
        "professor_id": professor_id,
        "professor_id_2": None,
        "aulas_por_semana": aulas_por_semana,
        "ativa": True
    }
    
    try:
        response = requests.post(f"{API_URL}/grades-curriculares", json=data)
        if response.status_code in [200, 201]:
            return True
        else:
            print(f"      ✗ Erro: {response.text}")
            return False
    except Exception as e:
        print(f"      ✗ Exceção: {e}")
        return False

def main():
    print("=" * 60)
    print("🔧 Ajustando Grades Curriculares")
    print("=" * 60)
    
    # 1. Deletar grades existentes
    turmas_ids = list(TURMAS.values())
    deletar_grades_existentes(turmas_ids)
    
    # 2. Criar novas grades
    print("\n📝 Criando novas grades...")
    
    total_criadas = 0
    total_erros = 0
    
    for turma_nome, grades in GRADES.items():
        print(f"\n   Turma {turma_nome}:")
        turma_id = TURMAS[turma_nome]
        
        for aulas, disciplina, professor in grades:
            disciplina_id = DISCIPLINAS.get(disciplina)
            professor_id = PROFESSORES.get(professor)
            
            if not disciplina_id:
                print(f"      ✗ Disciplina '{disciplina}' não encontrada!")
                total_erros += 1
                continue
            
            if not professor_id:
                print(f"      ✗ Professor '{professor}' não encontrado!")
                total_erros += 1
                continue
            
            if criar_grade(turma_id, disciplina_id, professor_id, aulas):
                print(f"      ✓ {aulas} aulas - {disciplina} - {professor}")
                total_criadas += 1
            else:
                total_erros += 1
    
    # Resumo
    print("\n" + "=" * 60)
    print(f"✅ Grades criadas: {total_criadas}")
    if total_erros > 0:
        print(f"❌ Erros: {total_erros}")
    print("=" * 60)

if __name__ == "__main__":
    main()
