from __future__ import annotations
from fastapi import APIRouter, Body, Depends, File, Form
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from Database.queries.snakeFuntions import insert_serpiente,all_Snakes
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


async def upload_image(image: UploadFile = File(...)):
    
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



@router.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    return {"filename": file.filename}



    
@router.post("/Snake/create", tags=["Snake"])
async def create_snakedata(textColumnNames: List[str] = Form(...),
               idColumn: str = Form(...),
               csvFile: UploadFile = File(...)):
    """
    Creates a new snake record in the database.

    Args:
        snake_data (Serpiente): The snake data to be inserted.

    Returns:
        Dict[str, str]: A dictionary containing a success message or error message.
    """

    return 


@router.get("/Snake/all", tags=["Snake"])
async def get_all_snakes():
    response = await all_Snakes()
    return response