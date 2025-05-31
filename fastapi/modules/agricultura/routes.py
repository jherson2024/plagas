#parcela_cultivo
from pathlib import Path
import shutil
import uuid
from fastapi import APIRouter, Depends, File, Form, HTTPException,Query, UploadFile
from sqlalchemy.orm import Session
from typing import List, Optional
from .schemas import CultivoOut, ParcelaIn, ParcelaOut, ParcelaResumen,ParcelaUpdate,ParcelaEstadoUpdate,CultivoBase,CultivoCreate,CultivoUpdate,CultivoEstadoUpdate
from models import Parcela, Cultivo  # Asumiendo que tus modelos están aquí
from database import get_db
from datetime import date
from config import IMAGEN_CULTIVO_PATH, IMAGEN_CULTIVO_URL
router = APIRouter()

@router.get("/parcelas/usuario/{UsuCod}", response_model=List[ParcelaOut])
def get_parcelas_by_usuario(UsuCod: int, db: Session = Depends(get_db)):
    parcelas = db.query(Parcela).filter(Parcela.ParUsuCod == UsuCod).all()
    return parcelas  # ✅ FastAPI usará ParcelaOut + orm_mode para serializar
# ------------------------
# CREAR PARCELA
# ------------------------
@router.post("/parcelas/", response_model=ParcelaOut)
def create_parcela(parcela_data: ParcelaIn, db: Session = Depends(get_db)):
    # 👇 Este dict excluye los campos que no fueron enviados
    data = parcela_data.dict(exclude_unset=True)

    # Establecer valores por defecto si no se enviaron
    data['ParFecReg'] = data.get('ParFecReg') or date.today()
    data['ParEstReg'] = data.get('ParEstReg') or 'A'

    nueva_parcela = Parcela(**data)
    db.add(nueva_parcela)
    db.commit()
    db.refresh(nueva_parcela)
    return nueva_parcela
# MODIFICAR PARCELA
# ------------------------
@router.put("/parcelas/{ParCod}", response_model=dict)
def update_parcela(ParCod: int, update_data: ParcelaUpdate, db: Session = Depends(get_db)):
    parcela = db.query(Parcela).filter(Parcela.ParCod == ParCod).first()
    if not parcela:
        raise HTTPException(status_code=404, detail="Parcela no encontrada")
    
    update_dict = update_data.dict(exclude_unset=True)
    for key, value in update_dict.items():
        setattr(parcela, key, value)

    db.commit()
    db.refresh(parcela)
    return {"message": "Parcela actualizada correctamente"}
# ------------------------
# ELIMINAR PARCELA
# ------------------------
@router.delete("/parcelas/{ParCod}")
def delete_parcela(ParCod: int, db: Session = Depends(get_db)):
    parcela = db.query(Parcela).filter(Parcela.ParCod == ParCod).first()
    if not parcela:
        raise HTTPException(status_code=404, detail="Parcela no encontrada")
    db.delete(parcela)
    db.commit()
    return {"detail": "Parcela eliminada"}

# ------------------------
# ELIMINAR CULTIVO
# ------------------------
@router.delete("/cultivos/{CulCod}")
def delete_cultivo(CulCod: int, db: Session = Depends(get_db)):
    cultivo = db.query(Cultivo).filter(Cultivo.CulCod == CulCod).first()
    if not cultivo:
        raise HTTPException(status_code=404, detail="Cultivo no encontrado")

    # 🧼 Eliminar la imagen del disco si existe
    if cultivo.CulUrlIma:
        ruta_archivo = Path("static") / "imagen_cultivo" / cultivo.CulUrlIma
        if ruta_archivo.exists():
            try:
                ruta_archivo.unlink()
                print(f"🧽 Imagen eliminada: {ruta_archivo}")
            except Exception as e:
                print(f"⚠️ No se pudo eliminar la imagen: {e}")

    db.delete(cultivo)
    db.commit()
    return {"detail": "Cultivo eliminado"}

@router.patch("/parcelas/{ParCod}/estado", response_model=dict)
def cambiar_estado_parcela(ParCod: int, estado_update: ParcelaEstadoUpdate, db: Session = Depends(get_db)):
    parcela = db.query(Parcela).filter(Parcela.ParCod == ParCod).first()
    if not parcela:
        raise HTTPException(status_code=404, detail="Parcela no encontrada")

    if estado_update.ParEstReg not in ["A", "I", "*"]:  # Opcional
        raise HTTPException(status_code=400, detail="Estado inválido")

    parcela.ParEstReg = estado_update.ParEstReg
    db.commit()
    db.refresh(parcela)

    return {"message": f"Estado actualizado a '{estado_update.ParEstReg}' correctamente"}

