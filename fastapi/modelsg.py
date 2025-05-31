from typing import List, Optional

from sqlalchemy import CHAR, DECIMAL, Date, ForeignKeyConstraint, Index, Integer, String
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
import datetime
import decimal

class Base(DeclarativeBase):
    pass

class FuenteRecomendacion(Base):
    __tablename__ = 'fuente_recomendacion'

    FueCod: Mapped[int] = mapped_column(Integer, primary_key=True)
    FueTipFue: Mapped[Optional[str]] = mapped_column(String(80))
    FueEstReg: Mapped[Optional[str]] = mapped_column(CHAR(1))

    recomendacion: Mapped[List['Recomendacion']] = relationship('Recomendacion', back_populates='fuente_recomendacion')

class Modelo(Base):
    __tablename__ = 'modelo'

    ModCod: Mapped[int] = mapped_column(Integer, primary_key=True)
    ModNom: Mapped[Optional[str]] = mapped_column(String(80))
    ModVer: Mapped[Optional[str]] = mapped_column(String(20))
    ModFecEnt: Mapped[Optional[datetime.date]] = mapped_column(Date)
    ModPre: Mapped[Optional[decimal.Decimal]] = mapped_column(DECIMAL(10, 0))
    ModDes: Mapped[Optional[str]] = mapped_column(String(160))
    ModTipArq: Mapped[Optional[str]] = mapped_column(String(40))
    ModDatUsa: Mapped[Optional[str]] = mapped_column(String(80))
    ModUltAct: Mapped[Optional[datetime.date]] = mapped_column(Date)
    ModEstReg: Mapped[Optional[str]] = mapped_column(CHAR(1))

    evaluacion_modelo: Mapped[List['EvaluacionModelo']] = relationship('EvaluacionModelo', back_populates='modelo')
    recomendacion: Mapped[List['Recomendacion']] = relationship('Recomendacion', back_populates='modelo')
    analisis: Mapped[List['Analisis']] = relationship('Analisis', back_populates='modelo')


class Permiso(Base):
    __tablename__ = 'permiso'
    __table_args__ = (
        Index('PerNom', 'PerNom', unique=True),
    )

    PerCod: Mapped[int] = mapped_column(Integer, primary_key=True)
    PerNom: Mapped[str] = mapped_column(String(80))
    PerDes: Mapped[Optional[str]] = mapped_column(String(120))
    PerNomTab: Mapped[Optional[str]] = mapped_column(String(80))
    PerAbr: Mapped[Optional[int]] = mapped_column(Integer)
    PerEstReg: Mapped[Optional[str]] = mapped_column(CHAR(1))

    permiso_permitido_rol: Mapped[List['PermisoPermitidoRol']] = relationship('PermisoPermitidoRol', back_populates='permiso')


class Plaga(Base):
    __tablename__ = 'plaga'

    PlaCod: Mapped[int] = mapped_column(Integer, primary_key=True)
    PlaNom: Mapped[Optional[str]] = mapped_column(String(80))
    PlaTip: Mapped[Optional[str]] = mapped_column(String(40))
    PlaDes: Mapped[Optional[str]] = mapped_column(String(160))
    PlaTraRec: Mapped[Optional[str]] = mapped_column(String(160))
    PlaEstReg: Mapped[Optional[str]] = mapped_column(CHAR(1))

    imagen_plaga: Mapped[List['ImagenPlaga']] = relationship('ImagenPlaga', back_populates='plaga')
    analisis: Mapped[List['Analisis']] = relationship('Analisis', back_populates='plaga')


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


