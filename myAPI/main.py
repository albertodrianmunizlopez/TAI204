#Importaciones
from fastapi import FastAPI
import asyncio
from typing import Optional #Especificar endpoint puedo o no puede pasar parametros

#Instancia del servidor
app = FastAPI(
    tittle = "Mi primer API",        #Se personaliza con la informacion 
    description = "Alberto M L",     # que proporcionemos
    version = "1.0"
)

#Tabla Ficticia
usuarios =[
            {"id":1,"nombre":"Diego","edad":21},
            {"id":2,"nombre":"Coral","edad":21},
            {"id":3,"nombre":"Saul","edad":21},

]


#Endpoints
@app.get("/",tags = ['Inicio'])   #Sirve para nombrar las acciones 
async def bienvenida():
    return {"mesaje": "Bienvenido a FastAPI"}

@app.get("/holaMundo", tags = ['Asincronia'])    #Nombra las acciones 
async def Hola():
    await asyncio.sleep(5)#Peticion, consultaBD, Archivo
    return {
        "mesaje": "Hola Mundo",
        "status": "200"
        }

#Endpoints Nuevo con parametros 
@app.get("/v1/usuario/{id}",tags = ['Parametro Obligatorio'])   #Parametro Obigatorio { }
async def consultauno(id:int):

    return {"mesaje": "Usuario encontrado",
            "usuario":id,
            "Status":"200" }

#Endpoints Nuevo con parametros        3 endpoint con mismo nombre con dif post get etc
@app.get("/v1/usuarios/",tags = ['Parametro Opcional'])   #Parametro opcional
async def consultatodos(id:Optional[int]=None): #en caso de ser opcional y si no vien ponlo nulo
    if id is not None: 
        for usuarioK in usuarios: #Llave usuuariosK a la tabla
            if usuarioK["id"] == id:#Busca la posicion y si la encontro 
                return{"mensaje":"Usuario encontrado ","usuario":usuarioK}  #mandar un json 
        return {"mensaje":"Usuario no encontrado","status":"200"}    
    else:
        return {"mensaje":"No se proporciono id"}
    
            
#Faltan caso donde no lo encontro y el default que no pasen usuarios
