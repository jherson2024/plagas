//Perfil.js
import './Perfil.css';
import { useAuth } from '../../context/AuthContext';
import { useState, useRef, useEffect } from 'react';
import { actualizarPerfil, subirFoto, eliminarFoto } from '../../services/usuario';

const Perfil = () => {
  const { usuario, login } = useAuth();
  const fileInputRef = useRef(null);
  const defaultAvatar = '/img/default-avatar.png';

  const [preview, setPreview] = useState(() =>
    usuario?.UsuUrlImaPer || defaultAvatar
  );
  useEffect(() => {
    setPreview(usuario?.UsuUrlImaPer || defaultAvatar);
  }, [usuario?.UsuUrlImaPer]);
  const [formData, setFormData] = useState({
    UsuNom: usuario?.UsuNom || "",
    UsuNumWha: usuario?.UsuNumWha || "",
  });
  const handleFileChange = async (e) => {
    const file = e.target.files[0];
    if (!file) return;
    try {
      const response = await subirFoto(file);
      const nuevaFoto = response.UsuUrlImaPer;

      const nuevaFotoConBypass = `${nuevaFoto}?t=${Date.now()}`;
      setPreview(nuevaFotoConBypass);

      const usuarioActualizado = {
        ...usuario,
        UsuUrlImaPer: nuevaFoto,
      };

      const token = localStorage.getItem('token');
      login({ usuario: usuarioActualizado, token });
    } catch (err) {
      console.error("Error al subir la foto", err);
    }
  };

  const handleRemovePhoto = async () => {
    try {
      await eliminarFoto();
      setPreview(defaultAvatar);

      const usuarioActualizado = {
        ...usuario,
        UsuUrlImaPer: null,
      };

      const token = localStorage.getItem('token');
      login({ usuario: usuarioActualizado, token });
    } catch (err) {
      console.error("Error al eliminar la foto", err);
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await actualizarPerfil(formData);
      alert("Perfil actualizado");
    } catch (err) {
      console.error("Error al actualizar perfil", err);
    }
  };

  return (
    <div className="profile-form">
      <section className="profile-section">
        <h3>Personal</h3>
        <p>Manage your personal details and keep them up to date.</p>

        <div className="profile-photo">
          <img src={preview} alt="Avatar" />
          <div>
            <button type="button" onClick={() => fileInputRef.current.click()}>
              Upload new photo
            </button>
            <button type="button" onClick={handleRemovePhoto}>
              Remove
            </button>
            <input
              type="file"
              ref={fileInputRef}
              style={{ display: "none" }}
              accept="image/*"
              onChange={handleFileChange}
            />
          </div>
        </div>

        <form className="form-grid" onSubmit={handleSubmit}>
          <input
            type="text"
            name="UsuNom"
            placeholder="Nombre"
            value={formData.UsuNom}
            onChange={handleInputChange}
          />
          <input
            type="tel"
            name="UsuNumWha"
            placeholder="Número de WhatsApp"
            value={formData.UsuNumWha}
            onChange={handleInputChange}
          />

          <label>
            <input type="checkbox" defaultChecked />
            Participar en acceso anticipado a nuevas funciones
          </label>

          <button type="submit" className="update-button">
            Actualizar perfil
          </button>
        </form>
      </section>
    </div>
  );
};

export default Perfil;
