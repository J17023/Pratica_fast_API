from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class user(BaseModel):
    id:int
    name: str
    age:int 
    city: str
    url:str

     

users_list =[user(id=1,name = "julian", age= 21,city="popayan",url="url/sdad"),
             user(id=2,name ="dsadas",age= 23,city="dsdsd", url="google.com"),
             user(id=3,name ="deasa", age=43, city="dsadas",url= "das")]


     
@app.get("/")
async def root():
    return users_list

@app.get("/user/{id}")
async def get_user(id:int):
    return search_user(id)

@app.post("/user/")
async def introduce_user(user:user):
        users_list.append(user)
        return {"mensaje": "se realizo correctamente"}

def search_user(id: int):
    user_filter = filter(lambda user: user.id == id ,users_list)
    try:
        return list(user_filter)[0]
    except:
        return {"error": "no se encontro el usuario"}
    

