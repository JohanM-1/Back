from pydantic import BaseModel, EmailStr, constr

from routers.base_models.all_base_model import Usuario


class User(BaseModel):
    nombres: str | None = None
    correo: EmailStr | None = None
    direccion: str | None = None
    contraseña: str | None = None
    apellido: str | None = None
    fecha_n: str | None = None
    rol: str | None = None
    edad: int | None = None
    imagen: str | None = None
    Descripcion: str | None = None
    imagen_fonodo: str | None = None
    
    
class UserLogin(BaseModel):
    nombres: str
    email: EmailStr
    password: str
    
class Response(BaseModel):
    status: bool
    message: str
    data: User | None = None
    access_token: str | None = None

class Snake(BaseModel):
  nombre3: str   # Common name of the snake (required)
  nombreCientifico: str   # Scientific name (required)
  reino: str   # Kingdom (required)
  especie: str   # Species (required)
  clase: str   # Class (required)
  genero: str  # Genus (required)
  familia: str  # Family (required)


