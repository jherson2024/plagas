import axios from './axios';

const BASE_URL = '/asignaciones';

const asignacionesService = {
  // 📌 ASIGNACIONES

  // Crear una nueva asignación
  crear: (data) => axios.post(`${BASE_URL}/`, data),

  // Obtener todas las asignaciones
  obtenerTodas: () => axios.get(`${BASE_URL}/`),

  // Obtener asignaciones por dueño (parcelas o cultivos del dueño)
  obtenerPorDueno: (duenoId) => axios.get(`${BASE_URL}/dueno/${duenoId}`),

  // Modificar una asignación por ID
  actualizar: (id, data) => axios.put(`${BASE_URL}/${id}`, data),

  // Cambiar estado de la asignación (A/I)
  cambiarEstado: (id, nuevoEstado) =>
    axios.patch(`${BASE_URL}/${id}/estado`, null, {
      params: { nuevo_estado: nuevoEstado }
    }),

  // Eliminar lógicamente (inactivar)
  eliminar: (id) => axios.delete(`${BASE_URL}/${id}`),

  // 📌 PARCELAS del usuario dueño
  obtenerParcelasPorDueno: (duenoId) => axios.get(`${BASE_URL}/parcelas/dueno/${duenoId}`),

  // 📌 CULTIVOS del usuario dueño
  obtenerCultivosPorDueno: (duenoId) => axios.get(`${BASE_URL}/cultivos/dueno/${duenoId}`),

  // 📌 ROLES disponibles
  obtenerRoles: () => axios.get(`${BASE_URL}/roles`),

  // 📌 Buscar usuarios por nombre, correo o nombre de usuario
  buscarUsuarios: (filtro) => axios.get(`${BASE_URL}/usuarios/buscar`, {
    params: { filtro }
  })
};

export default asignacionesService;
