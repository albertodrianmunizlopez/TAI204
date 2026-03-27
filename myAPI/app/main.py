from fastapi import FastAPI
from app.routers import usuarios
from app.data.db import engine, Base

# Crear tablas en la BD
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(usuarios.router)