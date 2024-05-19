from __future__ import annotations
import json
from fastapi import APIRouter, Depends, HTTPException,status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import sessionmaker
from typing import Annotated, Dict
from Database.models.DataBaseModel import Usuario, engine
from Database.models.PasswordHash import verificar_token
from Database.queries.userFuntions import insert_usuario,all_usuarios,Login_Verificacion

from .base_models.user import User,UserLogin,Response


router = APIRouter()


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
            edad=user_data.edad,)
    return response


@router.get("/users/all", tags=["users"])
async def get_all_users():
    response = await all_usuarios()
    return response

@router.post("/users/login",tags=["users"])
async def login_user(user_data:UserLogin):
    Response = await Login_Verificacion(user_data.email,user_data.password)
    if(Response.status):
        return Response
    else:
        raise HTTPException(status_code=401, detail=Response.message)
    pass


