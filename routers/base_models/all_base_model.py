from pydantic import BaseModel, EmailStr, Field

class Usuario(BaseModel):
    idUsuario: int = Field(..., description="Unique identifier for the user")
    correo: EmailStr = Field(..., description="User's email address")
    direccion: str = Field(..., max_length=45, description="User's address")
    contraseña: str = Field(..., max_length=100, description="User's password (hashed)")
    nombre: str = Field(..., max_length=45, description="User's first name")
    apellido: str = Field(..., max_length=45, description="User's last name")
    fecha_n: str = Field(..., max_length=45, description="User's birth date")
    rol: str = Field(..., max_length=45, description="User's role (e.g., admin, user)")
    edad: int = Field(..., description="User's age")

    class Config:
        orm_mode = True  # Enable automatic ORM mode if using SQLAlchemy
        arbitrary_types_allowed = True  # Allow custom types like Mapped

    def __repr__(self):
        return f"Usuario(id={self.idUsuario}, nombre='{self.nombre} {self.apellido}', correo='{self.correo}')"


class Desarrollador(BaseModel):
    idDesarrollador: int = Field(..., description="Unique identifier for the developer")
    nombre2: str = Field(..., max_length=20, description="Developer's name")
    direccion2: str = Field(..., max_length=45, description="Developer's address")

    class Config:
        orm_mode = True  # Enable automatic ORM mode if using SQLAlchemy
        arbitrary_types_allowed = True


class Serpiente(BaseModel):
    idSerpiente: int = Field(..., description="Unique identifier for the snake")
    nombre3: str = Field(..., max_length=45, description="Snake's common name")
    nombreCientifico: str = Field(..., max_length=100, description="Snake's scientific name")
    reino: str = Field(..., max_length=45, description="Animal kingdom")
    especie: str = Field(..., max_length=45, description="Snake species")
    clase: str = Field(..., max_length=45, description="Taxonomic class")
    genero: str = Field(..., max_length=45, description="Snake genus")
    familia: str = Field(..., max_length=45, description="Snake family")

    class Config:
        orm_mode = True  # Enable automatic ORM mode if using SQLAlchemy
        arbitrary_types_allowed = True


class Georeferencia(BaseModel):
    idGeoreferencia: int = Field(..., description="Unique identifier for the georeference")
    fecha: str = Field(..., max_length=20, description="Date of georeference")
    zona: str = Field(..., max_length=100, description="Georeferenced area")
    coordenadas: str = Field(..., max_length=200, description="Geographic coordinates")

    # Foreign Key relationships (if using SQLAlchemy)
    # serpientes_id_serpientes: int = Field(..., description="Foreign key to Serpiente.idSerpiente")
    # usuario_id_usuario: int = Field(..., description="Foreign key to Usuario.idUsuario")
    # desarrollador_id_desarrollador: int = Field(..., description="Foreign key to Desarrollador.idDesarrollador")

    # Relationship fields (if using SQLAlchemy)
    # serpiente: Serpiente = relationship("Serpiente", backref="georeferencias")
    # usuario: Usuario = relationship("Usuario", backref="georeferencias")

    class Config:
        orm_mode = True  # Enable automatic ORM mode if using SQLAlchemy
        arbitrary_types_allowed = True


class Reporte(BaseModel):
    idReporte: int = Field(..., description="Unique identifier for the report")
    titulo: str = Field(..., max_length=100, description="Report title")
    descripcion: str = Field(..., max_length=1000, description="Detailed description of the snake sighting, including location, appearance, and behavior.")
    comentario: str = Field(..., max_length=250, description="Optional comments about the report, such as identification assistance or additional observations.")

    # Foreign Key relationships (if using SQLAlchemy)
    serpientes_id_serpientes: int = Field(..., description="Foreign key to Serpiente.idSerpiente")
    usuario_id_usuario: int = Field(..., description="Foreign key to Usuario.idUsuario")
    desarrollador_id_desarrollador: int = Field(..., description="Foreign key to Desarrollador.idDesarrollador")


    class Config:
        orm_mode = True  # Enable automatic ORM mode if using SQLAlchemy
        arbitrary_types_allowed = True
