// src/services/axios.js
import axios from 'axios';
import { BASE_URL } from '../config/config';

const instance = axios.create({
  baseURL: BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true, // Si usás cookies/sesiones
});

export default instance;
