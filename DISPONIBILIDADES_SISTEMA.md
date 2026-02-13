# Sistema de Disponibilidades dos Professores

## Problema Corrigido

O sistema de disponibilidades estava **impedindo a geração de horários** porque processava apenas disponibilidades negativas (bloqueios), ignorando disponibilidades positivas. Isso causava conflitos quando professores tinham horários específicos cadastrados.

## Como Funciona Agora

### 1. Disponibilidades Positivas (`disponivel=True`)
Quando um professor tem disponibilidades POSITIVAS cadastradas, o sistema:
- ✅ **PERMITE APENAS** os horários marcados como disponíveis
- ❌ **BLOQUEIA AUTOMATICAMENTE** todos os outros horários não marcados
- 📋 Exemplo: Se o professor marca "Segunda 08:00-12:00 disponível", apenas esse período será usado

### 2. Disponibilidades Negativas (`disponivel=False`)
Quando um professor tem disponibilidades NEGATIVAS cadastradas, o sistema:
- ❌ **BLOQUEIA** especificamente os horários marcados como indisponíveis
- ✅ **PERMITE** todos os outros horários
- 📋 Exemplo: Se o professor marca "Terça 14:00-18:00 indisponível", esse período será bloqueado

### 3. Sem Disponibilidades Cadastradas
Quando um professor NÃO tem disponibilidades cadastradas, o sistema:
- ✅ **PERMITE** qualquer horário disponível
- ⚠️ Recomenda cadastrar disponibilidades para melhor controle

## Detecção de Pendências

O sistema agora detecta automaticamente problemas de disponibilidade:

### Alta Severidade
- Professor não tem horários suficientes para todas as aulas
- Exemplo: "Professor João precisa de 15 slots mas tem apenas 10 disponíveis"

### Média Severidade  
- Professor tem disponibilidades justas (usando >80% dos horários)
- Exemplo: "Professor Maria utilizará 85% dos horários disponíveis"

### Baixa Severidade
- Professor sem disponibilidades cadastradas mas com muitas aulas
- Recomendação: cadastrar disponibilidades para melhor controle

## Como Usar no Sistema

### Cadastrar Disponibilidades Positivas
```
POST /api/disponibilidades/
{
  "professor_id": 1,
  "dia_semana": "SEGUNDA",
  "horario_inicio": "08:00",
  "horario_fim": "12:00",
  "disponivel": true,
  "turno": "MATUTINO"
}
```

### Bloquear Horários (Disponibilidades Negativas)
```
POST /api/disponibilidades/marcar-dia-nao-trabalha/1/SEGUNDA/MATUTINO
```

### Desbloquear Horários
```
DELETE /api/disponibilidades/desmarcar-dia-nao-trabalha/1/SEGUNDA/MATUTINO
```

## Turnos e Horários

### Turno Matutino (07:00 - 12:15)
- Slot 0: 07:00 - 07:50
- Slot 1: 07:50 - 08:40
- Slot 2: 08:45 - 09:35
- Slot 3: 09:45 - 10:35
- Slot 4: 10:35 - 11:25
- Slot 5: 11:25 - 12:15

### Turno Vespertino (13:00 - 18:15)
- Slot 0: 13:00 - 13:50
- Slot 1: 13:50 - 14:40
- Slot 2: 14:40 - 15:30
- Slot 3: 15:45 - 16:35
- Slot 4: 16:35 - 17:25
- Slot 5: 17:25 - 18:15

### Turno Noturno (18:00 - 22:30)
- Slot 0: 18:00 - 18:50
- Slot 1: 18:55 - 19:45
- Slot 2: 19:50 - 20:40
- Slot 3: 20:45 - 21:35
- Slot 4: 21:40 - 22:30

## Considerações Importantes

1. **Horas Atividade**: O sistema considera automaticamente as horas atividade do professor ao calcular slots necessários

2. **Múltiplos Professores**: Quando uma disciplina tem 2 professores, ambos precisam ter disponibilidades compatíveis

3. **Conflitos de Turno**: Disponibilidades são aplicadas por turno - um bloqueio no matutino não afeta o vespertino

4. **Bloqueio de Dia Inteiro**: Use horário "00:00" a "23:59" para bloquear um dia completo em todos os turnos

## Impacto nas Grades

Com as correções implementadas:
- ✅ Grades só serão criadas em horários permitidos pelos professores
- ✅ Sistema detecta automaticamente quando não há slots suficientes
- ✅ Mensagens de erro mais claras e com sugestões de resolução
- ✅ Melhor aproveitamento dos horários disponíveis

## Testando o Sistema

1. Cadastre disponibilidades para os professores
2. Tente gerar um horário
3. Verifique o campo `pendencias` na resposta para alertas
4. Ajuste as disponibilidades conforme necessário
5. Gere novamente o horário

## Logs e Debug

Durante a geração, o sistema exibe logs informativos:
```
Processando disponibilidades de 5 professores...
  Professor 1: aplicando 3 disponibilidade(s) positiva(s)
  Professor 2: aplicando 2 bloqueio(s)
```

Isso ajuda a identificar rapidamente como cada professor está configurado.
