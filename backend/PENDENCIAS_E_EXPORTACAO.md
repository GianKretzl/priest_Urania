# Sistema de Pendências e Exportação - Urânia

Este documento descreve o sistema de detecção de pendências, sugestões inteligentes e exportação de horários.

## 🔍 Sistema de Detecção de Pendências

O Urânia possui um sistema inteligente que analisa o processo de geração e identifica **por que** o horário não pôde ser gerado perfeitamente ou quais problemas foram encontrados.

### Tipos de Pendências Detectadas

#### 1. Aulas Não Alocadas
**Severidade**: ALTA  
**Quando ocorre**: Quando nem todas as aulas conseguem ser encaixadas no horário

**Exemplo de mensagem**:
```json
{
  "tipo": "AULAS_NAO_ALOCADAS",
  "severidade": "ALTA",
  "mensagem": "15 aula(s) não foram alocadas",
  "detalhes": "Taxa de alocação: 75.5%"
}
```

#### 2. Disponibilidade Insuficiente
**Severidade**: MÉDIA  
**Quando ocorre**: Professor tem muitas aulas mas poucos horários disponíveis

**Exemplo de mensagem**:
```json
{
  "tipo": "DISPONIBILIDADE_INSUFICIENTE",
  "severidade": "MEDIA",
  "mensagem": "Professor João Silva tem poucos horários disponíveis",
  "sugestao": "Considere liberar alguns horários bloqueados ou reduzir a carga horária",
  "professor_id": 5
}
```

**Sugestões oferecidas**:
- Liberar horários bloqueados em dias específicos
- Reduzir número de aulas do professor
- Redistribuir disciplinas para outros professores

#### 3. Capacidade de Ambientes
**Severidade**: MÉDIA  
**Quando ocorre**: Poucas salas para muitas turmas

**Exemplo de mensagem**:
```json
{
  "tipo": "CAPACIDADE_AMBIENTES",
  "severidade": "MEDIA",
  "mensagem": "Taxa de ocupação de ambientes muito alta (85.3%)",
  "sugestao": "Considere adicionar mais salas de aula ou distribuir turmas em outros turnos"
}
```

**Sugestões oferecidas**:
- Adicionar mais salas de aula
- Criar mais ambientes no cadastro
- Dividir turmas em múltiplos turnos

#### 4. Conflitos de Deslocamento
**Severidade**: BAIXA  
**Quando ocorre**: Professor tem tempo de deslocamento muito longo entre sedes

**Exemplo de mensagem**:
```json
{
  "tipo": "DESLOCAMENTO_PROBLEMATICO",
  "severidade": "BAIXA",
  "mensagem": "Professor Maria Costa tem tempo de deslocamento alto (60min)",
  "sugestao": "Considere alocar aulas do professor em apenas uma sede ou reduzir o tempo de deslocamento",
  "professor_id": 12
}
```

**Sugestões oferecidas**:
- Concentrar aulas do professor em uma única sede
- Ajustar tempo de deslocamento no cadastro
- Reorganizar distribuição de turmas por sede

### Como Usar as Pendências

#### 1. Geração de Horário
```bash
POST /api/v1/horarios/{id}/gerar
```

**Resposta com pendências**:
```json
{
  "success": true,
  "message": "Horário gerado com sucesso! (3 pendência(s) detectada(s))",
  "horario_id": 1,
  "total_aulas": 240,
  "aulas_alocadas": 235,
  "qualidade_score": 87,
  "tempo_geracao": 12.5,
  "pendencias": [
    {
      "tipo": "AULAS_NAO_ALOCADAS",
      "severidade": "ALTA",
      "mensagem": "5 aula(s) não foram alocadas",
      "detalhes": "Taxa de alocação: 97.9%"
    },
    {
      "tipo": "DISPONIBILIDADE_INSUFICIENTE",
      "severidade": "MEDIA",
      "mensagem": "Professor Carlos Santos tem poucos horários disponíveis",
      "sugestao": "Considere liberar alguns horários bloqueados ou reduzir a carga horária",
      "professor_id": 8
    }
  ]
}
```

#### 2. Aplicar Sugestões

1. **Revisar pendência**: Ler mensagem e sugestão
2. **Ajustar dados**: Modificar cadastros conforme sugestão
3. **Gerar novamente**: Executar geração de horário novamente

**Exemplo de fluxo**:
```
1. Gerar horário → Detecta pendência
2. Pendência diz: "Professor X tem poucos horários disponíveis"
3. Sugestão: "Libere sexta-feira à tarde"
4. Ação: Remover bloqueio de sexta à tarde do Professor X
5. Gerar novamente → Sucesso!
```

---

## 📈 Sistema de Qualidade Avançado

