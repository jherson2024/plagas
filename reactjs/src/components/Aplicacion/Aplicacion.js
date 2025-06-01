import './Aplicacion.css';
import { useState } from 'react';
import MainNav from './MainNav';
import Sidebar from './Sidebar';
import Header from './Header';
import Intro from '../Intro/Intro';
import Perfil from '../Config/Perfil';
import Contrasena from '../Config/Contrasena';
import Parcelas from '../Parcelas/Parcelas';
import Cultivos from '../Parcelas/Cultivos';
import Asignaciones from '../Parcelas/Asignaciones';
import IntroParcelas from '../Intro/IntroParcelas';
import IntroSensores from '../Intro/IntroSensores';
import IntroIA from '../Intro/IntroIA';
import IntroAlertas from '../Intro/IntroAlertas';
import IntroAdmin from '../Intro/IntroAdmin';
import IntroConfig from '../Intro/IntroConfig';
// Aquí importarías otros componentes, como Sensores, IA, etc.
const Aplicacion = () => {
  const [seccionPrincipal, setSeccionPrincipal] = useState('parcelas');
  const [vistaSecundaria, setVistaSecundaria] = useState('');
  const [mostrarSidebar, setMostrarSidebar] = useState(false);
  const volverAIntro = () => {
  setSeccionPrincipal('');
  setVistaSecundaria('');
};
  const getTitulo = () => {
    const titulos = {
      parcelas: {
        parcelas: 'Gestión de Parcelas',
        cultivos: 'Gestión de Cultivos',
        asignaciones: 'Asignaciones de Usuarios',
      },
      sensores: {
        sensores: 'Sensores',
        lecturas: 'Lecturas de Sensores',
        imagenes: 'Imágenes de Cultivo',
      },
      ia: {
        analisis: 'Análisis de IA',
        modelos: 'Modelos IA',
        evaluacion: 'Evaluación de Modelos',
        plagas: 'Imágenes de Plagas',
      },
      alertas: {
        alertas: 'Alertas',
        recomendaciones: 'Recomendaciones',
        fuentes: 'Fuentes de Recomendación',
      },
      admin: {
        usuarios: 'Usuarios',
        roles: 'Roles',
        permisos: 'Permisos',
        bitacora: 'Bitácora',
        acciones: 'Acciones',
      },
      config: {
        perfil: 'Perfil de Usuario',
        contrasena: 'Cambiar Contraseña',
        bloqueos: 'Historial de Bloqueos',
      }
    };
    return titulos[seccionPrincipal]?.[vistaSecundaria] || 'Bienvenid@';
  };
  const renderVista = () => {
  if (!seccionPrincipal) return <Intro />;

  if (seccionPrincipal === 'parcelas') {
    switch (vistaSecundaria) {
      case 'parcelas': return <Parcelas />;
      case 'cultivos': return <Cultivos />;
      case 'asignaciones': return <Asignaciones />;
      default: return <IntroParcelas />;
    }
  }

  if (seccionPrincipal === 'sensores') {
    switch (vistaSecundaria) {
      case 'sensores': return <div>Sensores</div>;
      case 'lecturas': return <div>Lecturas de Sensores</div>;
      case 'imagenes': return <div>Imágenes de Cultivo</div>;
      default: return <IntroSensores />;
    }
  }

  if (seccionPrincipal === 'ia') {
    switch (vistaSecundaria) {
      case 'analisis': return <div>Análisis de IA</div>;
      case 'modelos': return <div>Modelos IA</div>;
      case 'evaluacion': return <div>Evaluación de Modelos</div>;
      case 'plagas': return <div>Imágenes de Plagas</div>;
      default: return <IntroIA />;
    }
  }

  if (seccionPrincipal === 'alertas') {
    switch (vistaSecundaria) {
      case 'alertas': return <div>Alertas</div>;
      case 'recomendaciones': return <div>Recomendaciones</div>;
      case 'fuentes': return <div>Fuentes de Recomendación</div>;
      default: return <IntroAlertas />;
    }
  }

  if (seccionPrincipal === 'admin') {
    switch (vistaSecundaria) {
      case 'usuarios': return <div>Usuarios</div>;
      case 'roles': return <div>Roles</div>;
      case 'permisos': return <div>Permisos</div>;
      case 'bitacora': return <div>Bitácora</div>;
      case 'acciones': return <div>Acciones</div>;
      default: return <IntroAdmin />;
    }
  }

  if (seccionPrincipal === 'config') {
    switch (vistaSecundaria) {
      case 'perfil': return <Perfil />;
      case 'contrasena': return <Contrasena />;
      case 'bloqueos': return <div>Historial de Bloqueos</div>;
      default: return <IntroConfig />;
    }
  }

  return <Intro />;
};
  return (
    <div className="app-wrapper">
<MainNav
  onSelect={setSeccionPrincipal}
  onLogoClick={volverAIntro}
  onToggleSidebar={() => setMostrarSidebar(!mostrarSidebar)}
/>


  {/* Botón solo visible en móvil */}
  {seccionPrincipal && (
  <>
    {/* BOTÓN SOLO EN MÓVIL */}
    <button
      className="sidebar-toggle icon-button"
      onClick={() => setMostrarSidebar(!mostrarSidebar)}
    >
      ☰
    </button>

    {/* SIDEBAR */}
    <div className={`sidebar ${mostrarSidebar ? 'active' : ''}`}>
    <Sidebar
      seccion={seccionPrincipal}
      onOpcionSeleccionada={(val) => {
        setVistaSecundaria(val);
        setMostrarSidebar(false); // Cierra el sidebar después de seleccionar
      }}
    />
  </div>
  </>
)}


  <div className="main-wrapper">
    <Header titulo={getTitulo()} />
    <main className="main-content">{renderVista()}</main>
  </div>
</div>

  );
};
export default Aplicacion;
