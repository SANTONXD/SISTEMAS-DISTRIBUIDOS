from pydantic import BaseModel

class LibroBase(BaseModel):
    titulo: str
    autor: str
    genero: str
    precio: float
    stock: int

class LibroCreate(LibroBase):
    pass

class Libro(LibroBase):
    id: int
    class Config:
        orm_mode = True
