from fastapi import FastAPI, status, HTTPException,Depends,APIRouter
#importar la base de datos 
from app.data.database import usuarios
#importar el modelo de datos en este caso la clase de crear usuario
from app.models.usuarios import crear_usuario

#seguridad importamos 
from app.security.auth import verificar_peticion
from typing import Optional

#creamos importaciones 

from sqlalchemy.orm import Session
from app.data.db import get_db
from app.data.usuario import Usuarios as usuarioDB


#ahora vamos a arreglar la parte del error de app para ello vamos a hacer lo siguiente 
# no creamos una instancia del servidor lo que aremos es poner una aapi router paaraa que este pongaa un
# listado de tododos los anpoints dospinibles 

router = APIRouter(
    prefix="/v1/usuarios", 
    tags=["CRUD HTTP"]
)

#le decimos al servidor que tenemos unos enpitns disponibles
#dentro del api router vamos a definir el primer palamrtro como prefigo 
#el app se repite en toas ls rutas y se repite lo de /v1/usuarioeste sera nuestro prefijo



@router.get("/")
async def consultaT(db: Session = Depends(get_db)):
    querryUsuario = db.query(usuarioDB).all()
   
    return{
      
        "status":"200",
        "total": len(querryUsuario),
        "usuarios":querryUsuario

          
    }
    


@router.post("/")  
async def agregar_usuario(usuarioP: crear_usuario, db: Session = Depends(get_db)):
    usuarioNuevo = usuarioDB(nombre=usuarioP.nombre, edad=usuarioP.edad)
    db.add(usuarioNuevo)
    db.commit()
    db.refresh(usuarioNuevo)
    
    return{
        "mensaje":"usuario agregado",
        "Usuario": usuarioNuevo,
        "status":"200"
    }
    
  
@router.put("/") 
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
    
 
    
    
@router.delete("/{id}")
async def eliminar_usuario(id: int, usuarioAuth: str = Depends(verificar_peticion)):

    for usr in usuarios:
        if usr["id"] == id:
            usuarios.remove(usr)
            return {
                "mensaje": f"usuario eliminado por {usuarioAuth}",
                "status": 200
            }

    raise HTTPException(
        status_code=404,
        detail="usuario no encontrado"
    )
    