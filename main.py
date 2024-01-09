from fastapi import FastAPI
from app.routes import user
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.include_router(user.router)

@app.get("/")
async def root():
    return "Hola FastAPI!"


# Inicia el server: uvicorn main:app --reload
# Detener el server: CTRL+C

# Documentación con Swagger: http://127.0.0.1:8000/docs
# Documentación con Redocly: http://127.0.0.1:8000/redoc
