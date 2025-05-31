from typing import List, Optional

from sqlalchemy import CHAR, DECIMAL, Date, ForeignKeyConstraint, Index, Integer, String
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
import datetime
import decimal

class Base(DeclarativeBase):
    pass


class Modelo(Base):
    __tablename__ = 'modelo'
    __table_args__ = (
        Index('ModNom', 'ModNom', unique=True),
    )

    ModCod: Mapped[int] = mapped_column(Integer, primary_key=True)
    ModNom: Mapped[str] = mapped_column(String(80))
    ModVer: Mapped[str] = mapped_column(String(20))
    ModFecEnt: Mapped[Optional[datetime.date]] = mapped_column(Date)
    ModPre: Mapped[Optional[decimal.Decimal]] = mapped_column(DECIMAL(10, 0))
    ModDes: Mapped[Optional[str]] = mapped_column(String(160))
    ModTipArq: Mapped[Optional[str]] = mapped_column(String(40))
    ModDatUsa: Mapped[Optional[str]] = mapped_column(String(80))
    ModUltAct: Mapped[Optional[datetime.date]] = mapped_column(Date)
    ModEstReg: Mapped[Optional[str]] = mapped_column(CHAR(1))

    evaluacion_modelo: Mapped[List['EvaluacionModelo']] = relationship('EvaluacionModelo', back_populates='modelo')
    analisis: Mapped[List['Analisis']] = relationship('Analisis', back_populates='modelo')
    recomendacion: Mapped[List['Recomendacion']] = relationship('Recomendacion', back_populates='modelo')


class NivelesAlerta(Base):
    __tablename__ = 'niveles_alerta'
    __table_args__ = (
        Index('NivCodi', 'NivCodi', unique=True),
        Index('NivNom', 'NivNom', unique=True)
    )

    NivCod: Mapped[int] = mapped_column(Integer, primary_key=True)
    NivNom: Mapped[str] = mapped_column(String(40))
    NivCodi: Mapped[int] = mapped_column(Integer)
    NivDes: Mapped[Optional[str]] = mapped_column(String(160))
    NivEstReg: Mapped[Optional[str]] = mapped_column(CHAR(1))

    alerta: Mapped[List['Alerta']] = relationship('Alerta', back_populates='niveles_alerta')


class Permiso(Base):
    __tablename__ = 'permiso'
    __table_args__ = (
        Index('PerNom', 'PerNom', unique=True),
    )

    PerCod: Mapped[int] = mapped_column(Integer, primary_key=True)
    PerNom: Mapped[str] = mapped_column(String(80))
    PerDes: Mapped[Optional[str]] = mapped_column(String(120))
    PerEstReg: Mapped[Optional[str]] = mapped_column(CHAR(1))

    permiso_permitido_rol: Mapped[List['PermisoPermitidoRol']] = relationship('PermisoPermitidoRol', back_populates='permiso')


class Plaga(Base):
    __tablename__ = 'plaga'
    __table_args__ = (
        Index('PlaNom', 'PlaNom', unique=True),
    )

    PlaCod: Mapped[int] = mapped_column(Integer, primary_key=True)
    PlaNom: Mapped[str] = mapped_column(String(80))
    PlaTip: Mapped[Optional[str]] = mapped_column(String(40))
    PlaDes: Mapped[Optional[str]] = mapped_column(String(160))
    PlaTraRec: Mapped[Optional[str]] = mapped_column(String(160))
    PlaEstReg: Mapped[Optional[str]] = mapped_column(CHAR(1))

    fotografia: Mapped[List['Fotografia']] = relationship('Fotografia', back_populates='plaga')
    analisis: Mapped[List['Analisis']] = relationship('Analisis', back_populates='plaga')
    infestacion_plaga: Mapped[List['InfestacionPlaga']] = relationship('InfestacionPlaga', back_populates='plaga')
    alerta_por_plaga: Mapped[List['AlertaPorPlaga']] = relationship('AlertaPorPlaga', back_populates='plaga')


class Rol(Base):
    __tablename__ = 'rol'
    __table_args__ = (
        Index('RolNom', 'RolNom', unique=True),
    )

    RolCod: Mapped[int] = mapped_column(Integer, primary_key=True)
    RolNom: Mapped[str] = mapped_column(String(40))
    RolDes: Mapped[Optional[str]] = mapped_column(String(160))
    RolEstReg: Mapped[Optional[str]] = mapped_column(CHAR(1))

    permiso_permitido_rol: Mapped[List['PermisoPermitidoRol']] = relationship('PermisoPermitidoRol', back_populates='rol')
    asignacion_rol_usuario: Mapped[List['AsignacionRolUsuario']] = relationship('AsignacionRolUsuario', back_populates='rol')


class Severidad(Base):
    __tablename__ = 'severidad'
    __table_args__ = (
        Index('SevNom', 'SevNom', unique=True),
    )

    SevCod: Mapped[int] = mapped_column(Integer, primary_key=True)
    SevNom: Mapped[str] = mapped_column(String(40))
    SevNivRie: Mapped[int] = mapped_column(Integer)
    SevDes: Mapped[Optional[str]] = mapped_column(String(160))
    SevEstReg: Mapped[Optional[str]] = mapped_column(CHAR(1))

    analisis: Mapped[List['Analisis']] = relationship('Analisis', back_populates='severidad')
    infestacion_plaga: Mapped[List['InfestacionPlaga']] = relationship('InfestacionPlaga', back_populates='severidad')
    alerta_por_plaga: Mapped[List['AlertaPorPlaga']] = relationship('AlertaPorPlaga', back_populates='severidad')
    evaluacion_tratamiento: Mapped[List['EvaluacionTratamiento']] = relationship('EvaluacionTratamiento', back_populates='severidad')


