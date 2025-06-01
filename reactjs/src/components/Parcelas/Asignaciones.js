import { useEffect, useState } from 'react';
import { useAuth } from '../../context/AuthContext';
import asignacionesService from '../../services/asignaciones';
import './Asignaciones.css'

const Asignaciones = () => {
  const { usuario } = useAuth(); // contiene datos del usuario logueado
  const [parcelas, setParcelas] = useState([]);
  const [cultivos, setCultivos] = useState([]);
  const [roles, setRoles] = useState([]);
  const [usuariosEncontrados, setUsuariosEncontrados] = useState([]);
  const [asignaciones, setAsignaciones] = useState([]);
  const [form, setForm] = useState({
    usuarioId: '',
    rolId: '',
    parcelaId: '',
    cultivoId: ''
  });

  // Cargar parcelas, cultivos y roles al iniciar
  useEffect(() => {
    const cargarDatos = async () => {
      const [parcelasRes, cultivosRes, rolesRes,asignacionesRes] = await Promise.all([
        asignacionesService.obtenerParcelasPorDueno(usuario.UsuCod),
        asignacionesService.obtenerCultivosPorDueno(usuario.UsuCod),
        asignacionesService.obtenerRoles(),
        asignacionesService.obtenerPorDueno(usuario.UsuCod) 
      ]);
      setParcelas(parcelasRes.data);
      setCultivos(cultivosRes.data);
      setRoles(rolesRes.data);
      setAsignaciones(asignacionesRes.data);
    };

    cargarDatos();
  }, [usuario.UsuCod]);

  const handleBuscarUsuarios = async (e) => {
    const filtro = e.target.value;
    if (filtro.length >= 2) {
      const res = await asignacionesService.buscarUsuarios(filtro);
      setUsuariosEncontrados(res.data);
    } else {
      setUsuariosEncontrados([]);
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm({ ...form, [name]: value });

    // Si se selecciona parcela, se limpia cultivo (mutuamente excluyentes)
    if (name === 'parcelaId' && value) {
      setForm(prev => ({ ...prev, cultivoId: '' }));
    }
    if (name === 'cultivoId' && value) {
      setForm(prev => ({ ...prev, parcelaId: '' }));
    }
  };

  const handleAsignar = async () => {
    try {
      if (!form.usuarioId || !form.rolId || (!form.parcelaId && !form.cultivoId)) {
        alert('Complete todos los campos obligatorios.');
        return;
      }

      const payload = {
        AsiUsuCod: parseInt(form.usuarioId),
        AsiRolCod: parseInt(form.rolId),
        AsiFecAsi: new Date().toISOString().split('T')[0], // fecha actual
        AsiParCod: form.parcelaId ? parseInt(form.parcelaId) : null,
        AsiCulCod: form.cultivoId ? parseInt(form.cultivoId) : null
      };

      await asignacionesService.crear(payload);
      const nuevasAsignaciones = await asignacionesService.obtenerPorDueno(usuario.UsuCod);
setAsignaciones(nuevasAsignaciones.data);
      alert('Asignación realizada con éxito.');
      setForm({ usuarioId: '', rolId: '', parcelaId: '', cultivoId: '' });
    } catch (error) {
      console.error(error);
      alert('Error al asignar rol.');
    }
  };
  const cambiarEstado = async (asignacion) => {
  const nuevoEstado = asignacion.AsiEstReg === 'A' ? 'I' : 'A';
  try {
    await asignacionesService.cambiarEstado(asignacion.AsiCod, nuevoEstado);
    const res = await asignacionesService.obtenerPorDueno(usuario.UsuCod);
    setAsignaciones(res.data);
  } catch (err) {
    console.error(err);
    alert('Error al cambiar el estado.');
  }
};

const eliminarAsignacion = async (id) => {
  if (!window.confirm('¿Estás seguro de eliminar esta asignación?')) return;
  try {
    await asignacionesService.eliminar(id);
    const res = await asignacionesService.obtenerPorDueno(usuario.UsuCod);
    setAsignaciones(res.data);
  } catch (err) {
    console.error(err);
    alert('Error al eliminar la asignación.');
  }
};

  return (
    <div className="asignaciones">
      <div>
        <label>Buscar usuario (nombre, correo, usuario):</label>
        <input type="text" onChange={handleBuscarUsuarios} placeholder="ej. juan, juan@mail.com" />
        <select name="usuarioId" value={form.usuarioId} onChange={handleChange}>
          <option value="">Seleccione un usuario</option>
          {usuariosEncontrados.map((u) => (
            <option key={u.UsuCod} value={u.UsuCod}>{u.UsuNom} ({u.UsuEma})</option>
          ))}
        </select>
      </div>

      <div>
        <label>Rol:</label>
        <select name="rolId" value={form.rolId} onChange={handleChange}>
          <option value="">Seleccione un rol</option>
          {roles.map((r) => (
            <option key={r.RolCod} value={r.RolCod}>{r.RolNom}</option>
          ))}
        </select>
      </div>

      <div>
        <label>Parcela (si aplica):</label>
        <select name="parcelaId" value={form.parcelaId} onChange={handleChange}>
          <option value="">-- Ninguna --</option>
          {parcelas.map((p) => (
            <option key={p.ParCod} value={p.ParCod}>{p.ParNom}</option>
          ))}
        </select>
      </div>

      <div>
        <label>Cultivo (si aplica):</label>
        <select name="cultivoId" value={form.cultivoId} onChange={handleChange}>
          <option value="">-- Ninguno --</option>
          {cultivos.map((c) => (
            <option key={c.CulCod} value={c.CulCod}>{c.CulNom}</option>
          ))}
        </select>
      </div>

      <button onClick={handleAsignar}>Asignar Rol</button>
    {parcelas.map((parcela) => {
  const asignacionesParcela = asignaciones.filter(a => a.parcela?.ParCod === parcela.ParCod);

  return (
    <div key={`parcela-${parcela.ParCod}`} className="asignaciones-bloque">
      <h3 className="parcela">🧱 Parcela: {parcela.ParNom}</h3>
      <table className="asignaciones-table">
        <thead>
          <tr>
            <th>Usuario</th>
            <th>Rol</th>
            <th>Fecha</th>
            <th>Estado</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          {asignacionesParcela.length === 0 ? (
            <tr>
              <td colSpan="5">Sin asignaciones para esta parcela</td>
            </tr>
          ) : (
            asignacionesParcela.map((a) => (
              <tr key={a.AsiCod}>
                <td>{a.usuario?.UsuNom || `ID: ${a.AsiUsuCod}`}</td>
                <td>{a.rol?.RolNom || `ID: ${a.AsiRolCod}`}</td>
                <td>{new Date(a.AsiFecAsi).toLocaleDateString()}</td>
                <td style={{ color: a.AsiEstReg === 'A' ? 'green' : 'gray' }}>
                  {a.AsiEstReg === 'A' ? 'Activo' : 'Inactivo'}
                </td>
                <td>
                  <button
                    className={a.AsiEstReg === 'A' ? 'desactivar' : 'activar'}
                    onClick={() => cambiarEstado(a)}
                  >
                    {a.AsiEstReg === 'A' ? 'Desactivar' : 'Activar'}
                  </button>
                  <button
                    className="eliminar"
                    onClick={() => eliminarAsignacion(a.AsiCod)}
                  >
                    Eliminar
                  </button>
                </td>
              </tr>
            ))
          )}
        </tbody>
      </table>
    </div>
  );
})}

{cultivos.map((cultivo) => {
  const asignacionesCultivo = asignaciones.filter(a => a.cultivo?.CulCod === cultivo.CulCod);

  return (
    <div key={`cultivo-${cultivo.CulCod}`} className="asignaciones-bloque">
      <h3 className="cultivo">🌱 Cultivo: {cultivo.CulNom}</h3>
      <table className="asignaciones-table">
        <thead>
          <tr>
            <th>Usuario</th>
            <th>Rol</th>
            <th>Fecha</th>
            <th>Estado</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          {asignacionesCultivo.length === 0 ? (
            <tr>
              <td colSpan="5">Sin asignaciones para este cultivo</td>
            </tr>
          ) : (
            asignacionesCultivo.map((a) => (
              <tr key={a.AsiCod}>
                <td>{a.usuario?.UsuNom || `ID: ${a.AsiUsuCod}`}</td>
                <td>{a.rol?.RolNom || `ID: ${a.AsiRolCod}`}</td>
                <td>{new Date(a.AsiFecAsi).toLocaleDateString()}</td>
                <td style={{ color: a.AsiEstReg === 'A' ? 'green' : 'gray' }}>
                  {a.AsiEstReg === 'A' ? 'Activo' : 'Inactivo'}
                </td>
                <td>
                  <button
                    className={a.AsiEstReg === 'A' ? 'desactivar' : 'activar'}
                    onClick={() => cambiarEstado(a)}
                  >
                    {a.AsiEstReg === 'A' ? 'Desactivar' : 'Activar'}
                  </button>
                  <button
                    className="eliminar"
                    onClick={() => eliminarAsignacion(a.AsiCod)}
                  >
                    Eliminar
                  </button>
                </td>
              </tr>
            ))
          )}
        </tbody>
      </table>
    </div>
  );
})}

    </div>
  );
};

export default Asignaciones;
