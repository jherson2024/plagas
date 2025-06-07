import axios from 'axios';
import { BASE_URL } from '../config/config';

const API_URL = `${BASE_URL}/ia/analyze`;

export const analyzeImage = async (file) => {
  const formData = new FormData();
  formData.append('file', file);

  try {
    const response = await axios.post(API_URL, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data.result;
  } catch (error) {
    console.error("Error al analizar imagen:", error);
    return "❌ Error al analizar la imagen.";
  }
};
