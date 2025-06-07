from pydantic import BaseModel, Field
from typing import Optional, List


# -------- POSICIÓN DEL MAPA --------
class MapaOut(BaseModel):
    MapCod: int
    MapNom: str
    MapDes: str | None = None
    MapUrlIma: str | None = None
    MapEstReg: str

    class Config:
        orm_mode = True
class PosicionMapaCreate(BaseModel):
    PosPos: Optional[int]
    PosPosB: Optional[int]
    PosInd: Optional[str] = Field(None, max_length=20)
    PosEstReg: Optional[str] = Field(default="A", max_length=1)


class PosicionMapaOut(BaseModel):
    PosCod: int
    PosPos: Optional[int]
    PosPosB: Optional[int]
    PosInd: Optional[str]
    PosEstReg: Optional[str]

    class Config:
        orm_mode = True


# -------- IMAGEN CAPTURA --------

class ImagenCapturaOut(BaseModel):
    ImaCod: int
    ImaUrlIma: Optional[str]
    ImaCla: Optional[str]
    ImaInd: Optional[str]
    ImaEstReg: Optional[str]

    class Config:
        orm_mode = True
