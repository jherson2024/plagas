import { useAuth } from '../../context/AuthContext';
import './Header.css'
const Header = ({ titulo }) => {
  const { usuario } = useAuth();
  const avatarUrl = usuario?.UsuUrlImaPer || '/img/default-avatar.png';
  return (
    <header className="header">
      <div className="header-left">
        <h2>{titulo}</h2>
      </div>
      <div className="header-right">
        <button className="icon-button">🔔</button>
        <button className="icon-button">🌼</button>
        <span className="username">{usuario?.UsuNom ?? 'Usuario'}</span>
        <img src={avatarUrl} alt="Avatar" className="header-avatar" />
      </div>
    </header>
  );
};

export default Header;
