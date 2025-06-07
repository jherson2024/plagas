// src/services/usuario.js
import axios from './axios'; // Usa la instancia con interceptor

const API_URL = '/usuario'; // Ya está cubierto por baseURL

// ✅ Actualiza perfil del usuario autenticado
export const actualizarPerfil = async (data) => {
  return axios.put(`${API_URL}/actualizar`, data);
};

// ✅ Subir nueva imagen de perfil
export const subirFoto = async (archivo) => {
  const formData = new FormData();
  formData.append("archivo", archivo);

  const response = await axios.post(`${API_URL}/imagen-perfil`, formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });

  return response.data;
};

// ✅ Eliminar imagen de perfil
export const eliminarFoto = async () => {
  return axios.delete(`${API_URL}/imagen-perfil`);
};

// ✅ Cambiar contraseña
export const cambiarContrasena = async (datos) => {
  return axios.post(`${API_URL}/cambiar-contrasena`, datos);
};
