from __future__ import annotations
from fastapi import APIRouter, Body, Depends, File, Form
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from Database.queries.snakeFuntions import get_snake_base, insert_serpiente,all_Snakes,delete_snake
from .base_models.all_base_model import Serpiente
from fastapi import FastAPI, HTTPException, UploadFile
from typing import Annotated, List
import os
import uuid
from pathlib import Path

router = APIRouter()

# Definimos una carpeta para guardar las imágenes
images_dir = "images"

# Creamos la carpeta si no existe
Path(images_dir).mkdir(parents=True, exist_ok=True)

ALLOWED_IMAGE_EXTENSIONS = {"jpg", "jpeg", "png", "gif"}



@router.post("/upload_image",tags=["Files"])
async def create_upload_file(image: UploadFile):
    
    # Generate a unique identifier (UID) using UUID
    uid = uuid.uuid4().hex

    # Construct the filename using the UID and the original filename extension
    filename = f"{uid}.{image.filename.split('.')[-1]}"

    extension = filename.split(".")[-1].lower()  # Get lowercase extension
    if extension not in ALLOWED_IMAGE_EXTENSIONS:
        raise HTTPException(status_code=415, detail="Unsupported image format")


    # Save the image to the specified location using the UID-based filename
    image_path = os.path.join("images", filename)
    with open(image_path, "wb") as f:
        f.write(image.file.read())

    # Generate the URL to access the uploaded image
    image_url = f"{filename}"

    return (image_url)


# Ruta para ver la imagen
@router.get("/view_image/")
async def view_image(imagen:str):
    # Cambia esto para apuntar a la ubicación correcta de la imagen

    return FileResponse(images_dir+'/'+imagen)


@router.get("/snake/id", tags=["Snake"])
async def get_snake_id(id:int):
    response = await get_snake_base(id)
    if(response != None):
        return response
    else:
        raise HTTPException(status_code=404, detail=f"Id no encontrado: {id}")


@router.post("/snake/create", tags=["Snake"])
async def post_snake_create(serpiente:Serpiente):
    response = await insert_serpiente(
        serpiente
    )
    
    return (
        response
    )



@router.delete("/snake/delete", tags=["Snake"])
async def delete_report_id(id:int):
    id_verif = await get_snake_id(id)
    if (id_verif!=None):
        reponse = await delete_snake(id)
        return reponse


@router.get("/Snake/all", tags=["Snake"])
async def get_all_snakes():
    response = await all_Snakes()
    return response