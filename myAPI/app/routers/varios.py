import asyncio
from fastapi import APIRouter

routerV = APIRouter(
    prefix="/varios",
    tags=["Varios"]
)

# Ruta de bienvenida
@routerV.get("/")
async def bienvenido():
    return {
        "mensaje": "Bienvenido a rutas varias"
    }

# Ejemplo async
@routerV.get("/hola")
async def hola():
    await asyncio.sleep(2)
    return {
        "mensaje": "Hola mundo (async)",
        "status": 200
    }