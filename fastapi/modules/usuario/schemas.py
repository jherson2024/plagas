from pydantic import BaseModel
from typing import Optional

class UsuarioCreate(BaseModel):
    UsuNom: str
    UsuNumWha: int
    UsuCon: str

class LoginRequest(BaseModel):
    UsuNumWha: int
    UsuCon: str

class UsuarioOut(BaseModel):
    UsuCod: int
    UsuNom: Optional[str]
    UsuNumWha: Optional[int]
    UsuEstReg: Optional[str]
    UsuUrlImaPer: Optional[str]

class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    usuario: UsuarioOut

class UsuarioUpdate(BaseModel):
    UsuNom: Optional[str] = None
    UsuNumWha: Optional[int] = None
    UsuUrlImaPer: Optional[str] = None
    UsuEstReg: Optional[str] = None

class CambioContraseñaRequest(BaseModel):
    password_actual: str
    nueva_password: str
