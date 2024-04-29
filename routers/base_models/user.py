from pydantic import BaseModel, EmailStr

class User(BaseModel):
    nombres: str | None = None
    correo: EmailStr | None = None
    direccion: str | None = None
    contraseña: str | None = None
    apellido: str | None = None
    fecha_n: str | None = None
    rol: str | None = None
    edad: int | None = None