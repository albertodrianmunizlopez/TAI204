from pydantic import BaseModel
from typing import Optional

class crear_usuario(BaseModel):
    nombre: str
    edad: int

class actualizar_usuario(BaseModel):
    nombre: Optional[str] = None
    edad: Optional[int] = None