from fastapi import FastAPI
from app.routers import usuarios, varios

app = FastAPI()

app.include_router(usuarios.router)
app.include_router(varios.routerV)