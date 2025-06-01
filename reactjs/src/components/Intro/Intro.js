import './Intro.css';

const Welcome = () => {
  return (
    <div className="welcome-container">
      <img src="/assets/logo-agro-inteligente.png" alt="Logo del sistema" className="intro-logo" />

      <h1>Bienvenido al Sistema de Gestión Agrícola Inteligente</h1>

      <video className="intro-video" controls autoPlay muted loop>
        <source src="/assets/video-intro.mp4" type="video/mp4" />
        Tu navegador no soporta videos HTML5.
      </video>

      <p>
        Esta plataforma permite gestionar de forma integral parcelas, cultivos, sensores, usuarios y 
        análisis con inteligencia artificial. Está diseñada para agricultores, investigadores y técnicos 
        que necesitan optimizar la producción agrícola y el monitoreo de plagas.
      </p>

      <h2>¿Qué puedes hacer en esta plataforma?</h2>
      <ul className="intro-list">
        <li>
          <img src="/assets/icon-usuarios.png" alt="Usuarios" />
          <strong>Usuarios y Roles:</strong> Gestiona cuentas con permisos personalizados.
        </li>
        <li>
          <img src="/assets/icon-parcelas.png" alt="Parcelas" />
          <strong>Parcelas y Cultivos:</strong> Organiza tus terrenos y cultivos de forma visual.
        </li>
        <li>
          <img src="/assets/icon-sensor.gif" alt="Sensores" />
          <strong>Sensores:</strong> Conecta sensores y monitorea variables en tiempo real.
        </li>
        <li>
          <img src="/assets/icon-imagenes.png" alt="Imágenes" />
          <strong>Lecturas e Imágenes:</strong> Visualiza datos y fotografía geolocalizada.
        </li>
        <li>
          <img src="/assets/icon-ia.png" alt="IA" />
          <strong>Análisis con IA:</strong> Detecta plagas y evalúa tratamientos con modelos inteligentes.
        </li>
        <li>
          <img src="/assets/icon-bitacora.png" alt="Bitácora" />
          <strong>Historial y Bitácoras:</strong> Revisa actividades y eventos registrados por usuarios.
        </li>
      </ul>

      <p className="note">
        Puedes navegar por el menú lateral para comenzar. 
        <br />
        * Todos los campos con asterisco son obligatorios en los formularios del sistema.
      </p>
    </div>
  );
};

export default Welcome;
