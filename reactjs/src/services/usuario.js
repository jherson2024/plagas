import axios from 'axios';
import { BASE_URL } from '../config/config';
const API_URL = `${BASE_URL}/usuarios`;
/**
 * Actualiza los datos del perfil del usuario
 */
export const actualizarPerfil = (id, data) => {
  return axios.put(`${API_URL}/${id}`, data);
};
/**
 * Sube una nueva foto de perfil
 */
export const subirFoto = async (id, archivo) => {
  const formData = new FormData();
  formData.append("archivo", archivo);

  const response = await axios.post(`${API_URL}/${id}/imagen-perfil`, formData);

  // ❌ NO usar getFotoPerfilUrl aquí
  return response.data; // { foto_perfil: "archivo.webp" }
};
/**
 * Elimina la foto de perfil del usuario
 */
export const eliminarFoto = (id) => {
  return axios.delete(`${API_URL}/${id}/imagen-perfil`);
};

/**
 * Cambia la contraseña del usuario autenticado
 * @param {Object} datos - Contiene `password_actual` y `nueva_password`
 */
export const cambiarContrasena = async (datos, UsuCod) => {
  const token = localStorage.getItem("token");

  if (!token) {
    throw new Error("Token no encontrado. El usuario no está autenticado.");
  }

  const response = await axios.post(
    `${API_URL}/${UsuCod}/cambiar-contrasena`,
    datos,
    {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    }
  );

  return response.data;
};


