# Funcionalidade: Múltiplos Professores por Aula

## Visão Geral

Este documento descreve a funcionalidade que permite que disciplinas específicas (como Recuperação de Matemática e Recuperação de Língua Portuguesa) tenham dois professores simultaneamente na mesma aula.

## Conceito

Em algumas disciplinas de recuperação, é pedagógico ter dois professores trabalhando juntos na mesma sala de aula simultaneamente. Isso permite:

- Melhor atendimento individualizado aos alunos
- Divisão de turmas em grupos menores
- Troca de experiências entre professores
- Cobertura de diferentes estilos de aprendizagem

## Implementação Técnica

### 1. Modelo de Dados

#### Disciplina
Adicionado o campo `multiplos_professores` (BOOLEAN):
- `True`: A disciplina permite/requer 2 professores simultaneamente
- `False`: A disciplina funciona com apenas 1 professor (padrão)

```python
class Disciplina(Base):
    # ... campos existentes ...
    multiplos_professores = Column(Boolean, default=False)
```

#### Grade Curricular
Adicionado o campo `professor_id_2` (INTEGER, nullable):
- Armazena o ID do segundo professor quando a disciplina permite múltiplos professores
- Se `NULL`, a grade curricular tem apenas 1 professor

```python
class GradeCurricular(Base):
    # ... campos existentes ...
    professor_id = Column(Integer, ForeignKey("professores.id"), nullable=False)
    professor_id_2 = Column(Integer, ForeignKey("professores.id"), nullable=True)
```

#### Horário Aula
Adicionado o campo `professor_id_2` (INTEGER, nullable):
- Armazena o ID do segundo professor na aula gerada
- Copiado automaticamente da grade curricular durante a geração do horário

```python
class HorarioAula(Base):
    # ... campos existentes ...
    professor_id = Column(Integer, ForeignKey("professores.id"), nullable=False)
    professor_id_2 = Column(Integer, ForeignKey("professores.id"), nullable=True)
```

### 2. Scheduler/Generator

O scheduler foi modificado para:

1. **Restrições de Conflito**: Ao verificar se um professor está disponível em um horário, o sistema agora verifica se ele é o professor principal OU o segundo professor de alguma grade.

2. **Extração da Solução**: Ao criar as aulas, o sistema copia automaticamente o `professor_id_2` da grade curricular se existir.

```python
# Verificar se o professor é o principal ou o segundo professor
if grade.professor_id == prof_id or (hasattr(grade, 'professor_id_2') and grade.professor_id_2 == prof_id):
    # ... adicionar restrição ...
```

### 3. Schemas da API

Atualizados os schemas Pydantic para incluir os novos campos:

- `DisciplinaBase`: `multiplos_professores: bool = False`
- `DisciplinaUpdate`: `multiplos_professores: Optional[bool] = None`
- `GradeCurricularBase`: `professor_id_2: Optional[int] = None`
- `GradeCurricularUpdate`: `professor_id_2: Optional[int] = None`
- `HorarioAulaBase`: `professor_id_2: Optional[int] = None`

### 4. Dados Seed

Os dados de exemplo incluem disciplinas de recuperação configuradas automaticamente:

- **Rec. língua portuguesa**: 2 aulas/semana com 2 professores
- **Rec matemática**: 2 aulas/semana com 2 professores

Exemplo de configuração no seed:
```python
("Rec matemática", 2, "Mayhara", "Alvaro"),  # 2 professores simultaneamente
```

## Migração do Banco de Dados

Para aplicar as mudanças em um banco existente, execute:

```bash
cd backend
python migrations/add_multiplos_professores.py
```

O script de migração:
1. Adiciona `multiplos_professores` à tabela `disciplinas`
2. Adiciona `professor_id_2` à tabela `grades_curriculares`
3. Adiciona `professor_id_2` à tabela `horarios_aulas`
4. Marca automaticamente disciplinas de recuperação como `multiplos_professores = TRUE`

## Como Usar

### 1. Criar uma Disciplina com Múltiplos Professores

```json
POST /api/v1/disciplinas
{
  "nome": "Recuperação de Matemática",
  "carga_horaria_semanal": 2,
  "multiplos_professores": true
}
```