class Usuario(Base):
    __tablename__ = 'usuario'
    __table_args__ = (
        Index('UsuEma', 'UsuEma', unique=True),
    )

    UsuCod: Mapped[int] = mapped_column(Integer, primary_key=True)
    UsuNom: Mapped[Optional[str]] = mapped_column(String(80))
    UsuEma: Mapped[Optional[str]] = mapped_column(String(80))
    UsuNomUsu: Mapped[Optional[str]] = mapped_column(String(80))
    UsuCon: Mapped[Optional[str]] = mapped_column(String(80))
    UsuIdiPre: Mapped[Optional[str]] = mapped_column(String(40))
    UsuUrlFotPer: Mapped[Optional[str]] = mapped_column(String(60))
    UsuFecCre: Mapped[Optional[datetime.date]] = mapped_column(Date)
    UsuEstReg: Mapped[Optional[str]] = mapped_column(CHAR(1))

    bitacora_usuario: Mapped[List['BitacoraUsuario']] = relationship('BitacoraUsuario', back_populates='usuario')
    bloqueo_intentos: Mapped[List['BloqueoIntentos']] = relationship('BloqueoIntentos', back_populates='usuario')
    cambio_contrasena: Mapped[List['CambioContrasena']] = relationship('CambioContrasena', back_populates='usuario')
    parcela: Mapped[List['Parcela']] = relationship('Parcela', back_populates='usuario')
    accion_usuario: Mapped[List['AccionUsuario']] = relationship('AccionUsuario', back_populates='usuario')
    asignacion_rol_usuario: Mapped[List['AsignacionRolUsuario']] = relationship('AsignacionRolUsuario', back_populates='usuario')

class BitacoraUsuario(Base):
    __tablename__ = 'bitacora_usuario'
    __table_args__ = (
        ForeignKeyConstraint(['BitUsuCod'], ['usuario.UsuCod'], name='bitacora_usuario_ibfk_1'),
        Index('BitUsuCod', 'BitUsuCod')
    )

    BitCod: Mapped[int] = mapped_column(Integer, primary_key=True)
    BitFecHor: Mapped[Optional[datetime.date]] = mapped_column(Date)
    BitUsuCod: Mapped[Optional[int]] = mapped_column(Integer)
    BitAcc: Mapped[Optional[str]] = mapped_column(String(100))
    BitDes: Mapped[Optional[str]] = mapped_column(String(160))
    BitEstReg: Mapped[Optional[str]] = mapped_column(CHAR(1))

    usuario: Mapped[Optional['Usuario']] = relationship('Usuario', back_populates='bitacora_usuario')


class BloqueoIntentos(Base):
    __tablename__ = 'bloqueo_intentos'
    __table_args__ = (
        ForeignKeyConstraint(['BloUsuCod'], ['usuario.UsuCod'], name='bloqueo_intentos_ibfk_1'),
        Index('BloUsuCod', 'BloUsuCod')
    )

    BloCod: Mapped[int] = mapped_column(Integer, primary_key=True)
    BloUsuCod: Mapped[Optional[int]] = mapped_column(Integer)
    BloFecBlo: Mapped[Optional[datetime.date]] = mapped_column(Date)
    BloInt: Mapped[Optional[int]] = mapped_column(Integer)
    BloMot: Mapped[Optional[str]] = mapped_column(String(160))
    BloEstReg: Mapped[Optional[str]] = mapped_column(CHAR(1))

    usuario: Mapped[Optional['Usuario']] = relationship('Usuario', back_populates='bloqueo_intentos')


class CambioContrasena(Base):
    __tablename__ = 'cambio_contrasena'
    __table_args__ = (
        ForeignKeyConstraint(['CamUsuCod'], ['usuario.UsuCod'], name='cambio_contrasena_ibfk_1'),
        Index('CamUsuCod', 'CamUsuCod')
    )

    CamCod: Mapped[int] = mapped_column(Integer, primary_key=True)
    CamUsuCod: Mapped[Optional[int]] = mapped_column(Integer)
    CamFec: Mapped[Optional[datetime.date]] = mapped_column(Date)
    CamMet: Mapped[Optional[str]] = mapped_column(String(40))
    CamOri: Mapped[Optional[str]] = mapped_column(String(40))
    CamEstReg: Mapped[Optional[str]] = mapped_column(CHAR(1))

    usuario: Mapped[Optional['Usuario']] = relationship('Usuario', back_populates='cambio_contrasena')


