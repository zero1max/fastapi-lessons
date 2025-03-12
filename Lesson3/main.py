from fastapi import FastAPI, Query
from .models import Item
from typing import Annotated
from pydantic import AfterValidator
import random

app = FastAPI()

# @app.post("/item/")
# async def create_item(item: Item):
#     return item

# @app.put("/item/{item_id}")
# async def update_item(item_id: int ,item: Item, q: str | None = None):
#     result = {"item_id" : item_id, **item.dict()}
#     if q:
#         result.update({"q": q})
#     return result

# ------------------------------------------------------------------

# @app.get("/items/")
# async def read_item(q: Annotated[str | None, Query(max_length=3)]):
#     results = {"item": [{"item": "foo"}, {"item": "bar"}]}
#     if q:
#         results.update({"q": q})
#     return results

# ------------------------------------------------------------------

# @app.get("/items/")
# async def read_item(q: Annotated[list[str] | None, Query()] = None):
#     query_items = {
#         "q": q
#     }
#     return query_items

# ------------------------------------------------------------------

# @app.get("/items/")
# async def read_item(q: Annotated[list[str], Query()] = ["Select", "Class"]):
#     query_items = {
#         "q": q
#     }
#     return query_items

# ------------------------------------------------------------------

# @app.get("/items/")
# async def read_items(
#     q: Annotated[
#         str | None,
#         Query(
#             alias="item-query",
#             title="Query string",
#             description="Query string for the items to search in the database that have a good match",
#             min_length=3,
#             max_length=50,
#             pattern="^fixedquery$",
#             deprecated=True,
#         ),
#     ] = None,
# ):
#     results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
#     if q:
#         results.update({"q": q})
#     return results

# ------------------------------------------------------------------

# @app.get("/items/")
# async def read_items(
#         hidden_query: Annotated[str | None, Query(include_in_schema=False)] = None,
# ):
#     if hidden_query:
#         return {"hidden_query": hidden_query}
#     else:
#         return {"hidden_query": "Not found"}
    
# ------------------------------------------------------------------

# data = {
#     "isbn-9781529046137": "The Hitchhiker's Guide to the Galaxy",
#     "imdb-tt0371724": "The Hitchhiker's Guide to the Galaxy",
#     "isbn-9781439512982": "Isaac Asimov: The Complete Stories, Vol. 2",
# }


# def check_valid_id(id: str):
#     if not id.startswith(("isbn-", "imdb-")):
#         raise ValueError('Invalid ID format, it must start with "isbn-" or "imdb-"')
#     return id


# @app.get("/items/")
# async def read_items(
#     id: Annotated[str | None, AfterValidator(check_valid_id)] = None,
# ):
#     if id:
#         item = data.get(id)
#     else:
#         id, item = random.choice(list(data.items()))
#     return {"id": id, "name": item}

# ------------------------------------------------------------------

# data = {
#     "pdp-1234": "Nigmatjonov Muhammadjon",
#     "pdp-12345": "Xasan Xoliqnazarov",
#     "pdp-123456": "Ali Alimov",
# }


# def check_valid_id(id: str):
#     if not id.startswith(("pdp-")):
#         raise ValueError('Invalid ID format, it must start with "pdp-"')
#     return id


# @app.get("/items/")
# async def read_items(
#     id: Annotated[str | None, AfterValidator(check_valid_id)] = None,
# ):
#     if id:
#         item = data.get(id)
#     else:
#         id, item = random.choice(list(data.items()))
#     return {"id": id, "name": item}