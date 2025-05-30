#usuario,rol,permiso,permiso_permitido_rol,asignación_rol_usuario,cambio_contraseña,bloqueo_intentos,bitacora_usuario
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from models import Usuario,CambioContrasena,AsignacionRolUsuario
from schemas import LoginRequest, LoginResponse, CambioContraseñaRequest,AsignacionCreate,UsuarioUpdate,UsuarioOut
from auth import verificar_contraseña, crear_token_acceso,hashear_contraseña
from datetime import date
from database import get_db
import shutil, os, uuid
from pathlib import Path
from config import FOTO_PERFIL_URL, FOTO_PERFIL_PATH

router = APIRouter()

@router.post("/login", response_model=LoginResponse)
def login_usuario(request: LoginRequest, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.UsuEma == request.email).first()

    if not usuario or not verificar_contraseña(request.contraseña, usuario.UsuCon):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    token = crear_token_acceso(data={"sub": str(usuario.UsuCod)})

    # Armar la URL completa de la imagen
    url_foto = f"{FOTO_PERFIL_URL}/{usuario.UsuUrlFotPer}" if usuario.UsuUrlFotPer else None

    usuario_data = UsuarioOut(
        id=usuario.UsuCod,
        nombre=usuario.UsuNom,
        email=usuario.UsuEma,
        nombre_usuario=usuario.UsuNomUsu,
        idioma_preferido=usuario.UsuIdiPre,
        fecha_creacion=usuario.UsuFecCre,
        estado=usuario.UsuEstReg,
        imagen_perfil=url_foto
    )

    return {
        "access_token": token,
        "token_type": "bearer",
        "usuario": usuario_data
    }

@router.get("/usuarios/{usuario_id}", response_model=UsuarioOut)
def obtener_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.UsuCod == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Armar la URL completa de la imagen de perfil si tiene
    url_foto = f"{FOTO_PERFIL_URL}/{usuario.UsuUrlFotPer}" if usuario.UsuUrlFotPer else None

    return UsuarioOut(
        id=usuario.UsuCod,
        nombre=usuario.UsuNom,
        email=usuario.UsuEma,
        nombre_usuario=usuario.UsuNomUsu,
        idioma_preferido=usuario.UsuIdiPre,
        fecha_creacion=usuario.UsuFecCre,
        estado=usuario.UsuEstReg,
        imagen_perfil=url_foto
    )

@router.post("/usuarios/{usuario_id}/cambiar-contrasena")
def cambiar_contrasena(usuario_id: int, datos: CambioContraseñaRequest, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.UsuCod == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    if not verificar_contraseña(datos.contraseña_actual, usuario.UsuCon):
        raise HTTPException(status_code=400, detail="Contraseña actual incorrecta")

    usuario.UsuCon = hashear_contraseña(datos.nueva_contraseña)
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

@router.put("/usuarios/{usuario_id}")
def actualizar_datos_usuario(usuario_id: int, datos: UsuarioUpdate, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.UsuCod == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    mapeo = {
        "Nom": "UsuNom",
        "Ema": "UsuEma",
        "NomUsu": "UsuNomUsu",
        "IdiPre": "UsuIdiPre"
    }

    for campo, valor in datos.dict(exclude_unset=True).items():
        setattr(usuario, mapeo[campo], valor)

    db.commit()
    return {"mensaje": "Datos del usuario actualizados"}


@router.delete("/usuarios/{usuario_id}/imagen-perfil")
def eliminar_imagen_perfil(usuario_id: int, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.UsuCod == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    if usuario.UsuUrlFotPer:
        ruta_archivo = Path("static") / FOTO_PERFIL_PATH / usuario.UsuUrlFotPer
        if ruta_archivo.exists():
            ruta_archivo.unlink()

        usuario.UsuUrlFotPer = None
        db.commit()

    return {"mensaje": "Imagen de perfil eliminada"}

@router.post("/usuarios/{usuario_id}/imagen-perfil")
def subir_imagen_perfil(
    usuario_id: int,
    archivo: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    usuario = db.query(Usuario).filter(Usuario.UsuCod == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    carpeta_destino = Path("static") / FOTO_PERFIL_PATH
    carpeta_destino.mkdir(parents=True, exist_ok=True)

    extension = archivo.filename.split(".")[-1]
    nombre_base = archivo.filename.rsplit(".", 1)[0].replace(" ", "")
    nombre_unico = f"{usuario_id}_{uuid.uuid4().hex[:6]}_{nombre_base}.{extension}"
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
        "url": f"{FOTO_PERFIL_URL}/{nombre_unico}"
    }

@router.post("/asignaciones")
def crear_asignacion(asignacion: AsignacionCreate, db: Session = Depends(get_db)):
    nueva = AsignacionRolUsuario(
        AsiUsuCod=asignacion.usuario_id,
        AsiRolCod=asignacion.rol_id,
        AsiParCod=asignacion.parcela_id,
        AsiCulCod=asignacion.cultivo_id,
        AsiFecAsi=asignacion.fecha_asignacion,
        AsiEstReg="A"
    )
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva

@router.put("/asignaciones/{asignacion_id}/estado")
def cambiar_estado_asignacion(asignacion_id: int, nuevo_estado: str, db: Session = Depends(get_db)):
    asignacion = db.query(AsignacionRolUsuario).filter(AsignacionRolUsuario.AsiCod == asignacion_id).first()
    if not asignacion:
        raise HTTPException(status_code=404, detail="Asignación no encontrada")

    asignacion.AsiEstReg = nuevo_estado
    db.commit()
    return {"mensaje": f"Estado de asignación actualizado a '{nuevo_estado}'"}

@router.delete("/asignaciones/{asignacion_id}")
def eliminar_asignacion(asignacion_id: int, db: Session = Depends(get_db)):
    asignacion = db.query(AsignacionRolUsuario).filter(AsignacionRolUsuario.AsiCod == asignacion_id).first()
    if not asignacion:
        raise HTTPException(status_code=404, detail="Asignación no encontrada")

    db.delete(asignacion)
    db.commit()
    return {"mensaje": "Asignación eliminada"}
