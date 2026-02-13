from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import engine, Base
from app.api.routes import (
    disciplinas,
    turmas,
    professores,
    sedes,
    ambientes,
    grades_curriculares,
    disponibilidades,
    horarios,
)

# Criar tabelas
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todas as origens (dev)
    allow_credentials=False,  # Desabilitar credentials para permitir *
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rotas
app.include_router(disciplinas.router, prefix=settings.API_V1_STR)
app.include_router(turmas.router, prefix=settings.API_V1_STR)
app.include_router(professores.router, prefix=settings.API_V1_STR)
app.include_router(sedes.router, prefix=settings.API_V1_STR)
app.include_router(ambientes.router, prefix=settings.API_V1_STR)
app.include_router(grades_curriculares.router, prefix=settings.API_V1_STR)
app.include_router(disponibilidades.router, prefix=settings.API_V1_STR)
app.include_router(horarios.router, prefix=settings.API_V1_STR)


@app.get("/")
def root():
    return {
        "message": "Bem-vindo ao Sistema No Cry Baby de Geração de Horários Escolares",
        "version": settings.VERSION,
        "docs": "/docs",
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
