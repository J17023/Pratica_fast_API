
from fastapi import FastAPI
from routers import products, usuarios,autentificacion,autentificacion_jwt,user_mongo
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.include_router(products.router)
app.include_router(usuarios.router)
app.include_router(autentificacion_jwt.router)
app.include_router(autentificacion.router)
app.include_router(user_mongo.router)

app.mount("/resources",StaticFiles(directory="resources"), name="resources")

@app.get("/")
async def ruta_inicial():
    return {"holaaa": "bienvenido"}

@app.get("/root/")
async def root():
    return{"ruta": "inicial"}

