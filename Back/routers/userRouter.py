from __future__ import annotations
import json
from fastapi import APIRouter, Depends, HTTPException,status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import sessionmaker
from typing import Annotated, Dict
from Database.models.DataBaseModel import Usuario, engine
from Database.models.PasswordHash import verificar_token
from Database.queries.userFuntions import insert_usuario,all_usuarios,get_usuario_nombre
from .base_models.user import User


router = APIRouter()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

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


