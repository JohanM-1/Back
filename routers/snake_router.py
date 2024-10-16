from __future__ import annotations
from fastapi import APIRouter, UploadFile, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from Database.queries.snakeFuntions import (
    all_Snakes_poison,
    get_snake_base,
    insert_serpiente,
    all_Snakes,
    delete_snake,
)
from .base_models.all_base_model import Serpiente
from pathlib import Path
import os
import uuid
from typing import Annotated

router = APIRouter()

images_dir = "images"
Path(images_dir).mkdir(parents=True, exist_ok=True)

ALLOWED_IMAGE_EXTENSIONS = {"jpg", "jpeg", "png", "gif"}

@router.post("/upload_image", tags=["Files"])
async def create_upload_file(image: UploadFile):
    uid = uuid.uuid4().hex
    filename = f"{uid}.{image.filename.split('.')[-1]}"

    extension = filename.split(".")[-1].lower() 
    if extension not in ALLOWED_IMAGE_EXTENSIONS:
        raise HTTPException(status_code=415, detail="Unsupported image format")

    image_path = os.path.join(images_dir, filename)
    with open(image_path, "wb") as f:
        f.write(image.file.read())

    image_url = f"{filename}"
    return {"image_url": image_url}

# Ruta para ver la imagen
@router.get("/view_image/")
async def view_image(imagen: str):
    return FileResponse(os.path.join(images_dir, imagen))

@router.get("/snake/id", tags=["Snake"])
async def get_snake_id(id: int):
    response = await get_snake_base(id)
    if response is not None:
        return response
    else:
        raise HTTPException(status_code=404, detail=f"Id no encontrado: {id}")

@router.post("/snake/create", tags=["Snake"])
async def post_snake_create(serpiente: Serpiente):
    response = await insert_serpiente(serpiente)
    return response

@router.delete("/snake/delete", tags=["Snake"])
async def delete_snake_id(id: int):
    id_verif = await get_snake_id(id)
    if id_verif is not None:
        response = await delete_snake(id)
        return response
    else:
        raise HTTPException(status_code=404, detail=f"Id no encontrado: {id}")

@router.get("/Snake/all", tags=["Snake"])
async def get_all_snakes():
    response = await all_Snakes()
    return response

@router.get("/Snakes/poison", tags=["Snake"])
async def get_all_snakes(valid: bool):
    response = await all_Snakes_poison(valid)
    return response
