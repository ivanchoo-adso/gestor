from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from app.models.user import User,buscarUsuario
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.schemas.user import userdatos,buscarUsuarios,todosUsuarios
from app.schemas.jwt import tokenn
from jose import jwt, JWTError
from passlib.context import CryptContext
from app.schemas.encrypt import cifrada
from app.db.client import users
from bson import ObjectId
import os
from dotenv import load_dotenv

router = APIRouter(prefix="/userdb",
                   tags=["Usuarios "],
                   responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}})


load_dotenv()
oauth2 = OAuth2PasswordBearer(tokenUrl="login")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET = os.getenv("SECRET")
ALGORITH = os.getenv("ALGORITH")

@router.post("/crear/", response_model=User, status_code=status.HTTP_201_CREATED)
async def nuevoUsuario(user: User):
    
    for type in userdatos():
        if (type ["email"]==user.email):
            return JSONResponse(status_code=400,content=f"El usuario {{user.username}} ya existe ¡cambialo!")
    
    datos={"_id":str(ObjectId()),
           "username":user.username,
           "fullname":user.fullname,
           "document":user.document,
           "cel":user.cel,
           "password": cifrada(user.password),
           "email":user.email,
            } 
    
    users.insert_one(datos)
    return JSONResponse(status_code=201,content="Usuario creado")    


@router.get("/buscarUsuario/")
def getUser(email:str):
    return buscarUsuarios(email)

@router.get("/todosUsuarios/")
def getAllUser():
    return todosUsuarios()



@router.delete("/delete/", status_code=status.HTTP_204_NO_CONTENT)
async def user(email: str):

    for delete in userdatos():
        if delete ["email"]==email:
            users.delete_one({"email": email})
        return JSONResponse(f"El usuario {users.name} se elimino de la base de datos")
    return JSONResponse(status_code=404,content=f"El usuario con el {users} no fue encontrado")



@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends(OAuth2PasswordRequestForm)):
    
    user_list = userdatos()  
    user = next((usuario for usuario in user_list if usuario["username"] == form.username), None)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario no existe")
    
    if not crypt.verify(form.password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="La contraseña no es correcta")
    
    TOKEN_DURACION = 6
    print(user["id"])
    token = tokenn(user["id"],TOKEN_DURACION)
    return token, "Usuario ingresado con exito"



