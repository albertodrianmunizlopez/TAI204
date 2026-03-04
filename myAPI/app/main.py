#Importaciones
from fastapi import FastAPI, status, HTTPException, Depends   #Depends: Seguridad de los endpoints 
import asyncio
from typing import Optional
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from fastapi.security import HTTPBasic, HTTPBasicCredentials  #Importamos las dependencias de estas dos 
import secrets#Genral de python la compracion y acciones dentro de la contraseña de los usuarios


#Instancia del servidor
app = FastAPI(
    title="Mi Primer API",
    description="Muñiz Lopez Alberto Adrian ",
    version="1.0"
)

#TB ficticia usuarios
usuarios = [
    {"id": 1, "nombre": "Diego","edad": 21},
    {"id": 2, "nombre": "Coral","edad": 21},
    {"id": 3, "nombre": "saul","edad": 21}
]

#Tablas ficticias biblioteca
libros = []
prestamos = []

#=============================
# MODELOS USUARIOS GENERALES
#=============================

class crear_usuario(BaseModel):
    id: int = Field(..., gt=0, description="Identificador de usuario")
    nombre: str = Field(..., min_length=3, max_length=50, example="Juanito Doe")
    edad: int = Field(..., ge=1, le=125, description="Edad valida entre 1 y 125")

#=============================
# Sguridad con HTTP BASIC  
#=============================

security = HTTPBasic() #objeto security 

def verificar_peticion(credenciales:HTTPBasicCredentials=Depends(security)):# El parametro son las contraseñas 
    usuarioAut = secrets.compare_digest(credenciales.username,"Alberto")#Se crea el usuario el cual si tiene permisos 
    contraAuth = secrets.compare_digest(credenciales.password,"123456")#Se crea la contraseña el cual es la contraseña correcta

    if not(usuarioAut and contraAuth):
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Crdenciales no autorizadas"
        )
    
    return credenciales.username


#=============================
# ENDPOINTS GENERALES
#=============================

@app.get("/", tags=['Inicio'])
async def bienvenida():
    return {"mesaje": "Bienvenido a FastAPI"}

@app.get("/holaMundo", tags=['Asincronia'])
async def Hola():
    await asyncio.sleep(5)
    return {
        "mesaje": "Hola Mundo",
        "status": "200"
    }

@app.get("/v1/ParametroOb/{id}", tags=['Parametro obligatorio'])
async def consultauno(id:int):
    return {
        "mesaje": "Usuario encontrado",
        "usuario": id,
        "status": "200"
    }

@app.get("/v1/ParametroOp/", tags=['Parametro opcional'])
async def consultatodos(id:Optional[int] = None):
    if id is not None:
        for usuarioK in usuarios:
            if usuarioK["id"] == id:
                return {
                    "mesaje": "Usuario encontrado",
                    "usuario": usuarioK,
                    "status": "200"
                }
        return {"mesaje": "Usuario no encontrado", "status":"200"}
    else:
        return {"mesaje": "No se proporciono id", "status":"200"}

@app.get("/v1/usuarios/", tags=['CRUD HTTP'])
async def consultaT():
    return {
        "status":"200",
        "total": len(usuarios),
        "Usuarios":usuarios
    }

@app.post("/v1/usuarios/", tags=['CRUD HTTP'])
async def agregar_usuario(usuario:crear_usuario):
    for usr in usuarios:
        if usr["id"] == usuario.id:
            raise HTTPException(
                status_code=400,
                detail="El id ya existe"
            )
    usuarios.append(usuario.dict())
    return {
        "Mensaje":"Usuario agregado",
        "usuario": usuario,
        "status":"200"
    }

@app.put("/v1/usuarios/", tags=['CRUD HTTP'])
async def modificar_usuario(usuario:dict):
    for i, usr in enumerate(usuarios):
        if usr["id"] == usuario.get("id"):
            usuarios[i] = usuario
            return {
                "Mensaje":"Usuario modificado",
                "usuario": usuario,
                "status":"200"
            }
    raise HTTPException(
        status_code=404,
        detail="El id no existe"
    )

