# config.py

BACKEND_URL = "http://localhost:8000"
 # Cambia esto si usas un dominio real o puerto diferente
STATIC_URL = f"{BACKEND_URL}/static"

# Carpeta donde se guardan las imágenes de cultivos (dentro de /static)
IMAGEN_CULTIVO_PATH = "imagen_cultivo"
IMAGEN_CULTIVO_URL = f"{STATIC_URL}/{IMAGEN_CULTIVO_PATH}"
FOTO_PERFIL_PATH = "foto_perfil_usuario"
FOTO_PERFIL_URL = f"{STATIC_URL}/{FOTO_PERFIL_PATH}"

IMAGEN_MAPA_PATH = "mapa"
IMAGEN_MAPA_URL = f"{STATIC_URL}/{IMAGEN_MAPA_PATH}"

ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://192.168.16.119:3000",
    "https://tudominio.com", 
    "https://10.7.123.95", 
    "http://10.7.123.95:3000",
]
