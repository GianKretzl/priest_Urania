#!/usr/bin/env python3
"""Script para ajustar as grades curriculares do 1º Ano (1A, 1B, 1C)"""

import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

# Mapeamento de turmas
TURMAS = {
    "1A": {"id": 49, "nome": "1A - ADM"},
    "1B": {"id": 50, "nome": "1B - Eletromecânica"},
    "1C": {"id": 51, "nome": "1C"}
}

# Grades por turma
# Formato: (aulas_por_semana, disciplina_id, professor_id, nome_disciplina, nome_professor)
GRADES_1A = [
    (2, 185, 125, "Arte", "Andreza"),
    (2, 198, 126, "Biologia", "Carolina"),
    (2, 187, 146, "Educação Física", "Rodrigo"),
    (2, 188, 129, "Geografia", "Edelvan"),
    (1, 190, 144, "Língua Inglesa", "Rafaela"),
    (1, 191, 137, "Língua Portuguesa", "Márcia Regina"),
    (3, 192, 149, "Matemática", "Sandro"),
    (1, 193, 127, "Cidadania e Civismo", "Cristiano"),
    (1, 200, 135, "Programação e IA", "Lucas"),
    (2, 199, 123, "Química", "Aline V"),
    (2, 201, 135, "Estratégias de MkT", "Lucas"),
    (2, 202, 135, "Finanças Empresariais", "Lucas"),
    (2, 203, 136, "Princípios de Administração", "Lucia"),
    (2, 204, 136, "Recursos Humanos", "Lucia"),
    (1, 205, 139, "Técnicas Integradas", "Matheus"),
    (2, 206, 136, "Informática Empresarial", "Lucia"),
    (1, 207, 139, "Princípios Econômicos", "Matheus"),
]

GRADES_1B = [
    (2, 185, 125, "Arte", "Andreza"),
    (2, 198, 126, "Biologia", "Carolina"),
    (2, 187, 146, "Educação Física", "Rodrigo"),
    (2, 188, 129, "Geografia", "Edelvan"),
    (1, 190, 144, "Língua Inglesa", "Rafaela"),
    (2, 191, 137, "Língua Portuguesa", "Márcia Regina"),
    (3, 192, 149, "Matemática", "Sandro"),
    (1, 193, 127, "Cidadania e Civismo", "Cristiano"),
    (1, 200, 139, "Programação e IA", "Matheus"),
    (2, 199, 123, "Química", "Aline V"),
    (12, 208, 150, "SENAI", "SENAI"),
]

GRADES_1C = [
    (2, 185, 125, "Arte", "Andreza"),
    (2, 198, 126, "Biologia", "Carolina"),
    (2, 187, 146, "Educação Física", "Rodrigo"),
    (2, 188, 129, "Geografia", "Edelvan"),
    (2, 190, 144, "Língua Inglesa", "Rafaela"),
    (4, 191, 137, "Língua Portuguesa", "Márcia Regina"),
    (4, 192, 149, "Matemática", "Sandro"),
    (1, 193, 127, "Cidadania e Civismo", "Cristiano"),
    (2, 200, 139, "Programação e IA", "Matheus"),
    (2, 199, 123, "Química", "Aline V"),
    (2, 194, 128, "Educação Financeira", "Diomar"),
    (1, 209, 138, "Arte Paranaense", "Marly"),
    (2, 210, 147, "História do Paraná", "Rosane"),
    (2, 211, 129, "Geografia do Paraná", "Edelvan"),
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
    print("AJUSTE DE GRADES CURRICULARES - 1º ANO")
    print("="*70)
    
    resultados = {}
    
    # Processar cada turma
    resultados["1A"] = processar_turma("1A", GRADES_1A)
    resultados["1B"] = processar_turma("1B", GRADES_1B)
    resultados["1C"] = processar_turma("1C", GRADES_1C)
    
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
