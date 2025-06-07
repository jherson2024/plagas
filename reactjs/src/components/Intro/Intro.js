import './Intro.css';

const Welcome = () => {
  return (
    <div className="welcome-container card">
      <h1 className="welcome-title">Bienvenid@</h1>

      <div className="intro-video-wrapper">
        <video className="intro-video" controls autoPlay muted loop>
          <source src="/video/intro.mp4" type="video/mp4" />
          Tu navegador no soporta videos HTML5.
        </video>
      </div>

      <p>
        Este sistema te permite realizar algunas tareas básicas para el seguimiento de plagas en el campo.
        Podrás marcar zonas en un mapa, registrar capturas fotográficas y consultar información asociada.
      </p>

      <p>
        Es una herramienta sencilla, pensada para comenzar con un monitoreo visual básico y apoyar decisiones técnicas con información organizada.
      </p>

      <h2>Funciones disponibles:</h2>
      <ul className="intro-list">
        <li>
          <img src="/assets/icon-parcelas.png" alt="Mapa" />
          <strong>Mapa:</strong> Dibuja áreas para inspección.
        </li>
        <li>
          <img src="/assets/icon-imagenes.png" alt="Capturas" />
          <strong>Capturas:</strong> Registra imágenes de plagas geolocalizadas.
        </li>
        <li>
          <img src="/assets/icon-ia.png" alt="IA básica" />
          <strong>IA (en pruebas):</strong> Analiza imágenes con modelos simples.
        </li>
        <li>
          <img src="/assets/icon-usuarios.png" alt="Usuario" />
          <strong>Perfil:</strong> Cambia tu información de acceso.
        </li>
      </ul>

      <div className="welcome-actions">
        <p>Usa el menú lateral para comenzar.</p>
        <p className="note">Este sistema está en desarrollo, y se irá mejorando con el tiempo.</p>
      </div>
    </div>
  );
};

export default Welcome;