class EvaluacionModelo(Base):
    __tablename__ = 'evaluacion_modelo'
    __table_args__ = (
        ForeignKeyConstraint(['EvaModCod'], ['modelo.ModCod'], name='evaluacion_modelo_ibfk_1'),
        Index('EvaModCod', 'EvaModCod')
    )

    EvaCod: Mapped[int] = mapped_column(Integer, primary_key=True)
    EvaModCod: Mapped[Optional[int]] = mapped_column(Integer)
    EvaFecEva: Mapped[Optional[datetime.date]] = mapped_column(Date)
    EvaMet: Mapped[Optional[str]] = mapped_column(String(40))
    EvaVal: Mapped[Optional[decimal.Decimal]] = mapped_column(DECIMAL(10, 0))
    EvaCom: Mapped[Optional[str]] = mapped_column(String(160))
    EvaEstReg: Mapped[Optional[str]] = mapped_column(CHAR(1))

    modelo: Mapped[Optional['Modelo']] = relationship('Modelo', back_populates='evaluacion_modelo')


class ImagenPlaga(Base):
    __tablename__ = 'imagen_plaga'
    __table_args__ = (
        ForeignKeyConstraint(['ImaPlaCod'], ['plaga.PlaCod'], name='imagen_plaga_ibfk_1'),
        Index('ImaPlaCod', 'ImaPlaCod')
    )

    ImaCod: Mapped[int] = mapped_column(Integer, primary_key=True)
    ImaPlaCod: Mapped[Optional[int]] = mapped_column(Integer)
    ImaUrlIma: Mapped[Optional[str]] = mapped_column(String(160))
    ImaEstReg: Mapped[Optional[str]] = mapped_column(CHAR(1))

    plaga: Mapped[Optional['Plaga']] = relationship('Plaga', back_populates='imagen_plaga')


class Parcela(Base):
    __tablename__ = 'parcela'
    __table_args__ = (
        ForeignKeyConstraint(['ParUsuCod'], ['usuario.UsuCod'], name='parcela_ibfk_1'),
        Index('ParUsuCod', 'ParUsuCod')
    )

    ParCod: Mapped[int] = mapped_column(Integer, primary_key=True)
    ParNom: Mapped[Optional[str]] = mapped_column(String(80))
    ParUbi: Mapped[Optional[str]] = mapped_column(String(130))
    ParDes: Mapped[Optional[str]] = mapped_column(String(160))
    ParUsuCod: Mapped[Optional[int]] = mapped_column(Integer)
    ParFecReg: Mapped[Optional[datetime.date]] = mapped_column(Date)
    ParEstReg: Mapped[Optional[str]] = mapped_column(CHAR(1))

    usuario: Mapped[Optional['Usuario']] = relationship('Usuario', back_populates='parcela')
    cultivo: Mapped[List['Cultivo']] = relationship('Cultivo', back_populates='parcela')
    sensor: Mapped[List['Sensor']] = relationship('Sensor', back_populates='parcela')
    accion_usuario: Mapped[List['AccionUsuario']] = relationship('AccionUsuario', back_populates='parcela')
    asignacion_rol_usuario: Mapped[List['AsignacionRolUsuario']] = relationship('AsignacionRolUsuario', back_populates='parcela')
    imagen_cultivo: Mapped[List['ImagenCultivo']] = relationship('ImagenCultivo', back_populates='parcela')
    recomendacion: Mapped[List['Recomendacion']] = relationship('Recomendacion', back_populates='parcela')


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


