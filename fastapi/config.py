# config.py

BACKEND_URL = "http://192.168.16.119:8000"
 # Cambia esto si usas un dominio real o puerto diferente
STATIC_URL = f"{BACKEND_URL}/static"

# Carpeta donde se guardan las imágenes de cultivos (dentro de /static)
IMAGEN_CULTIVO_PATH = "imagen_cultivo"
IMAGEN_CULTIVO_URL = f"{STATIC_URL}/{IMAGEN_CULTIVO_PATH}"
FOTO_PERFIL_PATH = "foto_perfil_usuario"
FOTO_PERFIL_URL = f"{STATIC_URL}/{FOTO_PERFIL_PATH}"