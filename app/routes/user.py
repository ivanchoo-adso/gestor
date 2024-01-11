from fastapi import APIRouter, HTTPException, status, Depends,UploadFile, File
from fastapi.responses import JSONResponse
from app.models.user import User,buscarUsuario,UserDB
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.schemas.user import userdatos,buscarUsuarios,todosUsuarios
from app.schemas.jwt import tokenn
from jose import jwt, JWTError
from passlib.context import CryptContext
from app.schemas.encrypt import cifrada
from datetime import datetime, timedelta
from app.db.client import users
from bson import ObjectId
import os
import hashlib
from dotenv import load_dotenv
from PyPDF2 import PdfReader
import re
import io



router = APIRouter(prefix="/userdb",
                   tags=["Usuarios "],
                   responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}})


load_dotenv()
oauth2 = OAuth2PasswordBearer(tokenUrl="login")
crypt = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET = os.getenv("SECRET")
ALGORITH = os.getenv("ALGORITH")
ACCESS_TOKEN_DURATION = 1


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
           "hashed_password": get_password_hash(user.hashed_password),
           "email":user.email,
            } 
    
    users.insert_one(datos)
    return JSONResponse(status_code=201,content="Usuario creado")    



def search_user_db(username: str):
    users_list = userdatos()
    if any(user["username"] == username for user in users_list):
        return UserDB(**user)

# Resto del código...


def search_user(username: str):
    if username in userdatos:
        return User(**userdatos[username])



@router.get("/buscarUsuario/")
def getUser(email:str):
    return buscarUsuarios(email)

@router.get("/todosUsuarios/")
def getAllUser():
    return todosUsuarios()

def get_user(username: str):
    user_data = userdatos() 
    if any(user["username"] == username for user in user_data):
        return UserDB(user)


@router.delete("/delete/", status_code=status.HTTP_204_NO_CONTENT)
async def user(email: str):

    for delete in userdatos():
        if delete ["email"]==email:
            users.delete_one({"email": email})
        return JSONResponse(f"El usuario {users.name} se elimino de la base de datos")
    return JSONResponse(status_code=404,content=f"El usuario con el {users} no fue encontrado")



@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    # Función para buscar usuario
    user = users.find_one({"username":form.username})
    print(user["hashed_password"])
    # user_db = userdatos(form.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario no es correcto")

    # user = get_user(form.username)

    validate = crypt.verify(form.password, user["hashed_password"]) 
    if not validate:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="La contraseña no es correcta")

    access_token = {"sub": user["username"],
                    "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION)}

    return {"access_token": jwt.encode(access_token, SECRET, algorithm=ALGORITH), "token_type": "bearer"}


def get_password_hash(password):
    # Usar la función de CryptContext para obtener el hash de la contraseña
    return crypt.hash(password)



@router.post("/extract-cedula/")
async def extract_identification(file: UploadFile = File(...)):
    content = await file.read()
    
    # Usar PdfReader en lugar de PdfFileReader
    reader = PdfReader(io.BytesIO(content))

    identification_number = ""
    for page in reader.pages:
        page_text = page.extract_text()
        
        match = re.search(r'Id: (\d+)', page_text)
        if match:
            identification_number = match.group(1)
            break

    return {"identification_number": identification_number}