class Cultivo(Base):
    __tablename__ = 'cultivo'
    __table_args__ = (
        ForeignKeyConstraint(['CulParCod'], ['parcela.ParCod'], name='cultivo_ibfk_1'),
        Index('CulParCod', 'CulParCod')
    )

    CulCod: Mapped[int] = mapped_column(Integer, primary_key=True)
    CulNom: Mapped[Optional[str]] = mapped_column(String(80))
    CulTip: Mapped[Optional[str]] = mapped_column(String(40))
    CulParCod: Mapped[Optional[int]] = mapped_column(Integer)
    CulFecSie: Mapped[Optional[datetime.date]] = mapped_column(Date)
    CulFecCos: Mapped[Optional[datetime.date]] = mapped_column(Date)
    CulPro: Mapped[Optional[int]] = mapped_column(TINYINT(1))
    CulUrlIma: Mapped[Optional[str]] = mapped_column(String(60))
    CulEstReg: Mapped[Optional[str]] = mapped_column(CHAR(1))

    parcela: Mapped[Optional['Parcela']] = relationship('Parcela', back_populates='cultivo')
    accion_usuario: Mapped[List['AccionUsuario']] = relationship('AccionUsuario', back_populates='cultivo')
    asignacion_rol_usuario: Mapped[List['AsignacionRolUsuario']] = relationship('AsignacionRolUsuario', back_populates='cultivo')
    imagen_cultivo: Mapped[List['ImagenCultivo']] = relationship('ImagenCultivo', back_populates='cultivo')
    recomendacion: Mapped[List['Recomendacion']] = relationship('Recomendacion', back_populates='cultivo')


class Sensor(Base):
    __tablename__ = 'sensor'
    __table_args__ = (
        ForeignKeyConstraint(['SenParCod'], ['parcela.ParCod'], name='sensor_ibfk_1'),
        Index('SenParCod', 'SenParCod'),
        Index('SenSer', 'SenSer', unique=True)
    )

    SenCod: Mapped[int] = mapped_column(Integer, primary_key=True)
    SenSer: Mapped[str] = mapped_column(String(40))
    SenTipSen: Mapped[Optional[str]] = mapped_column(String(40))
    SenUniMed: Mapped[Optional[str]] = mapped_column(String(40))
    SenParCod: Mapped[Optional[int]] = mapped_column(Integer)
    SenLat: Mapped[Optional[decimal.Decimal]] = mapped_column(DECIMAL(10, 0))
    SenLon: Mapped[Optional[decimal.Decimal]] = mapped_column(DECIMAL(10, 0))
    SenFecIns: Mapped[Optional[datetime.date]] = mapped_column(Date)
    SenEstReg: Mapped[Optional[str]] = mapped_column(CHAR(1))

    parcela: Mapped[Optional['Parcela']] = relationship('Parcela', back_populates='sensor')
    imagen_cultivo: Mapped[List['ImagenCultivo']] = relationship('ImagenCultivo', back_populates='sensor')
    lectura_sensor: Mapped[List['LecturaSensor']] = relationship('LecturaSensor', back_populates='sensor')


