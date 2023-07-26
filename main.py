from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Union
import bson.objectid

app = FastAPI()


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
items_db = []


# Endpoint para crear un nuevo Item con un identificador único
@app.post("/items/", response_model=Item)
def create_item(item: Item):
    item_id = generate_unique_id()
    item_with_id = item.copy(update={"id": item_id})
    items_db.append(item_with_id)
    return item_with_id


# Endpoint para obtener todos los Items
@app.get("/items/", response_model=List[Item])
def read_items():
    return items_db


# Endpoint para obtener un Item por su identificador
@app.get("/items/{item_id}", response_model=Item)
def read_item(item_id: str):
    item = next((item for item in items_db if item.id == item_id), None)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


# Endpoint para actualizar un Item por su identificador
@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id: str, item: Item):
    item_index = next((index for index, item in enumerate(items_db) if item.id == item_id), None)
    if item_index is None:
        raise HTTPException(status_code=404, detail="Item not found")
    items_db[item_index] = item.model_copy(update={"id": item_id})
    return items_db[item_index]


# Endpoint para eliminar un Item por su identificador
@app.delete("/items/{item_id}", response_model=Item)
def delete_item(item_id: str):
    item_index = next((index for index, item in enumerate(items_db) if item.id == item_id), None)
    if item_index is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return items_db.pop(item_index)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
