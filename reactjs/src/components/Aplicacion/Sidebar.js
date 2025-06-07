import './Sidebar.css'
const Sidebar = ({ seccion, opciones = [], onOpcionSeleccionada }) => {
  if (!seccion) return null;

  return (
    <aside className="sidebar-content">
      <h2 className="sidebar-title">{seccion.toUpperCase()}</h2>
      <ul className="sidebar-menu">
        {opciones.map((op) => (
          <li key={op} onClick={() => onOpcionSeleccionada(op)}>
            {op.charAt(0).toUpperCase() + op.slice(1)}
          </li>
        ))}
      </ul>
    </aside>
  );
};

export default Sidebar;
