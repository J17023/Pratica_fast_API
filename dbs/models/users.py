from pydantic import BaseModel

class User(BaseModel):
    _id : str | None
    username: str
    email: str