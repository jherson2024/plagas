# main.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from modules.usuarios_seguridad.routes import router as usuarios_seguridad_router
from modules.agricultura.routes import router as agricultura_router
from modules.asignaciones.routes import router as asignaciones_router
# y así sucesivamente con tus otras carpetas...
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # o especifica dominios como ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],  # Esto incluye OPTIONS, GET, POST, etc.
    allow_headers=["*"],
)
# Montar carpeta estática para imágenes
app.mount("/static", StaticFiles(directory="static"), name="static")

# Registrar rutas de cada módulo
app.include_router(usuarios_seguridad_router, prefix="/usuarios", tags=["Usuarios y Seguridad"])
app.include_router(agricultura_router, prefix="/agricultura", tags=["Agricultura"])
app.include_router(asignaciones_router, prefix="/asignaciones", tags=["Asignaciones"])
# Agrega aquí el resto de tus routers...

@app.get("/")
def read_root():
    return {"mensaje": "API funcionando"}
