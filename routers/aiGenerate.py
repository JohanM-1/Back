import google.generativeai as genai
import os
from fastapi import  APIRouter, HTTPException, UploadFile
import os
import uuid
from pathlib import Path

router = APIRouter()

# Definimos una carpeta para guardar las imágenes
images_dir = "images"

# Creamos la carpeta si no existe
Path(images_dir).mkdir(parents=True, exist_ok=True)

ALLOWED_IMAGE_EXTENSIONS = {"jpg", "jpeg", "png", "gif"}



@router.post("/snakeidentify",tags=["Files"])
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
    genai.configure(api_key=os.environ["API_KEY"])


    myfile = genai.upload_file("images/"+image_url)
    print(f"{myfile=}")
    model = genai.GenerativeModel("gemini-1.5-flash")
    result = model.generate_content(
        [myfile, "Identify the species of snake in this image and porcent the acert. Is it venomous? Please provide the answer in Spanish."]
    )
    textResult = result.text.strip()
    print(textResult)
    if(textResult):

        return (textResult)



