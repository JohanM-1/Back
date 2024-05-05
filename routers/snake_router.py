from __future__ import annotations
from fastapi import APIRouter
from Database.queries.snakeFuntions import insert_serpiente,all_Snakes
from .base_models.all_base_model import Serpiente


router = APIRouter()

@router.post("/Snake/create", tags=["Snake"])
async def create_snake(snake_data: Serpiente):
    """
    Creates a new snake record in the database.

    Args:
        snake_data (Serpiente): The snake data to be inserted.

    Returns:
        Dict[str, str]: A dictionary containing a success message or error message.
    """
    response = await insert_serpiente(
        nombre3=snake_data.nombre3,
        nombreCientifico=snake_data.nombreCientifico,
        reino=snake_data.reino,
        especie=snake_data.especie,
        clase=snake_data.clase,
        genero=snake_data.genero,
        familia=snake_data.familia,
    )
    return response


@router.get("/Snake/all", tags=["Snake"])
async def get_all_snakes():
    response = await all_Snakes()
    return response