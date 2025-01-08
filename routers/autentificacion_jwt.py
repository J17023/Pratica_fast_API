from datetime import timedelta,datetime, timezone
from typing import Annotated


from fastapi import FastAPI, Depends, status,HTTPException
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordRequestForm, OAuth2AuthorizationCodeBearer
import jwt
from passlib.context import CryptContext

# Cantidad de minutos en los que expira el token 
ACCESS_TOKEN_TIME= 15
#algoritmo de la encriptacion 
ALGORITHM = "HS256"

#varialbe de secreto 
SECRET_KEY= "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"

#iniciacion de fasAPI
app = FastAPI()

#Gestion del algoritmo de encriptacion
pwd_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")

class Token(BaseModel): 
    access_token:str
    token_type:str

class Data_token(Token):
    username:str

class User(BaseModel):
    username: str
    email : str
    disabled: bool = False

class User_database(User):
    hashed_password: str

fake_database = {
    "julian" : {
        "username" : "julian",
        "email" : "google@gmail.com",
        "disabled" : False,
        "hashed_password" : pwd_context.hash("123456")
    },
    "jose" :{
        "username" : "jose",
        "email" : "outlook@gmail.com",
        "disabled" : False,
        "hashed_password":pwd_context.hash("654321")
    }
}

def verify_password(typed_password:str,hashed_password:str):
    return pwd_context.verify(typed_password, hashed_password)

def get_user(db, username:str):
    if username in db:
        user_dictionary = db.get(username)
        return User_database(**user_dictionary)
        
def authenticate_user(database, username:str, password:str):
    user = get_user(database,username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def encryptated_token(data:dict, time_expired:timedelta | None=None):
    to_encode = data.copy()
    if time_expired:
        expiration_time = datetime.now(timezone.utc) + time_expired
    else:
        expiration_time = datetime.now(timezone.utc) +timedelta(minutes=15)

    to_encode.update({"exp": expiration_time})

    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,ALGORITHM)
    return encoded_jwt


@app.post("/login/")
async def busqueda_usuarios(form: Annotated[OAuth2PasswordRequestForm, Depends()]):
    
    user = authenticate_user(fake_database,form.username,form.password)

    if not user: 
        raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, 
                            detail="usuario o contraseña incorrectos")

    access_token_time = timedelta(minutes= ACCESS_TOKEN_TIME)

    token = encryptated_token({"sup": user.username}, access_token_time)

    return Token(access_token= token, token_type= "Bearer")


