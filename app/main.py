from fastapi import FastAPI, HTTPException
from typing import List
from app.models import Item, ItemCreate

app = FastAPI(
    title="Tasks API",
    version="1.0.0"
)

items_db: List[Item] = []

@app.get("/")
def read_root():
     return {"message": "Bienvenido a la API de tareas!"}

@app.get("/items", response_model=List[Item])
def get_items():
     return items_db

@app.get("/items/{item_id}", response_model=Item)
def get_item(item_id: int):
    for item in items_db:
        if item.id == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item no encontrado")

@app.post("/items", response_model=Item)
def create_item(new_item: ItemCreate):
    next_id = len(items_db) + 1
    item = Item(id=next_id, **new_item.dict())
    items_db.append(item)
    return item

@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, updated_item: ItemCreate):
    for idx, item in enumerate(items_db):
        if item.id == item_id:
            items_db[idx] = Item(id=item_id, **updated_item.dict())
            return items_db[idx]
    raise HTTPException(status_code=404, detail="Item no encontrado")

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    for idx, item in enumerate(items_db):
        if item.id == item_id:
            del items_db[idx]
            return {"message": "Item eliminado"}
    raise HTTPException(status_code=404, detail="Item no encontrado")