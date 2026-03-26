from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base
import os
from sqlalchemy.orm import sessionmaker


#Definir URL de la conecxion

DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://admin:123456@postgres:5432/DB_miapi"
    )

#2 creamos motor de conexion
engine = create_engine(DATABASE_URL)

#3 creamos gestion de sesiones
SessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine)

#parte cuatro es base declarativa para los modelos
#ataravez de este objeto le daremos todas las propiedades para sql 

Base = declarative_base()

#5 funcion 
#que trabajara con als peticiones es una funcion publica llamada get db

def  get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()