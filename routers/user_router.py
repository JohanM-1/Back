from __future__ import annotations
import json
import re
from fastapi import APIRouter, Depends, HTTPException, Request,status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import firebase_admin
from httplib2 import Credentials
import pyrebase
from sqlalchemy.orm import sessionmaker
from typing import Annotated, Dict
from Database.models.DataBaseModel import Usuario, engine
from Database.models.PasswordHash import verificar_token
from Database.queries.userFuntions import  Login_Verificacion_username, check_user_email, edit_user_DB, edit_user_DB_pass, insert_usuario,all_usuarios,Login_Verificacion, login_auth_provider
from routers.base_models.all_base_model import UserTokenModelResp


from .base_models.user import User,UserLogin,Response



from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from pydantic import BaseModel, Field
from firebase_admin import auth,credentials
import os
from dotenv import load_dotenv


router = APIRouter()

# Cargar variables de entorno
load_dotenv()

def verify_firebase_credentials():
    """Verifica si las credenciales de Firebase están configuradas correctamente"""
    try:
        if not os.path.exists(os.getenv('FIREBASE_CREDENTIALS_PATH')):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Firebase credentials file not found"
            )
        
        cred = credentials.Certificate(os.getenv('FIREBASE_CREDENTIALS_PATH'))
        if not firebase_admin._apps:
            firebase_admin.initialize_app(cred)
        return True
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Firebase initialization error: {str(e)}"
        )

# Verificar credenciales al inicio
verify_firebase_credentials()

# Configuración de Firebase usando variables de entorno
firebaseConfig = {
    "apiKey": os.getenv('FIREBASE_API_KEY'),
    'authDomain': os.getenv('FIREBASE_AUTH_DOMAIN'),
    'projectId': os.getenv('FIREBASE_PROJECT_ID'),
    'storageBucket': os.getenv('FIREBASE_STORAGE_BUCKET'),
    'messagingSenderId': os.getenv('FIREBASE_MESSAGING_SENDER_ID'),
    'appId': os.getenv('FIREBASE_APP_ID'),
    'measurementId': os.getenv('FIREBASE_MEASUREMENT_ID'),
    'databaseURL': os.getenv('FIREBASE_DATABASE_URL')
}

# Verificar que todas las configuraciones necesarias estén presentes
required_configs = ['apiKey', 'authDomain', 'projectId', 'storageBucket', 'messagingSenderId', 'appId']
missing_configs = [key for key in required_configs if not firebaseConfig.get(key)]

if missing_configs:
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"Missing Firebase configurations: {', '.join(missing_configs)}"
    )

try:
    firebase = pyrebase.initialize_app(firebaseConfig)
except Exception as e:
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"Firebase initialization error: {str(e)}"
    )

class Token (BaseModel):
    access_token: str
    token_type: str


@router.post("/users/create", tags=["users"])
async def create_user(user_data:User):
    response = await insert_usuario(            
            nombres=user_data.nombres,
            correo=user_data.correo,
            direccion=user_data.direccion,
            contraseña=user_data.contraseña,
            apellido=user_data.apellido,
            fecha_n=user_data.fecha_n,
            rol="usuario",
            edad=user_data.edad,
            imagen=user_data.imagen,
            )
    return response

import secrets
import string

def generar_contraseña_segura(longitud=12):
    """Generate password

    Args:
        longitud: int large password.

    Returns:
        str: password generate.
    """

    caracteres = string.ascii_letters + string.digits + string.punctuation
    contraseña = ''.join(secrets.choice(caracteres) for _ in range(longitud))
    return contraseña  


@router.post("/users/google-auth", tags=["users"])
async def get_user_id(id: str):
    try:
        # Primero verificamos que Firebase esté correctamente inicializado
        if not firebase_admin._apps:
            verify_firebase_credentials()
            
        try:
            # Intentamos obtener el usuario
            user = auth.get_user(id)
        except auth.InvalidIdTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid Firebase ID token"
            )
        except auth.ExpiredIdTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Firebase token has expired"
            )
        except auth.RevokedIdTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Firebase token has been revoked"
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Firebase authentication error: {str(e)}"
            )

        # Si llegamos aquí, el token es válido
        try:
            bool = await check_user_email(user.email)
            if not bool:
                await insert_usuario(            
                    nombres=user.display_name,
                    correo=user.email,
                    direccion="",
                    contraseña=id,
                    apellido="",
                    fecha_n="null",
                    rol="usuario",
                    edad=0,
                    imagen=user.photo_url,
                )

            response = await Login_Verificacion(user.email, id)
            return response
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database operation failed: {str(e)}"
            )
            
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error: {str(e)}"
        )


