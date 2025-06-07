from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from models import Usuario
from .schemas import (
    LoginRequest, LoginResponse, CambioContraseñaRequest,
    UsuarioUpdate, UsuarioOut, UsuarioCreate
)
from .auth import verificar_contraseña, crear_token_acceso, hashear_contraseña, obtener_usuario_actual
from database import get_db
import shutil, os, uuid
from pathlib import Path
from config import FOTO_PERFIL_URL, FOTO_PERFIL_PATH

router = APIRouter()

# Registro de usuario
@router.post("/registro")
def registrar_usuario(datos: UsuarioCreate, db: Session = Depends(get_db)):
    if db.query(Usuario).filter(Usuario.UsuNumWha == datos.UsuNumWha).first():
        raise HTTPException(status_code=400, detail="El número de WhatsApp ya está registrado.")

    nuevo_usuario = Usuario(
        UsuNom=datos.UsuNom,
        UsuNumWha=datos.UsuNumWha,
        UsuCon=hashear_contraseña(datos.UsuCon),
        UsuEstReg="A"
    )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return {"mensaje": "Usuario registrado con éxito", "usuario_id": nuevo_usuario.UsuCod}


# Login por número de WhatsApp
@router.post("/login", response_model=LoginResponse)
def login_usuario(request: LoginRequest, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.UsuNumWha == request.UsuNumWha).first()

    if not usuario or not verificar_contraseña(request.UsuCon, usuario.UsuCon):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    token = crear_token_acceso(data={"sub": str(usuario.UsuCod)})
    url_imagen = f"{FOTO_PERFIL_URL}/{usuario.UsuUrlImaPer}" if usuario.UsuUrlImaPer else None

    usuario_data = UsuarioOut(
        UsuCod=usuario.UsuCod,
        UsuNom=usuario.UsuNom,
        UsuNumWha=usuario.UsuNumWha,
        UsuEstReg=usuario.UsuEstReg,
        UsuUrlImaPer=url_imagen
    )

    return {
        "access_token": token,
        "token_type": "bearer",
        "usuario": usuario_data
    }


# Cambio de contraseña (requiere token)
@router.post("/cambiar-contrasena")
def cambiar_contrasena(
    datos: CambioContraseñaRequest,
    usuario: Usuario = Depends(obtener_usuario_actual),
    db: Session = Depends(get_db)
):
    if not verificar_contraseña(datos.password_actual, usuario.UsuCon):
        raise HTTPException(status_code=400, detail="Contraseña actual incorrecta")

    usuario.UsuCon = hashear_contraseña(datos.nueva_password)
    db.add(usuario)
    db.commit()

    return {"mensaje": "Contraseña cambiada con éxito"}


# Actualizar datos de usuario
@router.put("/actualizar")
def actualizar_datos_usuario(
    datos: UsuarioUpdate,
    usuario: Usuario = Depends(obtener_usuario_actual),
    db: Session = Depends(get_db)
):
    for campo, valor in datos.dict(exclude_unset=True).items():
        setattr(usuario, campo, valor)
    db.commit()
    return {"mensaje": "Datos del usuario actualizados"}


# Eliminar imagen de perfil
@router.delete("/imagen-perfil")
def eliminar_imagen_perfil(
    usuario: Usuario = Depends(obtener_usuario_actual),
    db: Session = Depends(get_db)
):
    if usuario.UsuUrlImaPer:
        ruta_archivo = Path("static") / FOTO_PERFIL_PATH / usuario.UsuUrlImaPer
        if ruta_archivo.exists():
            ruta_archivo.unlink()
        usuario.UsuUrlImaPer = None
        db.commit()

    return {"mensaje": "Imagen de perfil eliminada"}


# Subir imagen de perfil
@router.post("/imagen-perfil")
def subir_imagen_perfil(
    archivo: UploadFile = File(...),
    usuario: Usuario = Depends(obtener_usuario_actual),
    db: Session = Depends(get_db)
):
    carpeta_destino = Path("static") / FOTO_PERFIL_PATH
    carpeta_destino.mkdir(parents=True, exist_ok=True)

    extension = archivo.filename.split(".")[-1]
    nombre_base = archivo.filename.rsplit(".", 1)[0].replace(" ", "")
    nombre_unico = f"{usuario.UsuCod}_{uuid.uuid4().hex[:6]}_{nombre_base}.{extension}"
    ruta_archivo = carpeta_destino / nombre_unico

    # Eliminar imagen anterior si existe
    if usuario.UsuUrlImaPer:
        anterior = carpeta_destino / usuario.UsuUrlImaPer
        if anterior.exists():
            anterior.unlink()

    # Guardar nueva imagen
    with open(ruta_archivo, "wb") as buffer:
        shutil.copyfileobj(archivo.file, buffer)

    usuario.UsuUrlImaPer = nombre_unico
    db.commit()

    return {
        "mensaje": "Imagen de perfil actualizada",
        "nombre_archivo": nombre_unico,
        "UsuUrlImaPer": f"{FOTO_PERFIL_URL}/{nombre_unico}"
    }
