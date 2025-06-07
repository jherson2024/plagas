import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { registrarUsuario, loginUsuario } from '../../services/authService';
import './Login.css';
import { useAuth } from '../../context/AuthContext';

const Register = () => {
  const [UsuNom, setUsuNom] = useState('');
  const [UsuNumWha, setUsuNumWha] = useState('');
  const [UsuCon, setUsuCon] = useState('');
  const [mensaje, setMensaje] = useState('');
  const [cargando, setCargando] = useState(false);
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMensaje('');
    setCargando(true);

    try {
      await registrarUsuario({
        UsuNom,
        UsuNumWha: parseInt(UsuNumWha),
        UsuCon,
      });

      // Iniciar sesión automáticamente después del registro
      const data = await loginUsuario({
        UsuNumWha: parseInt(UsuNumWha),
        UsuCon,
      });

      localStorage.setItem('token', data.access_token);
      login({ usuario: data.usuario, token: data.access_token });

      navigate('/aplicacion');
    } catch (error) {
      setMensaje(error.message || 'Error al registrar');
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
          <p>Already have an account? <a href="/login">Log in</a></p>
        </div>

        <div className="login-right">
          <h2>Register</h2>
          <form onSubmit={handleSubmit}>
            <label>Nombre completo</label>
            <input
              type="text"
              value={UsuNom}
              onChange={(e) => setUsuNom(e.target.value)}
              placeholder="Nombre completo"
              required
            />

            <label>Número de WhatsApp</label>
            <input
              type="tel"
              value={UsuNumWha}
              onChange={(e) => setUsuNumWha(e.target.value)}
              placeholder="Ej. 5491123456789"
              required
            />

            <label>Contraseña</label>
            <input
              type="password"
              value={UsuCon}
              onChange={(e) => setUsuCon(e.target.value)}
              placeholder="Contraseña"
              required
            />

            <button type="submit" disabled={cargando}>
              {cargando ? 'Registrando...' : 'Crear cuenta'}
            </button>
          </form>

          {mensaje && <p className="login-error">{mensaje}</p>}

          <div className="login-social">
            <p>O regístrate con</p>
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

export default Register;
