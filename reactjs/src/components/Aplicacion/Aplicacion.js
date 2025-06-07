import { useState } from 'react';
import configMenu from './configMenu.json';
import { componenteMap } from './componenteMap';
import MainNav from './MainNav';
import Sidebar from './Sidebar';
import Header from './Header';
import Intro from '../Intro/Intro';
import './Aplicacion.css'

const Aplicacion = () => {
  const [seccionPrincipal, setSeccionPrincipal] = useState('');
  const [vistaSecundaria, setVistaSecundaria] = useState('');
  const [mostrarSidebar, setMostrarSidebar] = useState(false);

  const volverAIntro = () => {
    setSeccionPrincipal('');
    setVistaSecundaria('');
  };

  const getTitulo = () => {
    if (!seccionPrincipal) return 'Bienvenid@';
    const seccion = configMenu[seccionPrincipal];
    if (!seccion) return 'Bienvenid@';
    return (
      seccion.vistas?.[vistaSecundaria]?.titulo ||
      seccion.titulo ||
      'Bienvenid@'
    );
  };

  const renderVista = () => {
    if (!seccionPrincipal) return <Intro />;

    const seccion = configMenu[seccionPrincipal];
    if (!seccion) return <Intro />;

    if (vistaSecundaria) {
      const compName = seccion.vistas?.[vistaSecundaria]?.componente;
      const Componente = componenteMap[compName];
      return Componente ? <Componente /> : <div>Vista no encontrada</div>;
    }

    const IntroComp = componenteMap[seccion.componenteIntro];
    return IntroComp ? <IntroComp setSeccionPrincipal={setSeccionPrincipal} setVistaSecundaria={setVistaSecundaria} /> : <Intro />;
  };

  return (
    <div className="app-wrapper">
      <MainNav
        onSelect={setSeccionPrincipal}
        onLogoClick={volverAIntro}
        onToggleSidebar={() => setMostrarSidebar(!mostrarSidebar)}
      />

      {seccionPrincipal && mostrarSidebar && (
        <div className="sidebar-overlay" onClick={() => setMostrarSidebar(false)}>
          <div className="sidebar active" onClick={(e) => e.stopPropagation()}>
            <Sidebar
              seccion={seccionPrincipal}
              opciones={Object.keys(configMenu[seccionPrincipal]?.vistas || {})}
              onOpcionSeleccionada={(val) => {
                setVistaSecundaria(val);
                setMostrarSidebar(false);
              }}
            />
          </div>
        </div>
      )}

      <div className="main-wrapper">
        <Header titulo={getTitulo()} />
        <main className="main-content">{renderVista()}</main>
      </div>
    </div>
  );
};

export default Aplicacion;
