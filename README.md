# 🎓 Urânia - Sistema de Geração de Horários Escolares

Sistema completo de geração automática de horários escolares, similar ao sistema Urânia comercial, desenvolvido com **FastAPI** (backend) e **Next.js + Tailwind CSS** (frontend).

![Status](https://img.shields.io/badge/status-active-success.svg)
![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![Next.js](https://img.shields.io/badge/next.js-14.0-black.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## 📋 Índice

- [Sobre o Projeto](#sobre-o-projeto)
- [Funcionalidades](#funcionalidades)
- [Tecnologias](#tecnologias)
- [Instalação](#instalação)
- [Uso](#uso)
- [Arquitetura](#arquitetura)
- [API](#api)
- [Contribuindo](#contribuindo)
- [Licença](#licença)

## 🎯 Sobre o Projeto

O **Urânia** é um sistema completo para geração automática de horários escolares que utiliza algoritmos de otimização para criar grades horárias respeitando diversas restrições, como:

- ✅ Disponibilidade de professores
- ✅ Capacidade de salas
- ✅ Limites de aulas consecutivas
- ✅ Minimização de "janelas" (horários vagos)
- ✅ Deslocamento entre sedes
- ✅ Horas-atividade dos professores

## ⭐ Funcionalidades

### 1. Cadastros (Entradas de Dados)

- **Disciplinas**: Gerenciamento de matérias com carga horária
- **Turmas**: Divisão por ano/série e turno (matutino, vespertino, noturno)
- **Professores**: Cadastro com especialidades e restrições
- **Sedes e Ambientes**: Gerenciamento de locais físicos (salas, quadras, laboratórios)
- **Grade Curricular**: Definição de disciplinas por turma e professor

### 2. Regras e Restrições

- **Disponibilidade do Professor**: Bloqueio de horários específicos
- **Redução de Janelas**: Minimização de horários vagos
- **Horas-Atividade**: Controle de tempo para atividades extras
- **Limites de Aulas**: Máximo de aulas seguidas e por dia
- **Deslocamento**: Tempo de viagem entre sedes

### 3. Motor de Geração

- Algorithm de programação com restrições (CP-SAT)
- Otimização automática de milhares de combinações
- Identificação e resolução de pendências
- Refinamento para melhor qualidade pedagógica
- Score de qualidade (0-100)

### 4. Visualização e Relatórios

- Visualização por turma
- Visualização por professor
- Exportação em PDF, HTML e planilhas
- Dashboard com estatísticas

## 🚀 Tecnologias

### Backend (FastAPI)

- **Python 3.9+**
- **FastAPI** - Framework web moderno e rápido
- **SQLAlchemy** - ORM para banco de dados
- **OR-Tools** - Biblioteca do Google para otimização
- **Pydantic** - Validação de dados
- **PostgreSQL/SQLite** - Banco de dados

### Frontend (Next.js)

- **Next.js 14** - Framework React com Server Side Rendering
- **TypeScript** - Tipagem estática
- **Tailwind CSS** - Framework CSS utilitário
- **Axios** - Cliente HTTP
- **React Icons** - Ícones
- **jsPDF** - Geração de PDFs

## 📦 Instalação

### Pré-requisitos

- Python 3.9 ou superior
- Node.js 18 ou superior
- npm ou yarn
- Git

### Backend

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/priest_Urania.git
cd priest_Urania

# Entre no diretório do backend
cd backend

# Crie um ambiente virtual
python -m venv venv

# Ative o ambiente virtual
# Linux/Mac:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Instale as dependências
pip install -r requirements.txt

# Configure as variáveis de ambiente
cp .env.example .env
# Edite o arquivo .env com suas configurações

# Execute as migrações (se necessário)
# alembic upgrade head

# Inicie o servidor
python main.py
```

O backend estará disponível em `http://localhost:8000`

### Frontend

```bash
# Entre no diretório do frontend
cd ../frontend

# Instale as dependências
npm install
# ou
yarn install

# Inicie o servidor de desenvolvimento
npm run dev
# ou
yarn dev
```

O frontend estará disponível em `http://localhost:3000`

## 💻 Uso

### 1. Acessar o Sistema

Abra seu navegador e acesse `http://localhost:3000`

### 2. Realizar Cadastros

Antes de gerar um horário, é necessário cadastrar:

1. **Sedes** - Cadastre as unidades escolares
2. **Ambientes** - Cadastre salas, laboratórios, quadras, etc.
3. **Disciplinas** - Cadastre as matérias
4. **Turmas** - Cadastre as turmas/anos
5. **Professores** - Cadastre os professores
6. **Grade Curricular** - Associe disciplinas, turmas e professores
7. **Disponibilidade** (opcional) - Configure horários de indisponibilidade

### 3. Criar um Horário

1. Acesse **Horários** no menu
2. Clique em **Novo Horário**
3. Preencha os dados (nome, ano letivo, semestre)
4. Clique em **Criar**

### 4. Gerar o Horário

1. Na lista de horários, clique em **Gerar**
2. Aguarde o processamento (pode levar alguns minutos)
3. Visualize o resultado e o score de qualidade
4. Se houver pendências, ajuste os cadastros e gere novamente

### 5. Visualizar e Exportar

- Clique em **Visualizar** para ver o horário
- Alterne entre visualização por turma ou por professor
- Exporte para PDF clicando em **Exportar PDF**

## 🏗️ Arquitetura

### Estrutura de Diretórios

```
priest_Urania/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── routes/          # Rotas da API
│   │   ├── core/                # Configurações
│   │   ├── models/              # Modelos SQLAlchemy
│   │   ├── schemas/             # Schemas Pydantic
│   │   └── scheduler/           # Motor de geração
│   ├── requirements.txt
│   └── main.py
├── frontend/
│   ├── app/                     # Páginas Next.js
│   │   ├── cadastros/
│   │   ├── horarios/
│   │   └── relatorios/
│   ├── components/              # Componentes React
│   ├── lib/                     # Utilitários e API
│   ├── package.json
│   └── next.config.js
└── README.md
```

### Fluxo de Dados

```
Frontend (Next.js) <-> API REST (FastAPI) <-> Database (PostgreSQL/SQLite)
                                    |
                            Scheduler Engine
                          (OR-Tools CP-SAT)
```

## 📚 API

A documentação interativa da API está disponível em:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

### Principais Endpoints

#### Disciplinas
- `GET /api/v1/disciplinas` - Listar todas
- `POST /api/v1/disciplinas` - Criar nova
- `PUT /api/v1/disciplinas/{id}` - Atualizar
- `DELETE /api/v1/disciplinas/{id}` - Deletar

#### Turmas
- `GET /api/v1/turmas` - Listar todas
- `POST /api/v1/turmas` - Criar nova
- `PUT /api/v1/turmas/{id}` - Atualizar
- `DELETE /api/v1/turmas/{id}` - Deletar

#### Professores
- `GET /api/v1/professores` - Listar todos
- `POST /api/v1/professores` - Criar novo
- `PUT /api/v1/professores/{id}` - Atualizar
- `DELETE /api/v1/professores/{id}` - Deletar

#### Horários
- `GET /api/v1/horarios` - Listar todos
- `POST /api/v1/horarios` - Criar novo
- `POST /api/v1/horarios/{id}/gerar` - **Gerar horário automaticamente**
- `GET /api/v1/horarios/{id}/aulas` - Listar aulas do horário
- `GET /api/v1/horarios/{id}/turma/{turma_id}` - Aulas por turma
- `GET /api/v1/horarios/{id}/professor/{professor_id}` - Aulas por professor

## 🎲 Algoritmo de Geração

O sistema utiliza o **CP-SAT Solver** do Google OR-Tools, que implementa:

1. **Modelagem como CSP** (Constraint Satisfaction Problem)
2. **Variáveis booleanas** para cada possível alocação de aula
3. **Restrições fortes** (hard constraints):
   - Uma aula por vez por turma
   - Uma aula por vez por professor
   - Uma aula por vez por ambiente
   - Respeitar disponibilidade

4. **Restrições fracas** (soft constraints / objetivos):
   - Minimizar janelas entre aulas
   - Distribuir uniformemente ao longo da semana
   - Respeitar preferências

5. **Otimização** para encontrar a melhor solução possível

## 🤝 Contribuindo

Contribuições são bem-vindas! Por favor, siga estes passos:

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 👥 Autores

- **Seu Nome** - *Desenvolvimento Inicial*

## 🙏 Agradecimentos

- Sistema inspirado no [Urânia Horários](https://horario.com.br/)
- Google OR-Tools pela excelente biblioteca de otimização
- Comunidade FastAPI e Next.js

## 📞 Contato

- Email: seu-email@example.com
- LinkedIn: [Seu Perfil](https://linkedin.com/in/seu-perfil)
- Website: [Seu Site](https://seu-site.com)

---

**Desenvolvido com ❤️ usando FastAPI e Next.js**
