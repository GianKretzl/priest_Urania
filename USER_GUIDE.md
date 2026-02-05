# 📖 Guia do Usuário - Sistema Urânia

## Introdução

O Sistema Urânia é uma ferramenta completa para geração automática de horários escolares. Este guia irá ajudá-lo a utilizar todas as funcionalidades do sistema.

## 🎯 Fluxo de Trabalho Recomendado

### 1️⃣ Configuração Inicial

Antes de criar seu primeiro horário, siga esta ordem de cadastros:

#### Passo 1: Cadastrar Sedes
1. Acesse **Cadastros > Sedes**
2. Clique em **Nova Sede**
3. Preencha:
   - Nome da sede
   - Endereço completo
   - Cidade e Estado
4. Clique em **Salvar**

**Exemplo:**
```
Nome: Sede Central
Endereço: Rua das Flores, 123
Cidade: São Paulo
Estado: SP
CEP: 01234-567
```

#### Passo 2: Cadastrar Ambientes
1. Acesse **Cadastros > Ambientes**
2. Clique em **Novo Ambiente**
3. Preencha:
   - Nome (ex: Sala 101)
   - Código único (ex: S101)
   - Tipo (Sala de Aula, Laboratório, etc.)
   - Capacidade de alunos
   - Sede associada
4. Clique em **Salvar**

**Dica:** Cadastre todos os ambientes que serão usados: salas, laboratórios, quadras, etc.

#### Passo 3: Cadastrar Disciplinas
1. Acesse **Cadastros > Disciplinas**
2. Clique em **Nova Disciplina**
3. Preencha:
   - Código (ex: MAT101)
   - Nome (ex: Matemática)
   - Carga horária semanal (número de aulas por semana)
   - Duração da aula em minutos (normalmente 50)
   - Cor (para visualização)
4. Clique em **Salvar**

**Exemplo:**
```
Código: MAT101
Nome: Matemática
Carga Horária: 5 aulas/semana
Duração: 50 minutos
Cor: Azul (#3B82F6)
```

#### Passo 4: Cadastrar Turmas
1. Acesse **Cadastros > Turmas**
2. Clique em **Nova Turma**
3. Preencha:
   - Nome (ex: 9º A)
   - Ano/Série (ex: 9º Ano)
   - Turno (Matutino, Vespertino, Noturno)
   - Número de alunos
4. Clique em **Salvar**

#### Passo 5: Cadastrar Professores
1. Acesse **Cadastros > Professores**
2. Clique em **Novo Professor**
3. Preencha:
   - Nome completo
   - Email
   - Telefone e CPF (opcional)
   - Carga horária máxima (horas/semana)
   - Horas-atividade
   - Máximo de aulas seguidas
   - Máximo de aulas por dia
4. Clique em **Salvar**

**Exemplo:**
```
Nome: João da Silva
Email: joao.silva@escola.com
Carga Horária Máxima: 40h/semana
Horas-Atividade: 8h/semana
Máx. Aulas Seguidas: 4
Máx. Aulas por Dia: 6
```

#### Passo 6: Configurar Grade Curricular
1. Acesse **Cadastros > Grade Curricular**
2. Clique em **Nova Grade**
3. Selecione:
   - Turma
   - Disciplina
   - Professor
   - Número de aulas por semana
4. Clique em **Salvar**

**Importante:** Cada combinação Turma + Disciplina deve ter um professor atribuído.

#### Passo 7: Configurar Disponibilidade (Opcional)
1. Acesse **Cadastros > Disponibilidade**
2. Clique em **Nova Disponibilidade**
3. Selecione:
   - Professor
   - Dia da semana
   - Horário de início e fim
   - Disponível ou Indisponível
4. Clique em **Salvar**

**Exemplo de Uso:**
- Professor tem outro emprego às tarças das 14h às 18h
- Marque como "Indisponível" nesse período

### 2️⃣ Criando um Horário

#### Passo 1: Criar Novo Horário
1. Acesse **Horários**
2. Clique em **Novo Horário**
3. Preencha:
   - Nome (ex: "Horário 1º Semestre 2024")
   - Ano Letivo (ex: 2024)
   - Semestre (1 ou 2)