class TipoAccion(Base):
    __tablename__ = 'tipo_accion'
    __table_args__ = (
        Index('TipNom', 'TipNom', unique=True),
    )

    TipCod: Mapped[int] = mapped_column(Integer, primary_key=True)
    TipNom: Mapped[str] = mapped_column(String(40))
    TipDes: Mapped[Optional[str]] = mapped_column(String(160))
    TipCla: Mapped[Optional[str]] = mapped_column(String(40))
    TipEstReg: Mapped[Optional[str]] = mapped_column(CHAR(1))

    accion_usuario: Mapped[List['AccionUsuario']] = relationship('AccionUsuario', back_populates='tipo_accion')


class Usuario(Base):
    __tablename__ = 'usuario'
    __table_args__ = (
        Index('UsuEma', 'UsuEma', unique=True),
        Index('UsuNom', 'UsuNom', unique=True),
        Index('UsuNomUsu', 'UsuNomUsu', unique=True)
    )

    UsuCod: Mapped[int] = mapped_column(Integer, primary_key=True)
    UsuNom: Mapped[str] = mapped_column(String(80))
    UsuEma: Mapped[str] = mapped_column(String(60))
    UsuNomUsu: Mapped[str] = mapped_column(String(60))
    UsuCon: Mapped[str] = mapped_column(String(60))
    UsuFecCre: Mapped[datetime.date] = mapped_column(Date)
    UsuIdiPre: Mapped[Optional[str]] = mapped_column(String(40))
    UsuUrlFotPer: Mapped[Optional[str]] = mapped_column(String(60))
    UsuEstReg: Mapped[Optional[str]] = mapped_column(CHAR(1))

    bitacora_usuario: Mapped[List['BitacoraUsuario']] = relationship('BitacoraUsuario', back_populates='usuario')
    bloqueo_intentos: Mapped[List['BloqueoIntentos']] = relationship('BloqueoIntentos', back_populates='usuario')
    cambio_contrasena: Mapped[List['CambioContrasena']] = relationship('CambioContrasena', back_populates='usuario')
    parcela: Mapped[List['Parcela']] = relationship('Parcela', back_populates='usuario')
    accion_usuario: Mapped[List['AccionUsuario']] = relationship('AccionUsuario', back_populates='usuario')
    asignacion_rol_usuario: Mapped[List['AsignacionRolUsuario']] = relationship('AsignacionRolUsuario', back_populates='usuario')
    recomendacion: Mapped[List['Recomendacion']] = relationship('Recomendacion', back_populates='usuario')
    alerta: Mapped[List['Alerta']] = relationship('Alerta', back_populates='usuario')
    alerta_por_plaga: Mapped[List['AlertaPorPlaga']] = relationship('AlertaPorPlaga', back_populates='usuario')
    tratamiento_plaga: Mapped[List['TratamientoPlaga']] = relationship('TratamientoPlaga', back_populates='usuario')


class BitacoraUsuario(Base):
    __tablename__ = 'bitacora_usuario'
    __table_args__ = (
        ForeignKeyConstraint(['BitUsuCod'], ['usuario.UsuCod'], name='bitacora_usuario_ibfk_1'),
        Index('BitFecHor', 'BitFecHor', unique=True),
        Index('BitUsuCod', 'BitUsuCod')
    )

    BitCod: Mapped[int] = mapped_column(Integer, primary_key=True)
    BitFecHor: Mapped[datetime.date] = mapped_column(Date)
    BitUsuCod: Mapped[int] = mapped_column(Integer)
    BitAcc: Mapped[str] = mapped_column(String(100))
    BitDes: Mapped[Optional[str]] = mapped_column(String(160))
    BitOri: Mapped[Optional[str]] = mapped_column(String(40))
    BitEstReg: Mapped[Optional[str]] = mapped_column(CHAR(1))

    usuario: Mapped['Usuario'] = relationship('Usuario', back_populates='bitacora_usuario')


class BloqueoIntentos(Base):
    __tablename__ = 'bloqueo_intentos'
    __table_args__ = (
        ForeignKeyConstraint(['BloUsuCod'], ['usuario.UsuCod'], name='bloqueo_intentos_ibfk_1'),
        Index('BloUsuCod', 'BloUsuCod')
    )

    BloCod: Mapped[int] = mapped_column(Integer, primary_key=True)
    BloUsuCod: Mapped[int] = mapped_column(Integer)
    BloFecBlo: Mapped[datetime.date] = mapped_column(Date)
    BloInt: Mapped[int] = mapped_column(Integer)
    BloMot: Mapped[Optional[str]] = mapped_column(String(160))
    BloEstReg: Mapped[Optional[str]] = mapped_column(CHAR(1))

    usuario: Mapped['Usuario'] = relationship('Usuario', back_populates='bloqueo_intentos')


