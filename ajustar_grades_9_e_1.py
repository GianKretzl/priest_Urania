#!/usr/bin/env python3
"""Script para ajustar grades curriculares das turmas 9º ano e 1º ano"""
import requests
import json

API_URL = "http://localhost:3000/api/proxy"

# Mapeamento de IDs
TURMAS = {
    "9A": 45,
    "9B": 46,
    "9C": 47,
    "9D": 48,
    "1A": 49,
    "1B": 50,
    "1C": 51
}

PROFESSORES = {
    "Aline": 122,
    "Aline V": 123,
    "Alvaro": 121,
    "Álvaro": 121,
    "Andreia": 124,
    "Andreza": 125,
    "Carolina": 126,
    "Cristiano": 127,
    "Diomar": 128,
    "Edelvan": 129,
    "Fernanda": 130,
    "Gessinger": 131,
    "Gian": 132,
    "Giovani": 133,
    "Helmut": 134,
    "Lucas": 135,
    "Lucia": 136,
    "Marly": 138,
    "MArly": 138,
    "Matheus": 139,
    "Mayhara": 140,
    "Mirele": 141,
    "Márcia Regina": 137,
    "Marcia Regina": 137,
    "Nadia": 142,
    "Paola": 143,
    "Rafaela": 144,
    "Renata": 145,
    "Rodrigo": 146,
    "Rosane": 147,
    "Rosani": 148,
    "SENAI": 150,
    "Sandro": 149
}

DISCIPLINAS = {
    "Arte": 185,
    "Arte II": 222,
    "Arte Paranaense": 209,
    "Biologia": 198,
    "Biologia II": 227,
    "Cidadania e Civismo": 193,
    "Ciências": 186,
    "Educação Financeira": 194,
    "Educação Física": 187,
    "Estratégias de MkT": 201,
    "Filosofia": 212,
    "Filosofia Análise de Textos Filos": 216,
    "Finanças Empresariais": 202,
    "Física": 220,
    "Física II": 228,
    "Física III": 229,
    "Física e Tecnologia": 219,
    "Geografia": 188,
    "Geografia I": 223,
    "Geografia do Paraná": 211,
    "História": 189,
    "História I": 224,
    "História do Paraná": 210,
    "Informática Empresarial": 206,
    "Literatura e Prod de texto": 214,
    "Língua Inglesa": 190,
    "Língua Inglesa I": 225,
    "Língua Portuguesa": 191,
    "Matemática": 192,
    "Matemática II": 230,
    "Princípios Econômicos": 207,
    "Princípios de Administração": 203,
    "Programação": 217,
    "Programação e IA": 200,
    "Programação e Robótica": 195,
    "Projeto de vida": 221,
    "Química": 199,
    "Rec. língua portuguesa": 196,
    "Recomp. língua portuguesa": 196,
    "Rec matemática": 197,
    "Recomp matemática": 197,
    "Rec matematica": 197,
    "Recursos Humanos": 204,
    "Robótica": 218,
    "SENAI": 208,
    "Sociologia": 213,
    "Sociologia GOV CID Sociedade": 215,
    "Sociologia I": 226,
    "Técnicas Integradas": 205
}

# Definição das grades
# Grade comum para todos os 9º anos
GRADE_9_ANO = [
    (2, "Arte", "Andreza", None),
    (2, "Ciências", "Andreia", None),
    (2, "Educação Física", "Giovani", None),
    (3, "Geografia", "Aline", None),
    (2, "História", "Rosani", None),
    (2, "Língua Inglesa", "Rafaela", None),
    (3, "Língua Portuguesa", "Renata", None),
    (5, "Matemática", "Nadia", None),
    (1, "Cidadania e Civismo", "Fernanda", None),
    (2, "Educação Financeira", "Diomar", None),
    (2, "Programação e Robótica", "Gian", None),
    (2, "Rec. língua portuguesa", "Márcia Regina", None),
    (2, "Rec matematica", "Mayhara", "Alvaro"),  # 2 professores
]

