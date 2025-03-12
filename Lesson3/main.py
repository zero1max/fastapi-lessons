from fastapi import FastAPI
from .models import Item

app = FastAPI()

@app.post("/item/")
async def create_item(item: Item):
    return item

@app.put("/item/{item_id}")
async def update_item(item_id: int ,item: Item, q: str | None = None):
    result = {"item_id" : item_id, **item.dict()}
    if q:
        result.update({"q": q})
    return result