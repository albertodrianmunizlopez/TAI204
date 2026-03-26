###crear modelo pydantic de validaciones
#aqui yaa tenemos nuestro modelo pydantic esto es solo paraa crear usuario
#para que pase la parte del pydantic necesita pasar la validacion de 
# los datos que recibimos en el endpoint de crear usuario

#agregamos importaciones 
from pydantic import BaseModel,Field

class crear_usuario(BaseModel):
    nombre:str= Field(...,min_length=3, max_length=50, example="Joohn Doe")
    edad:int=Field(...,gt=1,le=125,description="edad valida entre 1 y 125")