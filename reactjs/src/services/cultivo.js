import axios from './axios';
const BASE_URL = '/agricultura';
// ✅ Obtener cultivos por parcela o usuario (ajusta según tu backend)
export const obtenerCultivos = (UsuCod) => {
  return axios.get(`${BASE_URL}/cultivos/usuario/${UsuCod}`);
};
// ✅ Crear cultivo
export const crearCultivo = (data) => {
  const formData = new FormData();
  for (const key in data) {
    const value = data[key];
    if (
      value !== null &&
      value !== undefined &&
      value !== '' &&
      key !== 'CulUrlIma'
    ) {
      formData.append(key, value);
    }
  }
  if (data.CulUrlIma instanceof File) {
    formData.append('archivo', data.CulUrlIma);
  }
  return axios.post(`${BASE_URL}/cultivos`, formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
};
export const actualizarCultivo = (CulCod, data) => {
  const formData = new FormData();
  for (const key in data) {
    const value = data[key];
    if (
      value !== null &&
      value !== undefined &&
      value !== '' &&
      key !== 'CulUrlIma'
    ) {
      formData.append(key, value);
    }
  }
  if (data.CulUrlIma instanceof File) {
    formData.append('archivo', data.CulUrlIma);
  }
  return axios.put(`${BASE_URL}/cultivos/${CulCod}`, formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
};

// ✅ Eliminar cultivo (si lo manejas como eliminación lógica)
export const eliminarCultivo = (CulCod) => {
  return axios.delete(`${BASE_URL}/cultivos/${CulCod}`);
};
// ✅ Cambiar estado del cultivo (activo/inactivo/eliminado)
export const cambiarEstadoCultivo = (CulCod, estado) => {
  return axios.patch(`${BASE_URL}/cultivos/${CulCod}/estado`, {
    CulEstReg: estado,
  });
};
// ✅ Obtener solo código y nombre de parcelas por usuario
export const obtenerParcelasResumen = (UsuCod) => {
  return axios.get(`${BASE_URL}/parcelas/usuario/${UsuCod}/resumen`);
};