@app.delete("/v1/usuarios/{id}", tags=['CRUD HTTP'], status_code = status.HTTP_200_OK )
async def eliminar_usuario(id:int, usuarioAuth:str = Depends(verificar_peticion)):# verifica los datos del usuario con 
    global usuarios                                                               #permisos para eliminar 
    usuarios = [usr for usr in usuarios if usr["id"] != id]
    return {
        "Mensaje": f"Usuario eliminado por {usuarioAuth}", #La f es para que reconozca al usuario 
        "status":"200"
    }

#=================================================
#              API BIBLIOTECA DIGITAL
#=================================================

# Modelo Usuario Biblioteca
class Usuario(BaseModel):
    nombre: str = Field(..., min_length=3, max_length=50)
    correo: EmailStr

# Modelo Libro
class Libro(BaseModel):
    id: int = Field(..., gt=0)
    nombre: str = Field(..., min_length=2, max_length=100)
    autor: str = Field(..., min_length=3, max_length=100)
    anio: int = Field(..., gt=1450, le=datetime.now().year)
    paginas: int = Field(..., gt=1)
    estado: str = Field(..., pattern="^(disponible|prestado)$")

# Modelo Prestamo
class Prestamo(BaseModel):
    id: int = Field(..., gt=0)
    libro_id: int = Field(..., gt=0)
    usuario: Usuario

# a) Registrar libro
@app.post("/v1/libros/", status_code=201, tags=['Libros'])
async def registrar_libro(libro: Libro):

    for lb in libros:
        if lb["nombre"].lower() == libro.nombre.lower():
            raise HTTPException(
                status_code=400,
                detail="El nombre del libro ya existe"
            )

    libros.append(libro.dict())

    return {
        "Mensaje": "Libro registrado correctamente",
        "libro": libro,
        "status": "201"
    }

# b) Listar libros disponibles
@app.get("/v1/libros/disponibles", tags=['Libros'])
async def listar_disponibles():
    disponibles = [lb for lb in libros if lb["estado"] == "disponible"]
    return {
        "total": len(disponibles),
        "libros": disponibles,
        "status": "200"
    }

# c) Buscar libro por nombre
@app.get("/v1/libros/buscar/", tags=['Libros'])
async def buscar_libro(nombre: str):
    for lb in libros:
        if lb["nombre"].lower() == nombre.lower():
            return {
                "Libro encontrado": lb,
                "status": "200"
            }

    raise HTTPException(
        status_code=400,
        detail="Libro no encontrado"
    )

# d) Registrar préstamo
@app.post("/v1/prestamos/", tags=['Prestamos'])
async def registrar_prestamo(prestamo: Prestamo):

    for lb in libros:
        if lb["id"] == prestamo.libro_id:

            if lb["estado"] == "prestado":
                raise HTTPException(
                    status_code=409,
                    detail="El libro ya está prestado"
                )

            lb["estado"] = "prestado"
            prestamos.append(prestamo.dict())

            return {
                "Mensaje": "Prestamo registrado",
                "prestamo": prestamo,
                "status": "200"
            }

    raise HTTPException(
        status_code=400,
        detail="Libro no existe"
    )

# e) Devolver libro
@app.put("/v1/prestamos/devolver/{prestamo_id}", tags=['Prestamos'])
async def devolver_libro(prestamo_id: int):

    for i, pr in enumerate(prestamos):
        if pr["id"] == prestamo_id:

            for lb in libros:
                if lb["id"] == pr["libro_id"]:
                    lb["estado"] = "disponible"

            prestamos.pop(i)

            return {
                "Mensaje": "Libro devuelto correctamente",
                "status": "200"
            }

    raise HTTPException(
        status_code=409,
        detail="El registro de préstamo ya no existe"
    )

# f) Eliminar préstamo
@app.delete("/v1/prestamos/{prestamo_id}", tags=['Prestamos'])
async def eliminar_prestamo(prestamo_id: int):

    global prestamos
    prestamos = [pr for pr in prestamos if pr["id"] != prestamo_id]

    return {
        "Mensaje": "Prestamo eliminado",
        "status": "200"
    }