class CambioContrasena(Base):
    __tablename__ = 'cambio_contrasena'
    __table_args__ = (
        ForeignKeyConstraint(['CamUsuCod'], ['usuario.UsuCod'], name='cambio_contrasena_ibfk_1'),
        Index('CamUsuCod', 'CamUsuCod')
    )

    CamCod: Mapped[int] = mapped_column(Integer, primary_key=True)
    CamUsuCod: Mapped[int] = mapped_column(Integer)
    CamFec: Mapped[datetime.date] = mapped_column(Date)
    CamMet: Mapped[Optional[str]] = mapped_column(String(40))
    CamOri: Mapped[Optional[str]] = mapped_column(String(40))
    CamEstReg: Mapped[Optional[str]] = mapped_column(CHAR(1))

    usuario: Mapped['Usuario'] = relationship('Usuario', back_populates='cambio_contrasena')


class EvaluacionModelo(Base):
    __tablename__ = 'evaluacion_modelo'
    __table_args__ = (
        ForeignKeyConstraint(['EvaModCod'], ['modelo.ModCod'], name='evaluacion_modelo_ibfk_1'),
        Index('EvaModCod', 'EvaModCod')
    )

    EvaCod: Mapped[int] = mapped_column(Integer, primary_key=True)
    EvaModCod: Mapped[int] = mapped_column(Integer)
    EvaFecEva: Mapped[datetime.date] = mapped_column(Date)
    EvaMet: Mapped[str] = mapped_column(String(40))
    EvaVal: Mapped[decimal.Decimal] = mapped_column(DECIMAL(10, 0))
    EvaCom: Mapped[Optional[str]] = mapped_column(String(160))
    EvaEstReg: Mapped[Optional[str]] = mapped_column(CHAR(1))

    modelo: Mapped['Modelo'] = relationship('Modelo', back_populates='evaluacion_modelo')


class Fotografia(Base):
    __tablename__ = 'fotografia'
    __table_args__ = (
        ForeignKeyConstraint(['FotPlaCod'], ['plaga.PlaCod'], name='fotografia_ibfk_1'),
        Index('FotPlaCod', 'FotPlaCod'),
        Index('FotUrlIma', 'FotUrlIma', unique=True)
    )

    FotCod: Mapped[int] = mapped_column(Integer, primary_key=True)
    FotPlaCod: Mapped[int] = mapped_column(Integer)
    FotUrlIma: Mapped[str] = mapped_column(String(160))
    FotEstReg: Mapped[Optional[str]] = mapped_column(CHAR(1))

    plaga: Mapped['Plaga'] = relationship('Plaga', back_populates='fotografia')
    analisis: Mapped[List['Analisis']] = relationship('Analisis', back_populates='fotografia')


class Parcela(Base):
    __tablename__ = 'parcela'
    __table_args__ = (
        ForeignKeyConstraint(['ParUsuCod'], ['usuario.UsuCod'], name='parcela_ibfk_1'),
        Index('ParNom', 'ParNom', unique=True),
        Index('ParUsuCod', 'ParUsuCod')
    )

    ParCod: Mapped[int] = mapped_column(Integer, primary_key=True)
    ParNom: Mapped[str] = mapped_column(String(80))
    ParUsuCod: Mapped[int] = mapped_column(Integer)
    ParFecReg: Mapped[datetime.date] = mapped_column(Date)
    ParUbi: Mapped[Optional[str]] = mapped_column(String(130))
    ParDes: Mapped[Optional[str]] = mapped_column(String(200))
    ParEstReg: Mapped[Optional[str]] = mapped_column(CHAR(1))

    usuario: Mapped['Usuario'] = relationship('Usuario', back_populates='parcela')
    cultivo: Mapped[List['Cultivo']] = relationship('Cultivo', back_populates='parcela')
    historial_sanitario: Mapped[List['HistorialSanitario']] = relationship('HistorialSanitario', back_populates='parcela')
    sensor: Mapped[List['Sensor']] = relationship('Sensor', back_populates='parcela')
    accion_usuario: Mapped[List['AccionUsuario']] = relationship('AccionUsuario', back_populates='parcela')
    asignacion_rol_usuario: Mapped[List['AsignacionRolUsuario']] = relationship('AsignacionRolUsuario', back_populates='parcela')
    imagen_cultivo: Mapped[List['ImagenCultivo']] = relationship('ImagenCultivo', back_populates='parcela')
    infestacion_plaga: Mapped[List['InfestacionPlaga']] = relationship('InfestacionPlaga', back_populates='parcela')
    recomendacion: Mapped[List['Recomendacion']] = relationship('Recomendacion', back_populates='parcela')
    alerta_por_plaga: Mapped[List['AlertaPorPlaga']] = relationship('AlertaPorPlaga', back_populates='parcela')


class PermisoPermitidoRol(Base):
    __tablename__ = 'permiso_permitido_rol'
    __table_args__ = (
        ForeignKeyConstraint(['PerPerCod'], ['permiso.PerCod'], name='permiso_permitido_rol_ibfk_1'),
        ForeignKeyConstraint(['PerRolCod'], ['rol.RolCod'], name='permiso_permitido_rol_ibfk_2'),
        Index('PerPerCod', 'PerPerCod'),
        Index('PerRolCod', 'PerRolCod')
    )

    PerCod: Mapped[int] = mapped_column(Integer, primary_key=True)
    PerRolCod: Mapped[int] = mapped_column(Integer)
    PerPerCod: Mapped[int] = mapped_column(Integer)
    PerPre: Mapped[Optional[int]] = mapped_column(TINYINT(1))
    PerEstReg: Mapped[Optional[str]] = mapped_column(CHAR(1))

    permiso: Mapped['Permiso'] = relationship('Permiso', back_populates='permiso_permitido_rol')
    rol: Mapped['Rol'] = relationship('Rol', back_populates='permiso_permitido_rol')


