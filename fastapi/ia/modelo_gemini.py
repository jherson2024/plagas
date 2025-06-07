#/modelos_ia_evaluaciones/modelos/GeminiApi.py
from google import genai
from modules.modelos_ia_evaluaciones.claves.claves import claveGemini
client = genai.GenerativeModel(model_name="gemini-2.0-flash", api_key=claveGemini)
response = client.generate_content("Explain how AI works in a few words")
print(response.text)