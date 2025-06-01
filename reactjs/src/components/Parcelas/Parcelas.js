import { useState, useEffect, useCallback } from 'react';
import {
  obtenerParcelas,
  crearParcela,
  actualizarParcela,
  eliminarParcela,
  cambiarEstadoParcela,
} 
from '../../services/parcela';
import './Parcelas.css';
import { useAuth } from '../../context/AuthContext';
const Parcelas = () => {
  const { usuario } = useAuth();
  const [parcelas, setParcelas] = useState([]);
  const [formData, setFormData] = useState({
    ParNom: '',
    ParUbi: '',
    ParDes: '',
    ParUsuCod: '',
  });
  const [mensaje, setMensaje] = useState('');
  const [editId, setEditId] = useState(null);

  const fetchParcelas = useCallback(async () => {
    try {
      const res = await obtenerParcelas(usuario.UsuCod);
      setParcelas(res.data);
    } catch {
      setMensaje('Error al cargar parcelas');
    }
  }, [usuario.UsuCod]);

  useEffect(() => {
    fetchParcelas();
  }, [fetchParcelas]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const data = {
        ...formData,
        ParUsuCod: parseInt(usuario.UsuCod),
      };

      if (editId) {
        await actualizarParcela(editId, data);
        setMensaje('Parcela actualizada');
        setEditId(null);
      } else {
        await crearParcela(data);
        setMensaje('Parcela creada');
      }

      setFormData({
        ParNom: '',
        ParUbi: '',
        ParDes: '',
        ParUsuCod: '',
      });
      fetchParcelas();
    } catch {
      setMensaje('Error al guardar');
    }
  };

  const handleEditar = (p) => {
    setFormData({
      ParNom: p.ParNom,
      ParUbi: p.ParUbi,
      ParDes: p.ParDes,
      ParUsuCod: p.ParUsuCod,
    });
    setEditId(p.ParCod);
  };

  const handleCancelar = () => {
    setEditId(null);
    setFormData({
      ParNom: '',
      ParUbi: '',
      ParDes: '',
      ParUsuCod: '',
    });
  };

  const handleEliminar = async (id) => {
    if (!window.confirm('¿Seguro que deseas eliminar esta parcela?')) return;
    await eliminarParcela(id);
    fetchParcelas();
  };

  const handleToggleEstado = async (id, estado) => {
    await cambiarEstadoParcela(id, estado);
    fetchParcelas();
  };

  return (
    <div className="parcelas">
      <form onSubmit={handleSubmit}>
        <input name="ParNom" placeholder="Nombre" value={formData.ParNom} onChange={handleChange} />
        <input name="ParUbi" placeholder="Ubicación" value={formData.ParUbi} onChange={handleChange} />
        <input name="ParDes" placeholder="Descripción" value={formData.ParDes} onChange={handleChange} />
        <button type="submit">{editId ? 'Actualizar' : 'Crear'}</button>
        {editId && (
          <button type="button" onClick={handleCancelar}>
            Cancelar
          </button>
        )}
      </form>

      {mensaje && <p>{mensaje}</p>}

      <table className="tabla-parcelas">
        <thead>
          <tr>
            <th>Nombre</th>
            <th>Ubicación</th>
            <th>Descripción</th>
            <th>Estado</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          {parcelas.map(p => (
            <tr key={p.ParCod}>
              <td>{p.ParNom}</td>
              <td>{p.ParUbi}</td>
              <td>{p.ParDes}</td>
              <td>{p.ParEstReg === 'A' ? '🍃' : '🍂'}</td>
              <td>
                <button title="Modificar" onClick={() => handleEditar(p)}>✏️</button>
                <button
                  title={p.ParEstReg === 'A' ? 'Inactivar' : 'Activar'}
                  onClick={() => handleToggleEstado(p.ParCod, p.ParEstReg === 'A' ? 'I' : 'A')}
                >
                  {p.ParEstReg === 'A' ? '🍂' : '🍃'}
                </button>
                <button title="Eliminar" onClick={() => handleEliminar(p.ParCod)}>❌</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default Parcelas;
