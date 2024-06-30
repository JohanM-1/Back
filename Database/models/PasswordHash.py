
import jwt
from passlib.context import CryptContext
import asyncio
Clave = "Clave Segura Persona"




async def nuevo_token(Nombre:str,id:int,rol:str):
        return jwt.encode(
            {'id': id, 'nombre':Nombre,'rol' :rol},
            Clave, algorithm='HS256')

    #verificar si un token es valido

async def verificar_token(token:str):
    try:
        # Intenta decodificar el token con la clave secreta payload["nombre"],payload['id'],payload["rol"]
        payload = jwt.decode(token, Clave, algorithms=['HS256'])
        return (payload["nombre"],payload['id'],payload["rol"])
    except jwt.ExpiredSignatureError:
        # El token ha expirado
        return ("sesion expirada")
    except jwt.InvalidTokenError:
        # El token es inválido
        return ("sesion no valida")
    
    
#Funcion para hashear la contraseña para posteriormente guardarla en la base de datos
#devuelve un string de tipo hash
async def crear_hash(Valor:str)->str:
    #objeto de clase CryptContext para Hasheo de la contraseña
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    hash_password = pwd_context.hash(Valor)
    print(hash_password)
    return hash_password

#verifica el has si es corecto Devuelve un true si es no es por x o y razon devuelve false

async def verificar_hash(password_entrada: str, password_base: str) -> bool:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    # Hashear la contraseña de entrada
    password_entrada_hasheada = pwd_context.hash(password_entrada)

    # Verificar si la contraseña hasheada coincide con la contraseña base
    if pwd_context.verify(password_entrada, password_base):
        return True
    else:
        return False

#ejemplo de uso de funcion asyncio.run(crear_hash("asdasdsdad"))
