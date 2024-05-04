from typing import Dict
from fastapi import Body
from Database.models.DataBaseModel import Georeferencia, Serpiente, async_session, Usuario, Reporte
from sqlalchemy import select
from Database.models.PasswordHash import crear_hash
from routers.base_models.user import Response

async def insert_serpiente(
    nombre3: str = Body(...),
    nombreCientifico: str = Body(...),
    reino: str = Body(...),
    especie: str = Body(...),
    clase: str = Body(...),
    genero: str = Body(...),
    familia: str = Body(...),
) -> Dict[str, str]:
  """
  Inserts a new snake record with the provided information into the 'serpientes' table asynchronously.

  Args:
      nombre3 (str): The common name of the snake. (required)
      nombreCientifico (str): The scientific name of the snake. (required)
      reino (str): The kingdom the snake belongs to. (required)
      especie (str): The species of the snake. (required)
      clase (str): The class the snake belongs to. (required)
      genero (str): The genus of the snake. (required)
      familia (str): The family the snake belongs to. (required)

  Returns:
      Dict[str, str]: A dictionary with a success message or an error message.
  """

  try:
    async with async_session() as session:
      async with session.begin():
        # Check for existing snake with the same scientific name (optional)
        # existing_snake = await session.execute(
        #     select(Serpiente).where(Serpiente.nombreCientifico == nombreCientifico)
        # )
        # existing_snake = existing_snake.scalar()
        # if existing_snake:
        #     return {"error": f"Serpiente ya registrada: {existing_snake.nombreCientifico}"}

        # Create a new snake object
        serpiente = Serpiente(
            nombre3=nombre3,
            nombreCientifico=nombreCientifico,
            reino=reino,
            especie=especie,
            clase=clase,
            genero=genero,
            familia=familia,
        )

        session.add(serpiente)
        await session.commit()
        session.refresh(serpiente)
        return {
            "message": f"Serpiente creada exitosamente: ID {serpiente.idSerpiente}"
        }

  except Exception as e:
    print({"error": f"Error al insertar serpiente: {str(e)}"})
    return {"error": f"Error al insertar serpiente: {str(e)}"}


async def all_Snakes():
    """
    Retrieves all Snake information from the 'Serpientes' table asynchronously.

    Returns:
        A list of dictionaries, where each dictionary represents a Snake row.
        On error, returns an informative error message.
    """

    try:
        async with async_session() as session:
            async with session.begin():
                # Fetch all user data using select()
                query = select(Serpiente)
                result = await session.execute(query)
                usuarios = tuple(Snake for Snake in result.scalars())  # Extract Usuario objects
                return usuarios  
            
    except Exception as error:
        # Log the error for debugging purposes
        print(f"Error retrieving user data: {error}")
        return {"error": f"An error occurred: {error}"}  # Informative error message

    finally:
        # No explicit engine disposal is necessary within the function scope
        # as the async context manager handles it automatically.
        pass