
from fastapi import FastAPI, APIRouter
from pydantic import BaseModel
from routers import products, usuarios

app = FastAPI()

app.include_router(products.router)
app.include_router(usuarios.router)

@app.get("/")
async def ruta_inicial():
    return {"holaaa": "bienvenido"}

@app.get("/root/")
async def root():
    return{"ruta": "inicial"}