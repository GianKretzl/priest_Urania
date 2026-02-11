#!/usr/bin/env python3
"""Script para ajustar a grade curricular do 1A - ADM"""

import requests
import json

BASE_URL = "http://localhost:8000/api/v1"
TURMA_ID = 49  # 1A

# Lista de disciplinas para o 1A - ADM
# Formato: (aulas_por_semana, disciplina_id, professor_id, nome_disciplina, nome_professor)
GRADES = [
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

def criar_grade(aulas, disciplina_id, professor_id, disc_nome, prof_nome):
    """Cria uma grade curricular"""
    data = {
        "turma_id": TURMA_ID,
        "disciplina_id": disciplina_id,
        "professor_id": professor_id,
        "professor_id_2": None,
        "aulas_por_semana": aulas,
        "ativa": True
    }
    
    try:
        response = requests.post(f"{BASE_URL}/grades-curriculares/", json=data)
        if response.status_code == 200:
            print(f"✓ {aulas}x {disc_nome} - {prof_nome}")
            return True
        else:
            print(f"✗ Erro ao criar {disc_nome}: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"✗ Exceção ao criar {disc_nome}: {e}")
        return False

def main():
    print("Ajustando grade curricular do 1A - ADM\n")
    print("=" * 60)
    
    total = len(GRADES)
    sucesso = 0
    
    for aulas, disc_id, prof_id, disc_nome, prof_nome in GRADES:
        if criar_grade(aulas, disc_id, prof_id, disc_nome, prof_nome):
            sucesso += 1
    
    print("=" * 60)
    print(f"\nResumo: {sucesso}/{total} grades criadas com sucesso")
    
    # Calcular total de aulas
    total_aulas = sum(g[0] for g in GRADES)
    print(f"Total de aulas/semana: {total_aulas}")

if __name__ == "__main__":
    main()
