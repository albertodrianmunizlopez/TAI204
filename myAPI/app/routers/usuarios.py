from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.data.db import get_db
from app.data.usuario import Usuarios as usuarioDB
from app.models.usuarios import crear_usuario, actualizar_usuario

router = APIRouter(
    prefix="/v1/usuarios",
    tags=["Usuarios"]
)

# GET TODOS
@router.get("/")
def obtener_usuarios(db: Session = Depends(get_db)):
    usuarios = db.query(usuarioDB).all()
    return usuarios


#  GET POR ID
@router.get("/{id}")
def obtener_usuario(id: int, db: Session = Depends(get_db)):
    usuario = db.query(usuarioDB).filter(usuarioDB.id == id).first()

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return usuario


#  POST
@router.post("/")
def crear(usuario: crear_usuario, db: Session = Depends(get_db)):
    nuevo = usuarioDB(nombre=usuario.nombre, edad=usuario.edad)

    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)

    return nuevo


#  PUT (actualiza todo)
@router.put("/{id}")
def actualizar(id: int, datos: crear_usuario, db: Session = Depends(get_db)):
    usuario = db.query(usuarioDB).filter(usuarioDB.id == id).first()

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    usuario.nombre = datos.nombre
    usuario.edad = datos.edad

    db.commit()
    db.refresh(usuario)

    return usuario


#  PATCH (actualización parcial)
@router.patch("/{id}")
def actualizar_parcial(id: int, datos: actualizar_usuario, db: Session = Depends(get_db)):
    usuario = db.query(usuarioDB).filter(usuarioDB.id == id).first()

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    if datos.nombre is not None:
        usuario.nombre = datos.nombre
    if datos.edad is not None:
        usuario.edad = datos.edad

    db.commit()
    db.refresh(usuario)

    return usuario


#  DELETE
@router.delete("/{id}")
def eliminar(id: int, db: Session = Depends(get_db)):
    usuario = db.query(usuarioDB).filter(usuarioDB.id == id).first()

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    db.delete(usuario)
    db.commit()

    return {"mensaje": "Usuario eliminado"}