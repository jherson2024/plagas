from typing import List, Optional

from sqlalchemy import CHAR, ForeignKeyConstraint, Index, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass


class Usuario(Base):
    __tablename__ = 'usuario'
    __table_args__ = (
        Index('UsuNumWha', 'UsuNumWha', unique=True),
    )

    UsuCod: Mapped[int] = mapped_column(Integer, primary_key=True)
    UsuNom: Mapped[str] = mapped_column(String(80))
    UsuNumWha: Mapped[int] = mapped_column(Integer)
    UsuCon: Mapped[str] = mapped_column(String(60))
    UsuUrlImaPer: Mapped[Optional[str]] = mapped_column(String(80))
    UsuEstReg: Mapped[Optional[str]] = mapped_column(CHAR(1))

    mapa: Mapped[List['Mapa']] = relationship('Mapa', back_populates='usuario')


class Mapa(Base):
    __tablename__ = 'mapa'
    __table_args__ = (
        ForeignKeyConstraint(['MapUsuCod'], ['usuario.UsuCod'], name='mapa_ibfk_1'),
        Index('MapUsuCod', 'MapUsuCod')
    )

    MapCod: Mapped[int] = mapped_column(Integer, primary_key=True)
    MapNom: Mapped[str] = mapped_column(String(80))
    MapUsuCod: Mapped[int] = mapped_column(Integer)
    MapUrlIma: Mapped[str] = mapped_column(String(80))
    MapEstReg: Mapped[Optional[str]] = mapped_column(CHAR(1))

    usuario: Mapped['Usuario'] = relationship('Usuario', back_populates='mapa')
    posicion_mapa: Mapped[List['PosicionMapa']] = relationship('PosicionMapa', back_populates='mapa')


class PosicionMapa(Base):
    __tablename__ = 'posicion_mapa'
    __table_args__ = (
        ForeignKeyConstraint(['PosMapCod'], ['mapa.MapCod'], name='posicion_mapa_ibfk_1'),
        Index('PosMapCod', 'PosMapCod')
    )

    PosCod: Mapped[int] = mapped_column(Integer, primary_key=True)
    PosMapCod: Mapped[int] = mapped_column(Integer)
    PosPos: Mapped[Optional[int]] = mapped_column(Integer)
    PosPosB: Mapped[Optional[int]] = mapped_column(Integer)
    PosInd: Mapped[Optional[str]] = mapped_column(String(20))
    PosEstReg: Mapped[Optional[str]] = mapped_column(CHAR(1))

    mapa: Mapped['Mapa'] = relationship('Mapa', back_populates='posicion_mapa')
    imagen_captura: Mapped[List['ImagenCaptura']] = relationship('ImagenCaptura', back_populates='posicion_mapa')


class ImagenCaptura(Base):
    __tablename__ = 'imagen_captura'
    __table_args__ = (
        ForeignKeyConstraint(['ImaPosMapCod'], ['posicion_mapa.PosCod'], name='imagen_captura_ibfk_1'),
        Index('ImaPosMapCod', 'ImaPosMapCod')
    )

    ImaCod: Mapped[int] = mapped_column(Integer, primary_key=True)
    ImaUrlIma: Mapped[str] = mapped_column(String(160))
    ImaPosMapCod: Mapped[int] = mapped_column(Integer)
    ImaCla: Mapped[Optional[str]] = mapped_column(String(20))
    ImaInd: Mapped[Optional[str]] = mapped_column(String(20))
    ImaEstReg: Mapped[Optional[str]] = mapped_column(CHAR(1))

    posicion_mapa: Mapped['PosicionMapa'] = relationship('PosicionMapa', back_populates='imagen_captura')
