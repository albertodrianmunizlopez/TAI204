from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi import Depends, HTTPException, status
import secrets

security = HTTPBasic()

def verificar_peticion(credenciales: HTTPBasicCredentials = Depends(security)):
    usuario_ok = secrets.compare_digest(credenciales.username, "alberto")
    password_ok = secrets.compare_digest(credenciales.password, "123456")

    if not (usuario_ok and password_ok):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas"
        )

    return credenciales.username