O score de qualidade (0-100) é calculado baseado em múltiplos critérios:

### Componentes do Score

#### 1. Taxa de Alocação (40 pontos)
Percentual de aulas que foram alocadas com sucesso.

```
Pontos = (aulas_alocadas / total_aulas) × 40
```

**Exemplo**:
- 240 aulas planejadas
- 235 alocadas
- Score: (235/240) × 40 = 39.2 pontos

#### 2. Distribuição Uniforme (30 pontos)
Avalia se as aulas estão bem distribuídas ao longo da semana.

```
Pontos = max(0, 30 - (desvio_padrão × 5))
```

**Exemplo**:
- Segunda: 50 aulas
- Terça: 48 aulas  
- Quarta: 47 aulas
- Quinta: 49 aulas
- Sexta: 46 aulas
- Desvio baixo → Score alto (25-30 pontos)

#### 3. Minimização de Janelas (20 pontos)
Penaliza horários vagos entre aulas dos professores.

```
Pontos = max(0, 20 - (janelas_encontradas / max_janelas) × 20)
```

**O que é uma janela?**
```
08:00 - Matemática ✅
09:00 - (vazio) ❌ JANELA
10:00 - Física ✅
```

#### 4. Preferências (10 pontos)
Placeholder para futuras implementações de preferências de horário.

### Interpretação do Score

| Score | Qualidade | Descrição |
|-------|-----------|-----------|
| 90-100 | Excelente ⭐⭐⭐⭐⭐ | Horário ideal, todas as aulas alocadas, bem distribuído |
| 75-89 | Ótimo ⭐⭐⭐⭐ | Horário muito bom, poucas pendências |
| 60-74 | Bom ⭐⭐⭐ | Horário aceitável, algumas melhorias possíveis |
| 40-59 | Regular ⭐⭐ | Horário funcional mas com problemas significativos |
| 0-39 | Ruim ⭐ | Muitos problemas, revisar restrições |

---

## 📄 Sistema de Exportação

O Urânia oferece exportação de horários em múltiplos formatos para diferentes públicos.

### Formatos Disponíveis

#### 1. HTML (Visualização Elegante)
**Uso**: Visualização na web, impressão, compartilhamento

**Endpoints**:
```
GET /api/v1/horarios/{id}/export/turma/{turma_id}/html
GET /api/v1/horarios/{id}/export/professor/{professor_id}/html
```

**Características**:
- ✅ Visual profissional e limpo
- ✅ Cores diferenciadas (turma/professor)
- ✅ Responsivo (mobile-friendly)
- ✅ Otimizado para impressão
- ✅ Pronto para navegador

**Exemplo de uso**:
```bash
# Exportar horário da Turma 3A em HTML
curl http://localhost:8000/api/v1/horarios/1/export/turma/5/html > turma_3a.html

# Visualizar no navegador
open turma_3a.html
```

**Preview do HTML**:
```html
<!DOCTYPE html>
<html>
<head>
  <title>Horário - Turma 3A</title>
  <style>
    /* Estilo profissional incluído */
  </style>
</head>
<body>
  <h1>Horário de Aulas - Turma 3A</h1>
  <table>
    <thead>
      <tr>
        <th>Horário</th>
        <th>Segunda</th>
        <th>Terça</th>
        ...
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>07:30 - 08:20</td>
        <td>Matemática<br>Prof. João</td>
        ...
      </tr>
    </tbody>
  </table>
</body>
</html>
```

#### 2. CSV (Planilhas e Excel)
**Uso**: Análise em planilhas, processamento de dados

**Endpoints**:
```
GET /api/v1/horarios/{id}/export/turma/{turma_id}/csv
GET /api/v1/horarios/{id}/export/professor/{professor_id}/csv
```

**Características**:
- ✅ Compatível com Excel/Google Sheets
- ✅ Fácil manipulação de dados
- ✅ Importação em outros sistemas
- ✅ Formato universal

**Exemplo de uso**:
```bash
# Exportar horário do Professor em CSV
curl http://localhost:8000/api/v1/horarios/1/export/professor/3/csv > prof_joao.csv

# Abrir no Excel
open prof_joao.csv
```

**Formato do CSV**:
```csv
Horário,Segunda-feira,Terça-feira,Quarta-feira,Quinta-feira,Sexta-feira
07:30 - 08:20,Matemática - 3A (Sala 101),Física - 3B (Lab 1),-,-,Matemática - 3A (Sala 101)
08:20 - 09:10,-,-,Matemática - 3C (Sala 102),Física - 3A (Lab 1),-
...
```

### Diferenças por Público

#### Visualização por Turma
**Quem usa**: Alunos, coordenação, secretaria

**Informações exibidas**:
- Disciplina (destaque)
- Professor
- Ambiente (sala)

