
# ----------- Importaciones -----------
from fastapi import FastAPI, status, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime
import secrets

app = FastAPI(
    title="API Banco Turnos",
    description="API para gestionar turnos bancarios"
)



security = HTTPBasic()

def verificar_peticion(credenciales: HTTPBasicCredentials = Depends(security)):
    usuarioAut = secrets.compare_digest(credenciales.username, "banco")
    contraAuth = secrets.compare_digest(credenciales.password, "2468")

    if not (usuarioAut and contraAuth):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales no autorizadas"
        )

    return credenciales.username



# Datos cliente 

class Cliente(BaseModel):
    id: int = Field(..., description="ID del turno")
    nombre: str = Field(..., min_length=3, max_length=20)
    tramite: str = Field(..., description="deposito / retiro / consulta")
    fecha: datetime = Field(..., description="Fecha del turno")
    atendido: bool = False

#Tabla ficttcia de clientes 
cliente = [
    {"id": 1, "nombre": "Diegosto","Tramite": "deposito"},
    {"id": 2, "nombre": "Coralhjt","Tramite": "deposito"},
    {"id": 3, "nombre": "saulygbj","Tramite": "Consulta"},
    {"id": 4, "nombre": "abceedrft","Tramite": "retiro"},
]

turnos = [
    {"id": 1, "nombre": "Diego", "tramite": "deposito", "fecha": datetime.now(), "atendido": False},
    {"id": 2, "nombre": "Coral", "tramite": "deposito", "fecha": datetime.now(), "atendido": False},
    {"id": 3, "nombre": "Saul", "tramite": "consulta", "fecha": datetime.now(), "atendido": False},
    {"id": 4, "nombre": "Abel", "tramite": "retiro", "fecha": datetime.now(), "atendido": False},
]


#End points 


# Crear turno
@app.post("/v1/turnos", status_code=status.HTTP_201_CREATED)
def crear_turno(turno: Cliente, usuario: str = Depends(verificar_peticion)):
    turnos.append(turno.dict())
    return {
        "mensaje": "Turno creado correctamente",
        "turno": turno
    }



# Consultar turno por ID
@app.get("/v1/turnos/{id}")
def consultar_turno(id: int, usuario: str = Depends(verificar_peticion)):

    for turno in turnos:
        if turno["id"] == id:
            return turno

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Turno no encontrado"
    )



# Eliminar turno
@app.delete("/v1/turnos/{id}")
def eliminar_turno(id: int, usuario: str = Depends(verificar_peticion)):

    for turno in turnos:
        if turno["id"] == id:
            turnos.remove(turno)
            return {"mensaje": "Turno eliminado"}

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Turno no encontrado"
    )


# Listar turnos
@app.get("/v1/turnos")
def listar_turnos(usuario: str = Depends(verificar_peticion)):
    return turnos



# Marcar turno como atendido
@app.put("/v1/turnos/{id}/atender")
def atender_turno(id: int, usuario: str = Depends(verificar_peticion)):

    for turno in turnos:
        if turno["id"] == id:
            turno["atendido"] = True
            return {"mensaje": "Turno atendido", "turno": turno}

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Turno no encontrado"
    )



#docker build -t mi_api .
# docker run -d -p 8000:8000 --name api_contenedor mi_api
# docker compose up --build