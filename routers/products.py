from fastapi import FastAPI, APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/product", tags= ["products"])

class product(BaseModel):
    id: int
    nombre:str
    marca:str


product_list =[product(id=1 , nombre="leche" , marca="colanta"),
               product(id=2, nombre= "pan", marca = "bimbo"),
               product(id=3, nombre="tv", marca="lg")]

@router.get("/")
async def get_products():
    return product_list

@router.get("/obtener_producto")
async def get_producs(id:int):
    try:
        product = filter(lambda product: product.id == id, product_list)
        return list(product)[0]
    except IndexError:
        raise HTTPException(status_code=404,detail="no existe el producto")