class Analisis(Base):
    __tablename__ = 'analisis'
    __table_args__ = (
        ForeignKeyConstraint(['AnaFotCod'], ['fotografia.FotCod'], name='analisis_ibfk_1'),
        ForeignKeyConstraint(['AnaModCod'], ['modelo.ModCod'], name='analisis_ibfk_4'),
        ForeignKeyConstraint(['AnaPlaCod'], ['plaga.PlaCod'], name='analisis_ibfk_3'),
        ForeignKeyConstraint(['AnaSevCod'], ['severidad.SevCod'], name='analisis_ibfk_2'),
        Index('AnaFotCod', 'AnaFotCod'),
        Index('AnaModCod', 'AnaModCod'),
        Index('AnaPlaCod', 'AnaPlaCod'),
        Index('AnaSevCod', 'AnaSevCod')
    )

    AnaCod: Mapped[int] = mapped_column(Integer, primary_key=True)
    AnaFotCod: Mapped[int] = mapped_column(Integer)
    AnaModCod: Mapped[int] = mapped_column(Integer)
    AnaFecAna: Mapped[datetime.date] = mapped_column(Date)
    AnaPlaCod: Mapped[int] = mapped_column(Integer)
    AnaSevCod: Mapped[int] = mapped_column(Integer)
    AnaRes: Mapped[Optional[str]] = mapped_column(String(160))
    AnaCon: Mapped[Optional[decimal.Decimal]] = mapped_column(DECIMAL(10, 0))
    AnaObs: Mapped[Optional[str]] = mapped_column(String(160))
    AnaEstReg: Mapped[Optional[str]] = mapped_column(CHAR(1))

    fotografia: Mapped['Fotografia'] = relationship('Fotografia', back_populates='analisis')
    modelo: Mapped['Modelo'] = relationship('Modelo', back_populates='analisis')
    plaga: Mapped['Plaga'] = relationship('Plaga', back_populates='analisis')
    severidad: Mapped['Severidad'] = relationship('Severidad', back_populates='analisis')
    alerta: Mapped[List['Alerta']] = relationship('Alerta', back_populates='analisis')
    alerta_por_plaga: Mapped[List['AlertaPorPlaga']] = relationship('AlertaPorPlaga', back_populates='analisis')


class Cultivo(Base):
    __tablename__ = 'cultivo'
    __table_args__ = (
        ForeignKeyConstraint(['CulParCod'], ['parcela.ParCod'], name='cultivo_ibfk_1'),
        Index('CulNom', 'CulNom', unique=True),
        Index('CulParCod', 'CulParCod')
    )

    CulCod: Mapped[int] = mapped_column(Integer, primary_key=True)
    CulNom: Mapped[str] = mapped_column(String(80))
    CulParCod: Mapped[int] = mapped_column(Integer)
    CulTip: Mapped[Optional[str]] = mapped_column(String(40))
    CulFecSie: Mapped[Optional[datetime.date]] = mapped_column(Date)
    CulFecCos: Mapped[Optional[datetime.date]] = mapped_column(Date)
    CulPro: Mapped[Optional[int]] = mapped_column(TINYINT(1))
    CulUrlIma: Mapped[Optional[str]] = mapped_column(String(60))
    CulEstReg: Mapped[Optional[str]] = mapped_column(CHAR(1))

    parcela: Mapped['Parcela'] = relationship('Parcela', back_populates='cultivo')
    accion_usuario: Mapped[List['AccionUsuario']] = relationship('AccionUsuario', back_populates='cultivo')
    asignacion_rol_usuario: Mapped[List['AsignacionRolUsuario']] = relationship('AsignacionRolUsuario', back_populates='cultivo')
    imagen_cultivo: Mapped[List['ImagenCultivo']] = relationship('ImagenCultivo', back_populates='cultivo')
    infestacion_plaga: Mapped[List['InfestacionPlaga']] = relationship('InfestacionPlaga', back_populates='cultivo')
    recomendacion: Mapped[List['Recomendacion']] = relationship('Recomendacion', back_populates='cultivo')
    alerta_por_plaga: Mapped[List['AlertaPorPlaga']] = relationship('AlertaPorPlaga', back_populates='cultivo')


class HistorialSanitario(Base):
    __tablename__ = 'historial_sanitario'
    __table_args__ = (
        ForeignKeyConstraint(['HisParCod'], ['parcela.ParCod'], name='historial_sanitario_ibfk_1'),
        Index('HisParCod', 'HisParCod')
    )

    HisCod: Mapped[int] = mapped_column(Integer, primary_key=True)
    HisParCod: Mapped[int] = mapped_column(Integer)
    HisResEve: Mapped[Optional[str]] = mapped_column(String(160))
    HisPlaFre: Mapped[Optional[str]] = mapped_column(String(160))
    HisNumInf: Mapped[Optional[int]] = mapped_column(Integer)
    HisNumTra: Mapped[Optional[int]] = mapped_column(Integer)
    HisEstReg: Mapped[Optional[str]] = mapped_column(CHAR(1))

    parcela: Mapped['Parcela'] = relationship('Parcela', back_populates='historial_sanitario')


