import asyncio
#importamos 
from typing import Optional

from app.data.database import usuarios
from fastapi import APIRouter

routerV = APIRouter(
    prefix="/varios", 
    tags=["Varios"]
)


@routerV.get("/bienvenidos")

async def bienvenido():
    return{"mesage":"Bienvenido a fastapi"}


@routerV.get("/espera")
async def hola():
    await asyncio.sleep(5)
    return{"mesage":"Bienvenido a fastapi",
           "status":"200"
    }
    
@routerV.get("/usuario{id}")
async def consultauno(id:int):
    return{"mesage":"usuario encontrado","usuario":id,"status":"200"}
          
           
           
@routerV.get("/buscar")

async def consultatodos(id:Optional[int]=None):
    if id is not None:
    
        
        for usuarioK in usuarios:
            if usuarioK["id"] == id:
             return{"mesage":"usuario encontrado", "usuario":usuarioK,"status":"200"}
         
            
        return {"mesage":"usuario no encontrado"}
    
    
    else:
        return{"message":"no se proporciono el id"}