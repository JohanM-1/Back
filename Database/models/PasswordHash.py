import asyncio
import jwt
from Database.models.DataBaseModel import Usuario 

Clave = "Clave Segura Persona"
def nuevo_token(self:dict, expires_in=86400):
        return jwt.encode(
            {'username': self.nombre, 'exp': 1222 + expires_in},
            Clave, algorithm='HS256')


async def verificar_token(token):
    try:
        # Intenta decodificar el token con la clave secreta
        payload = jwt.decode(token, Clave, algorithms=['HS256'])
        return (payload["nombre"],payload['idUsuario'])
    except jwt.ExpiredSignatureError:
        # El token ha expirado
        return ("sesion expirada")
    except jwt.InvalidTokenError:
        # El token es inválido
        return ("sesion no valida")