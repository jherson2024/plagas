from pydantic import BaseModel
from typing import Optional
from datetime import date

class AsignacionRolUsuarioBase(BaseModel):
    AsiUsuCod: int
    AsiRolCod: int
    AsiFecAsi: date
    AsiParCod: Optional[int] = None
    AsiCulCod: Optional[int] = None

class AsignacionRolUsuarioCreate(AsignacionRolUsuarioBase):
    pass

class AsignacionRolUsuarioUpdate(BaseModel):
    AsiRolCod: Optional[int] = None
    AsiFecAsi: Optional[date] = None
    AsiParCod: Optional[int] = None
    AsiCulCod: Optional[int] = None

class UsuarioOut(BaseModel):
    UsuCod: int
    UsuNom: str

    class Config:
        orm_mode = True

class RolOut(BaseModel):
    RolCod: int
    RolNom: str

    class Config:
        orm_mode = True

class ParcelaOut(BaseModel):
    ParCod: int
    ParNom: str

    class Config:
        orm_mode = True

class CultivoOut(BaseModel):
    CulCod: int
    CulNom: str

    class Config:
        orm_mode = True

class AsignacionRolUsuarioOut(AsignacionRolUsuarioBase):
    AsiCod: int
    AsiEstReg: Optional[str]

    # Relaciones enriquecidas
    usuario: Optional[UsuarioOut]
    rol: Optional[RolOut]
    parcela: Optional[ParcelaOut]
    cultivo: Optional[CultivoOut]

    class Config:
        orm_mode = True