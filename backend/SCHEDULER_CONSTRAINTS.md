# Restrições do Gerador de Horários

Este documento descreve todas as restrições implementadas no motor de geração de horários do sistema Urânia.

## 🔒 Restrições Fortes (Hard Constraints)

Essas restrições **DEVEM** ser satisfeitas. Se não forem, o horário é considerado inválido.

### 1. Uma aula por vez por turma
Uma turma não pode ter duas aulas ao mesmo tempo.

### 2. Uma aula por vez por professor
Um professor não pode dar duas aulas ao mesmo tempo.

### 3. Uma aula por vez por ambiente
Um ambiente (sala) não pode ser usado por duas turmas ao mesmo tempo.

### 4. Todas as aulas devem ser alocadas
Cada aula prevista na grade curricular deve ser alocada exatamente uma vez.

### 5. Respeitar disponibilidade do professor
**Implementação**: `_adicionar_restricoes_disponibilidade()`

Se um professor indicar que está indisponível em determinado dia/horário:
- Ele **não pode** ser alocado para dar aula nesse período
- Casos de uso:
  - Professor tem outro emprego
  - Folgas semanais
  - Compromissos pessoais fixos

**Exemplo**:
```python
# Professor João não pode dar aula às segundas-feiras de manhã
Disponibilidade(
    professor_id=1,
    dia_semana="SEGUNDA",
    horario_inicio="07:30",
    horario_fim="12:00",
    disponivel=False  # FALSE = indisponível
)
```

### 6. Limitar aulas seguidas por professor
**Implementação**: `_adicionar_restricoes_aulas_seguidas()`

Respeita o número máximo de aulas consecutivas que um professor pode dar.
- Campo: `Professor.max_aulas_seguidas`
- Padrão: 4 aulas seguidas
- Previne cansaço excessivo do professor

**Exemplo**:
```python
# Professor não pode dar mais de 3 aulas seguidas
Professor(
    nome="Maria Silva",
    max_aulas_seguidas=3  # Máximo 3 aulas consecutivas
)
```

### 7. Limitar aulas por dia
**Implementação**: `_adicionar_restricoes_aulas_por_dia()`

Limita o total de aulas que um professor pode dar em um único dia.
- Campo: `Professor.max_aulas_dia`
- Padrão: 8 aulas por dia
- Garante equilíbrio na distribuição da carga

**Exemplo**:
```python
# Professor não pode dar mais de 6 aulas no mesmo dia
Professor(
    nome="Carlos Santos",
    max_aulas_dia=6  # Máximo 6 aulas por dia
)
```

### 8. Respeitar horas-atividade ⭐ **NOVO**
**Implementação**: `_adicionar_restricoes_horas_atividade()`

Garante que professores tenham tempo reservado para atividades extraclasse:
- Planejamento de aulas
- Correção de provas
- Reuniões pedagógicas
- Atendimento a alunos

**Cálculo**:
```
Horas disponíveis para aulas = Carga horária máxima - Horas-atividade
Máximo de aulas na semana = Horas disponíveis / Duração da aula
```

**Exemplo**:
```python
# Professor com 40h semanais, sendo 8h para atividades
Professor(
    nome="Ana Costa",
    carga_horaria_maxima=40,  # 40 horas semanais
    horas_atividade=8,        # 8 horas para atividades
)
# Resultado: Máximo de 32 horas de aula = 38 aulas de 50min
```

**Benefícios**:
- ✅ Respeita legislação trabalhista
- ✅ Melhora qualidade das aulas (professor mais preparado)
- ✅ Previne sobrecarga de trabalho

### 9. Considerar deslocamento entre sedes ⭐ **NOVO**
**Implementação**: `_adicionar_restricoes_deslocamento()`

Quando a escola possui múltiplas sedes, o sistema considera o tempo necessário para o professor se deslocar entre elas.

**Lógica**:
1. Identifica quando um professor tem aulas consecutivas em sedes diferentes
2. Calcula quantos slots de aula são necessários para o deslocamento
3. Bloqueia alocações que não respeitem esse tempo mínimo

**Cálculo de slots necessários**:
```
slots_deslocamento = ceil(tempo_deslocamento_minutos / duracao_aula_minutos)
mínimo = 1 slot (mesmo para deslocamentos curtos)
```

**Exemplo 1 - Tempo suficiente**:
```python
Professor(
    nome="Pedro Lima",
    tempo_deslocamento=60  # 60 minutos entre sedes
)

# Aula 1: Segunda-feira, 08:00 - Sede Centro (slot 1)
# Aula 2: Segunda-feira, 10:30 - Sede Norte (slot 4)
# ✅ VÁLIDO: 2h30min de intervalo (3 slots) > 1h de deslocamento
```

