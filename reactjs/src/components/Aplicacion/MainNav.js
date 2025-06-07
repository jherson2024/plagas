import './MainNav.css';
import configMenu from './configMenu.json'; // importa el JSON de configuración

const MainNav = ({ onSelect, onLogoClick, onToggleSidebar }) => {
  return (
    <nav className="main-nav">
      <button className="sidebar-toggle icon-button" onClick={onToggleSidebar}>
        ☰
      </button>
      <img 
        src="/img/logo.png" 
        alt="Logo" 
        className="main-logo"
        onClick={() => {
          onSelect('');
          onLogoClick();
        }}
      />
      <ul className="main-nav-icons">
        {Object.entries(configMenu).map(([clave, seccion]) => (
          <li
            key={clave}
            onClick={() => onSelect(clave)}
            title={seccion.titulo}
          >
            {seccion.icono || clave.toUpperCase()}
          </li>
        ))}
      </ul>
    </nav>
  );
};

export default MainNav;
