#seguridad con http 
#necesita un parametro para continuar necesita credenciales 

from  fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi import FastAPI, status, HTTPException,Depends
import secrets


security = HTTPBasic()

def verificar_peticion(credenciales: HTTPBasicCredentials = Depends(security)):

    usuarioAuth = secrets.compare_digest(credenciales.username, "alberto")
    contraAuth = secrets.compare_digest(credenciales.password, "123456")

    if not (usuarioAuth and contraAuth):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="credenciales no autorizadas"
        )

    return credenciales.username