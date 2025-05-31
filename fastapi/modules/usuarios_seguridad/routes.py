#usuario,rol,permiso,permiso_permitido_rol,asignación_rol_usuario,cambio_contraseña,bloqueo_intentos,bitacora_usuario
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from models import Usuario,CambioContrasena,AsignacionRolUsuario
from .schemas import LoginRequest, LoginResponse, CambioContraseñaRequest,AsignacionCreate,UsuarioUpdate,UsuarioOut,UsuarioCreate
from .auth import verificar_contraseña, crear_token_acceso,hashear_contraseña
from datetime import date
from database import get_db
import shutil, os, uuid
from pathlib import Path
from config import FOTO_PERFIL_URL, FOTO_PERFIL_PATH

router = APIRouter()

@router.post("/registro")
def registrar_usuario(datos: UsuarioCreate, db: Session = Depends(get_db)):
    if db.query(Usuario).filter(Usuario.UsuEma == datos.UsuEma).first():
        raise HTTPException(status_code=400, detail="El correo electrónico ya está registrado.")
    if db.query(Usuario).filter(Usuario.UsuNomUsu == datos.UsuNomUsu).first():
        raise HTTPException(status_code=400, detail="El nombre de usuario ya está en uso.")
    nuevo_usuario = Usuario(
        UsuNom=datos.UsuNom,
        UsuEma=datos.UsuEma,
        UsuNomUsu=datos.UsuNomUsu,
        UsuCon=hashear_contraseña(datos.UsuCon),
        UsuIdiPre=datos.UsuIdiPre,
        UsuFecCre=date.today(),
        UsuEstReg="A"
    )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return {"mensaje": "Usuario registrado con éxito", "usuario_id": nuevo_usuario.UsuCod}

@router.post("/login", response_model=LoginResponse)
def login_usuario(request: LoginRequest, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(
        (Usuario.UsuEma == request.identificador) | (Usuario.UsuNomUsu == request.identificador)
    ).first()
    if not usuario or not verificar_contraseña(request.UsuCon, usuario.UsuCon):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    token = crear_token_acceso(data={"sub": str(usuario.UsuCod)})
    # Armar la URL completa de la imagen
    url_foto = f"{FOTO_PERFIL_URL}/{usuario.UsuUrlFotPer}" if usuario.UsuUrlFotPer else None
    usuario_data = UsuarioOut(
        UsuCod=usuario.UsuCod,
        UsuNom=usuario.UsuNom,
        UsuEma=usuario.UsuEma,
        UsuNomUsu=usuario.UsuNomUsu,
        UsuIdiPre=usuario.UsuIdiPre,
        UsuFecCre=usuario.UsuFecCre,
        UsuEstReg=usuario.UsuEstReg,
        UsuUrlFotPer=url_foto
    )
    return {
        "access_token": token,
        "token_type": "bearer",
        "usuario": usuario_data
    }

@router.post("/{UsuCod}/cambiar-contrasena")
def cambiar_contrasena(UsuCod: int, datos: CambioContraseñaRequest, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.UsuCod == UsuCod).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    if not verificar_contraseña(datos.password_actual, usuario.UsuCon):
        raise HTTPException(status_code=400, detail="Contraseña actual incorrecta")
    usuario.UsuCon = hashear_contraseña(datos.nueva_password)
    db.add(usuario)
    cambio = CambioContrasena(
        CamUsuCod=usuario.UsuCod,
        CamFec=date.today(),
        CamMet="manual",
        CamOri=datos.ip,
        CamEstReg="A"
    )
    db.add(cambio)
    db.commit()
    return {"mensaje": "Contraseña cambiada con éxito"}

@router.put("/{UsuCod}")
def actualizar_datos_usuario(UsuCod: int, datos: UsuarioUpdate, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.UsuCod == UsuCod).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    for campo, valor in datos.dict(exclude_unset=True).items():
        setattr(usuario, campo, valor)
    db.commit()
    return {"mensaje": "Datos del usuario actualizados"}

@router.delete("/{UsuCod}/imagen-perfil")
def eliminar_imagen_perfil(UsuCod: int, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.UsuCod == UsuCod).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    if usuario.UsuUrlFotPer:
        ruta_archivo = Path("static") / FOTO_PERFIL_PATH / usuario.UsuUrlFotPer
        if ruta_archivo.exists():
            ruta_archivo.unlink()
        usuario.UsuUrlFotPer = None
        db.commit()

    return {"mensaje": "Imagen de perfil eliminada"}

@router.post("/{UsuCod}/imagen-perfil")
def subir_imagen_perfil(
    UsuCod: int,
    archivo: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    usuario = db.query(Usuario).filter(Usuario.UsuCod == UsuCod).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    carpeta_destino = Path("static") / FOTO_PERFIL_PATH
    carpeta_destino.mkdir(parents=True, exist_ok=True)

    extension = archivo.filename.split(".")[-1]
    nombre_base = archivo.filename.rsplit(".", 1)[0].replace("","")
    nombre_unico = f"{UsuCod}_{uuid.uuid4().hex[:6]}_{nombre_base}.{extension}"
    ruta_archivo = carpeta_destino / nombre_unico

    # Eliminar imagen anterior
    if usuario.UsuUrlFotPer:
        anterior = carpeta_destino / usuario.UsuUrlFotPer
        if anterior.exists():
            anterior.unlink()

    # Guardar archivo
    with open(ruta_archivo, "wb") as buffer:
        shutil.copyfileobj(archivo.file, buffer)

    usuario.UsuUrlFotPer = nombre_unico
    db.commit()

    return {
        "mensaje": "Imagen de perfil actualizada",
        "nombre_archivo": nombre_unico,
        "UsuUrlFotPer": f"{FOTO_PERFIL_URL}/{nombre_unico}"
    }

@router.post("/asignaciones")
def crear_asignacion(asignacion: AsignacionCreate, db: Session = Depends(get_db)):
    nueva = AsignacionRolUsuario(
        AsiUsuCod=asignacion.AsiUsuCod,
        AsiRolCod=asignacion.AsiRolCod,
        AsiParCod=asignacion.AsiParCod,
        AsiCulCod=asignacion.AsiCulCod,
        AsiFecAsi=asignacion.AsiFecAsi,
        AsiEstReg="A"
    )
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva

@router.put("/asignaciones/{asignacion_id}/estado")
def cambiar_estado_asignacion(AsiCod: int, nuevo_estado: str, db: Session = Depends(get_db)):
    asignacion = db.query(AsignacionRolUsuario).filter(AsignacionRolUsuario.AsiCod == AsiCod).first()
    if not asignacion:
        raise HTTPException(status_code=404, detail="Asignación no encontrada")

    asignacion.AsiEstReg = nuevo_estado
    db.commit()
    return {"mensaje": f"Estado de asignación actualizado a '{nuevo_estado}'"}

@router.delete("/asignaciones/{asignacion_id}")
def eliminar_asignacion(AsiCod: int, db: Session = Depends(get_db)):
    asignacion = db.query(AsignacionRolUsuario).filter(AsignacionRolUsuario.AsiCod == AsiCod).first()
    if not asignacion:
        raise HTTPException(status_code=404, detail="Asignación no encontrada")

    db.delete(asignacion)
    db.commit()
    return {"mensaje": "Asignación eliminada"}
