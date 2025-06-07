// services/capturas.js
import axios from './axios'; // Usa la instancia personalizada de Axios

// ✅ Crear una nueva posición en un mapa
export const crearPosicion = async (mapCod, data) => {
  return axios.post(`/imagen_captura/mapas/${mapCod}/posiciones/`, data);
};

// ✅ Obtener todas las posiciones de un mapa
export const obtenerPosiciones = async (mapCod) => {
  return axios.get(`/imagen_captura/mapas/${mapCod}/posiciones/`);
};

// ✅ Subir una imagen de captura a una posición
export const subirFotoCaptura = async (posCod, archivo) => {
  const formData = new FormData();
  formData.append("archivo", archivo);

  return axios.post(`/imagen_captura/posiciones/${posCod}/fotos/`, formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });
};

// ✅ Ver todas las fotos de una posición
export const obtenerFotosCaptura = async (posCod) => {
  return axios.get(`/imagen_captura/posiciones/${posCod}/fotos/`);
};
export const obtenerMapa = async (mapCod) => {
  return axios.get(`/imagen_captura/mapas/${mapCod}`);
};
// 🗑️ Eliminar una posición del mapa
export const eliminarPosicion = async (posCod) => {
  return axios.delete(`/imagen_captura/posiciones/${posCod}/`);
};

// 🗑️ Eliminar una imagen de captura de una posición
export const eliminarFotoCaptura = async (fotoCod) => {
  return axios.delete(`/imagen_captura/fotos/${fotoCod}/`);
};