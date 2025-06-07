import { useState, useEffect } from "react";
import {
  crearPosicion,
  obtenerPosiciones,
  subirFotoCaptura,
  obtenerFotosCaptura,
  eliminarPosicion as apiEliminarPosicion,
  eliminarFotoCaptura as apiEliminarFotoCaptura
} from "../../services/capturas";
import { obtenerMapas } from "../../services/mapa";
import { useAuth } from "../../context/AuthContext";
import CapturasTemplate from "./CapturasTemplate";
import "./Capturas.css";

const Capturas = () => {
  const { token } = useAuth();
  const [mapa, setMapa] = useState(null);
  const [posiciones, setPosiciones] = useState([]);
  const [fotos, setFotos] = useState({});
  const [archivos, setArchivos] = useState({});

  useEffect(() => {
    cargarMapaUnico();
  }, [token]);

  const cargarMapaUnico = async () => {
    try {
      const res = await obtenerMapas();
      const mapaUsuario = res.data[0];
      if (mapaUsuario) {
        setMapa(mapaUsuario);
        cargarPosiciones(mapaUsuario.MapCod);
      }
    } catch (err) {
      console.error("❌ Error al cargar el mapa:", err);
    }
  };

  const cargarPosiciones = async (mapId) => {
    try {
      const res = await obtenerPosiciones(mapId);
      setPosiciones(res.data);
    } catch (err) {
      console.error("❌ Error al cargar posiciones:", err);
    }
  };

  const handleClickCrearPosicion = async (posData) => {
    if (!mapa) return;
    const { PosPos, PosPosB, PosInd, Idn } = posData;

    if (!PosPos || !PosInd) return alert("Completa la descripción.");

    try {
      await crearPosicion(mapa.MapCod, {
        PosPos: Number(PosPos),
        PosPosB: Number(PosPosB),
        PosInd: `${PosInd} (Nivel ${Idn})`,
        PosEstReg: "A",
      });
      cargarPosiciones(mapa.MapCod);
    } catch (err) {
      console.error("❌ Error al crear posición:", err);
    }
  };

  const handleSeleccionarArchivo = (posCod, file) => {
    setArchivos((prev) => ({ ...prev, [posCod]: file }));
  };

  const handleSubirFoto = async (posCod) => {
    try {
      const archivo = archivos[posCod];
      if (!archivo) return;
      await subirFotoCaptura(posCod, archivo);
      setArchivos((prev) => ({ ...prev, [posCod]: null }));
      cargarFotos(posCod);
    } catch (err) {
      console.error("❌ Error al subir foto:", err);
    }
  };

  const cargarFotos = async (posCod) => {
    try {
      const res = await obtenerFotosCaptura(posCod);
      setFotos((prev) => ({ ...prev, [posCod]: res.data }));
    } catch (err) {
      console.error("❌ Error al cargar fotos:", err);
    }
  };

  const eliminarPosicion = async (posCod) => {
    if (!window.confirm("¿Seguro que deseas eliminar esta posición?")) return;
    try {
      await apiEliminarPosicion(posCod);
      cargarPosiciones(mapa.MapCod);
    } catch (err) {
      console.error("❌ Error al eliminar posición:", err);
    }
  };

  const eliminarFoto = async (fotoId, posCod) => {
    if (!window.confirm("¿Eliminar esta imagen?")) return;
    try {
      await apiEliminarFotoCaptura(fotoId);
      cargarFotos(posCod);
    } catch (err) {
      console.error("❌ Error al eliminar foto:", err);
    }
  };

  return (
    <CapturasTemplate
      mapa={mapa}
      posiciones={posiciones}
      archivos={archivos}
      handleSeleccionarArchivo={handleSeleccionarArchivo}
      handleSubirFoto={handleSubirFoto}
      cargarFotos={cargarFotos}
      eliminarPosicion={eliminarPosicion}
      fotos={fotos}
      eliminarFoto={eliminarFoto}
      handleClickCrearPosicion={handleClickCrearPosicion} // 💡 clave
    />
  );
};

export default Capturas;
