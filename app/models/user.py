from pydantic import BaseModel,Field


class User(BaseModel):
    username: str
    fullname:str
    document: int
    cel: int
    hashed_password: str
    email: str


class buscarUsuario(BaseModel):
    email: str
    hashed_password :str



class UserDB(User):
    hashed_password: str