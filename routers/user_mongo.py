from fastapi import FastAPI,APIRouter,status,HTTPException
from dbs.client import database
from dbs.models.users import User
from dbs.schemas.user_schema import User_schema, Users_list
from bson.objectid import ObjectId
#router = APIRouter(prefix="/mongo", tags="Mongo")

app = FastAPI()

@app.post("/mongo",response_model=User,status_code= status.HTTP_201_CREATED)
async def ingresar_usuario(user: User):

    user_dict = dict(user)
    if "_id" in user_dict:
        del user_dict["_id"]
    
    user_id = database.local.users.insert_one(user_dict).inserted_id

    new_user = User_schema(database.local.users.find_one({"_id": user_id}))

    return User(**new_user)

@app.get("/user/me/{id}", response_model= User, status_code= status.HTTP_200_OK)
async def buscar_usuario(id:str):

    user = User_schema(database.local.users.find_one({"_id":ObjectId(id)}))
    return User(**user)

@app.get("/users",response_model= list[User], status_code= status.HTTP_200_OK)
async def get_users():
    users = Users_list(database.local.users.find())

    return users

@app.delete("/user/delete/{id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(id:str):

    found = database.local.users.find_one_and_delete({"_id": ObjectId(id)})
    if not found:
        HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                         detail="no se encontro el usuario")
        
@app.put("/user/update/{id}", response_model=User, status_code=status.HTTP_202_ACCEPTED)
async def update_user(id:str, new_user : User):
  

    new_user_dictionary = dict(new_user)
    if "_id" in new_user_dictionary:
        del new_user_dictionary["_id"]

    try:
        user_dict= User_schema(database.local.users.
                               find_one_and_update({"_id":ObjectId(id)},
                                                {"$set":new_user_dictionary}))
    except Exception as e:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED,
                            detail=f"No se pudo actualizar el usuario{str(e)}")
    

    user = User(**user_dict)
    return user




