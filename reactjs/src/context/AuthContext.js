//AuthContext.js
import { createContext, useState, useEffect, useContext } from 'react';
import axios from 'axios';
// Crea el contexto
const AuthContext = createContext();
// Proveedor del contexto
export const AuthProvider = ({ children }) => {
  const [usuario, setUsuario] = useState(null);
  useEffect(() => {
    try {
      const usuarioGuardado = localStorage.getItem('usuario');
      // Validar que el valor exista y sea un JSON válido
      if (usuarioGuardado && usuarioGuardado !== 'undefined') {
        const usuarioParseado = JSON.parse(usuarioGuardado);
        setUsuario(usuarioParseado);
        // También puedes cargar el token si lo guardaste
        const token = localStorage.getItem('token');
        if (token) {
          axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
        }
      }
    } catch (error) {
      console.error('Error al leer usuario desde localStorage:', error);
      setUsuario(null);
      localStorage.removeItem('usuario');
      localStorage.removeItem('token');
    }
  }, []);
  const login = ({ usuario, token }) => {
    setUsuario(usuario);
    localStorage.setItem('usuario', JSON.stringify(usuario));
    localStorage.setItem('token', token);

    console.log('TOKEN GUARDADO:', token);

    axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
  };
  const logout = () => {
    setUsuario(null);
    localStorage.removeItem('usuario');
    localStorage.removeItem('token');
    delete axios.defaults.headers.common['Authorization'];
  };
  return (
    <AuthContext.Provider value={{ usuario, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};
// Hook para usar el contexto más fácilmente
export const useAuth = () => useContext(AuthContext);
