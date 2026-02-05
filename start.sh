#!/bin/bash

echo "🎓 Iniciando Sistema No Cry Baby..."
echo "================================"

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Verificar se Python está instalado
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 não está instalado${NC}"
    exit 1
fi

# Verificar se Node está instalado
if ! command -v node &> /dev/null; then
    echo -e "${RED}❌ Node.js não está instalado${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Pré-requisitos verificados${NC}"

# Função para cleanup
cleanup() {
    echo -e "\n${YELLOW}🛑 Encerrando serviços...${NC}"
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    exit 0
}

trap cleanup SIGINT SIGTERM

# Iniciar Backend
echo -e "\n${YELLOW}🚀 Iniciando Backend FastAPI...${NC}"
cd backend

# Verificar se venv existe
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}📦 Criando ambiente virtual...${NC}"
    python3 -m venv venv
fi

# Ativar venv
source venv/bin/activate

# Instalar dependências se necessário
if [ ! -f "venv/.installed" ]; then
    echo -e "${YELLOW}📥 Instalando dependências do backend...${NC}"
    pip install --upgrade pip
    pip install -r requirements.txt
    touch venv/.installed
fi

# Iniciar servidor FastAPI
python main.py &
BACKEND_PID=$!

echo -e "${GREEN}✅ Backend iniciado (PID: $BACKEND_PID)${NC}"

# Aguardar backend estar pronto
echo -e "${YELLOW}⏳ Aguardando backend estar pronto...${NC}"
sleep 5

# Iniciar Frontend
echo -e "\n${YELLOW}🚀 Iniciando Frontend Next.js...${NC}"
cd ../frontend

# Instalar dependências se necessário
if [ ! -d "node_modules" ]; then
    echo -e "${YELLOW}📥 Instalando dependências do frontend...${NC}"
    npm install
fi

# Iniciar servidor Next.js
npm run dev &
FRONTEND_PID=$!

echo -e "${GREEN}✅ Frontend iniciado (PID: $FRONTEND_PID)${NC}"

# Informações de acesso
echo -e "\n${GREEN}================================${NC}"
echo -e "${GREEN}✨ Sistema Urânia Iniciado!${NC}"
echo -e "${GREEN}================================${NC}"
echo -e "\n📊 ${YELLOW}Backend API:${NC}     http://localhost:8000"
echo -e "📚 ${YELLOW}Documentação:${NC}   http://localhost:8000/docs"
echo -e "🌐 ${YELLOW}Frontend:${NC}       http://localhost:3000"
echo -e "\n${YELLOW}Pressione Ctrl+C para encerrar${NC}\n"

# Aguardar
wait $BACKEND_PID $FRONTEND_PID
