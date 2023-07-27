from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Union
import bson.objectid

router = APIRouter(
    prefix="/items",
    tags=["items"],
    responses={404: {"description": "Not found"}},
)


# Función para generar identificador único similar a ObjectId de MongoDB
def generate_unique_id():
    return str(bson.objectid.ObjectId())


# Modelo Pydantic para el objeto Item
class Item(BaseModel):
    id: str = None
    name: str
    price: float
    quantity: Union[int, None] = None


# Lista de items en memoria (simulando una base de datos)
items_db = [
    Item(id="64c2d457b78bf61d46c7824f", name="MacBook Pro", price=7499.01, quantity=None),
    Item(id="64c2d4fbb78bf61d46c78250", name="Nike Air Max 270", price=949, quantity=8),
  ]


# Endpoint para crear un nuevo Item con un identificador único
@router.post("/items/", response_model=Item)
async def create_item(item: Item):
    item_id = generate_unique_id()
    item_with_id = item.model_copy(update={"id": item_id})
    items_db.append(item_with_id)
    return item_with_id


# Endpoint para obtener todos los Items
@router.get("/items/", response_model=List[Item])
async def read_items():
    return items_db


# Endpoint para obtener un Item por su identificador
@router.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: str):
    item = next((item for item in items_db if item.id == item_id), None)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.get("/items/saludo/")
async def read_items_saludo():
    print("INGRESO A RUTA SALUDO")
    return {"saludo": "otro get"}


# Endpoint para actualizar un Item por su identificador
@router.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: str, item: Item):
    item_index = next((index for index, item in enumerate(items_db) if item.id == item_id), None)
    if item_index is None:
        raise HTTPException(status_code=404, detail="Item not found")
    items_db[item_index] = item.model_copy(update={"id": item_id})
    return items_db[item_index]


# Endpoint para eliminar un Item por su identificador
@router.delete("/items/{item_id}", response_model=Item)
async def delete_item(item_id: str):
    item_index = next((index for index, item in enumerate(items_db) if item.id == item_id), None)
    if item_index is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return items_db.pop(item_index)