class AccionUsuario(Base):
    __tablename__ = 'accion_usuario'
    __table_args__ = (
        ForeignKeyConstraint(['AccCulCod'], ['cultivo.CulCod'], name='accion_usuario_ibfk_2'),
        ForeignKeyConstraint(['AccParCod'], ['parcela.ParCod'], name='accion_usuario_ibfk_1'),
        ForeignKeyConstraint(['AccUsuCod'], ['usuario.UsuCod'], name='accion_usuario_ibfk_3'),
        Index('AccCulCod', 'AccCulCod'),
        Index('AccParCod', 'AccParCod'),
        Index('AccUsuCod', 'AccUsuCod')
    )

    AccCod: Mapped[int] = mapped_column(Integer, primary_key=True)
    AccUsuCod: Mapped[Optional[int]] = mapped_column(Integer)
    AccParCod: Mapped[Optional[int]] = mapped_column(Integer)
    AccCulCod: Mapped[Optional[int]] = mapped_column(Integer)
    AccFec: Mapped[Optional[datetime.date]] = mapped_column(Date)
    AccTipAcc: Mapped[Optional[str]] = mapped_column(String(80))
    AccDesAcc: Mapped[Optional[str]] = mapped_column(String(260))
    AccRes: Mapped[Optional[str]] = mapped_column(String(160))
    AccFecDelRes: Mapped[Optional[datetime.date]] = mapped_column(Date)
    AccEstReg: Mapped[Optional[str]] = mapped_column(CHAR(1))

    cultivo: Mapped[Optional['Cultivo']] = relationship('Cultivo', back_populates='accion_usuario')
    parcela: Mapped[Optional['Parcela']] = relationship('Parcela', back_populates='accion_usuario')
    usuario: Mapped[Optional['Usuario']] = relationship('Usuario', back_populates='accion_usuario')


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
    AsiParCod: Mapped[Optional[int]] = mapped_column(Integer)
    AsiCulCod: Mapped[Optional[int]] = mapped_column(Integer)
    AsiFecAsi: Mapped[Optional[datetime.date]] = mapped_column(Date)
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
        Index('ImaParCod', 'ImaParCod'),
        Index('ImaSenCod', 'ImaSenCod')
    )

    ImaCod: Mapped[int] = mapped_column(Integer, primary_key=True)
    ImaFecHor: Mapped[datetime.date] = mapped_column(Date)
    ImaParCod: Mapped[Optional[int]] = mapped_column(Integer)
    ImaCulCod: Mapped[Optional[int]] = mapped_column(Integer)
    ImaUrlIma: Mapped[Optional[str]] = mapped_column(String(160))
    ImaSenCod: Mapped[Optional[int]] = mapped_column(Integer)
    ImaLat: Mapped[Optional[decimal.Decimal]] = mapped_column(DECIMAL(10, 0))
    ImaLon: Mapped[Optional[decimal.Decimal]] = mapped_column(DECIMAL(10, 0))
    ImaRes: Mapped[Optional[str]] = mapped_column(String(20))
    ImaTipIma: Mapped[Optional[str]] = mapped_column(String(40))
    ImaEstReg: Mapped[Optional[str]] = mapped_column(CHAR(1))

    cultivo: Mapped[Optional['Cultivo']] = relationship('Cultivo', back_populates='imagen_cultivo')
    parcela: Mapped[Optional['Parcela']] = relationship('Parcela', back_populates='imagen_cultivo')
    sensor: Mapped[Optional['Sensor']] = relationship('Sensor', back_populates='imagen_cultivo')
    analisis: Mapped[List['Analisis']] = relationship('Analisis', back_populates='imagen_cultivo')


class LecturaSensor(Base):
    __tablename__ = 'lectura_sensor'
    __table_args__ = (
        ForeignKeyConstraint(['LecSenCod'], ['sensor.SenCod'], name='lectura_sensor_ibfk_1'),
        Index('LecSenCod', 'LecSenCod')
    )

    LecCod: Mapped[int] = mapped_column(Integer, primary_key=True)
    LecFecHor: Mapped[datetime.date] = mapped_column(Date)
    LecSenCod: Mapped[Optional[int]] = mapped_column(Integer)
    LecVal: Mapped[Optional[decimal.Decimal]] = mapped_column(DECIMAL(10, 0))
    LecEstReg: Mapped[Optional[str]] = mapped_column(CHAR(1))

    sensor: Mapped[Optional['Sensor']] = relationship('Sensor', back_populates='lectura_sensor')
    alerta: Mapped[List['Alerta']] = relationship('Alerta', back_populates='lectura_sensor')


class Recomendacion(Base):
    __tablename__ = 'recomendacion'
    __table_args__ = (
        ForeignKeyConstraint(['RecCulCod'], ['cultivo.CulCod'], name='recomendacion_ibfk_3'),
        ForeignKeyConstraint(['RecFueRecCod'], ['fuente_recomendacion.FueCod'], name='recomendacion_ibfk_4'),
        ForeignKeyConstraint(['RecModCod'], ['modelo.ModCod'], name='recomendacion_ibfk_2'),
        ForeignKeyConstraint(['RecParCod'], ['parcela.ParCod'], name='recomendacion_ibfk_1'),
        Index('RecCulCod', 'RecCulCod'),
        Index('RecFueRecCod', 'RecFueRecCod'),
        Index('RecModCod', 'RecModCod'),
        Index('RecParCod', 'RecParCod')
    )

    RecCod: Mapped[int] = mapped_column(Integer, primary_key=True)
    RecFec: Mapped[Optional[datetime.date]] = mapped_column(Date)
    RecParCod: Mapped[Optional[int]] = mapped_column(Integer)
    RecCulCod: Mapped[Optional[int]] = mapped_column(Integer)
    RecDes: Mapped[Optional[str]] = mapped_column(String(160))
    RecFueRecCod: Mapped[Optional[int]] = mapped_column(Integer)
    RecModCod: Mapped[Optional[int]] = mapped_column(Integer)
    RecEstReg: Mapped[Optional[str]] = mapped_column(CHAR(1))

    cultivo: Mapped[Optional['Cultivo']] = relationship('Cultivo', back_populates='recomendacion')
    fuente_recomendacion: Mapped[Optional['FuenteRecomendacion']] = relationship('FuenteRecomendacion', back_populates='recomendacion')
    modelo: Mapped[Optional['Modelo']] = relationship('Modelo', back_populates='recomendacion')
    parcela: Mapped[Optional['Parcela']] = relationship('Parcela', back_populates='recomendacion')


