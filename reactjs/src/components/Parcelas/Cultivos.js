// src/pages/Cultivos/Cultivos.jsx
import { useState, useEffect, useCallback, useRef } from 'react';
import { useAuth } from '../../context/AuthContext';
import {
  obtenerCultivos,
  crearCultivo,
  actualizarCultivo,
  eliminarCultivo,
  cambiarEstadoCultivo,
  obtenerParcelasResumen
} from '../../services/cultivo';
import CultivosTemplate from './CultivosTemplate';

const Cultivos = () => {
  const inputImagenRef = useRef(null);
  const { usuario } = useAuth();
  const [cultivos, setCultivos] = useState([]);
  const [parcelas, setParcelas] = useState([]);
  const [mensaje, setMensaje] = useState('');
  const [editId, setEditId] = useState(null);
  const [formData, setFormData] = useState({
    CulNom: '',
    CulTip: '',
    CulParCod: '',
    CulFecSie: '',
    CulFecCos: '',
    CulPro: false,
    CulUrlIma: null,
  });

  const fetchCultivos = useCallback(async () => {
    try {
      const res = await obtenerCultivos(usuario.UsuCod);
      setCultivos(res.data);
    } catch {
      setMensaje('Error al cargar cultivos');
    }
  }, [usuario.UsuCod]);

  const fetchParcelas = useCallback(async () => {
    try {
      const res = await obtenerParcelasResumen(usuario.UsuCod);
      setParcelas(res.data);
    } catch {
      setMensaje('Error al cargar parcelas');
    }
  }, [usuario.UsuCod]);

  useEffect(() => {
    fetchCultivos();
    fetchParcelas();
  }, [fetchCultivos, fetchParcelas]);

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value,
    }));
  };

  const handleImageChange = (e) => {
    const file = e.target.files[0];
    setFormData((prev) => ({ ...prev, CulUrlIma: file }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const dataToSend = {
        CulNom: formData.CulNom,
        CulParCod: formData.CulParCod ? parseInt(formData.CulParCod) : undefined,
        CulTip: formData.CulTip || undefined,
        CulFecSie: formData.CulFecSie || undefined,
        CulFecCos: formData.CulFecCos || undefined,
        CulPro: formData.CulPro ? 1 : 0,
        CulUrlIma: formData.CulUrlIma instanceof File ? formData.CulUrlIma : undefined,
      };

      if (editId) {
        await actualizarCultivo(editId, dataToSend);
        setMensaje('Cultivo actualizado');
      } else {
        await crearCultivo(dataToSend);
        setMensaje('Cultivo creado');
      }

      setFormData({
        CulNom: '',
        CulTip: '',
        CulParCod: '',
        CulFecSie: '',
        CulFecCos: '',
        CulPro: false,
        CulUrlIma: null,
      });
      if (inputImagenRef.current) inputImagenRef.current.value = null;

      setEditId(null);
      fetchCultivos();
    } catch (error) {
      console.error(error);
      setMensaje('Error al guardar cultivo');
    }
  };

  const handleEditar = (c) => {
    setFormData({
      CulNom: c.CulNom,
      CulTip: c.CulTip,
      CulParCod: c.CulParCod,
      CulFecSie: c.CulFecSie,
      CulFecCos: c.CulFecCos,
      CulPro: c.CulPro,
      CulUrlIma: null,
    });
    setEditId(c.CulCod);
  };

  const handleCancelar = () => {
    setEditId(null);
    setFormData({
      CulNom: '',
      CulTip: '',
      CulParCod: '',
      CulFecSie: '',
      CulFecCos: '',
      CulPro: false,
      CulUrlIma: null,
    });
    if (inputImagenRef.current) inputImagenRef.current.value = null;
  };

  const handleEliminar = async (id) => {
    if (!window.confirm('¿Seguro que deseas eliminar este cultivo?')) return;
    await eliminarCultivo(id);
    fetchCultivos();
  };

  const handleToggleEstado = async (id, estado) => {
    try {
      await cambiarEstadoCultivo(id, estado);
      fetchCultivos();
    } catch (error) {
      console.error('Error al cambiar estado:', error.response?.data || error.message);
      setMensaje('Error al cambiar el estado');
    }
  };

  return (
    <CultivosTemplate
      formData={formData}
      parcelas={parcelas}
      cultivos={cultivos}
      mensaje={mensaje}
      inputImagenRef={inputImagenRef}
      editId={editId}
      onChange={handleChange}
      onImageChange={handleImageChange}
      onSubmit={handleSubmit}
      onEditar={handleEditar}
      onCancelar={handleCancelar}
      onEliminar={handleEliminar}
      onToggleEstado={handleToggleEstado}
    />
  );
};

export default Cultivos;
