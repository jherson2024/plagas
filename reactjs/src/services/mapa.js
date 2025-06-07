//services/mapa.js
import axios from 'axios';
import { BASE_URL } from '../config/config';
const API_URL = `${BASE_URL}/mapas`;

const authHeaders = () => {
  const token = localStorage.getItem("token");
  if (!token) throw new Error("No autenticado");
  return {
    Authorization: `Bearer ${token}`,
  };
};

// ✅ Crear un nuevo mapa
export const crearMapa = async (data) => {
  return axios.post(`${API_URL}/`, data, {
    headers: authHeaders(),
  });
};

// ✅ Obtener todos los mapas del usuario
export const obtenerMapas = async () => {
  return axios.get(`${API_URL}/`, {
    headers: authHeaders(),
  });
};

// ✅ Ver un solo mapa por ID
export const verMapa = async (mapCod) => {
  return axios.get(`${API_URL}/${mapCod}`, {
    headers: authHeaders(),
  });
};

// ✅ Editar un mapa existente
export const editarMapa = async (mapCod, data) => {
  return axios.put(`${API_URL}/${mapCod}`, data, {
    headers: authHeaders(),
  });
};

// ✅ Eliminar un mapa
export const eliminarMapa = async (mapCod) => {
  return axios.delete(`${API_URL}/${mapCod}`, {
    headers: authHeaders(),
  });
};

// ✅ Subir imagen de mapa
export const subirImagenMapa = async (mapCod, archivo) => {
  const formData = new FormData();
  formData.append("archivo", archivo);

  return axios.post(`${API_URL}/${mapCod}/imagen`, formData, {
    headers: {
      ...authHeaders(),
      "Content-Type": "multipart/form-data",
    },
  });
};

// ✅ Eliminar imagen del mapa
export const eliminarImagenMapa = async (mapCod) => {
  return axios.delete(`${API_URL}/${mapCod}/imagen`, {
    headers: authHeaders(),
  });
};
