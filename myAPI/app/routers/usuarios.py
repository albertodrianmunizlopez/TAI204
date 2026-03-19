from fastapi import APIRouter, HTTPException, status, Depends
from typing import Optional
from app.data.database import usuarios
from app.models.usuarios import CrearUsuario
from app.security.auth import verificar_peticion
import asyncio

router = APIRouter(
    prefix="/usuarios",
    tags=["Usuarios"]
)

# Bienvenida
@router.get("/")
async def inicio():
    return {"mensaje": "API de usuarios"}

# Async ejemplo
@router.get("/hola")
async def hola():
    await asyncio.sleep(2)
    return {"mensaje": "Hola mundo"}

# Obtener todos o uno
@router.get("/buscar")
async def obtener_usuario(id: Optional[int] = None):
    if id:
        for u in usuarios:
            if u["id"] == id:
                return u
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuarios

# Crear usuario
@router.post("/")
async def crear(usuario: CrearUsuario):
    for u in usuarios:
        if u["id"] == usuario.id:
            raise HTTPException(status_code=400, detail="ID ya existe")

    usuarios.append(usuario.dict())
    return {"mensaje": "Usuario agregado", "usuario": usuario}

# Actualizar
@router.put("/")
async def actualizar(usuario: dict):
    for u in usuarios:
        if u["id"] == usuario.get("id"):
            u.update(usuario)
            return {"mensaje": "Actualizado", "usuario": u}

    raise HTTPException(status_code=404, detail="Usuario no encontrado")

# Eliminar
@router.delete("/{id}")
async def eliminar(id: int, user: str = Depends(verificar_peticion)):
    for i, u in enumerate(usuarios):
        if u["id"] == id:
            usuarios.pop(i)
            return {"mensaje": f"Eliminado por {user}"}

    raise HTTPException(status_code=404, detail="Usuario no encontrado")