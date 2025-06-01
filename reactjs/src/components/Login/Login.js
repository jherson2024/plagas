import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { loginUsuario } from '../../services/authService';
import './Login.css';
import { useAuth } from '../../context/AuthContext';
const Login = () => {
  const [usuario, setUsuario] = useState('');
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
      const data = await loginUsuario({ identificador: usuario, UsuCon: password });
      localStorage.setItem('token', data.token);
      console.log("Usuario recibido desde loginUsuario:", data.usuario);
      login({ usuario: data.usuario, token: data.token });
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
          <label>Email or Username</label>
          <input
            type="text"
            value={usuario}
            onChange={(e) => setUsuario(e.target.value)}
            placeholder="Email or Username"
            required
          />
          <label>Password</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="Password"
            required
          />
          <div className="login-options">
            <label>
              <input type="checkbox" /> Keep me logged in
            </label>
            <a href="/forgot-password">Forgot your password?</a>
          </div>
          <button type="submit" disabled={cargando}>
            {cargando ? 'Loading...' : 'Log in now'}
          </button>
        </form>
        {mensaje && <p className="login-error">{mensaje}</p>}
        <div className="login-social">
          <p>Or sign in with</p>
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
