// src/pages/Cultivos/CultivosTemplate.jsx
import React from 'react';
import './Cultivos.css';

const CultivosTemplate = ({
  formData,
  parcelas,
  cultivos,
  mensaje,
  inputImagenRef,
  editId,
  onChange,
  onImageChange,
  onSubmit,
  onEditar,
  onCancelar,
  onEliminar,
  onToggleEstado,
}) => {
  return (
    <div className="parcelas">
      <form onSubmit={onSubmit}>
        <input name="CulNom" placeholder="Nombre" value={formData.CulNom} onChange={onChange} />
        <input name="CulTip" placeholder="Tipo" value={formData.CulTip} onChange={onChange} />
        <select name="CulParCod" value={formData.CulParCod} onChange={onChange}>
          <option value="">Selecciona una parcela</option>
          {parcelas.map((p) => (
            <option key={p.ParCod} value={p.ParCod}>
              {p.ParNom}
            </option>
          ))}
        </select>
        <input type="date" name="CulFecSie" value={formData.CulFecSie} onChange={onChange} />
        <input type="date" name="CulFecCos" value={formData.CulFecCos} onChange={onChange} />
        <label>
          <input type="checkbox" name="CulPro" checked={formData.CulPro} onChange={onChange} />
          Programado
        </label>
        <input
          type="file"
          accept="image/*"
          name="CulUrlIma"
          onChange={onImageChange}
          ref={inputImagenRef}
        />
        <button type="submit">{editId ? 'Actualizar' : 'Crear'}</button>
        {editId && (
          <button type="button" onClick={onCancelar}>
            Cancelar
          </button>
        )}
      </form>

      {mensaje && <p>{mensaje}</p>}

   <div className="cultivos-tarjetas">
  {cultivos.map((c) => {
    const parcela = parcelas.find((p) => p.ParCod === c.CulParCod);
    return (
      <div key={c.CulCod} className="tarjeta-wrapper">
        <div
          className="tarjeta-cultivo"
          style={{
            backgroundImage: `url(${c.CulUrlIma || '/img/default-cultivo.png'})`,
          }}
        >
          <div className="tipo">@{c.CulTip}</div>
          <div className="ojo">◉</div>
          <div
  className="nombre"
  style={{
    color: c.CulUrlIma ? 'white' : 'black',
  }}
>
  {c.CulNom}
</div>

          {/* Botones verticales */}
          <div className="acciones-laterales">
            <button title="Editar" onClick={() => onEditar(c)}>✏️</button>
            <button
              title={c.CulEstReg === 'A' ? 'Inactivar' : 'Activar'}
              onClick={() => onToggleEstado(c.CulCod, c.CulEstReg === 'A' ? 'I' : 'A')}
            >
              {c.CulEstReg === 'A' ? '🍂' : '🍃'}
            </button>
            <button title="Eliminar" onClick={() => onEliminar(c.CulCod)}>❌</button>
          </div>

         {c.CulPro == 1 && <div className="programado">P</div>}
          <div className="plaga">🪳 ...</div>
            <div className="sombra-inferior"></div>
        </div>

        <div className="tarjeta-detalle">
          <p><strong>Tipo:</strong> {c.CulTip}</p>
          <p><strong>Parcela:</strong> {parcela?.ParNom || 'Sin nombre'}</p>
          <p><strong>Siembra:</strong> {c.CulFecSie}</p>
          <p><strong>Cosecha:</strong> {c.CulFecCos}</p>
          <p><strong>Estado:</strong> {c.CulEstReg === 'A' ? 'Activo' : 'Inactivo'}</p>
          <p><strong>Programado:</strong> {c.CulPro ? 'Sí' : 'No'}</p>
        </div>
      </div>
    );
  })}
</div>
    </div>
  );
};

export default CultivosTemplate;
