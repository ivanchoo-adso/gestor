from pydantic import BaseModel,Field


class User(BaseModel):
    username: str
    fullname:str
    document: int
    cel: int
    password :str
    email: str


class buscarUsuario(BaseModel):
    email: str
    password :str