class Sensor(Base):
    __tablename__ = 'sensor'
    __table_args__ = (
        ForeignKeyConstraint(['SenParCod'], ['parcela.ParCod'], name='sensor_ibfk_1'),
        Index('SenParCod', 'SenParCod'),
        Index('SenSer', 'SenSer', unique=True)
    )

    SenCod: Mapped[int] = mapped_column(Integer, primary_key=True)
    SenSer: Mapped[str] = mapped_column(String(40))
    SenParCod: Mapped[int] = mapped_column(Integer)
    SenLat: Mapped[decimal.Decimal] = mapped_column(DECIMAL(10, 0))
    SenLon: Mapped[decimal.Decimal] = mapped_column(DECIMAL(10, 0))
    SenFecIns: Mapped[datetime.date] = mapped_column(Date)
    SenTipSen: Mapped[Optional[str]] = mapped_column(String(40))
    SenUniMed: Mapped[Optional[str]] = mapped_column(String(40))
    SenEstReg: Mapped[Optional[str]] = mapped_column(CHAR(1))

    parcela: Mapped['Parcela'] = relationship('Parcela', back_populates='sensor')
    imagen_cultivo: Mapped[List['ImagenCultivo']] = relationship('ImagenCultivo', back_populates='sensor')
    lectura_sensor: Mapped[List['LecturaSensor']] = relationship('LecturaSensor', back_populates='sensor')


class AccionUsuario(Base):
    __tablename__ = 'accion_usuario'
    __table_args__ = (
        ForeignKeyConstraint(['AccCulCod'], ['cultivo.CulCod'], name='accion_usuario_ibfk_3'),
        ForeignKeyConstraint(['AccParCod'], ['parcela.ParCod'], name='accion_usuario_ibfk_2'),
        ForeignKeyConstraint(['AccTipAccCod'], ['tipo_accion.TipCod'], name='accion_usuario_ibfk_1'),
        ForeignKeyConstraint(['AccUsuCod'], ['usuario.UsuCod'], name='accion_usuario_ibfk_4'),
        Index('AccCulCod', 'AccCulCod'),
        Index('AccParCod', 'AccParCod'),
        Index('AccTipAccCod', 'AccTipAccCod'),
        Index('AccUsuCod', 'AccUsuCod')
    )

    AccCod: Mapped[int] = mapped_column(Integer, primary_key=True)
    AccUsuCod: Mapped[int] = mapped_column(Integer)
    AccParCod: Mapped[int] = mapped_column(Integer)
    AccCulCod: Mapped[int] = mapped_column(Integer)
    AccFec: Mapped[datetime.date] = mapped_column(Date)
    AccTipAccCod: Mapped[int] = mapped_column(Integer)
    AccDesAcc: Mapped[str] = mapped_column(String(260))
    AccRes: Mapped[Optional[str]] = mapped_column(String(160))
    AccFecDelRes: Mapped[Optional[datetime.date]] = mapped_column(Date)
    AccEstReg: Mapped[Optional[str]] = mapped_column(CHAR(1))

    cultivo: Mapped['Cultivo'] = relationship('Cultivo', back_populates='accion_usuario')
    parcela: Mapped['Parcela'] = relationship('Parcela', back_populates='accion_usuario')
    tipo_accion: Mapped['TipoAccion'] = relationship('TipoAccion', back_populates='accion_usuario')
    usuario: Mapped['Usuario'] = relationship('Usuario', back_populates='accion_usuario')


class AsignacionRolUsuario(Base):
    __tablename__ = 'asignacion_rol_usuario'
    __table_args__ = (
        ForeignKeyConstraint(['AsiCulCod'], ['cultivo.CulCod'], name='asignacion_rol_usuario_ibfk_2'),
        ForeignKeyConstraint(['AsiParCod'], ['parcela.ParCod'], name='asignacion_rol_usuario_ibfk_1'),
        ForeignKeyConstraint(['AsiRolCod'], ['rol.RolCod'], name='asignacion_rol_usuario_ibfk_4'),
        ForeignKeyConstraint(['AsiUsuCod'], ['usuario.UsuCod'], name='asignacion_rol_usuario_ibfk_3'),
        Index('AsiCulCod', 'AsiCulCod'),
        Index('AsiParCod', 'AsiParCod'),
        Index('AsiRolCod', 'AsiRolCod'),
        Index('AsiUsuCod', 'AsiUsuCod')
    )

    AsiCod: Mapped[int] = mapped_column(Integer, primary_key=True)
    AsiUsuCod: Mapped[int] = mapped_column(Integer)
    AsiRolCod: Mapped[int] = mapped_column(Integer)
    AsiFecAsi: Mapped[datetime.date] = mapped_column(Date)
    AsiParCod: Mapped[Optional[int]] = mapped_column(Integer)
    AsiCulCod: Mapped[Optional[int]] = mapped_column(Integer)
    AsiEstReg: Mapped[Optional[str]] = mapped_column(CHAR(1))

    cultivo: Mapped[Optional['Cultivo']] = relationship('Cultivo', back_populates='asignacion_rol_usuario')
    parcela: Mapped[Optional['Parcela']] = relationship('Parcela', back_populates='asignacion_rol_usuario')
    rol: Mapped['Rol'] = relationship('Rol', back_populates='asignacion_rol_usuario')
    usuario: Mapped['Usuario'] = relationship('Usuario', back_populates='asignacion_rol_usuario')