### 2. Criar uma Grade Curricular com 2 Professores

```json
POST /api/v1/grades-curriculares
{
  "turma_id": 1,
  "disciplina_id": 5,
  "professor_id": 10,
  "professor_id_2": 15,
  "aulas_por_semana": 2
}
```

### 3. Gerar Horário

O horário é gerado normalmente. O scheduler automaticamente:
- Aloca ambos os professores para o mesmo horário
- Garante que ambos os professores estejam disponíveis
- Verifica conflitos para ambos os professores

```json
POST /api/v1/horarios/{horario_id}/gerar
{
  "tempo_maximo_geracao": 300
}
```

### 4. Visualizar Aulas Geradas

As aulas geradas incluirão o `professor_id_2`:

```json
GET /api/v1/horarios/{horario_id}/aulas

[
  {
    "id": 123,
    "disciplina_id": 5,
    "turma_id": 1,
    "professor_id": 10,
    "professor_id_2": 15,
    "dia_semana": "SEGUNDA",
    "horario_inicio": "08:00",
    "horario_fim": "08:50",
    ...
  }
]
```

## Considerações

### Carga Horária
- A carga horária de **ambos** os professores é incrementada pelas aulas com múltiplos professores
- Se uma disciplina tem 2 aulas/semana com 2 professores, cada professor tem +2 aulas na sua carga

### Disponibilidade
- Ambos os professores precisam estar disponíveis no mesmo horário
- Isso pode tornar o problema de alocação mais restrito
- Se não houver horário comum, a aula não será alocada

### Conflitos
- Um professor não pode ter duas aulas simultaneamente, seja como professor principal ou secundário
- O scheduler valida ambos os papéis ao verificar conflitos

### Ambientes
- Uma aula com 2 professores ainda ocupa apenas 1 ambiente
- Os dois professores compartilham o mesmo espaço físico

## Disciplinas Aplicáveis

Por padrão, as seguintes disciplinas são marcadas como `multiplos_professores = TRUE`:

- Rec. língua portuguesa
- Rec matemática
- Recuperação de Matemática
- Recuperação de Língua Portuguesa

Outras disciplinas podem ser configuradas conforme necessário através da API.

## Exemplo de Fluxo Completo

1. **Disciplina configurada**: `Rec matemática` (multiplos_professores = true)
2. **Grade criada**: Turma 9A, Rec matemática, Prof. Mayhara + Prof. Alvaro, 2 aulas/semana
3. **Horário gerado**: O scheduler encontra horários onde ambos estão disponíveis
4. **Resultado**: 2 aulas criadas com ambos os professores alocados simultaneamente

## Troubleshooting

### Problema: Aulas de recuperação não sendo alocadas

**Possíveis causas:**
1. Os 2 professores não têm horários em comum disponíveis
2. Conflitos com outras aulas de um ou ambos os professores
3. Falta de ambientes disponíveis

**Soluções:**
1. Verificar e ajustar disponibilidades dos professores
2. Reduzir carga horária de outros componentes
3. Aumentar flexibilidade nas restrições de horário
4. Adicionar mais ambientes/salas

### Problema: Erro ao criar grade curricular

**Causa:** `professor_id_2` referencia um professor inválido

**Solução:** Verificar que o ID do segundo professor existe e está ativo

## Extensões Futuras

Possíveis melhorias para esta funcionalidade:

1. **Suporte a 3+ professores**: Generalizar para N professores
2. **Preferências de duplas**: Alguns professores trabalham melhor juntos
3. **Divisão de turmas**: Permitir que os professores dividam a turma em grupos
4. **Rodízio**: Alternar quais professores trabalham juntos a cada semana
5. **Visualização especial**: Interface que destaque aulas com múltiplos professores

## Arquivos Modificados

- `backend/app/models/disciplina.py`
- `backend/app/models/grade_curricular.py`
- `backend/app/models/horario.py`
- `backend/app/scheduler/generator.py`
- `backend/app/schemas/__init__.py`
- `backend/seed_data.py`
- `backend/migrations/add_multiplos_professores.py` (novo)

---

**Última atualização:** 2026-02-09
**Versão:** 1.0
