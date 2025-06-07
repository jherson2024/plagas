import React from 'react';
import './IntroMapa.css';

const IntroMapa = ({ setSeccionPrincipal, setVistaSecundaria }) => {
  const irAMapa = () => {
    setSeccionPrincipal('mapa');
    setVistaSecundaria('mapa');
  };
  const irACapturas = () => {
    setSeccionPrincipal('mapa');
    setVistaSecundaria('capturas');
  };
  return (
    <div className="intro-mapa card">
      <h2 className="intro-title">Monitorea tu campo con el módulo de Mapa</h2>

      <p>
        Esta herramienta te permite visualizar y registrar <strong>zonas de inspección</strong> en el campo agrícola.
      </p>

      <p>
        Primero, debes <strong>crear un área de monitoreo</strong> en el mapa. Este área representará la zona donde realizarás observaciones de plagas.
      </p>

      <p>
        Luego podrás comenzar a <strong>registrar capturas</strong> dentro de esa área: indica el tipo de plaga, el nivel de infestación, y adjunta fotografías para un mejor seguimiento.
      </p>

      <p>
        Así podrás <strong>documentar la evolución</strong> de la situación y facilitar decisiones técnicas de manejo.
      </p>

      <div className="intro-button-group">
        <button className="intro-button primary" onClick={irAMapa}>
          🗺️ Crear Área en el Mapa
        </button>
        <button className="intro-button secondary" onClick={irACapturas}>
          📸 Ver Capturas Registradas
        </button>
      </div>
    </div>
  );
};

export default IntroMapa;
