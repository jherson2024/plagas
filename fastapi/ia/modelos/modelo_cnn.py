import torch
from torchvision import transforms
from PIL import Image
import os
import io
import base64
# Comprobar si hay GPU
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# Cargar el modelo entrenado
modelo_path = os.path.join("modules", "ia", "modelos", "modelo_cnn.pt")
modelo = torch.load(modelo_path, map_location=device)
modelo.eval()
# Etiquetas de ejemplo (ajústalas a las reales de tu modelo)
CLASES = {
    0: "Sin plaga",
    1: "Pulgón",
    2: "Mosca blanca",
    3: "Trips",
    4: "Araña roja"
}
# Transformaciones de imagen
transformaciones = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])
def predecir_plaga_desde_ruta(ruta_imagen):
    try:
        imagen = Image.open(ruta_imagen).convert("RGB")
        tensor = transformaciones(imagen).unsqueeze(0).to(device)
        with torch.no_grad():
            salida = modelo(tensor)
            indice = torch.argmax(salida, dim=1).item()
            return {
                "clase": CLASES.get(indice, f"Clase desconocida: {indice}"),
                "confianza": torch.softmax(salida, dim=1)[0][indice].item()
            }
    except Exception as e:
        return {"error": f"Error al predecir: {str(e)}"}
def predecir_plaga_desde_base64(imagen_base64):
    try:
        imagen_bytes = base64.b64decode(imagen_base64)
        imagen = Image.open(io.BytesIO(imagen_bytes)).convert("RGB")
        tensor = transformaciones(imagen).unsqueeze(0).to(device)
        with torch.no_grad():
            salida = modelo(tensor)
            indice = torch.argmax(salida, dim=1).item()
            return {
                "clase": CLASES.get(indice, f"Clase desconocida: {indice}"),
                "confianza": torch.softmax(salida, dim=1)[0][indice].item()
            }
    except Exception as e:
        return {"error": f"Error al predecir desde base64: {str(e)}"}