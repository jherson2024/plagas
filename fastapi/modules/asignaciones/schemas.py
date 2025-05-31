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

class AsignacionRolUsuarioOut(AsignacionRolUsuarioBase):
    AsiCod: int
    AsiEstReg: Optional[str]

    class Config:
        orm_mode = True
