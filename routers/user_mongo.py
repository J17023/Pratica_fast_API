from fastapi import FastAPI,APIRouter,status
from db.client import database
from db.models.users import User
from db.schemas.user_schema import User_schema
#router = APIRouter(prefix="/mongo", tags="Mongo")

app = FastAPI()

@app.post("/mongo",response_model=User,status_code= status.HTTP_201_CREATED)
async def ingresar_usuario(user: User):
    user_dict = dict(user)
    del user_dict["_id"]
    user_id = await database.local.users.insert_one(user_dict).inserted_id

    new_user = await User_schema(database.local.users.find_one({"_id": user_id}))

    return User(**new_user)
    
