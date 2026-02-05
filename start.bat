@echo off
echo ================================
echo   Iniciando Sistema Urania
echo ================================

REM Verificar Python
where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Python nao encontrado!
    pause
    exit /b 1
)

REM Verificar Node
where node >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Node.js nao encontrado!
    pause
    exit /b 1
)

echo Pre-requisitos verificados!

REM Iniciar Backend
echo.
echo Iniciando Backend FastAPI...
cd backend

REM Criar venv se nao existe
if not exist "venv\" (
    echo Criando ambiente virtual...
    python -m venv venv
)

REM Ativar venv
call venv\Scripts\activate.bat

REM Instalar dependencias se necessario
if not exist "venv\.installed" (
    echo Instalando dependencias do backend...
    pip install --upgrade pip
    pip install -r requirements.txt
    type nul > venv\.installed
)

REM Iniciar servidor
start "Urania Backend" cmd /k python main.py

echo Backend iniciado!

REM Aguardar backend
timeout /t 5 /nobreak

REM Iniciar Frontend
echo.
echo Iniciando Frontend Next.js...
cd ..\frontend

REM Instalar dependencias se necessario
if not exist "node_modules\" (
    echo Instalando dependencias do frontend...
    call npm install
)

REM Iniciar servidor
start "Urania Frontend" cmd /k npm run dev

echo Frontend iniciado!

echo.
echo ================================
echo   Sistema Urania Iniciado!
echo ================================
echo.
echo Backend API:     http://localhost:8000
echo Documentacao:    http://localhost:8000/docs
echo Frontend:        http://localhost:3000
echo.
echo Pressione qualquer tecla para encerrar...
pause >nul
