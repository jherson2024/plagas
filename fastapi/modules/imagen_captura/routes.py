from typing import List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from pathlib import Path
import shutil, uuid
from fastapi import status
from sqlalchemy.exc import SQLAlchemyError
from models import Mapa, PosicionMapa, ImagenCaptura, Usuario
from database import get_db
from modules.usuario.auth import obtener_usuario_actual
from .schemas import MapaOut, PosicionMapaCreate, PosicionMapaOut, ImagenCapturaOut
from config import IMAGEN_MAPA_URL, STATIC_URL

router = APIRouter()

IMAGEN_CAPTURA_PATH = "imagen_captura"
IMAGEN_CAPTURA_URL = f"{STATIC_URL}/{IMAGEN_CAPTURA_PATH}"

@router.get("/mapas/{map_cod}", response_model=MapaOut)
def obtener_mapa(
    map_cod: int,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(obtener_usuario_actual)
):
    mapa = db.query(Mapa).filter(Mapa.MapCod == map_cod, Mapa.MapUsuCod == usuario.UsuCod).first()

    if not mapa:
        raise HTTPException(status_code=404, detail="Mapa no encontrado")

    # Agrega la URL completa si hay imagen
    if mapa.MapUrlIma:
        mapa.MapUrlIma = f"{IMAGEN_MAPA_URL}/{mapa.MapUrlIma}"

    return mapa
# Crear posición en un mapa
@router.post("/mapas/{map_cod}/posiciones/", response_model=PosicionMapaOut)
def crear_posicion_mapa(
    map_cod: int,
    datos: PosicionMapaCreate,
    usuario: Usuario = Depends(obtener_usuario_actual),
    db: Session = Depends(get_db)
):
    mapa = db.query(Mapa).filter(Mapa.MapCod == map_cod, Mapa.MapUsuCod == usuario.UsuCod).first()
    if not mapa:
        raise HTTPException(status_code=404, detail="Mapa no encontrado")

    nueva_posicion = PosicionMapa(
        PosMapCod=map_cod,
        PosPos=datos.PosPos,
        PosPosB=datos.PosPosB,
        PosInd=datos.PosInd,
        PosEstReg=datos.PosEstReg
    )
    db.add(nueva_posicion)
    db.commit()
    db.refresh(nueva_posicion)
    return nueva_posicion


# Listar posiciones de un mapa
@router.get("/mapas/{map_cod}/posiciones/", response_model=List[PosicionMapaOut])
def listar_posiciones(
    map_cod: int,
    usuario: Usuario = Depends(obtener_usuario_actual),
    db: Session = Depends(get_db)
):
    mapa = db.query(Mapa).filter(Mapa.MapCod == map_cod, Mapa.MapUsuCod == usuario.UsuCod).first()
    if not mapa:
        raise HTTPException(status_code=404, detail="Mapa no encontrado")

    return db.query(PosicionMapa).filter(PosicionMapa.PosMapCod == map_cod).all()


# Subir imagen de captura a una posición
@router.post("/posiciones/{pos_cod}/fotos/", response_model=ImagenCapturaOut)
def subir_foto_posicion(
    pos_cod: int,
    archivo: UploadFile = File(...),
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(obtener_usuario_actual)
):
    posicion = db.query(PosicionMapa).join(Mapa).filter(
        PosicionMapa.PosCod == pos_cod,
        Mapa.MapUsuCod == usuario.UsuCod
    ).first()

    if not posicion:
        raise HTTPException(status_code=404, detail="Posición no encontrada o no autorizada")

    carpeta_destino = Path("static") / IMAGEN_CAPTURA_PATH
    carpeta_destino.mkdir(parents=True, exist_ok=True)

    extension = archivo.filename.split('.')[-1]
    nombre_archivo = f"{pos_cod}_{uuid.uuid4().hex[:6]}.{extension}"
    ruta_archivo = carpeta_destino / nombre_archivo

    with open(ruta_archivo, "wb") as buffer:
        shutil.copyfileobj(archivo.file, buffer)

    imagen = ImagenCaptura(
        ImaUrlIma=nombre_archivo,
        ImaPosMapCod=pos_cod,
        ImaEstReg="A"
    )
    db.add(imagen)
    db.commit()
    db.refresh(imagen)

    imagen.ImaUrlIma = f"{IMAGEN_CAPTURA_URL}/{nombre_archivo}"
    return imagen


# Ver fotos de una posición
@router.get("/posiciones/{pos_cod}/fotos/", response_model=List[ImagenCapturaOut])
def ver_fotos_posicion(
    pos_cod: int,
    usuario: Usuario = Depends(obtener_usuario_actual),
    db: Session = Depends(get_db)
):
    posicion = db.query(PosicionMapa).join(Mapa).filter(
        PosicionMapa.PosCod == pos_cod,
        Mapa.MapUsuCod == usuario.UsuCod
    ).first()

    if not posicion:
        raise HTTPException(status_code=404, detail="Posición no encontrada")

    fotos = db.query(ImagenCaptura).filter(
        ImagenCaptura.ImaPosMapCod == pos_cod
    ).all()

    for f in fotos:
        if f.ImaUrlIma:
            f.ImaUrlIma = f"{IMAGEN_CAPTURA_URL}/{f.ImaUrlIma}"

    return fotos
# 🗑️ Eliminar una posición del mapa
@router.delete("/posiciones/{pos_cod}/", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_posicion(
    pos_cod: int,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(obtener_usuario_actual)
):
    posicion = db.query(PosicionMapa).join(Mapa).filter(
        PosicionMapa.PosCod == pos_cod,
        Mapa.MapUsuCod == usuario.UsuCod
    ).first()

    if not posicion:
        raise HTTPException(status_code=404, detail="Posición no encontrada o no autorizada")

    try:
        db.delete(posicion)
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error al eliminar la posición")


# 🗑️ Eliminar una foto de captura
@router.delete("/fotos/{foto_cod}/", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_foto_captura(
    foto_cod: int,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(obtener_usuario_actual)
):
    foto = db.query(ImagenCaptura).join(PosicionMapa).join(Mapa).filter(
        ImagenCaptura.ImaCod == foto_cod,
        Mapa.MapUsuCod == usuario.UsuCod
    ).first()

    if not foto:
        raise HTTPException(status_code=404, detail="Foto no encontrada o no autorizada")

    # También elimina el archivo físico del sistema (opcional)
    if foto.ImaUrlIma:
        ruta_fisica = Path("static") / IMAGEN_CAPTURA_PATH / foto.ImaUrlIma
        if ruta_fisica.exists():
            ruta_fisica.unlink(missing_ok=True)

    try:
        db.delete(foto)
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error al eliminar la imagen")