class Analisis(Base):
    __tablename__ = 'analisis'
    __table_args__ = (
        ForeignKeyConstraint(['AnaImaCulCod'], ['imagen_cultivo.ImaCod'], name='analisis_ibfk_1'),
        ForeignKeyConstraint(['AnaModCod'], ['modelo.ModCod'], name='analisis_ibfk_3'),
        ForeignKeyConstraint(['AnaPlaCod'], ['plaga.PlaCod'], name='analisis_ibfk_2'),
        Index('AnaImaCulCod', 'AnaImaCulCod'),
        Index('AnaModCod', 'AnaModCod'),
        Index('AnaPlaCod', 'AnaPlaCod')
    )

    AnaCod: Mapped[int] = mapped_column(Integer, primary_key=True)
    AnaImaCulCod: Mapped[Optional[int]] = mapped_column(Integer)
    AnaModCod: Mapped[Optional[int]] = mapped_column(Integer)
    AnaFecAna: Mapped[Optional[datetime.date]] = mapped_column(Date)
    AnaRes: Mapped[Optional[str]] = mapped_column(String(160))
    AnaCon: Mapped[Optional[decimal.Decimal]] = mapped_column(DECIMAL(10, 0))
    AnaObs: Mapped[Optional[str]] = mapped_column(String(160))
    AnaPlaCod: Mapped[Optional[int]] = mapped_column(Integer)
    AnaSev: Mapped[Optional[str]] = mapped_column(String(255))
    AnaEstReg: Mapped[Optional[str]] = mapped_column(CHAR(1))

    imagen_cultivo: Mapped[Optional['ImagenCultivo']] = relationship('ImagenCultivo', back_populates='analisis')
    modelo: Mapped[Optional['Modelo']] = relationship('Modelo', back_populates='analisis')
    plaga: Mapped[Optional['Plaga']] = relationship('Plaga', back_populates='analisis')
    alerta: Mapped[List['Alerta']] = relationship('Alerta', back_populates='analisis')


class Alerta(Base):
    __tablename__ = 'alerta'
    __table_args__ = (
        ForeignKeyConstraint(['AleAnaCod'], ['analisis.AnaCod'], name='alerta_ibfk_2'),
        ForeignKeyConstraint(['AleLecSenCod'], ['lectura_sensor.LecCod'], name='alerta_ibfk_1'),
        Index('AleAnaCod', 'AleAnaCod'),
        Index('AleLecSenCod', 'AleLecSenCod')
    )

    AleCod: Mapped[int] = mapped_column(Integer, primary_key=True)
    AleFecHor: Mapped[Optional[datetime.date]] = mapped_column(Date)
    AleLecSenCod: Mapped[Optional[int]] = mapped_column(Integer)
    AleAnaCod: Mapped[Optional[int]] = mapped_column(Integer)
    AleMen: Mapped[Optional[str]] = mapped_column(String(160))
    AleMedEnv: Mapped[Optional[str]] = mapped_column(String(40))
    AleNiv: Mapped[Optional[str]] = mapped_column(String(40))
    AleEstReg: Mapped[Optional[str]] = mapped_column(CHAR(1))

    analisis: Mapped[Optional['Analisis']] = relationship('Analisis', back_populates='alerta')
    lectura_sensor: Mapped[Optional['LecturaSensor']] = relationship('LecturaSensor', back_populates='alerta')
