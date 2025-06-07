from PIL import Image
from torchvision import transforms
import base64
import io
import os

# Transformaciones estándar para el modelo (ajusta si tu modelo necesita otras)
transformaciones = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor()
])

def cargar_imagen_desde_ruta(ruta_imagen: str) -> Image.Image:
    """Carga una imagen desde una ruta en disco."""
    if not os.path.exists(ruta_imagen):
        raise FileNotFoundError(f"No se encontró la imagen en: {ruta_imagen}")
    imagen = Image.open(ruta_imagen).convert("RGB")
    return imagen

def cargar_imagen_desde_base64(imagen_base64: str) -> Image.Image:
    """Carga una imagen desde un string en base64."""
    try:
        imagen_bytes = base64.b64decode(imagen_base64)
        imagen = Image.open(io.BytesIO(imagen_bytes)).convert("RGB")
        return imagen
    except Exception as e:
        raise ValueError("Base64 inválido o imagen corrupta") from e

def procesar_imagen(imagen: Image.Image):
    """Convierte una imagen PIL a un tensor listo para el modelo."""
    return transformaciones(imagen).unsqueeze(0)  # Batch de 1

def imagen_a_base64(ruta_imagen: str) -> str:
    """Convierte una imagen a base64 (opcionalmente útil para testing/API)."""
    with open(ruta_imagen, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")
