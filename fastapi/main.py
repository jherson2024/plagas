# main.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from modules.usuarios_seguridad.routes import router as usuarios_seguridad_router
# y así sucesivamente con tus otras carpetas...

app = FastAPI()

# Montar carpeta estática para imágenes
app.mount("/static", StaticFiles(directory="static"), name="static")

# Registrar rutas de cada módulo
app.include_router(usuarios_seguridad_router, prefix="/usuarios", tags=["Usuarios y Seguridad"])
# Agrega aquí el resto de tus routers...

@app.get("/")
def read_root():
    return {"mensaje": "API funcionando"}