@router.post("/cultivos")
def crear_cultivo(
    CulNom: str = Form(...),
    CulParCod: int = Form(...),
    CulTip: Optional[str] = Form(None),
    CulFecSie: Optional[date] = Form(None),
    CulFecCos: Optional[date] = Form(None),
    CulPro: Optional[int] = Form(0),
    CulEstReg: Optional[str] = Form("A"),
    archivo: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    cultivo = Cultivo(
        CulNom=CulNom,
        CulParCod=CulParCod,
        CulTip=CulTip,
        CulFecSie=CulFecSie,
        CulFecCos=CulFecCos,
        CulPro=CulPro,
        CulEstReg=CulEstReg
    )

    if archivo:
        print("📥 Archivo recibido:", archivo.filename)

        carpeta_destino = Path("static") / "imagen_cultivo"
        carpeta_destino.mkdir(parents=True, exist_ok=True)

        extension = archivo.filename.split('.')[-1]
        nombre_archivo = f"{uuid.uuid4().hex[:8]}.{extension}"
        ruta_archivo = carpeta_destino / nombre_archivo

        print("🧾 Nombre generado para imagen:", nombre_archivo)
        print("📂 Ruta completa:", ruta_archivo)

        try:
            with open(ruta_archivo, "wb") as buffer:
                shutil.copyfileobj(archivo.file, buffer)
            print("✅ Imagen guardada exitosamente en el disco")
        except Exception as e:
            print("❌ Error al guardar imagen:", str(e))

        cultivo.CulUrlIma = nombre_archivo
        print("📦 Se asignó CulUrlIma al modelo:", cultivo.CulUrlIma)

    db.add(cultivo)
    db.commit()
    db.refresh(cultivo)

    return cultivo

@router.get("/cultivos/usuario/{UsuCod}", response_model=List[CultivoOut])
def get_cultivos_by_usuario(UsuCod: int, db: Session = Depends(get_db)):
    cultivos = (
        db.query(Cultivo)
        .join(Parcela, Cultivo.CulParCod == Parcela.ParCod)
        .filter(Parcela.ParUsuCod == UsuCod)
        .all()
    )
    return [CultivoOut.from_orm_with_url(c) for c in cultivos]

@router.put("/cultivos/{CulCod}")
def actualizar_cultivo(
    CulCod: int,
    CulNom: Optional[str] = Form(None),
    CulParCod: Optional[int] = Form(None),
    CulTip: Optional[str] = Form(None),
    CulFecSie: Optional[date] = Form(None),
    CulFecCos: Optional[date] = Form(None),
    CulPro: Optional[int] = Form(None),
    CulEstReg: Optional[str] = Form(None),
    archivo: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    cultivo = db.query(Cultivo).filter(Cultivo.CulCod == CulCod).first()
    if not cultivo:
        raise HTTPException(status_code=404, detail="Cultivo no encontrado")

    if CulNom is not None:
        cultivo.CulNom = CulNom
    if CulParCod is not None:
        cultivo.CulParCod = CulParCod
    if CulTip is not None:
        cultivo.CulTip = CulTip
    if CulFecSie is not None:
        cultivo.CulFecSie = CulFecSie
    if CulFecCos is not None:
        cultivo.CulFecCos = CulFecCos
    if CulPro is not None:
        cultivo.CulPro = CulPro
    if CulEstReg is not None:
        cultivo.CulEstReg = CulEstReg

    if archivo:
        carpeta_destino = Path("static") / "imagen_cultivo"
        carpeta_destino.mkdir(parents=True, exist_ok=True)

        extension = archivo.filename.split('.')[-1]
        nombre_archivo = f"{uuid.uuid4().hex[:8]}.{extension}"
        ruta_archivo = carpeta_destino / nombre_archivo

        # Eliminar imagen anterior
        if cultivo.CulUrlIma:
            ruta_anterior = carpeta_destino / cultivo.CulUrlIma
            if ruta_anterior.exists():
                ruta_anterior.unlink()

        with open(ruta_archivo, "wb") as buffer:
            shutil.copyfileobj(archivo.file, buffer)

        cultivo.CulUrlIma = nombre_archivo

    db.commit()
    db.refresh(cultivo)

    return cultivo

@router.patch("/cultivos/{CulCod}/estado", response_model=dict)
def cambiar_estado_cultivo(CulCod: int, estado: CultivoEstadoUpdate, db: Session = Depends(get_db)):
    cultivo = db.query(Cultivo).filter(Cultivo.CulCod == CulCod).first()
    if not cultivo:
        raise HTTPException(status_code=404, detail="Cultivo no encontrado")
    
    if estado.CulEstReg not in ["A", "I", "E"]:
        raise HTTPException(status_code=400, detail="Estado inválido")
    
    cultivo.CulEstReg = estado.CulEstReg
    db.commit()
    db.refresh(cultivo)
    return {"message": f"Estado actualizado a '{estado.CulEstReg}'"}
@router.get("/parcelas/usuario/{UsuCod}/resumen", response_model=List[ParcelaResumen])
def get_parcelas_resumen_by_usuario(UsuCod: int, db: Session = Depends(get_db)):
    parcelas = (
        db.query(Parcela.ParCod, Parcela.ParNom)
        .filter(Parcela.ParUsuCod == UsuCod)
        .all()
    )
    return parcelas
