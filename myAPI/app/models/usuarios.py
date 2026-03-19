from pydantic import BaseModel, Field

class CrearUsuario(BaseModel):
    id: int = Field(..., gt=0)
    nombre: str = Field(..., min_length=3, max_length=50)
    edad: int = Field(..., ge=1, le=125)