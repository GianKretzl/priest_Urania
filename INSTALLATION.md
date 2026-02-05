# 🚀 Guia de Instalação e Execução - Sistema No Cry Baby

Este guia fornece instruções detalhadas para configurar e executar o sistema de geração de horários escolares.

## 📋 Sumário

1. [Pré-requisitos](#pré-requisitos)
2. [Instalação do Backend](#instalação-do-backend)
3. [Instalação do Frontend](#instalação-do-frontend)
4. [Configuração do Banco de Dados](#configuração-do-banco-de-dados)
5. [Executando o Sistema](#executando-o-sistema)
6. [Testes](#testes)
7. [Troubleshooting](#troubleshooting)

## 🔧 Pré-requisitos

Antes de começar, certifique-se de ter instalado:

### Software Necessário

- **Python 3.9 ou superior**
  ```bash
  python --version  # Deve mostrar 3.9 ou superior
  ```

- **Node.js 18 ou superior**
  ```bash
  node --version  # Deve mostrar v18 ou superior
  npm --version   # Gerenciador de pacotes
  ```

- **Git**
  ```bash
  git --version
  ```

### Opcional (mas recomendado)

- **PostgreSQL 13+** (para produção)
- **Docker** (para desenvolvimento)

## 🐍 Instalação do Backend

### 1. Clone o Repositório

```bash
git clone https://github.com/seu-usuario/priest_Urania.git
cd priest_Urania
```

### 2. Crie um Ambiente Virtual

#### Linux/Mac:
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
```

#### Windows:
```bash
cd backend
python -m venv venv
venv\Scripts\activate
```

Você saberá que o ambiente virtual está ativo quando ver `(venv)` no início do prompt.

### 3. Instale as Dependências

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Nota**: A instalação do OR-Tools pode levar alguns minutos.

### 4. Configure as Variáveis de Ambiente

```bash
# Copie o arquivo de exemplo
cp .env.example .env

# Edite o arquivo .env com suas configurações
nano .env  # ou use seu editor preferido
```

Exemplo de `.env`:
```env
DATABASE_URL=sqlite:///./nocrybaby.db
SECRET_KEY=sua-chave-secreta-super-segura-mude-em-producao
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Para PostgreSQL:
```env
DATABASE_URL=postgresql://usuario:senha@localhost:5432/nocrybaby_db
```

### 5. Inicialize o Banco de Dados

O banco será criado automaticamente na primeira execução se você estiver usando SQLite.

Para PostgreSQL, primeiro crie o banco:
```sql
CREATE DATABASE nocrybaby_db;
```

### 6. Teste o Backend

```bash
python main.py
```

Se tudo estiver correto, você verá:
```
INFO:     Started server process [xxxxx]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

Acesse `http://localhost:8000/docs` para ver a documentação da API.

## 🎨 Instalação do Frontend

### 1. Entre no Diretório do Frontend

```bash
# Se ainda estiver no backend:
cd ../frontend

# Ou do diretório raiz:
cd frontend
```

### 2. Instale as Dependências

#### Usando npm:
```bash
npm install
```

#### Usando yarn:
```bash
yarn install
```

**Nota**: A primeira instalação pode levar alguns minutos.

### 3. Configure as Variáveis de Ambiente

Crie um arquivo `.env.local`:
```bash
echo "API_URL=http://localhost:8000/api/v1" > .env.local
```

### 4. Teste o Frontend

```bash
npm run dev
# ou
yarn dev
```

Se tudo estiver correto, você verá:
```
ready - started server on 0.0.0.0:3000, url: http://localhost:3000
```

Acesse `http://localhost:3000` no navegador.

## 💾 Configuração do Banco de Dados

### Opção 1: SQLite (Desenvolvimento)

**Vantagens**: Configuração zero, arquivo único
**Desvantagens**: Performance limitada

Já configurado por padrão! Nenhuma ação necessária.

### Opção 2: PostgreSQL (Produção)

#### Instalação do PostgreSQL

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
```

**macOS (Homebrew):**
```bash
brew install postgresql
brew services start postgresql
```

**Windows:**
Baixe e instale de: https://www.postgresql.org/download/windows/

#### Criar Banco de Dados

```bash
# Entrar no PostgreSQL
sudo -u postgres psql

# Criar usuário e banco
CREATE USER nocrybaby_user WITH PASSWORD 'sua_senha_segura';
CREATE DATABASE nocrybaby_db OWNER nocrybaby_user;
GRANT ALL PRIVILEGES ON DATABASE nocrybaby_db TO nocrybaby_user;
\q
```

#### Atualizar .env

```env
DATABASE_URL=postgresql://nocrybaby_user:sua_senha_segura@localhost:5432/nocrybaby_db
```

#### Instalar Driver do PostgreSQL

```bash
pip install psycopg2-binary
```

### Opção 3: Docker (Recomendado)

Crie um arquivo `docker-compose.yml`:

```yaml
version: '3.8'

services:
  db:
    image: postgres:15
    environment:
      POSTGRES_USER: nocrybaby_user
      POSTGRES_PASSWORD: nocrybaby_pass
      POSTGRES_DB: nocrybaby_db
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

Execute:
```bash
docker-compose up -d
```

## 🚀 Executando o Sistema

### Desenvolvimento (Modo Manual)

#### Terminal 1 - Backend:
```bash
cd backend
source venv/bin/activate  # ou venv\Scripts\activate no Windows
python main.py
```

#### Terminal 2 - Frontend:
```bash
cd frontend
npm run dev
```

### Desenvolvimento (Script Único)

Crie um arquivo `start.sh` (Linux/Mac):
```bash
#!/bin/bash

# Inicia o backend
cd backend
source venv/bin/activate
python main.py &
BACKEND_PID=$!

# Inicia o frontend
cd ../frontend
npm run dev &
FRONTEND_PID=$!

# Aguarda Ctrl+C
trap "kill $BACKEND_PID $FRONTEND_PID" EXIT
wait
```

Execute:
```bash
chmod +x start.sh
./start.sh
```

### Produção

#### Backend com Gunicorn:
```bash
cd backend
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

#### Frontend - Build para Produção:
```bash
cd frontend
npm run build
npm start
```

## 🧪 Testes

### Backend

```bash
cd backend
pytest  # Quando os testes forem implementados
```

### Frontend

```bash
cd frontend
npm run test  # Quando os testes forem implementados
```

## ❗ Troubleshooting

### Problema: Porta já em uso

**Erro**: `Address already in use`

**Solução**:
```bash
# Encontrar e matar processo na porta 8000
lsof -ti:8000 | xargs kill -9

# Ou na porta 3000
lsof -ti:3000 | xargs kill -9
```

### Problema: Módulo não encontrado

**Erro**: `ModuleNotFoundError: No module named 'X'`

**Solução**:
```bash
# Backend
cd backend
source venv/bin/activate
pip install -r requirements.txt

# Frontend
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### Problema: Erro de permissão no PostgreSQL

**Erro**: `FATAL: role "user" does not exist`

**Solução**:
```bash
sudo -u postgres createuser -s seu_usuario
```

### Problema: OR-Tools não instala

**Erro durante instalação do OR-Tools**

**Solução**:
```bash
# Certifique-se de ter pip atualizado
pip install --upgrade pip

# Instale dependências de build
# Ubuntu/Debian:
sudo apt install build-essential python3-dev

# macOS:
xcode-select --install

# Tente novamente
pip install ortools
```

### Problema: CORS no navegador

**Erro**: `CORS policy: No 'Access-Control-Allow-Origin'`

**Solução**: Verifique se o backend está configurado corretamente no `main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Problema: Geração de horário muito lenta

**Sintoma**: Gerar horário demora muito ou trava

**Causas possíveis**:
1. Muitas restrições conflitantes
2. Grade curricular muito complexa
3. Tempo limite muito baixo

**Soluções**:
1. Simplificar restrições inicialmente
2. Aumentar `tempo_maximo_geracao` para 600 segundos
3. Verificar se não há conflitos nos cadastros

## 📊 Verificação de Instalação

Execute estes comandos para verificar se tudo está funcionando:

### Backend:
```bash
cd backend
source venv/bin/activate
python -c "from app.scheduler.generator import HorarioGenerator; print('✅ Backend OK')"
```

### Frontend:
```bash
cd frontend
npm run build && echo "✅ Frontend OK"
```

## 🎯 Próximos Passos

Após a instalação bem-sucedida:

1. ✅ Acesse o frontend em `http://localhost:3000`
2. ✅ Cadastre uma sede
3. ✅ Cadastre ambientes (salas)
4. ✅ Cadastre disciplinas
5. ✅ Cadastre turmas
6. ✅ Cadastre professores
7. ✅ Configure a grade curricular
8. ✅ Crie um horário
9. ✅ Gere o horário automaticamente
10. ✅ Visualize e exporte!

## 📞 Suporte

Se você encontrar problemas não listados aqui:

1. Verifique os logs no terminal
2. Consulte a documentação da API em `/docs`
3. Abra uma issue no GitHub
4. Entre em contato via email

---

**Boa sorte! 🚀**
