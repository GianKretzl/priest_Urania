#!/usr/bin/env python3
"""Script para ajustar as grades curriculares do 2º e 3º Ano (2A, 2B, 3A, 3B)"""

import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

# Mapeamento de turmas
TURMAS = {
    "2A": {"id": 52, "nome": "2A"},
    "2B": {"id": 53, "nome": "2B"},
    "3A": {"id": 54, "nome": "3A"},
    "3B": {"id": 55, "nome": "3B"}
}

# Grades por turma
# Formato: (aulas_por_semana, disciplina_id, professor_id, nome_disciplina, nome_professor)
GRADES_2A = [
    (2, 185, 125, "Arte", "Andreza"),
    (2, 187, 146, "Educação Física", "Rodrigo"),
    (2, 190, 144, "Língua Inglesa", "Rafaela"),
    (4, 191, 145, "Língua Portuguesa", "Renata"),
    (4, 192, 149, "Matemática", "Sandro"),
    (2, 212, 127, "Filosofia", "Cristiano"),
    (2, 194, 140, "Educação Financeira", "Mayhara"),
    (1, 193, 130, "Cidadania e Civismo", "Fernanda"),
    (2, 213, 127, "Sociologia", "Cristiano"),
    (2, 214, 130, "Literatura e Prod de texto", "Fernanda"),
    (1, 215, 129, "Sociologia GOV CID Sociedade", "Edelvan"),
    (2, 216, 127, "Filosofia Análise de Textos Filos", "Cristiano"),
    (2, 220, 121, "Física", "Alvaro"),
    (2, 189, 147, "História", "Rosane"),
]

GRADES_2B = [
    (2, 185, 125, "Arte", "Andreza"),
    (2, 187, 146, "Educação Física", "Rodrigo"),
    (2, 190, 144, "Língua Inglesa", "Rafaela"),
    (4, 191, 145, "Língua Portuguesa", "Renata"),
    (4, 192, 149, "Matemática", "Sandro"),
    (2, 212, 127, "Filosofia", "Cristiano"),
    (2, 194, 140, "Educação Financeira", "Mayhara"),
    (1, 193, 130, "Cidadania e Civismo", "Fernanda"),
    (2, 213, 127, "Sociologia", "Cristiano"),
    (2, 217, 132, "Programação", "Gian"),
    (2, 218, 132, "Robótica", "Gian"),
    (2, 220, 121, "Física", "Alvaro"),
    (2, 189, 147, "História", "Rosane"),
    (1, 219, 121, "Física e Tecnologia", "Alvaro"),
]

GRADES_3A = [
    (2, 187, 133, "Educação Física", "Giovani"),
    (2, 220, 121, "Física", "Alvaro"),
    (4, 191, 141, "Língua Portuguesa", "Mirele"),
    (4, 192, 143, "Matemática", "Paola"),
    (1, 193, 129, "Cidadania e Civismo", "Edelvan"),
    (2, 194, 140, "Educação Financeira", "Mayhara"),
    (1, 221, 129, "Projeto de vida", "Edelvan"),
    (2, 196, 141, "Recomp. língua portuguesa", "Mirele"),
    (2, 197, 140, "Recomp matemática", "Mayhara"),
    (2, 222, 138, "Arte II", "Marly"),
    (2, 223, 129, "Geografia I", "Edelvan"),
    (2, 224, 147, "História I", "Rosane"),
    (2, 225, 131, "Língua Inglesa I", "Gessinger"),
    (2, 226, 127, "Sociologia I", "Cristiano"),
]

GRADES_3B = [
    (2, 187, 133, "Educação Física", "Giovani"),
    (2, 220, 121, "Física", "Alvaro"),
    (4, 191, 141, "Língua Portuguesa", "Mirele"),
    (4, 192, 143, "Matemática", "Paola"),
    (1, 193, 129, "Cidadania e Civismo", "Edelvan"),
    (2, 194, 143, "Educação Financeira", "Paola"),
    (1, 221, 129, "Projeto de vida", "Edelvan"),
    (2, 196, 141, "Recomp. língua portuguesa", "Mirele"),
    (2, 197, 140, "Recomp matemática", "Mayhara"),
    (2, 227, 126, "Biologia II", "Carolina"),
    (2, 228, 121, "Física II", "Alvaro"),
    (2, 229, 121, "Física III", "Alvaro"),
    (2, 230, 134, "Matemática II", "Helmut"),
    (2, 199, 123, "Química", "Aline V"),
]

def criar_grade(turma_id, aulas, disciplina_id, professor_id, disc_nome, prof_nome):
    """Cria uma grade curricular"""
    data = {
        "turma_id": turma_id,
        "disciplina_id": disciplina_id,
        "professor_id": professor_id,
        "professor_id_2": None,
        "aulas_por_semana": aulas,
        "ativa": True
    }
    
    try:
        response = requests.post(f"{BASE_URL}/grades-curriculares/", json=data)
        if response.status_code == 200:
            print(f"  ✓ {aulas}x {disc_nome} - {prof_nome}")
            return True
        else:
            print(f"  ✗ Erro ao criar {disc_nome}: {response.status_code} - {response.text[:100]}")
            return False
    except Exception as e:
        print(f"  ✗ Exceção ao criar {disc_nome}: {e}")
        return False

def processar_turma(turma_key, grades):
    """Processa todas as grades de uma turma"""
    turma_info = TURMAS[turma_key]
    turma_id = turma_info["id"]
    turma_nome = turma_info["nome"]
    
    print(f"\n{'='*70}")
    print(f"Processando: {turma_nome}")
    print('='*70)
    
    sucesso = 0
    total = len(grades)
    
    for aulas, disc_id, prof_id, disc_nome, prof_nome in grades:
        if criar_grade(turma_id, aulas, disc_id, prof_id, disc_nome, prof_nome):
            sucesso += 1
    
    total_aulas = sum(g[0] for g in grades)
    print(f"\nResumo {turma_nome}: {sucesso}/{total} grades criadas")
    print(f"Total de aulas/semana: {total_aulas}")
    
    return sucesso, total, total_aulas

def main():
    print("\n" + "="*70)
    print("AJUSTE DE GRADES CURRICULARES - 2º E 3º ANO")
    print("="*70)
    
    resultados = {}
    
    # Processar cada turma
    resultados["2A"] = processar_turma("2A", GRADES_2A)
    resultados["2B"] = processar_turma("2B", GRADES_2B)
    resultados["3A"] = processar_turma("3A", GRADES_3A)
    resultados["3B"] = processar_turma("3B", GRADES_3B)
    
    # Resumo geral
    print("\n" + "="*70)
    print("RESUMO GERAL")
    print("="*70)
    
    total_grades = sum(r[1] for r in resultados.values())
    total_criadas = sum(r[0] for r in resultados.values())
    total_aulas = sum(r[2] for r in resultados.values())
    
    for turma_key, (sucesso, total, aulas) in resultados.items():
        print(f"{TURMAS[turma_key]['nome']:30} {sucesso}/{total} grades | {aulas} aulas/semana")
    
    print("="*70)
    print(f"TOTAL: {total_criadas}/{total_grades} grades criadas | {total_aulas} aulas/semana")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
