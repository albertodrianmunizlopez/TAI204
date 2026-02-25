# main.py
from fastapi import FastAPI, status, HTTPException
import asyncio
from typing import Optional
from pydantic import BaseModel

app = FastAPI(
    title="Mi Primer API",
    description="Jose Angel Sanchez Linares",
    version="1.0"
)

# Base de datos ficticia
usuarios = [
    {"id": 1, "nombre": "Diego","edad": 21},
    {"id": 2, "nombre": "Coral","edad": 21},
    {"id": 3, "nombre": "Saul","edad": 21}
]

# Modelo Pydantic
class CrearUsuario(BaseModel):
    id: int
    nombre: str
    edad: int

@app.get("/")
async def bienvenida():
    return {"mensaje": "Bienvenido a FastAPI"}

@app.get("/v1/usuarios/")
async def consultaT():
    return {
        "status": "200",
        "total": len(usuarios),
        "Usuarios": usuarios
    }

@app.post("/v1/usuarios/")
async def agregar_usuario(usuario: CrearUsuario):
    for usr in usuarios:
        if usr["id"] == usuario.id:
            raise HTTPException(
                status_code=400,
                detail="El id ya existe"
            )
    usuarios.append(usuario.dict())  # 
    return {
        "mensaje": "Usuario agregado",
        "usuario": usuario,
        "status": "200"
    }

@app.delete("/v1/usuarios/{id}")
async def eliminar_usuario(id: int):
    global usuarios
    usuarios = [usr for usr in usuarios if usr["id"] != id]
    return {
        "mensaje": "Usuario eliminado",
        "status": "200"
    }

@app.put("/v1/usuarios/")
async def modificar_usuario(usuario: CrearUsuario):
    for i, usr in enumerate(usuarios):
        if usr["id"] == usuario.id:
            usuarios[i] = usuario.dict()
            return {
                "mensaje": "Usuario modificado",
                "usuario": usuario,
                "status": "200"
            }
    raise HTTPException(
        status_code=404,
        detail="El id no existe"
    )