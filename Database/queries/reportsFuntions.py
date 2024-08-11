from typing import Dict, Optional, Union
from fastapi import Body
from Database.models.DataBaseModel import async_session,Reporte
from sqlalchemy import delete, select, update
from Database.models.PasswordHash import crear_hash
from routers.base_models.all_base_model import ReporteModel
from routers.base_models.user import Response 


#funcion para crear un reporte
async def insert_report(
    
    report:ReporteModel

):
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

                # Create a new Report object
                Report = Reporte(
                    titulo=report.titulo,
                    descripcion=report.descripcion,
                    serpientes_id_serpientes=report.serpientes_id_serpientes,
                    usuario_id_usuario=report.usuario_id_usuario
                )
                
                session.add(Report)
                await session.commit()
                session.refresh(Report)
        return (report)

    except Exception as e:
        print({"error": f"Error al insertar usuario: {str(e)}"})
        return {"error": f"Error al insertar usuario: {str(e)}"}

#funcion para ver el reporte segun el id
async def get_report_base(identifier: Union[int, str]) -> Optional[Reporte]:
    try:  
        async with async_session() as session:
            async with session.begin():
                if isinstance(identifier, int):
                    stm = select(Reporte).where(Reporte.idReporte == identifier)
                elif isinstance(identifier, str):
                    stm = select(Reporte).where(Reporte.titulo == identifier)
                else:
                    raise ValueError("El identificador debe ser un entero o una cadena de caracteres")
                
                result = await session.execute(stm)
                report_obj = result.scalar()  # Utilizamos result.scalar() para obtener un único resultado
                
                if(report_obj):
                    return  report_obj
                else:
                    return None
    except Exception as error:
        # Manejo de la excepción
        print(f"Se ha producido un error al realizar la búsqueda: {error}")
        return None
    

#funcion para Eliminar un reporte 

async def delete_report(id:int):
    report = get_report_base(id)
    if(report != None):
        try:  
            async with async_session() as session:
                async with session.begin():
                    stm = delete(Reporte).where(Reporte.idReporte == id)

                    await session.execute(stm)
                    await session.commit()
                    return(f"Se ha eliminado el reporte con el id: {id}")
                    
        except Exception as error:
            # Manejo de la excepción
            return (f"Se ha producido un error al realizar la búsqueda: {error}")
        pass

    else:
        return {"message": "No existe ese un reporte con ese id"}

#funcion para Actualizar un reporte

async def update_report(id:int,titulo:str,descripcion:str):
    report = get_report_base(id)
    if(report != None):
        try:  
            async with async_session() as session:
                async with session.begin():
                    report = await get_report_base(id)

                    if(report != None):
                            
                        stmt = (
                            update(Reporte)
                            .where(Reporte.idReporte == id)
                            .values(titulo=titulo,descripcion=descripcion)
                            )

                        await session.execute(stmt)
                        await session.commit()
                        return(f"Se ha Actualizacod el reporte con el id: {id}")
                    else:
                        return (f"Se ha producido un error al realizar la búsqueda: ID{id} no econtrado")
        except Exception as error:
            # Manejo de la excepción
            return (f"Se ha producido un error al realizar la búsqueda: {error}")
        pass

    else:
        return {"message": "No existe ese un reporte con ese id"}
    
    
async def all_reportes():
    """
    Retrieves all georeferencias information from the 'Georeferencia' table asynchronously.

    Returns:
        A list of dictionaries, where each dictionary represents a georeferencias row.
        On error, returns an informative error message.
    """

    try:
        async with async_session() as session:
            async with session.begin():
                # Fetch all user data using select()
                query = select(Reporte)
                result = await session.execute(query)
                reporte = tuple(reporte for reporte in result.scalars())  # Extract Georeferencia objects
                return reporte  
            
    except Exception as error:
        # Log the error for debugging purposes
        print(f"Error retrieving user data: {error}")
        return {"error": f"An error occurred: {error}"}  # Informative error message

    finally:
        # No explicit engine disposal is necessary within the function scope
        # as the async context manager handles it automatically.
        pass