def verify_firebase_id_token(token):
    """
    A helper function for verifying ID tokens issued by Firebase.
    See https://firebase.google.com/docs/auth/admin/verify-id-tokens for
    more information.

    Parameters:
       token (str): A token issued by Firebase.

    Output:
       auth_context (dict): Authentication context.
    """
    try:
        full_auth_context = auth.verify_id_token(token,check_revoked=True,clock_skew_seconds=0)
    except InvalidTokenError:
        return {"error"}

    auth_context = {
        'username': full_auth_context.get('name'),
        'uid': full_auth_context.get('uid'),
        'email': full_auth_context.get('email')
    }
    return auth_context 


@router.get("/users/google-auth-token", tags=["users"])
async def get_user_id(request: Request):
    try:
        headers = request.headers
        jwt = headers.get('authorization')
        jwt = re.sub(r'^Bearer\s+', '', jwt)
        user = verify_firebase_id_token(jwt)
        print(user['uid'])
        user = auth.get_user(user['uid'])
        print(user.email)
        print(user.photo_url)
        bool = await check_user_email(user.email)
        if( bool == False):
            await insert_usuario(            
            nombres=user.display_name,
            correo=user.email,
            direccion= "",
            contraseña= generar_contraseña_segura(),
            apellido="",
            fecha_n= "null",
            rol= "usuario",
            edad= 0,
            imagen= user.photo_url,
            )


        response = await login_auth_provider(user.email)
        return response
        
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )





@router.get("/users/all", tags=["users"])
async def get_all_users():
    try:
        user = auth.get_user("yjFmIs1SPCWLcwMm4PEWBsXTu8U2")
        print(user.display_name)
    except:
        print("error")
    response = await all_usuarios()
    return response



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = await Login_Verificacion(form_data.username,form_data.password)
    if (user.status == False):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return Token(access_token=user.access_token, token_type="bearer")


async def verificar_token_route(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
        
    var = await verificar_token(token)

    if (var is not UserTokenModelResp):
        return var
    else:
        
        raise credentials_exception

async def get_current_active_user(
    current_user: Annotated[User, Depends(verificar_token_route)],
):
    return current_user

@router.get("/users/me/", response_model=UserTokenModelResp,tags=["users"])
async def read_users_me(
    current_user: Annotated[UserTokenModelResp, Depends(get_current_active_user)],
):
    return current_user


class Usuario_Edit(BaseModel):
    
    nombre: str 
    imagenurl: str 
    imagen_fonodo: str | None = None
    Descripcion: str | None = None


@router.post("/usuario/edit", tags=["users"])
async def edit_user_route(
    data: Usuario_Edit,
    current_user: Annotated[UserTokenModelResp, Depends(get_current_active_user)]
    ):
    
    response = await edit_user_DB(
        id=current_user.id,
        nombre= data.nombre,
        imagen_url= data.imagenurl,
        imagen_fonodo= data.imagen_fonodo,
        Descripcion=data.Descripcion,

    )

    return response



class UsuarioEditPass(BaseModel):
    
    nombre: str | None = None
    password: str | None = None
    email: str | None = None


@router.post("/usuario/editpass", tags=["users"])
async def edit_user_route_pass(
    data: UsuarioEditPass,
    current_user: Annotated[UserTokenModelResp, Depends(get_current_active_user)]
    ):
    
    response = await edit_user_DB_pass(
        id=current_user.id,
        nombre= data.nombre,
        email=data.email,
        password=data.password,

    )

    return response


@router.post("/usuario/editpassAdmin", tags=["users"])
async def edit_user_route_pass(
    data: UsuarioEditPass,
    id:int
    ):
    
    response = await edit_user_DB_pass(
        id=id,
        nombre= data.nombre,
        email=data.email,
        password=data.password,

    )

    return response



@router.post("/users/login", tags=["users"])
async def login_user_route(user_data: UserLogin):
    if "@" in user_data.identifier:
        # Verificación por correo electrónico
        Response = await Login_Verificacion(user_data.identifier, user_data.password)
    else:
        # Verificación por nombre de usuario
        Response = await Login_Verificacion_username(user_data.identifier, user_data.password)

    if Response.status:
        return Response
    else:
        raise HTTPException(status_code=401, detail=Response.message)
    

@router.get("/firebase/test-credentials", tags=["users"])
async def test_firebase_credentials():
    try:
        verify_firebase_credentials()
        # Intenta una operación simple con Firebase
        auth.get_user_by_email("test@test.com")
        return {"status": "success", "message": "Firebase credentials are valid"}
    except auth.UserNotFoundError:
        # Este error es normal si el usuario no existe
        return {"status": "success", "message": "Firebase credentials are valid"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Firebase credentials error: {str(e)}"
        )
    