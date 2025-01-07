
from fastapi import FastAPI, APIRouter
from pydantic import BaseModel
from routers import products, usuarios
from fastapi.staticfiles import StaticFiles

app = FastAPI()



app.include_router(products.router)
app.include_router(usuarios.router)

app.mount("/resources",StaticFiles(directory="resources"), name="resources")

@app.get("/")
async def ruta_inicial():
    return {"holaaa": "bienvenido"}

@app.get("/root/")
async def root():
    return{"ruta": "inicial"}