**Cor predominante**: Verde 🟢

#### Visualização por Professor  
**Quem usa**: Professores, recursos humanos

**Informações exibidas**:
- Disciplina (destaque)
- Turma
- Ambiente (sala)

**Cor predominante**: Amarelo 🟡

### Exemplos de Integração

#### JavaScript/TypeScript (Frontend)
```typescript
// Exportar e baixar HTML
async function exportarHorarioTurma(horarioId: number, turmaId: number) {
  const response = await fetch(
    `/api/v1/horarios/${horarioId}/export/turma/${turmaId}/html`
  );
  const html = await response.text();
  
  // Abrir em nova janela
  const win = window.open();
  win.document.write(html);
}

// Exportar e baixar CSV
async function downloadCSV(horarioId: number, professorId: number) {
  const response = await fetch(
    `/api/v1/horarios/${horarioId}/export/professor/${professorId}/csv`
  );
  const csv = await response.text();
  
  // Criar download
  const blob = new Blob([csv], { type: 'text/csv' });
  const url = window.URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `professor_${professorId}.csv`;
  a.click();
}
```

#### Python (Scripts)
```python
import requests

# Exportar horário
def exportar_horario_html(horario_id, turma_id):
    url = f"http://localhost:8000/api/v1/horarios/{horario_id}/export/turma/{turma_id}/html"
    response = requests.get(url)
    
    with open(f"turma_{turma_id}.html", "w", encoding="utf-8") as f:
        f.write(response.text)
    
    print(f"Horário exportado: turma_{turma_id}.html")

# Usar
exportar_horario_html(1, 5)
```

---

## 🔄 Fase de Refinamento

Após gerar o horário inicial, o sistema entra em uma **fase de refinamento** para melhorar a qualidade pedagógica.

### O que o Refinamento Faz

1. **Identifica dias sobrecarregados**: Detecta dias com muitas aulas seguidas
2. **Tenta redistribuir**: Move aulas para balancear a carga
3. **Recalcula qualidade**: Verifica se houve melhoria
4. **Mantém restrições**: Não viola nenhuma restrição obrigatória

### Quando é Ativado

- ✅ Apenas quando geração é **OPTIMAL** (solução ótima encontrada)
- ❌ Não ativa em soluções **FEASIBLE** (viáveis mas não ótimas)

### Exemplo de Refinamento

**Antes do Refinamento**:
```
Segunda: 8 aulas
Terça:   8 aulas
Quarta:  3 aulas  ← Dia muito leve
Quinta:  8 aulas
Sexta:   8 aulas
```

**Depois do Refinamento**:
```
Segunda: 7 aulas
Terça:   7 aulas
Quarta:  5 aulas  ← Melhor distribuído
Quinta:  7 aulas
Sexta:   7 aulas
```

**Resultado**: Score de qualidade aumenta de 82 para 88 🎉

---

## 📊 Resumo dos Endpoints

### Geração
```
POST /api/v1/horarios/{id}/gerar
```

### Visualização
```
GET /api/v1/horarios/{id}/turma/{turma_id}
GET /api/v1/horarios/{id}/professor/{professor_id}
```

### Exportação - HTML
```
GET /api/v1/horarios/{id}/export/turma/{turma_id}/html
GET /api/v1/horarios/{id}/export/professor/{professor_id}/html
```

### Exportação - CSV
```
GET /api/v1/horarios/{id}/export/turma/{turma_id}/csv
GET /api/v1/horarios/{id}/export/professor/{professor_id}/csv
```

---

## 🎯 Melhores Práticas

### Para Obter Melhor Score de Qualidade

1. **Evite bloqueios excessivos**: Quanto mais disponibilidade, melhor
2. **Distribua disciplinas**: Evite concentrar tudo em poucos professores
3. **Adicione ambientes**: Mais salas = mais flexibilidade
4. **Configure tempos realistas**: Deslocamento deve refletir realidade
5. **Balance carga horária**: Professores com carga similar

### Para Resolver Pendências Rapidamente

1. **Leia as sugestões**: Sistema indica exatamente o que fazer
2. **Priorize por severidade**: ALTA → MÉDIA → BAIXA
3. **Ajuste gradualmente**: Faça uma mudança por vez
4. **Teste após cada ajuste**: Gere novamente para validar

### Para Exportação Eficiente

1. **HTML para impressão**: Melhor visualização
2. **CSV para análise**: Manipulação de dados
3. **Salve versões**: Mantenha histórico de horários
4. **Compartilhe adequadamente**: Turmas com alunos, professores com RH

---

**Versão**: 1.0  
**Última atualização**: Fevereiro 2026  
**Autor**: Sistema Urânia - No Cry Baby
