from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import or_
from sqlalchemy.orm import Session
from models import AsignacionRolUsuario, Cultivo, Parcela, Rol, Usuario
from database import get_db
from .schemas import (
    AsignacionRolUsuarioCreate,
    AsignacionRolUsuarioUpdate,
    AsignacionRolUsuarioOut
)

router = APIRouter()

# Crear una asignación
@router.post("/", response_model=AsignacionRolUsuarioOut)
def crear_asignacion(asignacion: AsignacionRolUsuarioCreate, db: Session = Depends(get_db)):
    if not asignacion.AsiParCod and not asignacion.AsiCulCod:
        raise HTTPException(status_code=400, detail="Debe asignarse a una parcela o cultivo.")

    if asignacion.AsiParCod and asignacion.AsiCulCod:
        raise HTTPException(status_code=400, detail="Solo puede asignarse a una parcela o un cultivo, no ambos.")

    nueva = AsignacionRolUsuario(**asignacion.dict(), AsiEstReg='A')
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva

@router.get("/dueno/{dueno_id}", response_model=list[AsignacionRolUsuarioOut])
def obtener_asignaciones_por_dueno(dueno_id: int, db: Session = Depends(get_db)):
    # Subquery de parcelas del dueño
    parcelas_ids = db.query(Parcela.ParCod).filter(Parcela.ParUsuCod == dueno_id)
    
    # Subquery de cultivos del dueño
    cultivos_ids = db.query(Cultivo.CulCod).filter(Cultivo.CulUsuCod == dueno_id)
    
    # Asignaciones a esas parcelas o cultivos
    asignaciones = db.query(AsignacionRolUsuario).filter(
        (AsignacionRolUsuario.AsiParCod.in_(parcelas_ids)) |
        (AsignacionRolUsuario.AsiCulCod.in_(cultivos_ids))
    ).all()

    return asignaciones


# Modificar una asignación
@router.put("/{asignacion_id}", response_model=AsignacionRolUsuarioOut)
def modificar_asignacion(asignacion_id: int, datos: AsignacionRolUsuarioUpdate, db: Session = Depends(get_db)):
    asignacion = db.query(AsignacionRolUsuario).filter_by(AsiCod=asignacion_id).first()
    if not asignacion:
        raise HTTPException(status_code=404, detail="Asignación no encontrada.")

    for key, value in datos.dict(exclude_unset=True).items():
        setattr(asignacion, key, value)

    db.commit()
    db.refresh(asignacion)
    return asignacion

# Cambiar estado (activar/desactivar) una asignación
@router.patch("/{asignacion_id}/estado", response_model=AsignacionRolUsuarioOut)
def cambiar_estado_asignacion(asignacion_id: int, nuevo_estado: str, db: Session = Depends(get_db)):
    if nuevo_estado not in ['A', 'I']:
        raise HTTPException(status_code=400, detail="Estado inválido. Use 'A' para activo o 'I' para inactivo.")

    asignacion = db.query(AsignacionRolUsuario).filter_by(AsiCod=asignacion_id).first()
    if not asignacion:
        raise HTTPException(status_code=404, detail="Asignación no encontrada.")

    asignacion.AsiEstReg = nuevo_estado
    db.commit()
    db.refresh(asignacion)
    return asignacion

# Eliminar lógicamente (marcar como inactivo)
@router.delete("/{asignacion_id}")
def eliminar_asignacion(asignacion_id: int, db: Session = Depends(get_db)):
    asignacion = db.query(AsignacionRolUsuario).filter_by(AsiCod=asignacion_id).first()
    if not asignacion:
        raise HTTPException(status_code=404, detail="Asignación no encontrada.")

    asignacion.AsiEstReg = 'I'
    db.commit()
    return {"mensaje": "Asignación desactivada correctamente."}

@router.get("/parcelas/dueno/{dueno_id}")
def obtener_parcelas_por_dueno(dueno_id: int, db: Session = Depends(get_db)):
    parcelas = db.query(Parcela).filter(
        Parcela.ParUsuCod == dueno_id,
        Parcela.ParEstReg == 'A'
    ).all()
    return parcelas

@router.get("/cultivos/dueno/{dueno_id}")
def obtener_cultivos_por_dueno(dueno_id: int, db: Session = Depends(get_db)):
    parcelas_ids = db.query(Parcela.ParCod).filter(Parcela.ParUsuCod == dueno_id)
    cultivos = db.query(Cultivo).filter(
        Cultivo.CulParCod.in_(parcelas_ids),
        Cultivo.CulEstReg == 'A'
    ).all()
    return cultivos

@router.get("/roles")
def obtener_roles(db: Session = Depends(get_db)):
    roles = db.query(Rol).filter(Rol.RolEstReg == 'A').all()
    return roles
@router.get("/usuarios/buscar")
def buscar_usuarios(
    filtro: str = Query(..., min_length=2),
    db: Session = Depends(get_db)
):
    usuarios = db.query(Usuario).filter(
        Usuario.UsuEstReg == 'A',
        or_(
            Usuario.UsuNom.ilike(f"%{filtro}%"),
            Usuario.UsuEma.ilike(f"%{filtro}%"),
            Usuario.UsuNomUsu.ilike(f"%{filtro}%")
        )
    ).all()
    return usuarios