4. Clique em **Criar**

#### Passo 2: Revisar Dados
Antes de gerar, certifique-se de que:
- ✅ Todas as turmas têm grade curricular
- ✅ Todos os professores estão cadastrados
- ✅ Há ambientes suficientes
- ✅ Disponibilidades estão configuradas

#### Passo 3: Gerar Horário
1. Na lista de horários, clique em **Gerar**
2. Confirme a ação
3. Aguarde o processamento (pode levar alguns minutos)
4. Visualize o resultado com:
   - Total de aulas alocadas
   - Score de qualidade
   - Lista de pendências (se houver)

### 3️⃣ Visualizando o Horário

#### Por Turma
1. No horário gerado, clique em **Visualizar**
2. Selecione **Por Turma**
3. Escolha a turma desejada no dropdown
4. Visualize a grade completa da semana

#### Por Professor
1. No horário gerado, clique em **Visualizar**
2. Selecione **Por Professor**
3. Escolha o professor no dropdown
4. Visualize todos os horários do professor

### 4️⃣ Exportando Relatórios

1. Na visualização do horário, clique em **Exportar PDF**
2. O relatório será gerado automaticamente
3. Salve ou imprima conforme necessário

## 💡 Dicas e Boas Práticas

### Para Melhores Resultados

✅ **Configure disponibilidades realistas**
- Evite bloquear muitos horários
- Seja flexível quando possível

✅ **Distribua bem as disciplinas**
- Evite sobrecarregar um único professor
- Balance a carga horária

✅ **Tenha ambientes suficientes**
- Número de salas ≥ número de turmas simultâneas
- Considere laboratórios e espaços especiais

✅ **Revise a grade curricular**
- Verifique se não há duplicatas
- Confirme as cargas horárias

### Resolvendo Problemas Comuns

#### ❌ Problema: Horário não gerado completamente

**Causas possíveis:**
1. Professores com muitas indisponibilidades
2. Conflito de recursos (salas insuficientes)
3. Restrições muito rígidas

**Soluções:**
1. Revise as disponibilidades dos professores
2. Adicione mais ambientes
3. Aumente os limites de aulas seguidas
4. Redistribua professores na grade curricular

#### ❌ Problema: Score de qualidade baixo

**Significa:**
- Muitas "janelas" (horários vagos) entre aulas
- Distribuição não uniforme

**Soluções:**
1. Ajuste os horários de disponibilidade
2. Permita mais flexibilidade nos limites
3. Gere novamente para tentar outra combinação

#### ❌ Problema: Pendências reportadas

**O que fazer:**
1. Leia a mensagem de pendência
2. Ajuste o cadastro indicado
3. Gere o horário novamente

## 🔧 Manutenção do Sistema

### Backup Regular

Recomendamos fazer backup:
- Semanal: Durante cadastros
- Mensal: Após finalizar horários
- Semestral: Ao final de cada período

### Limpeza de Dados

Periodicamente:
1. Desative disciplinas não utilizadas
2. Marque professores inativos
3. Arquive turmas de anos anteriores
4. Limpe horários antigos

### Atualizações

Sempre que houver mudanças:
- ✏️ Atualize dados de professores
- ✏️ Revise grades curriculares
- ✏️ Ajuste disponibilidades
- ✏️ Adicione novos ambientes

## 📞 Suporte

### Documentação Adicional

- **README.md**: Visão geral do sistema
- **INSTALLATION.md**: Guia de instalação
- **API Docs**: http://localhost:8000/docs

### Solução de Problemas

1. Consulte a seção Troubleshooting
2. Verifique os logs do sistema
3. Entre em contato com suporte técnico

## 🎓 Glossário

- **Grade Curricular**: Associação entre turma, disciplina e professor
- **Janela**: Horário vago entre aulas de um professor
- **Horas-Atividade**: Tempo reservado para atividades fora de sala
- **Score de Qualidade**: Métrica de 0-100 da qualidade do horário gerado
- **Pendência**: Restrição que não pode ser satisfeita no horário atual

---

**Versão do Guia:** 1.0  
**Última Atualização:** 2026
