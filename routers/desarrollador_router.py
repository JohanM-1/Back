from __future__ import annotations
from fastapi import APIRouter
from .base_models.all_base_model import Desarrollador
from Database.queries.desarroladorFuntions import insert_desarrollador,all_desarrolladores


router = APIRouter()

@router.post("/Desarrollador/Create", tags=["Desarrollador"])
async def create_Desarrollador(Desarrollador_data: Desarrollador):
    """
    Creates a new snake record in the database.

    Args:
        snake_data (Serpiente): The snake data to be inserted.

    Returns:
        Dict[str, str]: A dictionary containing a success message or error message.
    """
    response = await insert_desarrollador(
        nombre2=Desarrollador_data.nombre2,
        direccion2=Desarrollador_data.direccion2
    )
    return response

@router.get("/Desarrollador/all", tags=["Desarrollador"])
async def get_all_Georeference():
    response = await all_desarrolladores()
    return response