GRADES = {
    "9A": GRADE_9_ANO,
    "9B": GRADE_9_ANO,
    "9C": GRADE_9_ANO,
    "9D": GRADE_9_ANO,
    "1A": [
        (2, "Arte", "Andreza", None),
        (2, "Biologia", "Carolina", None),
        (2, "Educação Física", "Rodrigo", None),
        (2, "Geografia", "Edelvan", None),
        (1, "Língua Inglesa", "Rafaela", None),
        (1, "Língua Portuguesa", "Marcia Regina", None),
        (3, "Matemática", "Sandro", None),
        (1, "Cidadania e Civismo", "Cristiano", None),
        (1, "Programação e IA", "Lucas", None),
        (2, "Química", "Aline V", None),
        (2, "Estratégias de MkT", "Lucas", None),
        (2, "Finanças Empresariais", "Lucas", None),
        (2, "Princípios de Administração", "Lucia", None),
        (2, "Recursos Humanos", "Lucia", None),
        (1, "Técnicas Integradas", "Matheus", None),
        (2, "Informática Empresarial", "Lucia", None),
        (1, "Princípios Econômicos", "Matheus", None),
    ],
    "1B": [
        (2, "Arte", "Andreza", None),
        (2, "Biologia", "Carolina", None),
        (2, "Educação Física", "Rodrigo", None),
        (2, "Geografia", "Edelvan", None),
        (1, "Língua Inglesa", "Rafaela", None),
        (2, "Língua Portuguesa", "Marcia Regina", None),
        (3, "Matemática", "Sandro", None),
        (1, "Cidadania e Civismo", "Cristiano", None),
        (1, "Programação e IA", "Matheus", None),
        (2, "Química", "Aline V", None),
        (12, "SENAI", "SENAI", None),
    ],
    "1C": [
        (2, "Arte", "Andreza", None),
        (2, "Biologia", "Carolina", None),
        (2, "Educação Física", "Rodrigo", None),
        (2, "Geografia", "Edelvan", None),
        (2, "Língua Inglesa", "Rafaela", None),
        (4, "Língua Portuguesa", "Márcia Regina", None),
        (4, "Matemática", "Sandro", None),
        (1, "Cidadania e Civismo", "Cristiano", None),
        (2, "Programação e IA", "Matheus", None),
        (2, "Química", "Aline V", None),
        (2, "Educação Financeira", "Diomar", None),
        (1, "Arte Paranaense", "MArly", None),
        (2, "História do Paraná", "Rosane", None),
        (2, "Geografia do Paraná", "Edelvan", None),
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

def main():
    print("=" * 60)
    print("🔧 Ajustando Grades Curriculares - 9º Ano e 1º Ano")
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
        
        for item in grades:
            aulas, disciplina, professor = item[0], item[1], item[2]
            professor_2 = item[3] if len(item) > 3 else None
            
            disciplina_id = DISCIPLINAS.get(disciplina)
            professor_id = PROFESSORES.get(professor)
            professor_id_2 = PROFESSORES.get(professor_2) if professor_2 else None
            
            if not disciplina_id:
                print(f"      ✗ Disciplina '{disciplina}' não encontrada!")
                total_erros += 1
                continue
            
            if not professor_id:
                print(f"      ✗ Professor '{professor}' não encontrado!")
                total_erros += 1
                continue
            
            if professor_2 and not professor_id_2:
                print(f"      ✗ Professor 2 '{professor_2}' não encontrado!")
                total_erros += 1
                continue
            
            prof_text = f"{professor}"
            if professor_2:
                prof_text += f" + {professor_2}"
            
            if criar_grade(turma_id, disciplina_id, professor_id, aulas, professor_id_2):
                print(f"      ✓ {aulas} aulas - {disciplina} - {prof_text}")
                total_criadas += 1
            else:
                total_erros += 1
    
    # Resumo
    print("\n" + "=" * 60)
    print(f"✅ Grades criadas: {total_criadas}")
    if total_erros > 0:
        print(f"❌ Erros: {total_erros}")
    print("=" * 60)
    
    # Mostrar resumo por turma
    print("\n📊 Resumo por turma:")
    response = requests.get(f"{API_URL}/grades-curriculares")
    grades = response.json()
    
    for turma_nome, turma_id in TURMAS.items():
        grades_turma = [g for g in grades if g['turma_id'] == turma_id]
        total_aulas = sum(g['aulas_por_semana'] for g in grades_turma)
        print(f"   {turma_nome}: {len(grades_turma)} disciplinas, {total_aulas} aulas/semana")

if __name__ == "__main__":
    main()