class ImagenCultivo(Base):
    __tablename__ = 'imagen_cultivo'
    __table_args__ = (
        ForeignKeyConstraint(['ImaCulCod'], ['cultivo.CulCod'], name='imagen_cultivo_ibfk_3'),
        ForeignKeyConstraint(['ImaParCod'], ['parcela.ParCod'], name='imagen_cultivo_ibfk_1'),
        ForeignKeyConstraint(['ImaSenCod'], ['sensor.SenCod'], name='imagen_cultivo_ibfk_2'),
        Index('ImaCulCod', 'ImaCulCod'),
        Index('ImaFecHor', 'ImaFecHor', unique=True),
        Index('ImaParCod', 'ImaParCod'),
        Index('ImaSenCod', 'ImaSenCod')
    )

    ImaCod: Mapped[int] = mapped_column(Integer, primary_key=True)
    ImaFecHor: Mapped[datetime.date] = mapped_column(Date)
    ImaParCod: Mapped[int] = mapped_column(Integer)
    ImaCulCod: Mapped[int] = mapped_column(Integer)
    ImaUrlIma: Mapped[str] = mapped_column(String(160))
    ImaSenCod: Mapped[int] = mapped_column(Integer)
    ImaLat: Mapped[decimal.Decimal] = mapped_column(DECIMAL(10, 0))
    ImaLon: Mapped[decimal.Decimal] = mapped_column(DECIMAL(10, 0))
    ImaRes: Mapped[Optional[str]] = mapped_column(String(20))
    ImaTipIma: Mapped[Optional[str]] = mapped_column(String(40))
    ImaAnc: Mapped[Optional[int]] = mapped_column(Integer)
    ImaAlt: Mapped[Optional[int]] = mapped_column(Integer)
    ImaEstReg: Mapped[Optional[str]] = mapped_column(CHAR(1))

    cultivo: Mapped['Cultivo'] = relationship('Cultivo', back_populates='imagen_cultivo')
    parcela: Mapped['Parcela'] = relationship('Parcela', back_populates='imagen_cultivo')
    sensor: Mapped['Sensor'] = relationship('Sensor', back_populates='imagen_cultivo')


class InfestacionPlaga(Base):
    __tablename__ = 'infestacion_plaga'
    __table_args__ = (
        ForeignKeyConstraint(['InfCulCod'], ['cultivo.CulCod'], name='infestacion_plaga_ibfk_4'),
        ForeignKeyConstraint(['InfParCod'], ['parcela.ParCod'], name='infestacion_plaga_ibfk_3'),
        ForeignKeyConstraint(['InfPlaCod'], ['plaga.PlaCod'], name='infestacion_plaga_ibfk_2'),
        ForeignKeyConstraint(['InfSevCod'], ['severidad.SevCod'], name='infestacion_plaga_ibfk_1'),
        Index('InfCulCod', 'InfCulCod'),
        Index('InfParCod', 'InfParCod'),
        Index('InfPlaCod', 'InfPlaCod'),
        Index('InfSevCod', 'InfSevCod')
    )

    InfCod: Mapped[int] = mapped_column(Integer, primary_key=True)
    InfFecDet: Mapped[datetime.date] = mapped_column(Date)
    InfSevCod: Mapped[int] = mapped_column(Integer)
    InfParCod: Mapped[Optional[int]] = mapped_column(Integer)
    InfCulCod: Mapped[Optional[int]] = mapped_column(Integer)
    InfPlaCod: Mapped[Optional[int]] = mapped_column(Integer)
    InfEstAct: Mapped[Optional[str]] = mapped_column(String(40))
    InfObs: Mapped[Optional[str]] = mapped_column(String(160))
    InfEstReg: Mapped[Optional[str]] = mapped_column(CHAR(1))

    cultivo: Mapped[Optional['Cultivo']] = relationship('Cultivo', back_populates='infestacion_plaga')
    parcela: Mapped[Optional['Parcela']] = relationship('Parcela', back_populates='infestacion_plaga')
    plaga: Mapped[Optional['Plaga']] = relationship('Plaga', back_populates='infestacion_plaga')
    severidad: Mapped['Severidad'] = relationship('Severidad', back_populates='infestacion_plaga')
    tratamiento_plaga: Mapped[List['TratamientoPlaga']] = relationship('TratamientoPlaga', back_populates='infestacion_plaga')


class LecturaSensor(Base):
    __tablename__ = 'lectura_sensor'
    __table_args__ = (
        ForeignKeyConstraint(['LecSenCod'], ['sensor.SenCod'], name='lectura_sensor_ibfk_1'),
        Index('LecFecHor', 'LecFecHor', unique=True),
        Index('LecSenCod', 'LecSenCod')
    )

    LecCod: Mapped[int] = mapped_column(Integer, primary_key=True)
    LecFecHor: Mapped[datetime.date] = mapped_column(Date)
    LecSenCod: Mapped[int] = mapped_column(Integer)
    LecVal: Mapped[decimal.Decimal] = mapped_column(DECIMAL(10, 0))
    LecEstReg: Mapped[Optional[str]] = mapped_column(CHAR(1))

    sensor: Mapped['Sensor'] = relationship('Sensor', back_populates='lectura_sensor')
    alerta: Mapped[List['Alerta']] = relationship('Alerta', back_populates='lectura_sensor')
    alerta_por_plaga: Mapped[List['AlertaPorPlaga']] = relationship('AlertaPorPlaga', back_populates='lectura_sensor')


