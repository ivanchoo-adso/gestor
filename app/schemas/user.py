from app.db.client import users

def userdatos():
    resultado=[]
    for newUsuario in users.find():
        resultado.append({
             "username":newUsuario["username"],
             "fullname":newUsuario["fullname"],
             "document":newUsuario["document"],
             "cel":newUsuario["cel"],
             "password":newUsuario["password"],
             "email":newUsuario["email"]
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
    