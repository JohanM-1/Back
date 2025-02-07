import json
import typing
import google.generativeai as genai
import os
from fastapi import  APIRouter, HTTPException, UploadFile
import uuid
from pathlib import Path
from googleapiclient.errors import HttpError
import pathlib
import textwrap
import asyncio
from openai import OpenAI, OpenAIError
import base64

import google.generativeai as genai

from IPython.display import display
from IPython.display import Markdown

def to_markdown(text : str):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))



router = APIRouter()

# Definimos una carpeta para guardar las imágenes
images_dir = "images"

# Creamos la carpeta si no existe
Path(images_dir).mkdir(parents=True, exist_ok=True)

ALLOWED_IMAGE_EXTENSIONS = {"jpg", "jpeg", "png", "gif"}



@router.post("/snakeidentify",tags=["Files"])
async def create_upload_file(image: UploadFile):
    class ResponseJson(typing.TypedDict):
        title: str
        body: str
        venomous: bool
    
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


    try:
        # Intentar primero con Gemini con timeout de 5 segundos
        myfile = genai.upload_file("images/"+image_url)
        model = genai.GenerativeModel("gemini-1.5-flash")

        class Recipe(typing.TypedDict):
            name: str
            description: str
            venomous: bool
            issnake: bool
            service: str



        async def get_gemini_response():
            return model.generate_content(
                ["identifica la serpiente de la imagen, si es venenosa o no y en la descripcion agregar que hacer en caso de una mordedura de esta serpiente como en un paso a pose, la respuesta debe ser en español", myfile],
                generation_config=genai.GenerationConfig(
                    response_mime_type="application/json", response_schema=Recipe
                ),
            )

        try:
            result = await asyncio.wait_for(get_gemini_response(), timeout=1)
            formatted_json = json.loads(result.text)
            formatted_json["service"] = "Gemini"
        except asyncio.TimeoutError:
            raise Exception("Timeout en Gemini")
        
    except Exception as e:
        print(f"Gemini error: {str(e)}")
        try:
            # Fallback a ChatGPT con timeout de 30 segundos
            client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
            
            # Leer la imagen y convertirla a base64
            image.file.seek(0)
            image_data = image.file.read()
            base64_image = base64.b64encode(image_data).decode('utf-8')
            
            async def get_chatgpt_response():
                return client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "text",
                                    "text": "Analiza esta imagen de serpiente y responde SOLO en formato JSON válido con esta estructura exacta: {\"name\": \"nombre de la serpiente\", \"description\": \"descripción y pasos a seguir\", \"venomous\": true/false, \"issnake\": true/false}"
                                },
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:image/{extension};base64,{base64_image}"
                                    }
                                }
                            ]
                        }
                    ]
                )

            try:
                response = await asyncio.wait_for(get_chatgpt_response(), timeout=1)
                response_text = response.choices[0].message.content.strip()
                
                # Intentar encontrar el JSON en la respuesta
                try:
                    # Buscar el primer { y último } en caso de que haya texto adicional
                    start_idx = response_text.find('{')
                    end_idx = response_text.rfind('}') + 1
                    if start_idx != -1 and end_idx != 0:
                        json_str = response_text[start_idx:end_idx]
                        formatted_json = json.loads(json_str)
                    else:
                        raise json.JSONDecodeError("No JSON found", response_text, 0)
                    
                    formatted_json["service"] = "ChatGPT"
                except json.JSONDecodeError as e:
                    print(f"JSON Error: {str(e)}")
                    print(f"Response received: {response_text}")
                    raise HTTPException(
                        status_code=500,
                        detail="Error al procesar la respuesta del servicio de AI. Por favor intente nuevamente."
                    )
            except asyncio.TimeoutError:
                raise HTTPException(
                    status_code=504,
                    detail="El servicio está tardando demasiado tiempo en responder. Por favor intente nuevamente."
                )
            
        except Exception as e:
            print(f"ChatGPT error: {str(e)}")
            raise HTTPException(
                status_code=503,
                detail="El servicio de AI está desactivado. Por favor comuníquese con un administrador."
            )

    # Limpiar la imagen
    if os.path.exists("images/"+image_url):
        os.remove("images/"+image_url)
        print("La imagen ha sido eliminada exitosamente.")

    formatted_json["description"] += " Numero de emergencias: Fauna Cormacarena (+57 321 4820327)"
    
    return formatted_json