**Exemplo 2 - Tempo insuficiente**:
```python
# Aula 1: Segunda-feira, 08:00 - Sede Centro (slot 1)
# Aula 2: Segunda-feira, 08:50 - Sede Norte (slot 2)
# ❌ INVÁLIDO: 50min de intervalo < 1h de deslocamento necessário
```

**Benefícios**:
- ✅ Evita atrasos do professor
- ✅ Respeita condições reais de trânsito
- ✅ Reduz estresse e melhora pontualidade

**Estrutura de dados**:
```python
# Sedes
Sede(nome="Sede Centro", endereco="Rua A, 123")
Sede(nome="Sede Norte", endereco="Av. B, 456")

# Ambientes vinculados a sedes
Ambiente(nome="Sala 101", sede_id=1)  # Sede Centro
Ambiente(nome="Sala 201", sede_id=2)  # Sede Norte

# Professor com tempo de deslocamento
Professor(
    nome="Roberto Alves",
    tempo_deslocamento=45  # 45 minutos entre sedes
)
```

---

## 🎯 Restrições Fracas (Soft Constraints)

Essas restrições são **DESEJÁVEIS** mas não obrigatórias. O sistema tenta otimizá-las.

### Minimizar Janelas
**Implementação**: `adicionar_objetivos()`

Busca evitar ou minimizar horários vagos ("janelas") na grade do professor.

**O que é uma janela?**
- Professor tem aula às 8h
- Não tem aula às 9h (janela)
- Tem aula às 10h

**Por que é ruim?**
- Professor fica ocioso na escola
- Tempo desperdiçado
- Desmotivação

**Como funciona**:
- Detecta sequências: aula → vazio → aula
- Adiciona penalidade para cada janela encontrada
- Função objetivo minimiza essas penalidades

---

## 🔧 Como Usar

### Configurar um Professor

```python
professor = Professor(
    nome="José da Silva",
    email="jose@escola.com",
    
    # Carga horária
    carga_horaria_maxima=40,  # 40h semanais
    horas_atividade=8,        # 8h para atividades extraclasse
    
    # Limites
    max_aulas_seguidas=4,     # Máx 4 aulas consecutivas
    max_aulas_dia=8,          # Máx 8 aulas por dia
    
    # Deslocamento
    tempo_deslocamento=30,    # 30min entre sedes
    
    ativo=True
)
```

### Configurar Disponibilidade

```python
# Professor NÃO disponível às quartas-feiras à tarde
disponibilidade = Disponibilidade(
    professor_id=professor.id,
    dia_semana="QUARTA",
    horario_inicio="13:00",
    horario_fim="18:00",
    disponivel=False  # FALSE = bloqueado
)
```

---

## 📊 Impacto no Desempenho

| Restrição | Complexidade | Impacto na Geração |
|-----------|--------------|-------------------|
| Alocação única | O(n) | Baixo ⚡ |
| Disponibilidade | O(n×d×s) | Médio ⚡⚡ |
| Aulas seguidas | O(n×d×s²) | Médio ⚡⚡ |
| Horas-atividade | O(n×d×s) | Baixo ⚡ |
| Deslocamento | O(n×d×s²×k²) | Alto ⚡⚡⚡ |
| Minimizar janelas | O(n×d×s³) | Alto ⚡⚡⚡ |

**Legenda**:
- n = número de professores
- d = dias da semana
- s = slots por dia
- k = número de sedes

---

## 🐛 Troubleshooting

### Erro: "Não foi possível gerar um horário válido"

**Causas possíveis**:

1. **Disponibilidade muito restritiva**
   - Solução: Revisar bloqueios de horários dos professores

2. **Deslocamento impossível**
   - Solução: Reduzir `tempo_deslocamento` ou aumentar gaps entre aulas

3. **Horas-atividade muito alta**
   - Solução: Ajustar proporção horas_atividade/carga_horaria_maxima

4. **Conflito de recursos**
   - Solução: Adicionar mais ambientes (salas) ou professores

### Dica: Análise incremental

Desabilite restrições temporariamente para identificar o problema:

```python
# Comentar temporariamente no método adicionar_restricoes():
# self._adicionar_restricoes_horas_atividade()  # Teste sem essa restrição
# self._adicionar_restricoes_deslocamento()     # Teste sem essa restrição
```

---

## 📚 Referências

- [OR-Tools CP-SAT Documentation](https://developers.google.com/optimization/cp/cp_solver)
- [Constraint Programming Handbook](https://www.springer.com/gp/book/9780444527264)
- [Employee Scheduling Problem](https://developers.google.com/optimization/scheduling/employee_scheduling)

---

**Versão**: 1.0  
**Última atualização**: Fevereiro 2026  
**Autor**: Sistema Urânia - No Cry Baby
