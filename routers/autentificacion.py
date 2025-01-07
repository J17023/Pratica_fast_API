from fastapi import FastAPI, APIRouter,Depends,HTTPException,status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from typing import  Annotated

# Crear instancia de FastAPI
app = FastAPI()

# Configuración de autenticación OAuth2
oauth= OAuth2PasswordBearer(tokenUrl="login")

# Modelos de usuario
class User(BaseModel):
    id: str
    username : str
    email: str
    disabled: bool = False

class User_db(User):
    password:str

# Base de datos simulada
Users_DataBase ={
    "julian" : {
        "id" : "1",
        "username": "J1723",
        "email":"google@gmail.com",
        "disabled": False,
        "password" : "1234567"
    },

    "jose":{
        "id" : "2",
        "username": "drepredador",
        "email":"microsoft@gmail.com",
        "disabled": False,
        "password" : "7654321"  
    }
}

# Función para buscar un usuario en la base de datos
def search_user(username: str):
    if username in Users_DataBase:
        return User(**Users_DataBase[username])

# Endpoint de inicio de sesión
@app.post("/login/")
async def login(form: Annotated[OAuth2PasswordRequestForm,Depends()]):
    user_dict = Users_DataBase.get(form.username)
    if not user_dict:
        raise HTTPException(status_code=404, 
                            detail="No se encontro el usuario en la base de datos")
    user = User_db(**user_dict)
    password_entered = form.password

    if password_entered != user.password:
        raise HTTPException(status_code=404, detail = "no coincide el usuario o la contraseña")

    return {"access-token": user.username, "token-type":"bearer"}

# Dependencia para obtener el usuario actual
async def current_user(token : Annotated[str,Depends(oauth)]):
    user= search_user(token)
    if not user:
        raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED,
                            detail="No se encontro el usuario ingresado",
                            headers= {"WWW-Authenticate":"Bearer"})
    return user

# Endpoint para obtener información del usuario actual
@app.get("/user/me")
async def get_user(user: Annotated[User,Depends(current_user)]):
    return user


