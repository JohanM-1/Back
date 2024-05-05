from typing import Dict
from fastapi import Body
from Database.models.DataBaseModel import async_session, Usuario, Reporte
from sqlalchemy import select
from Database.models.PasswordHash import crear_hash
from routers.base_models.user import Response 

#funcion para crear un reporte
async def insert_usuario(
    
    nombres: str = Body(...),  # Make all parameters mandatory
    correo: str = Body(...),
    direccion: str = Body(...),
    contraseña: str = Body(...),
    apellido: str = Body(...),
    fecha_n: str = Body(...),
    rol: str = Body(...),
    edad: int = Body(...),
) -> Dict[str, str]:
    """
    Inserts a new user with the provided information into the 'usuarios' table asynchronously.

    Args:
        nombres (str): The name of the user to insert. (required)
        correo (str): The user's email address. (required)
        direccion (str): The user's address. (required)
        contraseña (str): The user's password. (required)
        apellido (str): The user's last name. (required)
        fecha_n (str): The user's birth date (as a string). (required)
        rol (str): The user's role. (required)
        edad (int): The user's age. (required)

    Returns:
        Dict[str, str]: A dictionary with a success message or an error message.
    """

    try:
        async with async_session() as session:
            async with session.begin():
                # Check for existing user with the same name
                existing_user = await session.execute(
                    select(Usuario).where(Usuario.nombre == nombres)
                )
                existing_user = existing_user.scalar()
                if existing_user:
                    return {"error": f"Usuario ya registrado: {existing_user.nombre}"}

                # Create a new user object
                contraseña_hash = await crear_hash(contraseña)
                usuario = Usuario(
                    nombre=nombres,
                    correo=correo,
                    direccion=direccion,
                    contraseña=contraseña_hash,
                    apellido=apellido,
                    fecha_n=fecha_n,
                    rol=rol,
                    edad=edad,
                )
                
                session.add(usuario)
                await session.commit()
                session.refresh(usuario)
        return {"message": f"Usuario: {usuario.nombre} agregado exitosamente y su contraseña {usuario.contraseña}"}

    except Exception as e:
        print({"error": f"Error al insertar usuario: {str(e)}"})
        return {"error": f"Error al insertar usuario: {str(e)}"}

#funcion para ver el reporte segun el id

#funcion para Eliminar un reporte 

#funcion para Actualizar un reporte