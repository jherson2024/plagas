# main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import config  # Importa tu archivo de configuración

from modules.usuario.routes import router as usuario_router
from modules.mapa.routes import router as mapa_router
from modules.imagen_captura.routes import router as imagen_captura_router
from modules.ia.routes import router as ia_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=config.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Montar carpeta estática
app.mount("/static", StaticFiles(directory="static"), name="static")

# Incluir routers
app.include_router(usuario_router, prefix="/usuario", tags=["Usuario"])
app.include_router(mapa_router, prefix="/mapas", tags=["Mapa"])
app.include_router(imagen_captura_router, prefix="/imagen_captura", tags=["ImagenCaptura"])
app.include_router(ia_router, prefix="/ia", tags=["IA"])

@app.get("/")
def read_root():
    return {"mensaje": "API funcionando"}
