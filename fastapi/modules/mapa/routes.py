from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from pathlib import Path
import shutil, uuid

from models import Mapa, Usuario
from database import get_db
from .schemas import MapaCreate, MapaUpdate, MapaOut
from modules.usuario.auth import obtener_usuario_actual
from config import IMAGEN_MAPA_PATH, IMAGEN_MAPA_URL

router = APIRouter()


@router.post("/", response_model=MapaOut)
def crear_mapa(
    datos: MapaCreate,
    usuario: Usuario = Depends(obtener_usuario_actual),
    db: Session = Depends(get_db)
):
    nuevo_mapa = Mapa(
        MapNom=datos.MapNom,
        MapUrlIma=datos.MapUrlIma,
        MapEstReg=datos.MapEstReg,
        MapUsuCod=usuario.UsuCod
    )
    db.add(nuevo_mapa)
    db.commit()
    db.refresh(nuevo_mapa)
    return nuevo_mapa


@router.get("/", response_model=list[MapaOut])
def listar_mapas(
    usuario: Usuario = Depends(obtener_usuario_actual),
    db: Session = Depends(get_db)
):
    mapas = db.query(Mapa).filter(Mapa.MapUsuCod == usuario.UsuCod).all()

    # Construir URL completa
    for mapa in mapas:
        if mapa.MapUrlIma:
            mapa.MapUrlIma = f"{IMAGEN_MAPA_URL}/{mapa.MapUrlIma}"

    return mapas



@router.get("/{map_cod}", response_model=MapaOut)
def ver_mapa(
    map_cod: int,
    usuario: Usuario = Depends(obtener_usuario_actual),
    db: Session = Depends(get_db)
):
    mapa = db.query(Mapa).filter(Mapa.MapCod == map_cod, Mapa.MapUsuCod == usuario.UsuCod).first()
    if not mapa:
        raise HTTPException(status_code=404, detail="Mapa no encontrado")

    if mapa.MapUrlIma:
        mapa.MapUrlIma = f"{IMAGEN_MAPA_URL}/{mapa.MapUrlIma}"

    return mapa



@router.put("/{map_cod}", response_model=MapaOut)
def modificar_mapa(
    map_cod: int,
    datos: MapaUpdate,
    usuario: Usuario = Depends(obtener_usuario_actual),
    db: Session = Depends(get_db)
):
    mapa = db.query(Mapa).filter(Mapa.MapCod == map_cod, Mapa.MapUsuCod == usuario.UsuCod).first()
    if not mapa:
        raise HTTPException(status_code=404, detail="Mapa no encontrado")

    for campo, valor in datos.dict(exclude_unset=True).items():
        setattr(mapa, campo, valor)

    db.commit()
    db.refresh(mapa)
    return mapa


@router.delete("/{map_cod}")
def eliminar_mapa(
    map_cod: int,
    usuario: Usuario = Depends(obtener_usuario_actual),
    db: Session = Depends(get_db)
):
    mapa = db.query(Mapa).filter(Mapa.MapCod == map_cod, Mapa.MapUsuCod == usuario.UsuCod).first()
    if not mapa:
        raise HTTPException(status_code=404, detail="Mapa no encontrado")

    # Eliminar imagen asociada si existe
    if mapa.MapUrlIma:
        ruta = Path("static") / IMAGEN_MAPA_PATH / mapa.MapUrlIma
        if ruta.exists():
            ruta.unlink()

    db.delete(mapa)
    db.commit()
    return {"mensaje": "Mapa eliminado correctamente"}


@router.post("/{map_cod}/imagen")
def subir_imagen_mapa(
    map_cod: int,
    archivo: UploadFile = File(...),
    usuario: Usuario = Depends(obtener_usuario_actual),
    db: Session = Depends(get_db)
):
    mapa = db.query(Mapa).filter(Mapa.MapCod == map_cod, Mapa.MapUsuCod == usuario.UsuCod).first()
    if not mapa:
        raise HTTPException(status_code=404, detail="Mapa no encontrado")

    carpeta_destino = Path("static") / IMAGEN_MAPA_PATH
    carpeta_destino.mkdir(parents=True, exist_ok=True)

    extension = archivo.filename.split('.')[-1]
    nombre_archivo = f"{map_cod}_{uuid.uuid4().hex[:6]}.{extension}"
    ruta_archivo = carpeta_destino / nombre_archivo

    # Eliminar imagen anterior si existe
    if mapa.MapUrlIma:
        anterior = carpeta_destino / mapa.MapUrlIma
        if anterior.exists():
            anterior.unlink()

    with open(ruta_archivo, "wb") as buffer:
        shutil.copyfileobj(archivo.file, buffer)

    mapa.MapUrlIma = nombre_archivo
    db.commit()

    return {
        "mensaje": "Imagen del mapa actualizada",
        "nombre_archivo": nombre_archivo,
        "MapUrlIma": f"{IMAGEN_MAPA_URL}/{nombre_archivo}"
    }


@router.delete("/{map_cod}/imagen")
def eliminar_imagen_mapa(
    map_cod: int,
    usuario: Usuario = Depends(obtener_usuario_actual),
    db: Session = Depends(get_db)
):
    mapa = db.query(Mapa).filter(Mapa.MapCod == map_cod, Mapa.MapUsuCod == usuario.UsuCod).first()
    if not mapa:
        raise HTTPException(status_code=404, detail="Mapa no encontrado")

    if mapa.MapUrlIma:
        ruta_archivo = Path("static") / IMAGEN_MAPA_PATH / mapa.MapUrlIma
        if ruta_archivo.exists():
            ruta_archivo.unlink()
        mapa.MapUrlIma = None
        db.commit()

    return {"mensaje": "Imagen del mapa eliminada"}