class Recomendacion(Base):
    __tablename__ = 'recomendacion'
    __table_args__ = (
        ForeignKeyConstraint(['RecCulCod'], ['cultivo.CulCod'], name='recomendacion_ibfk_3'),
        ForeignKeyConstraint(['RecModCod'], ['modelo.ModCod'], name='recomendacion_ibfk_2'),
        ForeignKeyConstraint(['RecParCod'], ['parcela.ParCod'], name='recomendacion_ibfk_1'),
        ForeignKeyConstraint(['RecUsuCod'], ['usuario.UsuCod'], name='recomendacion_ibfk_4'),
        Index('RecCulCod', 'RecCulCod'),
        Index('RecModCod', 'RecModCod'),
        Index('RecParCod', 'RecParCod'),
        Index('RecUsuCod', 'RecUsuCod')
    )

    RecCod: Mapped[int] = mapped_column(Integer, primary_key=True)
    RecFec: Mapped[datetime.date] = mapped_column(Date)
    RecParCod: Mapped[int] = mapped_column(Integer)
    RecCulCod: Mapped[int] = mapped_column(Integer)
    RecDes: Mapped[Optional[str]] = mapped_column(String(200))
    RecUsuCod: Mapped[Optional[int]] = mapped_column(Integer)
    RecModCod: Mapped[Optional[int]] = mapped_column(Integer)
    RecRecUsu: Mapped[Optional[str]] = mapped_column(String(200))
    RecEstReg: Mapped[Optional[str]] = mapped_column(CHAR(1))

    cultivo: Mapped['Cultivo'] = relationship('Cultivo', back_populates='recomendacion')
    modelo: Mapped[Optional['Modelo']] = relationship('Modelo', back_populates='recomendacion')
    parcela: Mapped['Parcela'] = relationship('Parcela', back_populates='recomendacion')
    usuario: Mapped[Optional['Usuario']] = relationship('Usuario', back_populates='recomendacion')


class Alerta(Base):
    __tablename__ = 'alerta'
    __table_args__ = (
        ForeignKeyConstraint(['AleAnaCod'], ['analisis.AnaCod'], name='alerta_ibfk_2'),
        ForeignKeyConstraint(['AleLecSenCod'], ['lectura_sensor.LecCod'], name='alerta_ibfk_1'),
        ForeignKeyConstraint(['AleNivAleCod'], ['niveles_alerta.NivCod'], name='alerta_ibfk_3'),
        ForeignKeyConstraint(['AleUsuCod'], ['usuario.UsuCod'], name='alerta_ibfk_4'),
        Index('AleAnaCod', 'AleAnaCod'),
        Index('AleLecSenCod', 'AleLecSenCod'),
        Index('AleNivAleCod', 'AleNivAleCod'),
        Index('AleUsuCod', 'AleUsuCod')
    )

    AleCod: Mapped[int] = mapped_column(Integer, primary_key=True)
    AleFecHor: Mapped[datetime.date] = mapped_column(Date)
    AleMen: Mapped[str] = mapped_column(String(160))
    AleNivAleCod: Mapped[int] = mapped_column(Integer)
    AleLecSenCod: Mapped[Optional[int]] = mapped_column(Integer)
    AleUsuCod: Mapped[Optional[int]] = mapped_column(Integer)
    AleAnaCod: Mapped[Optional[int]] = mapped_column(Integer)
    AleMedEnv: Mapped[Optional[str]] = mapped_column(String(40))
    AleEstReg: Mapped[Optional[str]] = mapped_column(CHAR(1))

    analisis: Mapped[Optional['Analisis']] = relationship('Analisis', back_populates='alerta')
    lectura_sensor: Mapped[Optional['LecturaSensor']] = relationship('LecturaSensor', back_populates='alerta')
    niveles_alerta: Mapped['NivelesAlerta'] = relationship('NivelesAlerta', back_populates='alerta')
    usuario: Mapped[Optional['Usuario']] = relationship('Usuario', back_populates='alerta')


