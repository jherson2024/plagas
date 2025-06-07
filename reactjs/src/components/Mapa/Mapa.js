import { useState, useEffect } from 'react';
import './Mapa.css';
import {
  obtenerMapas,
  crearMapa,
  subirImagenMapa,
  eliminarMapa,
} from '../../services/mapa';
import { useAuth } from '../../context/AuthContext';

const Mapa = () => {
  const { token } = useAuth();
  const [mapas, setMapas] = useState([]);
  const [nombre, setNombre] = useState('');
  const [imagenArchivo, setImagenArchivo] = useState(null);
  const [mapaSeleccionado, setMapaSeleccionado] = useState(null);

  useEffect(() => {
    cargarMapas();
  }, [token]);

  const cargarMapas = async () => {
    try {
      const res = await obtenerMapas();
      setMapas(res.data);
    } catch (err) {
      console.error("Error al cargar mapas", err);
    }
  };

  const handleCrearMapa = async (e) => {
    e.preventDefault();
    if (!nombre.trim()) return;

    try {
      await crearMapa({ MapNom: nombre, MapUrlIma: '' });
      setNombre('');
      await cargarMapas();
    } catch (err) {
      console.error("Error al crear mapa", err);
    }
  };

  const handleSeleccionarImagen = (e, mapa) => {
    setMapaSeleccionado(mapa);
    setImagenArchivo(e.target.files[0]);
  };

  const handleSubirImagen = async () => {
    if (!mapaSeleccionado || !imagenArchivo) return;
    try {
      await subirImagenMapa(mapaSeleccionado.MapCod, imagenArchivo);
      setImagenArchivo(null);
      setMapaSeleccionado(null);
      await cargarMapas();
    } catch (err) {
      console.error("Error al subir imagen", err);
    }
  };

  const handleEliminar = async (mapCod) => {
    if (!window.confirm("¿Seguro que quieres eliminar este mapa?")) return;
    try {
      await eliminarMapa(mapCod);
      await cargarMapas();
    } catch (err) {
      console.error("Error al eliminar mapa", err);
    }
  };

  return (
    <div className="mapa-container">
      <h2>Mis Mapas</h2>

      <form onSubmit={handleCrearMapa} className="mapa-form">
        <input
          type="text"
          placeholder="Nombre del mapa"
          value={nombre}
          onChange={(e) => setNombre(e.target.value)}
        />
        <button type="submit">Crear Mapa</button>
      </form>

      <div className="mapa-lista">
        {mapas.map((mapa) => (
          <div key={mapa.MapCod} className="mapa-item">
            <h4>{mapa.MapNom}</h4>
            {mapa.MapUrlIma ? (
              <img
                src={mapa.MapUrlIma}
                alt="Mapa"
                className="mapa-imagen"
              />
            ) : (
              <p>Sin imagen</p>
            )}

            <input
              type="file"
              accept="image/*"
              onChange={(e) => handleSeleccionarImagen(e, mapa)}
            />

            {mapaSeleccionado?.MapCod === mapa.MapCod && imagenArchivo && (
              <button onClick={handleSubirImagen}>Subir Imagen</button>
            )}

            <button onClick={() => handleEliminar(mapa.MapCod)}>Eliminar</button>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Mapa;
