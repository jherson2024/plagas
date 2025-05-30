# schemas.py

from datetime import date
from pydantic import BaseModel
from typing import Optional
class LoginRequest(BaseModel):
    email: str
    contraseña: str


class UsuarioOut(BaseModel):
    id: int
    nombre: Optional[str]
    email: Optional[str]
    nombre_usuario: Optional[str]
    idioma_preferido: Optional[str]
    fecha_creacion: Optional[date]
    estado: Optional[str]
    imagen_perfil: Optional[str]
class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    usuario: UsuarioOut

class UsuarioUpdate(BaseModel):
    Nom: Optional[str] = None         # Nombre
    Ema: Optional[str] = None         # Email
    NomUsu: Optional[str] = None      # Nombre de usuario
    IdiPre: Optional[str] = None      # Idioma preferido


class CambioContraseñaRequest(BaseModel):
    contraseña_actual: str
    nueva_contraseña: str
    ip: str

# schemas.py
class AsignacionCreate(BaseModel):
    usuario_id: int
    rol_id: int
    parcela_id: Optional[int]
    cultivo_id: Optional[int]
    fecha_asignacion: date
