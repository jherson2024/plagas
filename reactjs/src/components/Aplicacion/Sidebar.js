import './Sidebar.css'; // Asegúrate de tener este import si usas CSS separado

const Sidebar = ({ seccion, onOpcionSeleccionada }) => {
  const opciones = {
    parcelas: ['parcelas', 'cultivos', 'asignaciones'],
    sensores: ['sensores', 'lecturas', 'imagenes'],
    ia: ['analisis', 'modelos', 'evaluacion', 'plagas'],
    alertas: ['alertas', 'recomendaciones', 'fuentes'],
    admin: ['usuarios', 'roles', 'permisos', 'bitacora', 'acciones'],
    config: ['perfil', 'contrasena', 'bloqueos'],
  };

  if (!seccion) return null; // Seguridad extra

  return (
    <aside className="sidebar-content">
      <h2 className="sidebar-title">{seccion.toUpperCase()}</h2>
      <ul className="sidebar-menu">
        {opciones[seccion]?.map((op) => (
          <li key={op} onClick={() => onOpcionSeleccionada(op)}>
            {op.charAt(0).toUpperCase() + op.slice(1)}
          </li>
        ))}
      </ul>
    </aside>
  );
};

export default Sidebar;
