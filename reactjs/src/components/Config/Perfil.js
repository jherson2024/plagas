import './Perfil.css';
import { useAuth } from '../../context/AuthContext';
import { useState, useRef, useEffect } from 'react';
import { actualizarPerfil, subirFoto, eliminarFoto } from '../../services/usuario';

const Perfil = () => {
  const { usuario, login } = useAuth();
  const fileInputRef = useRef(null);
  const defaultAvatar = '/img/default-avatar.png';

  // Imagen inicial con fallback
  const [preview, setPreview] = useState(() =>
    usuario?.UsuUrlFotPer || defaultAvatar
  );
 useEffect(() => {
  setPreview(usuario?.UsuUrlFotPer || defaultAvatar);
}, [usuario?.UsuUrlFotPer]);

  const [formData, setFormData] = useState({
    UsuNom: usuario?.UsuNom || "",
    UsuEma: usuario?.UsuEma || "",
    UsuNomUsu: usuario?.UsuNomUsu || "",
    UsuIdiPre: usuario?.UsuIdiPre || "Español",
  });

  const handleFileChange = async (e) => {
  const file = e.target.files[0];
  if (!file) return;

  try {
    const response = await subirFoto(usuario.UsuCod, file);
    const nuevaFoto = response.UsuUrlFotPer;

   const nuevaFotoConBypass = `${nuevaFoto}?t=${Date.now()}`;
   setPreview(nuevaFotoConBypass);

    const usuarioActualizado = {
      ...usuario,
      UsuUrlFotPer: nuevaFoto,
    };

    const token = localStorage.getItem('token'); // ⚠️ Importante: recuperar token
    login({ usuario: usuarioActualizado, token }); // ✅ mantener forma esperada
  } catch (err) {
    console.error("Error al subir la foto", err);
  }
};

 const handleRemovePhoto = async () => {
  try {
    await eliminarFoto(usuario.UsuCod);
    setPreview(defaultAvatar);

    const usuarioActualizado = {
      ...usuario,
      UsuUrlFotPer: null,
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
      await actualizarPerfil(usuario.UsuCod, formData);
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
            placeholder="Name"
            value={formData.UsuNom}
            onChange={handleInputChange}
          />
          <input
            type="email"
            name="UsuEma"
            placeholder="Email"
            value={formData.UsuEma}
            onChange={handleInputChange}
          />
          <input
            type="text"
            name="UsuNomUsu"
            placeholder="UserName"
            value={formData.UsuNomUsu}
            onChange={handleInputChange}
          />
          <label>
            <input type="checkbox" defaultChecked />
            Participar en acceso anticipado a nuevas funciones
          </label>

          <h3>Preferencias</h3>
          <select
            name="UsuIdiPre"
            value={formData.UsuIdiPre}
            onChange={handleInputChange}
          >
            <option value="Español">Español</option>
            <option value="Inglés">Inglés</option>
          </select>

          <button type="submit" className="update-button">
            Update Profile
          </button>
        </form>
      </section>
    </div>
  );
};

export default Perfil;
