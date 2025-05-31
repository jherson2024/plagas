from typing import Optional
from pydantic import BaseModel
from datetime import date
from config import IMAGEN_CULTIVO_URL
class ParcelaIn(BaseModel):
    ParNom: str
    ParUbi: str
    ParDes: str
    ParUsuCod: int
    ParFecReg: Optional[date] = None  # opcional
    ParEstReg: Optional[str] = None   # opcional
class ParcelaOut(BaseModel):
    ParCod: int
    ParNom: str
    ParUbi: str
    ParDes: str
    ParUsuCod: int
    ParFecReg: date
    ParEstReg: str

    class Config:
        orm_mode = True
class ParcelaUpdate(BaseModel):
    ParNom: Optional[str] = None
    ParUbi: Optional[str] = None
    ParDes: Optional[str] = None
    ParUsuCod: Optional[int] = None
    ParFecReg: Optional[date] = None
    ParEstReg: Optional[str] = None
class ParcelaEstadoUpdate(BaseModel):
    ParEstReg: str
    
class CultivoBase(BaseModel):
    CulNom: str
    CulParCod: int
    CulTip: Optional[str] = None
    CulFecSie: Optional[date] = None
    CulFecCos: Optional[date] = None
    CulPro: Optional[int] = None
    CulUrlIma: Optional[str] = None
    CulEstReg: Optional[str] = "A"

class CultivoCreate(CultivoBase):
    pass

class CultivoUpdate(BaseModel):
    CulNom: Optional[str]
    CulParCod: Optional[int]
    CulTip: Optional[str]
    CulFecSie: Optional[date]
    CulFecCos: Optional[date]
    CulPro: Optional[int]
    CulUrlIma: Optional[str]
    CulEstReg: Optional[str]

class CultivoEstadoUpdate(BaseModel):
    CulEstReg: str
class ParcelaResumen(BaseModel):
    ParCod: int
    ParNom: str

    class Config:
        orm_mode = True
class CultivoOut(BaseModel):
    CulCod: int
    CulNom: str
    CulTip: Optional[str]
    CulParCod: int
    CulFecSie: Optional[date]
    CulFecCos: Optional[date]
    CulPro: Optional[int]
    CulEstReg: Optional[str]
    CulUrlIma: Optional[str]

    class Config:
        orm_mode = True

    @staticmethod
    def from_orm_with_url(cultivo):
        url = f"{IMAGEN_CULTIVO_URL}/{cultivo.CulUrlIma}" if cultivo.CulUrlIma else None
        return CultivoOut(
            CulCod=cultivo.CulCod,
            CulNom=cultivo.CulNom,
            CulTip=cultivo.CulTip,
            CulParCod=cultivo.CulParCod,
            CulFecSie=cultivo.CulFecSie,
            CulFecCos=cultivo.CulFecCos,
            CulPro=cultivo.CulPro,
            CulEstReg=cultivo.CulEstReg,
            CulUrlIma=url
        )