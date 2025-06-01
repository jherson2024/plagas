import axios from './axios';

const BASE_URL = '/agricultura';

// ✅ Obtener parcelas por usuario
export const obtenerParcelas = (UsuCod) => {
  return axios.get(`${BASE_URL}/parcelas/usuario/${UsuCod}`);
};

// ✅ Crear parcela
export const crearParcela = (data) => {
  return axios.post(`${BASE_URL}/parcelas/`, {
    ...data,
    ParUsuCod: parseInt(data.ParUsuCod),
  });
};

// ✅ Actualizar parcela
export const actualizarParcela = (ParCod, data) => {
  return axios.put(`${BASE_URL}/parcelas/${ParCod}`, data);
};

// ✅ Eliminar parcela
export const eliminarParcela = (ParCod) => {
  return axios.delete(`${BASE_URL}/parcelas/${ParCod}`);
};

// ✅ (Opcional si lo agregas) Cambiar estado — debes tener este endpoint en backend si quieres usarlo
export const cambiarEstadoParcela = (ParCod, estado) => {
  return axios.patch(`${BASE_URL}/parcelas/${ParCod}/estado`, { ParEstReg: estado });
};

