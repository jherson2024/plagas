import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { registrarUsuario } from '../../services/authService'; // asegúrate que esta función exista
import './Login.css'; // Usamos el mismo CSS del login para mantener diseño
import { useAuth } from '../../context/AuthContext';

const Register = () => {
  const [UsuNom, setUsuNom] = useState('');
  const [UsuNomUsu, setUsuNomUsu] = useState('');
  const [UsuEma, setUsuEma] = useState('');
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
      const data = await registrarUsuario({
        UsuNom,
        UsuNomUsu,
        UsuEma,
        UsuCon,
        UsuIdiPre: 'es',
});
      localStorage.setItem('token', data.token);
      login({ usuario: data.usuario, token: data.token });
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
          <label>Username</label>
          <label>Nombre completo</label>
<input
  type="text"
  value={UsuNom}
  onChange={(e) => setUsuNom(e.target.value)}
  placeholder="Nombre completo"
  required
/>

<label>Username</label>
<input
  type="text"
  value={UsuNomUsu}
  onChange={(e) => setUsuNomUsu(e.target.value)}
  placeholder="Username"
  required
/>

<label>Email</label>
<input
  type="email"
  value={UsuEma}
  onChange={(e) => setUsuEma(e.target.value)}
  placeholder="Email"
  required
/>

<label>Password</label>
<input
  type="password"
  value={UsuCon}
  onChange={(e) => setUsuCon(e.target.value)}
  placeholder="Password"
  required
/>
          <button type="submit" disabled={cargando}>
            {cargando ? 'Registering...' : 'Create account'}
          </button>
        </form>

        {mensaje && <p className="login-error">{mensaje}</p>}

        <div className="login-social">
          <p>Or sign up with</p>
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
