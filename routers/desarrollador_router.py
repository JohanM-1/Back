from __future__ import annotations
from fastapi import APIRouter
from .base_models.all_base_model import Desarrollador


router = APIRouter()

@router.post("/desarrolladores")
async def create_desarrollador(desarrollador: Desarrollador):
    # Use `SessionLocal` to interact with the database if necessary
    # ...
    return {"message": "Developer created successfully!"}
