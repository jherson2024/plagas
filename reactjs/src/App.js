import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Login from './components/Login/Login';
import Register from './components/Login/Register';
import Aplicacion from './components/Aplicacion/Aplicacion';
import { AuthProvider } from './context/AuthContext'; // Asegúrate del path correcto

function App() {
  return (
    <AuthProvider> {/* 👈 Aquí va el proveedor, envolviendo todo */}
      <Router>
        <Routes>
          <Route path="/" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/aplicacion" element={<Aplicacion />} />
          <Route path="/login" element={<Login />} />
        </Routes>
      </Router>
    </AuthProvider>
  );
}

export default App;
