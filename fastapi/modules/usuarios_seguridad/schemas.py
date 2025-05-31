# schemas.py

from datetime import date
from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class UsuarioCreate(BaseModel):
    UsuNom: str
    UsuEma: EmailStr
    UsuNomUsu: str
    UsuCon: str
    UsuIdiPre: Optional[str] = "es"

class LoginRequest(BaseModel):
    identificador: str
    UsuCon: str

class UsuarioOut(BaseModel):
    UsuCod: int
    UsuNom: Optional[str]
    UsuEma: Optional[str]
    UsuNomUsu: Optional[str]
    UsuIdiPre: Optional[str]
    UsuFecCre: Optional[date]
    UsuEstReg: Optional[str]
    UsuUrlFotPer: Optional[str]

class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    usuario: UsuarioOut

class UsuarioUpdate(BaseModel):
    UsuNom: Optional[str] = None         # Nombre
    UsuEma: Optional[str] = None         # Email
    UsuNomUsu: Optional[str] = None      # Nombre de usuario
    UsuIdiPre: Optional[str] = None      # Idioma preferido

class CambioContraseñaRequest(BaseModel):
    password_actual: str
    nueva_password: str
    ip: Optional[str] = None

# schemas.py
class AsignacionCreate(BaseModel):
    AsiUsuCod: int
    AsiRolCod: int
    AsiParCod: Optional[int]
    AsiCulCod: Optional[int]
    AsiFecAsi: date
