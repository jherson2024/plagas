import { BASE_URL } from '../config/config';

const API_URL = `${BASE_URL}/usuario`;

/**
 * Inicia sesión con número de WhatsApp y contraseña.
 * Guarda el token JWT en localStorage si es exitoso.
 */
export async function loginUsuario({ UsuNumWha, UsuCon }) {
  const response = await fetch(`${API_URL}/login`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ UsuNumWha, UsuCon }),
  });

  const resultado = await response.json();

  if (!response.ok) {
    throw new Error(resultado.detail || 'Error al iniciar sesión');
  }

  // Guarda el token en localStorage
  localStorage.setItem('token', resultado.access_token);

  return resultado;
}

/**
 * Registra un nuevo usuario con nombre, número de WhatsApp y contraseña.
 */
export async function registrarUsuario({ UsuNom, UsuNumWha, UsuCon }) {
  const response = await fetch(`${API_URL}/registro`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ UsuNom, UsuNumWha, UsuCon }),
  });

  const resultado = await response.json();

  if (!response.ok) {
    throw new Error(resultado.detail || 'Error al registrar');
  }

  return resultado;
}

/**
 * Obtiene los datos del usuario autenticado usando el token JWT.
 */
export async function getUsuarioActual() {
  const token = localStorage.getItem('token');
  if (!token) throw new Error('No autenticado');

  const response = await fetch(`${API_URL}/actualizar`, {
    method: 'GET', // o crea un endpoint /me si prefieres
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  const resultado = await response.json();

  if (!response.ok) {
    throw new Error(resultado.detail || 'Error al obtener usuario');
  }

  return resultado;
}
