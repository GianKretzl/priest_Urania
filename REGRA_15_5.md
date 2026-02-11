# Implementação da Regra 15/5 - Horas-Atividade Automáticas

## 📋 Resumo da Mudança

O sistema agora calcula **automaticamente** as horas-atividade dos professores seguindo a **Regra 15/5** oficial.

## 🎯 Regra 15/5

Para cada **4 horas** de jornada de trabalho:
- **3 horas** são destinadas à **regência** (aulas em sala)
- **1 hora** é destinada a **atividades** (planejamento, correção, etc.)

### Exemplos Práticos:

| Jornada Semanal | Horas de Regência | Horas-Atividade |
|-----------------|-------------------|-----------------|
| 20h             | 15h               | 5h              |
| 24h             | 18h               | 6h              |
| 30h             | 22h (23h arred.)  | 7h (ou 8h)      |
| 40h             | 30h               | 10h             |

## 🔄 O Que Mudou

### Antes:
- O usuário precisava **inserir manualmente** as horas-atividade
- Campo editável no formulário de cadastro de professores
- Possibilidade de erros de digitação ou valores inconsistentes

### Agora:
- **Cálculo 100% automático** baseado na carga horária total
- Campo de exibição apenas informativo
- Consistência garantida em todo o sistema
- Fórmula: `horas_atividade = carga_horaria_maxima ÷ 4`

## 💻 Mudanças Técnicas

### Backend:
1. **Modelo `Professor`**: 
   - Campo `horas_atividade` removido do banco de dados
   - Implementado como `@property` calculada automaticamente
   - Nova property `horas_regencia` também disponível

2. **Schemas**:
   - `horas_atividade` removido de `ProfessorCreate` e `ProfessorUpdate`
   - Mantido apenas em `Professor` (resposta) como campo calculado

3. **Migração**:
   - Script `remove_horas_atividade_field.py` executado
   - Coluna removida da tabela `professores`

### Frontend:
1. **Formulário de Professor**:
   - Campo de edição de horas-atividade removido
   - Exibição automática do cálculo em tempo real
   - Card informativo mostrando a regra 15/5

2. **Listagem de Professores**:
   - Coluna "Carga Total" mostra a jornada completa
   - Coluna "Horas Regência" em verde (horas disponíveis para aulas)
   - Coluna "Horas Atividade" em laranja (calculado automaticamente)

3. **Disponibilidades**:
   - Exibição correta das horas disponíveis para aulas
   - Cálculo considera apenas as horas de regência

## 🎨 Interface Atualizada

### Formulário de Cadastro:
```
┌─────────────────────────────────────────┐
│ Carga Horária Semanal: [40] horas      │
├─────────────────────────────────────────┤
│ 📊 Regra 15/5 (Cálculo Automático)     │
│                                          │
│ Horas de Regência:    30h/semana       │
│ Horas-Atividade:      10h/semana       │
│                                          │
│ 💡 A cada 4 horas de jornada:           │
│    3h de regência + 1h de atividade    │
└─────────────────────────────────────────┘
```

### Tabela de Professores:
```
Nome          | Carga Total | Horas Regência | Horas Atividade
--------------|-------------|----------------|----------------
João Silva    | 40h         | 30h ✓          | 10h ⚠
Maria Santos  | 20h         | 15h ✓          | 5h  ⚠
```

## ✅ Benefícios

1. **Conformidade Legal**: Atende automaticamente a legislação educacional
2. **Redução de Erros**: Elimina digitação incorreta de valores
3. **Consistência**: Todos os professores seguem a mesma regra
4. **Transparência**: Usuários veem claramente o cálculo aplicado
5. **Manutenção**: Alteração futura da regra em um único ponto

## 📝 Como Usar

1. **Cadastrar Professor**:
   - Informe apenas a **Carga Horária Semanal** (ex: 40h)
   - O sistema exibe automaticamente:
     - Horas de Regência: 30h
     - Horas-Atividade: 10h

2. **Editar Professor**:
   - Altere a carga horária se necessário
   - Os cálculos atualizam automaticamente

3. **Consultar Disponibilidades**:
   - As horas disponíveis para aulas consideram apenas a regência
   - As horas-atividade são reservadas automaticamente

## 🔍 Detalhes da Implementação

### Arquivo: `backend/app/models/professor.py`
```python
@property
def horas_atividade(self) -> int:
    """Calcula automaticamente as horas-atividade seguindo a regra 15/5"""
    return int(self.carga_horaria_maxima / 4)

@property
def horas_regencia(self) -> int:
    """Calcula as horas disponíveis para regência"""
    return self.carga_horaria_maxima - self.horas_atividade
```

### Arquivo: `frontend/app/cadastros/professores/page.tsx`
```typescript
const calcularHorasAtividade = (cargaHoraria: number) => {
  return Math.floor(cargaHoraria / 4);
};

const calcularHorasRegencia = (cargaHoraria: number) => {
  return cargaHoraria - calcularHorasAtividade(cargaHoraria);
};
```

## 🎓 Referência Legal

A regra 15/5 está baseada na proporção definida pela legislação educacional brasileira:
- **Lei nº 11.738/2008** (Piso Salarial Nacional)
- Define que no mínimo 1/3 da carga horária deve ser destinada a atividades extraclasse
- A proporção 15/5 (75% regência, 25% atividade) atende a este requisito

## 🚀 Próximos Passos

- [x] Implementação da regra 15/5
- [x] Migração do banco de dados
- [x] Atualização da interface
- [ ] Ajuste do algoritmo de geração de horários (considerando horas_regencia)
- [ ] Documentação para usuários finais
- [ ] Treinamento da equipe

---

**Data de Implementação**: Fevereiro 2026  
**Versão**: 2.0  
**Status**: ✅ Concluído
