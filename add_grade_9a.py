#!/usr/bin/env python3
"""Adicionar grades da turma 9A"""
import requests
import json

API_URL = "http://localhost:3000/api/proxy"

# IDs
TURMA_9A = 45

PROFESSORES = {
    "Andreza": 125,
    "Andreia": 124,
    "Giovani": 133,
    "Aline": 122,
    "Rosane": 147,
    "Rafaela": 144,
    "Renata": 145,
    "Nadia": 142,
    "Fernanda": 130,
    "Diomar": 128,
    "Gian": 132,
    "Márcia Regina": 137,
    "Mayhara": 140,
    "Alvaro": 121
}

DISCIPLINAS = {
    "Arte": 185,
    "Ciências": 186,
    "Educação Física": 187,
    "Geografia": 188,
    "História": 189,
    "Língua Inglesa": 190,
    "Língua Portuguesa": 191,
    "Matemática": 192,
    "Cidadania e Civismo": 193,
    "Educação Financeira": 194,
    "Programação e Robótica": 195,
    "Rec. língua portuguesa": 196,
    "Rec matematica": 197
}

GRADES_9A = [
    (2, "Arte", "Andreza", None),
    (2, "Ciências", "Andreia", None),
    (2, "Educação Física", "Giovani", None),
    (3, "Geografia", "Aline", None),
    (2, "História", "Rosane", None),
    (2, "Língua Inglesa", "Rafaela", None),
    (3, "Língua Portuguesa", "Renata", None),
    (5, "Matemática", "Nadia", None),
    (1, "Cidadania e Civismo", "Fernanda", None),
    (2, "Educação Financeira", "Diomar", None),
    (2, "Programação e Robótica", "Gian", None),
    (2, "Rec. língua portuguesa", "Márcia Regina", None),
    (2, "Rec matematica", "Mayhara", "Alvaro"),  # 2 professores
]

def criar_grade(turma_id, disciplina_id, professor_id, aulas_por_semana, professor_id_2=None):
    """Criar uma nova grade curricular"""
    data = {
        "turma_id": turma_id,
        "disciplina_id": disciplina_id,
        "professor_id": professor_id,
        "professor_id_2": professor_id_2,
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

print("=" * 60)
print("📝 Cadastrando Grades da Turma 9A")
print("=" * 60)

total_criadas = 0
total_erros = 0

for item in GRADES_9A:
    aulas, disciplina, professor = item[0], item[1], item[2]
    professor_2 = item[3] if len(item) > 3 else None
    
    disciplina_id = DISCIPLINAS.get(disciplina)
    professor_id = PROFESSORES.get(professor)
    professor_id_2 = PROFESSORES.get(professor_2) if professor_2 else None
    
    if not disciplina_id:
        print(f"✗ Disciplina '{disciplina}' não encontrada!")
        total_erros += 1
        continue
    
    if not professor_id:
        print(f"✗ Professor '{professor}' não encontrado!")
        total_erros += 1
        continue
    
    if professor_2 and not professor_id_2:
        print(f"✗ Professor 2 '{professor_2}' não encontrado!")
        total_erros += 1
        continue
    
    prof_text = f"{professor}"
    if professor_2:
        prof_text += f" + {professor_2}"
    
    if criar_grade(TURMA_9A, disciplina_id, professor_id, aulas, professor_id_2):
        print(f"✓ {aulas} aulas - {disciplina} - {prof_text}")
        total_criadas += 1
    else:
        total_erros += 1

print("\n" + "=" * 60)
print(f"✅ Grades criadas: {total_criadas}")
if total_erros > 0:
    print(f"❌ Erros: {total_erros}")
print("=" * 60)
