// Contrasena.js
import './Contrasena.css';
import { useState } from 'react';
import { cambiarContrasena } from '../../services/usuario';
import { useAuth } from '../../context/AuthContext';

const Contrasena = () => {
  const { usuario } = useAuth();
  console.log(usuario);

  const [formData, setFormData] = useState({
    password_actual: '',
    nueva_password: '',
    confirmar: '',
  });

  const [mensaje, setMensaje] = useState(null);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMensaje(null);

    if (formData.nueva_password !== formData.confirmar) {
      setMensaje('Las contraseñas no coinciden');
      return;
    }

    try {
      await cambiarContrasena(
        {
          password_actual: formData.password_actual,
          nueva_password: formData.nueva_password,
        },
        usuario.UsuCod
      );
      setMensaje('Contraseña actualizada exitosamente');

      // ✅ Reiniciar campos con las claves correctas
      setFormData({
        password_actual: '',
        nueva_password: '',
        confirmar: '',
      });
    } catch (err) {
      console.error('Error al cambiar la contraseña', err);
      setMensaje('Error al cambiar la contraseña');
    }
  };

  return (
    <div className="password-form">
      <h3>Seguridad</h3>
      <p>Cambia tu contraseña actual por una nueva.</p>
      <form onSubmit={handleSubmit}>
        <input
          type="password"
          name="password_actual"
          placeholder="Contraseña actual"
          value={formData.password_actual}
          onChange={handleChange}
        />
        <input
          type="password"
          name="nueva_password"
          placeholder="Nueva contraseña"
          value={formData.nueva_password}
          onChange={handleChange}
        />
        <input
          type="password"
          name="confirmar"
          placeholder="Confirmar nueva contraseña"
          value={formData.confirmar}
          onChange={handleChange}
        />
        <button type="submit">Cambiar contraseña</button>
      </form>
      {mensaje && (
  <p
    className={`mensaje ${
      mensaje.includes('exitosamente') ? 'mensaje-exito' : 'mensaje-error'
    }`}
  >
    {mensaje}
  </p>
)}
    </div>
  );
};

export default Contrasena;
