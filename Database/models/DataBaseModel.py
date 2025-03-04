from __future__ import annotations
import asyncio
import datetime
import os
from typing import List, Optional

import asyncpg
from dotenv import load_dotenv
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, func , Time ,Date
from sqlalchemy.ext.asyncio import AsyncSession,create_async_engine,async_sessionmaker,AsyncAttrs
from sqlalchemy.orm import declarative_base, relationship, mapped_column, Mapped,DeclarativeBase

from sqlalchemy.ext.declarative import declared_attr



# Obtener la ruta absoluta del directorio actual
current_dir = os.path.dirname(os.path.abspath(__file__))

# Ascender dos directorios y concatenar la ruta al archivo .env
env_path = os.path.join(current_dir, '../../.env')

# Cargar las variables de entorno desde el archivo .env
# (Aquí deberías utilizar una librería como `dotenv` para cargar las variables)
from dotenv import load_dotenv
load_dotenv(dotenv_path=env_path)



# Obtener valores de las variables de entorno
API_KEY = os.environ.get("API_KEY")  # Valor por defecto de settings
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")  # Puerto predeterminado de Postgres
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_NAME = os.environ.get("DB_NAME")

engine = create_async_engine(
        f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}",echo = True
    )

    

async_session = async_sessionmaker(engine, expire_on_commit=False)

class Base(AsyncAttrs, DeclarativeBase):
    pass



class TimestampMixin(object):
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

class Usuario(Base):
    __tablename__ = 'usuario'
    idUsuario: Mapped[int] = mapped_column(Integer, primary_key=True)
    
    imagen: Mapped[str] = mapped_column(String(200),nullable=True)
    correo: Mapped[str] = mapped_column(String(45))
    direccion: Mapped[str] = mapped_column(String(45))
    contraseña: Mapped[str] = mapped_column(String(100))
    nombre: Mapped[str] = mapped_column(String(45))
    apellido: Mapped[str] = mapped_column(String(45))
    fecha_n: Mapped[str] = mapped_column(String(45))
    rol: Mapped[str] = mapped_column(String(45))
    edad: Mapped[int] = mapped_column(Integer)
    Descripcion: Mapped[str] = mapped_column(String(300),nullable=True)
    imagen_fonodo: Mapped[str] = mapped_column(String(300),nullable=True)
        
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
    imagen: Mapped[str] = mapped_column(String(200),nullable=True)
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
    descripcion: Mapped[str] = mapped_column(String(1000),nullable=True)
    imagen: Mapped[str] = mapped_column(String(200))
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
    
async def async_main() -> None:
    async with engine.begin() as conn:
        try:
            await conn.run_sync(Base.metadata.create_all)
            print("Tablas creadas exitosamente.")
        except Exception as e:
            print(f"Error al crear las tablas: {e}")

    await engine.dispose()
    
    


async def create_database(user, password, host, port, dbname):
    """
    Crea la base de datos si no existe.

    Args:
        user: Nombre de usuario de la base de datos.
        password: Contraseña del usuario.
        host: Host de la base de datos.
        port: Puerto de la base de datos.
        dbname: Nombre de la base de datos a crear.
    """
    try:
        # Conectar a la base de datos 'postgres' (la base de datos predeterminada)
        conn = await asyncpg.connect(user=user, password=password, host=host, port=port, database="postgres")
        await conn.execute(f"CREATE DATABASE {dbname}")
        await conn.close()
        print(f"Base de datos '{dbname}' creada exitosamente.")
    except asyncpg.exceptions.DuplicateDatabaseError:
        print(f"La base de datos '{dbname}' ya existe.")
    except Exception as e:
        print(f"Error al crear la base de datos: {e}")

if __name__ == "__main__":
    asyncio.run(create_database(user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT, dbname=DB_NAME))
    asyncio.run(async_main())
