import './MainNav.css'
const MainNav = ({ onSelect, onLogoClick ,onToggleSidebar}) => {
  return (
    <nav className="main-nav">
      <button
  className="sidebar-toggle icon-button"
  onClick={onToggleSidebar}
>
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
        <li onClick={() => onSelect('parcelas')} title="Parcelas">🌾</li>
        <li onClick={() => onSelect('sensores')} title="Sensores">📟</li>
        <li onClick={() => onSelect('ia')} title="IA">🤖</li>
        <li onClick={() => onSelect('alertas')} title="Alertas">🚨</li>
        <li onClick={() => onSelect('admin')} title="Admin">🛠️</li>
        <li onClick={() => onSelect('config')} title="Configuración">⚙️</li>
      </ul>
    </nav>
  );
};

export default MainNav;
