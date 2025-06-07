import os

# Extensiones válidas de imágenes
EXTENSIONES_VALIDAS = {".jpg", ".jpeg", ".png", ".bmp"}

def es_extension_valida(ruta_imagen: str) -> bool:
    """Verifica si una imagen tiene una extensión válida."""
    _, ext = os.path.splitext(ruta_imagen.lower())
    return ext in EXTENSIONES_VALIDAS

def cargar_etiquetas_desde_txt(ruta: str) -> dict:
    """
    Carga etiquetas desde un archivo de texto con una clase por línea.
    Devuelve un diccionario {indice: nombre}
    """
    if not os.path.exists(ruta):
        raise FileNotFoundError(f"No se encontró el archivo de etiquetas: {ruta}")
    
    with open(ruta, "r", encoding="utf-8") as f:
        lineas = [line.strip() for line in f if line.strip()]
    
    return {i: nombre for i, nombre in enumerate(lineas)}

def formatear_prediccion(clase: int, confianza: float, etiquetas: dict) -> dict:
    """Devuelve la predicción en formato legible."""
    return {
        "clase": etiquetas.get(clase, f"Desconocida ({clase})"),
        "confianza": round(confianza * 100, 2)  # como porcentaje
    }

def normalizar_nombre_archivo(nombre: str) -> str:
    """Limpia un nombre de archivo (útil para guardar imágenes predichas)."""
    return nombre.strip().replace(" ", "_").lower()
