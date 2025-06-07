from pydantic import BaseModel, Field
from typing import Optional


class MapaCreate(BaseModel):
    MapNom: str = Field(..., max_length=80)
    MapUrlIma: str = Field(..., max_length=80)
    MapEstReg: Optional[str] = Field(default='A', max_length=1)


class MapaUpdate(BaseModel):
    MapNom: Optional[str] = Field(None, max_length=80)
    MapUrlIma: Optional[str] = Field(None, max_length=80)
    MapEstReg: Optional[str] = Field(None, max_length=1)


class MapaOut(BaseModel):
    MapCod: int
    MapNom: str
    MapUrlIma: str
    MapEstReg: Optional[str]

    class Config:
        orm_mode = True
