// src/services/authService.js
import { BASE_URL } from '../config/config';

export async function loginUsuario(data) {
  const response = await fetch(`${BASE_URL}/usuarios/login`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  });

  const resultado = await response.json();

  if (!response.ok) {
    throw new Error(resultado.detail || 'Error al iniciar sesión');
  }

  return resultado;
}

export const registrarUsuario = async (usuario) => {
  const response = await fetch(`${BASE_URL}/usuarios/registro`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(usuario),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Error al registrar');
  }

  return await response.json();
};