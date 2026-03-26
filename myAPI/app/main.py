#importaciones

from fastapi import FastAPI, APIRouter
#importar los routers el de usuarios y el de varios 
from app.routers import usuarios,varios

#agregamos dos importraciones importamos el motor de conexiones ese motoro lo definimos en db

from app.data.db import engine

#importamnos para decir conectate y genrame esta tabla en caso de que no este
from app.data import usuario

#si no esta la tabla que acabampos de decirle usa esta conexion para poder crearla
usuario.Base.metadata.create_all(bind= engine)

app=FastAPI(
    title="Mi primer API",
    description="Alberto Adrian Muiz Lopez",
    version="1.0"   
)

app.include_router(usuarios.router)
app.include_router(varios.routerV)