class AlertaPorPlaga(Base):
    __tablename__ = 'alerta_por_plaga'
    __table_args__ = (
        ForeignKeyConstraint(['AleAnaCod'], ['analisis.AnaCod'], name='alerta_por_plaga_ibfk_2'),
        ForeignKeyConstraint(['AleCulCod'], ['cultivo.CulCod'], name='alerta_por_plaga_ibfk_6'),
        ForeignKeyConstraint(['AleLecSenCod'], ['lectura_sensor.LecCod'], name='alerta_por_plaga_ibfk_1'),
        ForeignKeyConstraint(['AleParCod'], ['parcela.ParCod'], name='alerta_por_plaga_ibfk_5'),
        ForeignKeyConstraint(['AlePlaCod'], ['plaga.PlaCod'], name='alerta_por_plaga_ibfk_4'),
        ForeignKeyConstraint(['AleSevCod'], ['severidad.SevCod'], name='alerta_por_plaga_ibfk_3'),
        ForeignKeyConstraint(['AleUsuCod'], ['usuario.UsuCod'], name='alerta_por_plaga_ibfk_7'),
        Index('AleAnaCod', 'AleAnaCod'),
        Index('AleCulCod', 'AleCulCod'),
        Index('AleLecSenCod', 'AleLecSenCod'),
        Index('AleParCod', 'AleParCod'),
        Index('AlePlaCod', 'AlePlaCod'),
        Index('AleSevCod', 'AleSevCod'),
        Index('AleUsuCod', 'AleUsuCod')
    )

    AleCod: Mapped[int] = mapped_column(Integer, primary_key=True)
    AleFecHor: Mapped[datetime.date] = mapped_column(Date)
    AleSevCod: Mapped[int] = mapped_column(Integer)
    AleAnaCod: Mapped[Optional[int]] = mapped_column(Integer)
    AleLecSenCod: Mapped[Optional[int]] = mapped_column(Integer)
    AlePlaCod: Mapped[Optional[int]] = mapped_column(Integer)
    AleCulCod: Mapped[Optional[int]] = mapped_column(Integer)
    AleParCod: Mapped[Optional[int]] = mapped_column(Integer)
    AleUsuCod: Mapped[Optional[int]] = mapped_column(Integer)
    AleRecRap: Mapped[Optional[str]] = mapped_column(String(160))
    AleCanEnv: Mapped[Optional[str]] = mapped_column(String(40))
    AleEstReg: Mapped[Optional[str]] = mapped_column(CHAR(1))

    analisis: Mapped[Optional['Analisis']] = relationship('Analisis', back_populates='alerta_por_plaga')
    cultivo: Mapped[Optional['Cultivo']] = relationship('Cultivo', back_populates='alerta_por_plaga')
    lectura_sensor: Mapped[Optional['LecturaSensor']] = relationship('LecturaSensor', back_populates='alerta_por_plaga')
    parcela: Mapped[Optional['Parcela']] = relationship('Parcela', back_populates='alerta_por_plaga')
    plaga: Mapped[Optional['Plaga']] = relationship('Plaga', back_populates='alerta_por_plaga')
    severidad: Mapped['Severidad'] = relationship('Severidad', back_populates='alerta_por_plaga')
    usuario: Mapped[Optional['Usuario']] = relationship('Usuario', back_populates='alerta_por_plaga')


class TratamientoPlaga(Base):
    __tablename__ = 'tratamiento_plaga'
    __table_args__ = (
        ForeignKeyConstraint(['TraInfPlaCod'], ['infestacion_plaga.InfCod'], name='tratamiento_plaga_ibfk_1'),
        ForeignKeyConstraint(['TraUsuCod'], ['usuario.UsuCod'], name='tratamiento_plaga_ibfk_2'),
        Index('TraInfPlaCod', 'TraInfPlaCod'),
        Index('TraUsuCod', 'TraUsuCod')
    )

    TraCod: Mapped[int] = mapped_column(Integer, primary_key=True)
    TraInfPlaCod: Mapped[int] = mapped_column(Integer)
    TraFecApl: Mapped[datetime.date] = mapped_column(Date)
    TraUsuCod: Mapped[int] = mapped_column(Integer)
    TraProUsa: Mapped[Optional[str]] = mapped_column(String(80))
    TraDos: Mapped[Optional[str]] = mapped_column(String(40))
    TraMetApl: Mapped[Optional[str]] = mapped_column(String(40))
    TraRes: Mapped[Optional[str]] = mapped_column(String(160))
    TraObs: Mapped[Optional[str]] = mapped_column(String(160))
    TraEstReg: Mapped[Optional[str]] = mapped_column(CHAR(1))

    infestacion_plaga: Mapped['InfestacionPlaga'] = relationship('InfestacionPlaga', back_populates='tratamiento_plaga')
    usuario: Mapped['Usuario'] = relationship('Usuario', back_populates='tratamiento_plaga')
    evaluacion_tratamiento: Mapped[List['EvaluacionTratamiento']] = relationship('EvaluacionTratamiento', back_populates='tratamiento_plaga')


class EvaluacionTratamiento(Base):
    __tablename__ = 'evaluacion_tratamiento'
    __table_args__ = (
        ForeignKeyConstraint(['EvaSevCod'], ['severidad.SevCod'], name='evaluacion_tratamiento_ibfk_1'),
        ForeignKeyConstraint(['EvaTraPlaCod'], ['tratamiento_plaga.TraCod'], name='evaluacion_tratamiento_ibfk_2'),
        Index('EvaSevCod', 'EvaSevCod'),
        Index('EvaTraPlaCod', 'EvaTraPlaCod')
    )

    EvaCod: Mapped[int] = mapped_column(Integer, primary_key=True)
    EvaTraPlaCod: Mapped[int] = mapped_column(Integer)
    EvaFecEva: Mapped[datetime.date] = mapped_column(Date)
    EvaMejObs: Mapped[Optional[int]] = mapped_column(TINYINT(1))
    EvaSevCod: Mapped[Optional[int]] = mapped_column(Integer)
    EvaIma: Mapped[Optional[str]] = mapped_column(String(255))
    EvaCom: Mapped[Optional[str]] = mapped_column(String(160))
    EvaEstReg: Mapped[Optional[str]] = mapped_column(CHAR(1))

    severidad: Mapped[Optional['Severidad']] = relationship('Severidad', back_populates='evaluacion_tratamiento')
    tratamiento_plaga: Mapped['TratamientoPlaga'] = relationship('TratamientoPlaga', back_populates='evaluacion_tratamiento')
