#importaciones
#status es para manejar los estados de las respuestas HTTP
#HTTPException es para manejar las excepciones HTTP y enviar respuestas de error personalizadas
from fastapi import FastAPI, status, HTTPException
import asyncio
#importamos 
from typing import Optional
from pydantic import BaseModel   #Modelo pydantic

#agregar dos nuevas importaciones 


#instancia del servidor
#preparar todo el servidor con laas ventajas que ofrece fastapi 
app=FastAPI(
    title="Mi primer API",
    description="Alberto Adrian Muiñz Lopez",
    version="1.0"   
)

#tabla ficticia solo para verificar 
#datos para ver como nos responderia un diccionario de usuarios

usuarios=[
    {"id":1,"nombre":"Alberto","edad":20},
    {"id":2,"nombre":"Diego","edad":20},
    {"id":3,"nombre":"Jochua","edad":20}
]


#***************
#Modelo Pydantic de validacion 
#***************

class crear_Usuario(BaseModel):
    id: int 
    nombre: str
    edad: int



#Endpoints 
@app.get("/",tags=["inicio"])
#endpoint de inicio es la ruta con la que arrncara el servidor
async def bienvenido():
    return{"mesage":"Bienvenido a fastapi"}
#lado izquirdo clave 
#lado derecho el vamor en este caso clase es mensaje= valor igual a bienvenido a fastapi

#hasta aqui ya tenemos nuestro servidor ya esta funcionado 

#correr un servidor tenemos que ir a nuestra terminal

#segundo endpoint 

@app.get("/holamundo",tags=["Asincronia"])
async def hola():
    await asyncio.sleep(5)
    return{"mesage":"Bienvenido a fastapi",
           "status":"200"
           }
    
    
    
#Endpoints creamos otro Endpoints lo que tenemos en cuenta es que los parametros lo estamos 
#solicitando entre llaves  en este caso le decimos que para que v1 funcione es obligatorio un id 
#nos aseguramos que el id se obligatorio y que lleve con el formato que necvesitamos en este caso 
#sera entero es el mas comun 
#el id que llegue sera entero y para poder pasar la va;idacion tiene que ser entero
#cuidar las , por que son objetos JSON
@app.get("/v1/usuarioOb/{id}",tags=["parametro obligatorio"])
#endpoint de inicio es la ruta con la que arrncara el servidor
async def consultauno(id:int):
    return{"mesage":"usuario encontrado","usuario":id,"status":"200"}

#obligatorio que el paramtro este en el endpoint
    
    
    
    #4
    #no puede aver dos enpoints con el mismo nombre en este caso si los dos son get 
    #no pueden aver dos con el mismo nombre al menos que sean delete
    #aguas con las llaves por que no es oblitario este caso no es obligatorio 
    #y la funcion tiene que ser otro nombre por que si no reutilizamos la funcion del otro 
    #optional[int]= None puede que venga o no venga un dato y en caso de que no 
    #lo declaramos como nulo
    
@app.get("/v1/usuariosOp/",tags=["parametro obligatorio"])
#endpoint de inicio es la ruta con la que arrncara el servidor
async def consultatodos(id:Optional[int]=None):
    if id is not None:
        #verificamos si el id no es nulo con is not None  
        # si no es nulo quiere decir que viene con un valor 
        #recorremos con un for es la llave que va recorrriendo el for 
        #recorremos con usuarioK en la tabla usuarios
        
        for usuarioK in usuarios:
            if usuarioK["id"] == id:
             return{"mesage":"usuario encontrado", "usuario":usuarioK,"status":"200"}
            
            #caso donde si encontre al usuario en este caso si lo encontre
            #si el for acaba y nose encontro el usuario enconces se ejecuta el return de abajo
        
            
        return {"mesage":"usuario no encontrado"}
    
    #esto es por si el usuario no ingreso ningun id en el endpoint
    #si el id es nulo osea que no se proporciono ningun id en el endpoint se ejecuta este return
    else:
        return{"message":"no se proporciono el id"}
    
    
#crear un nuevo endpoint 
#etiqueta crud http para que se vea en la documentacion que es un endpoint de crud http
#y con laa funcion consultaT para consultar 
#todo lo que aremos sera simular las acciones en la tabla que tebemos arriba 
#creammos un json y contendra status

@app.get("/v1/usuarios/",tags=['CRUD HTTP'])
async def consultaT():
    return{
        # lo que estamos haciendo aqui es simular una consulta a la tabla de usuarios que tenemos arriba
        #status es el estado de la consulta en este caso 200
        #total es el total de usuarios que tenemos en la tabla en este caso len(usuarios) nos da el total de usuarios
        #
        "status":"200",
        "total":len(usuarios),
        "usuarios":usuarios
          
    }
    
   
    
#vamos a hacer un enpoint de tipo post 
#pueden tener el mismo nombre y no hay conflicto ya que cada uno va a su camino
#post se usa para crear
#agregar un nuevo usuario a la tabla de usuarios que tenemos arriba
#el nuevo usuario lo vamos a recibir en formato json y 
#lo vamos a agregar a la tabla de usuarios que tenemos arriba

@app.post("/v1/usuarios/",tags=['CRUD HTTP'])  
async def agregar_usuario(usuario:crear_Usuario):
    for usr in usuarios:
        if usr["id"] == usuario.get("id"):
            raise HTTPException(
                status_code=400, 
                  detail="el id ya existe"
            )
    usuarios.append(usuario)
    return{
        "nebsaje":"usuario agregado",
        "Usuario" :usuario,
        "status":"200"
    }
    
    #hacer put y delete de acuerdo a las funciones anteriores como "create"

#put se usa para actualizar 
#actualizar un usuario de la tabla de usuarios que tenemos arriba
#el usuario actualizado lo vamos a recibir en formato json y
#lo vamos a actualizar en la tabla de usuarios que tenemos arriba
@app.put("/v1/usuarios/",tags=['CRUD HTTP']) 
async def actualizar_usuarios(usuario:dict):
    for usr in usuarios:
        if usr["id"] == usuario.get("id"):
            usr.update(usuario)
            return{
                "mensaje":"usuario actualizado",
                "usuario":usr,
                "status":"200"
            }
    raise HTTPException(
        status_code=404,
        detail="usuario no encontrado"
    )
    
    
    
    #delete se usa para eliminar
    #eliminar un usuario de la tabla de usuarios que tenemos arriba
    #el usuario a eliminar lo vamos a recibir en formato json y
    #lo vamos a eliminar de la tabla de usuarios que tenemos arriba
@app.delete("/v1/usuarios/",tags=['CRUD HTTP']) 
#la funcion se llama eliminar_usuario y recibe un id de tipo entero
async def agregar_usuario(usuario:dict):
    for usr in usuarios:
        if usr["id"] == usuario.get("id"):
            usuarios.remove(usr)
            return{
                "mensaje":"usuario eliminado",
                "usuario":usr,
                "status":"200"
            }
    raise HTTPException(
        status_code=404,
        detail="usuario no encontrado"
    )
    