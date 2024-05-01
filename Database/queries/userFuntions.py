
from typing import Dict
from fastapi import Body
from pydantic import BaseModel
from Database.models.DataBaseModel import async_session, Usuario
from sqlalchemy import func, select
from Database.models.PasswordHash import nuevo_token,crear_hash,verificar_hash


#Insertar un Nuevo usaurio a la db

#interface para guardar la respuesta en este formato
class Response(BaseModel):
    status: bool
    message: str
    data: str | None = None
    access_token: str | None = None

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
                contraseña_hash = crear_hash(contraseña)
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
        return {"message": f"Usuario: {usuario.nombre} agregado exitosamente"}

    except Exception as e:
        print({"error": f"Error al insertar usuario: {str(e)}"})
        return {"error": f"Error al insertar usuario: {str(e)}"}

        



async def all_usuarios():
    """
    Retrieves all user information from the 'usuarios' table asynchronously.

    Returns:
        A list of dictionaries, where each dictionary represents a user row.
        On error, returns an informative error message.
    """

    try:
        async with async_session() as session:
            async with session.begin():
                # Fetch all user data using select()
                query = select(Usuario)
                result = await session.execute(query)
                usuarios = tuple(usuario for usuario in result.scalars())  # Extract Usuario objects
                return usuarios    
            
    except Exception as error:
        # Log the error for debugging purposes
        print(f"Error retrieving user data: {error}")
        return {"error": f"An error occurred: {error}"}  # Informative error message

    finally:
        # No explicit engine disposal is necessary within the function scope
        # as the async context manager handles it automatically.
        pass


async def get_user_base(id :int)->Usuario:
    try:  
        async with async_session() as session:
            async with session.begin():
            
                stm = select(Usuario).where(Usuario.idUsuario == id)
                result = await session.execute(stm)
                user_obj = result.scalar()  # Utilizamos result.scalar() para obtener un único resultado
                if user_obj:
                    return user_obj
                else:
                    return None
    except Exception as error:
        # Manejo de la excepción
        print(f"Se ha producido un error al realizar la busqueda: {error}")
        return None







async def Login_Verificacion(name:str,password:str ) -> dict:

    try:  
        async with async_session() as session:
            async with session.begin():
            
                stm = select(Usuario).where(Usuario.nombre == name)
                result = await session.execute(stm)
                user_now = result.scalar()  
                if user_now:
                    #objeto de clase CryptContext para Hasheo de la contraseña
                    
                    if verificar_hash(password, user_now.contraseña): #verificacion de la contraseña
                        token = nuevo_token(name,user_now.idUsuario)
                        return Response(status=True,message="Inicio de sesión exitoso",data=str(user_now),access_token=token)
                        
                    else:
                        return Response(status=False,message="Contraseña incorrecta")
                else:
                    return Response(status=False,message="Usuario incorrecto")

    except Exception as error:
        # Manejo de la excepción
        return(Response(status=False,message=error))

        
