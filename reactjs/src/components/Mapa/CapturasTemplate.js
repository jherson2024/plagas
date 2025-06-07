import React, { useState } from "react";

const CapturasTemplate = ({
  mapa,
  posiciones,
  archivos,
  fotos,
  handleSeleccionarArchivo,
  handleSubirFoto,
  cargarFotos,
  eliminarPosicion,
  eliminarFoto,
  handleClickCrearPosicion,
}) => {
  const [nuevaPosicion, setNuevaPosicion] = useState(null);
  const [mostrarTodas, setMostrarTodas] = useState(false);

  const handleClickMapa = (e) => {
    const rect = e.target.getBoundingClientRect();
    const x = ((e.clientX - rect.left) / rect.width) * 100;
    const y = ((e.clientY - rect.top) / rect.height) * 100;

    setNuevaPosicion({
      PosPos: Math.round(x),
      PosPosB: Math.round(y),
      PosInd: "",
      Idn: "1",
    });
  };

  const handleGuardarPosicion = (e) => {
    e.preventDefault();
    handleClickCrearPosicion(nuevaPosicion);
    setNuevaPosicion(null);
  };

  const getColorPorNivel = (ind) => {
    if (ind.includes("Nivel 1")) return "green";
    if (ind.includes("Nivel 2")) return "orange";
    return "red";
  };

  return (
    <div className="captura-container">
      {mapa ? (
        <>
          <h2>Capturas del Mapa: <strong>{mapa.MapNom}</strong></h2>
          {mapa.MapDes && <p><em>{mapa.MapDes}</em></p>}
          <div className="mapa-wrapper">
            <img
              src={mapa.MapUrlIma}
              alt={`Mapa: ${mapa.MapNom}`}
              className="mapa-imagen"
              onClick={handleClickMapa}
            />
            {posiciones.map((pos) => (
              <div
                key={pos.PosCod}
                style={{
                  position: "absolute",
                  top: `${pos.PosPosB}%`,
                  left: `${pos.PosPos}%`,
                  transform: "translate(-50%, -50%)",
                  backgroundColor: getColorPorNivel(pos.PosInd),
                  width: "10px",
                  height: "10px",
                  borderRadius: "50%",
                }}
                title={pos.PosInd}
              />
            ))}
          </div>
        </>
      ) : (
        <p>Cargando mapa...</p>
      )}

      {nuevaPosicion && (
        <div className="fondo-sombreado">
          <div className="form-popup">
            <form onSubmit={handleGuardarPosicion}>
              <input
                type="text"
                placeholder="Descripción"
                value={nuevaPosicion.PosInd}
                onChange={(e) =>
                  setNuevaPosicion({ ...nuevaPosicion, PosInd: e.target.value })
                }
              />
              <select
                value={nuevaPosicion.Idn}
                onChange={(e) =>
                  setNuevaPosicion({ ...nuevaPosicion, Idn: e.target.value })
                }
              >
                <option value="1">Nivel 1</option>
                <option value="2">Nivel 2</option>
                <option value="3">Nivel 3</option>
              </select>
              <button type="submit">Guardar Posición</button>
              <button type="button" onClick={() => setNuevaPosicion(null)}>
                Cancelar
              </button>
            </form>
          </div>
        </div>
      )}

      <div className="posicion-lista">
        {posiciones.length > 0 && (
          <>
            {/* Mostrar la última posición creada */}
            <div className="posicion-item">
              <h4>{posiciones[posiciones.length - 1].PosInd}</h4>
              <input
                type="file"
                accept="image/*"
                onChange={(e) =>
                  handleSeleccionarArchivo(
                    posiciones[posiciones.length - 1].PosCod,
                    e.target.files[0]
                  )
                }
              />
              <button onClick={() => handleSubirFoto(posiciones[posiciones.length - 1].PosCod)}>
                Subir Foto
              </button>
              <button onClick={() => cargarFotos(posiciones[posiciones.length - 1].PosCod)}>
                Ver Fotos
              </button>
              <button onClick={() => eliminarPosicion(posiciones[posiciones.length - 1].PosCod)}>
                Eliminar Posición
              </button>
              <div className="foto-grid">
                {fotos[posiciones[posiciones.length - 1].PosCod]?.map((foto) => (
                  <div key={foto.ImaCod} className="foto-item-container">
                    <img src={foto.ImaUrlIma} alt="Captura" className="foto-item" />
                    <button onClick={() => eliminarFoto(foto.ImaCod, posiciones[posiciones.length - 1].PosCod)}>
                      Eliminar
                    </button>
                  </div>
                ))}
              </div>
            </div>

            {/* Botón para ver todas las anteriores */}
            {posiciones.length > 1 && (
              <button
                onClick={() => setMostrarTodas(!mostrarTodas)}
                className="btn-ver-todo"
              >
                {mostrarTodas ? "Ocultar anteriores" : "Mostrar todas las posiciones"}
              </button>
            )}

            {/* Mostrar anteriores si el usuario lo desea */}
            {mostrarTodas &&
              posiciones
                .slice(0, posiciones.length - 1)
                .map((pos) => (
                  <div key={pos.PosCod} className="posicion-item">
                    <h4>{pos.PosInd}</h4>
                    <input
                      type="file"
                      accept="image/*"
                      onChange={(e) =>
                        handleSeleccionarArchivo(pos.PosCod, e.target.files[0])
                      }
                    />
                    <button onClick={() => handleSubirFoto(pos.PosCod)}>Subir Foto</button>
                    <button onClick={() => cargarFotos(pos.PosCod)}>Ver Fotos</button>
                    <button onClick={() => eliminarPosicion(pos.PosCod)}>Eliminar Posición</button>
                    <div className="foto-grid">
                      {fotos[pos.PosCod]?.map((foto) => (
                        <div key={foto.ImaCod} className="foto-item-container">
                          <img src={foto.ImaUrlIma} alt="Captura" className="foto-item" />
                          <button onClick={() => eliminarFoto(foto.ImaCod, pos.PosCod)}>
                            Eliminar
                          </button>
                        </div>
                      ))}
                    </div>
                  </div>
                ))}
          </>
        )}
      </div>
    </div>
  );
};

export default CapturasTemplate;
