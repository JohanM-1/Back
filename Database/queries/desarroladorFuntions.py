from typing import Dict
from fastapi import Body
from Database.models.DataBaseModel import Desarrollador, async_session
from sqlalchemy import select



async def insert_desarrollador(
    nombre2: str = Body(...),
    direccion2: str = Body(...),
) -> Dict[str, str]:
    """
    Inserts a new developer record with the provided information into a table (assuming the table name is 'desarrollador') asynchronously.

    Args:
        nombre2 (str): The developer's name. (required, max length 20)
        direccion2 (str): The developer's address. (required, max length 45)

    Returns:
        Dict[str, str]: A dictionary with a success message or an error message.
    """

    try:
        async with async_session() as session:
            async with session.begin():
                # Create a new developer object (assuming the table name is 'desarrollador')
                desarrollador = Desarrollador(nombre2=nombre2, direccion2=direccion2)

                session.add(desarrollador)
                await session.commit()
                session.refresh(desarrollador)
                return {
                    "message": f"Desarrollador creado exitosamente: ID {desarrollador.nombre2}"  # Assuming an id field exists
                }

    except Exception as e:
        print({"error": f"Error al insertar desarrollador: {str(e)}"})
        return {"error": f"Error al insertar desarrollador: {str(e)}"}


async def all_desarrolladores():
    """
    Retrieves all developer information from the 'desarrollador' table asynchronously.

    Returns:
        List[Dict[str, str]]: A list of dictionaries, where each dictionary represents a developer row.
        On error, returns an informative error message.
    """

    try:
        async with async_session() as session:
            async with session.begin():
                # Fetch all developer data using select()
                query = select(Desarrollador)
                result = await session.execute(query)
                desarrolladores = tuple(desarrollador for desarrollador in result.scalars())  # Extract Desarrollador objects
                return desarrolladores

    except Exception as error:
        # Log the error for debugging purposes
        print(f"Error retrieving developer data: {error}")
        return {"error": f"An error occurred: {error}"}  # Informative error message

