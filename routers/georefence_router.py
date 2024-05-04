from __future__ import annotations
from fastapi import APIRouter
from Database.queries.georeferenceFuntions import all_georeferencias,insert_georeferencia
from .base_models.user import Snake


router = APIRouter()

@router.post("/Georeference/create", tags=["Georeference"])
async def create_Georeference(snake_data: Snake):
    """
    Creates a new snake record in the database.

    Args:
        snake_data (Serpiente): The snake data to be inserted.

    Returns:
        Dict[str, str]: A dictionary containing a success message or error message.
    """
    response = await insert_georeferencia(
        nombre3=snake_data.nombre3,
        nombreCientifico=snake_data.nombreCientifico,
        reino=snake_data.reino,
        especie=snake_data.especie,
        clase=snake_data.clase,
        genero=snake_data.genero,
        familia=snake_data.familia,
    )
    return response


@router.get("/Georeference/all", tags=["Georeference"])
async def get_all_Georeference():
    response = await all_georeferencias()
    return response