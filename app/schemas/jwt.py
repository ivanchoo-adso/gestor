from jwt import encode,decode,ExpiredSignatureError,DecodeError
from jose import jwt, JWTError
from datetime import datetime, timedelta
import os


SECRET = os.getenv("SECRET")
ALGORITH = os.getenv("ALGORITH")


async def tokenn(user: str, tiempo:int):
    vence= datetime.utcnow() + timedelta (hours=tiempo)
    crear={"sub": user, "exp": vence}
    token = jwt.encode(crear,SECRET,algorithm=ALGORITH)
    return{"token": token, "tipo":"bearer"}


def validarToken (token:str):
    try:
        data = decode(token, key="colombia", algorithm="HS256")
        return data
    except ExpiredSignatureError:
        return "Token vencido"
    except DecodeError:
        "Error con el token"