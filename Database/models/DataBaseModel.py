from __future__ import annotations
import asyncio
from typing import List, Optional

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.ext.asyncio import AsyncSession,create_async_engine,async_sessionmaker,AsyncAttrs
from sqlalchemy.orm import declarative_base, relationship, mapped_column, Mapped,DeclarativeBase


engine = create_async_engine("postgresql+asyncpg://snake_meta_user:UDnZCTrikRMOQ7iKZekrMYQ8kdcriCZc@dpg-cookl1v79t8c73f5eua0-a.oregon-postgres.render.com/snake_meta", echo=True)
async_session = async_sessionmaker(engine, expire_on_commit=False)

class Base(AsyncAttrs, DeclarativeBase):
    pass

class Usuario(Base):
    __tablename__ = 'usuario'
    idUsuario: Mapped[int] = mapped_column(Integer, primary_key=True)
    correo: Mapped[str] = mapped_column(String(45))
    direccion: Mapped[str] = mapped_column(String(45))
    contraseña: Mapped[str] = mapped_column(String(45))
    nombre: Mapped[str] = mapped_column(String(100))
    apellido: Mapped[str] = mapped_column(String(45))
    fecha_n: Mapped[str] = mapped_column(String(45))
    rol: Mapped[str] = mapped_column(String(45))
    edad: Mapped[int] = mapped_column(Integer)
        
    def __repr__(self):
        return f"Usuario(id={self.idUsuario}, nombre='{self.nombre} {self.apellido}', correo='{self.correo}')"

class Desarrollador(Base):
    __tablename__ = 'desarrollador'
    idDesarrollador: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre2: Mapped[str] = mapped_column(String(20))
    direccion2: Mapped[str] = mapped_column(String(45))


class Serpiente(Base):
    __tablename__ = 'serpientes'
    idSerpiente: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre3: Mapped[str] = mapped_column(String(45))
    nombreCientifico: Mapped[str] = mapped_column(String(45))
    reino: Mapped[str] = mapped_column(String(45))
    especie: Mapped[str] = mapped_column(String(45))
    clase: Mapped[str] = mapped_column(String(45))
    genero: Mapped[str] = mapped_column(String(45))
    familia: Mapped[str] = mapped_column(String(45))


class Georeferencia(Base):
    __tablename__ = 'georeferencia'
    idGeoreferencia: Mapped[int] = mapped_column(Integer, primary_key=True)
    fecha: Mapped[str] = mapped_column(String(20))
    zona: Mapped[str] = mapped_column(String(45))
    coordenadas: Mapped[str] = mapped_column(String(45))
    serpientes_id_serpientes: Mapped[int] = mapped_column(Integer, ForeignKey('serpientes.idSerpiente'))
    usuario_id_usuario: Mapped[int] = mapped_column(Integer, ForeignKey('usuario.idUsuario'))
    desarrollador_id_desarrollador: Mapped[int] = mapped_column(Integer, ForeignKey('desarrollador.idDesarrollador'))

    serpiente: Mapped[Serpiente] = relationship('Serpiente')
    usuario: Mapped[Usuario] = relationship('Usuario')


class Reporte(Base):
    __tablename__ = 'reporte'
    idReporte: Mapped[int] = mapped_column(Integer, primary_key=True)
    titulo: Mapped[str] = mapped_column(String(45))
    descripcion: Mapped[str] = mapped_column(String(45))
    comentario: Mapped[str] = mapped_column(String(45))
    serpientes_id_serpientes: Mapped[int] = mapped_column(Integer, ForeignKey('serpientes.idSerpiente'))
    usuario_id_usuario: Mapped[int] = mapped_column(Integer, ForeignKey('usuario.idUsuario'))
    desarrollador_id_desarrollador: Mapped[int] = mapped_column(Integer, ForeignKey('desarrollador.idDesarrollador'))

    serpiente: Mapped[Serpiente] = relationship('Serpiente')
    usuario: Mapped[Usuario] = relationship('Usuario')

# Creacion de tablas en la base de datos
async def async_main() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    await engine.dispose()
    

