from __future__ import annotations
import asyncio
from typing import List, Optional

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.ext.asyncio import AsyncSession,create_async_engine,async_sessionmaker,AsyncAttrs
from sqlalchemy.orm import declarative_base, relationship, mapped_column, Mapped,DeclarativeBase

from sqlalchemy.ext.declarative import declared_attr
engine = create_async_engine("postgresql+asyncpg://snake_meta_db_local_user:1OLLl43SzKw9WWvTkk8WlAjYeCd4HHhk@dpg-cqcmk4mehbks738jfum0-a.oregon-postgres.render.com/snake_meta_db_local", echo=True)
async_session = async_sessionmaker(engine, expire_on_commit=False)

class Base(AsyncAttrs, DeclarativeBase):
    pass


class TimestampMixin(object):
    created_at = Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    updated_at = Mapped[DateTime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())
    
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

class Usuario(Base):
    __tablename__ = 'usuario'
    idUsuario: Mapped[int] = mapped_column(Integer, primary_key=True)
    correo: Mapped[str] = mapped_column(String(45))
    direccion: Mapped[str] = mapped_column(String(45))
    contraseña: Mapped[str] = mapped_column(String(100))
    nombre: Mapped[str] = mapped_column(String(45))
    apellido: Mapped[str] = mapped_column(String(45))
    fecha_n: Mapped[str] = mapped_column(String(45))
    rol: Mapped[str] = mapped_column(String(45))
    edad: Mapped[int] = mapped_column(Integer)
        
    def __repr__(self):
        return f"Usuario(id={self.idUsuario}, nombre='{self.nombre} {self.apellido}', correo='{self.correo}')"




class Serpiente(Base):
    __tablename__ = 'serpientes'
    idSerpiente: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre3: Mapped[str] = mapped_column(String(45))
    nombreCientifico: Mapped[str] = mapped_column(String(100))
    reino: Mapped[str] = mapped_column(String(45))
    especie: Mapped[str] = mapped_column(String(45))
    clase: Mapped[str] = mapped_column(String(45))
    genero: Mapped[str] = mapped_column(String(45))
    familia: Mapped[str] = mapped_column(String(45))
    imagen: Mapped[str] = mapped_column(String(200))
    venenosa:Mapped[bool] = mapped_column(Boolean)
    descripcion:Mapped[str] = mapped_column(String(2000))

class Georeferencia(Base):
    __tablename__ = 'georeferencia'
    idGeoreferencia: Mapped[int] = mapped_column(Integer, primary_key=True)
    fecha: Mapped[str] = mapped_column(String(20))
    zona: Mapped[str] = mapped_column(String(100))
    coordenadas: Mapped[str] = mapped_column(String(200))
    serpientes_id_serpientes: Mapped[int] = mapped_column(Integer, ForeignKey('serpientes.idSerpiente'))
    usuario_id_usuario: Mapped[int] = mapped_column(Integer, ForeignKey('usuario.idUsuario'))

    serpiente: Mapped[Serpiente] = relationship('Serpiente')
    usuario: Mapped[Usuario] = relationship('Usuario')





class Reporte(TimestampMixin,Base):
    __tablename__ = 'reporte'
    idReporte: Mapped[int] = mapped_column(Integer, primary_key=True)
    titulo: Mapped[str] = mapped_column(String(100))
    descripcion: Mapped[str] = mapped_column(String(1000))
    serpientes_id_serpientes: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey('serpientes.idSerpiente'))
    usuario_id_usuario: Mapped[int] = mapped_column(Integer, ForeignKey('usuario.idUsuario'))
    
    serpiente: Mapped[Serpiente] = relationship('Serpiente')
    usuario: Mapped[Usuario] = relationship('Usuario')


class Comentario(TimestampMixin,Base):
    __tablename__ = 'comentario'
    idComentario: Mapped[int] = mapped_column(Integer, primary_key=True)
    contenido: Mapped[str] = mapped_column(String(1000))
    reporte_id_reporte: Mapped[int] = mapped_column(Integer, ForeignKey('reporte.idReporte'))
    usuario_id_usuario: Mapped[int] = mapped_column(Integer, ForeignKey('usuario.idUsuario'))

    reporte: Mapped[Reporte] = relationship('Reporte')
    usuario: Mapped[Usuario] = relationship('Usuario')
    def __repr__(self):
        return {'fecha de creacion':self.created_at,'contenido':self.contenido}
    

# Creacion de tablas en la base de datos
async def async_main() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    await engine.dispose()


