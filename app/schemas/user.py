from app.db.client import users
from typing import Optional


def userdatos(username: Optional[str] = None):
    resultado = []
    if username:
        for newUsuario in users.find():
            resultado.append({
                "username": newUsuario["username"],
                "fullname": newUsuario["fullname"],
                "document": newUsuario["document"],
                "cel": newUsuario["cel"],
                "hashed_password": newUsuario["hashed_password"],
                "email": newUsuario["email"]
            })
    return resultado


def buscarUsuarios(email:str):
    result=users.find({"email":email})
    for Usuario in result:
         resultado={
            "_id":Usuario["_id"],
            "username":Usuario["username"],
            "fullname":Usuario["fullname"],
            "document":Usuario["document"],
            "hashed_password":Usuario["hashed_password"],
            "cel":Usuario["cel"],
            "email":Usuario["email"]
        }
         
    return resultado

def todosUsuarios():
    resultado=[]
    result=users.find()
    for Usuario in result:
         resultado.append({
           "_id":Usuario["_id"],
            "username":Usuario["username"],
            "fullname":Usuario["fullname"],
            "document":Usuario["document"],
            "cel":Usuario["cel"],
            "email":Usuario["email"]
        })
    return resultado
    