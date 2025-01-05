from fastapi import FastAPI,HTTPException, APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/user")

class user(BaseModel):
    id:int
    name: str
    age:int 
    city: str
    url:str

     

users_list =[user(id=1,name = "julian", age= 21,city="popayan",url="url/sdad"),
             user(id=2,name ="dsadas",age= 23,city="dsdsd", url="google.com"),
             user(id=3,name ="deasa", age=43, city="dsadas",url= "das")]


     
@router.get("/", status_code=200)
async def root():
    return users_list

@router.get("/{id}")
async def get_user(id:int):
    return search_user(id)

@router.post("/")
async def introduce_user(User:user):
        users_list.append(User)
        return {"mensaje": "se realizo correctamente"}

@router.put("/")
async def update_user(User: user):
    for index, existing_usuarios in enumerate(users_list):
        if existing_usuarios.id == User.id:
            users_list[index] = User
            return{"succesful":"se actualizo el usuario"}

    raise HTTPException(status_code=404, detail= "El id del usuario que colocaste no existe")

@router.delete("/")
async def delete_user(id:int):
    try:
        users_list.pop(id)
        return {"succes":"se elimino correctamente el usuario"}
    except IndexError:
        raise HTTPException(status_code=404, detail= "no se encontro el usuario")
    

def search_user(id: int):
    user_filter = filter(lambda user: user.id == id ,users_list)
    try:
        return list(user_filter)[0]
    except:
        raise HTTPException(status_code=404, detail= "no se encontro el usuario")
    

