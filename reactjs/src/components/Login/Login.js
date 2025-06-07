import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { loginUsuario } from '../../services/authService';
import './Login.css';
import { useAuth } from '../../context/AuthContext';

const Login = () => {
  const [numero, setNumero] = useState('');
  const [password, setPassword] = useState('');
  const [mensaje, setMensaje] = useState('');
  const [cargando, setCargando] = useState(false);
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMensaje('');
    setCargando(true);
    try {
      const data = await loginUsuario({ UsuNumWha: parseInt(numero), UsuCon: password });

      localStorage.setItem('token', data.access_token);

      login({ usuario: data.usuario, token: data.access_token });

      navigate('/aplicacion');
    } catch (error) {
      setMensaje(error.message);
    } finally {
      setCargando(false);
    }
  };

  return (
    <div className="login-wrapper">
      <div className="login-container">
        <div className="login-left">
          <h1>Welcome!</h1>
          <img src="/img/logo_b.png" alt="Smiley Icon" className="login-icon" />
          <p className="login-brand">W.</p>
          <p>Not a member yet? <a href="/register">Register now</a></p>
        </div>
        <div className="login-right">
          <h2>Log in</h2>
          <form onSubmit={handleSubmit}>
            <label>Número de WhatsApp</label>
            <input
              type="tel"
              value={numero}
              onChange={(e) => setNumero(e.target.value)}
              placeholder="Ej. 5491123456789"
              required
            />
            <label>Contraseña</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Contraseña"
              required
            />
            <div className="login-options">
              <label>
                <input type="checkbox" /> Mantener sesión iniciada
              </label>
              <a href="/forgot-password">¿Olvidaste tu contraseña?</a>
            </div>
            <button type="submit" disabled={cargando}>
              {cargando ? 'Cargando...' : 'Iniciar sesión'}
            </button>
          </form>
          {mensaje && <p className="login-error">{mensaje}</p>}
          <div className="login-social">
            <p>O inicia sesión con</p>
            <div className="login-social-buttons">
              <button>Google</button>
              <button>Facebook</button>
              <button>Twitter</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Login;
