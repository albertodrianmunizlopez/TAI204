
#Importaciones
from fastapi import FastAPI, status, HTTPException
from fastapi import FastAPI, status, HTTPException, Depends   #Depends: Seguridad de los endpoints 
import asyncio
from typing import Optional
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from fastapi.security import HTTPBasic, HTTPBasicCredentials  #Importamos las dependencias de estas dos 
import secrets#Genral de python la compracion y acciones dentro de la contraseña de los usuarios

Turnos = [

]

#=============================
# Sguridad con HTTP BASIC  
#=============================

security = HTTPBasic() #objeto security # Rutas protegidas por el usuario

def verificar_peticion(credenciales:HTTPBasicCredentials=Depends(security)):
    usuarioAut = secrets.compare_digest(credenciales.username,"banco")
    contraAuth = secrets.compare_digest(credenciales.password,"2468")

    if not(usuarioAut and contraAuth):
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Crdenciales no autorizadas"
        )
    
    return credenciales.username


# Datos cliente 

class cliente(BaseModel):
    id: int = Field(..., min_lenght=8 )
    tramite: int = Field(..., description="deposito/retiro/consulta")
    fecha: datetime = Field(..., description ="turno entre 9am y 3pm")
    turnos: int = Field(..., max_lenght = 5, description = "Maximo 5 ")

cliente = [
    {"id": 1, "nombre": "Diegosto","Tramite": "deposito"},
    {"id": 2, "nombre": "Coralhjt","Tramite": "deposito"},
    {"id": 3, "nombre": "saulygbj","Tramite": "Consulta"},
    {"id": 4, "nombre": "abceedrft","Tramite": "retiro"},
]
#End point 

#Crear usuarios 
app.post("/u1/Crearusuario") 
#Crear turnos post 

#listar turnos es un put

#Consultar id obligatorio 

#marcar como atendido put

#Eliminar  turno delete 
app.post("/v1/Eliminarturno")





